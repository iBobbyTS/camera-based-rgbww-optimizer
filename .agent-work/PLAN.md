# REF-P7-25-R2-B2-R2-C1-C1-C1-C1：source-root/direct-child 离线纠偏资格包

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-R2-C1-C1-C1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-C1-C1-SOURCE-ROOT-DIRECT-CHILD-QUALIFICATION-V1`

**当前唯一动作：** Orchestrator独立审核本review与PLAN，更新FULL并创建exact activation commit；activation后，Executer仅运行一次fresh pure-offline source-root identity/direct-child qualification。不得读取或重跑三份rejected controller，不得读取、复用或修改其rejected/absent roots，不得读取retained R3、重跑real B2或生成subordinate manifest。

**唯一 Planner stop：**
`B2_R2_C1_C1_C1_C1_SOURCE_ROOT_BINDING_QUALIFICATION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1039-p7-retained-r3-b2-r2-c1-c1-c1-source-root-binding-failure-review.md`，bytes `8985`，SHA-256
`c73850832792f4aef7248dcd75cc0b4cd5acbacbf2b3f343d431e53b127d75b9`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_r2_c1_c1_c1_c1_source_root_direct_child_qualification_v1","reference_task_id":"REF-P7-25-R2-B2-R2-C1-C1-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-C1-C1-SOURCE-ROOT-DIRECT-CHILD-QUALIFICATION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"486ae9274c3a670463b8bcece258fcb22ec7cc97","expected_subject":"chore(plan): activate b2 source root binding correction qualification","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1039-p7-retained-r3-b2-r2-c1-c1-c1-source-root-binding-failure-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-R2-C1-C1-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-C1-C1-SOURCE-ROOT-DIRECT-CHILD-QUALIFICATION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","candidate_contract_orchestrator_verified":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"reviewed_failure":{"activation_commit":"f9fc752fad1d0d48d2797f3d27a49ccf70cf24ec","activation_parent":"e3a776e493e3c7e4aaf6d98e159bb3c13c676bfd","evidence_commit":"486ae9274c3a670463b8bcece258fcb22ec7cc97","controller_path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-c1-c1-activation-binding-controller-e3a776e-20260731T1626Z.py","controller_bytes":19630,"controller_sha256":"e18a8824f30ecfa4ee8a5fc6dbf64c174035323dca23fddabaae7298a48b86c5","controller_device":16777240,"controller_inode":2218000,"controller_mode":"0600","output_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-c1-c1-activation-binding-qualification-e3a776e-20260731T1626Z","output_root_device":16777240,"output_root_inode":2218004,"output_root_mode":"0700","qualification_sha256":"20fae6a7b43b5a249e6579a861af85c9ca91f3d85779f50d6dbce04c7e9986ab","qualification_seal_sha256":"a4462e9ee2abf38f06bddcce8022d3474a00a5b9cedac46e5f9552d8c5b525bd","terminal_sha256":"6dfd2d78d26797dd330c13b4b89317e093cafeb40fb0e5b38abe93fa78e4aa21","terminal_seal_sha256":"ef30fa3ec0728c64f95d679134ce1dad988168f57616830f9f1e3ecc7a67737d","admission_sha256":"a27769143f69b7401487869d82905b6a25c876897d2008f20cf76bff48e3fc19","stable_code":"source_root_identity_unbound","disposition":"immutable_rejected_do_not_read_rerun_repair_rewrite_or_delete"},"source_root":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z","device":16777240,"inode":2188341,"physical_mode":448,"logical_mode":"0700"},"controller_source":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-c1-c1-c1-source-root-binding-controller-486ae92-20260731T1639Z.py","output_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-c1-c1-c1-source-root-binding-qualification-486ae92-20260731T1639Z","output_root_required_absent":true,"source_root_binding_contract":{"pre_root_lstat_count":1,"post_root_lstat_count":1,"root_bound_read_count":4,"total_live_root_identity_observations":6,"all_c1_reads_require_root_keyword":true,"all_file_identity_root_fields_equal_expected":true,"literal_only_root_identity_rejected":true,"rootless_read_rejected":true,"direct_child_required":true,"pre_post_identity_exact":true},"logical_mode_contract":{"physical_mode_type":"integer","physical_mode_value":384,"logical_mode_type":"string","logical_mode_value":"0600","mapping":"format_physical_mode_as_exact_four_digit_lowercase_octal_without_prefix","alternate_representations_rejected":[384,true,"0o600","600","00600"]},"owners":{"machine_contract_sha256":"743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f","machine_contract_blob":"5c581f9b502bcab1809b6a61a082a47f4150e09f","preparation_sha256":"882f3819d161369012ce7fcd52cb1de1b9c56e4e1f821ff4554f6a1d8340738b","preparation_blob":"ecfa62a37bb33cf23743fcb8d0bba706f8795458","provenance_io_sha256":"f603721fb8b90510e2a09b199701c3f3358574d1247b5883ebdccc6f585b0a48","provenance_io_blob":"492f31f5f6999e28a1f0eb60240780e2c4826f4f"},"input_budgets":{"plan_reads":1,"full_reads":1,"controller_source_writes":1,"controller_source_reads":1,"source_root_explicit_lstat":2,"source_root_owner_lstat":4,"c1_lstat_open_read_hash_each":1,"c1_file_count":4,"rejected_controller_reads":0,"rejected_root_reads":0,"retained_reads":0,"read_only_git_invocations":6},"execution_budgets":{"python_controller_process":1,"root_create":1,"qualification_write":1,"qualification_seal_write":1,"terminal_write":1,"terminal_seal_write":1,"er_admission_write":1,"execution_result_append":1,"matrix_case_count":24,"retry":0,"fallback":0,"alternate_source":0,"second_root":0,"second_process":0,"test_invocations":0,"compileall_invocations":0,"codegraph_sync":0,"git_stage":0,"git_commit":0},"zero_budgets":{"rejected_controller_reads":0,"rejected_root_reads":0,"retained_artifact_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_R2_C1_C1_C1_C1_SOURCE_ROOT_BINDING_QUALIFICATION_WAITING_PLANNER_REVIEW"}`

## 1. Activation、single-source binding 与 dispatch gate

本PLAN尚未授权Executer直接运行。Orchestrator须先：

1. 独立接受review decision
   `REJECTED_BOUNDED_B2_R2_C1_C1_C1_SOURCE_ROOT_IDENTITY_UNBOUND_CORRECTION_REQUIRED`；
2. 只修改Orchestrator-owned FULL：旧C1-C1-C1标为rejected，C1-C1-C1-C1成为唯一active，machine row exact匹配machine contract required subset；
3. 创建direct child of `486ae9274c3a670463b8bcece258fcb22ec7cc97`、subject exact为
   `chore(plan): activate b2 source root binding correction qualification`、changed paths exact为machine contract三路径的activation commit；
4. commit后worktree、stage、untracked为空，再dispatch fresh Executer。

Executer以accepted machine-contract parser各读取PLAN/FULL一次。Accepted Git owner call 1取得current full `HEAD`；calls 2-6复用同一SHA，验证active activation parent/subject/exact paths和三个owner blobs。不得从`reviewed_failure`、archive、旧source或short SHA建立active tuple。任一activation/static preflight失败时root、source-root lstat和C1 reads保持`0`；outer launcher仅使用首次source read已持有的`FileIdentity`向ER append一次pre-root FAIL并停止。

## 2. Frozen source root、four direct children 与 physical ownership

Static preflight通过并exclusive创建output root后，controller须对冻结source root执行如下exact物理边界：

1. root-only local capture以`os.lstat` exact一次观察source root；拒绝symlink/non-directory，要求path absolute exact、device `16777240`、inode `2188341`、mode integer `448`；
2. 以这次live observation构造accepted provenance-I/O owner的exact `DirectoryIdentity`；不得从qualification literal、PLAN dict或旧evidence直接构造未验证identity；
3. 四个C1文件均调用accepted `read_exact_file` exact一次，并显式传同一个`root=source_root_identity`；owner因此在每次read前重新lstat root并执行exact direct-child gate；
4. 第四次read完成后，root-only local capture再以`os.lstat` exact一次观察source root，要求与pre identity及四个`FileIdentity.root`完全一致。

仅这两个root-only `os.lstat`允许使用stdlib filesystem I/O。文件lstat/open/fstat/read/hash必须全部由accepted provenance owner完成；不得builtin `open`、`pathlib` read、glob、listdir、resolve、parent/sibling enumeration、第二reader或alternate path。四文件冻结身份不变：

| File | Bytes | Device | Inode | SHA-256 | Schema | Status |
| --- | ---: | ---: | ---: | --- | --- | --- |
| `path-owner-index.json` | `12195` | `16777240` | `2188342` | `b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35` | `p7_retained_r3_path_owner_index_v1` | `path_owner_resolved_waiting_for_planner` |
| `path-owner-index.sha256.json` | `682` | `16777240` | `2188343` | `867d1ffad5bd29f24dc81b24a58ce66393dd688833d3a4516fe7f45ef50875e9` | `p7_retained_r3_path_owner_index_seal_v1` | `sealed_waiting_for_planner` |
| `terminal-evidence.json` | `13455` | `16777240` | `2188344` | `c21a691272ca7466271349daa5b10236c9f36dfeb481d592e9c368a87e7a4763` | `p7_retained_r3_b2_c1_path_owner_terminal_v1` | `pass_waiting_for_planner` |
| `terminal-evidence.sha256.json` | `772` | `16777240` | `2188345` | `4bfebf4ad40e8c2e65ad2470faaed184f21d39eda73c13e689b09769d280752f` | `p7_retained_r3_b2_c1_path_owner_terminal_seal_v1` | `pass_waiting_for_planner` |

四者strict duplicate-key/non-finite reject、canonical compact sorted UTF-8 exact LF重构、schema/status exact type/value。四个logical record的`mode`只接受JSON string exact `"0600"`；physical mode保持integer `384`。不得读取index解析出的retained paths。

## 3. Fresh controller、root-first ordering 与 exact 24-case matrix

Executer只可exclusive创建machine contract冻结的fresh controller source，mode `0600`。Source写后立即由provenance owner exact读回一次并由outer launcher保留完整identity；验证strict UTF-8、AST parse、builtin compile。只可import三个accepted owners、`DirectoryIdentity`及无I/O stdlib；`os`/`stat`仅用于两次source-root capture。禁止读取/import/exec旧controller、repository code copy、subprocess/socket/env/device/release/validator imports或calls。

Static preflight通过后先由`create_exclusive_root`创建exact fresh output root mode `0700`，再观察source root或读取C1。Root已存在即fail closed；不得删除、复用、修复、alternate root或second process。允许direct-child set exact：

```text
c1-c1-c1-c1-source-root-binding-qualification.json
c1-c1-c1-c1-source-root-binding-qualification.sha256.json
terminal-evidence.json
terminal-evidence.sha256.json
execution-result-admission.json
```

所有write由`persist_canonical_json`完成，mode `0600`、exclusive no-follow、fsync及strict reload。Qualification在一次读取形成的immutable payload上运行exact `24` cases：

1. 保留原C1-C1-C1的cases `01-20`，case code、expected/observed语义与logical-mode/FAIL admission/hash identity覆盖不变；
2. case 21将一个in-memory `FileIdentity.root.device`漂移，必须拒绝；
3. case 22将一个in-memory `FileIdentity.root.inode`漂移，必须拒绝；
4. case 23将一个in-memory `FileIdentity.root.mode`漂移，必须拒绝；
5. case 24将direct-child path替换为sibling/escape path，必须拒绝。

Real case 01额外要求四个`FileIdentity.root`均为同一个live frozen `DirectoryIdentity`，且pre/post root observations相同。Static source inspection必须证明四个C1 calls均含`root=`，不得存在rootless alternate read。Negative case只操作内存对象，不得重读C1或触碰filesystem。

Qualification绑定active tuple、PLAN/FULL/controller、三个owner identities、output root、source-root pre/post live identities、root observation counts `1+4+1`、四个C1 physical/logical records、24 cases/counts、既有findings以及`REV-B2-R2-C1-C1-C1-001/002/003`、三份旧失败immutable dispositions和全部zero budgets。不得包含retained payload、Git provenance replay、subordinate manifest或eligible/validated/consumable/authorized语义。

## 4. PASS/FAIL terminal lifecycle

Root创建后，任一source-root capture、root-bound read、decode/schema/linkage/matrix/qualification失败均进入同一个FAIL terminal路径；不得因overall PASS assertion跳过admission。Terminal记录primary error、phase、completed cases、C1 reads、root observation counts、source-root pre/post identities、qualification presence/absence、output-root/source identities、activation tuple与zero counters。

PASS写qualification+seal；FAIL qualification targets为null。两者均写terminal、独立terminal seal，并由preparation owner构造seal target后调用`validate_and_emit_execution_result` exact一次：valid PASS写matching admission；valid FAIL写matching admission后重新抛primary error；terminal/seal/validation失败则admission `0`并保留physical evidence。Admission成功后Executer才向ER append一次matching handoff。

## 5. Acceptance、failure branches 与 hard locks

PASS要求：exact source/process/output-root `1/1/1`；active tuple及六次Git owner calls exact；output root早于source-root/C1 access；source-root explicit pre/post lstat `1/1`，owner internal root checks `4/4`，六次identity完全一致；四个C1 reads均root-bound direct-child且physical reads `4/4`；原20 cases及新增4 root cases共`24/24`；qualification+seal、terminal+seal、admission physical/logical linkage exact；logical mode仅`str "0600"` accepted；三份旧controller/root read/rerun `0`；retained/Git provenance replay/manifest/validator/eligibility/release/device/scientific budgets全`0`。

任一gate失败即停止；不得retry、fallback、repair、overwrite、delete、root reuse、alternate source/root、second process或把partial output解释为pass。PASS/FAIL均停在
`B2_R2_C1_C1_C1_C1_SOURCE_ROOT_BINDING_QUALIFICATION_WAITING_PLANNER_REVIEW`，不得自行授权fresh real B2。

持续hard locks：三份旧controller/source/root immutable rejected；real B2 retry、retained-R3 reads、Git provenance replay、subordinate manifest、B3/B4、retained audit、canonical validator、eligibility、release generation/qualification/copy/consumption、network/DNS/`.env`/credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware、deployment全部`0`。Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

## 6. Duration and maintainability

本包仅验证一个目录identity、读取四个small accepted C1 JSON、运行24个in-memory cases并写五个small JSON，预计低于10分钟；不得使用visible Terminal或automation。若preflight判断可能超过10分钟，Executer停止并回Planner/Orchestrator。

维护性判断：纠偏仅在一次性外置 controller 中把既有provenance owner的`DirectoryIdentity`真正接入四次read，并增加前后目录观察；不修改repo production/test owner，不新增validator、release语义或平行执行框架。
