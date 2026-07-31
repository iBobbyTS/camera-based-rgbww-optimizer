# REF-P7-25-R2-B2-P3-C2 observable full validation pipeline review

**Review date:** `2026-07-30`

**Reviewed reference task:** `REF-P7-25-R2-B2-P3-C2`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-PROVENANCE-IO-OBSERVABLE-FULL-VALIDATION-V1`

**Planner decision:**
`REJECTED_PLAN_PIPELINE_ZSH_STATUS_READONLY_CHILD_RESULT_UNPROVEN`

**Reviewed PLAN identity:** bytes `8201`, SHA-256
`607f0115876dbda21c6241130b05795cd28027fa116314eb54aed923ae6d8f22`.

**Reviewed stop:** `B2_P3_C2_OBSERVABLE_FULL_VALIDATION_WAITING_PLANNER_REVIEW`.

## 1. Reviewed scope and method

本次独立审核覆盖 P3-C2 activation、冻结 implementation/file/patch/archive identities、active PLAN exact pipeline、
Executer handoff、当前 Git topology/worktree，以及 FULL 中的 active/retained/real-B2 locks。审核目标仅是判断一次
observable full validation 是否满足 PLAN acceptance contract；不重新评估已在 P3-C1 关闭的
`REV-P3-001/002/003` code findings。

Planner 直接读取当前 Git objects、PLAN、FULL、P3-C1 archive 和 ER handoff，独立重算 implementation 两文件
bytes/SHA/blob 与 canonical binary patch SHA。没有运行 unittest、collection/count probe、compileall、CodeGraph
sync 或任何纠正命令；没有读取 `/Volumes/4T/temp/rgbww-optimizer` 下的 C1、retained-R3、release 或旧 run
evidence，也没有访问 network、`.env`、设备、camera、Ray、strip、cleanup、FORMAL 或 public analyzer。

## 2. Independently reconstructed identities

Activation topology exact：

- activation `4725c6545e414c55ef7e9bf86fe1381782035039`；
- direct parent `c0e20d1afe9e363f646fc5723be721d3b907deeb`；
- subject `chore(plan): activate retained r3 observable full validation`；
- exact paths为 `.agent-work/FULL_PLAN_REFERENCE.md`、`.agent-work/PLAN.md` 和
  `.agent-work/PLANS/20260730-2148-p7-retained-r3-provenance-io-p3-c1-review.md`。

Implementation topology exact：

- commit `1f88cf42d95c00c7db5692e78ed1d663732d5701`；
- direct parent `a736e95b968ffef813024a67c0cbcfbd67e971e4`；
- subject `fix(p7): harden retained r3 provenance io boundary`；
- exact changed paths仅
  `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py`和
  `tests/test_p7_retained_r3_provenance_io.py`；
- canonical binary patch SHA-256
  `df29a921b774010db020fdebfc12809feb2c92c293c247b14733a6e39e8595e1`。

Post identities independently match the handoff：

| Path | Bytes | Blob OID | SHA-256 |
| --- | ---: | --- | --- |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py` | `18853` | `492f31f5f6999e28a1f0eb60240780e2c4826f4f` | `f603721fb8b90510e2a09b199701c3f3358574d1247b5883ebdccc6f585b0a48` |
| `tests/test_p7_retained_r3_provenance_io.py` | `28525` | `a796e1ac336d58a0120dd6b99a3842c5c7b03a6b` | `59a6d87164abf6abc89c50ab7d899f94126fc949512d38b34967cae8f4e6d4e9` |

P3-C1 archive independently matches bytes `7898` and SHA-256
`ddb8167ef108d1043cadce621873b560874214da891f515ee2e9d96dbe3223a8`。Evidence handoff commit
`05495ae6e07a8b3ae3a2a2bc899590dbcb68a119` is a direct child of activation and changes only
`.agent-work/EXECUTION_RESULT.md`。Review-start worktree/stage/untracked sets were clean。

## 3. Pipeline-contract finding

The exact authorized pipeline assigned the unittest return code to `status`：

```zsh
set -o pipefail
{
  .venv/bin/python -m unittest discover -s tests -p 'test_*.py'
  status=$?
  print -r -- "__P3_C2_FULL_EXIT__=${status}"
  exit "${status}"
} 2>&1 | tail -n 40
```

In zsh, `status` is a read-only special parameter. The retained terminal ends with exact diagnostic
`zsh:4: read-only variable: status`；the assignment fails before the marker-producing `print` and explicit group
`exit` can execute。This is a defect in the Planner-authored pipeline contract, not evidence that unittest failed。

The unique unittest child was invoked once, but its return value was never copied into an observable ordinary variable。
The structured pipeline/shell exit `1` proves the zsh contract failed；it does **not** prove the unittest child exit was
`1`。Conversely, absence of a retained unittest failure does **not** prove child exit `0`。The tail has no
`__P3_C2_FULL_EXIT__=<n>` marker, no `Ran 741 tests in ...s`, and no subsequent `OK`。Therefore the child result and
full-suite acceptance remain unproven。

The merged stream also retained late test stdout ahead of the zsh diagnostic while omitting the unittest terminal summary。
The next package must make child stdout unbuffered before invoking unittest so that the low-output terminal tail can retain
the final summary in natural order；it may not infer or reconstruct the missing P3-C2 summary from arithmetic、Git state or
a second reader。

## 4. Validation evidence quality

Accepted P3-C1 evidence remains reusable and was not rerun：targeted `24/24`、focused `71/71`、compileall exit `0`、
CodeGraph sync exit `0`、pre/post scope/diff/commit checks and postcommit targeted `24/24` final `OK`。Current frozen
identities do not contradict those results。

P3-C2 evidence quality is sufficient to prove only：

- frozen preflight passed；
- exact PLAN pipeline and unique unittest invocation count were `1`；
- retry/fallback/alternate invocation/count probe were `0`；
- zsh failed at the read-only `status` assignment；
- shell/pipeline structured exit was `1`；
- source/test/PLAN/FULL/archive/stage/commit writes remained `0` during execution；
- all external/retained/release/network/device/scientific zero budgets remained `0`。

It is insufficient to prove unittest pass、failure、test count or terminal status。No subprocess outcome may be inferred from the
outer zsh failure。

## 5. Decision and exact next branch

Decision：
`REJECTED_PLAN_PIPELINE_ZSH_STATUS_READONLY_CHILD_RESULT_UNPROVEN`。

Exact next branch：`REF-P7-25-R2-B2-P3-C2-C1`，contract
`P7-TD-B-RETAINED-R3-PROVENANCE-IO-OBSERVABLE-FULL-VALIDATION-V2`。

The corrective package is limited to one corrected observable full validation. It must preserve every implementation/file/
patch identity，use an ordinary non-special zsh variable，make the Python child stdout unbuffered，and retain in one
same-session tail the real child exit marker、exact `Ran 741 tests in ...s` and subsequent `OK` or truthful failure output。
It may not edit code/tests，rerun accepted gates，read external retained evidence，run real B2，or touch validator、eligibility、
release、network、device or scientific routes。

## 6. Residual risks and exact transition

- The unique P3-C2 unittest process consumed its authorization but produced no acceptable outcome evidence；it must never be
  reinterpreted as pass or fail。
- The corrected one-shot full suite may reveal a real regression；any nonzero child exit、missing marker、missing/count-mismatched
  summary、missing `OK` or new shell-contract defect must fail closed without retry or repair。
- retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`；this review does not validate、qualify or consume it。
- real B2/B3/B4、canonical validator、eligibility、release operation、network、`.env`、device、camera、Ray、strip、cleanup、
  FORMAL、public analyzer、TD-C、sentinel、P8、firmware and deployment remain hard locked at zero。
- This is an engineering validation correction；Advisor scientific guidance and Human high-risk authorization are not needed。

**Proposed FULL transition:** mark `REF-P7-25-R2-B2-P3-C2` as
`REJECTED_PLAN_PIPELINE_ZSH_STATUS_READONLY_CHILD_RESULT_UNPROVEN`，add
`REF-P7-25-R2-B2-P3-C2-C1` as the sole `ACTIVE_EXECUTION_AUTHORIZED` task after Orchestrator review/activation，and keep
`REF-P7-25-R2-B2-R2` rejected/locked until C2-C1 independently passes and is Planner-accepted。

**Exact stop:** `B2_P3_C2_REJECTED_WAITING_ORCHESTRATOR_C2_C1_ACTIVATION`。

## 维护性判断

The defect is isolated to the PLAN shell observability contract；implementation and test ownership remain unchanged。The next
package adds no code、helper or artifact owner，so no maintainability refactor is indicated。
