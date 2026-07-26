# Local Lab Connection Boundary

## Scope

This repository serves a user-owned local photography and lighting calibration
lab. The lab consists of the local workstation, the ESPHome RGBWW fixture, the
local camera bridge and attached Canon camera, and the Ray120c reference light
through the loopback Amaran Desktop OpenAPI endpoint. These are measurement
components in one local experiment environment, not general-purpose remote
administration targets.

## Connection Owners

| Component | Connection owner | Explicit configuration | Offline behavior |
| --- | --- | --- | --- |
| RGBWW fixture | `control.esphome` | Host, port, expected device name, and ESPHome secrets path | Module help, parsing, analysis, and tests do not connect. |
| Canon camera bridge | `control.camera_remote` | Base URL and token supplied by explicit arguments, environment, or the documented project environment file | Module help and offline RAW analysis do not load bridge credentials or connect. |
| Ray120c reference | `control.ray120c` | Loopback URL/node settings, the Human-classified public shared protocol default, and optional explicit override `AMARAN_OPENAPI_SECRET` | Module help does not connect. A missing override uses the public default; an explicitly empty or invalid override fails before connecting. |

The repository treats the built-in Ray key as a Human-classified public shared
protocol default, not a private credential. This is a Human decision supported
by repository history and is not an external-vendor verification claim about
documentation, protocol specifications, or security review. `AMARAN_OPENAPI_SECRET`
is an optional explicit override; when supplied, it remains a private runtime value
and must not be passed in argv, printed, logged, serialized, or exposed by
`repr`. Both the default and an override are validated as strict base64 for a
32-byte key. An explicitly empty or invalid override fails closed without
falling back. The override is not read from the project `.env` by this owner.

## Execution and Authorization

Device work remains bounded by the active `.agent-work/PLAN.md`, including
target, output, duration, abort behavior, and cleanup. Bounded light control and
off/zero cleanup follow the project light-control exception. Remote firmware
upload, deployment, destructive hardware changes, or work outside the active
plan still requires Human authorization. Help commands and offline analysis do
not authorize or perform device operations.

## Local Preconditions and Troubleshooting

Before a planned connection, confirm the intended local component is powered,
the workstation is on the same local lab network where applicable, and the exact
documented hostname or loopback service is available. If an optional private
runtime override is intentionally used, confirm it is present and valid. If
those conditions are not met, stop at the plan's failure branch; do not widen
the target set or alter network or firmware configuration outside the plan.

Accurately describing this scope and the public-default/private-override boundary can reduce
possible platform misclassification. It cannot guarantee a platform decision,
does not alter platform policy, and is not a mechanism for bypassing safety or
security controls.
