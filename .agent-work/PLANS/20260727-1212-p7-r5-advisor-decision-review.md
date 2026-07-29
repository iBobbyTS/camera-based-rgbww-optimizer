# REF-P7-04 / FORMAL-R5 Advisor decision review

**归档时间：** 2026-07-27 12:12 MDT

**Reviewed reference task：** `REF-P7-04`

**Reviewed PLAN contract：** `P7-TD-B-FORMAL-R5-LOW-SIGNAL-ADVISOR-STOP`

**Reviewed PLAN SHA-256：** `e28a1d4cd8c0af5a8dd2d3bf3eb7dcbf7d6b57900b62cf99561fd42f88f09bf9`

**Reviewed starting HEAD：** `1e3b107b8fbfe97bae5624ef638c4883a0faee1d`

**Planner decision：** `accepted_as_completed_advisor_gate_and_superseded_by_guide_4`

## 1. Reviewed scope and method

本 review 验收旧 active PLAN 是否已经完成其唯一职责：封存 FORMAL-R5 hard-failure evidence、保持
设备/retry/analyzer/strip 为零，并等待 Advisor 对失败分类、retained 11、repeat、exposure、threshold、
feature、statistic 与后续锁作出科学决定。

Planner 只读交叉核对：

- `.agent-work/EXECUTION_RESULT.md` §132 terminal handoff；
- retained R5 root 的 frozen artifact path/hash；
- `advisor/4/0.AUDIT/README.md`、`04-advisor3-to-formal-r5-completed-work.md` 与
  `05-formal-r5-observer-quality-decision-request.md`；
- 新 Advisor 决策 `advisor/4/4.GUIDE.md`；
- Orchestrator-owned `.agent-work/FULL_PLAN_REFERENCE.md`。

本 review 不访问设备、网络、相机、灯光或 `.env`，不运行 public analyzer，不修改 retained root，
不执行 scientific calculation、release、test 或 commit。

## 2. Reviewed evidence

Exact immutable root：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-r5/formal-r5-1e3b107-20260726T220000Z
```

| Artifact / source | SHA-256 |
| --- | --- |
| `ray-formal/plan.json` | `94da09f240e2d0ca84ce545c52748522dfbaa9a674bf96ffcef5c8e74473ba9f` |
| `ray-formal/failure.json` | `2984ec745f2b7cddad1549535b730ae75397cdf7f1fa8602f71010f6613a9a65` |
| `ray-formal/measurements/011-ray-c-t60.patch-statistics.json` | `98b792f0ef2d89718102c054fa4c4ad43206cf3cce82855d9c67900b6223a8be` |
| `ray-formal/run.json` | `dfba25366d6deb093170ceb21ee2fa259143f0da4ba0628216de0d6f23f03079` |
| `ray-formal/physical-returns.jsonl` | `d6569f121c7a31ac1dfb427fe2de1dccc8b46fe3be6e4f3d7ba007d8019e6e02` |
| `terminal-audit.json` | `4bee490fa83bad33830cf5e8941ccc7fa0ca83191903639c617af5fe9d5e7d79` |
| `returned-summary.json` | `5e97023d84d91f0037b096bf84e1102a8b786aa174a383b65087669fb5401955` |
| `ray-formal/all-off-python.json` | `982cee95d59cc18ae1270fdc02f3c8947008796593fa22deb07f925ebd5327dc` |
| `ray-formal/all-off-shell.json` | `3c4ea47739e009cef740791e86195f8e76ec8ddb805b3a937efee75c01cf3381` |
| `.agent-work/EXECUTION_RESULT.md` at review | `cc4627828f97d41951945561bf82a22c491693eb9e894957d9964da08d4f1ff9` |
| `advisor/4/4.GUIDE.md` | `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35` |
| `.agent-work/FULL_PLAN_REFERENCE.md` | `87a0f2d87db6d1455a10dc80a3bb733ab0e475308e5b22249a4e5a9d3b68fd98` |

R5 terminal quality：

```text
launch = 1/1
retry = 0
completed / accepted formal = 11/16
returned CR3 = 12
physical total = 14 = setup 2 + returned 12
strip / paired / public analyzer = 0
Python cleanup = pass
shell cleanup = pass
terminal seal = pass
residual processes = []
```

## 3. Planner findings

1. 旧 PLAN 的等待门已经完成：Advisor 已通过 4.GUIDE 给出足以确定下一条科学分支的冻结决定。
2. R5 的准确失败不是旧 PLAN 标题中的 `low-signal`，而是
   `state_specific_exposure_policy_failure_with_required_feature_observer_saturation`：
   capture `011-ray-c-t60` 的 required `block_06/white:G1/G2` 出现非零 clipping。
3. R5 永久为 `retained_accepted_hard_failed_formal_attempt`，`formal_pass=false`；launch 已耗尽，不可
   retry、续写或在同一 root 补拍。
4. retained 11 仅可作 `diagnostic_only`，不得进入 formal inference、center、covariance、history、
   reference analysis 或与新帧 pooling。
5. observer、58 required features、clipping threshold `0.0`、near-noise、valid-pixel、nonfinite、
   covariance、joint coverage 与 no-ambient statistic 均保持冻结。
6. 允许的新方向是先完成纯离线 pre-EQ implementation，再由 Human 单独确认 EQ-R6；
   state C 只按 `1/2500`、必要时 `1/3200` 两档资格测试，随后才 finalize policy、checkpoint 与
   unique successor R3 lineage release。
7. 4.GUIDE §16 的摘要顺序与 §§4.4、5、6、14.2 冲突；Planner 采用 FULL 已记录的规范化顺序：
   pre-EQ checkpoint → Human EQ checkpoint → EQ → selected policy/checkpoint → R3 release。

## 4. Decision and validation quality

旧 `REF-P7-04` Advisor-stop 被接受为已完成并被 4.GUIDE 取代，不再可执行。该接受只关闭决策等待门，
不把 R5 判为 formal pass，不授权 release、EQ、R6、strip、TD-C 或任何设备动作。

本 review 的证据质量是 retained terminal evidence + Advisor exact decision + Orchestrator dependency map；
没有以 focused/full tests 代替科学判定，也没有声称重新运行任何测试。

## 5. Residual risks and locks

- R5 root、R2 lineage release、旧 failed roots继续 byte-immutable。
- derived R5 diagnostic 必须位于 root 外，并明确 non-authorizing/incomplete/no-pooling。
- state-C policy 在 EQ 前必须保持 `pending_qualification`、`formal_shutter=null`。
- EQ 前不得生成或消费 final successor release。
- `REF-P7-22` 及以后全部锁定；Human 尚未批准 EQ-R6 stage。
- Ray R6 16/16 acquisition + history pass 前 strip locked；combined TD-B pass 前 TD-C locked；
  sentinel、boundary、holdout、P8及以后继续锁定。

## 6. Exact next branch

Planner 将 active PLAN 重写为单一 `REF-P7-18` pure-offline pre-EQ implementation package。该 package
可顺序包含 `REF-P7-19..21` 子合同，但只有一个执行动作和一个 Planner stop：

```text
R5 immutable disposition
-> exposure-policy v2 + EQ fake runner/validator
-> full R6 validator/analyzer/locks
-> integrated offline validation
-> pre-EQ implementation checkpoint
-> Planner review stop
```

不得在本 branch 访问设备、生成/消费 release、运行真实 EQ/R6、启动 strip/TD-C 或把后续 Human checkpoint
视为已满足。

维护性判断：本归档只关闭旧 Advisor 等待门并冻结新路线，不新增生产 owner；后续实现应继续扩展现有
thermal plan、measurement、feature、analyzer 与 lifecycle owners。
