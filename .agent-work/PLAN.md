# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-13：exact machine-contract scanner owner 实现

**计划状态：** `EXECUTABLE_ONCE_WAITING_EXECUTER`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-13`

**Active plan contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-13`

**Parent reviewed task：** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-12`

**C12 review archive：** `.agent-work/PLANS/20260730-0153-p7-retained-r3-option-b-b1a-c3e6f17-corrective-12-review.md`；SHA-256 `c85655587e8b895d1a14170de38f4a75e69f8158254906b640bfd58e888e2eec`。

**Frozen activation-parent HEAD：** `df1cdffb27699da7feac54379a8581cff9e85392`

**Frozen FULL SHA-256：** `e1c81dbd63c33292845b43a6e719914d1149a709e8017f97cd315a6139d66a56`

**Activation identity owner：** Planner activation handoff 冻结 PLAN SHA；Orchestrator 整理工作区后，dispatch handoff 冻结 activation commit SHA。该 commit 的 direct parent 必须是上述 frozen activation-parent HEAD，changed paths 必须严格只有 `.agent-work/PLAN.md`，且 committed PLAN blob 的 SHA-256 必须等于 Planner handoff SHA。PLAN 不作递归自散列断言。

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-13","task_id":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-13","package_kind":"bounded_validation_only_helper_and_dedicated_test","frozen_activation_parent_head":"df1cdffb27699da7feac54379a8581cff9e85392","dispatch_head_owner":"orchestrator_activation_commit_handoff","frozen_full_sha256":"e1c81dbd63c33292845b43a6e719914d1149a709e8017f97cd315a6139d66a56","implementation_changed_paths":["src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py","tests/test_agent_work_machine_contract.py"],"evidence_append_path":".agent-work/EXECUTION_RESULT.md","before_identity":{"src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py":{"head_blob_oid":null,"sha256":null,"state":"absent"},"tests/test_agent_work_machine_contract.py":{"head_blob_oid":null,"sha256":null,"state":"absent"}},"execution_budget":{"implementation_file_creations":2,"execution_result_appends":1,"targeted_test_invocations":1,"compile_checks":1,"diff_checks":1,"retry":0,"fallback":0,"git_mutations":0,"artifact_operations":0,"external_path_operations":0,"retained_r3_access":0,"release_access":0,"candidate_access":0,"network_access":0,"env_access":0,"device_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"formal_access":0,"public_analyzer_access":0},"planner_stop_required":true}`

## 唯一 current package

只实现一个 repository-owned、validation-only、纯 `bytes` machine-contract scanner 及其 dedicated unit test。它替代 C11/C12 的临时手工 scanner，但不读取任何路径、不修复任何 payload、不访问 retained R3，也不判断或发出 eligibility。canonical lineage validator 继续是唯一 eligibility owner。

允许的 implementation changed-path set 必须严格等于以下两条，且二者在 frozen HEAD 与 dispatch 前 worktree 中都必须为 absent：

- `src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py`
- `tests/test_agent_work_machine_contract.py`

`.agent-work/EXECUTION_RESULT.md` 仅是角色要求的 append-only evidence channel，不计入 implementation changed-path set；除这两条实现路径与一次 ER append 外，不得修改、创建、删除、重命名或 stage 任何 repository path。

## 0. Preflight gate（任何写入之前）

Executer 必须一次性验证：

1. `git rev-parse HEAD` 恰为 Orchestrator dispatch handoff 的 activation commit；其 direct parent 恰为 frozen activation-parent HEAD，commit changed paths 严格只有 `.agent-work/PLAN.md`，committed PLAN SHA-256 恰为 Planner activation handoff SHA；FULL raw SHA-256 恰为 frozen FULL SHA。
2. FULL 的唯一 canonical machine row 仍绑定 active task/contract 为 C13，`retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`，且 `candidate_contract_orchestrator_verified=true`。
3. 两条 implementation path 都是 absent，HEAD blob OID、worktree bytes 与 symlink 均不存在；不得覆盖已有路径。
4. worktree 在写入前无 staged path，且除 Planner/Orchestrator 已明确交接的 PLAN/FULL 状态外无其他 dirty path。发现未知 dirty path 必须 fail closed，不得整理、覆盖或回退。

任一 gate 失败时，禁止创建两个目标文件；只允许向 ER append 一次可用失败 evidence，然后 Planner stop。不得 retry、fallback、改 PLAN/FULL、探测旧 root 或扩大读取范围。

## 1. Helper public contract

模块必须仅暴露以下 validation surface（命名可包含必要的 `__all__`，不得增加 path/controller/eligibility API）：

- `PLAN_MACHINE_MARKER = b"`PLAN_MACHINE_CONTRACT="`
- `FULL_PLAN_MACHINE_MARKER = b"`FULL_PLAN_MACHINE_STATE="`
- `MachineContractValidationError(ValueError)`：至少保存稳定 `code: str` 与 JSON-serializable `evidence: dict[str, object]`。
- frozen dataclass `MachineContractEvidence`，包含下列 exact fields，并提供 deterministic JSON-serializable mapping：
  - `schema="agent_work_machine_contract_scan_evidence_v1"`
  - `owner`（只可为 `PLAN` 或 `FULL`）
  - `marker_ascii`
  - `source_bytes`、`source_sha256`
  - `candidate_count`、`candidate_lines`（1-based）
  - 成功时的 `line_number`、`raw_row_bytes`、`raw_row_sha256`、`payload_bytes`、`payload_sha256`、`line_ending="LF"`
- frozen dataclass `ParsedMachineContract`，只包含 `value: dict[str, object]` 与 `evidence: MachineContractEvidence`。
- `parse_plan_machine_contract(source: bytes) -> ParsedMachineContract`
- `parse_full_plan_machine_state(source: bytes) -> ParsedMachineContract`

两个 public parser 必须把 marker/owner 固定在各自函数中；不得接受 caller-supplied marker、path、allowlist、repair callback、validator callback 或 eligibility callback。只接受 exact built-in `bytes`，`str`/`bytearray`/`memoryview` 等均 fail closed。

## 2. Pure-bytes exact semantics

对各自独立传入的 source bytes 执行以下唯一算法：

1. 计算整个 source 的 byte count 与 SHA-256；使用 `splitlines(keepends=True)`，只把从物理行首 `startswith(exact marker)` 的行计为 candidate。正文、缩进、inline example、另一 owner marker 都不是 candidate。
2. candidate 数量必须严格为 `1`；`0` 或 `>1` 均抛 `MachineContractValidationError`，evidence 必须保留 source identity、candidate count 与 candidate line numbers，不得选择 first/last、alias 或 fallback。
3. 唯一 candidate 必须以 exact bytes `` `\n `` 结束；CRLF、EOF 无 LF、backtick 后额外空格/字节、额外 backtick 或错误 suffix 全部 fail closed。只移除 exact marker 与末尾两个 bytes `` `\n ``；不得 `.strip()`、`.rstrip()`、normalize 或 repair。
4. payload 以 UTF-8 strict decode；使用 strict JSON object decode：拒绝 invalid UTF-8、syntax error、duplicate keys（含 nested object）、`NaN`/`Infinity`/`-Infinity` 及 top-level list/scalar/null。不得改变 JSON value 或 type；特别是 `true` 不得等同整数 `1`，整数 `0` 不得等同 `false`。
5. 成功只返回 parsed dict 与可重放 evidence；raw-row SHA 必须覆盖含末尾 LF 的完整物理行，payload SHA 必须覆盖 marker 后、末尾 backtick+LF 前的 exact JSON bytes。

Helper 不得 import/use `pathlib`、`os`、`subprocess`、network/device modules、retained-release audit module或 canonical validator；不得打开文件、读取环境变量、写文件、运行 Git、修复/重编码 input、输出 `candidate_eligible`、`production_release_usable` 或任何 eligibility verdict。

## 3. Dedicated tests

只创建 `tests/test_agent_work_machine_contract.py`，沿用项目 `unittest` 风格。至少覆盖并验证真实结果，而非仅执行代码：

1. 合法 PLAN LF row 与合法 FULL LF row：parsed nested value/type 完全保真；evidence 的 owner、marker、source/raw-row/payload bytes、SHA、1-based line 与 candidate count 均由测试独立重算。
2. PLAN/FULL owner separation：各 parser 忽略另一 owner row；只有错误 owner 时得到 zero-candidate；两份 bytes 不得共用或替换 owner。
3. CRLF、EOF 无 LF、错误 suffix（backtick 后空格、额外 backtick）、错误/缩进 prefix分别 fail closed。
4. duplicate valid candidates fail closed，并保留 count 与全部 candidate line numbers。
5. invalid UTF-8、malformed JSON、top-level list/string/number/bool/null 全部 fail closed。
6. duplicate JSON keys（顶层及 nested）与 non-finite constants 全部 fail closed。
7. JSON value/type：`true`、`false`、整数 `0/1`、字符串、null、list、nested object 的值与 Python type 均准确且不被等值比较混淆。
8. 非 exact `bytes` 输入全部 fail closed；异常 code/evidence schema 稳定且可 JSON serialize。
9. public surface 不接受 path/callback/marker 参数；source module 不含 path I/O、payload repair、validator import 或 eligibility emission owner。

## 4. 唯一验证序列

实现完成后只允许按顺序执行一次：

1. Targeted tests（一次 invocation）：`PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -p 'test_agent_work_machine_contract.py' -v`。
2. No-write compile check（一次）：用 `.venv/bin/python -c` 读取 helper bytes 并调用 built-in `compile(..., 'exec')`；不得用会产生 `__pycache__`/`.pyc` 的 `compileall` 或 `py_compile`。
3. Helper replay：由 caller 分别读取当前 PLAN/FULL bytes，调用两个 public parser，逐 owner 核对 C13 task/contract、FULL retained lock 与 candidate verification；记录两份 source SHA、raw-row SHA、payload SHA、line 与 evidence schema。Helper 自身不得读取路径。
4. Scope/diff check（一次 ledger）：`git diff --check --` 限定 exact two implementation paths，并确认 implementation diff path set 恰为两条、无 staged paths、无第三条 source/test/doc path。ER append 后单独允许 ER 成为 evidence-only dirty path。

任何一步失败，不得在本 package 内修改后重跑、fallback 或调用 broader/full tests；保留当前 bytes，append 一次 terminal evidence 并停 Planner review。通过也不得运行 full suite、canonical validator、public analyzer、bootstrap、manifest、real retained-R3 audit 或 release consumer；这些属于后继独立 PLAN。

## 5. Before/after identity 与 ER evidence schema

写入前冻结的两条 identity 均为：`state=absent`、`head_blob_oid=null`、`sha256=null`。写入和验证后，Executer 必须对每条目标记录：

- relative path、before state/blob/SHA；
- after byte count、SHA-256；
- read-only `git hash-object --no-filters -- <path>` 计算出的 after blob OID（不得使用 `-w`）；
- test/compile/replay 后再次读取的 final byte count、SHA 与 blob OID，并证明与 after identity 相同。

ER 只 append 一次 `C13_IMPLEMENTATION_RESULT` strict-JSON object，至少包含：

- schema、timestamp、terminal `PASS|FAIL`、first_failure_stage/reasons；
- task/contract、dispatch PLAN SHA、FULL SHA、activation-parent HEAD、dispatch activation HEAD 及其 exact one-path lineage；
- exact implementation path set；每条 before/after/final bytes、SHA-256 与 blob OID；
- helper API/version、test command/exit/test count、compile command/exit、diff-check result；
- PLAN/FULL replay evidence（source/raw-row/payload SHA、candidate lines/count、owner、解析出的 frozen fields）；
- `implementation_file_creations`、`execution_result_appends` 与全部 zero-budget counters；
- retained status、canonical validator call count `0`、eligibility emission count `0`、git status/staged ledger 与 `planner_stop=true`。

若失败发生在目标创建前，记录可用 preflight identity；若发生在创建后，保留当前文件并记录实际 identity。不得伪造缺失字段、删除失败文件、重写旧 ER 或 append 第二条结果。

## 硬锁与 stop

- `.agent-work/PLAN.md`、`.agent-work/FULL_PLAN_REFERENCE.md`、GUIDE、RESEARCH、debug、archive全部只读；ER 仅一次 append。
- 旧 controller/source、旧 evidence root、retained R3 三 artifact、candidate、setup/lineage release、manifest、canonical validator、consumer/replay、qualification、bootstrap、Git stage/commit/amend/rebase、network、DNS、`.env`、credential、device、camera、Ray、strip、cleanup、capture、FORMAL、TD-C、sentinel、P8、public analyzer全部为 `0`。
- 本包不命中高风险设备授权，也不需要 Advisor 科学决策；这不解锁任何后继任务。
- 无论 PASS/FAIL，ER append 一次后立即 Planner stop。Executer 不得自行 commit；Planner 必须独立审查 exact two-path diff、identities、tests 与 replay evidence，Orchestrator随后决定 FULL 状态与 Git 整理。

**Planner stop：** `C13_IMPLEMENTATION_TERMINAL_WAITING_PLANNER_REVIEW`。

**维护性判断：** 连续临时 scanner 漂移已满足 rule-of-three；单一纯 bytes helper 与 dedicated tests 把 machine-row解析收敛在 validation-only owner，不触碰 canonical eligibility owner，也不向实验 controller 增加复杂度。
