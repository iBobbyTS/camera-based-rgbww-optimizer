# REF-P7-25-R2-B1A / Pre-acquisition lifecycle hard-failure review

**Planner 日期：** 2026-07-29

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-CANONICAL-SEAM-INTEGRATION-V1`

**Decision：**
`ACCEPTED_HARD_FAILURE_REJECTED_FOR_IMPLEMENTATION_ADVANCEMENT`

## 1. Reviewed scope

本次只读验收 active B1A package 的 terminal failure、progressive evidence、clean-room state、共享 worktree边界与
zero counters。Reviewed PLAN SHA-256：
`54b51928ae2b88d28bc2ec8be16899ba9f49bd1392822de10545bf4d95735580`。

失败 evidence root：

```text
/Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-retained-r3-option-b-b1a-offline/20260729T164106Z
```

Canonical handoff hashes：

```text
11-validation-summary.json =
  22f6afe6f328d887e9949c9f0b7fbf9f21a164f9ff1f0b364736631d3f634046
12-terminal-summary.json =
  0096ad605c612c2855ff87fd55c52656fbd28a6d21534b624ba14ca02a1195c1
.agent-work/EXECUTION_RESULT.md after append =
  20ddd80e4fddb88c4ee36506a0acb7cd37d53ef533e991a20e75cf23fe933b79
```

## 2. Independent replay

Planner 独立确认：

- terminal summary bytes `5328`、mode `0600`、nlink `1`，SHA exact；
- validation summary bytes `1246`、mode `0600`、nlink `1`，SHA exact；
- top-level JSON `13/13` 通过 duplicate-key/non-finite rejecting strict parse；
- terminal 绑定的 preceding artifacts `14/14` 逐项 path/name/bytes/mode/nlink/SHA匹配；top-level file set恰为
  14 preceding files + terminal；
- clean-room actual path为 `<failure-root>/cleanroom`，HEAD=
  `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`，status clean，staged paths `0`；
- shared HEAD仍为 `9303aa2`，shared staged paths `0`，PLAN/FULL在 execution期间未被 Executer修改；
- output root与clean-room实际mode均为 `0755`，truthfully retained，没有failure后normalize；
- original retained R3仍为 `RETAINED_UNVALIDATED_UNCONSUMED`。

## 3. Root cause and acceptance quality

Pre-acquisition owner先对预期尚未存在的 fixed container
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-offline`调用`lstat`，得到
`FileNotFoundError`，failure phase=`pre_acquisition_parent_lstat`。该异常发生在冻结 machine gate、shared-before
snapshot与source hashes持久化之前。

外层 compound shell 未 fail fast，异常之后仍继续执行 local clone 与 detached checkout：

```text
clone_calls = 1
checkout_calls = 1
status = noncompliant_acquired_after_preflight_failure
root_lifecycle_noncompliant = true
```

因此该 run 不是 compliant acquisition，且没有 pre/post dirty-manifest equality proof。Planner接受其诚实、完整的 hard
failure和terminal seal，但拒绝将其视为实现进展或 B1A pass。

## 4. Preserved zero facts

下列计数均为 `0`：CodeGraph/source reads、helper/test materialization、implementation edits、compileall、focused/full tests、
CodeGraph sync、stage、commit、manifest write/rewrite、canonical verifier、retained metadata/content/semantic reads、helper
real audit、eligibility、consumer、replay、qualification、release generation/retry/repair/copy/consumption、network、DNS、
`.env`、device、camera、Ray、strip、cleanup、capture、public analyzer、FORMAL、firmware、deployment。

失败 root及其 clean-room必须 immutable retained；不得same-root repair、delete、normalize、retry或复用。

## 5. Residual risk and exact next branch

剩余问题仅是 execution lifecycle owner，而不是 scientific、provenance schema或 five-path implementation contract。
下一分支为`REF-P7-25-R2-B1A-C1`：一个全新 root、单一 Python fail-fast acquisition owner、显式 phase barrier；
只对 fixed container执行 ensure-dir/lstat，不对未创建 timestamp root做 lstat；exclusive mkdir并验证 timestamp root后才可
clone。任一 pre-clone failure必须证明 clone/checkout=`0/0`。

其余 exact five-path、ownership、tests、single commit、manifest seal、original R3 three-read和zero device/network/formal
合同不变。C1的`retry=0`是新 corrective package内部预算，不是复用或重试本失败root。

无 Advisor blocker，无 Human authorization blocker。此归档不授权执行；唯一执行授权来自随后重写的 active PLAN。

