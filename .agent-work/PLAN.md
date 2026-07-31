# REF-P7-25-R2-B2-R2-C1：C1 linkage、failure-admission 与 physical-seal 离线纠偏资格包

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-R2-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-LINKAGE-FAILURE-ADMISSION-PHYSICAL-SEAL-QUALIFICATION-V1`

**当前唯一动作：** Orchestrator独立审核本review与PLAN，按本PLAN创建exact activation commit并更新FULL；activation后，Executer仅运行一次pure-offline C1 four-file linkage/failure-admission qualification。不得重跑real B2，不得读取retained R3或生成subordinate manifest。

**唯一 Planner stop：**
`B2_R2_C1_LINKAGE_QUALIFICATION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-0948-p7-retained-r3-real-b2-r2-manifest-failure-review.md`，bytes `10094`，SHA-256
`f5e399212ec9a42189edfec4ac7a210668698ad5eafab3c7622e6a1a6ca1b833`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_r2_c1_linkage_failure_admission_physical_seal_qualification_v1","reference_task_id":"REF-P7-25-R2-B2-R2-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-LINKAGE-FAILURE-ADMISSION-PHYSICAL-SEAL-QUALIFICATION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"b74944fb0bd5ffa064ba1ac92ae390fff7e008dc","expected_subject":"chore(plan): activate real b2 linkage correction qualification","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-0948-p7-retained-r3-real-b2-r2-manifest-failure-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-R2-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-LINKAGE-FAILURE-ADMISSION-PHYSICAL-SEAL-QUALIFICATION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","candidate_contract_orchestrator_verified":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"reviewed_failure":{"controller_sha256":"a5a24ef557978eb9b76cb47bdf8c58808035d98a7470100dce18c1c838f8de4e","root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-real-manifest-3a05490-20260730T2254Z","terminal_sha256":"b94680160307e9c3577ed59da1217dff344f3011e2b2f5c99edb5fdaac1f6d69","terminal_seal_sha256":"e7ffc6b080729afaf926656b68f5d2e1f50fe2be8d3f5475af6a4986a908be90","handoff_terminal_seal_sha256":"e7ffc6b080729af926656b68f5d2e1f50fe2be8d3f5475af6a4986a908be90","handoff_identity_status":"rejected_62_hex_transcription_missing_af","stable_code":"RuntimeError:index_seal_link_drift","disposition":"immutable_rejected_do_not_reuse_retry_repair_or_delete"},"source_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z","controller_source":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-linkage-qualification-controller-b74944f-20260731T0948Z.py","output_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-linkage-qualification-b74944f-20260731T0948Z","output_root_required_absent":true,"owners":{"machine_contract_sha256":"743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f","machine_contract_blob":"5c581f9b502bcab1809b6a61a082a47f4150e09f","preparation_sha256":"882f3819d161369012ce7fcd52cb1de1b9c56e4e1f821ff4554f6a1d8340738b","preparation_blob":"ecfa62a37bb33cf23743fcb8d0bba706f8795458","provenance_io_sha256":"f603721fb8b90510e2a09b199701c3f3358574d1247b5883ebdccc6f585b0a48","provenance_io_blob":"492f31f5f6999e28a1f0eb60240780e2c4826f4f"},"input_budgets":{"plan_reads":1,"full_reads":1,"controller_source_writes":1,"controller_source_reads":1,"c1_lstat_open_read_hash_each":1,"c1_file_count":4,"retained_reads":0,"failed_root_reads":0,"read_only_git_invocations":6},"execution_budgets":{"python_controller_process":1,"root_create":1,"qualification_write":1,"qualification_seal_write":1,"terminal_write":1,"terminal_seal_write":1,"er_admission_write":1,"execution_result_append":1,"matrix_case_count":17,"retry":0,"fallback":0,"second_root":0,"test_invocations":0,"compileall_invocations":0,"codegraph_sync":0,"git_stage":0,"git_commit":0},"zero_budgets":{"retained_artifact_reads":0,"git_provenance_replay":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_R2_C1_LINKAGE_QUALIFICATION_WAITING_PLANNER_REVIEW"}`

## 1. Activation 与 dispatch gate

本PLAN尚未授权Executer直接运行。Orchestrator须先：

1. 独立接受review decision `REJECTED_BOUNDED_B2_R2_C1_LINKAGE_FAILURE_ADMISSION_AND_HANDOFF_IDENTITY_CORRECTION_REQUIRED`；
2. 只修改Orchestrator-owned FULL machine row，使其exact匹配machine contract中的required subset，并将旧R2标为rejected、C1标为唯一active；
3. 创建一个direct child of `b74944fb0bd5ffa064ba1ac92ae390fff7e008dc`、subject exact为`chore(plan): activate real b2 linkage correction qualification`、changed paths exact为machine contract三路径的activation commit；
4. commit后worktree/stage/untracked为空，再dispatch一个fresh Executer。

Executer启动后使用repo-owned machine-contract parser各读取PLAN/FULL一次，并通过accepted provenance Git owner执行exact `6`个read-only argv：HEAD verify、HEAD metadata、HEAD diff-tree及三个`HEAD:path` owner blob lookup；验证HEAD、parent、subject、exact changed path set与三个owner worktree SHA/HEAD blob。任一preflight失败时controller source write、root、C1 reads与ER append保持0，只向EXECUTION_RESULT append一次pre-dispatch FAIL后停止。不得用alias、fallback、第二parser或直接shell Git。

## 2. Frozen accepted C1 inputs

只允许从exact source root读取以下四个absolute direct-child regular non-symlink mode-`0600`文件。每个文件exact一次`lstat`、一次`O_RDONLY|O_NOFOLLOW` open、descriptor read、before/after `fstat`、bytes/SHA验证；必须使用accepted provenance-I/O owner，禁止builtin `open`、`pathlib` read或第二reader。

| File | Bytes | Device | Inode | SHA-256 | Schema | Status |
| --- | ---: | ---: | ---: | --- | --- | --- |
| `path-owner-index.json` | `12195` | `16777240` | `2188342` | `b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35` | `p7_retained_r3_path_owner_index_v1` | `path_owner_resolved_waiting_for_planner` |
| `path-owner-index.sha256.json` | `682` | `16777240` | `2188343` | `867d1ffad5bd29f24dc81b24a58ce66393dd688833d3a4516fe7f45ef50875e9` | `p7_retained_r3_path_owner_index_seal_v1` | `sealed_waiting_for_planner` |
| `terminal-evidence.json` | `13455` | `16777240` | `2188344` | `c21a691272ca7466271349daa5b10236c9f36dfeb481d592e9c368a87e7a4763` | `p7_retained_r3_b2_c1_path_owner_terminal_v1` | `pass_waiting_for_planner` |
| `terminal-evidence.sha256.json` | `772` | `16777240` | `2188345` | `4bfebf4ad40e8c2e65ad2470faaed184f21d39eda73c13e689b09769d280752f` | `p7_retained_r3_b2_c1_path_owner_terminal_seal_v1` | `pass_waiting_for_planner` |

Source root必须exact absolute path、device `16777240`、inode `2188341`、mode `0700`。四者必须strict duplicate-key/non-finite reject并重构canonical compact sorted UTF-8 exact LF；顶层schema/status与table逐项exact type/value匹配。不得枚举parent/sibling、递归搜索、alternate path或读取index解析出的retained paths。

## 3. Corrected direct linkage contract

纠偏不得继续使用recursive `contains_identity`，不得要求accepted C1 logical target记录包含不存在的absolute `path`、`device`或`inode`。Physical identity由source-root-bound non-following descriptor read独立证明；logical linkage只从每个schema的direct owner field取值并进行exact key/type/value比较：

1. `path-owner-index.sha256.json.index`必须exact six keys：`relative_path`,`bytes`,`sha256`,`mode`,`schema`,`status`；值必须绑定physical index direct child及其accepted schema/status。
2. `terminal-evidence.json.index_identity`与`.index_seal_identity`各必须exact four keys：`relative_path`,`bytes`,`sha256`,`mode`；分别绑定physical index与index seal。
3. `terminal-evidence.sha256.json.terminal`必须exact six keys：`relative_path`,`bytes`,`sha256`,`mode`,`schema`,`status`；绑定physical terminal及accepted schema/status。
4. 所有`relative_path`必须是无分隔符、非`.`/`..`的exact filename，并与source root形成lexical direct child；不接受absolute、nested、alternate spelling、coercion、bool/int alias、recursive decoy或cross-record borrowing。
5. C1 terminal必须direct声明`terminal_write_returned=confirmed_by_terminal_seal_only_after_writer_return`；terminal seal必须direct声明`terminal_write_returned=true`及`terminal_seal_self_write_return=not_self_attested`。

Qualification source须对已读取的immutable in-memory payload运行exact `17` case matrix：`1`个真实四链pass；index seal的relative_path/bytes/SHA/mode/schema/status各`1`个drift；terminal index identity drift `1`；terminal index-seal identity drift `1`；terminal seal target drift `1`；missing field `1`；extra field `1`；type/coercion drift `1`；recursive decoy不得救活direct mismatch `1`；valid FAIL terminal seal使ER callback exact `1`次 `1`；invalid FAIL terminal seal使ER callback `0`次 `1`；authoritative 64-character physical seal SHA必须pass且62-character ER transcription必须作为同一identity-admission case被exact reject `1`。每个negative必须fail closed并有stable case code；不得通过重新读取文件构造case。该last case只消费PLAN冻结的physical identity与known-bad handoff string，不得读取或修改旧ER/failed root。

## 4. Single-process qualification and evidence lifecycle

Executer只可exclusive创建machine contract冻结的controller source，mode `0600`。Source写后立即由provenance owner读回一次，冻结bytes/SHA，strict UTF-8、AST parse及builtin compile。它只可import machine-contract、preparation、provenance-I/O三个accepted owners及无I/O stdlib数据/hash/JSON类型；禁止builtin/open/pathlib/raw-fd/subprocess/socket/env/device/release/validator imports或calls，禁止nested source、temporary helper、second state machine或仓库代码复制。

Static/compile/preflight全部通过后，才可由`create_exclusive_root`创建machine contract exact output root，mode `0700`。Root若已存在即fail closed；不得删除、复用、修复或选择第二root。允许direct-child file set exact为：

```text
c1-seal-linkage-qualification.json
c1-seal-linkage-qualification.sha256.json
terminal-evidence.json
terminal-evidence.sha256.json
execution-result-admission.json
```

所有write必须由`persist_canonical_json`完成，`0600`、`O_EXCL|O_NOFOLLOW`、partial-write loop、file fsync、directory fsync、strict reload。Qualification record必须绑定activation、PLAN/FULL physical identities、controller source、三个accepted owner identities、四个C1 physical identities、direct logical records、17-case results/counts、findings `REV-B2-R2-001/002/003`、authoritative old terminal-seal SHA `e7ffc6b080729afaf926656b68f5d2e1f50fe2be8d3f5475af6a4986a908be90`、known-bad ER transcription、旧failed root/controller/terminal/seal immutable disposition，以及all zero budgets。它不得包含retained payload、Git provenance结果、subordinate manifest、eligible/validated/consumable/authorized语义。

Terminal无论PASS/FAIL都必须记录primary error、completed matrix count、C1 read count、qualification presence/absence、root/source identities和所有zero counters，再physical write+seal。Seal有效后必须无条件建立preparation owner的`SealTargetIdentity`并调用`validate_and_emit_execution_result` exactly一次：

- PASS terminal写一个matching admission，qualification/seal target非null；
- pre-qualification FAIL terminal也写matching admission，qualification/seal target为null；
- terminal/seal写入或seal validation本身失败时admission为0，保留physical evidence并停止。

不得在overall PASS assertion之后才执行admission。Admission成功后Executer才可向`.agent-work/EXECUTION_RESULT.md` append一次matching handoff；PLAN、FULL、GUIDE、RESEARCH和archives均只读。

## 5. Acceptance, failure branches and locks

PASS要求：exact source/process/root `1/1/1`；C1 physical reads `4/4`；17-case matrix `17/17`；qualification+seal、terminal+seal、ER admission均存在且physical/logical linkage exact；authoritative old terminal-seal SHA为exact 64-character physical value且known-bad 62-character ER transcription被拒；failed R2 evidence未读取/修改；retained reads、Git provenance replay、manifest、validator、eligibility、release与所有device/scientific budgets exact `0`；source root/files pre/post descriptor identities不变。

任一gate失败即停止，后续预算为0；不得 retry、fallback、repair、overwrite、delete、root reuse、alternate root、second process或把partial output解释为pass。PASS/FAIL都停在`B2_R2_C1_LINKAGE_QUALIFICATION_WAITING_PLANNER_REVIEW`，Executer不得自行授权fresh real B2。

持续hard locks：旧R2 controller/root immutable rejected；real B2 retry/second root、retained-R3 reads、Git provenance replay、subordinate manifest、B3/B4、retained audit、canonical validator、eligibility、release generation/qualification/copy/consumption、network/DNS/`.env`/credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware、deployment全部`0`。Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

## 6. Duration and maintainability

本包只读取四个small accepted C1 JSON、运行17个in-memory cases并写五个small JSON，预计低于10分钟；不得使用visible Terminal长任务或automation。若preflight判断可能超过10分钟，Executer停止并回Planner/Orchestrator，不得自行改变launch topology。

维护性判断：本纠偏仅验证outer composition对既有C1 schema的direct mapping及seal-dominant ER admission，不修改repo production/test owner，不新增validator或release语义。通过后由后续fresh real-B2 package消费冻结合同；不得把qualification扩张为长期平行owner。
