# P7-TD-B Z0-R2-C1R7 predecessor FIFO 验收归档

**归档时间：** 2026-07-25 17:47 MDT

**Reference task ID：** `REF-P7-01`

**Reviewed PLAN contract：** `P7-TD-B-Z0-R2-C1R7`

**Reviewed PLAN SHA-256：** `2ad06f269cee414fec0937260fa74bd7619a83a5ade6bc8b312a8acf13caae39`

**Planner decision：** `accepted_pre_driver_fifo15_signal_unknown20_and_seal; rejected_c1r6_predecessor_replay_root_scope; c1r8_required`

**Exact next branch：** `P7-TD-B-Z0-R2-C1R8`；只把 historical FIFO root identity 从冻结 C1R3 精确扩展为冻结 C1R3 与冻结 C1R6 两个 exact root，每个 root 仍绑定 exact path/type/mode/size/provenance；禁止 new root、generic/multi/glob/subtree 或其他 unsupported-type 接受。随后在 fresh root 执行一次完整 driver。

## Reviewed scope 与方法

C1R7 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r2-c1r7-offline/20260725T231258Z/`

Executor冻结 C1R6 review/source/evidence，新增 assigned-stage `attempted_result_unknown` writer、validator 与精确负例，完成 source、cases bootstrap、PLAN identity、historical FIFO 和 normalized seal pre-driver gates，再启动 driver 一次。Planner核对 EXECUTION_RESULT 第56节、validation/failure artifacts、driver日志、policy matrices、seal ledger、source identities及两个历史 FIFO 的当前 `lstat`；未运行任何 old driver/launcher，也未访问设备或网络。

## Evidence 与 accepted partial validation

- `historical-fifo-policy-matrix.json`：bytes `4667`，SHA-256 `e45a7564b07775927310656b6ad1bcefbfc37220f8ee96fc6f14e96b14cb1633`；冻结 C1R3-only policy `15/15`。
- `signal-unknown-accounting-matrix.json`：bytes `2861`，SHA-256 `eefc723e87f8b172645dfa6d5216d4e0bab3c801ce0221b30da676858c9b809c`；missing/tampered/ordering/PID/signal/exit/reap/residual/result/unknown multiplicity 与 misuse 负例 `20/20`。
- `seal-ast-delta-ledger.json`：bytes `1424`，SHA-256 `7ba008fc72e1f29269940ee43812e5336aef4769523c8bd09b62bee28e789a6b`；raw delta `4`、unclassified `0`，typed normalized baseline/current SHA 均为 `5945a83726f581d6291964a67df8f712f56fc6f15d3bdcc24c613fb926609185`。
- `cases-bootstrap.json`：SHA-256 `ee16962b74f0580bb237878c7de11dc3d5abab3564619d541c8b9b25593fbae7`；single empty regular `0755` parent bootstrap通过。
- `validation-summary.json`：SHA-256 `eeda60d72a5ea22e02e9ba912de3098b6e7c357e03371e468bcef42fcb4cf7fd`。
- `first-failure-audit.json`：SHA-256 `a6423c30469959d7f4b406b84a52bc7b0064b50ded8381fc876143a6864fdb26`。
- C1R7 harness：bytes `101971`，SHA-256 `4dcd6285affe933a5ce57c3fcbcd3b55cd8d70e0870561b878e022076a2f29bd`；wrapper、adapter、launcher SHA-256 分别为 `890caf867a4f5630c52bd59b8c7d078daf0f59cd75dfc7b32c79879fe93354e6`、`c2bc28683a1e789f1945164471f6693f48c79dd3c6dcdb1b7e36d1f0e37fc186`、`75c589929e08e00043591b683c128e86d30cc60f566caec4a2d5ec5472068dbc`。

两个冻结 FIFO 的 `lstat` 均为同一相对路径 `fixtures/evidence-tree/06-unsupported-fifo/tree/pipe`、ordinary non-symlink FIFO、mode `0644`、size `0`；C1R3 inode `1912145`，C1R6 inode `1912671`。C1R3 manifest provenance 已冻结为 `c1r3_evidence_tree_matrix_unsupported_fifo_negative_fixture`；C1R6 必须绑定其自身 frozen-root/evidence-tree-negative-fixture provenance，不能借 root-agnostic 或 C1R3 identity 通过。

driver stdout为空，SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`；stderr SHA-256 `9e5c4169c8bacc72732d8e5ae9dc47e57e7916308c6d790d520a236bfd8891bf`；launcher exact传播 exit `1`。fresh package/driver/rerun=`1/1/0`，owned residual process=`0`，全部已落盘 JSON strict parse通过。

## Finding、decision 与 residual risk

唯一首失败发生在 old-root before manifest 读取 C1R6 predecessor：C1R7要求把 C1R6 追加到 whole-tree replay，但冻结 historical owner只接受 exact C1R3 root。C1R6自身的 evidence-tree negative matrix保留了同路径 FIFO，因此两项合同无法同时满足。lifecycle、前五 required matrices、real adapter、old-root after/replay和terminal seal均未启动；四个 signal unknown artifacts尚未产生，不能视为signal实现已通过。

Planner接受精确 root 扩展，因为 C1R3/C1R6 均是已冻结、只读、具名 predecessor，路径/类型/mode/size/provenance可逐 root 固定，且读取策略仍只做 `lstat`，不打开、读取、hash、follow或修改 FIFO。C1R8不得把这解释为 generic unsupported acceptance，也不得接受当前 fresh root、第三个 root、任意 allowlist、glob、subtree、multi-entry、不同 path/type/mode/size/provenance。

signal accounting、cleanup、seal、wrapper/adapter/launcher 与科学合同未发生失败，但仍需唯一 fresh C1R8 完整 driver 才能验收。secrets、`.env`、credential、production import、hostname、network、device、camera、Ray、strip、Z0、lineage、E2、formal、public analyzer、Git均为 `0`。不需要 Advisor 科学纠偏；这是局部 historical replay policy 的机械合同修正。

## Exact next stop

C1R8任一 source/root identity、exact FIFO metadata/provenance、new/generic policy rejection、signal negative matrix、matrix、old-root replay、seal或zero budget失败即保留首次证据并停 Planner；全部通过也只停 Planner验收，不能自动进入真实 Z0。
