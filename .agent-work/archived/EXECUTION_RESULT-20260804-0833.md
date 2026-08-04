# EXECUTION_RESULT

## Machine Status

```json
{"schema":"g4_06_corrected_package_execution_result_v1","reference_task":"REF-G4-06-RAY-R6","contract":"G4-RAY-R6-STAGE-GATE-FRESH-PACKAGE-EVIDENCE-V1","status":"READY_FOR_PLANNER_G4_06_CORRECTED_PACKAGE_EVIDENCE_REVIEW","planner_review_required":true,"planner_stop":"RETURN_FOR_G4_06_CORRECTED_PACKAGE_REVIEW","planner_contract_correction_count":1,"prior_prepare_launch_count":1,"prior_prepare_exit_code":1,"prior_describe_launch_count":0,"current_prepare_launch_count":1,"current_prepare_exit_code":0,"current_describe_launch_count":1,"current_describe_exit_code":0,"current_owner_root_create_count":1,"current_retry_count":0,"current_alternate_root_count":0,"further_replacement_root_count":0,"raw_combined_output_exact_equal":true,"historical_root_access_count":0,"replacement_root_direct_probe_count":0,"device_access_count":0,"network_access_count":0,"camera_access_count":0,"ray_access_count":0,"strip_access_count":0,"capture_access_count":0,"formal_access_count":0,"release_access_count":0,"retained_r3_access_count":0,"td_c_access_count":0}
```

## Result

The corrected live machine contract passed the repo-owned strict PLAN/FULL
parsers and production pure `_projection` before any external-root access. The
unchanged repo-owned stage-gate owner then prepared one durable package and
described it once. Both native calls returned exit code `0`; their raw combined
outputs are exact string-equal.

Proposed status:

`READY_FOR_PLANNER_G4_06_CORRECTED_PACKAGE_EVIDENCE_REVIEW`

This is only an offline durable package candidate for Planner review. It does
not grant formal, device, quality, history, release-consumption, or G4-07
authority.

## Activation Intake

- Branch: `main`
- Activation HEAD: `c5ef1fa32449a5e1bc4d7ff8e5e7aeefabc03892`
- Activation parent: `0eaf3867a39d4898ca028383335ddd321aefe2cc`
- Activation tree: `da08af2f0b7077552411985fefce5db1807a4558`
- Activation subject: `docs(plan): correct ray r6 package binding contract`
- Activation changed paths exact:
  - `.agent-work/EXECUTION_RESULT.md`
  - `.agent-work/PLAN.md`
  - `.agent-work/archived/EXECUTION_RESULT-20260804-0822.md`
  - `.agent-work/archived/PLAN-20260804-0822.md`
- Direct non-merge child of expected parent: pass
- Intake worktree: clean
- PLAN/FULL active task count: `1/1`
- PLAN/FULL active/current/canonical task: `REF-G4-06-RAY-R6`
- PLAN/FULL contract:
  `G4-RAY-R6-STAGE-GATE-FRESH-PACKAGE-EVIDENCE-V1`
- PLAN executable authority: `true`
- FULL executable authority: `false`
- Formal, device, and release-consumption authority: `false`

## Pre-root Strict Parser and Projection Evidence

- Repo-owned `parse_plan_machine_contract`: pass
- Repo-owned `parse_full_plan_machine_state`: pass
- Production pure `p7_td_b_r6_stage_gate._projection`: pass
- PLAN/FULL active counts: `1/1`
- PLAN/FULL task identity: exact `REF-G4-06-RAY-R6`
- PLAN/FULL contract identity: exact
  `G4-RAY-R6-STAGE-GATE-FRESH-PACKAGE-EVIDENCE-V1`
- `new_stage_gate_root == replacement_root`: true
- Legacy `stage_gate_root` absent: true
- `required_full_g4_06_state == FULL.g4_06_state`: true
- Source attestation binding accepted by production `_projection`: pass
- `build_stage_gate_input` was not called during this pre-root check

## Root and Attempt Ledger

Historical original root remains:

```text
/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-ebc40bf8e40c-20260804T063700Z
HISTORICAL_UNCONSUMED_UNKNOWN_NOT_PROBED
```

- Historical-root access count across this execution: `0`
- Orchestration harness replacement root count: `1`
- Frozen replacement root:
  `/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-ebc40bf8e40c-harness-replacement-20260804T141423Z`
- Direct root probe count: `0`
- Further replacement-root count: `0`

Prior reviewed attempt:

- Prepare launch count: `1`
- Prepare exit code: `1`
- Prepare raw combined output: `output_root_drift\n`
- Describe launch count: `0`
- Owner root-create count: `0`
- Retry/alternate count: `0/0`
- Disposition: `ARCHIVED_PLANNER_CONTRACT_OMISSION`

Current corrected attempt:

- Prepare launch count: `1`
- Describe launch count: `1`
- Owner root-create count: `1`
- Per-run retry count: `0`
- Per-run alternate-root count: `0`
- Repair/cleanup count: `0`

## Native Prepare Result

Exact argv:

```text
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.p7_td_b_r6_stage_gate prepare --repo-root /Users/ibobby/Projects/WLED-RGBWW --source-parent-checkpoint 310f547c91420c34f67d1d241ad4aedaa3bc9c2c --source-parent-tree e5184c3236ba053909332fff032691c1aad167d0 --package-root /Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-ebc40bf8e40c-harness-replacement-20260804T141423Z
```

- Native exit code: `0`
- Native raw combined output follows exactly, including its terminal newline:

```json
{"artifacts":{"launch-descriptor.json":{"bytes":10890,"device":16777244,"inode":2903752,"mode":384,"path":"launch-descriptor.json","sha256":"9dd7da778f0bfd1d5975a7babc0341fbc32ea4a10e44edf95ed4c8fd59d6afc8"},"stage-gate.json":{"bytes":24805,"device":16777244,"inode":2903751,"mode":384,"path":"stage-gate.json","sha256":"e14eabd51eab182f50b6c8ff7583ec7e96294ae21e6feb447400ca4aee718ef2"},"terminal-seal.json":{"bytes":980,"device":16777244,"inode":2903753,"mode":384,"path":"terminal-seal.json","sha256":"a7a84fae6abf60fba3a5aef891074c4a5a99be478f8f6f8fb95a507f908aa65e"}},"inventory":["launch-descriptor.json","stage-gate.json","terminal-seal.json"],"package_root":{"device":16777244,"inode":2903750,"mode":448,"path":"/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-ebc40bf8e40c-harness-replacement-20260804T141423Z"},"schema":"p7_td_b_r6_stage_gate_package_binding_v1"}
```

No stdout/stderr split, output byte count, or output hash is claimed.

## Native Describe Result

Exact argv:

```text
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.p7_td_b_r6_stage_gate describe --repo-root /Users/ibobby/Projects/WLED-RGBWW --package-root /Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-ebc40bf8e40c-harness-replacement-20260804T141423Z
```

- Native exit code: `0`
- Native raw combined output follows exactly, including its terminal newline:

```json
{"artifacts":{"launch-descriptor.json":{"bytes":10890,"device":16777244,"inode":2903752,"mode":384,"path":"launch-descriptor.json","sha256":"9dd7da778f0bfd1d5975a7babc0341fbc32ea4a10e44edf95ed4c8fd59d6afc8"},"stage-gate.json":{"bytes":24805,"device":16777244,"inode":2903751,"mode":384,"path":"stage-gate.json","sha256":"e14eabd51eab182f50b6c8ff7583ec7e96294ae21e6feb447400ca4aee718ef2"},"terminal-seal.json":{"bytes":980,"device":16777244,"inode":2903753,"mode":384,"path":"terminal-seal.json","sha256":"a7a84fae6abf60fba3a5aef891074c4a5a99be478f8f6f8fb95a507f908aa65e"}},"inventory":["launch-descriptor.json","stage-gate.json","terminal-seal.json"],"package_root":{"device":16777244,"inode":2903750,"mode":448,"path":"/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-ebc40bf8e40c-harness-replacement-20260804T141423Z"},"schema":"p7_td_b_r6_stage_gate_package_binding_v1"}
```

No stdout/stderr split, output byte count, or output hash is claimed.

Prepare/describe raw combined output exact string equality: `true`.

## Canonical Package Binding

- Schema: `p7_td_b_r6_stage_gate_package_binding_v1`
- Package root path:
  `/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-ebc40bf8e40c-harness-replacement-20260804T141423Z`
- Package root identity: device `16777244`, inode `2903750`, mode `448`
  (`0700`)
- Ordered inventory exact:
  1. `launch-descriptor.json`
  2. `stage-gate.json`
  3. `terminal-seal.json`
- `launch-descriptor.json`: bytes `10890`, SHA-256
  `9dd7da778f0bfd1d5975a7babc0341fbc32ea4a10e44edf95ed4c8fd59d6afc8`,
  device `16777244`, inode `2903752`, mode `384` (`0600`)
- `stage-gate.json`: bytes `24805`, SHA-256
  `e14eabd51eab182f50b6c8ff7583ec7e96294ae21e6feb447400ca4aee718ef2`,
  device `16777244`, inode `2903751`, mode `384` (`0600`)
- `terminal-seal.json`: bytes `980`, SHA-256
  `a7a84fae6abf60fba3a5aef891074c4a5a99be478f8f6f8fb95a507f908aa65e`,
  device `16777244`, inode `2903753`, mode `384` (`0600`)

Successful prepare proves the repo owner completed its build/evaluate,
exclusive root creation, persistence, internal replay, strict public replay,
and terminal-seal boundary. Successful describe independently replayed the
sealed root, exact inventory, artifact identities, stage gate, launch
descriptor, source references, authority locks, and terminal seal.

## Source and Validation Boundary

- Accepted code checkpoint:
  `ebc40bf8e40c4bb59bd070367a321a2e76c3ce5c`
- Accepted code tree:
  `9dc4b3fb70bc97b80fb1db3b2389585e349e8737`
- Verified parent checkpoint:
  `310f547c91420c34f67d1d241ad4aedaa3bc9c2c`
- Verified parent tree:
  `e5184c3236ba053909332fff032691c1aad167d0`
- Inherited accepted validation: `963/963`; not rerun
- Production code, tests, config, GUIDE, RESEARCH, PLAN, FULL, and archives
  were not modified by the Executer.
- Only `.agent-work/EXECUTION_RESULT.md` is intended to differ.

## Authority and Side Effects

- Owner-produced offline package root creation: `1`
- Owner-produced persist/internal replay/public replay/terminal seal: completed
- Per-run retry/alternate/formal/device/release counts: `0/0/0/0/0`
- No direct root probe or extra package read beyond the two authorized owner
  calls
- No device, network, camera, Ray, strip, capture, formal R6, release,
  retained-R3, or TD-C operation was authorized or called
- No wrapper, redirection, pipeline, controller, `python -c`, heredoc,
  TextEncoder, Web Crypto, hash, base64, environment override, monkeypatch, or
  stdout/stderr split was used for either native package invocation
- No third root or corrective task was created

## Planner Decision Request

Review the corrected offline package candidate at the sole Planner stop
`RETURN_FOR_G4_06_CORRECTED_PACKAGE_REVIEW`. Do not infer formal/device/quality,
history, release-consumption, or G4-07 authority from this evidence.
