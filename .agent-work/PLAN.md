# REF-P7-25-R2-B2-R2：fresh real-B2 manifest-only seal

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-R2`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-REAL-MANIFEST-ONLY-V2`

**当前唯一动作：** Orchestrator审核并以本PLAN冻结的activation topology更新FULL后，Executer在一个brand-new external root中运行一次single-process real-B2 manifest-only composition：先消费accepted C1 path-owner四件套，再对其解析出的原retained-R3三件套各做一次non-following exact read，并以accepted exact-five、preparation与provenance-I/O owners封存一个subordinate immutable v2 manifest及terminal/ER linkage。

**唯一 Planner stop：**
`B2_R2_REAL_MANIFEST_TERMINAL_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260730-2254-p7-retained-r3-provenance-io-acceptance-transition-stop.md`，bytes `2701`，SHA-256
`f6663ac6adfa63f4fc485cbd49e6adf021a770b4eb48bc7d972d71843906e045`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_r2_real_manifest_only_v2","reference_task_id":"REF-P7-25-R2-B2-R2","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-REAL-MANIFEST-ONLY-V2","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"3a05490ae2f2e112db54010a4843f2be42393947","expected_subject":"chore(plan): activate real b2 manifest seal","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260730-2254-p7-retained-r3-provenance-io-acceptance-transition-stop.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-R2","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-REAL-MANIFEST-ONLY-V2","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","candidate_contract_orchestrator_verified":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"candidate_contract":{"identity_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","exact_entry_count":5,"accepted_terminal_commit":"7c31c1be26274955686e9214a14bb29d1adc77b5","entries":[{"repo_path":"src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py","expected_sha256":"a9bc77340dc43a30c0733e6ed651ea155b2250739b02a69d5abe6b6d249a3d47","after_blob_oid":"839dfdd88f22970a2c77b88564ae016af3e76012"},{"repo_path":"src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py","expected_sha256":"48c0c57fb95c08205c3fef7b23e6df3729928352cd23e1722e8693b9f3634cf8","after_blob_oid":"b3daada521d3eec98ac0ac8382a8846546aaf780"},{"repo_path":"src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py","expected_sha256":"14955da5f19e9cd73532910eee295aaaf612ec9a78559c99a51d38c239c674d1","after_blob_oid":"da65983db057c30d664f4eae4757c3e09077b1b6"},{"repo_path":"tests/test_p7_retained_release_audit.py","expected_sha256":"c8d6c7c99815d823871ecfddce79eadd5d5def918affbcd7e4ce86de691d1b3f","after_blob_oid":"c1ec87913783cba4cc4322729d2222986953b1f0"},{"repo_path":"tests/test_p7_thermal_diagnostics.py","expected_sha256":"d57995180b26f8a04c7d43f5bd744dabedc6b133db30fe013785a6477c70a0d5","after_blob_oid":"78045e83ba2fa62b867d386615209ef47a7840be"}]},"accepted_bootstrap":{"record_sha256":"56fb1c806db56ce7f68240c1a35b4443dc4c41806bd4bb3107e85a095a8ecf97","seal_sha256":"568a32cab44be41322f51be3e812a044e3976c7689a2ffd8b49fad2ab379cca4"},"owners":{"exact_five_sha256":"746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726","preparation_sha256":"882f3819d161369012ce7fcd52cb1de1b9c56e4e1f821ff4554f6a1d8340738b","provenance_io_sha256":"f603721fb8b90510e2a09b199701c3f3358574d1247b5883ebdccc6f585b0a48","integration_test_sha256":"740652267178e3225edf03efacc293cfbdfb7c18efb749b6cd9aee281a728366"},"source_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z","controller_source":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-real-manifest-controller-3a05490-20260730T2254Z.py","output_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-real-manifest-3a05490-20260730T2254Z","output_root_required_absent":true,"subordinate_manifest":{"filename":"retained-r3-audit-provenance-manifest-v2.json","schema":"p7_retained_r3_audit_provenance_manifest_v2","status":"sealed_subordinate_provenance_evidence"},"input_budgets":{"plan_reads":1,"full_reads":1,"controller_source_writes":1,"controller_source_reads":1,"c1_lstat_open_read_hash_each":1,"c1_file_count":4,"retained_lstat_open_read_hash_each":1,"retained_file_count":3,"read_only_git_invocations":56,"alternate_path_search":0,"parent_or_sibling_listing":0,"recursive_search":0},"execution_budgets":{"python_controller_process":1,"exact_five_prepare":1,"exact_five_execute":1,"root_create":1,"manifest_write":1,"manifest_seal_write":1,"terminal_write":1,"terminal_seal_write":1,"er_admission_write":1,"execution_result_append":1,"retry":0,"fallback":0,"second_root":0,"test_invocations":0,"compileall_invocations":0,"codegraph_sync":0,"git_stage":0,"git_commit":0},"zero_budgets":{"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_R2_REAL_MANIFEST_TERMINAL_WAITING_PLANNER_REVIEW"}`

## 1. Activation与dispatch gate

本PLAN本身不允许直接dispatch。Orchestrator须先独立审核，并创建exact activation commit：

- direct parent必须为`3a05490ae2f2e112db54010a4843f2be42393947`；
- subject必须为`chore(plan): activate real b2 manifest seal`；
- changed paths必须恰为machine contract中的三路径；
- FULL machine row必须恰为`active_task_count=1`、本task/contract active、candidate identity/verified字段不变、retained status仍为`RETAINED_UNVALIDATED_UNCONSUMED`、`executer_dispatched=true`且device authorization false；
- commit后porcelain与stage必须为空。

Executer启动后先用repo-owned machine-contract parser各读取PLAN/FULL一次，并验证activation HEAD/parent/subject/path set、PLAN blob=worktree bytes、FULL required subset、所有builtin type和exact value。再验证四个accepted owner的当前worktree SHA与HEAD blob一致。任一不符时external source write、root、C1/retained read、Git replay、manifest和controller process全部保持0，仅向ER append一次pre-dispatch FAIL后停止；禁止猜测、alias、fallback或cross-owner borrowing。

## 2. Frozen inputs与exact read budgets

### 2.1 C1 path-owner evidence

只允许从exact source root读取以下四个direct-child regular non-symlink、mode`0600`文件。每个文件恰好一次`lstat`、一次`O_RDONLY|O_NOFOLLOW` open、descriptor稳定read、before/after `fstat`与SHA验证；不得第二次读取：

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `path-owner-index.json` | `12195` | `b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35` |
| `path-owner-index.sha256.json` | `682` | `867d1ffad5bd29f24dc81b24a58ce66393dd688833d3a4516fe7f45ef50875e9` |
| `terminal-evidence.json` | `13455` | `c21a691272ca7466271349daa5b10236c9f36dfeb481d592e9c368a87e7a4763` |
| `terminal-evidence.sha256.json` | `772` | `4bfebf4ad40e8c2e65ad2470faaed184f21d39eda73c13e689b09769d280752f` |

四者必须strict duplicate-key/non-finite reject、canonical compact sorted UTF-8+exact LF，并重放index→seal→terminal→terminal seal的path/bytes/SHA/schema/status链接。只能从accepted index的三个独立resolved records取得source root与三条absolute direct-child path；不得要求whole-list嵌套、不得扫描parent/sibling、不得重新发现或替换路径。

### 2.2 Original retained-R3 artifacts

C1四件套全部通过后，才可按resolved records对以下三件套各执行一次相同的non-following stable descriptor read；读取仅证明physical bytes/hash，不等于audit、validation或consumption：

| Artifact | Expected SHA-256 |
| --- | --- |
| `current-lineage-candidate.json` | `3a2ff5a2af200c55c925b954488c5c5dd31a35a481440d17dfcdd8b68419f2e0` |
| `resolved-formal-plan.json` | `cf7c78b6a6cfda4055d05f5e9bbe9914161213b380dc7736ee09e257dd45eb6b` |
| `setup-lineage-release.json` | `0bacf1878a97fcdc4436259e132e89f6e56611df6d7fb5d5a7da28f62c98ad3e` |

每件记录exact path、bytes、SHA、device、inode、mode、before/after identity；允许strict canonical JSON decode及B2 schema/self-consistency检查，但禁止调用`p7_retained_release_audit`、canonical lineage validator、consumer/replay/eligibility或任何release operation。三source在执行前后identity必须相同；不得copy、repair、rewrite、touch、chmod、relocate或regenerate。

### 2.3 Accepted Git/provenance baseline

所有Git访问必须只经`p7_retained_r3_provenance_io.run_read_only_git`，exact总数`56`，且argv必须落在其committed allowlist。不得调用直接`subprocess`、shell Git、`cat-file`、worktree mutation或第二Git owner。冻结并重算：

1. historical helper v1 commit`9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`及release parent`32b9e670ff3bbea0cd1505528c2ca87c2935446c`，disposition exact `retained_release_audit_prerequisite_v1_superseded_before_real_validation`；
2. integration commit`3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c`、parent`9303aa22...`、181-path LF ledger SHA`9596c3fa8aee58259aff13b44badcc7d448e0555c80f166b20706dcd1e321118`；selected helper/test after SHA分别为`48c0c57f...34cf8`与`c8d6c7c9...1b3f`，其余179 paths status只能是`present_in_commit_not_authorized_by_this_manifest`；
3. accepted chain按full SHA/direct parent/subject/exact changed paths/before-after blobs与binary patch绑定：`0682cd8763516dfb19a8e1ad48c53cb9934b9d19`、`ba816216af9d37397873e054f44dbb7eea0f9b10`、`a9a817137969d9d2692fdd0b244d08e26e8a025d`、`3a14fe0bd663250dd48c65e71f1a6550df89267f`、`7c31c1be26274955686e9214a14bb29d1adc77b5`；
4. governance manifest`config/hsi/p7-governance-lineage-successor-v1.json` SHA`69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e`及C17 accepted successor facts；
5. machine contract内exact sorted five entries的7c31 commit-qualified blob/SHA；不得使用generic allowlist、第六路径、current descendant substitution或nearby path。

`56`次矩阵固定为：上述7个commit各`rev-parse --verify`/metadata show/diff-tree=`21`；integration selected-two before/after blobs=`4`；五chain changed-path before/after blobs=`20`；integration selected binary patch=`1`；五chain binary patch=`5`；terminal exact-five entries at 7c31 blob lookup=`5`。任一argv、count、exit、stdout parse或identity不符立即失败，后续Git调用为0且不补足/重试。

## 3. Single-process owner composition

Executer只可创建一个package-local controller source：
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-real-manifest-controller-3a05490-20260730T2254Z.py`。创建必须exclusive、mode`0600`；写后立即冻结bytes/SHA，AST parse并用builtin`compile()`一次。Source只能直接import：

- `agent_work_machine_contract`；
- `p7_retained_r3_exact_five_controller`；
- `p7_retained_r3_controller_preparation`；
- `p7_retained_r3_provenance_io`；
- 必需的无I/O stdlib数据类型/hash/JSON模块。

Source禁止builtin `open`、`pathlib` read/write、raw `os` fd/filesystem API、`subprocess`、socket/network/env、temporary source generation、nested controller、第二phase state machine或自行复制P3 I/O实现。所有physical read/root/persist/Git必须调用accepted provenance owner；phase ordering/call cardinality必须调用exact-five owner；terminal exact-target/ER admission必须调用preparation owner。Source static/compile失败时不得创建output root或读取real inputs。

随后只允许`create_exclusive_root()`创建exact output root，mode`0700`，parent不得创建/修复；若已存在即`root_exists` terminal failure且不得复用或选择第二root。Output root的允许文件集仅为：

```text
retained-r3-audit-provenance-manifest-v2.json
retained-r3-audit-provenance-manifest-v2.sha256.json
terminal-evidence.json
terminal-evidence.sha256.json
execution-result-admission.json
```

所有文件必须由`persist_canonical_json`以direct child、`O_EXCL|O_NOFOLLOW`、mode`0600`、partial-write loop、file fsync、directory fsync、strict reload创建；任何已存在target、physical identity drift或close/fsync/reload failure都fail closed，不得删除或覆盖partial target。

Exact-five request使用machine contract的five entries、activation parent/subject、candidate identity、bootstrap record/seal、schema。Callback顺序与预算固定：

```text
acquire C1 four-file replay = 1
materialize five accepted Git entries = 5
import/static gate = 1
accepted-preparation gate = 1
accepted-integration gate = 1
accepted-provenance-I/O gate = 1
activation/single-commit read-only verification = 1
subordinate manifest persist+seal = 1
canonical_validator callback field = 1 exact-True zero-budget guard
actual canonical validator invocation = 0
terminal persist+seal = 1
```

这里`canonical_validator`只是exact-five API要求的callback slot：它必须验证`actual_canonical_validator_calls==0`并返回exact `True`；不得import/call真实validator，不得输出eligibility。Callback count与actual validator count必须在manifest/terminal分字段记录，禁止将slot count误报为validator工作。

## 4. Manifest、terminal与ER evidence

Manifest必须至少绑定：GUIDE SHA`659152f6...00e35`、Advisor decision evidence SHA`842cfad0...5620`、attachment SHA`91a88e54...33d6`、Human engineering-governance override；C1四件套physical identities；三原artifact pre/post identities；全部Git ledgers与accepted owner source identities；historical v1 superseded/unconsumable disposition；production runtime false；generation/copy/consumption/device/formal authority false/none；logical rollback`32b9e670ff3bbea0cd1505528c2ca87c2935446c`；exact zero counters。

Manifest schema/status必须exact为machine contract值。它不得包含或暗示`eligible`、`candidate_eligible=true`、`consumable`、`authorized`、`validated`或formal pass。Manifest一旦写入并seal，不得rewrite、repair、replace或relocate；success只解锁B3 planning，不解锁B4/validator。

Terminal success/failure必须包含exact-five callback counts/results、actual validator count、C1/retained/Git read counts、output physical targets、manifest presence/absence、primary error type/stable code、all zero budgets。Terminal seal必须在physical terminal writer返回后由independent target identity绑定；使用`SealTargetIdentity(path,bytes,sha256,device,inode)`和`validate_terminal_seal`。只有该gate通过后才可通过`validate_and_emit_execution_result`写一个`execution-result-admission.json`，最后由Executer向`.agent-work/EXECUTION_RESULT.md` append一次matching摘要。PLAN/FULL/GUIDE/RESEARCH/archive不得被Executer修改。

## 5. Failure branches、acceptance与locks

- 任一dispatch/source/root/C1/retained/Git/manifest/terminal/ER gate失败：立即停止，后续phase count为0，保留root/partial files作为immutable rejected evidence；retry/fallback/alternate path/second root/repair/delete均0。
- 若manifest已经seal后后续terminal或ER失败，manifest仍immutable但B2整体FAIL，不能因manifest存在而进入B3。
- PASS要求：exact one source/process/root；C1 reads`4/4`；retained reads`3/3`；Git`56/56`；exact-five phase/cardinality全部通过；manifest+seal、terminal+seal、ER admission均存在且物理链接精确；all prohibited budgets为0；source三件套pre/post identity不变。
- PASS或FAIL都停在唯一Planner stop，等待Planner独立读取root、重放Git/manifest/terminal/ER并接受或拒绝；Executer不得自行进入B3、B4或更新retained status。

Hard locks持续为：canonical retained validator、retained audit、eligibility、release qualification/generation/copy/consumption、network/DNS/`.env`/credentials、device、camera、Ray、strip、cleanup、capture、FORMAL-R6、public analyzer、TD-C、sentinel、P8、firmware与deployment全部`0`。本包是纯本地provenance computation，不命中Human高危授权，也不存在需要Advisor判断的科学分支。

## 6. Duration与维护性判断

本包不跑tests/full suite、不访问设备，只做7个bounded file reads、56个本地read-only Git argv和5个small canonical writes，预计明显低于10分钟；不得使用visible Terminal长任务/automation流程。若执行前有新证据表明预计超过10分钟，Executer不得自行改变launch topology，须停Planner/Orchestrator重规划。

维护性判断：物理I/O继续由`p7_retained_r3_provenance_io`独占，phase/cardinality由exact-five独占，terminal/ER admission由preparation独占；outer source只做字段映射与callback composition，不增加repo production owner或平行validator。当前无需后续重构，B3应作为独立包验证本manifest，而非扩张本包。
