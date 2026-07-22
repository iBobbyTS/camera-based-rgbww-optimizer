# P7 TD-B trusted prerequisite path identity

## Status

Active PATH-R1 correction. The first E0X setup attempt failed closed before backend construction,
output ownership, device access, camera request, or CR3 production. Planner accepted the E0X
orchestration and authorized one fresh setup retry only after this offline contract is verified.

## Confirmed root cause

`build_diagnostic_plan()` reads the caller-provided operating-envelope path and persists
`file_reference(prerequisite_artifact)`, preserving relative spelling. The setup runner compares that
reference with `file_reference(OPERATING_ENVELOPE_V2_PATH)`, whose path is canonical absolute. Both
references identify the same bytes and SHA-256, but raw mapping equality rejects them.

This is a local identity representation defect, not an experimental or device failure.

## Frozen hypothesis and boundary

A narrow resolver owned by `optimization.p7_thermal_diagnostics` must canonicalize only the trusted
operating-envelope prerequisite. Producer, setup frozen-input validation, and public analyzer replay
must share it. The generic `file_reference()` contract must remain unchanged.

The resolver must reject before JSON parsing or side effects when the input contains traversal, is
outside the project, missing, a directory, a symlink, or a same-content copy at another path. The
accepted v2 artifact is exactly:

```text
/Users/ibobby/Projects/WLED-RGBWW/config/hsi/p7-operating-envelope-v2.json
sha256 = 7012f254e5fa5182dd51b72624f64ce03645fd3d8b7227ab9144f5c7767cfc16
```

## Verification contract

1. Relative, `./`-relative, and exact absolute spellings produce the same canonical plan reference.
2. Relative resolution is independent of process cwd.
3. Traversal, outside-root, missing, directory, symlink, same-hash copy, wrong config, and hash drift fail closed.
4. Setup validation rejects tampered plan path/hash before backend construction or output creation.
5. Public analysis independently replays the canonical identity.
6. At least one fake production round trip crosses plan build, setup frozen gate, fake backend boundary,
   retained setup evidence, and public replay with zero device/network side effects.

## Resolution state

Unresolved until focused/full tests, offline artifacts, CodeGraph sync, focused commit, and post-checkpoint
fake replay all pass. Device execution remains locked until then.
