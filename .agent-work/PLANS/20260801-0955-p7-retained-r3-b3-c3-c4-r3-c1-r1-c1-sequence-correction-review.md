# P7 retained-R3 Option B：R3-C1-R1-C1 sequence correction 验收归档

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R3-C1-R1-C1`

**被验收 contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R3-C1-R1-C1-P3-FROZEN-SEQUENCE-CORRECTION-V1`

**Planner 决定：** `ACCEPTED_COMPLETE_SUBORDINATE_OWNER_ONLY_NO_ELIGIBILITY`

## 1. 冻结拓扑与范围

- activation：`20f6c0e59131e5fba8b8f7e8f23c0ae209ead063`；parent evidence `27424dd1feedb620d8b527c7aea4e8d27010dbed`；subject `chore(plan): correct P3 typed sequence boundary`；tree `936fc9a2954d9ab6f98f5e8f7a9bafc311417631`。
- implementation：`b23b358fd6322372587db6faa24e852bc38c3172`；parent exact activation；subject `fix(p7): align real manifest decoded sequences`；tree `e0b3931f4da507a071fd46e6123250839ce0a480`。
- implementation changed paths exact two：
  - `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py`；bytes/SHA-256 `f139b6e4071b7ec9f2658a4b60305894011c64764236b3f10610e7effc04ecd9`。
  - `tests/test_p7_retained_r3_real_manifest_self_check.py`；bytes/SHA-256 `361a5c268aff07d0b50c8788a4eb8bc8af5b311e5c263697fad3f2a34d404508`。
- evidence：`36ea02ad1993c34e119c6bb80e5a841c2e77b205`；parent exact implementation；subject `chore(evidence): record P3 sequence correction`；tree `f6d1af07f3aa98e3c44ad02a7fca7719f8cbe9a0`；changed path exact `.agent-work/EXECUTION_RESULT.md`。
- evidence append 是 physical EOF append：parent blob `d38db436786342558f565f6f2056056d1e4d09b3` / bytes `1399960` / SHA-256 `cd3974db2939e8638eb663d4e4f56ddddb877ade0c7b0e80f3fa225dc696eba5`；child blob `03e8ff2960768390f9903540b6426ba2c74b666f` / bytes `1404105` / SHA-256 `169716925b35283bb13e65cc59f8ca4ec5cd4c3d6a8e359adeceed70eb0d7142`；append bytes `4145`，SHA-256 `f4e7199b62c0f6f5d6d798f4df3960a21bd4397bf29f7768d129206aa2fb3256`。

## 2. 验证质量

- targeted：`12/12`；focused：`53/53`；full suite：`822/822`；post-commit targeted：`12/12`。
- exact-two compileall、CodeGraph sync/post-query、`git diff --check`、exact path/status、commit topology均通过。
- retry/fallback `0`；real/C1/retained/external artifact reads、validator、eligibility、release consumption、network、device、camera、Ray、strip、formal、public analyzer均 `0`。
- Planner 独立静态验收确认 six public exports保持；tuple/list仅在JSON sequence边界语义等价，mapping key set/order递归比较仍严格，scalar concrete type仍严格，因此`1 != true`。
- decoded report在re-encode前显式re-native；五artifact identity、root/path/inode/hash/bytes、C1/retained label order、commit/path collision、seam bytes/OID、18条ordered Git ledger、diff-tree order、full ledger facts与no-authority边界保持。
- dedicated negatives现到达各自owner：bytes drift保留tuple；seam OID与key collision直接由`required_real_manifest_git_argv`拒绝，不再被无关manifest前置条件遮蔽。
- source未新增filesystem persistence、process runner、validator、eligibility或release authority。

## 3. Planner findings 与决定

先前唯一阻断项是P3 frozen tuple与JSON-native list表示边界导致golden无法到达科学/身份验证路径。`b23b358`在exact-two范围内修复该adapter边界，并保持typed spec、artifact identity、Git ledger与authority boundaries。Planner未发现新的correctness、scope、证据或维护性阻断项，因此接受本包完成。

本接受只关闭subordinate real-self-check owner实现纠偏，不构成真实retained-R3审计、不发出canonical eligibility、不使release可消费。现有canonical lineage validator继续是唯一eligibility owner。

## 4. 残余风险与下一分支

- real manifest、C1与retained-R3三组物理artifact尚未由新owner进行独立真实读取；因此B3 credit、release consumption及所有设备阶段继续锁定。
- 下一分支只解锁`REF-P7-25-R2-B3-C3-C4-R4`：生成一个不可变、纯离线、非执行的real-self-check preparation package，冻结exact roots/artifacts、owner commit、未来18条Git acquisition和R5 stop/failure contract。
- R4不得读取任何real/C1/retained物理artifact，不得运行self-check owner或canonical validator，不得发eligibility。它只为后续R5真实离线审计提供sealed execution spec。
- 网络、设备、camera、Ray、strip、formal、public analyzer与release consumption保持0；无需Human设备授权或Advisor科学决策。

维护性判断：修复仍集中于单一wire-representation comparator及其dedicated tests，没有引入平行owner或权限面；下一包继续把执行配置与真实审计分离，降低一次性controller歧义。
