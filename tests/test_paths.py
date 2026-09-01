from pathlib import Path
import unittest

from camera_based_rgbww_optimizer.paths import (
    DATA_ROOT_ENV,
    PROJECT_ROOT,
    PROJECT_TMP_DIR,
    resolve_project_tmp_dir,
)


class PathsTests(unittest.TestCase):
    def test_project_root_points_to_repository_root(self):
        expected_root = Path(__file__).resolve().parents[1]
        self.assertEqual(PROJECT_ROOT, expected_root)
        self.assertTrue((PROJECT_ROOT / "pyproject.toml").exists())
        self.assertEqual(PROJECT_TMP_DIR, Path("D:/rgbww-optimizer"))

    def test_data_root_keeps_macos_default(self):
        self.assertEqual(
            resolve_project_tmp_dir({}, platform="posix"),
            Path("/Volumes/4T/temp/rgbww-optimizer"),
        )

    def test_data_root_environment_override_wins(self):
        self.assertEqual(
            resolve_project_tmp_dir({DATA_ROOT_ENV: "E:/lab-data"}, platform="nt"),
            Path("E:/lab-data"),
        )


if __name__ == "__main__":
    unittest.main()
