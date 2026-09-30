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


if __name__ == "__main__":
    unittest.main()
