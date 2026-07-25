import contextlib
import io
import unittest

from camera_based_rgbww_optimizer.control import camera_remote, esphome, ray120c
from camera_based_rgbww_optimizer.control.local_lab_context import LOCAL_LAB_CONTEXT


class LocalLabCliContextTests(unittest.TestCase):
    def _help(self, callable_):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), self.assertRaises(SystemExit) as raised:
            callable_(["--help"])
        self.assertEqual(raised.exception.code, 0)
        return stdout.getvalue()

    def test_control_help_uses_shared_context_and_specific_actions(self):
        outputs = {
            "RGBWW ESPHome fixture": self._help(esphome._main),
            "Canon camera bridge": self._help(camera_remote.parse_args),
            "Amaran Ray120c": self._help(ray120c.main),
        }
        for action, output in outputs.items():
            self.assertIn(LOCAL_LAB_CONTEXT, " ".join(output.split()))
            self.assertIn(action, output)
            self.assertNotIn("--secret", output)
            self.assertNotIn("AMARAN_OPENAPI_SECRET", output)


if __name__ == "__main__":
    unittest.main()
