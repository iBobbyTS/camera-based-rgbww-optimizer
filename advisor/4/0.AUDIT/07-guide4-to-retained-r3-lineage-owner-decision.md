# GUIDE 4 执行增量与 retained R3 lineage-owner 决策请求

## 1. 本文件范围

本文追加 `advisor/4/4.GUIDE.md` 下发后、截至 2026-07-28 的执行结果和当前唯一 Advisor 决策门。
它不重写 `04` 至 `06` 对 FORMAL-R5 的历史报告，也不修改 GUIDE。

```text
applicable GUIDE SHA-256 =
  659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35
current code HEAD =
  9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
release checkpoint =
  32b9e670ff3bbea0cd1505528c2ca87c2935446c
retained R3 status = RETAINED_UNVALIDATED_UNCONSUMED
active executable task count = 0
```

## 2. GUIDE 4 后已经完成的工作

### 2.1 EQ-R6 与 state-C policy

- Human 确认 EQ-R6：先 `1/2500`，仅 clipping-only 失败时使用 `1/3200`，最大 8 CR3、retry 0。
- 网络恢复后，EQ-R6 在 `1/2500` 完成并被 Planner 接受；`1/3200` fallback 未进入。
- selected state-C shutter 固定为 `1/2500`。
- post-EQ policy 与 exact lineage classification 已实现、验证并提交：
  - `161094f feat(p7): finalize eq-r6 state-c exposure policy`
  - `cc6dbd3 fix(p7): classify accepted post-eq lineage paths`
  - `32b9e67 test(p7): bind post-eq checkpoint drift injection`

这些结果不等于 R6 formal 或 strip 阶段完成；后续仍按 PLAN/lineage 门控制。

### 2.2 successor R3 release

唯一 successor R3 artifacts 已在 release checkpoint `32b9e67` 生成并保留：

```text
current-lineage-candidate.json
  SHA-256 = 3a2ff5a2af200c55c925b954488c5c5dd31a35a481440d17dfcdd8b68419f2e0
resolved-formal-plan.json
  SHA-256 = cf7c78b6a6cfda4055d05f5e9bbe9914161213b380dc7736ee09e257dd45eb6b
setup-lineage-release.json
  SHA-256 = 0bacf1878a97fcdc4436259e132e89f6e56611df6d7fb5d5a7da28f62c98ad3e
```

生成后的外置 evidence controller 连续暴露 parent/root、writer import 和错误 binding predicate 等
生命周期问题。第三次同边界失败后，Orchestrator 按 second-pass 阈值选择 Option A：建立 repository-owned
retained-release audit helper，停止继续堆叠外置 controller。

### 2.3 repository-owned audit helper

Helper prerequisite 已完成并被 Planner 接受：

```text
commit = 9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
subject = fix(p7): validate retained release terminal counts
exact paths =
  src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py
  tests/test_p7_retained_release_audit.py
durable full suite = 661/661 OK
postcommit focused = 20/20 OK
synthetic owner/terminal/replay = pass
```

首次真实 retained-R3 audit 随后证明 helper 的 schema boundary 只接受 synthetic shape；真实三 artifacts
符合现有 public candidate/release/resolved contracts，却在 public validator callback 之前被 helper 拒绝。

纯离线 Branch-A 纠偏已形成两文件未提交 diff：

```text
src/.../p7_retained_release_audit.py
  SHA-256 = 48c0c57fb95c08205c3fef7b23e6df3729928352cd23e1722e8693b9f3634cf8
  numstat = +186/-33
tests/test_p7_retained_release_audit.py
  SHA-256 = c8d6c7c99815d823871ecfddce79eadd5d5def918affbcd7e4ce86de691d1b3f
  numstat = +159/-0
focused = 21/21 pass
```

这两份 diff 当前保持 unstaged、未接受；不得在 Advisor 选择 lineage owner 前提交、丢弃或继续修改。

## 3. 当前阻塞的精确事实

Lineage gate 的旧 test oracle 期望 setup→checkpoint changed paths 为 `59`，当前得到 `61`。独立 ancestry、
Git path set、CodeGraph 和最窄 raw-source evidence 证明：

```text
setup checkpoint = 9c804abdeabbc5da18a66d0acf25a1f13128bc2d
release checkpoint = 32b9e670ff3bbea0cd1505528c2ca87c2935446c
helper commit = 9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
setup -> release changed paths = 59
setup -> helper changed paths = 61
exact +2 paths = helper module + dedicated helper test
```

两个新增路径均不属于现有六个 owner：

1. `TD_B_LINEAGE_ALLOWED_PRODUCTION_PATHS`
2. `TD_B_LINEAGE_ALLOWED_VALIDATION_PATHS`
3. `TD_B_PUBLIC_DEFAULT_SUCCESSOR_CLASSIFICATIONS`
4. `TD_B_WORKFLOW_PATH_CLASSIFICATIONS`
5. `TD_B_CLEANUP_TEST_PROVENANCE_CLASSIFICATIONS`
6. `TD_B_POST_EQ_POLICY_CLASSIFICATIONS`

因此它们都会落入 `prohibited_or_unreviewed`；candidate `eligible=false`。只把 test literal 从 `59`
改成 `61` 仍不能使 candidate eligible，也会掩盖真正的 provenance-owner 缺口。

Canonical decision evidence：

```text
path =
  /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-retained-release-lineage-owner-o3-c1r3/20260728T0121/
  lineage-owner-decision-evidence.json
bytes = 7066
SHA-256 = 842cfad090549ebf6379df4551bd4f051267e4bf93014f899c5e329c57085620
status = advisor_decision_required
```

Evidence 还证明：six-owner absence、`prohibited_or_unreviewed`、count-only fix 仍 ineligible、source/retained
payload未再读取，并且 qualification、generation、repair、copy、consume、设备、网络和 formal 计数全部为 0。

## 4. 请求 Advisor 明确选择

### Option A — 现有 lineage policy 中增加 exact classification

Advisor 必须明确：

- authoritative owner/map；
- classification category 与 provenance 语义；
- 是否只绑定 exact commit `9303aa2`；
- 是否同时绑定 parent、exact path set 与 blob/diff hashes。

风险：generic path-only allowlist 会把未来无关 revision 一并授权，混淆 production/test provenance。

### Option B — exact provenance-manifest owner

为 helper commit 建立 commit-bound exact manifest owner，并明确 manifest/validator owner、commit、parent、
paths、blob/diff hashes、scope 与 rollback provenance。

风险：若没有唯一 consumption boundary，会形成第二套平行 owner 和长期维护负担；优点是不会永久放宽路径。

### Option C — 拒绝 helper commit 并重生成/重构

拒绝 `9303aa2` 作为 release-lineage successor，并说明当前两文件未提交 diff 的 disposition，以及新的 prerequisite
checkpoint/release 路线。

风险：避免扩大现有 policy，但会丢弃或重做已经验证的 helper 工作，并可能需要从新 checkpoint 重建 evidence。

Advisor 可以提出其他路线，但必须解决同一 exact commit/path provenance ownership，并明确为何 A/B/C 不适用。

## 5. 当前硬锁

在 Advisor 决策到达前：

```text
Planner/Executer dispatch = 0
repository edit/test/commit = 0
helper/public validator/consumer/replay = 0
retained R3 audit/validation/consumption = 0
qualification/release generation/retry/repair/copy = 0
network/device/camera/Ray/strip/formal/public analyzer = 0
```

本次审计追加由 Orchestrator 直接完成，没有经过 Planner→Executer→Planner 流程；未修改 GUIDE、PLAN、
FULL reference、实现或测试，也没有访问设备、网络、`.env`、相机或灯光。
