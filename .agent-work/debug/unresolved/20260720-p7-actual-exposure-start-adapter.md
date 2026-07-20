# P7 actual exposure-start adapter capability

## Status

Blocked for Advisor decision. No device, network, `.env`, remote API, capture, or `all_off` access is authorized.

## Confirmed local evidence

- `control.camera_remote.RemoteCaptureResult` contains only `saved_file`, `byte_count`, `endpoint`, and `http_attempts`.
- `capture_remote_image()` treats the successful response as a pure binary stream and does not parse any timing header or metadata envelope.
- `RemoteCameraBackend.capture()` projects only saved-file and HTTP provenance into the shared `CaptureResult`.
- The retained deployed bridge source returns CR3 bytes directly. Its successful response sets only `Content-Type`, `Cache-Control`, `Content-Disposition`, and content length.
- The deployment-time public API contract lists the same binary response headers and no exposure-start field.
- The bridge's filename timestamp is generated after capture/download and is not exposure-start evidence.

## Decision

The current API has no actual exposure-start field, unit, clock domain, or provenance hash. Per PLAN branch 2, stop client-side implementation. Do not use host request-start, HTTP response time, filename time, CR3 write time, or a fake callback.

Advisor must decide one of these research directions before Planner can define another executable package:

1. change the remote camera service to produce independently defined and validated exposure-start provenance; or
2. revise the TD timing contract around evidence the camera/service can actually provide.

Either direction changes the remote service or measurement contract and is outside the current Executer authorization.
