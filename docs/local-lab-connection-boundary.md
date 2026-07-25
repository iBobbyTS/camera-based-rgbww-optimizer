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
| Ray120c reference | `control.ray120c` | Loopback URL/node settings and required `AMARAN_OPENAPI_SECRET` from the process environment | Module help does not read the secret or connect. A real command fails before connecting when it is absent or invalid. |

The Ray secret has no source-code default and cannot be passed on the command
line. Programmatic callers may construct `OpenAPISettings` explicitly; its
secret is validated as strict base64 for a 32-byte key and is excluded from the
dataclass representation. Tests use generated fake key material and do not
inspect the developer environment.

## Execution and Authorization

Device work remains bounded by the active `.agent-work/PLAN.md`, including
target, output, duration, abort behavior, and cleanup. Bounded light control and
off/zero cleanup follow the project light-control exception. Remote firmware
upload, deployment, destructive hardware changes, or work outside the active
plan still requires Human authorization. Help commands and offline analysis do
not authorize or perform device operations.

## Local Preconditions and Troubleshooting

Before a planned connection, confirm the intended local component is powered,
the workstation is on the same local lab network where applicable, the exact
documented hostname or loopback service is available, and the required
credential/configuration is present in the user-owned runtime environment. If
those conditions are not met, stop at the plan's failure branch; do not widen
the target set or alter network or firmware configuration outside the plan.

Accurately describing this scope and removing a built-in credential can reduce
possible platform misclassification. It cannot guarantee a platform decision,
does not alter platform policy, and is not a mechanism for bypassing safety or
security controls.
