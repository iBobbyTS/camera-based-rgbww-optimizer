# P7 TD-A production settings preflight

## Status

Blocked before device access. Human authorization exists, but the offline entry gate proves the production runner would send invalid remote capture settings.

## Confirmed evidence

- TD-A retained shutters exist: Ray `1/5000`, strip `1/320`.
- Both TD-A dry plans incorrectly list future TD-B key `ray-h120-s50` in `exposure_setup_required`.
- `run_authorized_plan()` passes `iso=None` and `aperture=None` into the native timed capture adapter.
- A fake-only adapter probe observes ambient `CaptureSettings(iso=None, aperture=None, shutter_speed="30")`.
- `_capture_payload()` serializes those values as JSON `null`; the frozen remote API accepts only exact string choices.
- No device, network, `.env`, remote API, camera, Ray, ESPHome, capture, or `all_off` call occurred.

## Required next step

Planner must define an offline repair and acceptance package before the one-time TD-A hardware authorization can be consumed. The repair needs a single remote config/settings owner before capture or light output, source-scoped shutter requirements, and a production fake round-trip covering ambient plus retained Ray/strip shutters.
