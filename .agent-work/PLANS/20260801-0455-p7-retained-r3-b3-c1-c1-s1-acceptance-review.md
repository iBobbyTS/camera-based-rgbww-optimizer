# P7 retained-R3 Option B：B3-C1-C1-S1 terminal supersession 验收归档

**审核日期：** `2026-08-01`

**Reviewed task：** `REF-P7-25-R2-B3-C1-C1-S1`

**Activation：** `c2949adc8230a7e624485fe4ecf8aaf8ec0a0380`

**Evidence commit：** `751a04d14c263853d56836049ce1bb3038a5e990`

**Planner decision：**
`ACCEPTED_COMPLETE_GIT_ER_TERMINAL_SUPERSESSION_RECORDED`

## 1. 审核范围与方法

Planner独立只读检查active PLAN、activation/evidence commit metadata、两版committed
`.agent-work/EXECUTION_RESULT.md` bytes、最长公共前缀与physical EOF、末尾strict JSON payload、预算与zero locks。
未读取external governance evidence、Advisor attachment、old B2 manifest five、C1或retained R3 artifacts；未运行
controller、test、CodeGraph、canonical validator、retained audit、release、network或device。

Evidence commit parent为`c2949adc8230a7e624485fe4ecf8aaf8ec0a0380`，subject为
`chore(evidence): append B3 governance supersession`，changed path exact one：
`.agent-work/EXECUTION_RESULT.md`。

## 2. 独立证据重算

- parent ER：bytes `1301614`，SHA-256
  `6c2ccf6170aca4e1b51b1192b1be93ab0a43457063ac3675be5afb052c64128c`；
- new ER：bytes `1309616`，SHA-256
  `f0474fcc4b6f835d91c9483f4923b9ca50f54ce3b0fa7816ca2be32caeee7546`；
- parent bytes是new ER的完整prefix，最长公共前缀`1301614`，preserved suffix `0`；
- physical EOF新增suffix：bytes `8002`，SHA-256
  `f091513ca4d160fbc0648e04d283591da8fc02a1934c264299a91b0b5f190142`；
- EOF最后fenced payload为duplicate-free/nonfinite-safe strict JSON，且是canonical encoding；schema、reference、contract、
  outcome与唯一Planner stop均匹配active PLAN；
- payload重算并冻结旧handoff的non-EOF insertion、unauthorized CodeGraph3及governance position8/9 owner
  misbinding，不修改或再生旧payload。

## 3. 预算、锁与验收

实际Git reads `14/18`、committed ER reads `2/2`、apply_patch `1/1`、ER append `1/1`、retry/fallback/
postappend operations均`0`。External governance/Advisor/real manifest/C1/retained/code/test/CodeGraph/controller/
validator/audit/release/network/device/formal与implementation commit全部`0`。

`RETAINED_UNVALIDATED_UNCONSUMED`保持不变；canonical lineage validator仍是唯一eligibility owner；B4、release
consumption、设备、FORMAL-R6、strip、TD-C、sentinel与P8继续锁定。本验收只credit repository evidence ledger的
physical-EOF supersession，不credit旧B3-C1-C1验证通过，也不生成eligibility。

## 4. Exact next branch

下一唯一包为`REF-P7-25-R2-B3-C2` bounded production governance identity correction：

1. 只修改现有production owner
   `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py`及其dedicated test；
2. 将`RealManifestBaselineIdentity.advisor_decision_sha256`更名为
   `lineage_owner_decision_evidence_sha256`并修正唯一使用点；
3. 保持baseline positional payload的shape/value完全不变：zero-based position 8明确属于external lineage-owner
   decision evidence `842cfad...`，position 9仍属于Advisor Option-B attachment `91a88...`；Advisor request Git文件
   `advisor/4/0.AUDIT/07-guide4-to-retained-r3-lineage-owner-decision.md`由独立Git owner/path识别，不得放入或替换
   baseline positions；
4. old B2 manifest five、old/new ER payload与external/retained inputs immutable，不repair/regenerate/read；
5. 按CodeGraph preflight→two-path edit→dedicated/focused/compileall/full→CodeGraph sync→diff check完成离线验证；
   不运行synthetic/real audit/validator/eligibility/release/device。

维护性判断：本轮supersession已在单一ER ledger边界闭环。下一包只纠正existing frozen dataclass的误导字段名及
dedicated test，不新增parallel provenance owner，不改变artifact schema或科学合同。
