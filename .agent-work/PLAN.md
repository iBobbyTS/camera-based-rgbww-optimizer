# REF-P7-25-R2-B1A-C3E6F17：exact PLAN-row-marker fixed-container bootstrap

**计划状态：** `active_executable_exact_marker_bootstrap`

**Planner 日期：** `2026-07-29`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F17`

**执行合同：**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-PLAN-ROW-MARKER-BOOTSTRAP-V1`

**当前只读 FULL SHA-256：**
`15127763a68a68b70404ce57ece44efbbfc1375a844588520584e2d1615b6725`

**F16 review archive：**
`.agent-work/PLANS/20260729-1659-p7-retained-r3-option-b-b1a-c3e6f16-plan-row-label-review.md`

**F16 review archive SHA-256：**
`8f5a221061fe242c6a1696214b8493a47bddb10fd2c1e5dfc0e0a3f22e1e16b9`

`PLAN_MACHINE_CONTRACT={"schema":"context_closed_bootstrap_plan_v2","reference_task_id":"REF-P7-25-R2-B1A-C3E6F17","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-PLAN-ROW-MARKER-BOOTSTRAP-V1","frozen_full_sha256":"15127763a68a68b70404ce57ece44efbbfc1375a844588520584e2d1615b6725","plan_machine_row_marker":"PLAN_MACHINE_CONTRACT=","full_machine_row_marker":"FULL_PLAN_MACHINE_STATE=","full_machine_row_scope":"unique_FULL_PLAN_MACHINE_STATE_row_only","full_reference_scope":"REF-P7-25-R2-B1A-C3E6F17_section_only","required_full_machine_subset":{"schema":"orchestrator_full_plan_reference_v2","active_task_count":1,"active_task":"REF-P7-25-R2-B1A-C3E6F17","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-PLAN-ROW-MARKER-BOOTSTRAP-V1","checkpoint_head":"9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e","release_checkpoint":"32b9e670ff3bbea0cd1505528c2ca87c2935446c","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","executer_dispatched":true,"device_authorized_by_this_file":false,"release_authorized_by_this_file":false,"candidate_machine_contract_sha256":"3c5847fcbe0af85833c901f6f01058d000a3cecdc0f84e6ae331ed24e138c225","candidate_contract_orchestrator_verified":true},"observed_full_active_task":"REF-P7-25-R2-B1A-C3E6F17","observed_full_active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-PLAN-ROW-MARKER-BOOTSTRAP-V1","observed_full_executer_dispatched":true,"activation_status":"ACTIVE_EXACT","executer_dispatch_authorized":true,"bootstrap_exec_command_max_after_activation":1,"pre_bootstrap_other_tool_calls":0,"post_bootstrap_er_appends_max":1,"codex_cli_secondary_dispatcher_forbidden":true,"controller_execution_authorized":false,"test_execution_authorized":false,"git_mutation_authorized":false,"r3_authorized":false,"release_authorized":false,"network_authorized":false,"device_authorized":false,"planner_stop":"return_after_one_bootstrap_terminal_and_one_ER_append"}`

## 1. 当前唯一动作与 Planner stop

F16 已因 bootstrap loader 错把 PLAN owner 读作不存在的 `PLAN_MACHINE_STATE` 而在任何路径检查前
hard-fail。Orchestrator 已把 FULL 的唯一 active task/contract 更新为本 F17，并保持
`active_task_count=1`、`executer_dispatched=true`、checkpoint、retained-R3 lock、device/release false
和其余 roadmap locks 不变。Planner已按新 FULL SHA刷新本 PLAN，并证明 required subset `12/12`
exact、activation mismatch为零；现在只授权本计划定义的唯一 direct Executer bootstrap。

## 2. F17 唯一固定路径

激活后只允许以下四条全新路径：

1. target：`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f17-offline`
2. record：`/Volumes/4T/temp/rgbww-optimizer/c3e6f17-container-bootstrap.json`
3. seal：`/Volumes/4T/temp/rgbww-optimizer/c3e6f17-container-bootstrap.seal.json`
4. fallback：`/Volumes/4T/temp/rgbww-optimizer/c3e6f17-container-bootstrap.fallback.json`

四条路径在 bootstrap attempt 前必须全部 absent。不得读取、删除、修复、重试或复用 F16 路径；
不得创建 timestamp root、clone、临时路径、alternate target 或其他 artifact。

## 3. Direct Executer 与 exact row-marker owner

激活后 Orchestrator 只能派发一个直接 worker Executer subagent，并把本合同完整交给它。Executer 的
首个 tool call 必须是唯一 bootstrap `exec_command`；此前不得 memory lookup、skill/doc/GUIDE、FULL
broad read、shell discovery、status 或其他 tool call，不得启动 Codex CLI 或二级 dispatcher。

该唯一命令只启动一次 Python 标准库进程。limited-input loader 必须按以下两个不同且不可互换的 exact
markers 解析：

- PLAN：恰好一条以反引号包裹、内容前缀为 `PLAN_MACHINE_CONTRACT=` 的行；JSON bytes 是 exact
  marker 后至末尾反引号前的 substring。
- FULL：恰好一条以反引号包裹、内容前缀为 `FULL_PLAN_MACHINE_STATE=` 的行；JSON bytes 是 exact
  marker 后至末尾反引号前的 substring。

不得搜索、要求、生成或把 `PLAN_MACHINE_STATE` 当成 alias。两个 loader 都必须拒绝零条、多条、错误
marker、非对象、duplicate key、NaN/Infinity、错误 JSON 类型或 required-key mismatch。它只能读取当前
PLAN raw bytes、FULL 的唯一 machine row 与唯一 F17 section、shared Git metadata；不得读取 MEMORY、
skill、GUIDE、ER、archive、controller/source、candidate、fixture、canonical content、测试、retained R3、
release 或设备内容。

任一 limited-input、marker、activation、hash、section uniqueness 或 required-subset failure 必须在检查
四条路径前终止；container/record/seal/fallback attempts 与 succeeded 全部为 `0`，仅 append 一次 ER 后
停 Planner。

## 4. 唯一 bootstrap 方法

通过 limited-input gate 后，标准库进程执行且只执行：

1. 证明四条 F17 路径 absent、parent 是 existing directory/non-symlink；仅一次
   `os.mkdir(target, 0o700)`。
2. `lstat`/directory-fd `fstat` 证明 exact target、directory/non-symlink、mode `0700`、
   uid/gid/dev/inode一致；container empty；fsync container 与 parent。
3. 仅一次 `O_CREAT|O_EXCL|O_WRONLY`、mode `0600` 写 deterministic UTF-8 strict JSON record；
   file/parent fsync、duplicate/nonfinite-reject reload、serialized raw-byte equality 与独立 SHA-256。
4. 同样一次性写 seal；seal绑定 PLAN raw SHA、限定 FULL row/F17 section raw SHA、Git metadata、
   target/record identities、record raw SHA和实际 counters；完成相同 fsync/reload/raw hash。
5. 写后再次证明 target identity/mode未漂移且仍为空；record/seal必须在 container 外。

成功实际计数必须精确为 container/record/seal attempts+succeeded 各 `1`，fallback `0/0`；
`retry=reuse=rewrite=alternate_path=0`。

## 5. 失败 terminal 与实际计数

bootstrap gate 后任一 creation、identity、mode、emptiness、fsync、strict reload、raw equality/hash、Git
metadata或post-write drift失败，保留已有 F17 artifact，不删除、修复、替换或重试。只可对 fixed fallback
尝试一次 `O_EXCL`/`0600` deterministic strict JSON terminal，并执行 strict reload、file/directory fsync
与独立 raw SHA；随后停 Planner。

所有 terminal 必须记录实际 attempted/succeeded，且每类 attempt `<=1`、succeeded `<=attempted`。
Limited-input/dispatch failure仍是四类 `0/0`且不得检查路径或创建 fallback；fallback自身失败不得重试。

## 6. 零预算、交接与锁

Controller/source/candidate root/clone/fixture/canonical-content、package/import、tests、stage、commit、validator、
manifest、retained R3、audit、eligibility、consumer、release、network、DNS、`.env`、credential、device、camera、
Ray、strip、cleanup、capture、public analyzer、FORMAL、firmware和deployment全部为 `0`。

唯一 bootstrap command 返回后，Executer只可 append一次 `.agent-work/EXECUTION_RESULT.md`，再做该记录
必要的只读 hash/stat核验并立即停 Planner。Pass也只建立一个empty sealed F17 prerequisite，不授权
controller、后继package、R3、eligibility、release、network或device。

**维护性判断：** F17 只把 PLAN/FULL 两个 machine-row marker 的不同 owner 显式固定；不改代码或科学合同，不新增并行执行路径。
