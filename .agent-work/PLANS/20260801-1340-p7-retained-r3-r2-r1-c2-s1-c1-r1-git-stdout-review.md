# P7 retained-R3 Option B：R2-R1-C2-S1-C1-R1 real self-check Git stdout mismatch 验收归档

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-RAW-BYTES-ACTIVATION-GATE-AND-COLLISION-FIXTURE-CORRECTION-AND-REAL-SELF-CHECK-V1`

**Implementation：** `a80c26ffceb223726e241bae244c10133f6fbbdf`

**Evidence：** `c7792cbc7cfe9730b295885bead9e5f726f6136d`

**Planner 决定：** `IMPLEMENTATION_ACCEPTED_REAL_SELF_CHECK_REJECTED_GIT_STDOUT_MISMATCH`

## 1. Reviewed scope 与 topology

Planner完整读取AGENTS、project skill、committed PLAN、FULL machine state及当前任务条目、被归档PLAN、implementation diff和ER physical EOF section，并只读核验本轮fresh root四件套。未读取旧failed/synthetic roots，未运行owner、tests、validator、release或设备操作。

Activation `a9c85923e9e54d59a75857ed7c4802807ebea844`是evidence `c52fd8753f84802da1829dd5c90e1061d71ee9cc`的direct child，subject exact `chore(plan): pass raw bytes to machine row parser`，changed paths exact FULL、PLAN与`.agent-work/PLANS/20260801-1325-p7-retained-r3-r2-r1-c2-s1-c1-parser-input-review.md`。Implementation `a80c26f`是activation direct child；evidence `c7792cb`是implementation direct child且changed path exact `.agent-work/EXECUTION_RESULT.md`。Review时HEAD为evidence且worktree clean。

ER最后完整level-2 section为`R2-R1-C2-S1-C1-R1 raw-bytes corrected real self-check physical EOF handoff`；从该heading至physical EOF为bytes `6348`、SHA-256 `c344e32d21554df62d399d7d916b33909e7d616886fe7dcd344d6366795ef41f`，closing fence后以LF结束。

## 2. Accepted implementation 与 validation credit

Raw Git stdout bytes直接进入accepted repo-owned PLAN/FULL parsers；PLAN/FULL各调用一次，archive由`Path.read_bytes()`取得。Gate记录text decode、text mode、`read_text`与手写parser均为0，FULL required subset通过。该raw-bytes acquisition gate接受。

冻结的一行dedicated negative fixture修正接受：只将`release_checkpoint=spec.activation.parent,`替换为`helper_v1=spec.activation.parent,`；production source保持原已实现bytes不变，assertion与precedence未改。Implementation commit：

- parent `a9c85923e9e54d59a75857ed7c4802807ebea844`；subject exact `fix(p7): correct real manifest seam commits`；changed paths exact production owner与dedicated test。
- source bytes/SHA-256/blob为`25094` / `a14c947322219b198e98c94f0063cbc8018fe6568bee8593253d6a1013bcab1a` / `ccecfde60f96c9b54464df19fc18d1cb60de5973`。
- test bytes/SHA-256/blob为`25814` / `7237b0407f4836e2e013e43c0a583bb2bc326b214bf779100cc7c44bebae7c3e` / `b40a8438e6f5e69a0e4ef931156cbb38704d2af8`。
- targeted `12/12`、focused `53/53`、full unittest discover exit `0`、compileall、CodeGraph sync/post-query、diff check、exact-two status及postcommit targeted `12/12`均按冻结顺序一次通过。

因此raw-bytes gate、fixture correction、implementation与全部验证获得信用；不得回退、amend或重做该implementation。

## 3. Fresh real self-check rejection 与 terminal seal

Fresh source为`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-real-self-check-r2-r1-c2-s1-c1-r1-a80c26ffceb2-source.py`；fresh root为同basename去除`-source.py`。Root inventory exact四件套，root mode `0700`，所有文件mode `0600`：

- `00-execution-contract.json`：bytes `668`，SHA-256 `030873fc588974e6de57d735bb4f2355bbcc8a4affbf1829c00a25472463cc3f`；seal逐字绑定该target/bytes/hash。
- `99-terminal-summary.json`：bytes `880`，SHA-256 `714533a9a90c2b1f2ccf3c63357daedc7f552a05ec8d02faf40a63fc6ee3f361`；seal逐字绑定该target/bytes/hash。
- 四件套均为strict JSON；terminal status为`failed_sealed_subordinate_provenance_evidence`，`passed=false`，primary failure exact `RealManifestSelfCheckError(code="git_stdout_mismatch")`。
- Terminal counters封存physical input reads `14`、Git file acquisition processes `8`、required argv checks `1`、self-check owner calls `1`、owner ledgers `0`、retry/fallback `0`。Authority仍为`subordinate_self_check_only`，eligibility与release consumable均false。

该failure发生在owner内部Git stdout校验且success report未生成；不能从`owner_git_ledgers=0`判断是哪一个stdout，也不能给real self-check、manifest truth、eligibility或release信用。Fresh root必须immutable保留，不得重试、修复、重建或复用。

## 4. Exact next branch

唯一successor为`REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1`。它是bounded attribution diagnostic，不是owner retry：使用全新activation-derived source/root，按原controller acquisition order精确运行8次literal Git file acquisition，并为每次封存role、exact argv、expected byte count/SHA-256/blob、actual exit code、stdout bytes/SHA-256、stderr bytes/SHA-256及全部match booleans。重复的activation与baseline seam acquisitions必须作为8个独立有序事实保留，不能set-collapse、缓存或省略。

Diagnostic不得调用`required_real_manifest_git_argv`或`run_real_manifest_self_check`，不得读取任何旧root/source、14个real physical inputs或retained R3 payload，不得更改production/test，不得放宽owner校验。它只回答8个acquisition是否逐项返回冻结bytes，并根据首个mismatch给出下一工程分支；owner retry与real self-check successor必须等待该diagnostic另行验收。

Canonical validator、eligibility emission、release consumption/copy/generation/qualification、network、device、camera、Ray、strip、cleanup、formal与public analyzer保持0。无需Advisor科学决策或Human设备授权。

**Planner stop：** `B3_C3_C4_R5_R1_C1_R2_R1_C2_S1_C1_R1_D1_GIT_STDOUT_ATTRIBUTION_WAITING_PLANNER_REVIEW`。

维护性判断：accepted production owner与dedicated test边界不变；successor是一次性只读Git attribution evidence，不新增production abstraction或第二eligibility owner。
