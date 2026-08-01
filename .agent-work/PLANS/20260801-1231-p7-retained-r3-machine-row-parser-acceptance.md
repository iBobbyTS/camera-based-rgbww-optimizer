# P7 retained-R3 Option B：P1-C1-R1-C1 machine-row parser owner 验收

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1-C1-R1-C1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-P1-C1-R1-C1-EVIDENCE-OWNER-TEST-CORRECTION-V1`

**Planner decision：** `ACCEPTED_COMPLETE_REPO_OWNED_MACHINE_ROW_PARSER_OWNER`

## 1. 冻结 topology 与 scope

- activation `619beeacccd27f9d67b6d72aa5f7b603b164f30b`，parent `4b512ecb3b5caf34c25decb45f967f466c3b8909`，subject exact `chore(plan): correct parser evidence owner expectation`；changed paths exact FULL、PLAN与`20260801-1220` review archive。
- implementation `495adc02931a6a627fec353540ed0df0f61cf4ee`，parent exact activation，subject exact `fix(p7): harden machine row parsing`；changed paths exact `src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py`与`tests/test_agent_work_machine_contract.py`。
- evidence `e4f10665752651d612ae90d4be114d45b7ed38d0`，parent exact implementation，subject exact `chore(evidence): record parser evidence owner correction`；changed path exact `.agent-work/EXECUTION_RESULT.md`。
- 当前worktree clean；未发现额外source、test、PLAN、FULL、archive或runtime artifact写入。

## 2. Implementation 与 identity 验收

既有single production owner已扩展为public `parse_machine_row(complete_text, literal_marker)`，两个legacy wrapper继续委派同一`_parse_machine_row`。实现保持exact-bytes输入、唯一Markdown row、whole-line two-backtick、LF、strict UTF-8/JSON object、duplicate-key/nonfinite rejection；成功值递归冻结为`MappingProxyType`/tuple。generic owner `PLAN_MACHINE_CONTRACT`与legacy owner `PLAN`按合同有意不同，其余evidence fields exact一致。

最终identity独立复核为：

- source：bytes `9414`，SHA-256 `a02a30c026fba548c81c04a277e2f235385ddb8a459c4ff2f73c91ee87c3737e`，blob `ce2200181bd2a493cfaab621daa17b89a13bdf1f`；
- test：bytes `14638`，SHA-256 `8f9ba840cc0846cdb4c82edf9ebf8540a748c86a6331227a7a0e2d8e27e328a0`，blob `be1d5e955edf38566f274bedcac02b1a4fa93e44`。

CodeGraph只读验收确认`parse_plan_machine_contract`与`parse_full_plan_machine_state`仍由同一production core拥有，direct caller blast radius已被focused suite覆盖；test-local recursive semantic adapter没有进入production。

## 3. Validation 与 evidence 质量

Executer记录：targeted `15/15`、focused `41/41`、指定full unittest discover command exit `0`/PASS、compileall `1`、CodeGraph sync `1`、post-query `1`、diff check PASS、status exact two、postcommit targeted `15/15`。ER没有记录full tests-run总数，但active PLAN只要求指定discover命令全通过，并未冻结数量；exact command、exit `0`和PASS已满足该硬门。因此该省略是非阻塞的evidence detail，不构成重跑或拒收理由。

ER handoff以一次complete-last-section-heading-to-physical-EOF extraction和一次append封存，append后operations `0`；最终handoff位于physical EOF，无需supersession。

## 4. Locks、residual risk 与 next branch

real artifacts、old roots、self-check owner、canonical validator、eligibility、release、network与全部device操作均为`0`。retained R3仍是`RETAINED_UNVALIDATED_UNCONSUMED`，本验收不授予eligibility或release consumption。

Residual risk仅是full suite未携带tests-run计数；命令/退出状态已经满足当前合同。后续PLAN若把计数作为科学或provenance事实，应明确冻结并要求记录actual count。

**Exact next branch：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1`。恢复context-bound corrected Git seam owner + fresh pure-offline real self-check；activation machine-row gate必须直接调用本轮接受的repo-owned `parse_plan_machine_contract`和`parse_full_plan_machine_state`，输入raw bytes，禁止任何手写Markdown扫描、bare-marker搜索、decode/read_text或并行parser。canonical validator、eligibility、release、network与device继续锁定。

维护性判断：machine-row grammar与deep immutability集中在单一owner，legacy wrapper和caller边界清晰，dedicated/focused/full验证充足；无需跟进重构。
