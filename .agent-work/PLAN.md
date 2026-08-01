# P7 retained-R3 Option B：M1-C1 existing-root identity owner correction

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED_AFTER_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-M1-C1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-C1-EXISTING-ROOT-IDENTITY-OWNER-V1`

**当前唯一动作：** 在 Orchestrator 建立 exact activation commit 后，Executer 只扩展既有 P3 provenance-I/O owner与P4
controller-conformance owner，使generated controller能以typed、no-follow、fail-closed方式取得并静态证明existing `0700` roots；完成exact
four-path实现、冻结验证、唯一implementation commit与一次ER handoff后停止。

**唯一 Planner stop：**
`B2_M1_C1_EXISTING_ROOT_IDENTITY_OWNER_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-2111-p7-retained-r3-b2-m1-existing-root-owner-gap-review.md`；bytes `4516`，SHA-256
`a6c4524fabed4935c67f68264d289ee6acdbdd6dbadb017017c16f93ec0596bf`；不得覆盖 earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_m1_c1_existing_root_identity_owner_v1","reference_task_id":"REF-P7-25-R2-B2-M1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-C1-EXISTING-ROOT-IDENTITY-OWNER-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"195afbe54caeda01fcf65af4d97604665d5e7adb","expected_subject":"chore(plan): activate existing root identity owner correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-2111-p7-retained-r3-b2-m1-existing-root-owner-gap-review.md"],"clean_porcelain_required_after_activation":true},"implementation_commit":{"expected_parent_source":"current_activation_head_runtime","expected_subject":"feat(p7): own existing root identity acquisition","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py","src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py","tests/test_p7_retained_r3_controller_conformance.py","tests/test_p7_retained_r3_provenance_io.py"],"single_commit":true,"clean_porcelain_required_after_commit":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-M1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-C1-EXISTING-ROOT-IDENTITY-OWNER-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","real_manifest_domain_owner_status":"BLOCKED_ON_EXISTING_ROOT_IDENTITY_OWNER","existing_root_identity_owner_status":"ACTIVE_IMPLEMENTATION","executer_dispatched":true,"device_authorized_by_this_file":false},"exact_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py","src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py","tests/test_p7_retained_r3_controller_conformance.py","tests/test_p7_retained_r3_provenance_io.py"],"p3_contract":{"entrypoint":"read_existing_root","return_type":"DirectoryIdentity","absolute_canonical_path":true,"lstat_no_follow_calls":1,"required_mode":448,"create_calls":0,"open_calls":0,"child_reads":0,"child_enumeration":0,"repair_calls":0,"dependency_injection":true,"stable_codes":["invalid_path","root_not_absolute","root_not_canonical","root_lstat_failed","root_not_directory","root_mode_mismatch"]},"p4_contract":{"recognized_owner_call":"read_existing_root","owner_result_type":"DirectoryIdentity","effect_owned":true,"direct_bound_name_required":true,"exact_unaliased_import_required":true,"live_read_root":true,"multiple_live_roots_allowed":true,"direct_constructor_allowed":false,"attribute_call_allowed":false,"local_shadow_allowed":false,"alias_allowed":false,"reflection_allowed":false,"generic_transport_allowed":false,"container_transport_allowed":false,"nested_call_allowed":false,"rootless_read_allowed":false,"existing_codes_preserved":true,"new_codes":["existing_root_owner_import_invalid","existing_root_owner_call_invalid"]},"test_contract":{"new_p3_test_methods":4,"new_p4_test_methods":5,"new_test_methods_total":9,"targeted_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_controller_conformance","targeted_expected":41,"focused_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_domain_template","focused_expected":58,"compileall_command":".venv/bin/python -m compileall -q src tests","full_command":"PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'","full_baseline":778,"full_expected":787,"postcommit_targeted_expected":41},"codegraph_contract":{"pre_edit_sync":1,"pre_edit_query":1,"post_edit_sync":1,"post_edit_query":1,"sync_before_query":true,"query_before_source_edit":true},"execution_budgets":{"implementation_commits":1,"execution_result_appends":1,"test_invocations":4,"compileall_invocations":1,"codegraph_sync":2,"codegraph_queries":2,"retry":0,"fallback":0},"zero_budgets":{"m1_source_test_writes":0,"m1_implementation_commits":0,"third_owner":0,"generic_path_allowlist":0,"accepted_c1_physical_reads":0,"retained_artifact_physical_reads":0,"external_controller_writes":0,"external_controller_reads":0,"external_controller_processes":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260731-2111-p7-retained-r3-b2-m1-existing-root-owner-gap-review.md","bytes":4516,"sha256":"a6c4524fabed4935c67f68264d289ee6acdbdd6dbadb017017c16f93ec0596bf"},"planner_stop":"B2_M1_C1_EXISTING_ROOT_IDENTITY_OWNER_WAITING_PLANNER_REVIEW"}`

## 1. Review decision 与 activation gate

上一M1结果判定为
`REJECTED_EXISTING_ROOT_IDENTITY_OWNER_MISSING_M1_NOT_IMPLEMENTED`。Executer正确在required CodeGraph query后、任何source/test edit前fail closed：
P3没有existing-root acquisition API，而P4只把effect-owned `DirectoryIdentity` name视为live read root；M1同时需要七个existing roots、output create
exact1、P3/P4 edits0，合同不可满足。该结果不接受M1，也不消耗M1实现机会。

Executer开始本包前必须验证activation是parent
`195afbe54caeda01fcf65af4d97604665d5e7adb`的direct child，subject exact，changed paths exact
FULL/PLAN/本archive三项，PLAN/FULL machine rows strict JSON且required FULL subset exact，porcelain clean。任一不符须在CodeGraph/source/test
读取或编辑前做single ER handoff并停止。

本包是pure-offline engineering/security boundary correction，不命中AGENTS高危设备授权，不需Human或Advisor。它只授权exact four paths：

1. `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py`；
2. `tests/test_p7_retained_r3_provenance_io.py`；
3. `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py`；
4. `tests/test_p7_retained_r3_controller_conformance.py`。

Implementation commit必须是activation direct child，subject exact
`feat(p7): own existing root identity acquisition`，changed paths按machine row lexicographic exact four。不得修改M1 module/test、P5/P7、PLAN/FULL/archive、
debug或任何其他路径。

## 2. CodeGraph 与 maintainability boundary

Activation gate后、source/test read或edit前，先运行一次`codegraph sync`，再运行一次精确query，覆盖P3
`DirectoryIdentity/_path/_directory_identity/_require_root/create_exclusive_root/read_exact_file/ProvenanceDependencies`与P4
`_CALL_OWNERS/_OWNER_TYPES/analyze_controller_source/root_names/root_reads/effect_bindings/effect_transport_uses`，确认没有public existing-root owner以及
current shared-root rejection。不得以grep/read替代或先读后补。

编辑后再运行一次`codegraph sync`与一次精确query，证明：P3仍是唯一physical provenance-I/O owner；P4仍是唯一static analyzer/effect provenance
owner；`read_existing_root`只有P3 definition且由P4 exact识别；无第三owner、second analyzer、generic allowlist、parallel framework或M1 edit。两次sync/query都
必须exit0，不得降级warning。

维护性边界：P3拥有no-follow filesystem observation及typed identity；P4只拥有source AST与effect provenance；未来M1只消费这些owners。不得把lstat、
path validation或identity construction复制进P4/M1，也不得把AST/import classifier放进P3。

## 3. P3 exact public `read_existing_root` owner

在P3现有public surface新增并只新增：

```python
def read_existing_root(
    path: os.PathLike[str] | str,
    *,
    dependencies: Mapping[str, Callable[..., Any]] | None = None,
) -> DirectoryIdentity: ...
```

函数必须复用现有`_dependencies`、`_path`、`_directory_identity/_directory_from_stat`安全边界并返回exact existing frozen
`DirectoryIdentity(path,device,inode,mode)`；加入现有`__all__`（若module使用显式export surface）。行为冻结为：

- 输入必须是exact可转换为`str`的absolute lexical canonical path。原始text必须以`/`开头，反斜杠、physical NUL、空segment（除leading root）、`.`、
  `..`、重复slash、trailing slash（root自身除外）或`str(Path(text)) != text`均fail closed；relative为`root_not_absolute`，非canonical为
  `root_not_canonical`，unsupported/NUL为existing `invalid_path`。不得调用`resolve()`、`realpath()`或任何follow-symlink API。
- 对通过lexical gate的path调用dependency-injected `lstat` exact1。`FileNotFoundError`、permission及其他`OSError`均映射existing
  `root_lstat_failed`；symlink或非physical directory为`root_not_directory`；`stat.S_IMODE != 0o700`为`root_mode_mismatch`。
- 成功时typed identity字段必须逐项来自该次lstat且path为输入canonical text。函数自身`mkdir/chmod/chown/rename/unlink/open/fstat/read/write/fsync/
  close/listdir/glob/walk/process/network`调用全0；不创建parent、不修复mode、不打开root、不枚举或读取child。
- 该identity只是采样时刻的能力证据，不承诺永久稳定。后续`read_exact_file(..., root=identity)`必须继续通过existing `_require_root`做fresh
  lstat identity equality；symlink/rebind/mode/device/inode drift仍报existing `root_identity_drift`或更早existing root error。不得cache或绕开二次验证。

`create_exclusive_root`、`read_exact_file`、persist、canonical JSON、Git owner的既有行为与错误码必须byte-semantically unchanged。

## 4. P4 exact effect provenance extension

P4只能在现有`analyze_controller_source`与owner metadata内做最小扩展：

- `_CALL_OWNERS`加入exact `read_existing_root -> DirectoryIdentity`。只有一个由exact unaliased
  `from camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io import ... read_existing_root ...`引入、且以direct `ast.Name`
  `read_existing_root(...)`调用并direct赋给single local name的结果，才能进入`effect_bindings`与live `root_names`。
- Import missing/duplicate/aliased/wildcard/wrong-module，attribute call，local def/argument/assignment/class shadow，或其他不能证明canonical owner import的形状必须在该
  result进入effect set前以`existing_root_owner_import_invalid`或`existing_root_owner_call_invalid` fail closed。不得建立generic module/callee/path allowlist。
- `read_exact_file(..., root=<name>)`仍必须含exact一个named keyword，root值必须是direct `ast.Name`且绑定为effect-owned
  `DirectoryIdentity`；rootless、positional、constructor、nested owner call、alias、tuple/list/dict/container、closure/callback、generic helper transport、reflection
  和rebind继续使用existing rejection或上述new exact codes。
- 移除“所有read必须共享一个root”的过度约束，允许多个分别由`create_exclusive_root`或exact `read_existing_root`直接取得的live root names；
  `ControllerConformanceReport.root_reads`和`transport.effect_bindings`必须逐项、deterministic sorted报告每个file-result/root与root owner call provenance，不能折叠。
- Existing output-root路径保持不变：`create_exclusive_root`仍是唯一creation owner；它返回的root仍可用于persist/reload reads；
  `RootIdentityChain`仍只接受effect-owned before/files/after且必须exact validate；新增existing-root API不得把fixture constructor升级为effect、不得放宽
  effect alias/container/generic transport、不得改变owner fields/public method schema或`effect_transport_uses=()`成功条件。

P4不得调用filesystem API，P3不得解析source。Future M1的7 existing reads与output readbacks才可使用本能力；本包自身不得生成、运行或修改M1。

## 5. Dedicated regression contract

保持现有test methods与assertions；只新增exact `4`个P3 methods和`5`个P4 methods，最终P3 `22`、P4 `19`、合计targeted `41`。新methods
必须冻结name inventory并有meaningful assertions，不得只执行代码：

### P3 four methods

1. public signature/export、frozen typed result、valid absolute canonical root、device/inode/mode/path逐项、dependency lstat exact1及所有create/open/read/repair
   counters0；
2. invalid type/NUL/relative/noncanonical matrix（double slash、trailing slash、`.`、`..`、backslash等），逐项stable code并证明lstat0；
3. missing/permission lstat、symlink、regular file/FIFO、wrong modes matrix，逐项stable code、lstat exact1、无repair/follow/open；
4. acquired identity交给real/fake `read_exact_file` direct-child positive，并覆盖root inode/device/mode/rebind或symlink drift fail closed，证明fresh identity revalidation，
   file open/read在root drift时0。

### P4 five methods

1. exact canonical import+direct owner call+direct read root positive，冻结bound result、root_reads、effect binding call provenance与empty transport violations；
2. multiple separately acquired existing roots及existing+created output root positive，冻结每个read/root映射、deterministic report并证明不恢复shared-root restriction；
3. import missing/wrong/duplicate/alias/wildcard、attribute call、local shadow/generic same-name function逐项以new stable codes在accept前拒绝；
4. constructor/nested/alias/rebind/container/reflection/generic helper/rootless/positional/non-name root negatives继续以exact existing codes拒绝；
5. existing created-root read与RootIdentityChain positive/negative regressions、owner schema/import source AST inventory，以及effect-owned identity不可逃逸；证明P5/P7既有
   generated source conformance不漂移。

Tests只能使用`tempfile`或fully fake dependency/source bytes；不得读取accepted C1、retained R3或external roots。不要新增test helper framework或第三test path。

## 6. Exact validation、commit 与 ER evidence

编辑完成后严格依次、每项exact一次，任一nonzero或count mismatch立即停止，不得retry或以narrow green覆盖：

1. targeted：`.venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_controller_conformance`，exact
   `41/41`；
2. focused：`.venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_domain_template`，exact `58/58`；
3. compileall：`.venv/bin/python -m compileall -q src tests`，exit0；
4. full discovery：`PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`，current baseline `778` + new9 = exact
   `787/787`且唯一`OK`；
5. post-edit CodeGraph sync/query与`git diff --check`，并验证unstaged diff exact four paths；
6. stage exact four paths，创建唯一implementation commit；
7. postcommit targeted exact `41/41`，验证direct parent、subject、changed paths、blob identities与porcelain clean。

总test invocations4、compileall1、CodeGraph sync2/query2、implementation commit1、retry/fallback0。不得运行额外ad-hoc Python、pytest、test discovery、
formatter或second correction。若现有method count与冻结baseline在任何edit前不符，视为gate failure，不自行改count。

无论通过/失败，只向`.agent-work/EXECUTION_RESULT.md`做一次EOF append。记录activation topology、CodeGraph before/after、exact four-path before/after
bytes/SHA/blob/diff、API/signature/errors、lstat/effect counters、P4 import/call/root provenance inventory、method inventory、四组test/compileall exit与count、commit
topology、first failure及all zero budgets。旧ER bytes必须保持prefix exact；Executer不得改PLAN/FULL/archive/debug/GUIDE。

## 7. Hard locks、failure branches 与 next unlock

本包的M1 source/test/commit全部0；它不会构造real manifest，不会读real inputs或运行controller。Accepted C1/retained physical reads、external
controller/root/process、Git provenance replay、M1 implementation、M1-I1、real B2、manifest/seal写入、canonical validator/callback、eligibility、retained audit、
release、network/DNS/`.env`/credentials、device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment全部0。
Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

- activation/CodeGraph/pre-edit count gate失败：source/test writes0、commit0，single ER handoff后停Planner；
- implementation/precommit validation失败：保留exact four-path diff，不跨界修复、不commit、不retry，single ER handoff后停Planner；
- commit后posttarget/topology失败：保留commit为non-consumable evidence，不amend/rebase，single ER handoff后停Planner；
- 全绿：只报告M1-C1 candidate waiting Planner review，不得自行接受或进入M1。

Planner若接受本correction，下一步是重新规划一个fresh M1 successor，使用新activation与accepted P3/P4 owner；不得复用被拒绝M1 activation，也不得由本PLAN
直接执行M1。

维护性判断：本包把existing-root物理身份 acquisition留在P3、静态能力证明留在P4，仅增加一个public effect owner与精确provenance分支；四加五项
回归覆盖path/lstat/drift/import/transport/multi-root边界，不引入第三owner或framework，接受后无需额外重构。
