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


if __name__ == "__main__":
    unittest.main()
