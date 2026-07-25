# P7-TD-B-F0B+FORMAL：Lineage release 与 formal dispatch 验收

**审查日期：** `2026-07-23`

**审查范围：** active `.agent-work/PLAN.md`（审查前 SHA-256
`b690d0a51e63dcbcc5ca2ae3de2800489ad467ce1605e2aedfb651e6c292d51d`）、Executer 本轮 F0B 离线
实现、lineage release、E2、Ray formal 启动失败及离线 dispatch 修复。

## 1. Executer 交付与证据

### 离线 lineage release

- 提交：`3db7ae25efab74cc800d87ac0a97aead0990ecc1`。
- release：`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release/lineage-release-20260723-170501/setup-lineage-release.json`
- release SHA-256：`e95261953aa4321ea16ba3f12451998021d9b76a0e021b5395dbb11273b9ac3c`
- schema：`p7_td_b_setup_lineage_release_v2`
- `production_release_usable=true`、`formal_cap=16`、`ambient_cap=0`、setup physical count `2`。
- public replay：`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-f0b-offline/f0b-20260723-165652/lineage-release-public-replay.json`
  （SHA-256 `cb21eb6fadf8c80cfe623ccaba5ca9722103514dafe6514c0b75a54e35f60f61`），backend connect
  为 `false`，fake production round-trip 为 pass。

### E2

- 目录：`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2/e2-20260723-171320`
- `e2-preflight.json` SHA-256：`10e7f37d67471741b64f26e6e27a0b7e9022a178ab5ee3e031e29af5dc31cd6a`
- checkpoint `3db7ae25efab74cc800d87ac0a97aead0990ecc1` 下 E2 pass。
- health/config/v2 capability、RAW/ISO 100/非空光圈、Ray readback、strip identity/MAC/generation-bearing
  全零和 Python/shell cleanup 均有证据；capture、非零灯光和新 CR3 均为 `0`。

### Ray formal 启动失败与恢复

- run：`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-ray-20260723-172000`
- wrapper-result SHA-256：`4d2590255bd21875c02ee1fc7bb2f6bfcb18a4cdae42520b82f7d101c11d769a`
- 实际结果：`child_exit_code=1`，错误为 `PermissionError: TD-B execute plan is locked until TD-A passes`；发生在
  backend 构造、command application、相机 capture、run ledger 和 Python finally 之前。
- shell cleanup SHA-256：`2f4588f6b066250d0b2defcd99223e6fe7f8a3fc94f448862aac453330dac202`，exit `0`。
- 独立 recovery zero SHA-256：`acd37f19ef2fa0a2fafdfef20b5ac0be53e27426a02e7ef2054d0064f2b5cc59`；Ray intensity `0`，strip 五通道
  全零，generation `5 -> 6`，无残留 formal 进程。
- physical CR3、formal capture 和 `.npy` 均为 `0`；因此该失败不是 partial formal data，也不启动 strip。

### 离线修复

- 修复提交：`b38caa489754b76cbab616da275517cffa403a83`，`fix(p7): dispatch lineage formal release first`。
- 修复内容：存在 exact `--setup-release` 时先 dispatch `run_resolved_td_b_formal`，不再先构造 unresolved plan；新增
  regression test `test_lineage_formal_cli_dispatches_before_unresolved_td_b_plan_gate`。
- 当前 fresh focused `unittest`：`64/64` pass。
- 当前 fresh full `unittest discover`：`545/545` pass，159.350 s。
- `git diff --check` pass；`codegraph sync` pass。
- 旧 F0B 离线日志也报告 post-fix focused/full、compileall、wrapper syntax 和 negative matrix pass，但其旧 release
  仍只属于旧 checkpoint。

## 2. Planner findings

1. 离线 F0B lineage 实现和 CLI dispatch 修复满足本轮代码/测试/负例合同，接受。
2. Ray formal 包没有达到“16 张采集 + public analysis”的完成条件；它按 PLAN 的 hard-failure stop 合法停止，不能标记为 formal 完成，也没有 paired scientific claim。
3. `setup-lineage-release.json` 绑定 `3db7ae25...`，当前 HEAD 已为 `b38caa4...`。代码 checkpoint 漂移使旧 release 不可执行，不能重试、rebind 或只修改其字段。
4. E2 证据只证明旧 release/checkpoint 下的设备前门；它不能替代新 release 的 E2，也不能证明 formal capture readiness。
5. 本轮未改变新 setup、曝光比例、timing tier、58-feature、uncertainty、covariance 或科学门；未产生新的正式 CR3。

## 3. 决定

```text
offline F0B implementation = accepted
formal attempt = accepted as valid hard failure, not complete
old lineage release = rejected for reuse because checkpoint drifted
old E2 = retained evidence, not current release acceptance
Ray formal data = none
strip formal = correctly not started
scientific claim = none
TD-C / sentinel / remaining / boundary / holdout / Gate-6 / P8 = locked
```

## 4. 残余风险

- 新 checkpoint 下尚未生成可执行 lineage release，也没有新 E2。
- remote-v2 timing、Canon recorded exposure 和 source isolation 尚未被 formal CR3 实际验证。
- Ray formal 若再次在 capture 后 report/feature/timing 失败，必须保留 physical-return ledger 并停止，不能自动重拍或启动 strip。
- 工作树中的 `.agent-work` 审计文件仍有用户/Executer dirty 状态；不得把它们误判为 production-scope clean。

## 5. 精确下一分支

`regenerate_current_lineage_release_then_rerun_e2_then_ray_only`

下一 active PLAN 只授权：在当前 `b38caa489754b76cbab616da275517cffa403a83` checkpoint，以同一旧 setup、F0A candidate 和当前
TD-B v2 plan 重新生成新的 lineage release；完成新 E2 后，在全新目录只运行 Ray TD-B formal `16 formal / 0 ambient`、public
analyzer 和独立双零。任何 offline/lineage/E2/capture/analysis/ledger/wrapper/cleanup/final-zero hard failure 立即保存证据、
双灯关闭并停止。

禁止 fresh setup、旧 release reuse、自动重试、strip formal、TD-C 或任何后续阶段。

