# REF-P7-25-R2-B2-P3-C2：provenance I/O observable full validation

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-P3-C2`

**Parent reference task：** `REF-P7-25-R2-B2-P3-C1`

**Contract ID：** `P7-TD-B-RETAINED-R3-PROVENANCE-IO-OBSERVABLE-FULL-VALIDATION-V1`

**当前唯一动作：** Orchestrator独立审核、同步FULL并激活后，Executer只运行一次低输出且保留真实exit与完整
`Ran 741 tests ...`/`OK`终态的full suite；不得编辑、重跑任何已接受gate、提交或进入real B2。

**预计时长：** `<10 minutes`；不使用visible Terminal、automation或后台长任务流程。

**唯一执行 stop：** `B2_P3_C2_OBSERVABLE_FULL_VALIDATION_WAITING_PLANNER_REVIEW`。

**本次P3-C1 review archive：**
`.agent-work/PLANS/20260730-2148-p7-retained-r3-provenance-io-p3-c1-review.md`，
bytes `7898`，SHA-256
`ddb8167ef108d1043cadce621873b560874214da891f515ee2e9d96dbe3223a8`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_provenance_io_observable_full_validation_plan_v1","reference_task_id":"REF-P7-25-R2-B2-P3-C2","parent_reference_task_id":"REF-P7-25-R2-B2-P3-C1","contract_id":"P7-TD-B-RETAINED-R3-PROVENANCE-IO-OBSERVABLE-FULL-VALIDATION-V1","execution_authorized":true,"activation_required":true,"activation_commit":{"expected_parent":"c0e20d1afe9e363f646fc5723be721d3b907deeb","expected_subject":"chore(plan): activate retained r3 observable full validation","exact_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260730-2148-p7-retained-r3-provenance-io-p3-c1-review.md"]},"frozen_implementation_commit":"1f88cf42d95c00c7db5692e78ed1d663732d5701","validation":{"quiet_full":1,"retry":0,"fallback":0,"targeted":0,"focused":0,"compileall":0,"codegraph_sync":0,"postcommit_targeted":0},"writes":{"source":0,"test":0,"plan":0,"full":0,"archive":0,"stage":0,"commit":0},"zero_budgets":{"external_evidence_reads":0,"external_root_creation":0,"retained_release_audit":0,"canonical_validator":0,"eligibility":0,"release_operation":0,"network":0,"environment":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"planner_stop":"B2_P3_C2_OBSERVABLE_FULL_VALIDATION_WAITING_PLANNER_REVIEW"}`

## 1. Activation与frozen preflight

Executer不得在Orchestrator activation前执行。Activation commit必须满足machine contract的exact parent、subject和
exact three-path topology；激活后的FULL必须有exact一个active task/contract为本包，并继续声明：

- `retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`；
- P3-C1 implementation findings closed but acceptance blocked only by full terminal evidence；
- P3-C2 active；
- real B2/B3/B4、validator、eligibility和release consumption locked。

执行前只读证明：

1. HEAD为activation commit且worktree/stage clean；
2. implementation commit仍为`1f88cf42d95c00c7db5692e78ed1d663732d5701`，direct parent
   `a736e95b968ffef813024a67c0cbcfbd67e971e4`，subject exact
   `fix(p7): harden retained r3 provenance io boundary`，exact two-path topology；
3. current HEAD tree中的两个frozen files仍exact：
   - helper bytes `18853`、SHA-256
     `f603721fb8b90510e2a09b199701c3f3358574d1247b5883ebdccc6f585b0a48`、blob
     `492f31f5f6999e28a1f0eb60240780e2c4826f4f`；
   - test bytes `28525`、SHA-256
     `59a6d87164abf6abc89c50ab7d899f94126fc949512d38b34967cae8f4e6d4e9`、blob
     `a796e1ac336d58a0120dd6b99a3842c5c7b03a6b`；
4. canonical exact-two-path binary patch SHA-256仍为
   `df29a921b774010db020fdebfc12809feb2c92c293c247b14733a6e39e8595e1`；
5. P3-C1 archive bytes/hash与本PLAN header一致。

任一不符即preflight hard failure：full invocation为0，只向ER追加真实handoff并stop。不得repair、retry、rebase、
checkout、reset、stage或接管ambient work。

本包可读取repo source、tests、Git object database、PLAN/FULL/archive/ER。禁止读取
`/Volumes/4T/temp/rgbww-optimizer`中的C1、retained-R3、release或旧run artifact；full tests自己按既有
tearDown管理的disposable test directories不算external evidence read/root。

## 2. Accepted evidence that must not be rerun

Planner已接受P3-C1的以下one-shot evidence，Executer必须复用而不得重新调用：

- targeted `24/24`；
- focused `71/71`；
- compileall exit `0`；
- CodeGraph sync exit `0`，`Already up to date`；
- pre/post scope、diff、stage和commit topology checks；
- postcommit targeted `24/24`，final `OK`；
- REV-P3-001、REV-P3-002和REV-P3-003的code/test closure。

不得运行targeted、focused、compileall、`codegraph sync`、postcommit targeted、第二种test command、collection
probe或dry-run。不得编辑source/test以改变count或输出。

## 3. 唯一quiet full invocation与observable terminal contract

Preflight通过后，运行exact一次以下zsh pipeline，保持一个shell/session owner，避免把大段中间输出交给transport，
同时在同一terminal tail中保留unittest summary和真实child exit marker：

```zsh
set -o pipefail
{
  .venv/bin/python -m unittest discover -s tests -p 'test_*.py'
  status=$?
  print -r -- "__P3_C2_FULL_EXIT__=${status}"
  exit "${status}"
} 2>&1 | tail -n 40
```

这段pipeline中的unittest process是本包唯一validation invocation。不得用`tee`、文件重定向、第二个reader、
新log/evidence root、detached process、background owner或外部wrapper。Executer必须保留该same session的：

- structured shell terminal exit；
- exact一行`__P3_C2_FULL_EXIT__=<n>`；
- unittest terminal `Ran 741 tests in ...s`；
- summary后的`OK`，或任何真实failure/error output。

Pass仅当：structured shell exit `0`、marker exact `0`、exact一条`Ran 741 tests in ...s`且其后final `OK`，并且
没有`FAILED`、`ERROR`、traceback、broken pipe、missing/truncated marker或count mismatch。

任一其他结果均hard failure。禁止retry、fallback、增大tail后重跑、另跑collection/count、用算术推导替代terminal、
修复测试、运行narrow suite或继续后续任务。只向ER记录真实输出、exit、缺口和计数后stop。

## 4. Handoff与acceptance evidence

无论pass/fail，Executer都只向`.agent-work/EXECUTION_RESULT.md`追加一个P3-C2 handoff；不得修改PLAN、FULL或
archive，不得stage/commit ER。Handoff至少记录：

- activation、implementation、two-file、patch和archive preflight identities；
- exact pipeline text、shell/session owner、unittest invocation count；
- structured shell exit、marker、完整retained tail、`Ran` count/time、final status；
- source/test/stage/commit写入计数全部0；
- targeted/focused/compileall/CodeGraph/postcommit rerun计数全部0；
- retry/fallback全部0；
- 所有machine-contract zero budgets及retained/real-B2 locked state。

Planner仅在上述observable full pass证据完整且所有frozen identities/zero budgets保持时，结合已经接受的P3-C1
evidence接受provenance I/O correction。即使P3-C2被接受，也只允许Orchestrator把
`REF-P7-25-R2-B2-R2`重新标为`READY_FOR_PLANNING`；不得由Executer直接运行real B2/B3/B4、validator、
eligibility或release。

## 5. Locks与授权

External C1/retained/release evidence reads/root、retained release audit、canonical validator、eligibility、release
generation/qualification/copy/consumption、network/DNS/`.env`/credentials、device、camera、Ray、strip、cleanup、
capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware和deployment全部hard locked at zero。

这是纯离线validation observability package，不涉及科学分支或高风险设备操作，不需要Advisor或Human授权。唯一stop为
`B2_P3_C2_OBSERVABLE_FULL_VALIDATION_WAITING_PLANNER_REVIEW`；到达后必须由Planner独立验收，再由Orchestrator
决定FULL状态。

## 维护性判断

本包不改code/test、不新增owner或artifact，只用单一低输出shell owner补齐full terminal evidence。现有helper/test
ownership和复杂度不变，无需维护性重构。
