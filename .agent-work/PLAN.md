# REF-P7-25-R2-B2-R2-C1-C1-C1-C1-C1：owner API conformance + source-root 离线纠偏资格包

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-R2-C1-C1-C1-C1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-C1-C1-C1-OWNER-API-CONFORMANCE-SOURCE-ROOT-QUALIFICATION-V1`

**当前唯一动作：** Orchestrator独立审核本review与PLAN、更新FULL并创建exact activation commit；activation后，Executer只运行一次fresh pure-offline owner-API-conformance/source-root qualification。不得读取或运行任何旧controller/source/root/evidence，不得读取retained R3、重跑real B2、写subordinate manifest或调用validator。

**唯一 Planner stop：**
`B2_R2_C1_C1_C1_C1_C1_OWNER_API_QUALIFICATION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1052-p7-retained-r3-b2-r2-c1-c1-c1-c1-git-ledger-interface-failure-review.md`，bytes `6576`，SHA-256
`35995c4fd83d5529a8d0372bd19d1133cd90ddda84422c2db9d88210e673016d`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_r2_c1_c1_c1_c1_c1_owner_api_conformance_source_root_qualification_v1","reference_task_id":"REF-P7-25-R2-B2-R2-C1-C1-C1-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-C1-C1-C1-OWNER-API-CONFORMANCE-SOURCE-ROOT-QUALIFICATION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"c48d8dd7bf648a2e59ce4f79fd1cb9a929c7461a","expected_subject":"chore(plan): activate b2 owner api correction qualification","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1052-p7-retained-r3-b2-r2-c1-c1-c1-c1-git-ledger-interface-failure-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-R2-C1-C1-C1-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-C1-C1-C1-OWNER-API-CONFORMANCE-SOURCE-ROOT-QUALIFICATION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","candidate_contract_orchestrator_verified":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"reviewed_failure":{"activation_commit":"486ae9274c3a670463b8bcece258fcb22ec7cc97","evidence_commit":"67a5579382d1a52ce6de3d287cf57a70868c0c75","controller_path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-c1-c1-c1-source-root-binding-controller-486ae92-20260731T1639Z.py","controller_bytes":23629,"controller_sha256":"0fbda54d91a6941782ea0470100ab55ca66811ca6e31a3463523be5ff0bd9c93","controller_mode":"0600","controller_device":16777240,"controller_inode":2218110,"process_count":1,"process_exit":1,"read_only_git_calls_returned":6,"stable_code":"AttributeError:GitLedger.returncode","root_create":0,"source_root_reads":0,"c1_reads":0,"matrix_completed":0,"artifacts":0,"disposition":"immutable_rejected_do_not_read_rerun_repair_rewrite_reuse_or_delete"},"controller_source":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-c1-c1-c1-c1-owner-api-controller-c48d8dd-20260731T1052Z.py","output_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-c1-c1-c1-c1-owner-api-qualification-c48d8dd-20260731T1052Z","output_root_required_absent":true,"source_root":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z","device":16777240,"inode":2188341,"physical_mode":448,"logical_mode":"0700"},"owner_api_contract":{"unknown_attribute_policy":"reject_before_dispatch","dynamic_attribute_access_rejected":true,"opaque_seal_gate_introspection_rejected":true,"git_ledger_fields":["argv","cwd","exit_code","stdout","stderr","stdout_sha256","stderr_sha256"],"git_success_field":"exit_code","git_success_value":0,"git_stderr_bytes":0,"git_stderr_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","all_six_ledgers_checked":true,"forbidden_dispatched_attribute":"returncode","accepted_return_type_count":9,"static_negative_unknown_attribute_cases":1,"static_positive_controller_cases":1},"source_root_binding_contract":{"pre_root_lstat_count":1,"post_root_lstat_count":1,"root_bound_read_count":4,"total_live_root_identity_observations":6,"all_c1_reads_require_root_keyword":true,"all_file_identity_root_fields_equal_expected":true,"literal_only_root_identity_rejected":true,"rootless_read_rejected":true,"direct_child_required":true,"pre_post_identity_exact":true},"logical_mode_contract":{"physical_mode_type":"integer","physical_mode_value":384,"logical_mode_type":"string","logical_mode_value":"0600","mapping":"format_physical_mode_as_exact_four_digit_lowercase_octal_without_prefix","alternate_representations_rejected":[384,true,"0o600","600","00600"]},"owners":{"machine_contract_sha256":"743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f","machine_contract_blob":"5c581f9b502bcab1809b6a61a082a47f4150e09f","preparation_sha256":"882f3819d161369012ce7fcd52cb1de1b9c56e4e1f821ff4554f6a1d8340738b","preparation_blob":"ecfa62a37bb33cf23743fcb8d0bba706f8795458","provenance_io_sha256":"f603721fb8b90510e2a09b199701c3f3358574d1247b5883ebdccc6f585b0a48","provenance_io_blob":"492f31f5f6999e28a1f0eb60240780e2c4826f4f"},"input_budgets":{"plan_reads":1,"full_reads":1,"controller_source_writes":1,"controller_source_reads":1,"old_source_reads":0,"old_root_reads":0,"old_evidence_reads":0,"source_root_explicit_lstat":2,"source_root_owner_lstat":4,"c1_lstat_open_read_hash_each":1,"c1_file_count":4,"retained_reads":0,"read_only_git_invocations":6},"execution_budgets":{"python_controller_process":1,"owner_api_predispatch_gate":1,"root_create":1,"qualification_write":1,"qualification_seal_write":1,"terminal_write":1,"terminal_seal_write":1,"er_admission_write":1,"execution_result_append":1,"matrix_case_count":24,"retry":0,"fallback":0,"alternate_source":0,"second_root":0,"second_process":0,"test_invocations":0,"compileall_invocations":0,"codegraph_sync":0,"git_stage":0,"git_commit":0},"zero_budgets":{"old_source_reads":0,"old_root_reads":0,"old_evidence_reads":0,"retained_artifact_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_R2_C1_C1_C1_C1_C1_OWNER_API_QUALIFICATION_WAITING_PLANNER_REVIEW"}`

## 1. Activation 与 immutable boundaries

本PLAN只有Orchestrator创建activation commit后才可执行。Activation必须是
`c48d8dd7bf648a2e59ce4f79fd1cb9a929c7461a`的direct child，subject和exact
三路径必须与machine row一致，commit后worktree/stage/untracked均为空。Executer
各读取PLAN/FULL一次；accepted Git owner call 1取得current full HEAD，calls 2-6
复用同一SHA并核对parent、subject、exact paths和三个owner blobs。

所有旧controller/source/root/evidence均为immutable rejected，read/exec/import/
stat/list/repair/rewrite/reuse/delete计数严格`0`。本PLAN中的旧身份仅是冻结literal，
不能变成I/O目标。任一pre-dispatch gate失败时fresh root、source-root及C1访问保持`0`，
launcher仅以首次controller source read保留的in-memory `FileIdentity`向ER append一次FAIL。

## 2. Source-backed owner API conformance gate（dispatch前）

Fresh controller source exclusive写一次、mode `0600`，由provenance owner读回一次，
strict UTF-8、AST parse、builtin compile。Outer launcher随后必须在**dispatch前**完成
一次source-backed gate：三个owner blob OID/SHA已由active Git tuple绑定，运行时只从这些
accepted imported classes的`dataclasses.fields`与明确public methods构造字段registry，
不得手抄或猜测接口。

Exact registry如下：

- `DirectoryIdentity`: `path,device,inode,mode`；
- `FileIdentity`: `path,data,byte_count,sha256,device,inode,mode,root`；
- `GitLedger`: `argv,cwd,exit_code,stdout,stderr,stdout_sha256,stderr_sha256`；
- `MachineContractEvidence`: `schema,owner,marker_ascii,source_bytes,source_sha256,candidate_count,candidate_lines,line_number,raw_row_bytes,raw_row_sha256,payload_bytes,payload_sha256,line_ending`，仅public method `to_mapping`；
- `ParsedMachineContract`: `value,evidence`；
- `ByteSpan`: `start,end`；`OwnedStatementPair`: `assignment_span,validation_span,function_name`；
- `PreparedControllerSource`: `source,source_sha256,pair`；
- `SealTargetIdentity`: `path,byte_count,sha256,device,inode`，仅public method `as_mapping`。

Gate须把controller每个accepted-owner call的assigned name绑定到exact return type，枚举
该name的所有direct attribute access并逐一核对registry。Unknown field、unbound result、
alias escape、dynamic `getattr`、`vars`、`__dict__`、reflection或内部seal gate属性访问均
fail closed。内部validated seal gate只可opaque传给callback。Negative specimen对
`GitLedger.returncode`必须被拒绝；实际dispatched AST内`returncode` occurrences必须为`0`。

六次Git调用返回后、root前，每个ledger必须逐一验证type exact、`exit_code == 0`、
`stderr == b""`、stderr SHA为machine row冻结值，并核对其余使用字段都在registry；不得
读取`returncode`。API gate及任一ledger失败均pre-root hard fail。

## 3. Root-first、C1 reads 与 exact 24-case matrix

API/activation gate全部通过后，先用`create_exclusive_root`创建唯一fresh root mode
`0700`，再访问source root。Source root冻结为machine row身份；允许stdlib `os.lstat`
exact pre/post各一次。由pre observation构造accepted `DirectoryIdentity`；四个accepted
C1文件各经`read_exact_file(..., root=same_identity)`exact一次，owner内部root lstat
共4次、direct-child gate必过，返回的四个`FileIdentity.root`与pre/post identity全等。
除两次root-only lstat外，不得builtin open/pathlib read/glob/listdir/resolve/enumeration。

四个C1冻结文件及身份、schema/status与上一PLAN完全不变：

| File | Bytes | Device | Inode | SHA-256 | Schema | Status |
| --- | ---: | ---: | ---: | --- | --- | --- |
| `path-owner-index.json` | `12195` | `16777240` | `2188342` | `b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35` | `p7_retained_r3_path_owner_index_v1` | `path_owner_resolved_waiting_for_planner` |
| `path-owner-index.sha256.json` | `682` | `16777240` | `2188343` | `867d1ffad5bd29f24dc81b24a58ce66393dd688833d3a4516fe7f45ef50875e9` | `p7_retained_r3_path_owner_index_seal_v1` | `sealed_waiting_for_planner` |
| `terminal-evidence.json` | `13455` | `16777240` | `2188344` | `c21a691272ca7466271349daa5b10236c9f36dfeb481d592e9c368a87e7a4763` | `p7_retained_r3_b2_c1_path_owner_terminal_v1` | `pass_waiting_for_planner` |
| `terminal-evidence.sha256.json` | `772` | `16777240` | `2188345` | `4bfebf4ad40e8c2e65ad2470faaed184f21d39eda73c13e689b09769d280752f` | `p7_retained_r3_b2_c1_path_owner_terminal_seal_v1` | `pass_waiting_for_planner` |

Strict canonical JSON/schema/status/type exact；logical record mode仅接受string `"0600"`，
physical mode为integer `384`。不得读取index内retained paths。

Matrix必须原样保留已规划的exact `24` cases：原20个linkage/logical-mode/FAIL
admission/hash cases，加root device drift、inode drift、mode drift、sibling/escape path
四个in-memory negatives。不得以owner API cases替换或增删这24项；owner API gate是
独立pre-dispatch acceptance surface。Real case仍要求4个root-bound identities和pre/post
全等。

## 4. Evidence lifecycle、acceptance 与 locks

允许direct-child artifacts exact为qualification、qualification seal、terminal、terminal
seal、ER admission五个。全部由`persist_canonical_json` exclusive/no-follow/fsync/reload。
PASS写qualification+seal；root后FAIL的qualification targets为null。PASS/FAIL均写terminal
和独立seal，并调用`validate_and_emit_execution_result` exact一次；valid FAIL admission后
重新抛primary error。Seal失败则admission `0`。Admission成功后才append ER一次。

PASS要求owner API gate `1/1`；unknown `returncode` negative拒绝且dispatched source occurrence
`0`；六个Git ledgers均使用`exit_code==0`与empty stderr；process/root `1/1`；root-first；
source-root observations `1+4+1`；C1 reads `4/4`；matrix `24/24`；五artifact physical/logical
linkage exact；所有旧I/O、retained、real B2、manifest、validator、eligibility、release、
network/device/scientific budgets全`0`。

任一失败不得retry/fallback/alternate source/root/second process、repair、overwrite或删除。
PASS/FAIL均停在唯一Planner stop，不得自行运行real B2。Retained R3持续
`RETAINED_UNVALIDATED_UNCONSUMED`。

预计低于10分钟，不使用visible Terminal或automation。

维护性判断：新增gate直接绑定accepted owner dataclass字段并覆盖全部controller return-type
属性访问，从根因阻断猜接口；不修改production/test owner，不新增validator、release或科学路径。
