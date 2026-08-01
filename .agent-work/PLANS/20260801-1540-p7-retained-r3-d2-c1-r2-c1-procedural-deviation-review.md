# P7 retained-R3 Option B：D2-C1-R2-C1 attribution事实与程序偏差验收归档

**Planner 日期：** `2026-08-01 15:40 America/Edmonton`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-LEDGER-BINDING-CORRECTIVE-ATTRIBUTION-V1`

**Activation：** `9ddd486d1923cd8cb87d565a8b874f0ecac95e2a`

**Evidence：** `fd9291a49383c20f742137f5c798ddbca10240d6`

**Planner 决定：** `REJECTED_EXECUTION_HANDOFF_AND_POSTTERMINAL_READ_CONTRACT_VIOLATION_ATTRIBUTION_FACTS_ACCEPTED_PENDING_READ_ONLY_S1`

## 1. Reviewed scope、topology 与证据边界

Planner完整读取repo `AGENTS.md`、project skill、activation committed PLAN、适用FULL machine state/reference task、evidence ER最后完整section至physical EOF，并独立核验activation/evidence topology、fresh root exact inventory/modes/hashes/seals、report/terminal matrix结构与边界状态。Fresh root检查严格只读；未修改artifact，未重跑controller、selector、Git ledger、self-check、tests、validator、release、network或device，也未读取production/test source。

Activation `9ddd486d1923cd8cb87d565a8b874f0ecac95e2a`是`5f80e929b8c9f79a0fd1ecc23cf5486709f2c60c`的direct child，subject exact `chore(plan): correct ledger row binding`，changed paths exact且有序为FULL、PLAN及`.agent-work/PLANS/20260801-1524-p7-retained-r3-d2-c1-r2-ledger-binding-failure-review.md`。Evidence `fd9291a49383c20f742137f5c798ddbca10240d6`是activation direct child，subject exact `chore(evidence): record corrected ledger attribution`，changed path exact仅`.agent-work/EXECUTION_RESULT.md`。Review开始时HEAD exact evidence且worktree clean。

Activation ER bytes `1534254`、SHA-256 `bc154807a4cf3a2bb5d21231dc11e6e4e2fc07af546989ba86f6aca097032dda`。Evidence ER bytes `1540765`、SHA-256 `7cd4258114b184c29ed37916c1ea2a3045fb40f8700964336f5b35dbae36b6c3`；最后physical EOF suffix bytes `6511`、SHA-256 `3052d554052a79862f179c37ca02970b0ba81d648c66ce5ac1652cb49869d59c`。

## 2. 可接受的 attribution 事实

Fresh root `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-owner-expectation-attribution-d2-c1-r2-c1-9ddd486d1923` mode exact `0700`，inventory exact六件且每件mode `0600`：

- contract `4344` bytes / `92fa34096d6de0110eba198287d70b4b2032d60bb05a4b4cd2ee2f8873b98967`
- contract seal `154` / `6f4e7d5fc9f4eebdeefb38c7d72f51bcc61b47f757fa21c8bb7e2519f0eba9c3`
- report `41685` / `923f32afae0f375469d03a6b6a18a71261c19e7bcfefcd0bb041bdfde11b849a`
- report seal `166` / `068ee79657f4765928b80909514d37b431d779fc2a6ccd914c127e1453c08c49`
- terminal `42810` / `418efd0e974432633d21f1ad7e18a8f24633ef1d4a21a82d466dc215efdaa936`
- terminal seal `153` / `cde7160f3685cbeccd8951e9370a019691599b39b00c958eeb12b4afe9b01bc3`

三份seal的target/bytes/SHA与对应artifact exact。Report与terminal中的`.matrix` strict JSON结构哈希均为`4a1bcd6ecf186c277875041ac809857a84b91004047201556a84a8953c3b4240`，ordered indices exact `1..18`；selector、Git attempts与Git processes各`18`，retry/fallback `0`。

Ledger-binding proof exact成立：frozen path `$.ledger_rows`、owner `PLAN_MACHINE_ROOT`、exact type `builtins.tuple`、cardinality `18`、binding identity same object、indices `1..18`；`synthetic_spec` exact type `builtins.mappingproxy`、exact keys为`repo_root/activation/baseline/git_file_bytes_acquisition`且`ledger_rows` absent。Typed projection walks `8`、projection/canonical serialization/strict reload各`4`，四次Git file acquisition完成。

完整matrix为15 match与3 mismatch。First mismatch row `7` `activation_changed_paths`、owner-returned kind `paths`：actual为历史root commit完整ordered NUL path tuple，frozen expected仅helper/test两路径。Row `15` `baseline_helper_patch`与row `18` `baseline_test_patch`的owner-returned kind均为`sha`且owner value均为combined patch SHA `dc362c278425b25e15048495e3324d6da2e1c5f3c43d866c7f04117f0b7c23b3`；actual individual patch SHA分别为`f325afe07d3faaca557d94a760652fd6c9ede66201e52b3cb4ccc196810750ec`与`a99769889cfe01b6ed66193823105c506c444312e58104f1685c9fdc20c7f2ed`。

这些是可接受的synthetic/injected engineering attribution facts：它们证明root-ledger binding已纠正，并定位了frozen synthetic expectation与existing owner selector实际返回值的三个不一致。它们不是科学分支结论，也不构成production owner、lineage、manifest truth、eligibility或release信用；Advisor无需参与该工程事实判断。

## 3. 不可接受的执行合同偏差

原合同要求terminal/seal由precomputed canonical bytes写入，`postterminal_root_reads_for_handoff=0`，并要求在physical ER EOF append `same handoff`。实际执行在terminal写入后为构造ER handoff再次读取terminal一次；这是明确的postterminal fresh-root read，不能由未记录该动作的counters或artifact正确性豁免。

此外，preterminal handoff包含完整18-row matrix，而evidence ER EOF的compact `EXECUTION_HANDOFF_JSON`只给出`full_ordered_18_row_matrix_artifact` path/bytes/SHA，没有逐项内嵌相同完整matrix。因此ER append不是合同要求的same handoff；`er_complete_suffix_extractions=1`、`er_apply_patch_appends=1`与physical EOF位置正确不能弥补内容缺失。

结论是D2-C1-R2-C1原执行合同拒绝，不可标记为完整PASS。但sealed report、seal与terminal彼此一致，且偏差发生在matrix与artifact已经完成之后；无需第三次重跑18 selector/18 Git ledger。最小纠偏是一次S1只读supersession，完整封存matrix和两项程序偏差。

## 4. Exact successor 与边界

唯一successor为`REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1`，contract `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-READ-ONLY-ATTRIBUTION-HANDOFF-SUPERSESSION-V1`。

S1只能读取committed PLAN/FULL/ER和本轮sealed report及report seal；不得读取terminal/source/其他fresh或旧root文件，不得stat/list/hash整个root。它必须验证report与seal exact fixed identities，strict-load report一次，冻结完整`.matrix`，验证18 indices、15/3 match分布、mismatch rows `7/15/18`、ledger proof、counters、zero locks及false boundary；随后在ER physical EOF一次append完整supersession JSON，逐项内嵌完整18-row matrix，并明确记录原执行的terminal post-read和compact-ER偏差。不得修改fresh root、重跑selector/Git/controller/self-check或形成更高层结论。

**Exact next Planner stop：** `B3_C3_C4_R5_R1_C1_R2_R1_C2_S1_C1_R1_D1_D2_C1_R2_C1_S1_READ_ONLY_ATTRIBUTION_HANDOFF_SUPERSESSION_WAITING_PLANNER_REVIEW`。

## 5. Required FULL updates（Orchestrator-owned）

- 将`d2_c1_r2_c1_status`设为`REJECTED_EXECUTION_HANDOFF_AND_POSTTERMINAL_READ_CONTRACT_VIOLATION_ATTRIBUTION_FACTS_ACCEPTED_PENDING_S1`，并记录evidence commit `fd9291a49383c20f742137f5c798ddbca10240d6`。
- 新增并激活唯一task `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1`，active contract切换到上述read-only supersession V1，`active_task_count=1`。
- `real_self_check_owner_status`与`real_execution_status`继续blocked on D2-C1-R2-C1-S1 acceptance；不得提前解锁real self-check。
- 保持`retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`、`manifest_authority=SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER`、production owner/lineage/eligibility/release均false及device authorization false。

维护性判断：本轮不改production owner或repository代码；S1只补齐durable handoff并诚实记录procedural deviation，避免无价值地第三次重跑完整ledger，无后续代码清理建议。
