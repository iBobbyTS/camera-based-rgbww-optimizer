# REF-P7-23 / Bounded EQ-R6 activation continuation with canonical C3E2 paths

**计划状态：** `executable_bounded_live_activation_continuation`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-23`

**PLAN contract ID：** `P7-TD-B-RAY-C-EXPOSURE-QUAL-R6-CANONICAL-PATH-CONTINUATION`

**Package kind：** `bounded_predevice_continuation_then_conditional_visible_terminal_dispatch`

**Expected HEAD：** `f37517af3ae25efb41f085904fd48f037980ed04`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-RAY-C-EXPOSURE-QUAL-R6-CANONICAL-PATH-CONTINUATION","reference_task_id":"REF-P7-23","package_kind":"bounded_predevice_continuation_then_conditional_visible_terminal_dispatch","expected_head":"f37517af3ae25efb41f085904fd48f037980ed04","single_current_action":"run_one_new_static_preflight_with_exact_canonical_c3e2_paths_then_continue_the_unchanged_one_shot_live_activation","predecessor_decision":"REJECTED_PREDEVICE_EXECUTER_PREFLIGHT_PATH_MAPPING","canonical_validation_path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c3e2-offline-f37517a-20260727T1756/11-validation-summary.json","canonical_validation_sha256":"3b136148a2571dba893447c0558d9663d08a44ceef59000bd19a1fb22c48dc3c","canonical_terminal_path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c3e2-offline-f37517a-20260727T1756/12-terminal-summary.json","canonical_terminal_sha256":"c50e40e2b28fb0a69aa80e0016b39c06ff79f2818440c9b890417405d1ad309a","prior_package_static_preflight_processes":1,"prior_package_device_entry":false,"static_preflight_cap":1,"production_prelaunch_invocation_cap":1,"prelaunch_root_acquisition_cap":1,"handoff_validation_cap":1,"outer_dispatch_cap":1,"candidate_1_cap":1,"candidate_2_cap":1,"candidate_1_shutter":"1/2500","candidate_2_shutter":"1/3200","candidate_2_unlock":"candidate_1_clipping_only_and_candidate_terminal_cleanup_final_zero_pass","per_candidate_dwell":"A@600s+C@60/120/300/600s","real_capture_cap":8,"formal_measurement_count":0,"ambient_measurement_count":0,"retry":0,"relaunch":0,"alternative_root":0,"same_root_repair":0,"human_authorization_required":false,"human_authorization_reask_required":false,"source_edits_authorized":false,"test_edits_authorized":false,"docs_edits_authorized":false,"skill_edits_authorized":false,"wrapper_edits_authorized":false,"config_edits_authorized":false,"commit_authorized":false,"camera_access":"bounded_readiness_and_eq_candidate_capture","ray_access":"bounded_readiness_candidate_light_and_cleanup","strip_access":"generation_bearing_zero_state_only","public_analyzer_authorized":false,"formal_r6_authorized":false,"release_authorized":false,"strip_stage_authorized":false,"td_c_authorized":false,"planner_stop_required":true}`

**当前唯一动作：** 运行一个明确映射canonical C3E2 `11/12` artifacts的新static preflight；仅其完整通过时，
继续同一个仍未取得root的activation transaction：

```text
new static preflight exactly once
-> production prelaunch exactly once
-> exact fresh handoff validation within 600 seconds
-> one visible macOS Terminal outer dispatch
-> three sparse read-only liveness checks
-> terminal read-only audit or Orchestrator automation handoff
```

**唯一 Planner 停止点：** static preflight、prelaunch、handoff validation、Terminal dispatch、candidate
lifecycle、quality、physical evidence、cleanup、final-zero或terminal seal任一步失败立即stop；outer在三次
liveness前terminal则完成最终只读审计并stop；L3后仍存活则记录证据并交Orchestrator automation后stop。
成功terminal也必须停回Planner，不得进入public analyzer、successor release、formal R6、strip或TD-C。

## 1. Predecessor review and exact continuation authority

Reviewed predecessor：

```text
decision =
  REJECTED_PREDEVICE_EXECUTER_PREFLIGHT_PATH_MAPPING
archive =
  .agent-work/PLANS/20260727-1937-p7-eq-r6-preflight-path-mapping-review.md
archive SHA-256 =
  88ba18b3212cd342efac7559267d91fbf6920fcf1be4eea1c0ae176d3b634cd9
reviewed EXECUTION_RESULT SHA-256 =
  f933149efff307cf6fe8775cef689022b108c1b6fa8a674a61a82f2624f9bc88
```

Predecessor事实：

```text
static preflight process attempted / transaction completed = 1 / 0
failure = local nonexistent logical filename mapping
production prelaunch / handoff validation / dispatch = 0 / 0 / 0
device / network / camera / Ray / strip / cleanup = 0
root acquisition / capture / physical return = 0 / 0 / 0
retry / relaunch / repair / alternative root = 0 / 0 / 0 / 0
```

Current package is a new Planner-authorized bounded continuation, not a retry within the rejected PLAN. It permits one
new static preflight process only because the prior process stopped before any root acquisition or live/device entry.
It does not restore any same-root repair, candidate retry, second prelaunch or second dispatch authority.

Human reauthorization remains unnecessary under the current AGENTS high-risk boundary: no firmware upload/flash,
remote deployment, destructive hardware change or out-of-PLAN operation is present. Advisor direction is unchanged.

## 2. Canonical C3E2 evidence mapping — no logical filename aliases

Exact C3E2 root：

```text
C3E2_ROOT =
  /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-eq-r6-c3e2-offline-f37517a-20260727T1756
```

The static preflight must use these exact absolute paths, byte-for-byte：

```text
C3E2_VALIDATION =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c3e2-offline-f37517a-20260727T1756/11-validation-summary.json
C3E2_VALIDATION SHA-256 =
  3b136148a2571dba893447c0558d9663d08a44ceef59000bd19a1fb22c48dc3c

C3E2_TERMINAL =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c3e2-offline-f37517a-20260727T1756/12-terminal-summary.json
C3E2_TERMINAL SHA-256 =
  c50e40e2b28fb0a69aa80e0016b39c06ff79f2818440c9b890417405d1ad309a
```

Forbidden aliases：

```text
${C3E2_ROOT}/validation-summary.json
${C3E2_ROOT}/terminal-summary.json
any glob-derived first match
any basename normalization or numeric-prefix stripping
```

Both canonical files must be regular non-symlink files, safely contained under exact C3E2_ROOT, with exact hashes.
Static preflight must also confirm the root contains the accepted exact 12 numbered JSON filenames and no unexpected
top-level file. It must not mutate, replay, reserialize or repair C3E2 evidence.

Accepted evidence remains：

```text
C3E2 validation / terminal status = pass / pass
all mismatch arrays = []
accepted implementation HEAD =
  f37517af3ae25efb41f085904fd48f037980ed04
```

## 3. Frozen repository and dynamic dispatch inputs

```text
REPO =
  /Users/ibobby/Projects/WLED-RGBWW
HEAD =
  f37517af3ae25efb41f085904fd48f037980ed04
HEAD parent =
  0f36671a351d537f204e8bc20849ac83e7e57c2b
HEAD subject =
  fix(p7): select eq-r6 policy features atomically
```

Frozen file hashes：

```text
advisor/4/4.GUIDE.md
  659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35
.agents/skills/camera-based-rgbww-optimizer/SKILL.md
  c8dd57a23ad684b4f7001f342ed3413a1abf4349bc6aeb90dbee7f5158139607
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
  a9bc77340dc43a30c0733e6ed651ea155b2250739b02a69d5abe6b6d249a3d47
src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py
  34758f854cd5b17f3f844d8f8312b31fdbda11965aa4f695a3b1421e19522dc3
tests/test_p7_td_b_r6_contract.py
  030497bddc6735a6912abb08fe40e12bd3c0b4f37d47ef9954a61a5b88a39ad4
config/hsi/p7-ray-td-b-exposure-policy-v2.json
  9e5ec953fdeedf0e73a26a3a476b7336febdbdb2c3e83819123c7b9ad4060ec2
tmp/run-p7-thermal-diagnostics.zsh
  2730d43507af14a531453978477439bb29ef93ae7dea8e0bddb6c2330e1242e5
```

Orchestrator dispatch必须提供exact：

```text
CONTINUATION_PLAN_SHA256
CONTINUATION_FULL_SHA256
CONTINUATION_EXECUTION_RESULT_START_SHA256
```

PLAN不能自嵌自身hash。任一dynamic hash缺失、格式错误或current path/hash不符即stop。Executer不得修改
PLAN、FULL或任何archive。

## 4. Reserved fresh root remains unchanged

```text
SAFE_PARENT =
  /Volumes/4T/temp/rgbww-optimizer
FAMILY =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-f37517a-20260727T1928
PRELAUNCH =
  ${FAMILY}/prelaunch
RUN =
  ${FAMILY}/run
```

The predecessor never acquired these paths. At this package start, FAMILY/PRELAUNCH/RUN must remain absent and
non-symlink. The root is therefore still fresh and reserved; keeping it is not same-root repair or reuse.

Production prelaunch remains the only FAMILY/PRELAUNCH acquisition owner; outer remains the only RUN owner. Do not
precreate, delete, repair, rename or replace the root. Alternative root cap=`0`.

## 5. One new static preflight

Run exactly one local read/hash/stat transaction. It must verify：

```text
HEAD / parent / subject and frozen hashes = §3 exact
PLAN / FULL / EXECUTION_RESULT = Orchestrator dynamic hashes
review archive and reviewed EXECUTION_RESULT = §1 exact hashes
C3E2 canonical paths and hashes = §2 exact
C3E2 exact numbered 12 top-level JSON artifacts
SAFE_PARENT = safe
FAMILY / PRELAUNCH / RUN = absent and non-symlink
repository .env = regular non-symlink if present
```

Implementation constraint：

```text
static preflight process cap in this package = 1
static preflight transaction completion cap = 1
path mapping source = exact literal §2 absolute paths
logical basename synthesis = prohibited
glob fallback = prohibited
post-failure correction/rerun = prohibited
```

`.env`只可lstat，不得读取、打印、hash或复制。Static preflight不得做DNS、resolver、ping、HTTP、camera、Ray、
strip、cleanup或capture probe。任一failure立即stop并保留计数；不得在本PLAN内修正或第二次运行。

## 6. Fresh production prelaunch exactly once

Only after §5 passes completely, run once from repo root：

```zsh
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics \
  --execute \
  --allow-device-control \
  --eq-r6-prelaunch \
  --experiment-id p7_td_b_command_switch_history_v1 \
  --source ray \
  --phase formal \
  --output-dir /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-f37517a-20260727T1928 \
  --run-name prelaunch \
  --code-checkpoint f37517af3ae25efb41f085904fd48f037980ed04 \
  --human-authorization P7-TD-B-RAY-C-EXPOSURE-QUAL-R6 \
  --camera-backend remote
```

Invocation/root acquisition cap=`1/1`。The authorization CLI value is the already-confirmed frozen experiment identity,
not a new Human approval gate. Do not set ESPHome host override or consume any old handoff.

Prelaunch allows bounded camera/Ray readiness, strip generation-bearing zero and cleanup. It allows no capture, CR3,
nonzero strip, RUN, candidate, formal measurement, public analyzer, release, formal R6, strip stage or TD-C.

PRELAUNCH exact 9：

```text
frozen-inputs.json
offline-plan.json
camera-readiness.json
ray-readiness.json
all-off-python.json
all-off-shell.json
independent-final-zero.json
prelaunch-terminal.json
prelaunch-manifest.json
```

Exit nonzero, missing artifact, failed terminal/manifest or invalid zero proof immediately stops. No supplemental probe,
cleanup, second prelaunch, retry or same-root repair is authorized.

## 7. Exact handoff validation within 600 seconds

Only after prelaunch exit `0`, validate once and dispatch within 600 seconds of
`prelaunch-terminal.json.sealed_at`. Use production `_eq_prelaunch_validate_root` read-only and independently confirm：

```text
exact 9 names/order; strict JSON; modes 0700/0600; safe containment
terminal.status / manifest.status = pass / pass
manifest references = exact bytes and SHA-256
camera / Ray / Python cleanup / shell cleanup / final-zero = all pass
strip generation-bearing five-channel zero = true
Ray zero and validate_both_off = pass
capture / nonzero / dispatch counts = 0 / 0 / 0
RUN = absent and non-symlink
launch_handoff.ready_for_dispatch = true
launch_handoff.dispatch_count / outer_launch_count = 0 / 0
launch_handoff.run_root = §4 exact RUN
checkpoint / authorization label = §3 and §1 exact
outer_argv = §8 exact
outer_argv_sha256 =
  4f96b6d78c12ecdfbbf7cf6c40073c25bb20e4778efb981ad55172855b274589
secret material = absent
```

Hash definition：UTF-8 compact JSON array，`separators=(",",":")`、`ensure_ascii=False`、no newline。
Validation cap=`1`。Any mismatch or timeout stops; no argv edit, handoff rebuild, second validator or old handoff.

## 8. Visible macOS Terminal single outer dispatch

Exact outer argv：

```text
/Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python
-m
camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics
--execute
--allow-device-control
--eq-r6-orchestrate
--experiment-id
p7_td_b_command_switch_history_v1
--source
ray
--phase
formal
--output-dir
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-f37517a-20260727T1928
--run-name
run
--code-checkpoint
f37517af3ae25efb41f085904fd48f037980ed04
--human-authorization
P7-TD-B-RAY-C-EXPOSURE-QUAL-R6
--camera-backend
remote
```

Visible Terminal exact command：

```zsh
cd /Users/ibobby/Projects/WLED-RGBWW && exec /Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics --execute --allow-device-control --eq-r6-orchestrate --experiment-id p7_td_b_command_switch_history_v1 --source ray --phase formal --output-dir /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-f37517a-20260727T1928 --run-name run --code-checkpoint f37517af3ae25efb41f085904fd48f037980ed04 --human-authorization P7-TD-B-RAY-C-EXPOSURE-QUAL-R6 --camera-backend remote
```

Use visible macOS Terminal `do script` or equivalent foreground tab, never a Codex-managed background process.
Dispatch attempt cap=`1`; uncertain Terminal API result also consumes it and cannot be retried.

Record tab/window identifier, exact command/hash, observed unique PID/argv, RUN first appearance and launch ledger.

## 9. Unchanged EQ-R6 scientific and capture contract

```text
experiment = P7-TD-B-RAY-C-EXPOSURE-QUAL-R6
runner experiment_id = p7_td_b_command_switch_history_v1
source / phase / variant = ray / formal / core
qualification formal-authorizing = false
strip = generation-bearing zero throughout
ambient / formal = 0 / 0
candidate 1 = nominal 1/2500 s
candidate 2 = nominal 1/3200 s, clipping-only fallback
candidate count = 1, or 2 under exact unlock only
physical CR3 cap = 4 per candidate, 8 total
retry / relaunch / alternate shutter = 0 / 0 / 0
public analyzer / release / formal R6 / strip / TD-C = 0
```

Each candidate：

```text
verify strip generation-bearing five-channel zero
Ray A H120/S100/INT100 for 600 s
A -> Ray C H300/S100/INT100
C capture at 60 / 120 / 300 / 600 s
Ray off
Python finally all_off
shell trap all_off
independent generation-bearing final-zero
candidate terminal seal
```

No A capture, TD-B history or P6 compatibility is allowed. Each C capture must use the formal measurement path and
pass 58/58 required features, zero clipped fraction, finite/near-noise/valid-pixel gates, recorded MakerNote exposure,
nominal/recorded ratio, Ray command/readback, source isolation, strip zero, CR3/sidecar ownership/hash/remote IDs and
truthful attempted/physical-return/accepted accounting.

Candidate 2 unlock requires all of：

```text
candidate 1 failure causes are all and only required_feature_clipping
candidate 1 physical evidence is preserved
candidate 1 Python cleanup = pass
candidate 1 shell cleanup = pass
candidate 1 independent final-zero = pass
candidate 1 terminal seal = pass
```

Candidate 1 `4/4` selects 1/2500 and forbids candidate 2. Any candidate-1 non-clipping failure forbids candidate 2.
Candidate 2 `4/4` selects 1/3200; any failure stops unresolved/run-invalid. No faster shutter, auto exposure, weak
reacquire, same-root continuation or third candidate.

## 10. Progressive evidence and physical preservation

Outer and candidates must progressively atomic-write：

```text
frozen inputs / live plan / launch ledger
PID/argv/parent binding
Ray/strip command-readback chronology
capture attempts and remote request/capture IDs
physical-returns ledger
CR3/sidecar path/type/mode/bytes/SHA-256
RAW patch statistics and frozen 58-feature decision
candidate result/failure and terminal seal
Python/shell cleanup and independent final-zero
outer result/failure and terminal seal
```

After physical return, later sidecar/feature/policy/classification failure must retain and truthfully count returned
CR3/sidecar and remote IDs. Any runtime, quality, ownership, isolation, readback, containment, symlink, hash, accounting,
cleanup, final-zero or seal failure hard-stops and preserves evidence. Retry, relaunch, repair and alternate root remain 0.

## 11. Three sparse liveness checks

Expected duration is approximately 25 minutes for one candidate or 50 minutes for clipping fallback. After dispatch,
perform only read-only checks：

```text
L1 approximately +60 s
L2 approximately +300 s
L3 approximately +540 s
```

Each checks the same Terminal tab, same PID/argv, existing RUN progressive filenames/hashes, launch/terminal evidence,
and duplicate/residual owned processes. Do not perform DNS, network, device, camera, capture, light, cleanup or analyzer
probes.

If terminal before L3, proceed to §12 without restart. If still alive after L3, append the three checks, PID, latest
evidence, start time and estimated completion to EXECUTION_RESULT, then stop for Orchestrator automation.

## 12. Terminal read-only audit and Planner handoff

Audit only the same tab/PID/FAMILY/RUN：

```text
outer exit / terminal status
candidate launch count and candidate-2 exact unlock
launch ledger PID/argv/parent
candidate and outer terminal seals
owner-recorded terminal classification
truthful attempted / physical-returned / accepted counts
all returned CR3/sidecar path/bytes/hash/remote IDs
Python cleanup / shell cleanup / independent final-zero
strip generation-bearing zero and Ray zero
no duplicate/residual process
retry / relaunch / alternate root / repair = 0
HEAD and frozen file hashes unchanged
formal / ambient / analyzer / release / strip / TD-C = 0
```

Executer appends evidence and decision request only to `.agent-work/EXECUTION_RESULT.md`, then stops. PLAN, FULL,
archives and GUIDE remain read-only.

## 13. Acceptance branches and locks

```text
A. candidate 1 4/4 and lifecycle/evidence pass
   -> qualified_1_2500

B. candidate 1 exact clipping-only plus lifecycle pass,
   candidate 2 4/4 and lifecycle/evidence pass
   -> qualified_1_3200

C. valid scientific/quality rejection with valid evidence/cleanup/seal
   -> retain and Planner select GUIDE-defined stop

D. runtime/readiness/ownership/evidence/accounting/cleanup/seal failure
   -> retain and Planner-only bounded corrective decision
```

Every branch stops at Planner. This PLAN never authorizes a second current-package preflight, second prelaunch,
retry, fresh alternate root, third shutter, public analyzer, successor release, formal R6, strip stage or TD-C.

## 14. 维护性判断

本continuation只消除Planner/Executer handoff中的canonical filename歧义，不修改production/test或新增owner。
设备、科学、预算、Terminal和evidence lifecycle全部复用accepted实现；不需要Advisor或架构重构。

---

## 15. Planner formal review — Branch A accepted

**Review 时间：** 2026-07-27 20:17 America/Edmonton

Reviewed freeze：

```text
PLAN SHA-256 =
  9916f001e38dbdb224648ec1fe0a4c602a8a9d3bc945e98e1120238f69a3b848
FULL_PLAN_REFERENCE SHA-256 =
  e35415fd80decc511f7c9478312c984b04e15503786ab61821734db54ee2c523
EXECUTION_RESULT §152-153 SHA-256 =
  1ec2773e2a829d19d89c58b05c5b7488d43201291484664ed005ebb8aabd06d6
HEAD =
  f37517af3ae25efb41f085904fd48f037980ed04
```

Planner decision：

```text
REF-P7-23 = ACCEPTED_QUALIFIED_1_2500
PLAN acceptance branch = A
selected state-C nominal shutter = 1/2500
candidate 2 call count = 0
REF-P7-24 = UNLOCKED_FOR_OFFLINE_PLANNING
Advisor / Human decision required = false / false
```

Accepted fresh family：

```text
/Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-exposure-qual-r6-f37517a-20260727T1928
```

Planner independent whole-family audit：

```text
entries / files = 47 / 42
symlinks = 0
strict JSON and JSONL parse = pass
canonical manifest SHA-256 =
  41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9
```

Prelaunch and handoff：

```text
canonical C3E2 11/12 paths and hashes = exact
static preflight process / transaction = 1 / 1
production prelaunch invocation / acquisition = 1 / 1
prelaunch terminal / manifest = pass / pass
production handoff validator = pass
exact manifest artifact_order = pass
sorted exact prelaunch filename set = pass
handoff argv SHA-256 =
  4f96b6d78c12ecdfbbf7cf6c40073c25bb20e4778efb981ad55172855b274589
handoff age = within 600 seconds
outer dispatch / duplicate dispatch = 1 / 0
```

Terminal and owner：

```text
outer status = qualified_1_2500
candidate launches / candidate-2 calls = 1 / 0
attempted / physical-returned / accepted = 4 / 4 / 4
candidate / wrapper / shell / outer exits = 0 / 0 / 0 / 0
candidate seal / outer candidate terminal = pass / pass
former outer/wrapper/runner PIDs alive = false / false / false
duplicate or residual owner process = 0
retry / relaunch / alternate root / repair = 0 / 0 / 0 / 0
```

Exact qualification artifacts：

```text
run/outer-result.json
  SHA-256 20a4ee42c931e7df74b7fdd756eab3077530726e8ae5c03d3d48b45e8b562f0a
run/candidate-1-outer-terminal.json
  SHA-256 6401f0f162ce3efcd1ca6139e8394ed17411df7552fb1722e2db3eb7a8e4cd16
run/candidate-1/candidate-result.json
  SHA-256 7db4d60627c9a63304945664b4ba2e7918dafb12495f5fbf1d45500a46748612
run/candidate-1/terminal-seal.json
  SHA-256 8baa46bc6431e9e79c035a6f83954d810c25def2c8b662a761784fd1d81417a3
```

Quality and exposure：

```text
capture IDs =
  000-ray-c2500-t60
  001-ray-c2500-t120
  002-ray-c2500-t300
  003-ray-c2500-t600
required features = 58/58 x4
all finite = true
maximum clipped fraction = 0.0
maximum near-noise fraction = 0.0
minimum valid pixels = 29745
RAW accepted / rejected / pending = 92 / 0 / 0 x4
recorded owner = Canon:ExposureTime
recorded exposure range seconds =
  [0.000387549084953174, 0.000387549084953174]
recorded-to-nominal ratio = 0.9688727123829349
nominal ratio / command / isolation / strip-zero / chronology = pass
```

Physical and cleanup：

```text
four CR3 and four sidecars = regular, non-symlink, exact bytes/SHA-256
remote request/capture IDs = complete and cross-ledger exact
HTTP attempt per receipt = 1
physical-first ledger rows = 4
Python cleanup / shell cleanup / independent final-zero = pass / pass / pass
strip final generation = 4 > baseline 3
strip final five channels = zero
Ray final intensity = 0
```

Negative scope：

```text
candidate 2 = 0
formal / ambient = 0 / 0
public analyzer / release / formal R6 / strip / TD-C = 0
new device/network action during Planner review = 0
```

### Transparent residual adjudication

The pre-dispatch auxiliary checker returned exit `1` because it directly compared raw filesystem directory enumeration
with the manifest sequence：

```text
raw readdir order =
  camera-readiness, frozen-inputs, prelaunch-terminal, prelaunch-manifest,
  independent-final-zero, all-off-python, ray-readiness, all-off-shell,
  offline-plan

manifest artifact_order =
  frozen-inputs, offline-plan, camera-readiness, ray-readiness,
  all-off-python, all-off-shell, independent-final-zero,
  prelaunch-terminal, prelaunch-manifest
```

Planner does not hide or rewrite this exit. It is adjudicated as：

```text
REV-EQ-R6-AUX-ORDER-005 =
  NON_BLOCKING_REVIEW_TOOL_DEFECT_CLOSED_BY_INDEPENDENT_AUDIT
```

Reason：

1. raw `readdir` enumeration has no ordering semantics and the PLAN did not define it as the canonical order owner;
2. sorted raw set equals the exact expected nine names;
3. the production validator passed the exact set and canonical JSON references;
4. `prelaunch-manifest.json.artifact_order` equals the PLAN exact order;
5. all nine bytes/SHA-256 references and terminal/handoff facts independently match;
6. no second validator, altered handoff or hidden device retry occurred.

Therefore the checker exit does not evidence a production handoff mismatch and does not invalidate Branch A. Future
audit helpers must sort raw directory entries before set comparison and separately validate manifest order; their
process exit must not be represented as a production validator exit.

The later terminal local verifier also used wrong expected owner-schema literals (`launched` and `candidate_pass`
status). Direct schema-aware read confirmed actual authoritative values `launch_bound` and
`status=complete, classification=candidate_pass`; no RUN evidence defect exists.

Residual scientific boundary：

```text
EQ 4/4 proves exposure eligibility only
state C settled / TD-B pass = not claimed
release / formal R6 / analyzer / strip / TD-C remain locked
```

Exact next branch：only `REF-P7-24`, selected C policy finalization plus a new post-EQ code/config checkpoint. It must
derive `1/2500` and recorded exposure provenance from the accepted artifacts above, rerun the GUIDE-required full
offline validation, create one focused commit, and stop before release generation or any device operation.
