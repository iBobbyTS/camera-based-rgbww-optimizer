# P7 R2-H3 terminal-owner correction review

**Review 时间：** 2026-07-26

**Reviewed PLAN SHA-256：** `3169ecac63e2eeb6469904c68f7e339ce6135b125c940a5edb710e11950d19e1`

**Reference task：** `REF-P7-04`

**Decision：** `rejected_real_output_and_audit_failure_owner_mismatch`

## 1. Independent verification

H3 root：
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-evidence-qualification-r2-h3-offline-terminal-owner-correction/20260726T123000Z`。

H1 regression `49/49`、H2 regression `31/31`、H3 final terminal matrix `26/26` 均通过。Closure SHA
`a6b41ebaaa71e3c180ec2b829546397a714b5084f0528c51e59c1f3aaa8c3ceb`；terminal owner
`6f61fb4c88dd8416c2f160aa917be78d6f287e06187903ff26f05c064529e952`；harness
`6768a50ee0a844456feab9674cc38d1a22136b760fcc2cba9d54866126797553`；driver
`547ddf525443ffbc66eef9fecbffb3b5667b818bc1d45201c3543f91a5c9226e`；matrix summary
`30c7c51f66928f2f65d49b1630bb30f9b926e7dd6c6bf39f27850fa912d98a6b`；validation summary
`761518573f7db6919025de1e6fc589cc85fd25f4044bf2a8d5981b2226c93c09`。

关键 fake accounting 独立读取 audit 后确认：child `1/78` + post 0 分别 wrapper `1/78`；post 70、七类 status
invalid、三域 fixture scan、combined failure 与 declared audit-write case 均 wrapper 70；direct child fields/status hashes 按
各 case 保留。Actual H3 PLAN 与 template 均 pre-child exit 65，child/production import false。

首次 partial failure record SHA
`a147d89402681f3dd2c61e7d270f9c1e78e72cd8b65761af4dec583c212e7326`；partial/final tree 声明分别
159/268（保留树当前 regular-file 计数分别 158/267，差一来自树 manifest 的 entry 计数口径）。Strict JSON audit
`610/610`，SHA `3a5470ab3680003c8dca207397fd4d321847479ccad39f78803c3f511567e5cc`；当前递归解析 610 JSON
entry、error 0。Authorization=true artifact 0；H1/H2/tracked immutability、residual、所有禁止 budget 为 0；future R2
仍 `0/1`。PLAN/FULL hashes exact，EXECUTION_RESULT §116 SHA
`05d0fd339efff1ba957aab91465fa7f5548b2977bafc9e617f9ece312e02a5d2`。

## 2. Rejection findings

`REV-H3-002`：real generated-output/provenance owner 绑定错误。

- Production argv 的 `--output-dir` 是 run-contract `output_root`，`--run-name evidence-r2`；production writer 实际生成
  `<output_root>/evidence-r2/qualification-evidence.json`。
- H3 terminal owner 却只扫描自己创建的 `<output_root>/generated-output/`，并在 real mode 因 config 为空、
  `evidence_present` 默认 true 而写入 `safe_fake_evidence_v1`。这既漏扫真实 production evidence，又向真实输出树注入 fake
  evidence，可能掩盖真实 evidence 缺失或违规内容。
- H3 自建空 `input-provenance.json` 并只扫描该文件，不绑定 production evidence 的实际 input references；允许的历史
  reference 也只比较声明字典，没有像 H1 accepted validator 一样重新验证 target regular/non-symlink/bytes/hash。

`REV-H3-003`：primary terminal-audit write failure recovery 未被实现或真实测试。

- `audit_write_failure=true` 时代码没有尝试 primary `terminal-audit.json` 写入，也没有捕获 atomic write exception；它只是
  直接选择 `terminal-audit-fallback.json` 并人为加入 finding。
- real execution 中若 primary `atomic_json` 真正抛错，当前 owner 没有 exception handler/fallback audit；fake case 23 因此
  不能证明 PLAN 要求的真实 failure branch，尽管 direct status 文件会留存。

所以 `REV-H2-001` 的 child/post 非零传播子问题已修复，但完整 closure 不成立；H3 **判退**，不得发布或执行 future R2。

## 3. Exact next branch

发布 bounded `R2-H4-OFFLINE-REAL-OUTPUT-OWNER-CORRECTION`：保留已通过的 H2 gate 与 H3 status/accounting，删除 real
mode 的 fake evidence/provenance writer，把 strict scan/validation 精确绑定到 production 实际
`<output_root>/evidence-r2/qualification-evidence.json` 及其 input references；补上真实可注入的 primary audit atomic-write
exception handling/fallback test。全程只用 injected production-shaped child fixture，不调用 production adapter。

H4 完成后再次停 Planner；future R2 budget 保持 `0/1`，授权 real contract artifact 保持 0。

## 4. Suggested Orchestrator reference update

- H3 status → `rejected_REV-H3-002_REV-H3-003`；
- `REV-H2-001` → `partially_closed_child_status_accounting_only`；
- REF-P7-04 current action → R2-H4 offline real-output owner correction；
- future R2 remains locked，all live/device/formal routes remain `PAUSED_BY_HUMAN_PRIORITY`。

维护性判断：问题仍局限于外置 terminal owner 的 real/fake 输出映射和 failure injection 边界；无需修改 production 或设备
路径，但必须消除 fake owner 对 real branch 的污染。
