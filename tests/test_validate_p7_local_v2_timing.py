import json
import tempfile
import unittest
from pathlib import Path

from camera_based_rgbww_optimizer.optimization import validate_p7_local_v2_timing as subject


class ValidateP7LocalV2TimingTests(unittest.TestCase):
    def test_generates_complete_fake_only_validation_tree(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = subject.generate_validation_artifacts(tempdir, "r0c")
            summary = json.loads((root / "validation-summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["status"], "pass")
            self.assertEqual(summary["counters"], {"device": 0, "network": 0, "env": 0, "all_off": 0})
            self.assertTrue((root / "plan.json").is_file())
            self.assertTrue((root / "valid-v2-response-fixture").is_dir())
            self.assertTrue((root / "malformed-response-fixtures").is_dir())
            self.assertTrue((root / "timing-reconstruction.json").is_file())
            self.assertTrue((root / "production-roundtrip-analysis.json").is_file())
            self.assertTrue(all(item["actual"] == "reject" for item in summary["negative_fixtures"]))
            self.assertFalse(list(Path(root).rglob("*.npy")))


if __name__ == "__main__":
    unittest.main()
