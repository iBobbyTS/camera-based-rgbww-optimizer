import base64
import os
import unittest
from unittest import mock

from camera_based_rgbww_optimizer.control import all_off


class AllOffTests(unittest.TestCase):
    def setUp(self):
        secret = base64.b64encode(bytes(range(32))).decode("ascii")
        self.environment = mock.patch.dict(os.environ, {"AMARAN_OPENAPI_SECRET": secret}, clear=True)
        self.environment.start()

    def tearDown(self):
        self.environment.stop()

    def test_turn_everything_off_turns_strip_off_then_ray_off(self):
        calls = []

        def strip_off():
            calls.append(("strip",))
            return {"red": 0, "green": 0, "blue": 0, "warm_white": 0, "cold_white": 0}

        def ray_get_cct(*, settings):
            calls.append(("ray_get", settings.timeout))
            return {"data": {"cct": 3200, "gm": 130}}

        def ray_set_cct(cct, **kwargs):
            calls.append(("ray_set", cct, kwargs))
            return {"code": 0, "data": {"cct": cct, "intensity": kwargs["intensity"], "gm": kwargs["gm"]}}

        steps = all_off.turn_everything_off(
            ray_timeout=7.0,
            strip_off_fn=strip_off,
            ray_get_cct_fn=ray_get_cct,
            ray_set_cct_fn=ray_set_cct,
        )

        self.assertTrue(all(step.ok for step in steps))
        self.assertEqual([step.name for step in steps], ["esphome", "ray120c"])
        self.assertEqual(calls[0], ("strip",))
        self.assertEqual(calls[1], ("ray_get", 7.0))
        self.assertEqual(calls[2][0], "ray_set")
        self.assertEqual(calls[2][1], 3200)
        self.assertEqual(calls[2][2]["intensity"], 0)
        self.assertEqual(calls[2][2]["gm"], 130)
        self.assertEqual(calls[2][2]["settings"].timeout, 7.0)

    def test_strip_failure_does_not_skip_ray_shutdown(self):
        calls = []

        def strip_off():
            calls.append(("strip",))
            raise RuntimeError("strip offline")

        def ray_get_cct(*, settings):
            calls.append(("ray_get",))
            return {"data": {"cct": 5600, "gm": 100}}

        def ray_set_cct(cct, **kwargs):
            calls.append(("ray_set", cct, kwargs["intensity"], kwargs["gm"]))
            return {"code": 0}

        steps = all_off.turn_everything_off(
            strip_off_fn=strip_off,
            ray_get_cct_fn=ray_get_cct,
            ray_set_cct_fn=ray_set_cct,
        )

        self.assertFalse(steps[0].ok)
        self.assertTrue(steps[1].ok)
        self.assertEqual(calls, [("strip",), ("ray_get",), ("ray_set", 5600, 0, 100)])

    def test_ray_shutdown_uses_default_fallback_when_current_cct_read_fails(self):
        calls = []

        def ray_get_cct(*, settings):
            calls.append(("ray_get",))
            raise ConnectionError("not reachable")

        def ray_set_cct(cct, **kwargs):
            calls.append(("ray_set", cct, kwargs["intensity"], kwargs["gm"]))
            return {"code": 0}

        steps = all_off.turn_everything_off(
            strip=False,
            ray_get_cct_fn=ray_get_cct,
            ray_set_cct_fn=ray_set_cct,
        )

        self.assertEqual(len(steps), 1)
        self.assertTrue(steps[0].ok)
        self.assertEqual(calls, [("ray_get",), ("ray_set", 5600, 0, 100)])
        self.assertIn("current_read_error", steps[0].detail)

    def test_ray_shutdown_uses_fallback_for_invalid_off_state_cct(self):
        calls = []

        def ray_get_cct(*, settings):
            return {"data": {"cct": 0, "gm": 0, "intensity": 0}}

        def ray_set_cct(cct, **kwargs):
            calls.append((cct, kwargs["intensity"], kwargs["gm"]))
            return {"code": 0}

        steps = all_off.turn_everything_off(
            strip=False,
            ray_get_cct_fn=ray_get_cct,
            ray_set_cct_fn=ray_set_cct,
        )

        self.assertTrue(steps[0].ok)
        self.assertEqual(calls, [(5600, 0, 0)])
        self.assertIn("invalid current CCT 0", steps[0].detail["current_read_error"])

    def test_empty_environment_uses_public_default_and_serializes_both_fake_outcomes(self):
        ray_settings = []

        def fail_ray(*_args, **kwargs):
            ray_settings.append(kwargs["settings"])
            raise RuntimeError("fake Ray failure")

        with mock.patch.dict(os.environ, {}, clear=True):
            steps = all_off.turn_everything_off(
                strip_off_fn=lambda: {"state": "off"},
                ray_set_cct_fn=fail_ray,
                ray_cct=5600,
                ray_gm=100,
            )

        rows = [step.to_jsonable() for step in steps]
        self.assertEqual([row["name"] for row in rows], ["esphome", "ray120c"])
        self.assertTrue(rows[0]["ok"])
        self.assertFalse(rows[1]["ok"])
        self.assertIn("fake Ray failure", rows[1]["error"])
        self.assertEqual(ray_settings[0].secret, all_off.ray120c.DEFAULT_OPENAPI_SECRET)
        self.assertNotIn(all_off.ray120c.DEFAULT_OPENAPI_SECRET, str(rows))

    def test_invalid_explicit_override_fails_before_ray_fake_adapter(self):
        ray_calls = []
        with mock.patch.dict(os.environ, {"AMARAN_OPENAPI_SECRET": "private-invalid-override"}, clear=True):
            with self.assertRaisesRegex(ValueError, "strict base64"):
                all_off.turn_everything_off(
                    strip=False,
                    ray_get_cct_fn=lambda **_kwargs: ray_calls.append("get") or {},
                    ray_set_cct_fn=lambda *_args, **_kwargs: ray_calls.append("set") or {},
                )
        self.assertEqual(ray_calls, [])


if __name__ == "__main__":
    unittest.main()
