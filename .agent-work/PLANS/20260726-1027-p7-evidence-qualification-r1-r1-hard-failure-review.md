# P7 evidence-only qualification R1-R1 hard-failure review

**Review 时间：** 2026-07-26

**Reviewed PLAN SHA-256：** `aa3fc4d86cc323da7a8765baebad5ff3060f73bcf6283435e627cc485accdb7b`

**Reference task：** `REF-P7-04`

**Decision：** `rejected_unique_run_consumed_offline_correction_required`

## 1. Run facts

Preflight passed and the sole evidence-only invocation was launched; budget is consumed `1/1` and may not be retried.
Child produced exactly one evidence artifact:

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-evidence-qualification-r1-r1/20260726T102400Z/output/evidence-r1-r1/qualification-evidence.json`

Bytes `5212`，SHA-256 `16658e497fab1246deb88a3d75dbc5c3edf311c28a49624de22a8ca79fce504c`；schema/status、17 references、
empty mismatch/prohibited 与 all-zero side-effect budgets 均通过。Output evidence 自身不含 banned
release/formal/device/readiness/consumer claims。

Stdout SHA-256 `df8869aa17d6fe4cbacd6b2ec6d17c795f58dc9c965eceb27ecbb4936f47116e`；stderr empty SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。Post-audit SHA-256
`f70f1967900561625654a8fbcd2980ff525e79103c1398c4ce293844180637a9`；canonical 23 before/after exact、
cached index empty、residual processes empty、release/live/device budgets 0。

## 2. Rejection findings

### REV-P7-R1-R1-EXIT-ACCOUNTING-001 — open

Wrapper 在 child 返回后执行 zsh `status=$?`；`status` 为只读变量，赋值使 wrapper exit 1。Child exit 未在该赋值前
持久化，post-audit `child_exit=null`、owner 为 `not_persisted_due_zsh_readonly_status_assignment`。因此 wrapper exit、
stdout/evidence presence 均不能推导 child exit 0；本 run 不可接受为 qualification evidence success。

### REV-P7-R1-R1-SCAN-SCOPE-002 — open

Whole-root negative scan 唯一命中
`preflight-before.json` 中 canonical retained historical path `setup-lineage-release.json`。Output evidence 自身 clean。
当前 scan 将“输入 provenance 对历史 retained release 的允许路径引用”与“新输出产生 release-like claim/artifact”混为
同一 scope，产生 false positive；但不能简单全局 allow 该字符串。

## 3. Decision and next branch

R1-R1 **拒绝**；唯一 run 已消费，严禁重试。Generated evidence 作为 retained failure evidence 保留，不得改写、移动、
删除或升级为 accepted qualification result。

下一唯一包：`P7-TD-B-RAY-PUBLIC-DEFAULT-LINEAGE-EVIDENCE-QUALIFICATION-R1-R1-C1-OFFLINE-ACCOUNTING-SCAN`。
只创建外部 corrected harness contract/fake matrix：child exit 使用非只读 `child_rc` 并在任何 post-processing 前独立持久化；
wrapper status 与 child status 分开；scan 分 output strict scope、wrapper metadata scope、input-provenance scope，historical
release path 只在 exact retained reference schema/path/hash 下允许。不得再调用 evidence adapter、生成/消费 release、修改
production/tests 或进入 live/device。

Human“暂时不得启动灯、相机或任何设备测试”继续冻结。本 review 使用 FULL SHA-256
`626b7647fffd3c972050378ae3a7ab419784fa95dd201408d85861098076db0b`。

维护性判断：失败位于外置 shell accounting 与 scan oracle，不是 production evidence serializer；用单一外置 harness
contract与protective fake matrix纠偏即可，无需修改 production 架构。
