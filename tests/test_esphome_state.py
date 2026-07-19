from __future__ import annotations

import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from camera_based_rgbww_optimizer.control import esphome
from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import (
    validate_strip_device_evidence,
)


class _FakeClient:
    def __init__(self, *_args, baseline=None, observed=None, entity_count=1, **_kwargs):
        self.baseline = baseline
        self.observed = observed
        self.entity_count = entity_count
        self.callback = None
        self.disconnected = False

    async def connect(self, *, login):
        self.login = login

    async def disconnect(self):
        self.disconnected = True

    async def device_info_and_list_entities(self):
        entities = [
            SimpleNamespace(object_id=esphome.STATE_OBJECT_ID, key=7 + index)
            for index in range(self.entity_count)
        ]
        services = [SimpleNamespace(name=esphome.SET_SERVICE), SimpleNamespace(name=esphome.OFF_SERVICE)]
        return SimpleNamespace(name=esphome.DEFAULT_EXPECTED_NAME, mac_address="fake"), entities, services

    def subscribe_states(self, callback):
        self.callback = callback
        callback(SimpleNamespace(key=7, state=json.dumps(self.baseline)))

    async def execute_service(self, _service, _payload):
        if self.observed is not None:
            self.callback(SimpleNamespace(key=7, state=json.dumps(self.observed)))


class EspHomeVerifiedStateTests(unittest.TestCase):
    def _run(self, baseline, observed, *, entity_count=1, timeout=0.02):
        with tempfile.TemporaryDirectory() as tempdir:
            secrets = Path(tempdir) / "secrets.yaml"
            secrets.write_text("api_encryption_key: fake\n", encoding="utf-8")
            client = _FakeClient(baseline=baseline, observed=observed, entity_count=entity_count)
            result = asyncio.run(esphome.async_verified_light(
                5, 4, 1, 2, 3, secrets_path=secrets, curve_path=None,
                state_timeout=timeout, client_factory=lambda *_args, **_kwargs: client,
            ))
        return result, client

    def test_success_requires_independent_newer_snapshot(self):
        baseline = _snapshot(10, red=0, green=0, blue=0, warm_white=0, cold_white=0)
        observed = _snapshot(11, red=1, green=2, blue=3, warm_white=4, cold_white=5)
        result, client = self._run(baseline, observed)
        self.assertEqual(result["requested_payload"], {
            "red": 1, "green": 2, "blue": 3, "warm_white": 4, "cold_white": 5,
        })
        self.assertEqual(result["device_snapshot"]["generation"], 11)
        self.assertTrue(client.disconnected)

    def test_missing_entity_channel_mismatch_and_stale_generation_fail_closed(self):
        baseline = _snapshot(10, red=0, green=0, blue=0, warm_white=0, cold_white=0)
        for entity_count in (0, 2):
            with self.subTest(entity_count=entity_count), self.assertRaisesRegex(RuntimeError, "missing or duplicated"):
                self._run(baseline, None, entity_count=entity_count)
        mismatch = _snapshot(11, red=9, green=2, blue=3, warm_white=4, cold_white=5)
        with self.assertRaisesRegex(ValueError, "channels differ"):
            self._run(baseline, mismatch)
        for generation in (10, 9):
            with self.subTest(generation=generation), self.assertRaisesRegex(RuntimeError, "timed out"):
                self._run(baseline, _snapshot(generation, red=1, green=2, blue=3, warm_white=4, cold_white=5))

    def test_bare_payload_and_nonincreasing_evidence_are_rejected(self):
        command = {"cw": 5, "ww": 4, "r": 1, "g": 2, "b": 3}
        with self.assertRaisesRegex(ValueError, "independent device-state schema"):
            validate_strip_device_evidence(command, command, {})
        evidence = {
            "schema_version": 1,
            "requested_payload": {"red": 1, "green": 2, "blue": 3, "warm_white": 4, "cold_white": 5},
            "baseline_snapshot": _snapshot(10, red=0, green=0, blue=0, warm_white=0, cold_white=0),
            "device_snapshot": _snapshot(10, red=1, green=2, blue=3, warm_white=4, cold_white=5),
            "device_state_entity": {"object_id": esphome.STATE_OBJECT_ID, "key": 7},
            "device_identity": {"name": esphome.DEFAULT_EXPECTED_NAME, "mac_address": "fake"},
        }
        with self.assertRaisesRegex(ValueError, "strictly increase"):
            validate_strip_device_evidence(evidence, command, {})

    def test_formal_p7_entrypoints_use_verified_api_and_firmware_contract_is_present(self):
        from camera_based_rgbww_optimizer.optimization import measure_hsi_reference_repeatability, measure_strip_hsi_pilot
        source = Path(measure_strip_hsi_pilot.__file__).read_text(encoding="utf-8")
        r1_source = Path(measure_hsi_reference_repeatability.__file__).read_text(encoding="utf-8")
        firmware = Path(__file__).parents[1] / "firmware/esphome/bedroom-rgbww-strip-common.yaml"
        text = firmware.read_text(encoding="utf-8")
        self.assertIn("verified_light", source)
        self.assertIn("verified_light", r1_source)
        self.assertIn("rgbww_state_generation", text)
        self.assertIn("rgbww_commanded_state", text)
        self.assertIn("apply_rgbww_12bit", text)


def _snapshot(generation, **channels):
    return {"schema_version": 1, "generation": generation, **channels}


if __name__ == "__main__":
    unittest.main()
