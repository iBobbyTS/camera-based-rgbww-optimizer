# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-3：local-run bytecode owner correction

**计划状态：** `WAITING_ORCHESTRATOR_FULL_ALIGNMENT`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-3`

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-3-BYTECODE-OWNER`

**唯一当前动作：** Orchestrator 将 FULL active task/contract 对齐到 C3，整理并提交当前 C2
test/evidence/review 变更；随后由一个新的 Planner activation pass 冻结 committed parent/child、FULL、
PLAN、test/controller identity 和 fresh-root absence。当前不得派发 Executer。

**C2 review archive：**
`.agent-work/PLANS/20260730-0348-p7-retained-r3-option-b-b1a-c3e6f19-corrective-2-review.md`；
SHA-256 `d72cd628103396b51d05d3baeee1564da319582ed90aae0347984fd0e69a8072`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_3_pre_activation_plan_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-3","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-3-BYTECODE-OWNER","dispatch_state":"waiting_orchestrator_full_alignment","single_current_action":"orchestrator_align_full_commit_c2_evidence_then_fresh_planner_activation","frozen_current_test":{"path":"tests/test_p7_retained_r3_exact_five_controller.py","sha256":"e9b51d5d83319e68d29da68a2a023ef6feb248bf6c4b3ce8d776a70e63b957e6"},"frozen_controller":{"path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py","sha256":"746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726","preserve_byte_exact":true},"old_c2_evidence":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-2-offline","preserve_immutable":true,"artifact_count":5},"fresh_c3_evidence_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-3-offline","fresh_root_absent_at_review":true,"repo_edit_paths":["tests/test_p7_retained_r3_exact_five_controller.py"],"allowed_run_bytecode_owner_opcodes":[["execute_prepared_exact_five_controller","STORE_FAST"],["execute_prepared_exact_five_controller","LOAD_FAST"]],"forbidden_run_bytecode_opcodes":["LOAD_GLOBAL","LOAD_NAME","LOAD_ATTR","LOAD_METHOD"],"validation_chain":{"fail_fast":true,"compileall":1,"targeted_unittest":1,"focused_unittest":1,"full_unittest":1,"codegraph_sync":1,"git_diff_check":1,"retry":0},"operation_budgets":{"controller_source_edits":0,"controller_calls":0,"candidate_payload_reads":0,"retained_r3_reads":0,"canonical_validator_calls":0,"eligibility_emissions":0,"manifest_writes":0,"release_calls":0,"network_calls":0,"env_reads":0,"device_calls":0,"camera_calls":0,"ray_calls":0,"strip_calls":0,"cleanup_calls":0,"formal_calls":0,"public_analyzer_calls":0},"planner_stop":"F19_CORRECTIVE_3_WAITING_FRESH_PLANNER_ACTIVATION"}`

## C3 activation必须冻结的执行合同

1. 唯一repo实现改动仍为dedicated test；controller必须保持上述SHA byte-exact。当前test after SHA
   是C3 before SHA，不得回退C2中已建立的AST、global/name、attribute/method和forbidden-import边界。
2. 仅修正最后的bytecode断言：argval `run`只能由
   `execute_prepared_exact_five_controller`拥有，且允许的opcode精确为`STORE_FAST`和`LOAD_FAST`；
   其他owner/opcode全部拒绝。AST必须继续证明唯一nested `def run`及全部`Name("run")`调用的词法owner。
3. 继续禁止global/name `run`、attribute/method `run`、subprocess式调用、直接I/O、forbidden import、
   generic allowlist、字符串缺失替代、production rename或删除static regression。
4. C2 root及五个冻结artifact保持byte-exact；C3必须exclusive-create上述fresh root，mode `0700`，
   artifacts regular/non-symlink/exclusive-create/mode `0600`，terminal seal不可变。
5. 完整链固定为compileall、targeted 11 tests、focused、full、CodeGraph、`git diff --check`，每项最多
   一次、fail-fast、retry/fallback `0`；PASS/FAIL均append ER最多一次并停在Planner门。
6. retained R3/candidate/release不得读取或probe；真实controller/validator/eligibility/manifest consumer、
   network/env/device/camera/Ray/strip/cleanup/formal/public analyzer及B2全部保持`0`和硬锁。

**Planner stop：** `F19_CORRECTIVE_3_WAITING_FRESH_PLANNER_ACTIVATION`。

**维护性判断：** 下一包只修正dedicated test对Python局部函数绑定字节码的语义建模，不改变production
controller或所有权边界；精确owner/opcode断言比generic name allowlist更可维护，无需Advisor或架构重构。
