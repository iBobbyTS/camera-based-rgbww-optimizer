from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Mapping


EXHAUSTIBILITY_MATRIX = {
    "logical.initial": {"sub_budget": "initial", "trigger_point": "capture.consume", "classification": "guarded_unreachable", "origin": "logical_start", "counter_scope": "start", "capture_attempted": False, "formal_status": "not_emitted", "phase_pattern": r"^initial$"},
    "logical.initial_probes": {"sub_budget": "initial_probes", "trigger_point": "reserve_or_consume_initial_probes", "classification": "guarded_unreachable", "origin": "logical_start", "counter_scope": "start", "capture_attempted": False, "formal_status": "not_emitted", "phase_pattern": r"^probe(?:-.*)?$"},
    "logical.feedback_attempts": {"sub_budget": "feedback_attempts", "trigger_point": "feedback_backtrack_consume", "classification": "production_reachable", "origin": "logical_start", "counter_scope": "start", "capture_attempted": False, "formal_status": "solver_budget_exhausted", "phase_pattern": r"^feedback-\d+(?:-backtrack-(?:0\.5|0\.25))?$"},
    "logical.rebase_probes": {"sub_budget": "rebase_probes", "trigger_point": "reserve_or_consume_rebase_probes", "classification": "guarded_unreachable", "origin": "logical_start", "counter_scope": "start", "capture_attempted": False, "formal_status": "not_emitted", "phase_pattern": r"^(?:prediction|thermal)-rebase-\d+(?:-.*)?$"},
    "logical.confirmation_captures": {"sub_budget": "confirmation_captures", "trigger_point": "confirmation_capture_consume", "classification": "guarded_unreachable", "origin": "logical_start", "counter_scope": "start", "capture_attempted": False, "formal_status": "not_emitted", "phase_pattern": r"^confirm-\d+-\d+$"},
    "logical.confirmation_groups": {"sub_budget": "confirmation_groups", "trigger_point": "confirmation_group_reservation", "classification": "production_reachable", "origin": "logical_start", "counter_scope": "start", "capture_attempted": False, "formal_status": "solver_budget_exhausted", "phase_pattern": r"^confirm-\d+$"},
    "logical.rebases": {"sub_budget": "rebases", "trigger_point": "rebase_group_reservation", "classification": "guarded_unreachable", "origin": "logical_start", "counter_scope": "start", "capture_attempted": False, "formal_status": "not_emitted", "phase_pattern": r"^(?:prediction|thermal)-rebase-\d+$"},
    "logical.total": {"sub_budget": "logical_observations", "trigger_point": "logical_total_consume_or_reserve", "classification": "guarded_unreachable", "origin": "logical_start", "counter_scope": "start", "capture_attempted": False, "formal_status": "not_emitted", "phase_pattern": r"^(?:initial|probe|feedback|confirm|(?:prediction|thermal)-rebase)(?:-.*)?$"},
    "physical.pre_capture_denial": {"sub_budget": "physical_cr3", "trigger_point": "capture_source_remaining_precheck", "classification": "guarded_unreachable", "origin": "physical_target", "counter_scope": "target", "capture_attempted": False, "formal_status": "not_emitted", "phase_pattern": r"^[a-z0-9][a-z0-9_.-]*$"},
    "physical.post_capture_overrun": {"sub_budget": "physical_cr3", "trigger_point": "physical_budget_record_after_capture", "classification": "fatal_accounting_error", "origin": "physical_target", "counter_scope": "target", "capture_attempted": True, "formal_status": "physical_budget_accounting_violation", "phase_pattern": r"^[a-z0-9][a-z0-9_.-]*$"},
    "physical.autoexposure_overrun": {"sub_budget": "autoexposure", "trigger_point": "physical_budget_record_after_capture", "classification": "fatal_accounting_error", "origin": "physical_target", "counter_scope": "target", "capture_attempted": True, "formal_status": "physical_budget_accounting_violation", "phase_pattern": r"^[a-z0-9][a-z0-9_.-]*$"},
    "physical.weak_reacquire": {"sub_budget": "weak_reacquire", "trigger_point": "allow_weak_reacquire_precheck", "classification": "guarded_unreachable", "origin": "physical_target", "counter_scope": "target", "capture_attempted": False, "formal_status": "not_emitted", "phase_pattern": r"^[a-z0-9][a-z0-9_.-]*$"},
    "physical.weak_reacquire_overrun": {"sub_budget": "weak_reacquire", "trigger_point": "physical_budget_record_after_capture", "classification": "fatal_accounting_error", "origin": "physical_target", "counter_scope": "target", "capture_attempted": True, "formal_status": "physical_budget_accounting_violation", "phase_pattern": r"^[a-z0-9][a-z0-9_.-]*$"},
}


def match_exhaustibility_path(
    *, sub_budget: str, origin: str, counter_scope: str,
    capture_attempted: bool, phase: str, formal_status: str | None = None,
) -> tuple[str, Mapping[str, Any]]:
    matches = [
        (path_id, contract)
        for path_id, contract in EXHAUSTIBILITY_MATRIX.items()
        if contract["sub_budget"] == sub_budget
        and contract["origin"] == origin
        and contract["counter_scope"] == counter_scope
        and contract["capture_attempted"] is capture_attempted
        and (formal_status is None or contract["formal_status"] == formal_status)
        and re.fullmatch(str(contract["phase_pattern"]), phase) is not None
    ]
    if len(matches) != 1:
        raise ValueError("exhaustion evidence does not match exactly one frozen path")
    return matches[0]


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
