# P7 FORMAL-R5 prelaunch Terminal-policy Planner review

**Review date：** 2026-07-26

**Reference task：** `REF-P7-04`

**Reviewed PLAN contract：** `P7-TD-B-RAY-PUBLIC-DEFAULT-FORMAL-R5`

**Reviewed PLAN SHA-256：** `c23762e1c552d61990e4ac62ed7d5b55663d09b9fdc22866ae8745558acfc2cf`

**FULL_PLAN_REFERENCE SHA-256：** `ad0d4bbd974d1d6c7f19e0c911f983efd23136fab8da77de0bbaae81de4e0cfc`

**EXECUTION_RESULT §128 SHA-256：** `c58e93d3256cb697c9a0aa3c7a81e5e7d49a66aaa6dca161ddc52c403a973853`

## Accepted stop facts

- Local preflight通过；HEAD/parent、PLAN/FULL/review、C1 owners/audits、release和production frozen inputs均exact；initial activation/
  package/children/ledger/PID paths均fresh；production/staged diff与owned processes为空。
- Exact activation parent被创建为regular/non-symlink/mode0700；activation原子生成且independent validator调用exactly once、findings `[]`，
  之后未重写。Activation SHA-256 `ca1121af1b306f87a159bc954b297089d8396191f91b98add6a1b15c73119af1`。
- Computer Use只尝试读取可见Terminal state；平台以`Computer Use is not allowed to use the app 'com.apple.Terminal' for safety reasons.`
  拒绝。未创建/选择tab，未typing或Return，未dispatch exact command。
- Launch ledger终态`dispatch_blocked_prelaunch`，SHA-256 `040321fdff6e4e1c5803d186b3e8dc5fbb0650898b0078e452d2f571ff9e2744`。
- Terminal/candidate launch `0/1`；PID/package/Ray/strip/paired不存在；release consumption、device/network/camera/Ray/strip/formal/
  capture/CR3/NPY/cleanup均0；retry/commit均0；无残留process。未达到cleanup条件。
- Executer没有使用AppleScript、`osascript`、Codex background、替代app或fallback launcher绕过可见Terminal合同。

## Decision

**结论：** `accepted_valid_prelaunch_infrastructure_stop`。

该结果不是formal scientific failure，也没有消耗launch或release预算。Candidate/validator/lifecycle未运行，device state未改变。平台UI
限制不能通过后台process绕过；下一合法owner只能是Human在其可见Terminal中手动dispatch exact zero-argument candidate，随后Executer只读
观察同一owned PID/package。

这不是新的危险操作授权请求。设备、light、camera和single formal package已由active scientific plan精确放行；Human只代为完成Codex系统
不能执行的可见Terminal UI动作。Firmware、deployment和破坏性硬件操作仍禁止。

## Retained artifact disposition

- Existing blocked ledger必须留在原path只读，永久分类为attempt `prelaunch-ui-policy-blocked`、launch used0/1；不得覆盖、改成started或计入
  后续launch attempt。
- Existing activation绑定已归档PLAN SHA `c23762e1...fc2cf`。Active PLAN一旦重写，该activation不再满足later-PLAN fact，不能直接复用。
- 下一package必须先把existing activation原子移动到一个exact superseded path，保持bytes/hash/mode；写disposition manifest绑定原path、retained
  path、old PLAN、blocked ledger与zero budgets。然后在canonical activation path生成绑定新active PLAN的新activation并再次独立validator。
- 新Human-dispatch ledger使用新的exact path，launch预算继承为0/1；不得把旧blocked ledger的UI read attempt记作dispatch或retry。

## Exact next branch

发布一个single Human-owned visible-Terminal action gate：Executer只执行上述离线disposition/rebind与validator，写`awaiting_human_dispatch`
ledger后停止。Human手动打开可见Terminal、粘贴并按Return一次exact inner command，再回复已启动；Human不得运行第二次。Executer收到回复后
只读确认PID/package并完成三次sparse liveness；同一PLAN继续执行原Ray→gate→conditional strip流程。

若Human未执行或command未dispatch，launch保持0/1且不访问设备；若Human报告错误或PID未出现，保留证据并停Planner，不由Codex补发。

维护性判断：失败位于平台UI权限边界，不需要修改candidate或production code；以Human-owned visible dispatch加machine-owned后续观察维持单一
execution owner且不绕过系统限制。
