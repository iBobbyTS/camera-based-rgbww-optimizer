from __future__ import annotations

import unittest

from camera_based_rgbww_optimizer.optimization.hsi_budget import (
    HsiPhysicalBudget,
    HsiPhysicalBudgetExhausted,
    HsiSolverBudgetLimits,
    HsiStartBudget,
)


class HsiBudgetTests(unittest.TestCase):
    def test_planner_caps_are_exact_for_n3_and_n5(self):
        ordinary = HsiSolverBudgetLimits(confirmations_per_group=3)
        boundary = HsiSolverBudgetLimits(confirmations_per_group=5)
        self.assertEqual((ordinary.logical_per_start, ordinary.logical_per_target, ordinary.physical_per_target), (27, 54, 67))
        self.assertEqual((boundary.logical_per_start, boundary.logical_per_target, boundary.physical_per_target), (31, 62, 75))

    def test_n3_exact_boundary_passes_and_one_over_is_structured(self):
        limits = HsiSolverBudgetLimits(confirmations_per_group=3)
        budget = HsiStartBudget(limits, start_index=0)
        self.assertTrue(budget.consume(phase="initial"))
        self.assertTrue(budget.reserve_probe_group(phase="probe", rebase=False))
        for channel in ("ww", "r", "g", "b"):
            self.assertTrue(budget.consume(phase=f"probe-{channel}"))
        for index in range(8):
            self.assertTrue(budget.consume(phase=f"feedback-{index}"))
        for rebase in range(2):
            self.assertTrue(budget.reserve_probe_group(phase=f"prediction-rebase-{rebase}", rebase=True))
            for channel in ("ww", "r", "g", "b"):
                self.assertTrue(budget.consume(phase=f"prediction-rebase-{rebase}-{channel}"))
        for group in range(2):
            self.assertTrue(budget.reserve_confirmation_group(phase=f"confirm-{group}"))
            for index in range(3):
                self.assertTrue(budget.consume(phase=f"confirm-{group}-{index}"))
        self.assertEqual(budget.logical_used, 27)
        self.assertFalse(budget.consume(phase="feedback-8"))
        self.assertEqual(budget.exhaustion["status"], "solver_budget_exhausted")

    def test_n5_exact_physical_boundary_and_one_over(self):
        limits = HsiSolverBudgetLimits(confirmations_per_group=5)
        budget = HsiPhysicalBudget(
            hard_cap=limits.physical_per_target,
            autoexposure_cap=10,
            weak_reacquire_cap=4,
        )
        budget.record(phase="initial", physical_count=10, auto_exposure=True, weak_reacquire=False)
        budget.record(phase="logical", physical_count=61, auto_exposure=False, weak_reacquire=False)
        budget.record(phase="weak", physical_count=4, auto_exposure=False, weak_reacquire=True)
        self.assertEqual(budget.physical_used, 75)
        with self.assertRaises(HsiPhysicalBudgetExhausted) as caught:
            budget.record(phase="one-over", physical_count=1, auto_exposure=False, weak_reacquire=False)
        self.assertEqual(caught.exception.evidence["physical_cr3_used"], 75)

    def test_rebase_is_all_or_none_and_backtracks_each_consume_attempt(self):
        limits = HsiSolverBudgetLimits(
            feedback_attempts_per_start=3,
            confirmation_groups_per_start=1,
            confirmations_per_group=3,
            rebase_count_per_start=1,
        )
        budget = HsiStartBudget(limits, start_index=1)
        self.assertTrue(budget.consume(phase="initial"))
        self.assertTrue(budget.reserve_probe_group(phase="probe", rebase=False))
        for channel in ("ww", "r", "g", "b"):
            budget.consume(phase=f"probe-{channel}")
        for phase in ("feedback-0", "feedback-0-backtrack-0.5", "feedback-0-backtrack-0.25"):
            self.assertTrue(budget.consume(phase=phase))
        self.assertFalse(budget.consume(phase="feedback-1"))
        self.assertEqual(budget.consumed["feedback_attempts"], 3)
        self.assertTrue(budget.reserve_probe_group(phase="prediction-rebase-0", rebase=True))
        self.assertFalse(budget.reserve_probe_group(phase="prediction-rebase-1", rebase=True))
        self.assertEqual(budget.consumed["rebase_probes"], 0)


if __name__ == "__main__":
    unittest.main()
