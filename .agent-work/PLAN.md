# REF-P7-25-R2-B2-P3-C2-C1：corrected observable full validation

**计划状态：** `WAITING_ORCHESTRATOR_REVIEW_AND_ACTIVATION`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-P3-C2-C1`

**Parent reference task：** `REF-P7-25-R2-B2-P3-C2`

**Contract ID：** `P7-TD-B-RETAINED-R3-PROVENANCE-IO-OBSERVABLE-FULL-VALIDATION-V2`

**当前唯一动作：** Orchestrator独立审核、同步FULL并激活后，Executer只运行一次修正后的低输出observable full
validation；使用普通非特殊zsh变量并使Python stdout unbuffered，保留真实child exit与完整
`Ran 741 tests ...`/`OK`终态。不得编辑code/test、重跑已接受gate、触碰external/retained evidence或进入real B2。

**预计时长：** `<10 minutes`；不使用visible Terminal、automation或后台长任务流程。

**唯一执行 stop：** `B2_P3_C2_C1_CORRECTED_OBSERVABLE_FULL_VALIDATION_WAITING_PLANNER_REVIEW`。

**本次P3-C2 review archive：**
`.agent-work/PLANS/20260730-2213-p7-retained-r3-provenance-io-p3-c2-pipeline-review.md`，
bytes `8122`，SHA-256
`4541967011d103c763fd80ae273285a7611308df6d9f3a510f39881b22708052`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_provenance_io_corrected_observable_full_validation_plan_v2","reference_task_id":"REF-P7-25-R2-B2-P3-C2-C1","parent_reference_task_id":"REF-P7-25-R2-B2-P3-C2","contract_id":"P7-TD-B-RETAINED-R3-PROVENANCE-IO-OBSERVABLE-FULL-VALIDATION-V2","execution_authorized":true,"activation_required":true,"activation_commit":{"expected_parent":"05495ae6e07a8b3ae3a2a2bc899590dbcb68a119","expected_subject":"chore(plan): activate corrected retained r3 observable full validation","exact_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260730-2213-p7-retained-r3-provenance-io-p3-c2-pipeline-review.md"]},"frozen_implementation_commit":"1f88cf42d95c00c7db5692e78ed1d663732d5701","validation":{"corrected_quiet_full":1,"retry":0,"fallback":0,"alternate_full":0,"count_probe":0,"targeted":0,"focused":0,"compileall":0,"codegraph_sync":0,"postcommit_targeted":0},"shell_contract":{"python_stdout_unbuffered":true,"exit_variable":"child_exit_code","forbidden_zsh_special_parameters":["status"],"marker":"__P3_C2_C1_FULL_EXIT__","tail_lines":40},"writes":{"source":0,"test":0,"plan":0,"full":0,"archive":0,"stage":0,"commit":0},"zero_budgets":{"external_evidence_reads":0,"external_root_creation":0,"retained_release_audit":0,"canonical_validator":0,"eligibility":0,"release_operation":0,"network":0,"environment":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"planner_stop":"B2_P3_C2_C1_CORRECTED_OBSERVABLE_FULL_VALIDATION_WAITING_PLANNER_REVIEW"}`

## 1. Activation与frozen preflight

Executer不得在Orchestrator activation前执行。Activation commit必须满足machine contract的exact parent、subject和
exact three-path topology；激活后的FULL必须有exact一个active task/contract为本包，并继续声明：

- `REF-P7-25-R2-B2-P3-C2`已因PLAN pipeline使用zsh只读特殊参数而rejected；
- `retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`；
- P3-C1 code findings closed，acceptance仍只缺corrected observable full terminal evidence；
- P3-C2-C1 active；
- real B2/B3/B4、validator、eligibility和release consumption locked。

执行前只读证明：

1. HEAD为activation commit且worktree/stage/untracked sets clean；
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
5. P3-C2 review archive bytes/hash与本PLAN header一致。

任一不符即preflight hard failure：corrected full invocation为0，只向ER追加真实handoff并stop。不得repair、retry、
rebase、checkout、reset、stage或接管ambient work。

本包可读取repo source、tests、Git object database、PLAN/FULL/archive/ER。禁止读取
`/Volumes/4T/temp/rgbww-optimizer`中的C1、retained-R3、release或旧run artifact；full tests自己按既有
tearDown管理的disposable test directories不算external evidence read/root。

## 2. Accepted/rejected evidence that must not be rerun or reinterpreted

Planner已接受P3-C1的以下one-shot evidence，Executer必须复用而不得重新调用：

- targeted `24/24`；
- focused `71/71`；
- compileall exit `0`；
- CodeGraph sync exit `0`，`Already up to date`；
- pre/post scope、diff、stage和commit topology checks；
- postcommit targeted `24/24`，final `OK`；
- `REV-P3-001`、`REV-P3-002`和`REV-P3-003` code/test closure。

P3-C2的唯一unittest invocation因exact PLAN pipeline在`status=$?`处触发
`zsh: read-only variable: status`而没有observable child marker或terminal summary。该invocation不得重跑、探测、
重解释、合并或算术推导；outer shell exit `1`既不证明unittest失败，也不证明unittest通过。

不得运行targeted、focused、compileall、`codegraph sync`、postcommit targeted、第二种test command、collection/count
probe或dry-run。不得编辑source/test以改变count或输出。

## 3. 唯一corrected quiet full与observable terminal contract

Preflight通过后，运行exact一次以下zsh pipeline。保持一个shell/session owner；使用普通变量
`child_exit_code`，明确禁止赋值或引用zsh只读特殊参数`status`；以`PYTHONUNBUFFERED=1`避免late buffered stdout把
unittest terminal summary推出retained tail：

```zsh
set -o pipefail
{
  PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'
  child_exit_code=$?
  print -r -- "__P3_C2_C1_FULL_EXIT__=${child_exit_code}"
  exit "${child_exit_code}"
} 2>&1 | tail -n 40
```

这段pipeline中的unittest process是本包唯一validation invocation。不得用`tee`、文件重定向、第二个reader、
新log/evidence root、detached process、background owner或外部wrapper。Executer必须保留该same session的：

- structured shell terminal exit；
- exact一行`__P3_C2_C1_FULL_EXIT__=<n>`；
- unittest terminal exact一行`Ran 741 tests in ...s`；
- summary后的`OK`，或任何真实failure/error output。

Pass仅当：structured shell exit `0`、marker exact `0`、exact一条`Ran 741 tests in ...s`且其后final `OK`，并且
没有`FAILED`、`ERROR`、traceback、broken pipe、read-only variable、missing/truncated marker或count mismatch。

任一其他结果均hard failure。禁止retry、fallback、增大tail后重跑、另跑collection/count、用算术推导替代terminal、
修复测试、运行narrow suite或继续后续任务。只向ER记录真实输出、exit、缺口和计数后stop。

## 4. Handoff与acceptance evidence

无论pass/fail，Executer都只向`.agent-work/EXECUTION_RESULT.md`追加一个P3-C2-C1 handoff；不得修改PLAN、FULL或
archive，不得stage/commit ER。Handoff至少记录：

- activation、implementation、two-file、patch和archive preflight identities；
- exact pipeline text、shell/session owner、unittest invocation count；
- `PYTHONUNBUFFERED=1`、ordinary variable `child_exit_code`和forbidden `status` assignment/reference事实；
- structured shell exit、marker、完整retained tail、`Ran` count/time、final status；
- source/test/stage/commit写入计数全部0；
- targeted/focused/compileall/CodeGraph/postcommit rerun计数全部0；
- retry/fallback/alternate full/count probe全部0；
- 所有machine-contract zero budgets及retained/real-B2 locked state。

Planner仅在上述corrected observable full pass证据完整且所有frozen identities/zero budgets保持时，结合已经接受的
P3-C1 evidence接受provenance I/O correction。即使P3-C2-C1被接受，也只允许Orchestrator把
`REF-P7-25-R2-B2-R2`重新标为`READY_FOR_PLANNING`；不得由Executer直接运行real B2/B3/B4、validator、
eligibility或release。

## 5. Locks与授权

External C1/retained/release evidence reads/root、retained release audit、canonical validator、eligibility、release
generation/qualification/copy/consumption、network/DNS/`.env`/credentials、device、camera、Ray、strip、cleanup、
capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware和deployment全部hard locked at zero。

这是纯离线validation observability correction，不涉及科学分支或高风险设备操作，不需要Advisor或Human授权。
唯一stop为`B2_P3_C2_C1_CORRECTED_OBSERVABLE_FULL_VALIDATION_WAITING_PLANNER_REVIEW`；到达后必须由Planner
独立验收，再由Orchestrator决定FULL状态。

## 维护性判断

本包不改code/test、不新增owner或artifact，只修正单一shell observability contract并运行一次full suite。现有
helper/test ownership和复杂度不变，无需维护性重构。
