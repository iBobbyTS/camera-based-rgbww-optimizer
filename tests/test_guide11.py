import hashlib
import math
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from camera_based_rgbww_optimizer.optimization import (
    guide11,
    measure_p7_thermal_diagnostics as measure,
    p7_thermal_diagnostics as thermal,
)
from camera_based_rgbww_optimizer.measurement.recorded_exposure import parse_nominal_exposure


CCTS = (1800, 1900, 2150, 2500, 3000, 3500, 4100, 4750, 5300, 6100, 7250, 9000, 12000, 17000)
GMS = (0, 70, 100, 130, 200)


def synthetic_lut() -> list[dict]:
    rows = []
    for cct in CCTS:
        for gm in GMS:
            rows.append({
                "cct": cct,
                "gm": gm,
                "command": {
                    "cw": (cct // 100) % 4096,
                    "ww": (gm * 8) % 4096,
                    "r": (cct + gm) % 4096,
                    "g": 128,
                    "b": (gm * 3) % 4096,
                },
            })
    return rows


def synthetic_shutters() -> dict[str, str]:
    shutters = {}
    for cct in CCTS:
        for gm in GMS:
            shutters[f"ray-white-{cct}-gm{gm}"] = "1/100"
            shutters[f"strip-white-{cct}-gm{gm}"] = "1/60"
    return shutters


class Guide11InterpolationTests(unittest.TestCase):
    def test_exact_node_returns_stored_command(self):
        lut = synthetic_lut()
        resolved = guide11.interpolate_white_command(lut, 3000, 100)
        stored = next(
            row for row in lut if row["cct"] == 3000 and row["gm"] == 100
        )["command"]
        self.assertTrue(resolved["exact_node"])
        self.assertFalse(resolved["clamped_to_hull"])
        self.assertEqual(resolved["command"], {k: int(v) for k, v in stored.items()})
        self.assertIsNone(resolved["nearest_node_command"])

    def test_midpoint_is_bilinear_not_nearest_copy(self):
        lut = synthetic_lut()
        resolved = guide11.interpolate_white_command(lut, 3200, 100)
        self.assertFalse(resolved["exact_node"])
        self.assertEqual(resolved["command"]["g"], 128)
        # 3200K sits between the 3000K and 3500K rows; GM 100 is an exact
        # column, so cw must land on the mired-linear interpolation.
        cw_low = next(r for r in lut if r["cct"] == 3000 and r["gm"] == 100)["command"]["cw"]
        cw_high = next(r for r in lut if r["cct"] == 3500 and r["gm"] == 100)["command"]["cw"]
        mired = 1_000_000.0 / 3200
        frac = (mired - 1_000_000.0 / 3500) / (1_000_000.0 / 3000 - 1_000_000.0 / 3500)
        expected = int(round(cw_low * frac + cw_high * (1.0 - frac)))
        self.assertEqual(resolved["command"]["cw"], expected)
        self.assertNotEqual(resolved["command"], resolved["nearest_node_command"])

    def test_outside_hull_clamps(self):
        resolved = guide11.interpolate_white_command(synthetic_lut(), 800, 250)
        self.assertTrue(resolved["clamped_to_hull"])
        edge = guide11.interpolate_white_command(synthetic_lut(), 1800, 200)
        self.assertEqual(resolved["command"], edge["command"])

    def test_n1_builder_uses_shared_interpolation_for_non_nodes(self):
        lut = synthetic_lut()
        plan = guide11.build_guide11_n1_session_plan(
            lut, synthetic_shutters(), session_index=1, cycle_index=1,
        )
        audit = {
            (row["cct"], row["gm"]): row for row in plan["analysis_contract"]["commands_audit"]
        }
        self.assertTrue(audit[(1800, 100)]["exact_node"])
        for key in ((2300, 200), (3200, 0), (5600, 100), (14000, 0), (20000, 100)):
            self.assertFalse(audit[key]["exact_node"], key)
            shared = guide11.interpolate_white_command(lut, *key)
            self.assertEqual(audit[key]["strip_command"], shared["command"], key)


class Guide11N1PlanTests(unittest.TestCase):
    def test_session_structure_and_balance(self):
        lut = synthetic_lut()
        s1 = guide11.build_guide11_n1_session_plan(
            lut, synthetic_shutters(), session_index=1, cycle_index=1,
        )
        s2 = guide11.build_guide11_n1_session_plan(
            lut, synthetic_shutters(), session_index=2, cycle_index=2,
        )
        self.assertEqual(len(s1["captures"]), 24)
        self.assertEqual(len(s2["captures"]), 12)
        self.assertEqual(s1["budgets"]["physical_cr3_cap"], 24)
        self.assertEqual(s2["budgets"]["physical_cr3_cap"], 12)
        burst_roles = [c["n1_burst_role"] for c in s1["captures"]]
        self.assertEqual(burst_roles.count("burst_main"), 6)
        self.assertEqual(burst_roles.count("burst_extra_1"), 6)
        self.assertEqual(burst_roles.count("burst_extra_2"), 6)
        self.assertEqual(
            burst_roles.count("paired_cycle_main"),
            24 - 18,
        )
        # Source order flips between the two cycles for the same point.
        def first_source(plan, cct, gm):
            return next(
                c["source_id"] for c in plan["captures"]
                if c["target_cct"] == cct and c["target_gm"] == gm
            )
        for cct, gm in guide11.N1_POINTS:
            self.assertNotEqual(
                first_source(s1, cct, gm), first_source(s2, cct, gm), (cct, gm)
            )
        # Bursts share the group state and add no reset: same state_id and
        # strictly increasing dwell targets within each burst triplet.
        by_state: dict[str, list[float]] = {}
        for c in s1["captures"]:
            by_state.setdefault(c["state_id"], []).append(float(c["requested_elapsed_s"]))
        self.assertEqual(len(by_state), 12)
        for state, elapsed in by_state.items():
            self.assertEqual(elapsed, sorted(elapsed), state)
        self.assertEqual(
            sorted(by_state["N1_C1_CCT1800_GM100_RAY"]), [120.0, 125.0, 130.0]
        )
        # Dwell label matches the plan's own timing contract.
        self.assertEqual(s1["timing_resolution"], "guide11_n1_reset600_D120")
        self.assertEqual(s1["cold_proxy_wait_s"], 600)

    def test_builder_never_self_verifies_authorization(self):
        plan = guide11.build_guide11_n1_session_plan(
            synthetic_lut(), synthetic_shutters(), session_index=1, cycle_index=1,
        )
        auth = plan["execution_authorization"]
        self.assertEqual(auth["schema"], guide11.N1_AUTHORIZATION_SCHEMA)
        self.assertFalse(auth["human_authorization_verified"])
        self.assertEqual(auth["device_use_granted_by"], "operator_cli_allow_device_control")
        # The plan as built must clear the execution validator.
        measure.validate_authorized_execution_plan(plan)


class Guide11TimingLabelTests(unittest.TestCase):
    def _plan(self) -> dict:
        return guide11.build_guide11_n1_session_plan(
            synthetic_lut(), synthetic_shutters(), session_index=1, cycle_index=1,
        )

    def test_long_label_rejects_fast_execution_values(self):
        plan = self._plan()
        plan["timing_resolution"] = "guide11_long_reset1800_D600"
        with self.assertRaises(PermissionError):
            measure.validate_authorized_execution_plan(plan)  # reset still 600
        plan["cold_proxy_wait_s"] = 1800
        plan["cold_proxy"] = 1800
        with self.assertRaises(PermissionError):
            measure.validate_authorized_execution_plan(plan)  # dwell still 120
        for step in plan["captures"]:
            step["requested_elapsed_s"] = 600
        measure.validate_authorized_execution_plan(plan)

    def test_dwell_label_rejects_reset_mismatch(self):
        plan = self._plan()
        plan["cold_proxy_wait_s"] = 1800
        with self.assertRaises(PermissionError):
            measure.validate_authorized_execution_plan(plan)

    def test_self_verified_authorization_is_rejected(self):
        plan = self._plan()
        plan["execution_authorization"] = {
            "schema": "direct_legacy_self_grant_v1",
            "human_authorization_required": False,
            "human_authorization_verified": True,
            "human_authorization_experiment_id": plan["guide_experiment_id"],
            "experiment_id": plan["guide_experiment_id"],
            "remote_v2_capability": True,
        }
        with self.assertRaises(PermissionError):
            measure.validate_authorized_execution_plan(plan)


class Guide11FullToleranceNavigationTests(unittest.TestCase):
    def test_mired_violation_blocks_pass_despite_cct_duv_within(self):
        from camera_based_rgbww_optimizer.optimization import white_lut_feedback

        candidate = {"cct_K": 10150.0, "duv": 0.0}
        target = {"cct_K": 10000.0, "duv": 0.0}
        metrics = white_lut_feedback.white_point_metrics(
            candidate, target,
            cct_tolerance_K=200.0, duv_tolerance=0.002, mired_tolerance=8.0,
        )
        self.assertLess(metrics["normalized_gates"]["cct_K"], 1.0)
        self.assertLess(metrics["normalized_gates"]["duv"], 1.0)
        # |1e6/10150 - 1e6/10000| = 1.48 mired < 8: still passing here.
        self.assertLess(metrics["normalized_gates"]["mired"], 1.0)
        self.assertTrue(metrics["within_goal"])
        tight = white_lut_feedback.white_point_metrics(
            candidate, target,
            cct_tolerance_K=200.0, duv_tolerance=0.002, mired_tolerance=1.0,
        )
        self.assertLess(tight["normalized_gates"]["cct_K"], 1.0)
        self.assertGreaterEqual(tight["normalized_gates"]["mired"], 1.0)
        self.assertFalse(tight["within_goal"])
        self.assertEqual(tight["goal_score"], tight["normalized_gates"]["mired"])

    def test_w5_candidate_method_labels_recorded(self):
        from camera_based_rgbww_optimizer.optimization import guide10_white70

        def node(cct, gm, status, command):
            return {
                "cct": cct, "gm": gm, "status": status,
                "strip_command": dict(command),
                "strip": {"white_point": {"cct_K": 3000.0, "duv": 0.0}},
                "ray": {"white_point": {"cct_K": 3200.0, "duv": 0.0}},
                "limits": {"cct_K": 150.0, "duv": 0.002},
            }

        failed = node(1800, 100, "fail", {"cw": 1000, "ww": 500, "r": 4095, "g": 200, "b": 100})
        nodes = [failed] + [
            node(1800 + i * 100, 0, "pass", {"cw": 10, "ww": 10, "r": 4095, "g": 10, "b": 10})
            for i in range(69)
        ]
        step_template = {
            "source_id": "ray", "capture_id": "x", "exposure_cache_key": "k",
            "nominal_shutter": "1/100", "requested_elapsed_s": 120,
            "formal_measurement": True, "capture_role": "formal",
            "command": {}, "exact_command_hash": "h", "state_id": "s",
        }
        plan = {
            "captures": [
                {**step_template, "source_id": "ray", "target_cct": 1800, "target_gm": 100},
                {**step_template, "source_id": "strip", "target_cct": 1800, "target_gm": 100},
            ],
            "analysis_contract": {
                "target_contracts": [{
                    "cct": 1800, "gm": 100, "source_order": ["ray", "strip"],
                    "resolved_cct_tolerance_K": 150.0, "cct_tolerance_mired": 8.0,
                    "duv_tolerance": 0.002, "strip_command": {},
                }],
            },
        }
        calibration = {"targets": [{
            "cct": 1800, "gm": 100,
            "feedback_goal": {"resolved_cct_tolerance_K": 150.0},
            "feedback_optimizer": {"active_channel": "r", "damping": 0.05},
        }]}
        result = guide10_white70.build_guide10_white70_w5_plan(
            {"node_count": 70, "nodes": nodes}, plan, calibration,
            analysis_reference={}, round1_reference={}, calibration_reference={},
        )
        rows = result["analysis_contract"]["candidate_rows"]
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["method"], "measured_secant_toward_passing_neighbor")
        self.assertEqual(row["objective"], "guide11_full_tolerance_E_max")
        self.assertEqual(row["tolerances"]["mired"], 8.0)
        # The same-face passing neighbors exist (r-saturated face), so the
        # secant path must produce a bounded step, never a ±256 name-ranked
        # guess on channel "b" by letter order.
        base = row["base_command"]
        stepped = row["commands"][0]
        changed = {name: stepped[name] - base[name] for name in base if stepped[name] != base[name]}
        self.assertTrue(changed)
        self.assertTrue(all(abs(delta) <= 768 for delta in changed.values()))


class _FakeClock:
    def __init__(self):
        self.now = 1000.0

    def monotonic(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.now += float(seconds)


class Guide11ExecutionProtocolTests(unittest.TestCase):
    """Injected-clock execution: FAST 600/120, LONG 1800/600, burst shares reset."""

    def _run_plan(self, plan, root: Path):
        feature_ids = tuple(
            json.loads(thermal.POLICY_PATH.read_text(encoding="utf-8"))["feature_set"]["ids"]
        )
        curve = json.loads(thermal.CURVE_PATH.read_text(encoding="utf-8"))
        clock = _FakeClock()
        reset_sleeps: list[float] = []
        gate_ids: list[str] = []
        command_rows: list[dict] = []

        def capture(step):
            clock.now += 2.0
            index = int(str(step["capture_id"]).split("-", 1)[0])
            raw = root / f"{step['capture_id']}.cr3"
            raw.write_bytes(f"fake-{index}".encode())
            sidecar = raw.with_suffix(raw.suffix + ".metadata.json")
            sidecar.write_text("{}")
            timing = {
                "tier": "tier_b",
                "status": "accepted_best_effort_anchor",
                "provenance": thermal.TIMING_CONTRACT_V2["provenance"],
                "best_effort_elapsed_s": clock.now - owner_start["value"],
            }
            covariates = thermal.build_covariate_record(
                source_id=step["source_id"], state_id=step["state_id"],
                command=step["command"], sequence_index=index, capture_order=index,
                source_order=int(step.get("source_order", 1)),
                monotonic_timestamp_ns=index + 1,
                wall_clock_timestamp="2026-09-22T00:00:00+00:00",
                session_elapsed_s=float(index), source_on_elapsed_s=1.0,
                state_on_elapsed_s=1.0, off_duration_before_s=0.0,
                previous_state_id=None, previous_state_dwell_s=None,
                shutter_seconds=1 / 100,
                raw_black_levels=(0, 0, 0, 0), raw_white_level=65535,
                load_history={60: 0.0, 300: 0.0, 900: 0.0},
                readback={"status": "pass"},
                curve=curve if step["source_id"] == "strip" else None,
            )
            output = {
                "capture_id": step["capture_id"], "saved_file": str(raw),
                "remote_metadata_path": str(sidecar), "physical_capture_count": 1,
                "timing_evidence": timing, "thermal_covariates": covariates,
                "recorded_exposure": {
                    "source": "Canon:ExposureTime", "status": "recorded",
                    "seconds": parse_nominal_exposure("1/100"),
                },
                "feature_values": {fid: 1.0 for fid in feature_ids},
                "direct_quality": {"status": "pass", "feature_count": len(feature_ids)},
            }
            if step["source_id"] == "ray":
                output["strip_zero_before_capture"] = {
                    "requested_payload": {
                        "red": 0, "green": 0, "blue": 0,
                        "warm_white": 0, "cold_white": 0,
                    },
                    "device_snapshot": {
                        "red": 0, "green": 0, "blue": 0,
                        "warm_white": 0, "cold_white": 0,
                    },
                }
            else:
                output["ray_zero_before_capture"] = {
                    "response": {"data": {"intensity": 0}},
                }
            return output

        owner_start: dict[str, float] = {"value": 0.0}

        def set_capture_context(value: float) -> None:
            owner_start["value"] = value

        def fake_sidecar(payload, *, raw_path, raw_payload=None, run_root):
            sidecar = Path(str(payload["remote_metadata_path"]))
            return {
                "sidecar_path": str(sidecar.resolve()),
                "sidecar_byte_count": sidecar.stat().st_size,
                "sidecar_sha256": hashlib.sha256(sidecar.read_bytes()).hexdigest(),
                "sidecar_validation_status": "pass",
                "remote_capture_id": f"remote-{payload['capture_id']}",
                "remote_request_id": f"request-{payload['capture_id']}",
                "remote_metadata": {
                    "capture_id": f"remote-{payload['capture_id']}",
                    "request_id": f"request-{payload['capture_id']}",
                    "exposure_start_estimate": {
                        "method": "gphoto_event_minus_recorded_exposure",
                    },
                },
                "receipt": {"timing_evidence": payload["timing_evidence"]},
            }

        original_sleep = clock.sleep

        def counting_sleep(seconds: float) -> None:
            if abs(float(seconds) - float(plan["cold_proxy_wait_s"])) < 1e-6:
                reset_sleeps.append(float(seconds))
            original_sleep(seconds)

        with patch.object(measure, "_validate_returned_sidecar", side_effect=fake_sidecar):
            measure.execute_plan(
                plan, run_dir=root,
                apply_command_fn=lambda step: clock.__setattr__("now", clock.now + 0.5)
                or {"status": "pass"},
                readback_fn=lambda step: clock.__setattr__("now", clock.now + 0.5)
                or {"status": "pass"},
                capture_fn=capture,
                both_off_gate_fn=lambda gate_id: gate_ids.append(gate_id)
                or {
                    "status": "pass", "strip_verified_off": True,
                    "ray_verified_off": True, "ray_off_command": {"status": "pass"},
                },
                source_isolation_check_fn=lambda gate_id: {
                    "status": "pass", "source_verified_zero": True,
                    "source_verified": "ray", "strip_verified_off": True,
                    "ray_verified_off": True,
                    "ray_off_command": {"status": "pass", "data": {"intensity": 0}},
                },
                cleanup_fn=lambda: {"status": "pass", "steps": [{"ok": True}]},
                runtime_capture_settings_provenance=plan["camera"]["resolved_capture_settings"],
                runtime_git_provenance={"commit": "0" * 40, "dirty": False, "dirty_entries": []},
                post_capture_validator_fn=measure.validate_direct_protocol_post_capture,
                set_capture_context_fn=set_capture_context,
                monotonic_fn=clock.monotonic,
                sleep_fn=counting_sleep,
            )
        commands_path = root / "commands.jsonl"
        if commands_path.is_file():
            command_rows = [
                json.loads(line) for line in commands_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
        return {"reset_sleeps": reset_sleeps, "gate_ids": gate_ids, "command_rows": command_rows}

    def test_fast_session_burst_shares_one_reset_and_true_source_on(self):
        plan = guide11.build_guide11_n1_session_plan(
            synthetic_lut(), synthetic_shutters(), session_index=1, cycle_index=1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "run"
            root.mkdir()
            result = self._run_plan(plan, root)
        # 12 observation groups (6 points x 2 sources), never one reset per
        # burst capture. One extra run_start gate precedes the groups.
        self.assertEqual(len(result["reset_sleeps"]), 12)
        self.assertTrue(all(value == 600.0 for value in result["reset_sleeps"]))
        self.assertEqual(
            sum("reset600" in gate_id for gate_id in result["gate_ids"]), 12
        )
        self.assertEqual(len(result["command_rows"]), 12)
        burst_row = next(
            row for row in result["command_rows"] if len(row["group_capture_ids"]) == 3
        )
        self.assertEqual(len(burst_row["group_capture_ids"]), 3)
        # The dwell clock starts at the command application, not after the
        # reset wait: source_on precedes command/readback completion.
        self.assertLess(
            burst_row["source_on_monotonic_s"],
            burst_row["readback_completed_monotonic_s"],
        )

    def test_long_plan_executes_true_1800_reset_and_600_dwell(self):
        plan = guide11.build_guide11_n1_session_plan(
            synthetic_lut(), synthetic_shutters(), session_index=1, cycle_index=1,
        )
        # Re-label as a true LONG protocol plan with 3 paired observations.
        plan = dict(plan)
        plan["timing_resolution"] = "guide11_long_reset1800_D600"
        plan["cold_proxy"] = 1800
        plan["cold_proxy_wait_s"] = 1800
        plan["analysis_contract"] = dict(plan["analysis_contract"])
        plan["analysis_contract"]["independent_reset_s"] = 1800
        plan["analysis_contract"]["dwell_s"] = 600
        keeps = []
        for step in plan["captures"]:
            step = dict(step)
            step["requested_elapsed_s"] = 600
            if len(keeps) < 4:
                keeps.append(step)
        plan["captures"] = keeps
        plan["capture_ids"] = [s["capture_id"] for s in keeps]
        plan["frozen_shutters"] = {
            key: value for key, value in plan["frozen_shutters"].items()
            if key in {s["exposure_cache_key"] for s in keeps}
        }
        plan["shutter_ledger_provenance"] = {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(plan["frozen_shutters"]),
            "frozen_shutters_sha256": thermal.canonical_sha256(plan["frozen_shutters"]),
        }
        plan["budgets"] = {
            "ray_cap": 2, "strip_cap": 2, "formal_cap": 4,
            "physical_cr3_cap": 4, "ambient_cap": 0, "retry": 0,
        }
        measure.validate_authorized_execution_plan(plan)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "run"
            root.mkdir()
            result = self._run_plan(plan, root)
        self.assertEqual(result["reset_sleeps"], [1800.0, 1800.0, 1800.0, 1800.0])
        # Dwell wait of the first capture in each group is ~600 s from the
        # true source-on instant (minus the small apply/readback cost).
        for row in result["command_rows"]:
            self.assertEqual(row["reset_wait_s"], 1800.0)
            self.assertIn("source_on_monotonic_s", row)


if __name__ == "__main__":
    unittest.main()


class Guide11N1AnalysisTests(unittest.TestCase):
    def _write_session(self, root: Path, session: int, cct_noise: float = 0.0):
        import numpy as np
        plan = guide11.build_guide11_n1_session_plan(
            synthetic_lut(), synthetic_shutters(), session_index=session, cycle_index=session,
        )
        root.mkdir(parents=True, exist_ok=True)
        (root / "experiment-spec.json").write_text(json.dumps(plan), encoding="utf-8")
        rows = []
        index = 0
        for step in plan["captures"]:
            capture_id = step["capture_id"]
            raw = root / "camera" / f"{capture_id}.cr3"
            raw.parent.mkdir(parents=True, exist_ok=True)
            raw.write_bytes(b"fake-cr3")
            sidecar = root / "measurements" / f"{capture_id}.patch-statistics.json"
            sidecar.parent.mkdir(parents=True, exist_ok=True)
            base_r, base_g, base_b = 900.0, 600.0, 300.0
            jitter = cct_noise * (1 if index % 2 else -1)
            sidecar.write_text(json.dumps({
                "patches": [{
                    "index": 6, "name": "block_06",
                    "planes": {
                        plane: {"statistics": {"normalized_per_second": {
                            "trimmed_mean": value,
                        }}}
                        for plane, value in (
                            ("R", base_r + 30 * index + jitter),
                            ("G1", base_g + 10 * index),
                            ("G2", base_g + 10 * index + 2),
                            ("B", base_b + 5 * index - jitter),
                        )
                    },
                }],
            }), encoding="utf-8")
            rows.append({
                "capture_id": capture_id,
                "source_id": step["source_id"],
                "plan_step": step,
                "capture": {"saved_file": str(raw)},
                "best_effort_exposure_start_elapsed_s": 120.0,
            })
            index += 1
        (root / "captures.jsonl").write_text(
            "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8"
        )
        return root

    def test_two_session_analysis_layers(self):
        import tempfile

        from camera_based_rgbww_optimizer.optimization import analyze_guide11_n1 as analyzer

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            s1 = self._write_session(base / "s1", 1, cct_noise=0.0)
            s2 = self._write_session(base / "s2", 2, cct_noise=0.0)
            with patch.object(
                analyzer.common, "_load_rawpy_rgb_xyz_matrix",
                side_effect=lambda *_args, **_kwargs: [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            ):
                result = analyzer.analyze_guide11_n1([s1, s2])
        self.assertEqual(result["observation_count"], 36)
        self.assertEqual(len(result["points"]), 6)
        by_point = {(p["cct"], p["gm"]): p for p in result["points"]}
        burst_point = by_point[(1800, 100)]
        self.assertTrue(burst_point["is_burst_point"])
        self.assertIn("ray", burst_point["burst_layer"])
        self.assertEqual(burst_point["burst_layer"]["ray"]["n"], 3)
        # Identical sessions give identical cycle differences: zero spread
        # with n=2 cycles reported per point.
        point = by_point[(3200, 0)]
        self.assertEqual(point["cct_K_diff"]["status"], "ok")
        self.assertEqual(point["cct_K_diff"]["n"], 2)
        for cycle in ("1", "2"):
            z = point["product_chromaticity"][cycle]["ray_z"]["log_R_over_G"]
            self.assertTrue(math.isfinite(z))


class Guide11C1ProductLayerTests(unittest.TestCase):
    def test_block06_gate_and_accepted_features(self):
        report = {
            "patches": [{
                "index": 6, "name": "block_06", "quality_status": "accepted",
                "planes": {
                    plane: {"statistics": {"normalized_per_second": {"trimmed_mean": 500.0 + i}}}
                    for i, plane in enumerate(("R", "G1", "G2", "B"))
                },
            }],
        }
        good = measure._c1_block06_quality(report)
        self.assertTrue(good["accepted"])
        self.assertEqual(good["planes"]["R"], 500.0)
        clipped = {
            "patches": [{
                "index": 6, "quality_status": "accepted",
                "planes": {
                    plane: {
                        "statistics": {"normalized_per_second": {"trimmed_mean": 500.0}},
                        "quality": {"clipped": plane == "R"},
                    }
                    for plane in ("R", "G1", "G2", "B")
                },
            }],
        }
        self.assertFalse(measure._c1_block06_quality(clipped)["accepted"])
        missing = {"patches": []}
        self.assertIsNone(measure._c1_block06_quality(missing))
        negative = {
            "patches": [{
                "index": 6, "quality_status": "accepted",
                "planes": {
                    plane: {"statistics": {"normalized_per_second": {"trimmed_mean": 0.0}}}
                    for plane in ("R", "G1", "G2", "B")
                },
            }],
        }
        self.assertFalse(measure._c1_block06_quality(negative)["accepted"])


class Guide11ExposureTriageTests(unittest.TestCase):
    def test_frame_profile_classifies_saturated_and_dark(self):
        import numpy as np

        class FakeRaw:
            def __init__(self, array):
                self._array = array

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def postprocess(self, **kwargs):
                return self._array

        from camera_based_rgbww_optimizer.measurement import frame_exposure

        white = np.full((64, 64, 3), 65500, dtype=np.uint16)
        dark = np.full((64, 64, 3), 300, dtype=np.uint16)
        normal = np.stack(
            [np.full((64, 64), 40000), np.full((64, 64), 5000), np.full((64, 64), 12000)],
            axis=-1,
        ).astype(np.uint16)
        with patch.object(
            frame_exposure.rawpy if hasattr(frame_exposure, "rawpy") else __import__("rawpy"),
            "imread",
            side_effect=[FakeRaw(white), FakeRaw(dark), FakeRaw(normal)],
        ):
            sat = frame_exposure.frame_exposure_profile("fake-sat.cr3")
            drk = frame_exposure.frame_exposure_profile("fake-dark.cr3")
            nrm = frame_exposure.frame_exposure_profile("fake-normal.cr3")
        self.assertEqual(sat["classification"], "saturated")
        self.assertIsNotNone(sat["warning"])
        self.assertEqual(drk["classification"], "dark")
        self.assertEqual(nrm["classification"], "normal")
        self.assertIsNone(nrm["warning"])

    def test_batch2_shutter_tiers_follow_exposure_amount(self):
        from camera_based_rgbww_optimizer.optimization import guide11

        # Measured anchors: r4095 and the G9 white anchor (cw4095/ww4095)
        # both pass at 1/400; mixed white+color tiers on the conservative
        # brightness proxy max(color)+max(white). Multi-channel dimmed
        # secants saturate at 1/8 -> 1/125. A single active color channel
        # is an extreme-dynamic-range target: r2048 sat at the sensor cap
        # in block_06 R at 1/8 and starved B below the near-noise floor at
        # 1/125; the measured in-window legal shutter is 1/25.
        cases = {
            "fullscale": ({"cw": 0, "ww": 0, "r": 4095, "g": 1024, "b": 1024}, "1/400"),
            "dimmed_secant": ({"cw": 0, "ww": 0, "r": 1280, "g": 399, "b": 399}, "1/125"),
            "single_channel_red": ({"cw": 0, "ww": 0, "r": 2048, "g": 0, "b": 0}, "1/25"),
            "single_channel_blue": ({"cw": 0, "ww": 0, "r": 0, "g": 0, "b": 1600}, "1/25"),
            "pure_white": ({"cw": 4095, "ww": 4095, "r": 0, "g": 0, "b": 0}, "1/400"),
            "white_color_mix_low_sat": ({"cw": 3199, "ww": 3076, "r": 242, "g": 1696, "b": 2253}, "1/400"),
            "faint_color": ({"cw": 0, "ww": 0, "r": 500, "g": 100, "b": 100}, "1/30"),
            "very_faint": ({"cw": 0, "ww": 0, "r": 200, "g": 50, "b": 50}, "1/8"),
        }
        for label, (command, expected) in cases.items():
            self.assertEqual(
                guide11.c1_strip_shutter_for_command(command), expected, label
            )


class Guide11C1ConfirmPlanTests(unittest.TestCase):
    @staticmethod
    def _batch2_analysis():
        def target(hue, sat, improved, best_cmd=None, fallback_id=None):
            entry = {
                "hue": hue,
                "sat": sat,
                "improved_vs_batch1": improved,
                "batch1_fallback": {"capture_id": fallback_id, "z_distance_to_ray": 0.5},
                "best": {
                    "capture_id": f"b2-h{hue}-s{sat}",
                    "command": best_cmd,
                    "z_distance_to_ray": 0.4,
                } if best_cmd else None,
            }
            return entry

        return {
            "schema": "guide11_c1_batch2_analysis_v1",
            "targets": [
                target(0, 50, True, best_cmd={"cw": 0, "ww": 0, "r": 3835, "g": 903, "b": 903}),
                target(0, 100, False, fallback_id="008-strip-fallback-h0-s100"),
                target(60, 50, True, best_cmd={"cw": 9, "ww": 9, "r": 4095, "g": 4095, "b": 974}),
                target(60, 100, False, fallback_id="019-strip-fallback-h60-s100"),
                target(180, 50, False, fallback_id="025-strip-fallback-h180-s50"),
                target(180, 100, False, fallback_id="031-strip-fallback-h180-s100"),
                target(240, 50, False, fallback_id="037-strip-fallback-h240-s50"),
                target(240, 100, False, fallback_id="043-strip-fallback-h240-s100"),
            ],
        }

    @staticmethod
    def _batch1_root(tmp: Path):
        root = tmp / "batch1"
        root.mkdir()
        rows = []
        fallback_commands = {
            "008-strip-fallback-h0-s100": {"cw": 0, "ww": 0, "r": 2048, "g": 0, "b": 0},
            "019-strip-fallback-h60-s100": {"cw": 0, "ww": 0, "r": 4095, "g": 4095, "b": 1024},
            "025-strip-fallback-h180-s50": {"cw": 0, "ww": 0, "r": 1024, "g": 4095, "b": 4095},
            "031-strip-fallback-h180-s100": {"cw": 0, "ww": 0, "r": 1024, "g": 4095, "b": 4095},
            "037-strip-fallback-h240-s50": {"cw": 0, "ww": 0, "r": 1024, "g": 2048, "b": 4095},
            "043-strip-fallback-h240-s100": {"cw": 0, "ww": 0, "r": 1024, "g": 2048, "b": 4095},
        }
        for capture_id, command in fallback_commands.items():
            rows.append({
                "capture_id": capture_id,
                "source_id": "strip",
                "plan_step": {"command": command},
            })
        rows.append({
            "capture_id": "999-ray-ignored",
            "source_id": "ray",
            "plan_step": {"command": {"hue": 0, "sat": 100}},
        })
        (root / "captures.jsonl").write_text(
            "\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8"
        )
        return root

    def test_confirm_plan_structure_and_selection(self):
        with tempfile.TemporaryDirectory() as tmp_name:
            tmp = Path(tmp_name)
            analysis_path = tmp / "batch2-analysis.json"
            analysis_path.write_text(
                json.dumps(self._batch2_analysis()), encoding="utf-8"
            )
            batch1_root = self._batch1_root(tmp)
            plan = guide11.build_guide11_c1_confirm_plan(analysis_path, batch1_root)

        self.assertEqual(len(plan["captures"]), 32)
        self.assertEqual(plan["guide_experiment_id"], "GUIDE11_C1_CONFIRM_V1")
        self.assertEqual(plan["execution_authorization"]["schema"], "direct_guide11_c1_confirm_v1")
        # Authorization stays with the operator CLI grant, never self-verified.
        self.assertFalse(plan["execution_authorization"]["human_authorization_verified"])
        self.assertEqual(
            plan["execution_authorization"]["device_use_granted_by"],
            "operator_cli_allow_device_control",
        )
        self.assertEqual(plan["timing_resolution"], "guide11_c1confirm_reset600_D120")
        self.assertEqual(plan["cold_proxy_wait_s"], 600)
        # Every capture is a full independent FAST cycle.
        self.assertTrue(all(s["requested_elapsed_s"] == 120 for s in plan["captures"]))

        by_target = {}
        for step in plan["captures"]:
            by_target.setdefault((step["c1_hue"], step["c1_sat"]), []).append(step)
        self.assertEqual(len(by_target), 8)
        for (hue, sat), steps in by_target.items():
            self.assertEqual(
                [s["role"].rsplit("_", 1)[-1] for s in steps],
                ["before", "1", "2", "after"],
                f"h{hue}/s{sat} bracket order",
            )
            sources = [s["source_id"] for s in steps]
            self.assertEqual(sources, ["ray", "strip", "strip", "ray"])
            for step in steps:
                self.assertEqual(step["strip_zero_required"], step["source_id"] == "ray")
                self.assertEqual(step["ray_zero_required"], step["source_id"] == "strip")
            # Both strip confirms repeat one identical command.
            self.assertEqual(steps[1]["command"], steps[2]["command"])
            self.assertEqual(steps[1]["exact_command_hash"], steps[2]["exact_command_hash"])

        # Improved targets use the batch-2 command; fallback targets resolve
        # the command from the batch-1 run root, not from the analysis JSON.
        self.assertEqual(
            by_target[(0, 50)][1]["command"],
            {"cw": 0, "ww": 0, "r": 3835, "g": 903, "b": 903},
        )
        self.assertEqual(
            by_target[(0, 100)][1]["command"],
            {"cw": 0, "ww": 0, "r": 2048, "g": 0, "b": 0},
        )
        self.assertEqual(
            by_target[(240, 100)][1]["command"],
            {"cw": 0, "ww": 0, "r": 1024, "g": 2048, "b": 4095},
        )

        # Exposure-amount shutter tiers: full-scale color keeps 1/400; the
        # single-channel r2048 takes the measured in-window 1/25 (R sat at
        # the cap at 1/8, B starved at 1/125).
        self.assertEqual(by_target[(0, 50)][1]["nominal_shutter"], "1/400")
        self.assertEqual(by_target[(0, 100)][1]["nominal_shutter"], "1/25")
        self.assertEqual(by_target[(60, 100)][1]["nominal_shutter"], "1/400")

        contract = {
            (t["hue"], t["sat"]): t for t in plan["analysis_contract"]["targets"]
        }
        self.assertEqual(contract[(0, 50)]["selection_batch"], "batch2")
        self.assertEqual(contract[(0, 100)]["selection_batch"], "batch1_fallback")
        self.assertTrue(
            contract[(0, 50)]["selection_frame_is_not_independent_confirmation"]
        )
        self.assertEqual(contract[(0, 100)]["independent_confirmations_required"], 2)

    def test_missing_fallback_capture_rejected(self):
        with tempfile.TemporaryDirectory() as tmp_name:
            tmp = Path(tmp_name)
            analysis = self._batch2_analysis()
            analysis["targets"][1]["batch1_fallback"]["capture_id"] = "nonexistent"
            analysis_path = tmp / "batch2-analysis.json"
            analysis_path.write_text(json.dumps(analysis), encoding="utf-8")
            batch1_root = self._batch1_root(tmp)
            with self.assertRaises(ValueError):
                guide11.build_guide11_c1_confirm_plan(analysis_path, batch1_root)

    def test_recovery_suffix_skips_complete_targets_and_rebrackets_partial(self):
        with tempfile.TemporaryDirectory() as tmp_name:
            tmp = Path(tmp_name)
            analysis_path = tmp / "batch2-analysis.json"
            analysis_path.write_text(
                json.dumps(self._batch2_analysis()), encoding="utf-8"
            )
            batch1_root = self._batch1_root(tmp)

            failed = tmp / "failed-run"
            (failed / "measurements").mkdir(parents=True)
            rows = []
            # H0/S50 complete bracket (all four roles, measurements present).
            for capture_id, role in (
                ("000-ray-guide11-c1c-h0-s50-ray_q_before", "ray_c1c_h0_s50_ray_q_before"),
                ("001-strip-guide11-c1c-h0-s50-confirm_1", "strip_c1c_h0_s50_confirm_1"),
                ("002-strip-guide11-c1c-h0-s50-confirm_2", "strip_c1c_h0_s50_confirm_2"),
                ("003-ray-guide11-c1c-h0-s50-ray_q_after", "ray_c1c_h0_s50_ray_q_after"),
                # H0/S100 only its q_before -> partial, must be re-bracketed.
                ("004-ray-guide11-c1c-h0-s100-ray_q_before", "ray_c1c_h0_s100_ray_q_before"),
            ):
                rows.append({
                    "capture_id": capture_id,
                    "source_id": role.split("_")[0],
                    "plan_step": {"c1_hue": int(role.split("_h")[1].split("_")[0]),
                                   "c1_sat": int(role.split("_s")[1].split("_")[0]),
                                   "role": role},
                })
                (failed / "measurements" / f"{capture_id}.patch-statistics.json").write_text(
                    "{}", encoding="utf-8"
                )
            (failed / "captures.jsonl").write_text(
                "\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8"
            )

            suffix = guide11.build_guide11_c1_confirm_recovery_suffix(
                analysis_path, batch1_root, failed
            )

        self.assertEqual(suffix["variant"], "guide11-c1-best-repeat-confirmation-recovery-suffix")
        self.assertEqual(len(suffix["captures"]), 28)  # 7 targets x 4
        target_keys = {(s["c1_hue"], s["c1_sat"]) for s in suffix["captures"]}
        self.assertNotIn((0, 50), target_keys)   # complete -> kept in failed root
        self.assertIn((0, 100), target_keys)     # partial -> re-bracketed whole
        self.assertEqual(
            suffix["recovery"]["completed_targets_kept_in_prior_roots"],
            [{"hue": 0, "sat": 50}],
        )
        self.assertEqual(len(suffix["recovery"]["completed_run_roots"]), 1)
        # Every bracket in the suffix is complete (ray/strip/strip/ray).
        by_target = {}
        for step in suffix["captures"]:
            by_target.setdefault((step["c1_hue"], step["c1_sat"]), []).append(step)
        for steps in by_target.values():
            self.assertEqual([s["source_id"] for s in steps], ["ray", "strip", "strip", "ray"])
        # Renumbered ids stay unique and carry the suffix marker.
        ids = [s["capture_id"] for s in suffix["captures"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all("-suffix-" in i for i in ids))
        # Corrected shutter: the single-channel r2048 takes 1/25.
        h0s100 = next(s for s in by_target[(0, 100)] if s["source_id"] == "strip")
        self.assertEqual(h0s100["nominal_shutter"], "1/25")


class Guide11PeriodicHueSatModelTests(unittest.TestCase):
    @staticmethod
    def _anchors():
        def command_for(hue, sat):
            # Smooth-ish periodic ground truth per channel, kept inside the
            # 12-bit command range at both SAT extremes.
            import math as _m
            t = 2 * _m.pi * hue / 360
            scale = 0.5 + sat / 100.0
            return {
                "r": int(2000 + 1100 * _m.cos(t) * scale),
                "g": int(1500 + 900 * _m.sin(t) * scale),
                "b": int(1000 + 550 * _m.cos(2 * t) * scale),
                "cw": int(300 * (1 - sat / 100.0)),
                "ww": int(250 * (1 - sat / 100.0)),
            }

        rows = []
        for sat in (50, 100):
            order_hues = (0, 60, 120, 180, 240, 300) if sat == 50 else (0, 90, 180, 270)
            for hue in order_hues:
                rows.append({
                    "hue": hue, "sat": sat,
                    "command": command_for(hue, sat),
                    "source": f"test-h{hue}-s{sat}",
                })
        return rows

    def test_fit_and_periodic_interpolation(self):
        model = guide11.fit_periodic_hue_sat_command_model(
            self._anchors(), white_layer={"r": 0, "g": 0, "b": 0, "cw": 1200, "ww": 1200}
        )
        # SAT layers with enough anchors are periodic-fitted, not anchor-only.
        self.assertFalse(model["layers"]["50"]["anchor_only"])
        self.assertEqual(model["layers"]["50"]["harmonic_order"], 2)
        self.assertEqual(model["layers"]["100"]["harmonic_order"], 1)
        # Anchor hues reproduce their commands up to fit residual; the S50
        # layer carries order-2 harmonics (6 anchors), the S100 layer only
        # supports order 1 (4 anchors).
        anchor = model["layers"]["50"]["anchor_commands"]["180"]
        out = guide11.interpolate_hsi_command(model, 180, 50)
        for channel, value in anchor.items():
            self.assertLessEqual(abs(out["command"][channel] - value), 8, channel)
        self.assertTrue(out["hue_applicable"])
        # 0/360 periodicity: same command.
        at_zero = guide11.interpolate_hsi_command(model, 0.0, 70)
        at_three_sixty = guide11.interpolate_hsi_command(model, 360.0, 70)
        self.assertEqual(at_zero["command"], at_three_sixty["command"])
        # Between-layer SAT interpolation is bounded by the layer commands.
        mid = guide11.interpolate_hsi_command(model, 45.0, 75)["command"]
        low = guide11.interpolate_hsi_command(model, 45.0, 50)["command"]
        high = guide11.interpolate_hsi_command(model, 45.0, 100)["command"]
        for channel in mid:
            self.assertTrue(
                min(low[channel], high[channel]) - 8 <= mid[channel]
                <= max(low[channel], high[channel]) + 8,
                channel,
            )

    def test_sat0_returns_white_and_hue_not_applicable(self):
        model = guide11.fit_periodic_hue_sat_command_model(
            self._anchors(), white_layer={"r": 0, "g": 0, "b": 0, "cw": 999, "ww": 888}
        )
        out = guide11.interpolate_hsi_command(model, 123.0, 0.0)
        self.assertEqual(out["command"], {"r": 0, "g": 0, "b": 0, "cw": 999, "ww": 888})
        self.assertFalse(out["hue_applicable"])
        no_white = guide11.fit_periodic_hue_sat_command_model(self._anchors())
        with self.assertRaises(ValueError):
            # No fitted layer covers SAT 5 and no white layer was provided.
            guide11.interpolate_hsi_command(no_white, 123.0, 5.0)

    def test_low_sat_blends_white_toward_s50_hue_first(self):
        model = guide11.fit_periodic_hue_sat_command_model(
            self._anchors(), white_layer={"r": 0, "g": 0, "b": 0, "cw": 1000, "ww": 1000}
        )
        white = guide11.interpolate_hsi_command(model, 45.0, 0.0)["command"]
        s50 = guide11.interpolate_hsi_command(model, 45.0, 50)["command"]
        s25 = guide11.interpolate_hsi_command(model, 45.0, 25)["command"]
        for channel in s25:
            low, high = min(white[channel], s50[channel]), max(white[channel], s50[channel])
            self.assertTrue(low <= s25[channel] <= high, channel)
            # halfway in SAT between the white and S50 endpoints
            self.assertLessEqual(abs(s25[channel] - (white[channel] + s50[channel]) / 2), 2, channel)
        # Hue continuity: neighbouring hues at fixed low SAT stay close.
        a = guide11.interpolate_hsi_command(model, 44.0, 20)["command"]
        b = guide11.interpolate_hsi_command(model, 46.0, 20)["command"]
        self.assertLess(max(abs(a[c] - b[c]) for c in a), 40)

    def test_anchor_only_layer_refuses_interpolation(self):
        sparse = [
            {"hue": 0, "sat": 25, "command": {"r": 100, "g": 0, "b": 0, "cw": 0, "ww": 0}, "source": "x"},
            {"hue": 120, "sat": 25, "command": {"r": 0, "g": 100, "b": 0, "cw": 0, "ww": 0}, "source": "x"},
        ]
        model = guide11.fit_periodic_hue_sat_command_model(sparse)
        self.assertTrue(model["layers"]["25"]["anchor_only"])
        with self.assertRaises(ValueError):
            guide11.interpolate_hsi_command(model, 60.0, 25.0)

    def test_clipping_reported(self):
        model = guide11.fit_periodic_hue_sat_command_model(
            self._anchors(), white_layer={"r": 1, "g": 1, "b": 1, "cw": 1, "ww": 1}
        )
        # Ground truth peaks above 4095 nowhere; force clipping by scaling an
        # anchor up before fitting.
        big = self._anchors()
        big[0]["command"]["r"] = 4095
        big[1]["command"]["r"] = 4095
        model_big = guide11.fit_periodic_hue_sat_command_model(big)
        clipped_seen = False
        for hue in range(0, 360, 5):
            out = guide11.interpolate_hsi_command(model_big, hue, 50)
            self.assertLessEqual(max(out["command"].values()), 4095)
            clipped_seen = clipped_seen or bool(out["clipped"])
        self.assertTrue(clipped_seen)


class Guide11C4HoldoutPlanTests(unittest.TestCase):
    def test_c4_plan_targets_frozen_with_model_commands(self):
        anchors = Guide11PeriodicHueSatModelTests._anchors()
        model = guide11.fit_periodic_hue_sat_command_model(
            anchors, white_layer={"r": 0, "g": 0, "b": 0, "cw": 1000, "ww": 1000}
        )
        plan = guide11.build_guide11_c4_holdout_plan(model)

        self.assertEqual(plan["guide_experiment_id"], "GUIDE11_C4_EXPERIENCE_HOLDOUT_V1")
        self.assertEqual(plan["execution_authorization"]["schema"], "direct_guide11_c4_holdout_v1")
        self.assertFalse(plan["execution_authorization"]["human_authorization_verified"])
        self.assertEqual(plan["timing_resolution"], "guide11_c4holdout_reset600_D120")
        self.assertEqual(plan["cold_proxy_wait_s"], 600)

        contract = plan["analysis_contract"]
        self.assertEqual(len(contract["targets"]), 10)
        hues = [t["hue"] for t in contract["targets"]]
        sats = {t["sat"] for t in contract["targets"]}
        # Six 60-degree sectors covered by non-main hues, plus 350, plus
        # low-SAT 20/10 holdouts.
        self.assertEqual(sorted(set(hues) & {30, 90, 150, 210, 270, 330}), [30, 90, 150, 210, 270, 330])
        self.assertIn(350, hues)
        self.assertIn(280, hues)
        self.assertEqual({20, 10} <= sats, True)
        self.assertTrue(contract["targets_frozen_before_capture"])

        # 10 targets x (ray, strip, ray) = 30 captures; every strip command
        # comes from the model and differs from a nearest-anchor copy at
        # non-anchor hues.
        self.assertEqual(len(plan["captures"]), 30)
        by_target = {}
        for step in plan["captures"]:
            by_target.setdefault((step["c1_hue"], step["c1_sat"]), []).append(step)
        for (hue, sat), steps in by_target.items():
            self.assertEqual([s["source_id"] for s in steps], ["ray", "strip", "ray"])
            strip = steps[1]
            expected = guide11.interpolate_hsi_command(model, float(hue), float(sat))
            self.assertEqual(strip["command"], expected["command"])
        # Ray shutter tiers: white-dominant fastest, S100 slowest.
        def ray_shutter(sat):
            return by_target[(90, sat)][0]["nominal_shutter"]
        self.assertEqual(ray_shutter(20), "1/16000")
        self.assertEqual(ray_shutter(75), "1/3200")
        self.assertEqual(guide11._c4_ray_shutter_for_sat(50), "1/6400")
        self.assertEqual(guide11._c4_ray_shutter_for_sat(100), "1/1600")
        # Non-anchor hue commands are model interpolations, not anchor copies.
        anchor_hues = set(model["layers"]["50"]["anchor_hues"]) | set(model["layers"]["100"]["anchor_hues"])
        all_anchor_commands = {
            tuple(sorted((k, anchor_cmd.get(k, 0)) for k in ("r", "g", "b", "cw", "ww")))
            for layer in model["layers"].values()
            for anchor_cmd in layer["anchor_commands"].values()
        }
        for (hue, _sat), steps in by_target.items():
            if hue in anchor_hues:
                continue
            key = tuple(sorted(steps[1]["command"].items()))
            self.assertNotIn(key, all_anchor_commands)


class Guide11C2S25PlanTests(unittest.TestCase):
    def test_c2_s25_plan_uses_c2_identity_and_compression_commands(self):
        anchors = Guide11PeriodicHueSatModelTests._anchors()
        model = guide11.fit_periodic_hue_sat_command_model(
            anchors, white_layer={"r": 0, "g": 0, "b": 0, "cw": 1200, "ww": 1200}
        )
        plan = guide11.build_guide11_c2_s25_plan(model)

        self.assertEqual(plan["guide_experiment_id"], "GUIDE11_C2_SAT_REACHABILITY_S25_V1")
        self.assertEqual(plan["stage"], "GUIDE11-C2-SAT-REACHABILITY-S25")
        contract = plan["analysis_contract"]
        self.assertEqual(contract["method"], "guide11_c2_sat_reachability")
        self.assertEqual(contract["descent_tier"], 25)
        self.assertEqual(
            [(t["hue"], t["sat"]) for t in contract["targets"]],
            [(0, 25), (60, 25), (180, 25), (240, 25)],
        )
        for target in contract["targets"]:
            self.assertEqual(
                target["checks"],
                ["bracket_consistency", "product_layer_validity", "equivalent_menu_sat_error"],
            )

        # 4 targets x (ray, strip, ray) = 12 captures with c2 identity.
        self.assertEqual(len(plan["captures"]), 12)
        by_target = {}
        for step in plan["captures"]:
            by_target.setdefault((step["c1_hue"], step["c1_sat"]), []).append(step)
            self.assertIn("-guide11-c2-h", step["capture_id"])
            self.assertTrue(step["state_id"].startswith("C2_H"))
            self.assertIn("_c2_h", step["role"])
        for (hue, _sat), steps in by_target.items():
            self.assertEqual([s["source_id"] for s in steps], ["ray", "strip", "ray"])
            # Strip commands come from the model's white->S50 compression path.
            expected = guide11.interpolate_hsi_command(model, float(hue), 25.0)
            strip = steps[1]
            self.assertEqual(strip["command"], expected["command"])
            # Ray side requests the same S25 menu point at the white-dominant tier.
            self.assertEqual(steps[0]["command"], {"hue": hue, "sat": 25, "intensity_percent": 100.0})
            self.assertEqual(steps[0]["nominal_shutter"], "1/16000")

    def test_c4_default_plan_ids_unchanged_by_label_parameter(self):
        anchors = Guide11PeriodicHueSatModelTests._anchors()
        model = guide11.fit_periodic_hue_sat_command_model(
            anchors, white_layer={"r": 0, "g": 0, "b": 0, "cw": 1200, "ww": 1200}
        )
        plan = guide11.build_guide11_c4_holdout_plan(model)
        first = plan["captures"][0]
        self.assertIn("-guide11-c4-h", first["capture_id"])
        self.assertTrue(first["state_id"].startswith("C4_H"))
        self.assertEqual(plan["guide_experiment_id"], "GUIDE11_C4_EXPERIENCE_HOLDOUT_V1")
