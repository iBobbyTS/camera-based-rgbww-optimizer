"""Behavior tests for the GUIDE12 N2 repeatability plan builders."""
from __future__ import annotations

import unittest

from camera_based_rgbww_optimizer.optimization.guide12_n2 import (
    N2_BURST_STATE_KEYS,
    N2_STATES,
    build_guide12_n2_hsi_ladder_plan,
    build_guide12_n2_session_plan,
)

HSI_SHUTTERS = {"ray-hsi-h0-s100": "1/2000", "ray-hsi-h240-s100": "1/2500"}


class Guide12N2SessionPlanTests(unittest.TestCase):
    def test_session_requires_ladder_frozen_hsi_shutters(self):
        with self.assertRaisesRegex(ValueError, "ray-hsi-h0-s100"):
            build_guide12_n2_session_plan(1)
        with self.assertRaisesRegex(ValueError, "ray-hsi-h240-s100"):
            build_guide12_n2_session_plan(
                1, hsi_ray_shutters={"ray-hsi-h0-s100": "1/2000"}
            )

    def test_session_index_out_of_design(self):
        with self.assertRaises(ValueError):
            build_guide12_n2_session_plan(4, hsi_ray_shutters=HSI_SHUTTERS)

    def test_session_frame_counts_match_frozen_design(self):
        for session_index in (1, 2, 3):
            plan = build_guide12_n2_session_plan(
                session_index, hsi_ray_shutters=HSI_SHUTTERS
            )
            formal = [c for c in plan["captures"] if c.get("capture_role") == "formal"]
            ambient = [c for c in plan["captures"] if c.get("capture_role") == "ambient"]
            expected_main = 6 * 2 * 2
            if session_index == 1:
                expected_main += len(N2_BURST_STATE_KEYS) * 2 * 2
            self.assertEqual(len(formal), expected_main, session_index)
            self.assertEqual(len(ambient), 4)
            self.assertEqual(plan["budgets"]["formal_cap"], len(formal))
            self.assertEqual(
                plan["budgets"]["physical_cr3_cap"], len(plan["captures"])
            )

    def _first_sources(self, plan, cycle):
        rows = [
            c for c in plan["captures"]
            if c.get("n2_state_key") == "white_1800_100"
            and c.get("n2_cycle_index") == cycle
            and c.get("n2_burst_role") in ("paired_cycle_main", "burst_main")
        ]
        return [c["source_id"] for c in rows]

    def test_order_reverses_within_session_and_rotates_across_sessions(self):
        plans = {
            s: build_guide12_n2_session_plan(s, hsi_ray_shutters=HSI_SHUTTERS)
            for s in (1, 2, 3)
        }
        for s in (1, 2, 3):
            self.assertNotEqual(
                self._first_sources(plans[s], 1),
                self._first_sources(plans[s], 2),
                f"session {s} cycles must reverse order",
            )
        self.assertNotEqual(
            self._first_sources(plans[1], 1), self._first_sources(plans[2], 1)
        )
        self.assertNotEqual(
            self._first_sources(plans[2], 1), self._first_sources(plans[3], 1)
        )
        self.assertEqual(
            self._first_sources(plans[1], 1), self._first_sources(plans[3], 1)
        )

    def test_bursts_share_fast_state_with_dwell_ladder(self):
        plan = build_guide12_n2_session_plan(1, hsi_ray_shutters=HSI_SHUTTERS)
        burst_rows = [
            c for c in plan["captures"]
            if str(c.get("n2_burst_role", "")).startswith("burst")
        ]
        self.assertEqual(len(burst_rows), 3 * 2 * 3)
        by_state = {}
        for row in burst_rows:
            by_state.setdefault(row["state_id"], []).append(row)
        for rows in by_state.values():
            elapsed = sorted(r["requested_elapsed_s"] for r in rows)
            self.assertEqual(elapsed, [120, 140.0, 160.0])
        plain = [
            c for c in plan["captures"]
            if c.get("n2_state_key") in N2_BURST_STATE_KEYS
            and c.get("n2_cycle_index") == 2
        ]
        self.assertTrue(
            all(c.get("n2_burst_role") == "paired_cycle_main" for c in plain)
        )

    def test_every_observation_is_its_own_fast_state_except_bursts(self):
        plan = build_guide12_n2_session_plan(1, hsi_ray_shutters=HSI_SHUTTERS)
        formal = [c for c in plan["captures"] if c.get("capture_role") == "formal"]
        burst_states = {
            c["state_id"] for c in formal
            if str(c.get("n2_burst_role", "")).startswith("burst")
        }
        non_burst = [
            c["state_id"] for c in formal if c["state_id"] not in burst_states
        ]
        self.assertEqual(len(non_burst), len(set(non_burst)))

    def test_all_six_strip_commands_are_actual_fullscale(self):
        for state in N2_STATES:
            self.assertEqual(max(state["strip_command"].values()), 4095, state["key"])

    def test_hsi_ray_commands_carry_hue_sat_and_white_carry_cct(self):
        plan = build_guide12_n2_session_plan(2, hsi_ray_shutters=HSI_SHUTTERS)
        ray_steps = [c for c in plan["captures"] if c["source_id"] == "ray"]
        by_state = {c["n2_state_key"]: c["command"] for c in ray_steps}
        self.assertEqual(
            by_state["white_3200_0"],
            {"mode": "cct", "cct": 3200, "gm": 0, "intensity_percent": 100.0},
        )
        self.assertEqual(
            by_state["color_red"],
            {"mode": "hsi", "hue": 0, "sat": 100, "intensity_percent": 100.0},
        )
        self.assertEqual(by_state["color_blue"]["hue"], 240)

    def test_shutter_ledger_is_frozen_and_complete(self):
        plan = build_guide12_n2_session_plan(1, hsi_ray_shutters=HSI_SHUTTERS)
        frozen = plan["frozen_shutters"]
        self.assertEqual(frozen["n2-ray-hsi-h0-s100"], "1/2000")
        self.assertEqual(frozen["n2-strip-color_blue"], "1/320")
        for step in plan["captures"]:
            if step.get("capture_role") == "formal":
                self.assertEqual(
                    frozen[step["exposure_cache_key"]], step["nominal_shutter"]
                )
        self.assertEqual(
            plan["execution_authorization"]["schema"],
            "direct_guide12_n2_repeatability_v1",
        )

    def test_ambient_policy_matches_ambient_frames(self):
        from camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation import (
            AMBIENT_POLICY_UNSUBTRACTED_WITH_ALL_OFF_DIAGNOSTIC,
        )
        for session in (1, 2, 3):
            plan = build_guide12_n2_session_plan(
                session, hsi_ray_shutters=HSI_SHUTTERS
            )
            self.assertEqual(
                plan["native_raw_ambient_policy"],
                AMBIENT_POLICY_UNSUBTRACTED_WITH_ALL_OFF_DIAGNOSTIC,
            )
            ambient_count = sum(
                1 for c in plan["captures"]
                if c.get("capture_role") == "ambient"
            )
            self.assertEqual(ambient_count, 4)
            self.assertEqual(plan["budgets"]["ambient_cap"], ambient_count)

    def test_predicted_raw_max_ceiling_is_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "pre-check ceiling"):
            build_guide12_n2_session_plan(
                1,
                hsi_ray_shutters=HSI_SHUTTERS,
                predicted_raw_max={"white_3200_0": 16000.0},
            )


class Guide12N2LadderPlanTests(unittest.TestCase):
    def test_ladder_plan_is_formal_with_three_stops_per_hue(self):
        plan = build_guide12_n2_hsi_ladder_plan()
        steps = plan["captures"]
        self.assertEqual(len(steps), 6)
        self.assertTrue(all(c["capture_role"] == "formal" for c in steps))
        h0 = [c["nominal_shutter"] for c in steps if "h0" in c["capture_id"]]
        self.assertEqual(h0, ["1/1000", "1/2000", "1/4000"])
        self.assertEqual(plan["budgets"]["formal_cap"], 6)

    def test_ladder_can_narrow_to_one_hue_and_stops_for_retries(self):
        plan = build_guide12_n2_hsi_ladder_plan(
            hues=(240,), stops=("1/1000", "1/2000")
        )
        steps = plan["captures"]
        self.assertEqual(len(steps), 2)
        self.assertTrue(all("h240" in c["capture_id"] for c in steps))
        self.assertEqual(
            [c["nominal_shutter"] for c in steps], ["1/1000", "1/2000"]
        )
        self.assertEqual(
            plan["analysis_contract"]["hues"], [240],
        )


if __name__ == "__main__":
    unittest.main()
