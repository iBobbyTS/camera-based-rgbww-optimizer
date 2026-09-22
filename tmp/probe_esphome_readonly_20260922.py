"""Read-only ESPHome RGBWW fixture probe.

Connects to the fixture, verifies device identity, lists entities/services,
and reads the current ``rgbww_commanded_state`` snapshot. Sends no channel
commands and changes no device state.
"""

from __future__ import annotations

import asyncio
import json
import sys

from aioesphomeapi import APIClient

from camera_based_rgbww_optimizer.control.esphome import (
    DEFAULT_EXPECTED_NAME,
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_SECRETS_PATH,
    RgbwwDeviceSnapshot,
    STATE_OBJECT_ID,
    _load_api_encryption_key,
)


async def main() -> int:
    result: dict[str, object] = {"host": DEFAULT_HOST, "port": DEFAULT_PORT}
    api_key = _load_api_encryption_key(DEFAULT_SECRETS_PATH)
    client = APIClient(
        DEFAULT_HOST,
        DEFAULT_PORT,
        None,
        noise_psk=api_key,
        expected_name=DEFAULT_EXPECTED_NAME,
    )
    await asyncio.wait_for(client.connect(login=True), timeout=10)
    device_info, entities, services = await asyncio.wait_for(
        client.device_info_and_list_entities(), timeout=10
    )
    result["connected"] = True
    result["device_name"] = device_info.name
    result["mac_address"] = str(device_info.mac_address)
    result["esphome_version"] = device_info.esphome_version
    result["expected_name"] = DEFAULT_EXPECTED_NAME
    result["name_matches"] = device_info.name == DEFAULT_EXPECTED_NAME
    result["entity_count"] = len(entities)
    result["services"] = sorted(str(getattr(s, "name", s)) for s in services)

    state_entities = [
        e for e in entities if getattr(e, "object_id", None) == STATE_OBJECT_ID
    ]
    snapshots: asyncio.Queue[RgbwwDeviceSnapshot] = asyncio.Queue()
    if len(state_entities) == 1:
        entity_key = int(state_entities[0].key)

        def on_state(state: object) -> None:
            if int(getattr(state, "key", -1)) != entity_key:
                return
            try:
                snapshots.put_nowait(RgbwwDeviceSnapshot.parse(getattr(state, "state", "")))
            except ValueError:
                pass

        client.subscribe_states(on_state)
        try:
            snapshot = await asyncio.wait_for(snapshots.get(), timeout=10)
            result["current_state"] = snapshot.to_jsonable()
            result["all_channels_zero"] = all(
                v == 0
                for k, v in snapshot.to_jsonable().items()
                if k in ("red", "green", "blue", "warm_white", "cold_white")
            )
        except asyncio.TimeoutError:
            result["current_state"] = "timeout waiting for state snapshot"
    else:
        result["current_state"] = f"state entity count={len(state_entities)}"

    try:
        await client.disconnect()
    except Exception:
        pass
    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
