from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class HsiSolverBudgetLimits:
    max_starts: int = 2
    feedback_attempts_per_start: int = 8
    confirmation_groups_per_start: int = 2
    confirmations_per_group: int = 3
    rebase_count_per_start: int = 2
    probe_count: int = 4
    autoexposure_physical_captures_per_target: int = 10
    weak_signal_reacquire_physical_captures_per_target: int = 4

    def __post_init__(self) -> None:
        values = (
            self.max_starts,
            self.feedback_attempts_per_start,
            self.confirmation_groups_per_start,
            self.confirmations_per_group,
            self.probe_count,
            self.autoexposure_physical_captures_per_target,
        )
        if any(value < 1 for value in values) or self.rebase_count_per_start < 0:
            raise ValueError("HSI solver budget limits must be positive")
        if self.confirmations_per_group not in {3, 5}:
            raise ValueError("HSI confirmation groups must contain exactly 3 or 5 captures")

    @property
    def logical_per_start(self) -> int:
        return (
            1
            + self.probe_count
            + self.feedback_attempts_per_start
            + self.rebase_count_per_start * self.probe_count
            + self.confirmation_groups_per_start * self.confirmations_per_group
        )

    @property
    def logical_per_target(self) -> int:
        return self.max_starts * self.logical_per_start

    @property
    def physical_per_target(self) -> int:
        return (
            self.logical_per_target
            + self.autoexposure_physical_captures_per_target
            - 1
            + self.weak_signal_reacquire_physical_captures_per_target
        )

    def to_jsonable(self) -> dict[str, int]:
        return {
            "max_starts": self.max_starts,
            "max_feedback_capture_attempts_per_start": self.feedback_attempts_per_start,
            "max_confirmation_groups_per_start": self.confirmation_groups_per_start,
            "confirmation_captures_per_group": self.confirmations_per_group,
            "max_rebases_per_start": self.rebase_count_per_start,
            "rebase_probe_count": self.probe_count,
            "max_autoexposure_physical_captures_per_target": self.autoexposure_physical_captures_per_target,
            "max_weak_signal_reacquire_physical_captures_per_target": self.weak_signal_reacquire_physical_captures_per_target,
            "max_logical_observations_per_start": self.logical_per_start,
            "max_logical_observations_per_target": self.logical_per_target,
            "max_physical_cr3_per_target": self.physical_per_target,
        }


@dataclass
class HsiStartBudget:
    limits: HsiSolverBudgetLimits
    start_index: int
    consumed: dict[str, int] = field(default_factory=lambda: {
        "initial": 0,
        "initial_probes": 0,
        "feedback_attempts": 0,
        "rebase_probes": 0,
        "confirmation_captures": 0,
    })
    confirmation_groups_started: int = 0
    rebases_started: int = 0
    exhaustion: dict[str, Any] | None = None

    @property
    def logical_used(self) -> int:
        return sum(self.consumed.values())

    def reserve_confirmation_group(self, *, phase: str) -> bool:
        if self.confirmation_groups_started >= self.limits.confirmation_groups_per_start:
            return self._exhaust(phase, "confirmation_groups")
        remaining = self.limits.logical_per_start - self.logical_used
        if remaining < self.limits.confirmations_per_group:
            return self._exhaust(phase, "logical_observations")
        self.confirmation_groups_started += 1
        return True

    def reserve_probe_group(self, *, phase: str, rebase: bool) -> bool:
        if rebase:
            if self.rebases_started >= self.limits.rebase_count_per_start:
                return self._exhaust(phase, "rebases")
            self.rebases_started += 1
        category = "rebase_probes" if rebase else "initial_probes"
        maximum = (
            self.limits.rebase_count_per_start * self.limits.probe_count
            if rebase else self.limits.probe_count
        )
        if self.consumed[category] + self.limits.probe_count > maximum:
            return self._exhaust(phase, category)
        if self.limits.logical_per_start - self.logical_used < self.limits.probe_count:
            return self._exhaust(phase, "logical_observations")
        return True

    def consume(self, *, phase: str) -> bool:
        category, maximum = self._category_and_limit(phase)
        if self.consumed[category] >= maximum:
            return self._exhaust(phase, category)
        if self.logical_used >= self.limits.logical_per_start:
            return self._exhaust(phase, "logical_observations")
        self.consumed[category] += 1
        return True

    def _category_and_limit(self, phase: str) -> tuple[str, int]:
        if phase == "initial":
            return "initial", 1
        if phase.startswith("probe-"):
            return "initial_probes", self.limits.probe_count
        if "rebase-" in phase:
            return "rebase_probes", self.limits.rebase_count_per_start * self.limits.probe_count
        if phase.startswith("confirm-"):
            return (
                "confirmation_captures",
                self.limits.confirmation_groups_per_start * self.limits.confirmations_per_group,
            )
        if phase.startswith("feedback-"):
            return "feedback_attempts", self.limits.feedback_attempts_per_start
        raise ValueError(f"unclassified HSI logical observation phase: {phase}")

    def _exhaust(self, phase: str, sub_budget: str) -> bool:
        self.exhaustion = {
            "status": "solver_budget_exhausted",
            "start_index": self.start_index,
            "phase": phase,
            "sub_budget": sub_budget,
        }
        return False

    def to_jsonable(self) -> dict[str, Any]:
        return {
            "start_index": self.start_index,
            "limits": self.limits.to_jsonable(),
            "consumed": dict(self.consumed),
            "logical_observations_used": self.logical_used,
            "confirmation_groups_started": self.confirmation_groups_started,
            "rebases_started": self.rebases_started,
            "exhaustion": None if self.exhaustion is None else dict(self.exhaustion),
        }


@dataclass
class HsiPhysicalBudget:
    hard_cap: int
    autoexposure_cap: int
    weak_reacquire_cap: int
    physical_used: int = 0
    autoexposure_used: int = 0
    weak_reacquire_used: int = 0
    events: list[dict[str, Any]] = field(default_factory=list)

    def remaining(self) -> int:
        return self.hard_cap - self.physical_used

    def allow_weak_reacquire(self) -> bool:
        return self.weak_reacquire_used < self.weak_reacquire_cap and self.remaining() > 0

    def record(
        self, *, phase: str, physical_count: int, auto_exposure: bool,
        weak_reacquire: bool,
    ) -> None:
        if physical_count < 1:
            raise ValueError("physical capture accounting requires at least one CR3")
        new_total = self.physical_used + physical_count
        if new_total > self.hard_cap:
            raise HsiPhysicalBudgetExhausted(self.evidence(phase=phase, requested=physical_count))
        if auto_exposure and self.autoexposure_used + physical_count > self.autoexposure_cap:
            raise HsiPhysicalBudgetExhausted(self.evidence(phase=phase, requested=physical_count, sub_budget="autoexposure"))
        if weak_reacquire and self.weak_reacquire_used + physical_count > self.weak_reacquire_cap:
            raise HsiPhysicalBudgetExhausted(self.evidence(phase=phase, requested=physical_count, sub_budget="weak_reacquire"))
        self.physical_used = new_total
        if auto_exposure:
            self.autoexposure_used += physical_count
        if weak_reacquire:
            self.weak_reacquire_used += physical_count
        self.events.append({
            "phase": phase,
            "physical_cr3": physical_count,
            "auto_exposure": auto_exposure,
            "weak_reacquire": weak_reacquire,
        })

    def evidence(
        self, *, phase: str, requested: int = 0, sub_budget: str = "physical_cr3",
    ) -> dict[str, Any]:
        return {
            "status": "solver_budget_exhausted",
            "phase": phase,
            "sub_budget": sub_budget,
            "requested_physical_cr3": requested,
            "hard_cap": self.hard_cap,
            "physical_cr3_used": self.physical_used,
            "autoexposure_cap": self.autoexposure_cap,
            "autoexposure_physical_cr3_used": self.autoexposure_used,
            "weak_reacquire_cap": self.weak_reacquire_cap,
            "weak_reacquire_physical_cr3_used": self.weak_reacquire_used,
        }

    def to_jsonable(self) -> dict[str, Any]:
        return {**self.evidence(phase="complete"), "events": list(self.events)}


class HsiPhysicalBudgetExhausted(RuntimeError):
    def __init__(self, evidence: Mapping[str, Any]):
        super().__init__("HSI physical CR3 budget exhausted")
        self.evidence = dict(evidence)
