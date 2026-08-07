# G4-DEENG-00 — Git 保护与可恢复拓扑 package

## Package 状态与单一 ownership boundary

- **milestone:** `G4-DEENG-00-GIT-PROTECTION`
- **active task:** `REF-G4-DEENG-00-PRESERVE-MERGE-BACKUP-BRANCH`
- **status:** `EXECUTABLE_GIT_PROTECTION_PACKAGE`
- **single ownership boundary:** 只收敛当前 dirty state，并建立可恢复的本地/远端 Git
  拓扑；dirty inventory、必要 checkpoint commit、local `main` fast-forward、backup
  branch push/verification 与 refactor branch creation 是一个不可拆分的低密度 batch。
- **Planner stop:** 切换到精确 refactor branch 并写完执行结果后，立即
  `RETURN_TO_PLANNER_ON_REFACTOR_BRANCH_FOR_TERMINAL_REVIEW`。当前 PLAN 不预先声称
  package 已终局接受；届时 Planner 只做一次终局验收、归档本 PLAN，并写入 terminal
  non-executable state。

## 科学目标与唯一 blocker

- **scientific_target:** 在不损失 accepted source/test、terminal evidence、冻结科学输入或
  可复现能力的前提下，为 GUIDE 4 去工程化建立完整、可远端恢复的起点。
- **next_scientific_action:** 去工程化 readiness 完成后的 Ray R6 acquisition；本 package
  不进入 readiness、实验或分析。
- **science_delta:** `none`；Git commit、branch 与 push 只是工程保护证据，不是 measurement、
  scientific unlock 或 scientific negative result。
- **唯一 blocker:** 当前 accepted dirty state 尚无合并后 exact baseline 的远端 rollback
  ref，直接开始大规模删除会缺少可恢复点。

## 冻结起点与 Human 授权

- source branch：`codex/g4-r6-owner-alignment-large-change`；design-time HEAD：
  `463a151bede3013db14d31802ea93fafa2322bf6`。
- local `main` design-time OID：`3c920c6d29e5c366ce3843a2532d30d80c6f0c33`；它是
  design-time source HEAD 的祖先，design-time `main...source` 为 `0 33`。
- local tracking `origin/main` design-time OID：
  `4e8d9c7330a0c2be6bb9f9dd912ec2b39348fbcd`；本 package 不 fetch 或 push `main`。
- frozen `origin` URL：`git@github.com:iBobbyTS/camera-based-rgbww-optimizer.git`。
- backup branch：`codex/backup-guide4-pre-deengineering-20260806`；refactor branch：
  `codex/guide4-science-first-deengineering`。设计时两者均无本地 ref，也无本地
  remote-tracking ref；任何执行时漂移都停止。
- Human 授权顺序固定为：先提交当前 source dirty state；再 FF-only 到 local `main`；从
  合并后的 exact `main` 建立并只推送 backup branch；验证远端同 OID 后，才从该 protected
  `main` 建立并切换 refactor branch。不得重排或扩大授权。

## 一次性 dirty inventory 与 Orchestrator 确认

Executer 在 package 起点只运行一次 read-only dirty inventory，取得 porcelain branch/status
与 exclude-standard untracked 清单；后续 clean-state 查询只是状态门，不得重新解释或扩展
分类。Orchestrator 必须亲自确认 status 类型、下列精确路径集、每项语义分类及 commit 目标；
Executer 只能执行确定性检查和已确认命令，不能代替该判断。

| 分类 | 起点路径与预期状态 |
| --- | --- |
| accepted runtime-consumer source/tests | `M src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`；`M src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py`；`M tests/test_agent_work_machine_contract.py`；`M tests/test_p7_td_b_r6_stage_gate.py` |
| active/terminal orchestration state | `M .agent-work/EXECUTION_RESULT.md`；`M .agent-work/PLAN-FULL.md`；`M .agent-work/PLAN.md`（本次 activation 内容仍属同一路径） |
| terminal archives | `?? .agent-work/archived/EXECUTION_RESULT-20260806-environment-terminal-stop.md`；`?? .agent-work/archived/EXECUTION_RESULT-20260806-ray-r6-package-mismatch-terminal.md`；`?? .agent-work/archived/PLAN-20260806-environment-terminal-stop.md`；`?? .agent-work/archived/PLAN-20260806-g4-runtime-consumer-boundary-v1.md`；`?? .agent-work/archived/PLAN-20260806-ray-r6-package-mismatch-terminal.md` |
| active debug route | `M .agent-work/debug/INDEX.md`；`?? .agent-work/debug/active/20260806-guide4-science-first-deengineering.md` |

精确集合应为 14 个路径、8 个 tracked 修改、6 个 untracked 文件，无 staged、deleted、
renamed 或其他条目。不得 stage `.DS_Store`、`desktop.ini`、editor swap、cache、`.venv`、
构建物、实验输出、临时日志或任何仓库外 root；当前 inventory 不含这些项目。出现任何额外、
无法分类或不应跟踪路径时，不删除、不 clean、不猜测归属，立即停止并报告 Human。

## 单一有序执行 batch

### 1. 既有证据核验与 rollback checkpoint

1. 不重跑已通过的 76-test suite，也不运行任何 targeted/full test。只读核验
   `.agent-work/archived/PLAN-20260806-g4-runtime-consumer-boundary-v1.md` 已记录的
   `Ran 76 tests in 504.422s`、`OK`、exit `0` 与 output SHA-256
   `6611d5ef56e7f62cf43abfb4870dfbc79169927fd2e886a2d288f04e919233d6`；核对当前
   source/test diff 仍严格只覆盖表中四个 accepted 路径及该 archive 描述的
   PLAN-FULL consumer/parser 迁移边界。
2. 对 14 个 classified paths 做 diff-scope 与 Markdown structure 检查；确认当前 PLAN 只有
   一个可 JSON 解析的 `PLAN_MACHINE_CONTRACT`，当前 PLAN-FULL 只有一个可解析的
   `PLAN_FULL_MACHINE_CONTRACT`，且 PLAN-FULL 仍为 context-only/non-executable、current
   milestone 为 `G4-DEENG-00-GIT-PROTECTION`。运行 `git diff --check`；任何失败只停止，
   不顺带修改 source/tests、archives、GUIDE 或 RESEARCH。
3. Executer 将本步实际 inventory、既有测试证据核验、diff/machine-row/Markdown/
   `git diff --check` 结果写入 `.agent-work/EXECUTION_RESULT.md`，仍由 Orchestrator 亲自
   确认最终 path allowlist 与 commit 目标。Orchestrator 亲自选择并记录准确 Conventional
   Commit message；Executer 不得自行扩大 staging。
4. 只按上表 14 个精确路径显式 stage，不使用 `git add -A`、glob 或目录级隐式扩展；核对
   staged path set 恰好等于 allowlist，并运行 `git diff --cached --check`。随后创建且只创建
   一个必要 checkpoint commit，保存 accepted dirty state、preflight evidence 与本 PLAN
   activation。把 activation 与 checkpoint 同 commit 是本 Git 保护 package 的明确例外；
   不允许 activation commit、selector commit、状态行 commit、amend 或任何额外 micro-commit。
5. 将新 commit OID 记为 `source_checkpoint_oid`，记录其 tree OID；确认 source branch 指向
   该 OID，index/worktree 在进入分支拓扑操作前均 clean。commit/hook/staged-scope 任一失败
   即停止，不使用 `--no-verify` 绕过。

### 2. local main 的 FF-only 保护合入

1. 紧邻 ref 写入前重新确认当前 source 指向 `source_checkpoint_oid`，local `main` 仍为
   `3c920c6d29e5c366ce3843a2532d30d80c6f0c33`，local tracking `origin/main` 仍为
   `4e8d9c7330a0c2be6bb9f9dd912ec2b39348fbcd`，`origin` URL 精确匹配冻结值，backup/
   refactor local refs 仍不存在，且 worktree/index clean；任一漂移停止。
2. 必须证明 `main` 仍是 `source_checkpoint_oid` 的祖先，`main...source_checkpoint_oid`
   left count 为 `0` 且 right count 大于 `0`。只有该门通过，才切换到 local `main` 并以
   `--ff-only` 合入 source branch；禁止 rebase、merge commit、squash、reset、clean、
   overwrite checkout 或 branch force-move。
3. 合入后 local `main` 必须精确等于 `source_checkpoint_oid`，没有第二个 commit，且
   worktree/index clean；否则停止。

### 3. exact backup branch 的唯一远端写入

1. 从已验证的 exact local `main == source_checkpoint_oid` 创建本地
   `codex/backup-guide4-pre-deengineering-20260806`；不得 `-f`，不得删除/复用漂移 ref。
2. 网络例外只允许对 `origin` 的 exact backup ref 做一次 pre-push `ls-remote`、一次显式
   push 和一次 post-push OID verification。pre-push remote ref 必须不存在；若已存在，
   无论 OID 为何都视为 ref drift 并停止。push refspec 必须只有：
   `refs/heads/codex/backup-guide4-pre-deengineering-20260806:refs/heads/codex/backup-guide4-pre-deengineering-20260806`。
   禁止 push `main`、其他 ref、tag 或 `--all`，禁止 force/force-with-lease，push attempt cap
   为 `1`。
3. post-push `ls-remote --refs` 必须只返回该 exact ref，且 OID 精确等于
   `source_checkpoint_oid`；本地 backup ref 也必须等于同一 OID。push 非零、拒绝、URL
   漂移、输出含额外 ref 或 OID 不一致均立即停止；即使远端可能已部分写入，也只记录一次
   exact-ref readback，不重试、不 force、不删除远端 ref。

### 4. refactor branch 与单一 Planner stop

1. 只有 remote backup 精确验证成功后，才从 protected local `main` 创建并切换
   `codex/guide4-science-first-deengineering`；不得从 remote-tracking、历史 ref 或其他 tree
   创建。新 branch、`HEAD`、local `main`、source 与 local/remote backup 必须都指向
   `source_checkpoint_oid`。
2. 在 refactor branch 上把 checkpoint OID/tree、FF relation、local/remote backup OID、
   exact origin URL、refactor base/current branch、无 main push 与所有 stop/failure 计数写入
   `.agent-work/EXECUTION_RESULT.md`。最终结果写入前必须已证明 worktree/index clean；写入后
   除该 Planner-review evidence 文件外不得出现其他新改动。
3. 立即回报 Planner 做一次终局验收。Planner 届时核验实际 Git refs/remote OID 与权限边界，
   决定接受或终态停止，归档本 PLAN，并写唯一 terminal non-executable state；当前执行者不得
   预写 acceptance、不得自行进入 `G4-DEENG-01`，也不得开始去工程化编辑。

## 成功、停止与恢复边界

- **执行成功候选（仍待 Planner 验收）：** refactor branch 当前 OID 等于 checkpoint；local
  `main`、source、local backup 与 remote backup 全部同 OID；main 未 push；初始 dirty state
  已由单一 checkpoint 保存；无设备/实验/外部-root effect。
- **checkpoint 前失败：** 保留原 dirty state 与 index 实况，停止；不得 stash、reset、clean、
  checkout 覆盖或删除用户文件。
- **checkpoint 后、main FF 前失败：** source checkpoint 是 rollback point；local `main`
  不变，停止。
- **main FF 后或 remote push 失败：** 保留 source/main/已创建 ref 的实际 OID 并停止；
  checkpoint 仍是恢复点。不得为了“回滚”移动 `main`、重写 commit、删除本地/远端 ref、
  force push 或执行反向 merge。
- **backup 已验证后、refactor creation 失败：** 保留远端 backup 与 exact main，停止；不删除
  backup，不改用别名 branch。任何恢复都必须由新的显式 Planner/Orchestrator 决策授权。
- 任一未分类改动、non-FF、branch/ref/OID/URL drift、push failure、remote verification
  mismatch 或权限疑问都 fail closed；retry=`0`，不得自行调整顺序或命令语义。

## 权限与禁止项

- 允许的 Git 写入仅为：一个 classified rollback checkpoint commit、local `main` FF-only、
  exact local backup branch creation、exact origin backup ref 的一次 push、exact refactor branch
  creation/switch。Orchestrator 必须亲自确认 dirty 分类、commit target/message 和所有 ref/
  URL/OID 远端写入目标。
- 一般网络权限为 `false`；唯一网络例外是上述 exact `origin` backup ref 的 precheck、一次
  push 与 post-push OID verification。不得 fetch、访问其他 remote/ref，或把该例外解释为
  设备/相机/实验网络权限。
- stage-gate/release package prepare/consume、formal/root、设备、相机、Ray、RGBWW strip、
  capture、analysis、TD-C、automation、外部 `/Volumes/4T` root 访问与测试执行全部为
  `false`。GUIDE/RESEARCH、source/tests、PLAN-FULL 与 archives 在执行期只读；Executer 仅可
  按本 PLAN 写 `EXECUTION_RESULT.md`，不得编辑 PLAN/PLAN-FULL。

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-DEENG-00-GIT-PROTECTION","plan_status":"EXECUTABLE_GIT_PROTECTION_PACKAGE","executable":true,"active_task_count":1,"active_task":"REF-G4-DEENG-00-PRESERVE-MERGE-BACKUP-BRANCH","current_milestone":"G4-DEENG-00-GIT-PROTECTION","single_ownership_boundary":"GIT_PROTECTION_RECOVERABLE_TOPOLOGY","scientific_target":"PRESERVE_ACCEPTED_GUIDE4_BASELINE_BEFORE_DEENGINEERING","next_scientific_action":"RAY_R6_AFTER_DEENGINEERING_READINESS","science_delta":"none","single_blocker":"NO_REMOTE_ROLLBACK_REF_FOR_EXACT_MERGED_PRE_DEENGINEERING_BASELINE","dirty_inventory_cap":1,"orchestrator_personal_dirty_classification_required":true,"orchestrator_personal_commit_target_message_confirmation_required":true,"orchestrator_personal_remote_target_confirmation_required":true,"existing_76_test_rerun_authorized":false,"test_execution_authorized":false,"full_suite_authorized":false,"git_checkpoint_commit_authorized":true,"git_checkpoint_commit_cap":1,"git_checkpoint_plan_activation_inclusion_authorized":true,"git_add_a_authorized":false,"git_amend_authorized":false,"git_fast_forward_main_authorized":true,"git_merge_commit_authorized":false,"git_rebase_authorized":false,"git_reset_authorized":false,"git_clean_authorized":false,"git_force_authorized":false,"git_branch_delete_authorized":false,"git_remote_delete_authorized":false,"git_main_push_authorized":false,"git_backup_branch_create_authorized":true,"git_backup_branch_push_authorized":true,"git_backup_branch_verify_authorized":true,"backup_push_attempt_cap":1,"git_refactor_branch_create_authorized":true,"git_refactor_branch_switch_authorized":true,"source_branch":"codex/g4-r6-owner-alignment-large-change","source_head_at_design":"463a151bede3013db14d31802ea93fafa2322bf6","main_head_at_design":"3c920c6d29e5c366ce3843a2532d30d80c6f0c33","origin_main_tracking_at_design":"4e8d9c7330a0c2be6bb9f9dd912ec2b39348fbcd","origin_url":"git@github.com:iBobbyTS/camera-based-rgbww-optimizer.git","backup_branch":"codex/backup-guide4-pre-deengineering-20260806","backup_remote":"origin","backup_remote_ref":"refs/heads/codex/backup-guide4-pre-deengineering-20260806","refactor_branch":"codex/guide4-science-first-deengineering","network_authorized":false,"origin_backup_git_network_exception_authorized":true,"origin_backup_git_network_scope":["PRE_PUSH_LS_REMOTE_EXACT_BACKUP_REF","ONE_EXACT_BACKUP_REF_PUSH","POST_PUSH_LS_REMOTE_EXACT_BACKUP_REF"],"package_prepare_authorized":false,"release_consumption_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"td_c_authorized":false,"automation_authorized":false,"external_root_access_authorized":false,"scientific_result_created":false,"terminal_review_required":true,"terminal_acceptance_preclaimed":false,"retry":0,"planner_stop":"RETURN_TO_PLANNER_ON_REFACTOR_BRANCH_FOR_TERMINAL_REVIEW"}`
