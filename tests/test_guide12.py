"""GUIDE12 deterministic corrections: secant algebra, signed units, rail gate.

The regression examples are the ones the Advisor prescribed: a secant whose
true response carries a nonzero intercept must recover a slope independent of
that intercept; a near-white-rail plateau must fail native plane quality even
when clipped_fraction stays 0; signed physical-unit errors must never be
populated from dimensionless normalized gate values.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from camera_based_rgbww_optimizer.optimization import guide12
from camera_based_rgbww_optimizer.optimization.guide11 import (
    build_guide11_w2_candidate_rows,
)


def _linear_response_observations(
    *,
    slope,
    intercept,
    base_command,
    delta_commands,
    target,
    tolerances,
    base_capture="base-000",
):
    """Observations with r(u) = target + intercept + slope @ (u - u_base).

    The white point of each observation is generated from an exact affine
    map in NORMALIZED components with the operating point centered on the
    base command, matching what ``build_guide11_w2_candidate_rows`` consumes
    from measured-secant evidence. The intercept stands in for every
    response offset the old absolute-residual regression absorbed.
    """
    import numpy as np

    names = list(base_command)
    u0 = np.array([float(base_command[n]) for n in names])
    m_matrix = np.asarray(slope, dtype="float64")  # outputs x channels
    intercept_vec = np.asarray(intercept, dtype="float64")
    target_vec = np.asarray(target, dtype="float64")

    def white_point_of(command):
        u = np.array([float(command[n]) for n in names])
        normalized = target_vec + intercept_vec + m_matrix @ (u - u0)
        return {
            "cct_K": float(normalized[0] * tolerances["cct_K"]),
            "mired": float(normalized[1] * tolerances["mired"]),
            "duv": float(normalized[2] * tolerances["duv"]),
        }

    observations = [
        {
            "capture_id": base_capture,
            "command": dict(base_command),
            "strip_white_point": white_point_of(base_command),
        }
    ]
    for index, delta in enumerate(delta_commands):
        command = {n: int(base_command[n] + delta.get(n, 0)) for n in names}
        observations.append({
            "capture_id": f"obs-{index:03d}",
            "command": command,
            "strip_white_point": white_point_of(command),
        })
    return observations


class SecantAlgebraRegressionTests(unittest.TestCase):
    """r(u) = a*u + b: the recovered slope must be independent of b."""

    TOLERANCES = {"cct_K": 200.0, "mired": 8.0, "duv": 0.002}

    def _frozen_targets(self, observations):
        return {
            "nodes": [{
                "cct": 3200, "gm": 100,
                "tolerances": dict(self.TOLERANCES),
                "ray_target": {"cct_K": 0.0, "mired": 0.0, "duv": 0.0},
                "measured_secant_evidence": {"observations": observations},
            }],
        }

    def _w6_analysis(self, tmp: Path) -> Path:
        import json

        path = tmp / "w6-analysis.json"
        path.write_text(json.dumps({
            "canonical_lut": [{
                "cct": 3200, "gm": 100, "status": "fail",
                "strip_command": {"cw": 0, "ww": 0, "r": 0, "g": 0, "b": 0},
            }],
        }), encoding="utf-8")
        return path

    def test_step_lands_on_target_for_any_intercept(self):
        import tempfile

        import numpy as np

        base_command = {"cw": 1000, "ww": 500, "r": 1000, "g": 100, "b": 200}
        # Three independent tested directions (cw, r, b) with an invertible
        # 3x3 output block: the differenced secant is exact, so the full step
        # must cancel the base residual for every intercept.
        slope = [
            [4.0e-4, 0.5e-4, 0.0, 0.0, 0.0],
            [2.0e-4, 0.0, 4.0e-4, 0.0, 0.0],
            [0.0, 3.0e-4, 0.0, 2.0e-4, 4.0e-4],
        ]
        delta_commands = [
            {"cw": 400, "ww": 0, "r": 0, "g": 0, "b": 0},
            {"cw": 0, "ww": 0, "r": 500, "g": 0, "b": 0},
            {"cw": 0, "ww": 0, "r": 0, "g": 0, "b": 300},
        ]
        target = [0.0, 0.0, 0.0]
        names = ("cw", "ww", "r", "g", "b")
        u0 = np.array([float(base_command[n]) for n in names])
        m_matrix = np.asarray(slope)
        intercepts = ([0.12, -0.08, 0.05], [-0.12, 0.05, -0.06], [0.02, 0.03, -0.04])
        for intercept in intercepts:
            observations = _linear_response_observations(
                slope=slope,
                intercept=intercept,
                base_command=base_command,
                delta_commands=delta_commands,
                target=target,
                tolerances=self.TOLERANCES,
            )
            with tempfile.TemporaryDirectory() as tmp_dir:
                frozen = self._frozen_targets(observations)
                analysis_path = self._w6_analysis(Path(tmp_dir))
                rows = build_guide11_w2_candidate_rows(frozen, analysis_path)
            self.assertEqual(len(rows), 1)
            row = rows[0]
            self.assertEqual(row["method"], "measured_secant_full_tolerance_step")
            diagnostics = row["secant_diagnostics"]
            self.assertEqual(diagnostics["command_delta_rank"], 3)
            self.assertEqual(diagnostics["sensitivity_rank"], 3)
            self.assertEqual(diagnostics["base_capture_id"], "base-000")
            self.assertEqual(len(diagnostics["command_delta_singular_values"]), 3)
            proposed = row["commands"][0]
            u1 = np.array([float(proposed[n]) for n in names])
            predicted = np.asarray(intercept) + m_matrix @ (u1 - u0)
            self.assertLess(
                float(np.max(np.abs(predicted))),
                5e-3,
                msg=f"intercept {intercept} not cancelled: {predicted}",
            )

    def test_absolute_residual_regression_would_be_wrong(self):
        """The prescribed counter-example, checked numerically.

        With r(u) = a*(u - u0) + b and a single secant row, regressing the
        absolute r(u1) against u1 - u0 (the old W2 algebra) yields a slope
        that shifts with b; the differenced fit recovers a exactly. This
        documents why the fix is behavioral, not cosmetic.
        """
        import numpy as np

        names = ("cw", "ww", "r", "g", "b")
        u0 = np.array([1000.0, 500.0, 200.0, 100.0, 50.0])
        u1 = u0 + np.array([400.0, 0.0, 0.0, 0.0, 0.0])
        a = np.array([1.0e-4, 2.0e-4, 3.0e-4])  # single channel -> rank 1
        b = np.array([0.37, -0.11, 0.05])
        old_slopes = []
        for intercept in (np.zeros(3), b):
            r0 = intercept
            r1 = intercept + a * (u1[0] - u0[0])
            old_slopes.append(r1 / (u1[0] - u0[0]))  # old B = r(u1), A = u1-u0
            fit = guide12.secant_sensitivity_fit(
                [
                    {"command": dict(zip(names, u0.tolist())),
                     "response": dict(zip(("o1", "o2", "o3"), r0.tolist()))},
                    {"command": dict(zip(names, u1.tolist())),
                     "response": dict(zip(("o1", "o2", "o3"), r1.tolist()))},
                ],
                channel_names=names,
                base_observation={
                    "command": dict(zip(names, u0.tolist())),
                    "response": dict(zip(("o1", "o2", "o3"), r0.tolist())),
                },
                output_names=("o1", "o2", "o3"),
            )
            self.assertEqual(fit["status"], "fitted")
            self.assertEqual(fit["command_delta_rank"], 1)
            # Sensitivity rows are channels x outputs; the "cw" channel row
            # must recover a exactly, independent of the intercept.
            cw_row = fit["sensitivity"][0]
            self.assertTrue(np.allclose(cw_row, a, rtol=1e-9, atol=1e-12))
        # With a zero intercept the single-row absolute form happens to
        # match a; any nonzero intercept moves it. The differenced form is
        # exact for both.
        self.assertTrue(np.allclose(old_slopes[0], a))
        self.assertFalse(np.allclose(old_slopes[1], a))
        self.assertFalse(np.allclose(old_slopes[0], old_slopes[1]))


class SignedWhiteErrorTests(unittest.TestCase):
    def test_signed_units_and_identity(self):
        strip = {"cct_K": 3195.0, "mired": 313.0, "duv": 0.0004}
        ray = {"cct_K": 3200.0, "mired": 312.0, "duv": 0.0001}
        tol = {"cct_K": 200.0, "mired": 8.0, "duv": 0.002}
        result = guide12.signed_white_errors(strip, ray, tol)
        self.assertEqual(result["sign_convention"], "strip_minus_reference")
        self.assertAlmostEqual(result["E_normalized"], 0.15)
        self.assertEqual(result["components"]["cct_K"]["error_signed"], -5.0)
        self.assertEqual(result["components"]["mired"]["error_signed"], 1.0)
        self.assertAlmostEqual(result["components"]["duv"]["error_signed"], 0.0003)
        self.assertEqual(result["components"]["cct_K"]["tolerance"], 200.0)
        self.assertAlmostEqual(
            result["components"]["mired"]["abs_normalized_error"], 0.125
        )
        # A normalized value must never be assigned to a physical field:
        # distinct namespaces make that misuse detectable.
        for name, component in result["components"].items():
            self.assertAlmostEqual(
                abs(component["error_signed"]) / component["tolerance"],
                component["abs_normalized_error"],
                places=12,
                msg=name,
            )


class FullscaleEvidenceTests(unittest.TestCase):
    def test_actual_payload_drives_status(self):
        evidence = guide12.fullscale_evidence(
            {"cw": 4095, "ww": 1542, "r": 21, "g": 90, "b": 1998},
            {"cold_white": 4095, "warm_white": 1542, "red": 21, "green": 90, "blue": 1998},
        )
        self.assertTrue(evidence["fullscale_actual"])
        self.assertEqual(evidence["actual_channels_at_4095"], ["cold_white"])

    def test_missing_actual_is_unknown_never_true(self):
        evidence = guide12.fullscale_evidence({"cw": 4095, "ww": 0, "r": 0, "g": 0, "b": 0}, None)
        self.assertIsNone(evidence["fullscale_actual"])
        self.assertTrue(evidence["requested_max_is_4095"])
        self.assertIsNone(evidence["fullscale_actual_source"])
        self.assertEqual(evidence["actual_channels_at_4095"], [])

    def test_sub_fullscale_actual(self):
        evidence = guide12.fullscale_evidence(
            {"cw": 4095, "ww": 0, "r": 0, "g": 0, "b": 0},
            {"cold_white": 3133, "warm_white": 0, "red": 0, "green": 0, "blue": 0},
        )
        self.assertFalse(evidence["fullscale_actual"])
        self.assertEqual(evidence["actual_max"], 3133)


class NativeRailGateTests(unittest.TestCase):
    """GUIDE12 2.2 forward gate on the native CFA planes."""

    def _quality(self, metrics, config):
        from camera_based_rgbww_optimizer.measurement.raw_mosaic_patches import (
            evaluate_plane_quality,
        )

        return evaluate_plane_quality(metrics, config)

    def test_whole_block_plateau_rejected_despite_zero_clipped_fraction(self):
        metrics = {
            "valid_pixel_count": 30072,
            "nonfinite_fraction": 0.0,
            "clipped_fraction": 0.0,
            "near_noise_floor_fraction": 0.0,
            "near_white_rail_fraction": 1.0,
            "white_rail_plateau": True,
        }
        config = {
            "minimum_valid_pixels_per_plane": 29000,
            "maximum_nonfinite_fraction": 0.0,
            "maximum_clipped_fraction": 0.0,
            "maximum_near_noise_floor_fraction": 0.05,
            "maximum_near_white_rail_fraction": 0.05,
        }
        quality = self._quality(metrics, config)
        self.assertEqual(quality["status"], "rejected")
        self.assertIn("white_rail_plateau", quality["failures"])
        self.assertIn("near_white_rail_fraction_exceeded", quality["failures"])

    def test_plateau_fails_even_without_configured_threshold(self):
        """The 16382/white-16383 plateau must never pass via a stale config."""
        metrics = {
            "valid_pixel_count": 30072,
            "nonfinite_fraction": 0.0,
            "clipped_fraction": 0.0,
            "near_noise_floor_fraction": 0.0,
            "near_white_rail_fraction": 1.0,
            "white_rail_plateau": True,
        }
        legacy_config = {
            "minimum_valid_pixels_per_plane": 29000,
            "maximum_nonfinite_fraction": 0.0,
            "maximum_clipped_fraction": 0.0,
            "maximum_near_noise_floor_fraction": 0.05,
        }
        quality = self._quality(metrics, legacy_config)
        self.assertEqual(quality["status"], "rejected")
        self.assertIn("white_rail_plateau", quality["failures"])

    def test_normal_plane_and_directions_not_inverted(self):
        metrics = {
            "valid_pixel_count": 30072,
            "nonfinite_fraction": 0.0,
            "clipped_fraction": 0.0,
            "near_noise_floor_fraction": 0.0,
            "near_white_rail_fraction": 0.0,
            "white_rail_plateau": False,
        }
        config = {
            "minimum_valid_pixels_per_plane": 29000,
            "maximum_nonfinite_fraction": 0.0,
            "maximum_clipped_fraction": 0.0,
            "maximum_near_noise_floor_fraction": 0.05,
            "maximum_near_white_rail_fraction": 0.05,
        }
        self.assertEqual(self._quality(metrics, config)["status"], "accepted")
        # Near-noise keeps its own direction: a dark floor is a low-end
        # failure, never a rail pass/failure, and vice versa.
        dark = dict(metrics, near_noise_floor_fraction=0.4)
        self.assertIn(
            "near_noise_floor_fraction_exceeded",
            self._quality(dark, config)["failures"],
        )

    def test_rendered_domain_profile_fields(self):
        """frame_exposure is labeled rendered RGB and cannot pose as native."""
        from camera_based_rgbww_optimizer.measurement import frame_exposure

        self.assertIs(
            frame_exposure.frame_exposure_profile,
            frame_exposure.rendered_rgb_exposure_profile,
        )

    def test_summarize_plane_emits_rail_metrics_and_quantiles(self):
        import numpy as np

        from camera_based_rgbww_optimizer.measurement.raw_mosaic_patches import (
            summarize_plane,
        )

        descriptor = {
            "label": "R",
            "color_code": "R",
            "color_index": 0,
            "row_offset": 0,
            "column_offset": 0,
            "black_level": 512.0,
            "black_level_source": "test",
            "camera_white_level": 16383.0,
            "global_white_level": 16383.0,
            "effective_white_level": 16383.0,
            "effective_white_level_source": "test",
            "observed_max": 16383,
        }
        statistics_config = {
            "trim_fraction": 0.1,
            "noise_floor_margin_normalized": 0.005,
            "clipping_margin_normalized": 0.0,
            "white_rail_margin_dn": 2.0,
        }
        quality_config = {
            "minimum_valid_pixels_per_plane": 1000,
            "maximum_nonfinite_fraction": 0.0,
            "maximum_clipped_fraction": 0.0,
            "maximum_near_noise_floor_fraction": 0.05,
            "maximum_near_white_rail_fraction": 0.05,
        }
        healthy = summarize_plane(
            np.full(4000, 4000.0),
            descriptor=descriptor,
            exposure_seconds=0.125,
            statistics_config=statistics_config,
            quality_config=quality_config,
        )
        self.assertEqual(healthy["quality"]["status"], "accepted")
        self.assertEqual(healthy["metrics"]["near_white_rail_fraction"], 0.0)
        self.assertIn("percentile_01", healthy["statistics"]["raw_code"])
        self.assertIn("percentile_99", healthy["statistics"]["raw_code"])
        # A plateau parked at 16382 (one DN below the 16383 white level) with
        # variance 0 is exactly the GUIDE11 C1 failure mode.
        plateau = summarize_plane(
            np.full(4000, 16382.0),
            descriptor=descriptor,
            exposure_seconds=0.125,
            statistics_config=statistics_config,
            quality_config=quality_config,
        )
        self.assertEqual(plateau["quality"]["status"], "rejected")
        self.assertIn("white_rail_plateau", plateau["quality"]["failures"])
        self.assertEqual(plateau["metrics"]["clipped_fraction"], 0.0)
        # Native fine but a partial rail fraction above threshold also fails.
        mixed_values = np.concatenate([
            np.full(3600, 4000.0), np.full(400, 16382.0),
        ])
        mixed = summarize_plane(
            mixed_values,
            descriptor=descriptor,
            exposure_seconds=0.125,
            statistics_config=statistics_config,
            quality_config=quality_config,
        )
        self.assertEqual(mixed["quality"]["status"], "rejected")
        self.assertIn("near_white_rail_fraction_exceeded", mixed["quality"]["failures"])


class RealInputReplayTests(unittest.TestCase):
    """Identity checks over the GUIDE12 offline-correction artifacts.

    Skipped on machines without the local D-drive evidence root so the suite
    stays portable; on the lab workstation these replay the real inputs.
    """

    BASE = Path("D:/rgbww-optimizer/guide11")
    PAIRING = BASE / "guide11-w2/derived/w2-fresh-pairing-audit-20260929.json"
    RAIL = BASE / "derived/raw-rail-audit-20260929.json"
    W8 = BASE / "guide11-w8/derived/guide11-white-final-report-signed-20260929.json"

    def _load(self, path):
        if not path.is_file():
            self.skipTest(f"local artifact absent: {path}")
        return json.loads(path.read_text(encoding="utf-8"))

    def test_pairing_signed_identities_and_nine_adopted(self):
        artifact = self._load(self.PAIRING)
        pairs = [
            p for node in artifact["nodes"] for p in node["pairs"]
            if p.get("status") == "paired"
        ]
        self.assertEqual(len(pairs), 49)
        for pair in pairs:
            components = pair["signed_vs_fresh_ray"]
            self.assertEqual(artifact["sign_convention"], "strip_minus_reference")
            self.assertAlmostEqual(
                pair["E_vs_fresh_ray"],
                max(c["abs_normalized_error"] for c in components.values()),
                places=12,
            )
            for name, component in components.items():
                self.assertAlmostEqual(
                    component["error_signed"],
                    float(pair["strip_white_point"][name])
                    - float(pair["fresh_ray_white_point"][name]),
                    places=9,
                    msg=f"{pair['cct']}/{pair['gm']} {name}",
                )
                self.assertAlmostEqual(
                    component["abs_normalized_error"],
                    abs(component["error_signed"]) / component["tolerance"],
                    places=12,
                    msg=name,
                )
        adopted = artifact["adopted_commands_fresh_vs_historical"]
        self.assertEqual(len(adopted), 9)
        self.assertTrue(all(
            a["independent_confirmation_status"] == "not_acquired" for a in adopted
        ))
        self.assertEqual(
            sum(
                1 for a in adopted
                if (a["paired_selection_frame"] or {}).get("E_vs_fresh_ray", 9) < 1.0
            ),
            7,
        )
        ranks = [
            d["command_delta_rank"]
            for d in artifact["command_delta_rank_diagnostics"]
            if d["command_delta_rank"] is not None
        ]
        self.assertTrue(ranks)
        self.assertEqual(max(ranks), 1)

    def test_rail_audit_c1_main_root_plateau_count(self):
        artifact = self._load(self.RAIL)
        by_root = {}
        for frame in artifact["quantitative_ineligible_frames"]:
            by_root[frame["root"]] = by_root.get(frame["root"], 0) + 1
        main = [k for k in by_root if k.endswith("formal-c1-20260924-r8")]
        self.assertEqual(len(main), 1)
        self.assertEqual(by_root[main[0]], 24)
        for frame in artifact["frames"]:
            if frame["block_06_frame_class"] != "plateau":
                continue
            planes = [
                p for p in frame["planes"].values() if p["rail_status"] == "plateau"
            ]
            self.assertTrue(planes)
            for plane in planes:
                self.assertEqual(plane["raw_code_variance"], 0.0)
                self.assertGreaterEqual(
                    plane["raw_code_min"], plane["effective_white_level"] - 2.0
                )

    def test_w8_report_signed_units_consistent(self):
        artifact = self._load(self.W8)
        counts = artifact["identity_counts"]
        self.assertEqual(counts.get("w6_single_observation"), 61)
        self.assertEqual(counts.get("w2_selection_frame_vs_same_candidate_fresh_ray"), 9)
        self.assertEqual(artifact["w2_adopted_within_tolerance_vs_fresh_ray"], 7)
        for node in artifact["nodes"]:
            evidence = node["error_evidence"]
            if evidence["identity"] == "w6_single_observation":
                for name, component in evidence["signed_components"].items():
                    if component["error_signed"] is None:
                        continue
                    self.assertAlmostEqual(
                        component["abs_normalized_error"],
                        abs(component["error_signed"]) / component["tolerance"],
                        places=12,
                        msg=f"{node['cct']}/{node['gm']} {name}",
                    )
            elif evidence["identity"].startswith("w2_selection_frame"):
                self.assertNotIn("e_cct_K", evidence)
                fresh = evidence["signed_vs_fresh_ray"]
                self.assertAlmostEqual(
                    evidence["E_vs_fresh_ray"],
                    max(c["abs_normalized_error"] for c in fresh.values()),
                    places=12,
                )


class Batch1PlanTests(unittest.TestCase):
    """GUIDE12 batch-1 frozen plan and runner validation."""

    @classmethod
    def setUpClass(cls):
        cls.plan = guide12.build_guide12_batch1_plan()

    def test_structure_counts_and_order(self):
        plan = self.plan
        captures = plan["captures"]
        self.assertEqual(len(captures), 13)
        self.assertEqual(
            [c["capture_role"] for c in captures[:2]], ["ambient", "ambient"]
        )
        self.assertEqual(
            [c["capture_role"] for c in captures[-2:]], ["ambient", "ambient"]
        )
        self.assertTrue(all(
            c["capture_role"] == "diagnostic" for c in captures[2:-2]
        ))
        self.assertEqual(plan["budgets"], {
            "formal_cap": 0, "diagnostic_cap": 9, "ambient_cap": 4,
            "physical_cr3_cap": 13, "setup_physical_cr3_cap": 0, "retry": 0,
        })
        self.assertEqual(len(plan["frozen_shutters"]), 9)
        for step in captures:
            if step["capture_role"] != "ambient":
                self.assertEqual(
                    plan["frozen_shutters"][step["exposure_cache_key"]],
                    step["nominal_shutter"],
                )

    def test_classes_are_actual_fullscale_commands(self):
        by_state = {}
        for step in self.plan["captures"]:
            if step["capture_role"] == "diagnostic":
                by_state[step["state_id"]] = step["command"]
        self.assertEqual(
            by_state["B1_R4095"],
            {"cw": 0, "ww": 0, "r": 4095, "g": 0, "b": 0},
        )
        self.assertEqual(
            by_state["B1_B4095"],
            {"cw": 0, "ww": 0, "r": 0, "g": 0, "b": 4095},
        )
        self.assertEqual(
            by_state["B1_WHITE2300"],
            {"cw": 0, "ww": 4095, "r": 1965, "g": 312, "b": 0},
        )
        for state, command in by_state.items():
            self.assertEqual(max(command.values()), 4095, msg=state)

    def test_ambient_steps_bracket_batch_with_gates(self):
        ambient = [
            c for c in self.plan["captures"] if c["capture_role"] == "ambient"
        ]
        self.assertEqual(len(ambient), 4)
        self.assertTrue(all(not c["formal_measurement"] for c in ambient))
        self.assertEqual(
            [c["ambient_position"] for c in ambient],
            ["start", "start", "end", "end"],
        )
        self.assertEqual(
            [c["ambient_shutter_speed"] for c in ambient],
            ["1/400", "1/8", "1/400", "1/8"],
        )
        self.assertTrue(all(c.get("isolation_gate_before") for c in ambient))

    def test_runner_validation_accepts_plan(self):
        from camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics import (
            validate_authorized_execution_plan,
        )

        validate_authorized_execution_plan(self.plan)

    def test_runner_validation_rejects_ambient_under_legacy_policy(self):
        import copy

        from camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics import (
            validate_authorized_execution_plan,
        )

        bad = copy.deepcopy(self.plan)
        bad["guide_experiment_id"] = None
        bad["native_raw_ambient_policy"] = "unsubtracted_no_ambient"
        bad["execution_authorization"]["schema"] = (
            "direct_guide11_w2_bounded_correction_v1"
        )
        bad["execution_authorization"]["experiment_id"] = (
            "GUIDE11_W2_BOUNDED_CORRECTION_V1"
        )
        with self.assertRaises(PermissionError):
            validate_authorized_execution_plan(bad)

    def test_policy_resolution_guide12_vs_default(self):
        from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
        from camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation import (
            AMBIENT_POLICY_UNSUBTRACTED_WITH_ALL_OFF_DIAGNOSTIC,
        )

        self.assertEqual(
            thermal.expected_native_raw_ambient_policy(
                thermal.TD_C,
                plan_schema=thermal.PLAN_SCHEMA_V2,
                guide_experiment_id=thermal.GUIDE12_BATCH1_EXPERIMENT_ID,
            ),
            AMBIENT_POLICY_UNSUBTRACTED_WITH_ALL_OFF_DIAGNOSTIC,
        )
        self.assertEqual(
            thermal.expected_native_raw_ambient_policy(
                thermal.TD_C, plan_schema=thermal.PLAN_SCHEMA_V2
            ),
            thermal.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        )

    def test_ambient_shutter_helper(self):
        from camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation import (
            ambient_shutter_for_step,
        )

        self.assertEqual(ambient_shutter_for_step({}, "30"), "30")
        self.assertEqual(ambient_shutter_for_step({"ambient_shutter_speed": "1/400"}, "30"), "1/400")
        self.assertEqual(ambient_shutter_for_step({"ambient_shutter_speed": 8}, "30"), "8")


class Batch1ValidatorOrderingTests(unittest.TestCase):
    """2026-09-30 recovery regression: the post-capture validator runs before
    execute_plan writes the terminal run state, so it must not consult
    run.json's status/cleanup; a fully captured root with run.json still
    "running" must validate."""

    def _synthetic_root(self, tmp: Path, plan):
        import json

        root = tmp / "run"
        root.mkdir()
        with open(root / "captures.jsonl", "w", encoding="utf-8") as fh:
            for step in plan["captures"]:
                capture = {"saved_file": "fake.cr3"}
                if step["capture_role"] != "ambient":
                    capture["ray_zero_before_capture"] = {"data": {"intensity": 0}}
                fh.write(json.dumps({
                    "capture_id": step["capture_id"],
                    "plan_step": step,
                    "capture": capture,
                }) + chr(10))
        with open(root / "physical-returns.jsonl", "w", encoding="utf-8") as fh:
            for step in plan["captures"]:
                fh.write(json.dumps({"capture_id": step["capture_id"]}) + chr(10))
        with open(root / "commands.jsonl", "w", encoding="utf-8") as fh:
            for state in ("B1_R4095", "B1_B4095", "B1_WHITE2300"):
                fh.write(json.dumps({
                    "event": "guide12_batch1_class_command_readback_verified",
                    "state_id": state,
                    "readback": {"device_snapshot": {
                        "cold_white": 0, "warm_white": 4095, "red": 4095,
                        "green": 312, "blue": 4095,
                    }},
                }) + chr(10))
        (root / "run.json").write_text(json.dumps({"status": "running"}), encoding="utf-8")
        return root

    def test_validator_passes_while_run_state_pending(self):
        import json
        import tempfile

        from camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics import (
            validate_direct_guide12_batch1_post_capture,
        )

        plan = guide12.build_guide12_batch1_plan()
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = self._synthetic_root(Path(tmp_dir), plan)
            quality = validate_direct_guide12_batch1_post_capture(root, plan, None)
            self.assertEqual(quality["status"], "pass")
            written = json.loads((root / "quality.json").read_text(encoding="utf-8"))
            self.assertEqual(written["capture_count"], 13)


class W12OpenQueueTests(unittest.TestCase):
    def _pairing(self, *rows):
        nodes = []
        for cct, gm, e, command in rows:
            nodes.append({
                "cct": cct, "gm": gm,
                "pairs": [{
                    "E_vs_fresh_ray": e, "command": command,
                    "strip_capture_id": f"strip-{cct}-{gm}", "ray_capture_id": f"ray-{cct}-{gm}",
                    "fresh_ray_white_point": {"cct_K": 3000.0, "mired": 333.0, "duv": 0.0},
                    "signed_vs_fresh_ray": {},
                }],
            })
        return {"schema": "guide12_w2_fresh_pairing_audit_v1", "nodes": nodes}

    def test_queue_order_and_exclusions(self):
        warm = {"cw": 24, "ww": 4095, "r": 157, "g": 10, "b": 712}
        queue = guide12.build_guide12_w12_open_queue(self._pairing(
            (6500, 0, 0.108, {"cw": 3888, "ww": 4095, "r": 0, "g": 124, "b": 2163}),
            (1800, 100, 5.0, dict(warm)),
            (2000, 200, 23.6, dict(warm)),
            (1800, 70, 1.116, dict(warm)),
            (2000, 100, 1.118, dict(warm)),
            (3200, 0, 10.288, dict(warm)),
        ))
        keys = [(n["cct"], n["gm"]) for n in queue["nodes"]]
        self.assertEqual(keys, [
            (3200, 0), (1800, 70), (2000, 100), (2000, 200),
        ])
        self.assertEqual(queue["open_node_count"], 4)
        self.assertEqual(queue["unchanged_qualified_nodes"], [
            {"cct": 6500, "gm": 0, "E_vs_fresh_ray": 0.108},
        ])
        self.assertEqual(queue["nodes"][0]["face_channels"], ["warm_white"])

    def test_cold_end_orders_by_descending_e(self):
        warm = {"cw": 24, "ww": 4095, "r": 157, "g": 10, "b": 712}
        queue = guide12.build_guide12_w12_open_queue(self._pairing(
            (2300, 200, 1.64, dict(warm)),
            (2000, 70, 14.29, dict(warm)),
            (2700, 100, 2.15, dict(warm)),
        ))
        keys = [(n["cct"], n["gm"]) for n in queue["nodes"]]
        self.assertEqual(keys, [(2000, 70), (2700, 100), (2300, 200)])

    def test_stage_node_budget_is_enforced(self):
        rows = []
        warm = {"cw": 24, "ww": 4095, "r": 157, "g": 10, "b": 712}
        for index, cct in enumerate(range(1800, 20000, 200)):
            rows.append((cct, 70, 1.5 + (index % 7), dict(warm)))
        with self.assertRaises(ValueError):
            guide12.build_guide12_w12_open_queue(self._pairing(*rows[:31]))
        queue = guide12.build_guide12_w12_open_queue(self._pairing(*rows[:30]))
        self.assertEqual(queue["open_node_count"], 30)


class W12ProbeDesignTests(unittest.TestCase):
    BASE = {"cw": 24, "ww": 4095, "r": 157, "g": 10, "b": 712}

    def test_probe_channels_rank(self):
        self.assertEqual(
            guide12.guide12_w12_probe_channels(self.BASE),
            ["cold_white", "blue", "red"],
        )
        self.assertEqual(
            guide12.guide12_w12_probe_channels(
                {"cw": 4095, "ww": 100, "r": 10, "g": 5, "b": 2000}
            ),
            ["warm_white", "blue", "red"],
        )

    def test_probe_candidates_structure(self):
        candidates = guide12.guide12_w12_probe_candidates(self.BASE)
        self.assertEqual([c["tag"] for c in candidates], [
            "u0_repeat", "probe_cw", "probe_b", "probe_r",
        ])
        self.assertEqual(len(candidates), guide12.W12_CANDIDATES_PER_BLOCK)
        by_tag = {c["tag"]: c for c in candidates}
        self.assertEqual(by_tag["u0_repeat"]["command"], self.BASE)
        self.assertFalse(by_tag["u0_repeat"]["new_unique_command"])
        self.assertTrue(all(by_tag[t]["new_unique_command"] for t in ("probe_cw", "probe_b", "probe_r")))
        self.assertEqual(by_tag["probe_cw"]["command"]["cw"], 24 + 768)
        self.assertEqual(by_tag["probe_b"]["command"]["b"], 712 + 768)
        self.assertEqual(by_tag["probe_r"]["command"]["r"], 157 + 768)
        for candidate in candidates[1:]:
            changed = [
                key for key, value in candidate["command"].items()
                if value != self.BASE[key]
            ]
            self.assertEqual(len(changed), 1)
            self.assertEqual(candidate["command"]["ww"], 4095)

    def test_probe_step_respects_headroom_and_cap(self):
        base = {"cw": 3900, "ww": 4095, "r": 0, "g": 0, "b": 4095 - 300}
        candidates = guide12.guide12_w12_probe_candidates(base)
        by_tag = {c["tag"]: c for c in candidates}
        # Headroom-limited probes stop exactly at the 4095 rail.
        self.assertEqual(by_tag["probe_cw"]["command"]["cw"], 4095)
        self.assertEqual(by_tag["probe_cw"]["probe_step_codes"], 195)
        self.assertEqual(by_tag["probe_b"]["command"]["b"], 4095)
        self.assertEqual(by_tag["probe_b"]["probe_step_codes"], 300)
        # Full-headroom probes take the whole 768-code single-step cap.
        self.assertEqual(by_tag["probe_r"]["command"]["r"], 768)
        self.assertEqual(by_tag["probe_r"]["probe_step_codes"], 768)


class W12FaceStepSolverTests(unittest.TestCase):
    """The constrained step must be a real box solve, not clip-after-lstsq.

    Slopes and errors are in tolerance-normalized units per code throughout.
    """

    SENS_N = {
        "cct_K": {"cold_white": -0.02, "warm_white": 0.0, "red": 0.004, "green": 0.001, "blue": -0.006},
        "mired": {"cold_white": -0.10, "warm_white": 0.0, "red": 0.02, "green": 0.005, "blue": -0.03},
        "duv": {"cold_white": 0.04, "warm_white": 0.0, "red": 0.20, "green": 0.02, "blue": -0.08},
    }
    BASE = {"cw": 500, "ww": 4095, "r": 500, "g": 500, "b": 500}

    def test_interior_solve_cancels_measured_error(self):
        base_error = {"cct_K": -0.5, "mired": 2.5, "duv": -0.4}
        result = guide12.solve_guide12_w12_face_step(
            self.BASE, base_error, self.SENS_N, face_channels=["warm_white"],
        )
        # Four free channels span the 2-D solve subspace; the integer-code
        # inward rounding leaves only quantization-level residuals.
        self.assertLess(abs(result["predicted_error_normalized"]["mired"]), 0.5)
        self.assertLess(abs(result["predicted_error_normalized"]["duv"]), 1.0)
        self.assertEqual(result["command"]["ww"], 4095)
        for short in ("cw", "r", "g", "b"):
            delta = result["command"][short] - self.BASE[short]
            self.assertLessEqual(abs(delta), 768 + 1e-9)
            self.assertGreaterEqual(result["command"][short], 0)
            self.assertLessEqual(result["command"][short], 4095)

    def test_single_channel_cap_pinned_analytic(self):
        # Only cold_white carries slope; cancelling +4.0 needs 4000 codes up,
        # so the 768-code cap pins and the residual is exact.
        sens = {
            "cct_K": dict(self.SENS_N["cct_K"]),
            "mired": {"cold_white": -0.001, "warm_white": 0.0, "red": 0.0, "green": 0.0, "blue": 0.0},
            "duv": {"cold_white": 0.0, "warm_white": 0.0, "red": 0.0, "green": 0.0, "blue": 0.0},
        }
        base_error = {"cct_K": 0.0, "mired": 4.0, "duv": 0.0}
        result = guide12.solve_guide12_w12_face_step(
            self.BASE, base_error, sens, face_channels=["warm_white"],
        )
        self.assertEqual(result["command"]["cw"], 500 + 768)
        self.assertIn("cw", result["active_bound_channels"])
        self.assertAlmostEqual(
            result["predicted_error_normalized"]["mired"], 4.0 - 0.768, places=9,
        )

    def test_two_channel_cap_analytic(self):
        sens = {
            "cct_K": dict(self.SENS_N["cct_K"]),
            "mired": {"cold_white": 0.01, "warm_white": 0.0, "red": 0.01, "green": 0.0, "blue": 0.0},
            "duv": {"cold_white": 0.001, "warm_white": 0.0, "red": -0.002, "green": 0.0, "blue": 0.0},
        }
        base_error = {"cct_K": 0.0, "mired": -30.0, "duv": 0.0}
        result = guide12.solve_guide12_w12_face_step(
            self.BASE, base_error, sens, face_channels=["warm_white"],
        )
        self.assertEqual(result["command"]["cw"], 500 + 768)
        self.assertEqual(result["command"]["r"], 500 + 768)
        self.assertAlmostEqual(
            result["predicted_error_normalized"]["mired"], -30.0 + 15.36, places=9,
        )
        self.assertAlmostEqual(
            result["predicted_error_normalized"]["duv"], 0.768 - 1.536, places=9,
        )

    def test_never_worse_than_clipped_unconstrained(self):
        import numpy as np

        rng = np.random.default_rng(20260930)
        channels = ["cold_white", "warm_white", "red", "green", "blue"]
        for _ in range(20):
            base = {
                "cw": int(rng.integers(20, 2000)), "ww": 4095,
                "r": int(rng.integers(0, 2000)), "g": int(rng.integers(0, 500)),
                "b": int(rng.integers(0, 2000)),
            }
            sens = {
                "cct_K": {c: 0.0 for c in channels},
                "mired": {c: float(rng.normal(0, 0.05)) for c in channels},
                "duv": {c: float(rng.normal(0, 0.08)) for c in channels},
            }
            sens["mired"]["warm_white"] = 0.0
            sens["duv"]["warm_white"] = 0.0
            base_error = {
                "cct_K": 0.0,
                "mired": float(rng.normal(0, 3.0)),
                "duv": float(rng.normal(0, 0.5)),
            }
            result = guide12.solve_guide12_w12_face_step(
                base, base_error, sens, face_channels=["warm_white"],
            )
            short = {"cold_white": "cw", "warm_white": "ww", "red": "r", "green": "g", "blue": "b"}
            ours = np.array([
                base_error["mired"], base_error["duv"]
            ]) + np.array([
                sum(
                    sens[o][c] * (result["command"][short[c]] - base[short[c]])
                    for c in channels
                )
                for o in ("mired", "duv")
            ])
            lower = np.array([
                max(-float(base[short[c]]), -768.0) for c in channels
            ])
            upper = np.array([
                min(float(4095 - base[short[c]]), 768.0) for c in channels
            ])
            matrix = np.array([
                [sens["mired"][c] for c in channels],
                [sens["duv"][c] for c in channels],
            ]).T
            unconstrained = np.linalg.lstsq(
                matrix.T, -np.array([base_error["mired"], base_error["duv"]]), rcond=None,
            )[0]
            clipped = np.clip(unconstrained, lower, upper)
            # Compare like for like: both owners end on integer codes.
            clipped_codes = np.clip(
                np.rint(np.array([
                    base[short[c]] + clipped[i] for i, c in enumerate(channels)
                ])), 0, 4095,
            )
            theirs = np.array([base_error["mired"], base_error["duv"]]) + matrix.T @ (
                clipped_codes - np.array([base[short[c]] for c in channels])
            )
            # Integer quantization: each code can shift by half a step, so the
            # comparison carries the aggregate half-step slack per channel.
            quantization_slack = float(
                0.5 * np.sum(np.linalg.norm(matrix, axis=1))
            )
            self.assertLessEqual(
                float(ours @ ours),
                float(theirs @ theirs) + quantization_slack**2
                + 2.0 * quantization_slack * float(np.linalg.norm(theirs)) + 1e-9,
            )
            for c in channels:
                self.assertTrue(0 <= result["command"][short[c]] <= 4095)
            self.assertEqual(result["command"]["ww"], 4095)

    def test_unmodeled_zero_slope_channel_cannot_move(self):
        # Green was never probed (zero sensitivity column); the box
        # enumeration must pin it instead of tie-breaking it to a bound
        # (2026-09-30 1800/70 defect: a -768 green step entered an
        # unmeasured physical direction with a fabricated prediction).
        sens = {
            "cct_K": dict(self.SENS_N["cct_K"]),
            "mired": dict(self.SENS_N["mired"]),
            "duv": dict(self.SENS_N["duv"]),
        }
        for output in sens:
            sens[output]["green"] = 0.0
        base_error = {"cct_K": -0.5, "mired": 2.5, "duv": -0.4}
        result = guide12.solve_guide12_w12_face_step(
            self.BASE, base_error, sens, face_channels=["warm_white"],
        )
        self.assertEqual(result["command"]["g"], self.BASE["g"])
        self.assertEqual(result["unmodeled_locked_channels"], ["g"])
        self.assertNotIn("g", result["active_bound_channels"])

    def test_all_directions_unmodeled_is_rejected(self):
        sens = {
            "cct_K": {c: 0.0 for c in
                      ("cold_white", "warm_white", "red", "green", "blue")},
            "mired": {c: 0.0 for c in
                      ("cold_white", "warm_white", "red", "green", "blue")},
            "duv": {c: 0.0 for c in
                    ("cold_white", "warm_white", "red", "green", "blue")},
        }
        base_error = {"cct_K": 0.0, "mired": 3.0, "duv": 0.0}
        with self.assertRaises(ValueError):
            guide12.solve_guide12_w12_face_step(
                self.BASE, base_error, sens, face_channels=["warm_white"],
            )

    def test_half_scale_stays_inside_box(self):
        base_error = {"cct_K": -0.5, "mired": 2.5, "duv": -0.4}
        result = guide12.solve_guide12_w12_face_step(
            self.BASE, base_error, self.SENS_N, face_channels=["warm_white"], scale=0.5,
        )
        for short in ("cw", "r", "g", "b"):
            self.assertLessEqual(abs(result["command"][short] - self.BASE[short]), 768 + 1e-9)
        self.assertEqual(result["scale"], 0.5)

    def test_face_channel_cannot_move(self):
        base_error = {"cct_K": 0.0, "mired": 3.0, "duv": 0.0}
        result = guide12.solve_guide12_w12_face_step(
            self.BASE, base_error, self.SENS_N, face_channels=["warm_white"],
        )
        self.assertEqual(result["command"]["ww"], 4095)
        self.assertEqual(result["face_channels"], ["ww"])


class W12BlockPlanTests(unittest.TestCase):
    NODE = {
        "cct": 3200, "gm": 0,
        "E_vs_fresh_ray": 10.288,
        "base_command": {"cw": 24, "ww": 4095, "r": 157, "g": 10, "b": 712},
        "base_capture_id": "033-strip-guide11-w2-cct3200-gm0-candidate0",
        "face_channels": ["warm_white"],
    }

    def test_probe_block_structure(self):
        candidates = guide12.guide12_w12_probe_candidates(self.NODE["base_command"])
        plan = guide12.build_guide12_w12_block_plan(
            self.NODE, candidates, block_index=1,
            predicted_raw_max={c["tag"]: 9000.0 for c in candidates},
        )
        self.assertEqual(len(plan["captures"]), 6)
        roles = [c["role"] for c in plan["captures"]]
        self.assertEqual(roles, [
            "ray_reference", "strip_candidate", "strip_candidate",
            "strip_candidate", "strip_candidate", "ray_reference",
        ])
        ids = [c["capture_id"] for c in plan["captures"]]
        self.assertEqual(len(set(ids)), 6)
        states = [c["state_id"] for c in plan["captures"]]
        self.assertEqual(len(set(states)), 6)
        self.assertEqual(plan["budgets"], {
            "formal_cap": 6, "diagnostic_cap": 0, "ambient_cap": 0,
            "physical_cr3_cap": 6, "setup_physical_cr3_cap": 0, "retry": 0,
        })
        self.assertEqual(
            plan["frozen_shutters"],
            {
                "ray-white-3200-gm0": "1/2500",
                "guide12-w12-strip-white-3200-gm0": "1/100",
            },
        )
        self.assertEqual(
            plan["execution_authorization"]["schema"],
            guide12.W12_AUTHORIZATION_SCHEMA,
        )
        self.assertEqual(plan["timing_resolution"], "guide12_w12_reset600_D120")
        self.assertEqual(plan["cold_proxy_wait_s"], 600)
        self.assertTrue(all(c["requested_elapsed_s"] == 120 for c in plan["captures"]))
        self.assertTrue(all(
            isinstance(c["session_index"], int) and c["session_index"] >= 1
            for c in plan["captures"]
        ))
        ray_commands = [
            c["command"] for c in plan["captures"] if c["source_id"] == "ray"
        ]
        self.assertEqual(ray_commands[0], ray_commands[1])
        self.assertEqual(ray_commands[0]["intensity_percent"], 100.0)
        self.assertEqual(
            plan["analysis_contract"]["new_unique_commands_in_block"], 3,
        )

    def test_block_rejects_oversized_and_ceiling_breach(self):
        candidates = guide12.guide12_w12_probe_candidates(self.NODE["base_command"])
        with self.assertRaises(ValueError):
            guide12.build_guide12_w12_block_plan(
                self.NODE, candidates + [dict(candidates[1], tag="probe_x")],
                block_index=1,
            )
        with self.assertRaises(ValueError):
            guide12.build_guide12_w12_block_plan(
                self.NODE, candidates, block_index=1,
                predicted_raw_max={c["tag"]: 20000.0 for c in candidates},
            )

    def test_unknown_ray_shutter_is_rejected(self):
        node = dict(self.NODE, cct=3300, gm=0)
        with self.assertRaises(ValueError):
            guide12.build_guide12_w12_block_plan(
                node, guide12.guide12_w12_probe_candidates(node["base_command"]),
                block_index=1,
            )


class W12ValidatorTests(unittest.TestCase):
    def _synthetic_root(self, tmp: Path, plan):
        root = tmp / "run"
        root.mkdir()
        feature_ids = ("f1", "f2")
        with open(root / "captures.jsonl", "w", encoding="utf-8") as fh:
            for step in plan["captures"]:
                capture = {
                    "saved_file": "fake.cr3",
                    "feature_values": {name: 1.0 for name in feature_ids},
                    "direct_quality": {
                        "status": "pass", "feature_count": len(feature_ids),
                    },
                }
                if step["source_id"] == "strip":
                    capture["ray_zero_before_capture"] = {"data": {"intensity": 0}}
                else:
                    capture["strip_zero_before_capture"] = {
                        "requested_payload": {
                            "cold_white": 0, "warm_white": 0, "red": 0,
                            "green": 0, "blue": 0,
                        },
                        "device_snapshot": {
                            "cold_white": 0, "warm_white": 0, "red": 0,
                            "green": 0, "blue": 0,
                        },
                    }
                fh.write(json.dumps({
                    "capture_id": step["capture_id"],
                    "plan_step": step,
                    "formal_measurement": step["formal_measurement"],
                    "source_id": step["source_id"],
                    "capture": capture,
                }) + chr(10))
        with open(root / "physical-returns.jsonl", "w", encoding="utf-8") as fh:
            for step in plan["captures"]:
                fh.write(json.dumps({
                    "capture_id": step["capture_id"], "cr3_byte_count": 1000,
                }) + chr(10))
        with open(root / "commands.jsonl", "w", encoding="utf-8") as fh:
            for step in plan["captures"]:
                if step["source_id"] != "strip":
                    continue
                snapshot = {
                    "cold_white": step["command"]["cw"],
                    "warm_white": step["command"]["ww"],
                    "red": step["command"]["r"],
                    "green": step["command"]["g"],
                    "blue": step["command"]["b"],
                }
                fh.write(json.dumps({
                    "event": "command_readback_verified",
                    "source_id": "strip",
                    "state_id": step["state_id"],
                    "readback": {"device_snapshot": snapshot},
                }) + chr(10))
        (root / "run.json").write_text(json.dumps({"status": "running"}), encoding="utf-8")
        return root

    def test_validator_passes_and_overwrites_quality_schema(self):
        import tempfile

        from camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics import (
            validate_direct_guide12_w12_post_capture,
        )

        candidates = guide12.guide12_w12_probe_candidates(W12BlockPlanTests.NODE["base_command"])
        plan = guide12.build_guide12_w12_block_plan(
            W12BlockPlanTests.NODE, candidates, block_index=1,
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = self._synthetic_root(Path(tmp_dir), plan)
            quality = validate_direct_guide12_w12_post_capture(root, plan, None)
            self.assertEqual(quality["status"], "pass")
            self.assertEqual(quality["schema"], "guide12_w12_fullscale_bounded_quality_v1")
            self.assertEqual(quality["strip_candidate_states"], 4)

    def test_validator_rejects_non_fullscale_readback(self):
        import tempfile

        from camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics import (
            validate_direct_guide12_w12_post_capture,
        )

        candidates = guide12.guide12_w12_probe_candidates(W12BlockPlanTests.NODE["base_command"])
        plan = guide12.build_guide12_w12_block_plan(
            W12BlockPlanTests.NODE, candidates, block_index=1,
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = self._synthetic_root(Path(tmp_dir), plan)
            commands_path = root / "commands.jsonl"
            rows = [
                json.loads(line)
                for line in commands_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            rows[0]["readback"]["device_snapshot"]["warm_white"] = 3000
            commands_path.write_text(
                chr(10).join(json.dumps(r) for r in rows) + chr(10), encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                validate_direct_guide12_w12_post_capture(root, plan, None)


if __name__ == "__main__":
    unittest.main()
