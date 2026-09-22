import hashlib
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
