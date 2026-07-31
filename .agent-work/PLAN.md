# REF-P7-25-R2-B2-R2-C1-C1-C1：activation-binding logical-mode 离线纠偏资格包

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-R2-C1-C1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-C1-ACTIVATION-BINDING-LOGICAL-MODE-QUALIFICATION-V1`

**当前唯一动作：** Orchestrator独立审核本review与PLAN，更新FULL并创建exact activation commit；activation后，Executer仅运行一次fresh pure-offline activation-binding/logical-mode/direct-linkage/failure-admission qualification。不得读取或重跑两份rejected controller，不得创建或读取其absent roots，不得读取retained R3、重跑real B2或生成subordinate manifest。

**唯一 Planner stop：**
`B2_R2_C1_C1_C1_ACTIVATION_BINDING_QUALIFICATION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1026-p7-retained-r3-b2-r2-c1-c1-activation-metadata-failure-review.md`，bytes `7958`，SHA-256
`d0fb86cfd78f6def7194f80fe295c369f2db7ed4154397ba83455c78ceae5898`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_r2_c1_c1_c1_activation_binding_logical_mode_qualification_v1","reference_task_id":"REF-P7-25-R2-B2-R2-C1-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-C1-ACTIVATION-BINDING-LOGICAL-MODE-QUALIFICATION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"e3a776e493e3c7e4aaf6d98e159bb3c13c676bfd","expected_subject":"chore(plan): activate b2 activation binding correction qualification","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1026-p7-retained-r3-b2-r2-c1-c1-activation-metadata-failure-review.md"],"clean_porcelain_required_after_activation":true},"activation_binding_contract":{"current_head_source":"git_rev_parse_head_call_1_full_sha","expected_parent_subject_paths_source":"active_activation_commit_object_only","head_reused_for_git_calls_2_through_6":true,"head_persisted_in_all_package_evidence":true,"reviewed_failure_fields_allowed_for_active_tuple":0,"historical_head_literals_allowed_for_active_tuple":0,"abbreviated_sha_allowed":false},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-R2-C1-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-C1-ACTIVATION-BINDING-LOGICAL-MODE-QUALIFICATION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","candidate_contract_orchestrator_verified":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"reviewed_failure":{"activation_commit":"03ce3df268096abe67568a806267ebf8a44c2980","activation_parent":"ebaddb5795720cc446f70ea1d32dfcb40cbae27a","activation_subject":"chore(plan): activate b2 logical mode correction qualification","evidence_commit":"e3a776e493e3c7e4aaf6d98e159bb3c13c676bfd","controller_path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-c1-logical-mode-controller-ebaddb5-20260731T1611Z.py","controller_bytes":19547,"controller_sha256":"0db566264282c3f97cee21bf5303bb91b830bd5aef53a3c9a27dfcf963d8b969","controller_mode":"0600","controller_device":16777240,"controller_inode":2217870,"incorrect_active_head_literal":"1bd06c4a0279f51546cf22c38581e2ab411c67d1","git_invocations_completed":2,"stable_code":"RuntimeError:activation_metadata","output_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-c1-logical-mode-qualification-ebaddb5-20260731T1611Z","output_root_status":"absent_immutable_do_not_create_reuse_or_delete","c1_reads":0,"matrix_cases":0,"disposition":"immutable_rejected_do_not_read_rerun_repair_rewrite_or_delete"},"source_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z","controller_source":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-c1-c1-activation-binding-controller-e3a776e-20260731T1626Z.py","output_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-c1-c1-activation-binding-qualification-e3a776e-20260731T1626Z","output_root_required_absent":true,"logical_mode_contract":{"physical_mode_type":"integer","physical_mode_value":384,"logical_mode_type":"string","logical_mode_value":"0600","mapping":"format_physical_mode_as_exact_four_digit_lowercase_octal_without_prefix","alternate_representations_rejected":[384,true,"0o600","600","00600"]},"owners":{"machine_contract_sha256":"743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f","machine_contract_blob":"5c581f9b502bcab1809b6a61a082a47f4150e09f","preparation_sha256":"882f3819d161369012ce7fcd52cb1de1b9c56e4e1f821ff4554f6a1d8340738b","preparation_blob":"ecfa62a37bb33cf23743fcb8d0bba706f8795458","provenance_io_sha256":"f603721fb8b90510e2a09b199701c3f3358574d1247b5883ebdccc6f585b0a48","provenance_io_blob":"492f31f5f6999e28a1f0eb60240780e2c4826f4f"},"input_budgets":{"plan_reads":1,"full_reads":1,"controller_source_writes":1,"controller_source_reads":1,"c1_lstat_open_read_hash_each":1,"c1_file_count":4,"rejected_controller_reads":0,"rejected_root_reads":0,"retained_reads":0,"read_only_git_invocations":6},"execution_budgets":{"python_controller_process":1,"root_create":1,"qualification_write":1,"qualification_seal_write":1,"terminal_write":1,"terminal_seal_write":1,"er_admission_write":1,"execution_result_append":1,"matrix_case_count":20,"retry":0,"fallback":0,"alternate_source":0,"second_root":0,"second_process":0,"test_invocations":0,"compileall_invocations":0,"codegraph_sync":0,"git_stage":0,"git_commit":0},"zero_budgets":{"rejected_controller_reads":0,"rejected_root_reads":0,"retained_artifact_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_R2_C1_C1_C1_ACTIVATION_BINDING_QUALIFICATION_WAITING_PLANNER_REVIEW"}`

## 1. Activation、single-source binding 与 dispatch gate

本PLAN尚未授权Executer直接运行。Orchestrator须先：

1. 独立接受review decision
   `REJECTED_BOUNDED_B2_R2_C1_C1_ACTIVATION_IDENTITY_DOMAIN_MIXUP_CORRECTION_REQUIRED`；
2. 只修改Orchestrator-owned FULL：旧C1-C1标为rejected，C1-C1-C1成为唯一active，machine row exact匹配machine contract required subset；
3. 创建direct child of `e3a776e493e3c7e4aaf6d98e159bb3c13c676bfd`、subject exact为
   `chore(plan): activate b2 activation binding correction qualification`、changed paths exact为machine contract三路径的activation commit；
4. commit后worktree、stage、untracked为空，再dispatch fresh Executer。

Executer以accepted machine-contract parser各读取PLAN/FULL一次。Active activation tuple只能这样建立：

1. accepted Git owner call 1运行exact current-`HEAD` verify，返回的full 40-character SHA成为本次唯一active head并冻结在内存；不得从PLAN的`reviewed_failure`、archive、旧source、历史commit或short SHA取得；
2. call 2以该full SHA查询metadata，并对比active `activation_commit.expected_parent`与`expected_subject`；
3. call 3以同一full SHA查询exact path set，对比`expected_changed_paths`；
4. calls 4-6以同一full SHA查询三条`HEAD:path` owner blob；
5. full head及parent/subject/paths写入所有qualification/terminal/admission/handoff evidence。

Controller source不得含旧head `1bd06c4a...`作为active tuple，不得读取`reviewed_failure`建立active tuple。Source/launcher static inspection必须证明activation inputs仅来自上述owner。任一activation/preflight失败时controller root/C1 reads保持`0`；launcher以dispatch前唯一source read已持有的`FileIdentity`向ER append一次pre-root FAIL并停止，不得为补hash第二次读取source，不得使用alias、fallback、第二parser或direct shell Git。

## 2. Frozen accepted C1 input and logical representation

Static preflight通过并exclusive创建root后，只允许从
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z`
读取四个冻结direct-child regular non-symlink mode-`0600`文件。每文件exact一次`lstat`、一次`O_RDONLY|O_NOFOLLOW` open、descriptor read、before/after`fstat`、bytes/SHA验证；必须使用accepted provenance-I/O owner，不得builtin `open`、`pathlib` read或第二reader。

| File | Bytes | Device | Inode | SHA-256 | Schema | Status |
| --- | ---: | ---: | ---: | --- | --- | --- |
| `path-owner-index.json` | `12195` | `16777240` | `2188342` | `b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35` | `p7_retained_r3_path_owner_index_v1` | `path_owner_resolved_waiting_for_planner` |
| `path-owner-index.sha256.json` | `682` | `16777240` | `2188343` | `867d1ffad5bd29f24dc81b24a58ce66393dd688833d3a4516fe7f45ef50875e9` | `p7_retained_r3_path_owner_index_seal_v1` | `sealed_waiting_for_planner` |
| `terminal-evidence.json` | `13455` | `16777240` | `2188344` | `c21a691272ca7466271349daa5b10236c9f36dfeb481d592e9c368a87e7a4763` | `p7_retained_r3_b2_c1_path_owner_terminal_v1` | `pass_waiting_for_planner` |
| `terminal-evidence.sha256.json` | `772` | `16777240` | `2188345` | `4bfebf4ad40e8c2e65ad2470faaed184f21d39eda73c13e689b09769d280752f` | `p7_retained_r3_b2_c1_path_owner_terminal_seal_v1` | `pass_waiting_for_planner` |

Source root device `16777240`、inode `2188341`、mode `0700`。四者必须strict duplicate-key/non-finite reject、canonical compact sorted UTF-8 exact LF重构、schema/status exact type/value匹配。不得枚举parent/sibling、递归搜索、alternate path或读取index解析出的retained paths。

四个direct logical records的`mode`必须是JSON string exact `"0600"`；physical `FileIdentity.mode`保持integer `384`。只允许一个local constructor使用exact four-digit lowercase octal、无`0o` prefix映射。integer `384`、bool、`"0o600"`、`"600"`、`"00600"`、coercion、normalization、alias、recursive decoy或cross-record borrowing全部拒绝。

## 3. Fresh controller、root-first ordering 与 exact 20-case matrix

Executer只可exclusive创建machine contract冻结的fresh controller source，mode `0600`。Source写后立即由provenance owner exact读回一次，outer launcher保留完整`FileIdentity`直到handoff；同时验证strict UTF-8、AST parse、builtin compile。只可import machine-contract、preparation、provenance-I/O三个accepted owners及无I/O stdlib数据/hash/JSON类型；禁止读取/import/exec旧controller，禁止nested source、temporary helper、repository code copy、subprocess/socket/env/device/release/validator imports或calls。

Source/PLAN/FULL/Git static preflight全部通过后，必须先由`create_exclusive_root`创建exact fresh output root mode `0700`，然后才可读取C1四文件或运行semantic matrix。Root若已存在即fail closed；不得删除、复用、修复、alternate root或second process。允许direct-child set exact：

```text
c1-c1-c1-activation-binding-qualification.json
c1-c1-c1-activation-binding-qualification.sha256.json
terminal-evidence.json
terminal-evidence.sha256.json
execution-result-admission.json
```

所有write由`persist_canonical_json`完成，mode `0600`、`O_EXCL|O_NOFOLLOW`、partial-write loop、file/directory fsync、strict reload。

Qualification必须在已读取的immutable in-memory payload上运行exact `20` cases：

1. real four-chain exact pass；
2. index-seal direct record的`relative_path/bytes/sha256/mode/schema/status` drift各一例；
3. terminal index identity、terminal index-seal identity、terminal-seal target drift各一例；
4. missing field、extra field各一例；
5. 四个direct records依次以integer `384`、string `"0o600"`、string `"600"`、bool `true`替换`"0600"`，各自fail closed；
6. recursive decoy不得救活direct mismatch；
7. valid FAIL terminal seal使ER callback exact一次；
8. invalid FAIL terminal seal使ER callback零次；
9. authoritative 64-character old physical seal SHA
   `e7ffc6b080729afaf926656b68f5d2e1f50fe2be8d3f5475af6a4986a908be90`
   accepted，而known-bad handoff string
   `e7ffc6b080729af926656b68f5d2e1f50fe2be8d3f5475af6a4986a908be90`
   malformed/mismatch rejected。

每个negative须有stable unique case code；不得重新读取文件构造case。Qualification须绑定single-source activation tuple、PLAN/FULL/controller、三个owner identities、source root、四个C1 physical identities、四个direct logical records、20 cases/counts、findings `REV-B2-R2-001/002/003`、`REV-B2-R2-C1-001/002/003`和`REV-B2-R2-C1-C1-001/002/003`、两份旧失败source/root immutable dispositions与all zero budgets。不得包含retained payload、Git provenance replay结果、subordinate manifest或eligible/validated/consumable/authorized语义。

## 4. PASS/FAIL terminal lifecycle

Root创建成功后，任何C1 read/decode/schema/linkage/matrix/qualification失败都进入同一个FAIL terminal路径；不得因overall PASS assertion跳过admission。Terminal记录primary error、phase、completed case count、C1 read count、qualification presence/absence、root/source identities、single-source activation tuple与所有zero counters。

PASS写qualification+seal；FAIL的qualification targets为null。两者都写terminal、独立terminal seal，并由preparation owner构造`SealTargetIdentity`后调用`validate_and_emit_execution_result` exact一次：

- valid PASS terminal写matching admission并正常返回；
- valid FAIL terminal写matching admission后重新抛出primary error；
- terminal write、seal write或seal validation失败时admission保持`0`，保留已写physical evidence并停止。

Admission成功后Executer才向`.agent-work/EXECUTION_RESULT.md` append一次matching handoff。Root acquisition失败则terminal/admission `0`，但handoff必须使用outer launcher已持有的source identity。PLAN、FULL、GUIDE、RESEARCH与archives始终只读。

## 5. Acceptance、failure branches 与 hard locks

PASS要求：exact source/process/root `1/1/1`；active head来自call 1 current full SHA，calls 2-6复用同一值，parent/subject/paths仅来自active activation object；root早于所有C1 reads；C1 physical reads `4/4`；main four-chain accepted；20-case matrix `20/20`；qualification+seal、terminal+seal、ER admission存在且physical/logical linkage exact；logical mode仅`str "0600"` accepted；两份旧controller read/rerun `0`、两份旧absent root仍absent；source root/files pre/post descriptor identities不变；retained/Git provenance replay/manifest/validator/eligibility/release/device/scientific budgets全`0`。

任一gate失败即停止；不得retry、fallback、repair、overwrite、delete、root reuse、alternate source/root、second process或把partial output解释为pass。PASS/FAIL均停在
`B2_R2_C1_C1_C1_ACTIVATION_BINDING_QUALIFICATION_WAITING_PLANNER_REVIEW`，不得自行授权fresh real B2。

持续hard locks：两份旧C1 controller/source/root immutable rejected；real B2 retry、retained-R3 reads、Git provenance replay、subordinate manifest、B3/B4、retained audit、canonical validator、eligibility、release generation/qualification/copy/consumption、network/DNS/`.env`/credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware、deployment全部`0`。Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

## 6. Duration and maintainability

本包只读四个small accepted C1 JSON、运行20个in-memory cases并写五个small JSON，预计低于10分钟；不得使用visible Terminal长任务或automation。若preflight判断可能超过10分钟，Executer停止并回Planner/Orchestrator，不得改变launch topology。

维护性判断：纠偏仅把一次性外置controller的active activation tuple收敛到唯一数据域，并让outer launcher保留首次source identity；logical-mode、root-first、matrix和seal/admission边界不变，不修改repo production/test owner，不新增validator或release语义。
