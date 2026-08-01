# P7 retained-R3 Option B：B3-C3-C2 durable fact diagnostic 审核归档

**归档时间：** `2026-08-01 06:21 America/Edmonton`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C2`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C2-PURE-DURABLE-TOP-LEVEL-FACT-DIAGNOSTIC-V1`

**Activation：** `ec7cb8c387d00f265cbc5eb348a1b534105c001b`

**Evidence commit：** `87d8d1848722e4d95b8719f624118658f90efd14`

**Planner decision：**
`DIAGNOSTIC_FACTS_ACCEPTED_EXECUTION_REJECTED_PLAN_FACT_MISBOUND_AND_APPLY_PATCH_BUDGET_EXCEEDED`

## 1. 审核范围与方法

Planner只读核对committed active PLAN、FULL machine state、Git commit/blob topology及evidence commit新增的ER physical-EOF
suffix。按本包禁止项，没有读取fresh external package、diagnostic artifacts本体、accepted real manifest本体、retained R3、C1或
其他external inputs；没有读取repository production/test源码，也没有调用test、controller、CodeGraph、canonical validator、retained
audit、release、network或device入口。

本轮使用second-pass evidence reset追溯了committed PLAN中的字段归属；没有创建额外debug owner，因为active PLAN与本归档已经构成
唯一持久状态。

## 2. Git、ER 与 physical EOF

- activation `ec7cb8c...`是`b923f4e...`的direct child，subject exact
  `chore(plan): activate pure top-level fact diagnostic`，changed paths为FULL、PLAN及C1 review archive三项；
- evidence `87d8d18...`是activation的direct child，subject exact
  `chore(evidence): record B3-C3-C2 top-level diagnostic`，changed path只有`.agent-work/EXECUTION_RESULT.md`；
- parent ER bytes `1327409`、SHA-256
  `594615188d35bc6c31833d0064c2fbeb32626cbee15226483f21cb936e69e50d`；
- evidence ER bytes `1332706`、SHA-256
  `0b5514770f001f329b84922789820f37c9c01f2763579653df253f0cf81602e1`；
- parent是current完整byte prefix；physical EOF suffix bytes `5297`、SHA-256
  `0ddfcfc2dc3f12aa5e13801689a01979c7e58edff3840a7b96425fa0ffff6f2f`，文件以LF结束；
- suffix只有一个外层handoff section；heading字符串第二次出现仅是strict JSON中
  `handoff_append_contract.heading`的值，不是第二次物理append；payload strict JSON解析通过；
- `git diff --check ec7cb8c..87d8d18`通过，审核开始时porcelain clean。

因此Git/ER topology与唯一physical EOF append有效，不需要另建Git/ER-only supersession包。

## 3. 接受的 diagnostic facts

Fresh root、controller与diagnostic identities均被terminal payload精确冻结：

- root `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-c3-c2-ec7cb8c387d0`，mode0700；
- controller bytes `17402`、mode0600、SHA-256
  `a91c49f327e9bc6f1e1eccb46208c931cfce4bec4b9a8c5c56f779083449eaf3`，pre/post相同；
- manifest identity bytes `4651`、mode0600、SHA-256
  `c3ac3bc712965e39453b32e8cde15ebc7e53dcc7e1a99f1ecb38177f65cadfaf`；
- fact bytes `1694`、mode0600、SHA-256
  `d364bb97e420844e7a718817bf43bc0297ea22351509c917a51b5f456c295f81`；
- seal bytes `132`、mode0600、SHA-256
  `ea4b150487f8cb578ec0ef185bb5005245b3d9dff16e5be36bc954f1b956ec1e`；
- fact/seal在judgment前各replay一次且验证通过；owned residual为空；retry/fallback/postappend operations均0。

Payload报告exact四项比较，mismatch数组只有：`immutable expected boolean true, observed null`。因此同一次snapshot的JSON object、
`schema == p7_retained_r3_audit_provenance_manifest_v2`及
`status == sealed_subordinate_provenance_evidence`三项均匹配。这个结论只接受为diagnostic fact，不等于remaining self-check、tests、
synthetic、retained audit或eligibility完成。

## 4. REV-B3-C3-C2-001 — `immutable`的语义 owner 被PLAN误绑定

追溯B3 committed machine reference可见，`real_manifest`对象同时保存root、mode、五件套identity、schema、status与
`immutable=true`。该布尔值描述accepted external package的路径、provenance及生命周期处置：旧package保持byte-immutable，禁止
rewrite/repair/regenerate/reuse为新artifact。它不是manifest JSON的top-level schema字段。

更早的accepted B3 review已经冻结：manifest artifact只要求schema/status；terminal只含status；admission只含
admitted/eligibility/release_consumable。当前diagnostic的observed `null`表示`immutable` key absent，不是JSON null值，更不是
manifest defect。Planner此前把machine reference disposition反投影为artifact top-level expected fact，属于验收合同错误。

后继必须把两层明确分开：

1. `real_manifest_reference.disposition`冻结路径/身份/禁止写入、repair、regenerate及failed-root reuse；
2. `manifest_top_level_contract`只核对JSON object、schema与status，不要求、搜索、推导或禁止额外`immutable`字段，也不冻结完整key set。

不得修改、重建或放宽real manifest；不得把observed keys变成generic schema allowlist或eligibility owner。

## 5. REV-B3-C3-C2-002 — execution budget独立失败

PLAN冻结`apply_patch_invocations=2`，实际为`3`。第一次ER append调用因context verification失败且未改变文件，第二次append成功；
虽然最终ER bytes、EOF topology与postappend0有效，但失败的调用仍消耗invocation budget。因此C2 execution不得标记
`DIAGNOSTIC_COMPLETE`或任何success label。

该预算失败与diagnostic事实真伪分层：durable fact/seal identities、replay、known comparisons及zero locks可被后继只读引用；C2
package整体保持immutable evidence-only，禁止复用、修补或改写。后继仍要求source create与ER append各一次成功
`apply_patch`，exact total2；任何failed invocation立即fail closed，不能用第二次尝试把本轮报success。

## 6. 决定、锁与后继

本轮接受Git/ER evidence、durable diagnostic identities、object/schema/status事实、`immutable` absent归因及全部zero locks；拒绝C2
execution success，也拒绝manifest defect结论。Focused/full/synthetic实际均0，postcommit verification未完成。

后继直接合并为一个fresh byte-stable postcommit verification包，不另设无意义的Git/ER中转：corrected remaining self-check通过后，
依序运行focused exact1/83、full exact1/800、brand-new synthetic exact1；任何failure立即停止。Canonical validator、real retained
audit、eligibility emission、release consumption、network/device及later stages全部继续锁定。

Next reference task：`REF-P7-25-R2-B3-C3-C3`。

Next contract：
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C3-CORRECTED-BYTE-STABLE-POSTCOMMIT-VERIFICATION-V1`。

Planner stop：
`B3_C3_C3_CORRECTED_BYTE_STABLE_POSTCOMMIT_VERIFICATION_WAITING_PLANNER_REVIEW`。

维护性判断：纠正的是一次性execution contract的字段归属，不改production、manifest schema或canonical eligibility owner；新包复用既有
builder/runtime/test owners，只把artifact facts与package disposition分层，并保留完整回归链。
