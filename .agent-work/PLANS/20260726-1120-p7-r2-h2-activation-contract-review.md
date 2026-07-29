# P7 R2-H2 activation-contract review

**Review 时间：** 2026-07-26

**Reviewed PLAN SHA-256：** `d6ca4865f04a04e921dfe26e1314481498e562308678aadb87da3efcf00b1665`

**Reference task：** `REF-P7-04`

**Decision：** `rejected_terminal_accounting_and_scan_owner_missing`

## 1. Independent verification

H2 root：
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-evidence-qualification-r2-h2-offline-activation-contract/20260726T120000Z`。

Exact owners：harness SHA
`cfb9c6f51d8db548c36497903d42d636f762b9c63a125f585faff699086896bb`；later gate
`411067fbf9d9787867897af06f40508bb32ac4cd84e1216994b88060cd2b3b0b`；matrix driver
`17df48276b3374995a58587a12007e4cba31e186987884867e8f87a9b502af1b`；non-authorizing template
`404526ce8ffda73f9ddbd7a9a7d51da60f0c8293d2543e778884653fe218a9f3`；final summary
`6811583826401376bba38fcba4d25b6a76081c84cb34455a76906be12d63c24b`。

H1 regression `49/49`。Final later-gate v3 `31/31`，其中只有一个 copied fake positive；其 schema 为
`p7_td_b_r2_later_plan_run_contract_fake_fixture_v1`、status 为
`copied_fake_fixture_non_authorizing`、`execution_authorized_by_later_plan=false`，且只启动 injected Python child。
其余 30 个均在 child 前 exit 65，`child_started=false`、`adapter_imported=false`。当前 H2 PLAN case 同样 exit 65；
授权 run-contract artifact 数为 0。

v1 `29/31` preserved summary SHA
`5b480130d7e939f48efe089b99551d09721ac77fb5ff854aa79743492ff27d12`；v2 `31/31` superseded summary SHA
`d0fe594ffe402802e77ab8b7fe5876d2599a477f321bb2e35e3ff264cbdd9f42`。Owned v1/v2 fixture tree cleanup
为 exact dry-run 后删除 138 files，summary 保留。Strict JSON audit `337/337`，SHA
`de88f023af7c92a7a0a48adae0763997cb24e89270258aeac276cb9fc8a98a5b`；当前保留 JSON 独立解析通过。
zsh syntax、Python compile、`git diff --check` 通过。

Frozen/canonical/tracked immutability 与 H1 before/after exact；所有 device/network/live/formal/release/commit budget 为 0，
future R2 仍为 `0/1`。EXECUTION_RESULT §115 当前 SHA
`7e1186c63bbb795f10640f2ef1f293a4d70d61913121b4ccd84e911d96bc3a18`；FULL disk SHA
`4e79700d26b819807ed81c0e71bfc89730adb9c1dc28f120a73f5e52b3b88bc0`。

## 2. Rejection finding

`REV-H2-001`：H2 real-capable gate 没有实现 PLAN §3 要求的终态 accounting 与 scope-aware scan owner。

- `later-plan-gate.py` 的 real branch 将 `post_rc` 固定为 0，执行 child 后无论 `child_rc` 是否非零都返回
  `post_rc`；因此真实 evidence child 非零可表现为 wrapper exit 0。
- H2 只原子写入 raw child status、stdout/stderr 与 terminal audit；没有调用或移植 H1 strict validator 的
  status path/schema/range/symlink/hash fail-closed 校验。
- H2 real branch 没有执行 generated output、wrapper metadata、input provenance 三个 scope-aware scans。
- Final `31/31` 只有 child0 fake positive 与 30 个 pre-child reject，未覆盖 H2 candidate 的 child nonzero、post failure、
  status anomaly 或 banned-output/provenance negative；H1 `49/49` 仅回归旧 fake-only harness，不能证明新 real branch。

因此 H2 的 PLAN gate 设计可接受，但不足以安全激活唯一 future R2 offline invocation。H2 **判退**；不得创建授权 run
contract、不得执行 R2。

## 3. Exact next branch

发布 bounded `R2-H3-OFFLINE-TERMINAL-OWNER-CORRECTION`：在新的外置 root 中保留 H2 gate semantics，给 real-capable
candidate 接入独立 terminal validator/accounting owner，确保 child nonzero/unknown、wrapper/post failure 都使最终 wrapper
非零，并恢复 generated output、wrapper metadata、input provenance 三域严格扫描。使用 injected child 与 copied fake
PLAN/contract 覆盖正负矩阵；真实 production adapter invocation 保持 0，授权 artifact 保持 0。

H3 通过后仍必须再次由 Planner 独立验收，才可决定是否发布唯一 R2 offline invocation PLAN。

## 4. Suggested Orchestrator reference update

- H2 status → `rejected_REV-H2-001`；
- REF-P7-04 current action → R2-H3 offline terminal-owner correction；
- future R2 remains locked，budget `0/1`；
- all live/device/formal routes remain `PAUSED_BY_HUMAN_PRIORITY`。

维护性判断：缺口位于外置 H2 gate 的终态 owner 边界；应在同一外置 validator/accounting owner 内纠偏，不需修改
production 或设备路径。
