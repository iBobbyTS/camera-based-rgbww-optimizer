from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from camera_based_rgbww_optimizer.optimization import guide9_white70_recovery as recovery


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value), encoding="utf-8")


class Guide9White70RecoveryTests(unittest.TestCase):
    def make_parent(self, root: Path) -> Path:
        parent = root / "parent"
        (parent / "camera").mkdir(parents=True)
        (parent / "measurements").mkdir()
        captures = []
        physical = []
        steps = []
        for index, source in enumerate(("ray", "strip", "strip")):
            capture_id = f"{index:03d}-{source}-sample"
            step = {"capture_id": capture_id, "source_id": source, "exposure_cache_key": f"{source}-key-{index}", "nominal_shutter": "1/80"}
            steps.append(step)
            if index < 2:
                raw = parent / "camera" / f"{capture_id}.cr3"
                report = parent / "measurements" / f"{capture_id}.json"
                raw.write_bytes(b"raw")
                write_json(report, {"patches": []})
                captures.append({"capture_id": capture_id, "plan_step": step, "capture": {"saved_file": f"/Volumes/4T/old/{raw.name}", "patch_statistics": f"/Volumes/4T/old/{report.name}", "capture": {"byte_count": 3, "saved_file": f"/Volumes/4T/old/{raw.name}"}}})
                physical.append({"capture_id": capture_id})
        write_json(parent / "experiment-spec.json", {"capture_ids": [step["capture_id"] for step in steps], "captures": steps, "inputs": {}, "analysis_contract": {"target_contracts": []}})
        write_json(parent / "run.json", {"accepted_formal_count": 2, "cleanup": "pass"})
        write_json(parent / "all-off-python.json", {"status": "pass", "steps": [{"ok": True}]})
        (parent / "captures.jsonl").write_text("".join(json.dumps(row) + "\n" for row in captures), encoding="utf-8")
        (parent / "physical-returns.jsonl").write_text("".join(json.dumps(row) + "\n" for row in physical), encoding="utf-8")
        return parent

    def test_validate_prefix_accepts_exact_retained_prefix(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = recovery.validate_prefix(self.make_parent(Path(temporary)))
        self.assertEqual(result["prefix_count"], 2)
        self.assertEqual(result["remaining_count"], 1)
        self.assertEqual(result["first_missing_capture_id"], "002-strip-sample")

    def test_validate_prefix_rejects_noncanonical_physical_ledger(self):
        with tempfile.TemporaryDirectory() as temporary:
            parent = self.make_parent(Path(temporary))
            (parent / "physical-returns.jsonl").write_text(json.dumps({"capture_id": "001-strip-sample"}) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "exact frozen-plan prefix"):
                recovery.validate_prefix(parent)

    def test_portable_capture_maps_macos_paths_to_retained_root(self):
        row = {"capture": {"saved_file": "/Volumes/4T/old/a.cr3", "patch_statistics": "/Volumes/4T/old/a.json", "capture": {"saved_file": "/Volumes/4T/old/a.cr3"}}}
        mapped = recovery._portable_capture(row, Path("D:/rgbww-optimizer/run"))
        self.assertEqual(Path(mapped["capture"]["saved_file"]).name, "a.cr3")
        self.assertEqual(Path(mapped["capture"]["patch_statistics"]).name, "a.json")
        self.assertIn("rgbww-optimizer", mapped["capture"]["saved_file"])

    def test_rebuild_probe_contracts_derives_four_bounded_free_channel_steps(self):
        channels = ("cw", "ww", "r", "g", "b")
        base = {"cw": 4095, "ww": 10, "r": 20, "g": 30, "b": 40}
        captures = [{"target_cct": 6500, "target_gm": 200, "role": "strip_base", "command": base}]
        for channel in channels[1:]:
            command = dict(base)
            command[channel] += 256
            captures.append({"target_cct": 6500, "target_gm": 200, "role": f"strip_probe_{channel}", "command": command})
        plan = {
            "captures": captures,
            "analysis_contract": {"target_contracts": [{
                "cct": 6500, "gm": 200, "active_channel": "cw",
                "base_command": base, "probes": [],
            }]},
        }
        contracts = recovery.rebuild_probe_contracts(plan)
        self.assertEqual({probe["channel"] for probe in contracts[0]["probes"]}, set(channels[1:]))
        self.assertTrue(all(probe["delta_code"] == 256 for probe in contracts[0]["probes"]))

    def test_rebuild_probe_contracts_rejects_multichannel_probe(self):
        base = {"cw": 4095, "ww": 10, "r": 20, "g": 30, "b": 40}
        captures = [{"target_cct": 6500, "target_gm": 200, "role": "strip_base", "command": base}]
        for channel in ("ww", "r", "g", "b"):
            command = dict(base)
            command[channel] += 256
            if channel == "b":
                command["g"] += 1
            captures.append({"target_cct": 6500, "target_gm": 200, "role": f"strip_probe_{channel}", "command": command})
        plan = {
            "captures": captures,
            "analysis_contract": {"target_contracts": [{
                "cct": 6500, "gm": 200, "active_channel": "cw",
                "base_command": base, "probes": [],
            }]},
        }
        with self.assertRaisesRegex(ValueError, "one bounded channel step"):
            recovery.rebuild_probe_contracts(plan)

    def test_build_suffix_plan_keeps_only_missing_ids_and_rebuilds_budgets(self):
        with tempfile.TemporaryDirectory() as temporary:
            parent = self.make_parent(Path(temporary))
            plan = json.loads((parent / "experiment-spec.json").read_text())
            plan.update({"budgets": {}, "frozen_shutters": {}, "shutter_ledger_provenance": {}, "recovery_contract": {}})
            write_json(parent / "experiment-spec.json", plan)
            with patch.object(recovery, "_current_input_references", return_value={}), patch.object(recovery.measure, "validate_authorized_execution_plan"):
                suffix = recovery.build_suffix_plan(parent, data_root=Path(temporary))
        self.assertEqual(suffix["capture_ids"], ["002-strip-sample"])
        self.assertEqual(suffix["budgets"]["formal_cap"], 1)
        self.assertEqual(suffix["budgets"]["strip_cap"], 1)
        self.assertEqual(suffix["recovery_contract"]["parent_capture_count"], 2)

    def test_build_resume_plan_slices_an_interrupted_checkpoint(self):
        with tempfile.TemporaryDirectory() as temporary:
            parent = self.make_parent(Path(temporary))
            run = json.loads((parent / "run.json").read_text())
            run["status"] = "running"
            write_json(parent / "run.json", run)
            with patch.object(recovery, "_current_input_references", return_value={}), patch.object(
                recovery.measure, "validate_authorized_execution_plan",
            ):
                resumed = recovery.build_resume_plan(parent, data_root=Path(temporary))
        self.assertEqual(resumed["capture_ids"], ["002-strip-sample"])
        self.assertEqual(resumed["budgets"]["formal_cap"], 1)
        self.assertEqual(resumed["recovery_contract"]["schema"], recovery.CHECKPOINT_SCHEMA)
        self.assertEqual(resumed["recovery_contract"]["parent_capture_count"], 2)

    def test_validate_checkpoint_rejects_completed_root(self):
        with tempfile.TemporaryDirectory() as temporary:
            parent = self.make_parent(Path(temporary))
            run = json.loads((parent / "run.json").read_text())
            run["status"] = "complete"
            write_json(parent / "run.json", run)
            with self.assertRaisesRegex(ValueError, "already complete"):
                recovery.validate_checkpoint(parent)

    def test_build_resume_plan_is_offline_and_reports_missing_suffix(self):
        with tempfile.TemporaryDirectory() as temporary:
            parent = self.make_parent(Path(temporary))
            run = json.loads((parent / "run.json").read_text())
            run["status"] = "running"
            write_json(parent / "run.json", run)
            with patch.object(recovery, "_current_input_references", return_value={}), patch.object(
                recovery.measure, "validate_authorized_execution_plan",
            ):
                result = recovery.main([
                    "inspect-resume", "--run-root", str(parent),
                    "--data-root", temporary,
                ])
        self.assertEqual(result, 0)

    def test_build_candidate_plan_creates_one_exact_pair_per_analysis_node(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            parent = root / "parent"
            parent.mkdir()
            base = {"cw": 4095, "ww": 20, "r": 30, "g": 40, "b": 50}
            ray = {
                "target_cct": 6500, "target_gm": 200, "role": "ray_reference",
                "source_id": "ray", "command": {"mode": "cct"},
                "exposure_cache_key": "ray-white-6500-gm200", "nominal_shutter": "1/2500",
            }
            strip = {
                "target_cct": 6500, "target_gm": 200, "role": "strip_base",
                "source_id": "strip", "command": base,
                "exposure_cache_key": "strip-white-6500-gm200", "nominal_shutter": "1/80",
            }
            plan = {
                "schema": "p7_thermal_diagnostic_plan_v2",
                "captures": [ray, strip], "inputs": {}, "budgets": {},
                "frozen_shutters": {}, "shutter_ledger_provenance": {},
                "execution_authorization": {},
                "analysis_contract": {"target_contracts": [{
                    "cct": 6500, "gm": 200, "active_channel": "cw", "base_command": base,
                }]},
            }
            write_json(parent / "experiment-spec.json", plan)
            candidate = {**base, "ww": 25}
            analysis = root / "analysis.json"
            write_json(analysis, {
                "status": "candidates_preregistered", "node_count": 1, "capture_count": 6,
                "global_model_refit": False, "default_lut_installation": False,
                "recovery_evidence": {
                    "combined_capture_count": 6, "rejected_dark_capture_included": False,
                    "diagnostic_captures_included": False,
                },
                "nodes": [{"cct": 6500, "gm": 200, "candidate": {"command": candidate}}],
            })
            with patch.object(recovery, "_current_input_references", return_value={}), patch.object(
                recovery.measure, "validate_authorized_execution_plan",
            ), patch.object(
                recovery.thermal, "expected_native_raw_ambient_policy", return_value={"owner": "current"},
            ):
                result = recovery.build_candidate_plan(parent, analysis, data_root=root)
        self.assertEqual(result["budgets"]["formal_cap"], 2)
        self.assertEqual([row["source_id"] for row in result["captures"]], ["ray", "strip"])
        self.assertEqual(result["captures"][1]["command"], candidate)
        self.assertEqual(result["analysis_contract"]["target_contracts"][0]["source_order"], ["ray", "strip"])
        self.assertEqual(result["candidate_contract"]["node_count"], 1)
        self.assertEqual(result["experiment_id"], recovery.thermal.TD_C)
        self.assertEqual(
            result["guide_experiment_id"],
            "GUIDE9_WHITE12_LOCAL_JACOBIAN_CANDIDATES_V1",
        )
        self.assertEqual(result["analysis_contract"]["target_contracts"][0]["cct_tolerance_mired"], 1.0)
        self.assertEqual(result["native_raw_ambient_policy"], {"owner": "current"})

    def test_build_candidate_plan_rejects_candidate_that_changes_active_channel(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            parent = root / "parent"
            parent.mkdir()
            base = {"cw": 4095, "ww": 20, "r": 30, "g": 40, "b": 50}
            write_json(parent / "experiment-spec.json", {
                "captures": [], "analysis_contract": {"target_contracts": [{
                    "cct": 6500, "gm": 200, "active_channel": "cw", "base_command": base,
                }]},
            })
            analysis = root / "analysis.json"
            write_json(analysis, {
                "status": "candidates_preregistered", "node_count": 1, "capture_count": 6,
                "global_model_refit": False, "default_lut_installation": False,
                "recovery_evidence": {
                    "combined_capture_count": 6, "rejected_dark_capture_included": False,
                    "diagnostic_captures_included": False,
                },
                "nodes": [{"cct": 6500, "gm": 200, "candidate": {
                    "command": {**base, "cw": 4094},
                }}],
            })
            with self.assertRaisesRegex(ValueError, "full-scale active channel"):
                recovery.build_candidate_plan(parent, analysis, data_root=root)


    def test_combine_analyze_uses_exact_suffix_and_portable_paths(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            parent = self.make_parent(root)
            suffix = root / "suffix"
            (suffix / "camera").mkdir(parents=True)
            (suffix / "measurements").mkdir()
            capture_id = "002-strip-sample"
            raw = suffix / "camera" / f"{capture_id}.cr3"
            report = suffix / "measurements" / f"{capture_id}.json"
            raw.write_bytes(b"raw")
            write_json(report, {"patches": []})
            write_json(suffix / "run.json", {"status": "complete", "cleanup": "pass"})
            write_json(suffix / "experiment-spec.json", {"recovery_contract": {"schema": recovery.RECOVERY_SCHEMA}})
            suffix_row = {
                "capture_id": capture_id,
                "capture": {
                    "saved_file": "/Volumes/4T/new/002-strip-sample.cr3",
                    "patch_statistics": "/Volumes/4T/new/002-strip-sample.json",
                    "capture": {"saved_file": "/Volumes/4T/new/002-strip-sample.cr3"},
                },
            }
            (suffix / "captures.jsonl").write_text(json.dumps(suffix_row) + "\n", encoding="utf-8")
            output = root / "analysis.json"
            with patch.object(
                recovery.analyze,
                "analyze_guide9_white_local_probes",
                return_value={"status": "candidates_preregistered"},
            ) as analyze_call:
                result = recovery.combine_and_analyze(parent, suffix, output=output)
            self.assertEqual(result, output.resolve())
            combined = analyze_call.call_args.args[0]
            self.assertEqual([row["capture_id"] for row in combined], [
                "000-ray-sample", "001-strip-sample", "002-strip-sample",
            ])
            self.assertTrue(all("Volumes" not in row["capture"]["saved_file"] for row in combined))
            stored = json.loads(output.read_text())
            self.assertEqual(stored["recovery_evidence"]["combined_capture_count"], 3)
            self.assertEqual(stored["recovery_evidence"]["duplicate_capture_count"], 0)

    def test_combine_recovered_probe_series_preserves_three_segment_lineage(self):
        expected_ids = [f"{index:03d}-sample" for index in range(36)]

        def rows(ids: list[str]) -> list[dict[str, object]]:
            return [{"capture_id": capture_id, "capture": {
                "saved_file": f"/old/{capture_id}.cr3",
                "patch_statistics": f"/old/{capture_id}.json",
            }} for capture_id in ids]

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prefix, recovery_root, resume = root / "prefix", root / "recovery", root / "resume"
            for path in (prefix, recovery_root, resume):
                path.mkdir()
            prefix_plan = {
                "capture_ids": expected_ids,
                "captures": [],
                "analysis_contract": {"target_contracts": []},
            }
            write_json(prefix / "experiment-spec.json", prefix_plan)
            write_json(prefix / "run.json", {"status": "failed", "cleanup": "pass", "accepted_formal_count": 24})
            write_json(prefix / "failure.json", {"rejected_capture": {"capture_id": expected_ids[24]}})
            write_json(prefix / "all-off-python.json", {"status": "pass", "steps": [{"ok": True}]})
            (prefix / "captures.jsonl").write_text("".join(json.dumps(row) + "\n" for row in rows(expected_ids[:24])))
            (prefix / "physical-returns.jsonl").write_text("".join(
                json.dumps({"capture_id": capture_id}) + "\n" for capture_id in expected_ids[:25]
            ))
            recovery_plan = {
                "capture_ids": expected_ids[24:],
                "recovery_contract": {
                    "schema": recovery.REMAINING_PROBE_SCHEMA,
                    "immutable_prefix_root": str(prefix),
                },
            }
            write_json(recovery_root / "experiment-spec.json", recovery_plan)
            write_json(recovery_root / "run.json", {"status": "running", "cleanup": "pending", "accepted_formal_count": 7})
            (recovery_root / "captures.jsonl").write_text("".join(json.dumps(row) + "\n" for row in rows(expected_ids[24:31])))
            (recovery_root / "physical-returns.jsonl").write_text("".join(
                json.dumps({"capture_id": capture_id}) + "\n" for capture_id in expected_ids[24:31]
            ))
            resume_contract = {
                "schema": recovery.CHECKPOINT_SCHEMA,
                "parent_root": str(recovery_root),
                "parent_capture_count": 7,
                "first_missing_capture_id": expected_ids[31],
                "combined_capture_count": 12,
            }
            write_json(resume / "experiment-spec.json", {"recovery_contract": resume_contract})
            write_json(resume / "run.json", {"status": "complete", "cleanup": "pass", "accepted_formal_count": 5})
            (resume / "captures.jsonl").write_text("".join(json.dumps(row) + "\n" for row in rows(expected_ids[31:])))
            (resume / "physical-returns.jsonl").write_text("".join(
                json.dumps({"capture_id": capture_id}) + "\n" for capture_id in expected_ids[31:]
            ))
            output = root / "analysis.json"
            with patch.object(recovery, "rebuild_probe_contracts", return_value=[]), patch.object(
                recovery.analyze, "analyze_guide9_white_local_probes",
                return_value={"status": "candidates_preregistered", "capture_count": 36},
            ) as analyze_call:
                recovery.combine_recovered_probe_series(prefix, recovery_root, resume, output=output)
            combined = analyze_call.call_args.args[0]
            self.assertEqual([row["capture_id"] for row in combined], expected_ids)
            evidence = json.loads(output.read_text())["recovery_evidence"]
            self.assertEqual(evidence["segment_capture_counts"], [24, 7, 5])
            self.assertFalse(evidence["rejected_dark_capture_included"])


if __name__ == "__main__":
    unittest.main()
