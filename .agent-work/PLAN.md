# REF-P7-25-R2-B1A-C3E6F18：Committed-helper fixed-container bootstrap prerequisite

**计划状态：** `WAITING_ORCHESTRATOR_FULL_ACTIVATION_NO_EXECUTER_DISPATCH`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F18`

**Proposed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F18-BOOTSTRAP-PREREQUISITE`

**Reviewed parent task：** `REF-P7-25-R2-B1A-C3E6F17-C13-LINEAGE-SEAL`

**Lineage-seal review archive：** `.agent-work/PLANS/20260730-0219-p7-retained-r3-option-b-b1a-c3e6f17-c13-lineage-seal-review.md`；SHA-256 `d6d8a47a0a60e06e7a4048dd7ae729e3952075031fe82858e358cf29a87319fb`。

## Planner decision and current stop

C13 lineage seal commit `64c34ade850aecd8c3aefb78358c7e66fcc4de88` 已通过 Planner 只读验收：direct parent、exact six changed paths、六条 committed identity、C13 archive、PLAN/FULL/ER binding 与 pre-review clean ledger 全部一致。该 commit 只固化 validation-only scanner owner，不产生 eligibility，也未触碰 retained R3、candidate 或 release。

本文件现在只保留一个 next package：使用已提交 helper 的最小离线 fixed-container bootstrap prerequisite。它尚未获得 FULL activation，当前严格禁止 dispatch Executer。

Orchestrator 必须先：

1. 独立复核上述 review handoff；
2. 更新其独占的 `.agent-work/FULL_PLAN_REFERENCE.md`，将 active task/contract 切换到本 task/contract，并记录 seal commit、direct parent、exact six-path lineage 与 review archive SHA；
3. 继续冻结 `retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`、canonical validator calls `0`、eligibility emissions `0`、`executer_dispatched=false`；
4. 按 AGENTS 整理并提交 Planner archive、PLAN 与 FULL 状态；
5. 再交 Planner 做一次 activation pass，冻结 dispatch HEAD、PLAN/FULL exact SHA 与唯一 machine contract。只有该 activation PLAN 被 Orchestrator 接受后才可 dispatch Executer。

## Prepared next package — exact objective

唯一目标是在外置临时根下创建一个全新、空、mode `0700`、identity 稳定且有 record/seal 证明的 fixed container prerequisite。此包不运行后继 controller，不创建 candidate root，不读取 retained R3，不运行 canonical validator，不产生 eligibility，也不创建或消费 release。

### Frozen repository owner

- accepted helper path：`src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py`
- committed helper blob：`5c581f9b502bcab1809b6a61a082a47f4150e09f`
- committed helper SHA-256：`743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f`
- owner functions：`parse_plan_machine_contract(source: bytes)` 与 `parse_full_plan_machine_state(source: bytes)`
- helper 只负责 exact machine-row pure-bytes parse/evidence；它不是 path、bootstrap、eligibility 或 release owner。

最终 activation 必须让同一 caller 分别读取 PLAN 与 FULL 为两个独立 raw `bytes` buffer，各调用对应 parser 恰一次；禁止手写/复制 marker scanner、alias、fallback parser、payload repair、跨 owner buffer 复用或从 prose 推导字段。

### Exact allowed repository paths

最终执行只允许读取：

- `.agent-work/PLAN.md` raw bytes；
- `.agent-work/FULL_PLAN_REFERENCE.md` raw bytes；
- 上述 committed helper 及 Python import 所需的现有 package metadata；
- shared Git repository 的只读 HEAD/direct-parent/changed-path/status metadata。

repository 写入只允许向 `.agent-work/EXECUTION_RESULT.md` append 一条 terminal strict-JSON evidence；PLAN、FULL、helper、test、GUIDE、RESEARCH、debug 与所有 archive 均只读。禁止 stage、commit、amend、rebase、checkout、reset、clean 或其他 Git mutation。

### Exact allowed external paths

只允许以下四条新路径；执行前均必须 absent，且不得选择 alternate/timestamp/fallback root：

1. container：`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f18-offline`
2. record：`/Volumes/4T/temp/rgbww-optimizer/c3e6f18-container-bootstrap.json`
3. seal：`/Volumes/4T/temp/rgbww-optimizer/c3e6f18-container-bootstrap.seal.json`
4. failure terminal：`/Volumes/4T/temp/rgbww-optimizer/c3e6f18-container-bootstrap.fallback.json`

parent `/Volumes/4T/temp/rgbww-optimizer` 必须是 existing regular directory、non-symlink。不得检查、读取、删除、修复或复用任何 F14/F15/F16/F17 root、record、seal、fallback 或历史外置 evidence。

### Exact call and operation budget

最终 activation pass 必须把整个 bootstrap 固定为 Executer 的首个且唯一 execution tool call：一个 `exec_command`、一个 Python 标准库 process、controller process/invocation `0`。该 process 内部完成 preflight、helper parse、只读 Git gate、四路径 absent gate、bootstrap、terminal evidence 与 ER 单次 append；不得启动 Codex CLI、二级 dispatcher、shell cleanup、test runner或另一个 Python process。

成功预算：

- PLAN helper parse `1`，FULL helper parse `1`；
- container create attempt/succeeded `1/1`；
- record create attempt/succeeded `1/1`；
- seal create attempt/succeeded `1/1`；
- fallback attempt/succeeded `0/0`；
- ER append `1`；
- retry、reuse、rewrite、alternate path、controller、test、canonical validator、eligibility、Git mutation全部 `0`。

失败预算：失败前操作按真实值记录；fixed fallback terminal最多 attempt `1`，不得删除、修复、重试或换路径。无论 PASS/FAIL，ER 只能 append 一次，随后立即 Planner stop。

## Bootstrap semantics

1. helper gate必须证明 PLAN/FULL各只有一个exact candidate，owner/source/raw-row/payload identity完整；激活后的 PLAN/FULL task/contract 必须均绑定C3E6F18，FULL retained lock保持不变。
2. Git gate必须绑定最终 activation 冻结的 dispatch HEAD/direct parent/changed-path set、seal commit `64c34ad...` 的祖先关系、helper committed blob/SHA及无未知 staged/dirty path。
3. 四条外置路径及目标container必须在任何创建前全部absent；任一存在或symlink立即fail closed，禁止检查内容或复用。
4. 只以单次 `os.mkdir(path, mode=0o700)` 创建container；禁止`mkdir -p`。以 `lstat` 与已打开directory fd的`fstat`证明exact absolute path、directory、non-symlink、mode、uid/gid/dev/inode，且container为空。
5. fsync container与parent。record/seal分别以`O_CREAT|O_EXCL`、mode `0600`创建；内容为deterministic UTF-8 strict JSON，reload时拒绝duplicate keys与non-finite constants；分别fsync file与parent并记录raw bytes/SHA-256。
6. seal必须绑定 PLAN/FULL/helper evidence、Git lineage、container identity、record bytes/SHA 与全部operation counters。写后再次证明container仍为空且lstat/fstat identity未漂移。
7. 任一 gate/creation/reload/fsync/identity/emptiness失败，只可按实际计数尝试一次fixed failure terminal；保留现场，不删除、不修复、不重试。

## Required terminal evidence

外置 record/seal/fallback 与 ER terminal row 必须至少记录：

- schema、UTC timestamp、terminal PASS/FAIL、first failure stage与reasons；
- task/contract、dispatch PLAN/FULL source bytes与SHA；
- helper committed path/blob/SHA以及PLAN/FULL parser evidence的owner、candidate count/lines、source/raw-row/payload bytes与SHA；
- dispatch HEAD/direct parent/changed paths/status ledger及seal commit ancestor binding；
- 四条exact paths、pre/post lstat/fstat、mode、uid/gid/dev/inode、emptiness、fsync结果；
- record/seal/fallback bytes与SHA、strict reload结果；
- 每项attempt/succeeded counter、ER append count和全部zero locks；
- `retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`、canonical validator calls `0`、eligibility emissions `0`；
- `planner_stop=true`。

## Acceptance, failure branch, and hard locks

PASS只证明一个empty sealed fixed-container prerequisite已建立；不授权后继 controller、candidate materialization、retained R3 audit、manifest、canonical eligibility validation、consumer或release。Planner必须独立只读验收外置 evidence、ER、路径 identity与预算后，再由Orchestrator决定下一包。

任何失败均保留现场并停止；不得在本包内修改脚本、换路径、重跑或进入后继。工程纠偏由Orchestrator建立新的bounded package，不需要Advisor；只有出现真正的色彩/测量科学分支矛盾才回Advisor。

retained R3、candidate、旧/新 release、manifest、consumer、canonical validator、eligibility emission、controller/source、clone、fixture/canonical content、tests、network、DNS、`.env`、credential、device、camera、Ray、strip、cleanup、capture、public analyzer、FORMAL、TD-C、sentinel、P8、firmware与deployment全部硬锁为 `0`。

**唯一当前 stop：** `C3E6F18_PREPARED_WAITING_ORCHESTRATOR_FULL_ACTIVATION_NO_EXECUTER_DISPATCH`。

**维护性判断：** 本包复用已提交的唯一 pure-bytes machine-contract owner，删除继续复制临时scanner的必要；bootstrap filesystem owner仍局限于单次外置执行，不增加生产或eligibility owner。
