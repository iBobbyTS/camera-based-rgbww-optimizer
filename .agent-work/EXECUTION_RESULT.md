# Executor 执行结果

**记录日期：** 2026-07-19

**执行角色：** Executer

**输入计划：** `.agent-work/PLAN.md`

**结果状态：** `offline_contract_fixes_complete_waiting_for_planner_review`

**设备授权消费：** 无

**设备访问：** 无；未访问相机、ESPHome、Ray120c、`.env` 或 remote camera API，未调用 `all_off`

---

## 1. 已完成的离线实现

- 新增 operating-envelope v1、exact TD-A/B/C plan builder、monotonic timed scheduler、thermal/history covariate schema、future authorized runner、analyzer 和 reference-epoch v2 derived writer。
- 复用现有 `RemoteCameraBackend`、native RAW capture adapter、recorded exposure、58-feature extraction、`verified_light`、Ray exact readback 和 `turn_everything_off` owner；未复制底层设备协议。
- 共享 RAW capture adapter 新增可选 frozen shutter cache；P7-R1 已保留的 source/state shutter 可直接用于 timed cycle，Ray H120/S50 明确标为需要独立 non-formal exposure setup，未伪造 cache。
- 新增 `tmp/run-p7-thermal-diagnostics.zsh`，保留 Python finally 与 shell EXIT/INT/TERM/HUP cleanup/exit evidence 路径。
- `config/hsi/p7-operating-envelope-v1.json` 的四个 settle 字段仍全部为 `null`，cold/steady covariance merge 仍为 `prohibited`。
- R1 derived v2 固定重现：stationarity fail、raw P6 compatibility fail、interpretable compatibility not evaluable、shift class not identifiable、legacy false 不代表 no shift；原 R1 artifact 未修改。
- 临时根已改为 `/Volumes/4T/temp/rgbww-optimizer`；仓库 `tmp/*.zsh` 仅保留版本化 wrapper 源码。
- 原仓库 `tmp/` 约 16 GB、3458 files 已复制至 `/Volumes/4T/temp/rgbww-optimizer/project-tmp/WLED-RGBWW/`。

## 2. 离线输出

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics-offline/td-a-ray-dry/plan.json
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics-offline/td-a-strip-dry/plan.json
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics-offline/td-b-ray-dry/plan.json
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics-offline/td-b-strip-dry/plan.json
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics-offline/td-c-core-dry/plan.json
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics-offline/td-c-expansion-dry/plan.json
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics-offline/r1-derived/reference-epoch-analysis-v2.json
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics-offline/r1-derived/p7-r1-analysis-v2-derived.json
```

## 3. Artifact hashes

```text
p7-operating-envelope-v1.json = d553a32fdb5ad0bba1fcfc1dbee4cc2e96cc8ffa151a289de810cd55c316fc25
td-a-ray-dry/plan.json = c59fc0fb5d8264e443803d3c086b8760516017cad0a03404f4dcea48761bc736
td-a-strip-dry/plan.json = 79a583600e533bf65ae2b42a2c2dd3226bce490a707607d3640375cb2ba73f67
td-b-ray-dry/plan.json = 4f34407f321455b6835fc36782248b53c432c5ff40a1ce84d4f1906996aa5445
td-b-strip-dry/plan.json = e41ecdb86ad96475d7fef06220c53b2980331e104eacc2f5a54f66132e99fc1e
td-c-core-dry/plan.json = 64b765b24c03a2541331f5908422d6a46fa57e54dcadb81e2d9e1c7e64b817c7
td-c-expansion-dry/plan.json = 852dcefdda8fd6c47137ee3ed027c3f8455e558b3beecd7f01c04e5f1bb00466
reference-epoch-analysis-v2.json = 521e2b7a1f77815987673e3674d2a748bcaf6c880bda7a9f5c7970b2df0b285f
p7-r1-analysis-v2-derived.json = fa15ea71824b157d758872b5a28b26ac593cc610fccb4cdfb6115c5bd587e3c5
```

## 4. 验证

```text
focused required suite = 37/37 pass, 19.639 s (real 19.83 s)
full suite = 450/450 pass, 121.654 s (real 121.90 s)
compileall = pass
wrapper zsh syntax = pass
git diff --check = pass
CodeGraph sync = pass, 4 changed files / 89 nodes
offline artifact audit = pass
device/network/.env/all_off calls during offline work = 0
```

## 5. 已关闭的 Planner 分支：`P7-TD-PLAN-BRANCH-001`

TD-C core 冻结合同同时要求：

```text
sessions = 4
per session = start ambient + 2 formal source captures + end ambient
formal = 8
physical cap = 14
```

若 ambient CR3 按项目一贯 physical accounting 计数，则最低物理数量为：

```text
4 × (2 ambient + 2 formal) = 16 physical CR3
```

Planner 已冻结保留完整 ambient ledger、TD-C core cap `16`、总 physical allocation `128`。Executer 按该决定实现，未改变实验方向。

此前 Executer 未自行：

- 把 ambient 从 physical CR3 ledger 排除；
- 删除某些 session ambient；
- 合并四个 session；
- 把 cap 从 14 提高到 16 或更高。

此前请求 Planner 冻结一个分支：

1. 保留每 session start/end ambient，把 TD-C core physical cap 至少改为 16，并同步总预算；或
2. 保留 physical cap 14，明确减少/共享 ambient 的 exact session schema 和可审计理由。

该分支现已关闭，但在本轮离线实现得到 Planner 验收和新的明确授权前：

```text
TD-A device authorization request = not issued
TD-A / TD-B / TD-C execute = locked
sentinel / remaining / boundary / holdout / Gate-6 / P8 = locked
```

## 6. Git checkpoint

本轮离线收口验证完成后由 Executer 创建 focused commit；Planner `PLAN.md` 与既有 `advisor/3/` 用户材料明确排除在提交外。

---

## 7. P7 thermal diagnostics 离线合同纠偏

**执行时间：** 2026-07-19 MDT

**输入状态：** `offline_implementation_rejected_pending_contract_fixes`

**输出状态：** `offline_contract_fixes_complete_waiting_for_planner_review`

**PLAN 所有权：** 本轮未修改 `.agent-work/PLAN.md`；当前文件 SHA-256 为 `8c919d7454c2b47a91e0210247a940d28c586bc20bf35b9b50f9463c87b4f59a`，仅作为交接时快照标识。

### 7.1 已修复的六项阻塞

1. 建立 canonical ambient/formal capture ledger。TD-A 为 start/mid/end ambient + 12 formal；TD-C 每 session 为 start ambient + 2 formal + end ambient。ambient 不进入 58-feature covariance，但保留 CR3、recorded exposure、chronology、ambient diagnostic 和独立 physical accounting。
2. TD-C core 冻结为 `8 formal + 8 ambient = 16 physical CR3`；总 diagnostic allocation 为 `128`，未超过 Advisor 的 `130` 上限。
3. TD-B return anchors 和 TD-C formal 时间在依赖 artifact 未接受时保持 `requested_elapsed_s=null`，状态分别为 `deferred_until_td_a` / `deferred_until_td_b`；runner 在任何设备/backend 调用前拒绝 unresolved timing。
4. 删除 host request-start 伪 provenance。正式路径只接受 `camera_adapter_actual_exposure_start_monotonic`；当前 remote adapter 不提供该能力，因此 execute 在 backend 构造前 fail closed。
5. 建立独立 `isolation-gates.jsonl`。run start、每个 ambient 前和每个 transition 后均要求 strip generation-bearing zero snapshot 与 Ray intensity-zero readback；public analyzer 逐项按 frozen plan 重放。
6. TD-C analyzer 实现结构化 gate：paired compatibility、balanced order effect、stable center、current Ray center versus P6 interpretability、ambient trend。任一失败返回 `td_c_gate_failed`，只有全部通过才返回 `td_c_core_pass_waiting_for_planner`。

附带收口：TD-B 七个 command/return group 均冻结 transition 后双源 off/readback gate；public analyzer 同时重放 command/readback ledger 的数量、顺序、source/state owner 和 exact command hash。

### 7.2 Production round-trip 与反例

- 成功路径由正式 `execute_plan` 生成 plan/run/captures/covariates/commands/isolation/cleanup artifacts，再交给 public `analyze_thermal_run`，不使用手工 target-row 成功 fixture。
- 已验证 fail closed：缺失 ambient、重复 ambient、ambient 乱序、ambient 伪装 formal、host request-start provenance、缺失 isolation gate、Ray 非零 off readback、command ledger 缺项及 command owner 篡改。
- fake runner 路径验证 TD-A 统计为 `completed_formal=12`、`ambient_capture_count=3`、`physical_cr3_count=15`，并保留 run-start/ambient/transition gate。

### 7.3 新离线 artifacts

根目录：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics-offline-r0b
```

六个 dry-run 独立审计：

```text
TD-A ray   = 15 captures / 12 formal / 3 ambient / cap 22 / deferred 0
TD-A strip = 15 captures / 12 formal / 3 ambient / cap 22 / deferred 0
TD-B ray   = 16 captures / 16 formal / 0 ambient / cap 24 / deferred 3 / transition gates 7
TD-B strip = 16 captures / 16 formal / 0 ambient / cap 24 / deferred 3 / transition gates 7
TD-C core  = 16 captures / 8 formal / 8 ambient / cap 16 / deferred 8
TD-C expand= 16 captures / 8 formal / 8 ambient / cap 20 / deferred 8
```

SHA-256：

```text
td-a-ray-dry/plan.json       f61d397f9001fe1904e7c8f79b11a3e797a730b20c4dd14a975ea39ea40dc6ca
td-a-strip-dry/plan.json     37e7e2cb853419250af6688f604c437f003cd1416d36df1fa120e63879aef642
td-b-ray-dry/plan.json       bcb58ef28e244adf286a75c6040eb197e6a49a75918cb2f13265202ea1030e86
td-b-strip-dry/plan.json     8778190b3264343cbf2272734ff6f0137640c4ecf00c15bdc5eca348f311ce47
td-c-core-dry/plan.json      fed070fb9f250554d3c88f696eee14486388fc7f82566ac30f1d17b44175c29d
td-c-expansion-dry/plan.json c791aa76b597788fadb5cd9f366efaba265e5015ad401fc37ca2a6e89f2a5564
reference-epoch-analysis-v2.json 521e2b7a1f77815987673e3674d2a748bcaf6c880bda7a9f5c7970b2df0b285f
p7-r1-analysis-v2-derived.json   fa15ea71824b157d758872b5a28b26ac593cc610fccb4cdfb6115c5bd587e3c5
p7-operating-envelope-v1.json   d553a32fdb5ad0bba1fcfc1dbee4cc2e96cc8ffa151a289de810cd55c316fc25
```

### 7.4 验证结果

```text
thermal focused = 26/26 pass
shared-adapter focused = 68/68 pass, 13.426 s
full suite = 461/461 pass, 103.263 s
compileall = pass (pycache on external temp volume)
wrapper zsh syntax = pass
git diff --check = pass
CodeGraph sync = pass
```

最终 full-suite 的临时根、pycache 和全部新 artifacts 均位于 `/Volumes/4T/temp/rgbww-optimizer`。本轮未访问相机、ESPHome、Ray120c、remote API、网络或 `.env`，未调用 `all_off`。

### 7.5 停止点

```text
TD-A = locked pending Planner acceptance and future exact Human authorization
TD-B = locked
TD-C = locked
sentinel / remaining 9 / boundary / holdout / Gate-6 / P8 = locked
```

当前 remote camera adapter 没有真实 exposure-start provenance，因此即使 Planner 接受本轮离线代码，也不能直接进入 TD-A；需由 Planner 决定如何提供或验证 camera-adapter actual exposure-start capability，之后再另行申请精确实机授权。
