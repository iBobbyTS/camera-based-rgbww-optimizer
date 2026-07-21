# Executor 执行结果

**记录日期：** 2026-07-20

**执行角色：** Executer

**输入计划：** `.agent-work/PLAN.md`

**结果状态：** `p7_td_a_r0d_complete_waiting_for_planner_review`

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

---

## 8. Actual exposure-start adapter 离线能力核查

**Planner 输入：** `offline_contract_accepted`

**结果：** `api_capability_absent_advisor_decision_required`

**执行边界：** 仅检查本地源码、测试、部署时保留的 bridge 源码和历史 API 合同；未访问设备、网络、`.env`、remote API，未调用 capture 或 `all_off`。

### 8.1 结论

当前 remote API 没有实际曝光起点字段，因此按 PLAN branch 2 停止代码扩展并交还 Advisor。

- 本地 `RemoteCaptureResult` 只有 `saved_file`、`byte_count`、`endpoint`、`http_attempts`。
- `capture_remote_image()` 将成功响应作为纯 CR3 二进制流读取，没有 timing header 或 metadata envelope 的解析入口。
- 部署时保留的 bridge 源码成功响应只包含 CR3 bytes、`Content-Type`、`Cache-Control`、`Content-Disposition` 和长度。
- bridge 的 filename timestamp 在拍摄和下载完成后生成，不能证明 shutter/exposure start。
- 部署时 API 文档没有 exposure-start 字段、单位、时钟域或来源 hash。

因此不存在可在 client 侧“补齐解析”的已有字段。禁止使用 request-start、HTTP response time、filename time、CR3 写入/下载时间或 fake callback。

### 8.2 固化证据

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics-offline-r0b/actual-exposure-start-capability-audit.json
```

```text
SHA-256 = 0abac8e03f1ed39a6657e606edd7aff675ef04b8058f1a1f1cb123aee906cdcc
```

输入 SHA-256：

```text
camera_remote.py = 75f9647b1dd343eca9b9b1e3a6e0a77a1d41e8af56adbd6eeb615eac208844b9
retained r6_camera_bridge.py = da844a3306dcdd56ab806abcf3bae58055b3b2ab26dae48d079e68e87a4acee6
bridge rollout summary = 44736b892bf59918aa41575046263d7061fbd381faf30bf0e7115fffabed60d4
```

### 8.3 Advisor 决策请求

Advisor 需决定：

1. 修改 remote camera service，定义并输出可独立验证的 actual exposure-start provenance；或
2. 根据相机/bridge 实际可提供的证据重写 TD timing 合同。

两条路径都会改变 remote service 或测量合同，超出当前 Executer 授权。TD-A、TD-B、TD-C 及后续阶段继续锁定；不得申请设备授权。

---

## 9. P7 本地 v2 timing integration（Executor 离线收口）

**执行范围：** 仅实现并重放本地 `/v2/capture` multipart 解析、CR3/metadata hash 与 capture ID 关联、Tier A/B/C best-effort timing 重建，以及 P7 runner/analyzer round-trip。未访问设备、网络、`.env`、remote API、ESPHome、Ray120c 或相机，未调用 `all_off`。

### 9.1 交付内容

- 新增结构化 MIME parser：严格要求 JSON metadata 在前、CR3 在后，校验 boundary、Content-Length、schema、capture/request ID、MIME、byte count、SHA-256、事件时序和 timing 字段；v1 路径未改变。
- 新增原子 CR3 保存与同名 metadata sidecar；hash/byte-count/ID 不一致、部分写入和 metadata replace 失败均 fail closed 并清理 `.part`。
- `CaptureResult` 保留 `timing_metadata`、`timing_evidence` 与 `remote_metadata_path`，旧构造方式仍兼容。
- 按冻结的 wired-LAN latency-negligible 决策重建 `best_effort_gphoto2`：Tier A=`estimated_not_absolute`、Tier B=`weak_estimate`、Tier C=`unavailable`；不得把 request-start、HTTP 返回、filename 或写盘时间冒充 exposure start，结果显式 `absolute_exposure_start=false`。
- P7 runner 强制 v2 timing capability；formal capture 只接受 Tier A/B，Tier C fail closed，并持久化独立 metadata path、local receipt 与 timing evidence。
- P7 public analyzer 独立读取 metadata sidecar，重新校验 CR3 hash/ID 和 timing arithmetic，再与 runner row 对照；输出 timing source、tier distribution、unknown count 和 `timing_absolute_truth=false`。
- 更新项目 README 与 camera skill，记录 v2 adapter、证据边界和 best-effort 语义。

### 9.2 验证

```text
focused = 70/70 pass (0.200 s)
full suite = 467/467 pass (101.358 s, log: /Volumes/4T/temp/rgbww-optimizer/full-v2-final.log)
compileall = pass (PYTHONPYCACHEPREFIX=/Volumes/4T/temp/rgbww-optimizer/pycache-v2-final)
wrapper zsh syntax = pass
git diff --check = pass
CodeGraph sync = pass (7 changed files)
```

测试覆盖包括 multipart 顺序/schema/hash/ID 篡改、Content-Length 与原子清理边界、Tier A/C timing、v2 文件保存、P7 runner/analyzer 独立 sidecar round-trip，以及篡改 row/metadata 的拒绝路径。

### 9.3 停止点与 Planner 请求

```text
status = local_v2_timing_integration_complete_waiting_for_planner
TD-A / TD-B / TD-C = locked
P7-R1 / sentinel / remaining 9 / boundary / holdout / Gate-6 / P8 = locked
```

本轮只证明本地 producer/consumer 的离线证据合同闭环；没有证明 remote service 已部署或设备端能提供真实 exposure-start provenance。请 Planner 验收本地实现，并决定是否另行授权 remote service 变更或新的实机阶段。不得将本轮结果解释为设备授权或 TD-A 放行。

---

## 10. P7-LV2-R0C 第二轮离线纠偏

**当前状态：** `local_v2_timing_r0c_complete_waiting_for_planner`

本节是对 Planner 针对 `cb9db30` 的部分验收结论的追加记录；历史章节保留，不把旧的“严格 Content-Length/strict schema”描述当作当前状态。

### 10.1 已修复

- `run_authorized_plan()` 现在第一步执行无副作用的 exact-plan/Human/v2/backend-owner validator；失败时不 import/construct/connect backend，不创建 run 目录，不触发灯光或 cleanup。legacy `exposure_start_capability` 仅保留为 deprecated dry-run 标记，不能满足 production v2 eligibility。
- CLI 在 backend 构造前要求 exact Human authorization、`remote` backend 和正式 v2 capability；支持注入 fake backend/runner 的离线 round-trip，local backend、缺失 v2、deferred、伪造 status 均 fail closed。
- v2 response 强制 HTTP 200、`Content-Length` 精确匹配、`X-Capture-ID`、`X-Request-ID`、`X-Capture-Metadata-Schema`；JSON/CR3 part 强制固定 Content-ID、Content-Disposition/name 和顺序。
- remote metadata 改为递归 strict allowlist；未知字段、remote path、camera serial、敏感 provenance 不会进入 sidecar；`network_observation.request_id` 必须等于顶层 request ID。
- 每个 busy retry attempt 单独记录 local request-start；sidecar 保留总 attempts、successful attempt index、成功 attempt 的本地 response/header/parser receipt。所有 attempts 失败时不保存 CR3/metadata。
- public analyzer 重新验证 response headers、schema header、parser version、successful attempt timing、sidecar owner/path、CR3 hash/byte count，并要求 capture row 中的 duplicate timing metadata 与 sidecar 精确一致。

### 10.2 新增回归覆盖

```text
focused = 77/77 pass
```

新增反例包含：缺少四类 response header、network request ID drift、unknown sensitive metadata、part Content-ID drift、busy retry successful-attempt clock、all-busy no-artifact、legacy capability impersonation、authorization-before-connect、deferred/local backend/forged status、analyzer header/parser/attempt/owner tampering。

### 10.3 离线 validation artifacts

生成器：

```text
camera_based_rgbww_optimizer.optimization.validate_p7_local_v2_timing
```

目标根目录：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-local-v2-timing-offline/p7-lv2-r0c-<timestamp>/
```

包含 `plan.json`、valid fake response/CR3/metadata、malformed response fixtures、
`timing-reconstruction.json`、`production-roundtrip-analysis.json` 和
`validation-summary.json`。全部 fixture 仅使用假 CR3 bytes；计数固定为
`device=0, network=0, env=0, all_off=0`。

本轮最终 artifact：

```text
root = /Volumes/4T/temp/rgbww-optimizer/p7-local-v2-timing-offline/p7-lv2-r0c-20260720-095000/
validation-summary.json SHA-256 = 8ddab5eface59100c3f59e70ce26b505fbb9c375da4470dd97ba09b1b02c4b14
production-roundtrip-analysis.json SHA-256 = 3fcb86ffbc469aba1a08cf04c0304683b1fff782f8ab25f55672257b4f142699
implementation commit = 8689da7 fix(p7): harden local v2 timing evidence
artifact-generation commit = f788b8d docs(p7): record r0c validation evidence
```

artifact `validation_results` 为 focused `78/78`、full `475/475`（`105.313s`）、
compileall/wrapper/diff/CodeGraph 全部 `pass`；每个 required negative fixture 的实际结果均为 `reject`。

TD-A、TD-B、TD-C、P7-R1、sentinel、remaining 9、boundary、holdout、Gate-6 和 P8 继续锁定；本轮不包含任何设备、网络、`.env`、remote API 或 `all_off` 调用。

---

## 11. TD-A 授权后离线进入门

**结果状态：** `td_a_offline_entry_rejected_pending_runner_contract_fix`

**授权消费：** 已确认 PLAN 记录 Human 于 `2026-07-20T16:04:40Z` 对 exact
`p7_td_a_cold_settling_v1` 的一次性授权；未重复询问。由于离线进入门失败，本节没有消费任何
设备调用、实拍或灯光预算。

### 11.1 已通过检查

- HEAD `c1c273a` 包含 PLAN 冻结的 local-v2 accepted commits。
- Advisor GUIDE/RESEARCH、location、Ray manifold、operating envelope、两份归档、R1 command
  ledger 和 local-v2 validation-summary 的 SHA-256 全部与 PLAN 一致。
- operating-envelope 的 `t_settle_ray_s`、`t_settle_strip_s`、
  `t_formal_provisional_s`、`t_formal_s` 仍全部为 `null`。
- 两个全新且不同的 dry-run 已生成：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-ray-dry-20260720-101500/plan.json
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-strip-dry-20260720-101500/plan.json
```

- 两个 plan 都冻结为 TD-A、3 cycles、`60/120/300/600`、12 formal、3 ambient、physical cap
  22、remote backend、`best_effort_gphoto2_v1`、双 cleanup；Ray command 为
  `H120/S100/INT100`，strip command 为 `518,0,0,4095,0`。source-specific retained shutter
  分别为 Ray `1/5000`、strip `1/320`。
- `tmp/run-p7-thermal-diagnostics.zsh` syntax 和 `git diff --check` 通过。

### 11.2 阻塞问题

1. 两个 TD-A dry plan 均自报：

```json
{"exposure_setup_required":["ray-h120-s50"]}
```

该 key 只属于未来 TD-B；当前 TD-A 的 Ray/strip source-specific shutter 均已存在。这个全局字段使
TD-A plan 看起来仍需未授权 exposure setup，违反“本次无额外 light-on exposure setup”的证据语义。

2. production runner 在
`measure_p7_thermal_diagnostics.run_authorized_plan()` 构造 native capture adapter 时显式传入：

```text
iso=None
aperture=None
```

adapter 的 ambient/fixed path 直接构造 `CaptureSettings`，不会先调用 remote backend 的
`resolve_capture_settings()`。纯离线 fake probe 已重现：

```text
CaptureSettings = {iso: None, aperture: None, shutter_speed: "30", image_format: "RAW"}
/v2/capture payload = {iso: null, aperture: null, shutter_speed: "30"}
```

归档 remote API 要求 `iso`、`aperture` 和 `shutter_speed` 若出现就必须是当前 config choice 的精确
字符串；因此当前正式路径会在首张 ambient 返回 `invalid_iso`/`invalid_aperture`，不能启动已知必败
实机 run。

### 11.3 Planner 决策请求

请 Planner 定义一个纯离线 TD-A runner 修复包，至少要求：

- 正式 remote backend 在任何 capture/灯光前解析一次 ISO/aperture，并把精确字符串注入全部
  ambient/formal timed capture；不得硬编码 `4` 或把 `null` 发给 remote API；
- remote config 解析失败时在灯光和 run directory 副作用前 fail closed；
- `exposure_setup_required` 只列当前 experiment/source 实际使用且缺失的 shutter key，TD-A 必须为空；
- 增加 production runner -> timed capture fake round-trip，断言 ambient `30` 与 Ray/strip retained
  shutter 都携带合法 ISO/aperture 字符串，并断言零 auto-exposure；
- 验证修复后重新生成两个新 dry-run，再决定是否继续消费现有一次性 TD-A 授权。

本轮精确计数：

```text
device = 0
network = 0
.env = 0
remote API = 0
camera = 0
Ray = 0
ESPHome = 0
all_off = 0
formal capture = 0
physical CR3 = 0
```

TD-A 未开始，Ray/strip 实机目录、wrapper PID、Terminal task 和 heartbeat 均未创建。TD-B、TD-C、
sentinel、remaining 9、boundary、holdout、Gate-6、P8、firmware 和 remote deployment 继续锁定。

---

## 12. P7-TD-A-R0D 离线 runner settings/shutter 修复

**Planner 输入状态：** `td_a_authorized_blocked_pending_r0d_offline_runner_fix`

**执行结果：** `p7_td_a_r0d_complete_waiting_for_planner_review`

**PLAN 所有权：** 本轮未修改 `.agent-work/PLAN.md`；执行时只读快照 SHA-256 为
`37a78f16aef8d6fa8120277ff2a35742ac870fe1a80e5900b82ed59e336a6371`。

**实现提交：** `3cbc72a fix(p7): bind thermal capture settings`

### 12.1 已闭合的 production contract

- plan builder 先生成 exact experiment/source capture steps，再由单一 step-to-shutter owner 反推
  shutter ledger。TD-A Ray 仅保留 `ray-h120-s100=1/5000`，TD-A strip 仅保留
  `strip-h120-s100-fullscale=1/320`；两者 `exposure_setup_required=[]`，均不含 TD-B-only
  `ray-h120-s50`。
- TD-B Ray dry contract 仍保留 `ray-h120-s50=null` 与显式 non-formal setup requirement；TD-B
  strip 四个正式 state shutter 均保留，没有破坏 future contract。
- production validator 从 capture steps 独立重算 exact shutter keys、ledger hash 和 setup list；
  缺失/空 shutter、extra TD-B key、owner/hash drift 均在 backend connect 前拒绝。
- runner 在 formal remote backend connect 后只调用一次
  `resolve_capture_settings(iso=None, aperture=None, image_format="RAW")`。空值、非字符串、
  non-RAW 或 backend choice failure 在 run directory、灯光、capture 和 cleanup 副作用前拒绝。
- 已解析 ISO/aperture/RAW 写入 plan/run provenance，并注入 ambient、fixed cached 和 timed capture。
  public analyzer 逐张重放 capture settings，拒绝 plan/run 与实际 CR3 capture row 不一致。

### 12.2 Fake-only binding round-trip

fake backend 对 Ray/strip 各执行一次 production runner binding；没有构造 network client：

```text
resolve_capture_settings calls = 1 per source run
synthetic ISO = 125
synthetic aperture = implicit auto
image format = RAW
ambient shutter = 30
Ray formal shutter = 1/5000
strip formal shutter = 1/320
auto_exposure = false for every observed raw step
null ISO/aperture = 0
```

ISO/aperture 是 synthetic choices，仅证明绑定和 analyzer replay，不是设备或 remote config 观测。
反例覆盖 resolver failure、null ISO、empty aperture、non-RAW、remote current 不属于 choices、
shutter 缺失和 TD-B key 污染。

### 12.3 全新 TD-A dry-run artifacts

根目录：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-r0d-20260720-122701
```

```text
ray-dry/plan.json
SHA-256 = 37e0cc9ce14b0b3d95edc6cbc406b870393743bc4763e7b752067efbf786c4f2

strip-dry/plan.json
SHA-256 = 20aad47e315ce71b1d87399e0e0556b58be1eb36b0f45fe60298d135dd4b54be

validation-summary.json
SHA-256 = 4e0c256677ef25a4c39d57462a0c63862eac8b6e72876bcb1ed8fcd149cc3b4a
```

两份 plan 均为 TD-A、3 cycles、`60/120/300/600`、12 formal、3 ambient、physical cap 22、
timed-cycle auto exposure false、`exposure_setup_required=[]`。递归搜索确认 artifacts 中不存在
`ray-h120-s50`、`"iso": null` 或 `"aperture": null`。

冻结输入 SHA-256：

```text
code-duty curve = 0b03ce50bda13112c95d64d1f5974991514067bbd9f48e920214654c122ff911
location = 21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80
Ray manifold = 20baaa26679039590679a122a5b4d2e658eae867c63e98d0a5d0556a2dc3bc34
RAW observer = b81d563eba1910286d879e560538dd497385e422c1bab762008c2b28a26fc4d9
operating envelope = d553a32fdb5ad0bba1fcfc1dbee4cc2e96cc8ffa151a289de810cd55c316fc25
P7 v2 policy = db9ebef1503c5e54c989649c719c4a5f75445bbd5487edb14c274e1b2894f3b4
R1 commands = 2d0667d235bffff9119eea54e76d76ed1914f246fec64903f2dd1a9b675b4ca3
R1 plan = 55c25a4b51d4a247e1888f3d6a075dea313f3dadc3e5e8435e53c419131a1c2e
P7 uncertainty = cedaa1e9d342beb7e464c4e38d77884ad8a7790771432ebdbb5a101ca604aa94
```

### 12.4 最终验证

```text
focused = 83/83 pass, 0.527 s
focused log SHA-256 = 9d9ee0b0eec32e1b0e1f4d34cfd06daaac63284c9e54d221b953ce2390fd620a
full suite = 480/480 pass, 145.348 s
full log SHA-256 = c2a69cb4d24c2dbb01c797b116bb213bc6b8f763b24183a8c2bd63bd226ab1b0
compileall = pass
all tmp/*.zsh syntax = pass
git diff --check = pass
CodeGraph sync = pass
```

所有 test temp、pycache、logs 和 dry artifacts 均位于
`/Volumes/4T/temp/rgbww-optimizer`。

### 12.5 零设备计数与停止点

```text
device = 0
network = 0
.env = 0
remote API = 0
camera = 0
Ray = 0
ESPHome = 0
all_off = 0
CR3 = 0
formal capture = 0
physical CR3 = 0
```

Human 的 exact TD-A 一次性授权未被消费；TD-A Ray/strip 实机 run、wrapper、PID、Terminal task
和 heartbeat 均未创建。R0D 按计划停在 Planner 验收门；不得自动进入 TD-A、TD-B、TD-C、
sentinel、remaining 9、boundary、holdout、Gate-6 或 P8。

## 13. P7 TD-A E0 production completion gate

**执行结果：** `td_a_e0_pass_continuing_to_authorized_device_entry`

**PLAN 所有权：** 本轮未修改 `.agent-work/PLAN.md`；E0 执行时只读 SHA-256 为
`805053e7dafb42f16f896e1b1d68d76c9d66be222676bd97a51f0a3b1b925e47`。

**实现提交：** `d5cc596521f938c4f353a7d7a498f6f7be6453f8 feat(p7): finalize td-a completion evidence`

### 13.1 单源 completion evidence replay

- `analyze_p7_thermal_diagnostics` 现在解析 `all-off-python.json`，要求 exact ESPHome/Ray 两步均
  `ok=true`、无 error 且 detail 可审计；解析 shell `all_off --json` 的 exact 两步结果。
- 独立要求 `run.json.cleanup=pass`，并重放 `wrapper-result.json` 的 schema、run owner、child/shell/
  wrapper exit `0`、signal `null` 与正 PID。
- 独立要求 `child-exit-status.txt=0`、`all-off-shell.exit-status.txt=0`；缺失、空 JSON、非零、
  schema drift 或任一灯 cleanup 未知均 fail closed。
- 单源报告新增 `source_id`、`cleanup_contract=pass`、`wrapper_contract=pass`，因此 analyzer 在 shell
  wrapper 完整退出前不能产出通过结果。

### 13.2 双源 TD-A finalizer

- 同一 analyzer module 新增 `analyze_td_a_pair(ray_run, strip_run, output_dir, feature_ids=...)` 和 CLI
  `--paired-run STRIP_RUN --combined-output OUTPUT_DIR`，没有建立第二套 analyzer。
- finalizer 对两个 run 重新执行完整单源 replay，要求 positional Ray owner + paired strip owner、exact
  TD-A、相同 frozen input path/hash 与 timing contract。
- 每源要求 12 formal、3 ambient、physical `<=22`、Tier A/B、零 NPY、capture/timing/covariate/
  isolation/cleanup/wrapper 全 pass；合计要求 24 formal、6 ambient、physical `<=44`。
- 双源 settle 均存在时写 `td_a_pass` 和 `max(ray,strip)`；任一合法 non-settle 时写
  `settling_not_demonstrated_by_600` 且 provisional 为 `null`。600 仍为 validation-only。
- 原子写入新的 `td-a-combined-analysis.json` 与 `EXPERIMENT_SUMMARY.md`；未生成或覆盖默认
  `config/hsi/p7-operating-envelope-v1.json`。

### 13.3 验证

验证根目录：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-a-e0
```

```text
focused = 67/67 pass, 1.085 s
focused log SHA-256 = b11bfb8d723a4b5b7f79e53a7958d7504d9ae9be754f68aa824dd3b03e5c9e4b
full suite = 486/486 pass, 110.772 s
full log SHA-256 = 1031580bd1663c93627f73251fe61f4f9b37221edb8837a4bec2a6634de8496f
compileall = pass
all tmp/*.zsh syntax = pass
git diff --check = pass
CodeGraph sync = pass / already up to date
```

`validation-summary.json` 位于上述目录；默认 operating envelope SHA-256 仍为
`d553a32fdb5ad0bba1fcfc1dbee4cc2e96cc8ffa151a289de810cd55c316fc25`。

### 13.4 E0 零设备计数与连续推进

```text
device = 0
network = 0
.env = 0
remote API = 0
camera = 0
Ray = 0
ESPHome = 0
all_off = 0
CR3 = 0
```

E0 已满足 active PLAN 第 5 节，按计划不在此交回 Planner；下一步直接执行第 6 节实机前离线进入门，
再消费 PLAN 已记录的 exact Human TD-A 授权。TD-B/C、sentinel、remaining、boundary、holdout、P8、
firmware 和 remote deployment 继续锁定。

## 14. TD-A 实机进入与 Ray wrapper hard-invalid

**执行结果：** `TD-A-RAY-HARD-INVALID / blocked_for_planner_review`

**PLAN 所有权：** 本轮未修改 `.agent-work/PLAN.md`。

### 14.1 第 6 节离线进入门

全部 accepted commit、三份 Planner 归档、第 3 节 frozen input、R1 retained plan/commands 与 R0D
validation hash 均一致；operating-envelope 四个 settle 字段仍为 `null`。

离线进入根目录：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-entry-20260721-040137
```

```text
ray dry plan SHA-256   = 779c39152fa4b34e957c85403f4671195aafd350e1795d2367f477457a682d0f
strip dry plan SHA-256 = 05e791f97cbd032bea087c9398f6c61cb539b4305edfcba81f0162bf1b6cc6dc
offline-entry.json SHA-256 = 0eafb358b69936390e65535aba9ebfcf51572345f01161a42a7952362085ca2f
focused entry = 67/67 pass
```

两个 dry plan 均为 exact TD-A、3 cycles、`60/120/300/600`、12 formal、3 ambient、cap 22；
Ray shutter 为 `1/5000`、strip 为 `1/320`；`exposure_setup_required=[]`，无 `ray-h120-s50`，
timed-cycle auto-exposure false。计划中的两个实机路径在进入时均不存在。

### 14.2 实机 preflight

未发现其他 calibration、gphoto2、相机、Ray、ESPHome 或 thermal wrapper process。随后按 PLAN 消费
既有 Human 授权执行 preflight：

```text
remote health = pass
remote v2 capability = remote_v2_capture_timing_v1
resolved ISO/aperture/format = 100 / implicit auto / RAW
Ray before/off readback = reachable, final intensity 0
strip identity = bedroom-rgbww-strip / E0:8C:FE:63:C9:40
strip generation = 2 -> 3
strip five channels = all zero
Python cleanup = pass
shell cleanup exit = 0 / pass
capture = 0
nonzero probe = 0
```

```text
device-preflight.json SHA-256 = d9cfe1183233084f1dbbad932dfb82da9d066a1693962f05f8b7bd6cd6d0b57c
preflight Python cleanup SHA-256 = 5b73d5c1ef2442ca276651eecff35925b58c49eeb910064e82c34f0d946577ec
preflight shell cleanup SHA-256 = 6a70ab3d3bc51d12c14e3b2ac3270c29d78683445a920e68309817dc6755d2a5
```

### 14.3 Ray wrapper runtime failure

Ray 通过 OS-owned Terminal 启动：

```text
Terminal window id = 164034
tab = 1
TTY = ttys002
wrapper PID = 84031
child PID = 84267
run dir = /Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-ray-20260721-040137
started_at = 2026-07-21T04:07:38.770885+00:00
```

正式 wrapper 在 child 启动后第一次写 `wrapper-state.json` 时失败：

```text
write_json:2: read-only variable: status
```

根因是 `tmp/run-p7-thermal-diagnostics.zsh` 的 `write_json()` 使用 `local status=...`；`status` 是
zsh 只读特殊变量。`set -e` 使 wrapper 进入 EXIT finalizer 并等待 child，finalizer 后续同样使用
`local ... status`，因此 completion evidence 必然再次失败：

```text
finalize:12: read-only variable: status
```

该问题未被 E0 的 `zsh -n` 和静态 wrapper-source assertions 触发；正式 runtime round-trip 并未在
active PLAN E0 fixture 中执行。

发现时 child 仍在第一次 `cold_proxy_wait_s=1800`，尚未发出非零 command 或 capture。Executor 对已
核对 PID 的 child 发送 TERM；结果：

```text
child exit = 143
formal = 0
ambient = 0
physical CR3 = 0
commands = 0
captures = 0
runner log = empty
strip run = not created
automatic retry = false
```

wrapper 的 shell cleanup 仍执行成功：`all-off-shell.exit-status.txt=0`，ESPHome/Ray 两步均
`ok=true`。由于 Python 被 TERM 且 wrapper completion writer 已损坏，本 run 按预期缺少
`all-off-python.json`、`wrapper-result.json` 和 `wrapper-state.json`，`run.json` 保留
`status=running / cleanup=pending`，不能被 analyzer 接受。

### 14.4 独立 recovery 与保留证据

Executor 在 child/wrapper 均退出后调用独立 recovery all-off，并再次做 generation-bearing readback：

```text
recovery status = pass
strip generation = 10 -> 11
strip five channels = all zero
strip identity = bedroom-rgbww-strip / E0:8C:FE:63:C9:40
Ray = CCT 5600 / GM 100 / intensity 0
```

```text
recovery-all-off.json SHA-256 = 98f083771475c80b09465e82ee7fe01ab0a5bc999e5b8397ed01108327d28c8f
wrapper log SHA-256 = bc0e618f19ed2a1cc0956e3efb1bf7ce6bfb7d0e5a898deb0ae69e9f201552ad
shell cleanup SHA-256 = e41c9caa98137b314a88d55a1ec276aca40044e00a350c7f39b46fd236179391
Ray plan SHA-256 = dcbbc250f4a48311ebabbb4ff0b4ec5c77d1631708d49eaa522fc447d2d78f77
Ray run SHA-256 = 37f2b0e02e47f06e39fe1d69c6b4b72aa14a74dcf934e713b7b5624b195f2eed
Ray isolation SHA-256 = 6391db7b3be69b3a4119a4773d644549fe6e50b318252f6fdc65db08c031baea
```

汇总 artifact：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/
  p7-td-a-entry-20260721-040137/ray-hard-invalid-summary.json
```

### 14.5 Planner 决策请求

按 active PLAN 第 8.3/12 节，Ray wrapper hard-invalid 后不得启动 strip、不得自动 retry。本轮已停止。
需要 Planner：

1. 归档此 zero-capture Ray valid-failure；
2. 授权一个纯离线 wrapper runtime fix，至少把两个 `status` local 改为非保留名，并增加真实 zsh
   runtime success/failure round-trip，不能只保留 `zsh -n`；
3. 明确本次已执行 preflight 且创建正式 Ray run/child、但无非零 command/capture 的失败，是否已消费
   Human 的一次性 TD-A run authorization；若允许修复后重试，必须在新 PLAN 中明确写出，不由
   Executor自行解释；
4. 在 Planner 新决定前继续锁定 strip TD-A、paired finalizer、TD-B/C、sentinel、remaining、
   boundary、holdout、Gate-6、P8、firmware 和 remote deployment。

## 15. P7 TD-A W0 wrapper runtime 离线纠偏

**执行结果：** `W0-PASS / waiting_for_Planner_review`

**实现提交：**
`960484e1107cbcfb3304075a5ac54a0fbe6a382e fix(p7): close td-a wrapper evidence gaps`

**PLAN 所有权：** Executor 未修改 `.agent-work/PLAN.md`；执行前后 SHA-256 均为
`249774c7924b40d4dcc72d5b01b0ab84e14ae7a5a4d101117a969405fa4e4dea`。

### 15.1 W0-001 production wrapper runtime

- `write_json()` 的 zsh 只读特殊参数 `status` 已改为 `result_status`；
- `finalize()` 的 `status` 已改为 `final_status`；
- 同一 wrapper 的全部 `local` 名称已对 zsh readonly/special parameter 集合审计，无命中；
- production wrapper SHA-256：
  `4f776135b18df57897011d6c37f7683768d772cd5a9ee7f73c07f2ffae0d7dfb`；
- 测试逐 case 复制 production wrapper exact bytes 到 fake project，再运行真实 `zsh`；runner 与
  cleanup 每条路径均恰好调用一次，final state 均为 `finished`，没有临时文件或残留进程。

| case | child | cleanup | wrapper | status | signal |
| --- | ---: | ---: | ---: | --- | --- |
| success | 0 | 0 | 0 | `complete` | `null` |
| child failure | 7 | 0 | 7 | `child_failed` | `null` |
| cleanup failure | 0 | 9 | 70 | `cleanup_failed` | `null` |
| INT | 130 | 0 | 130 | `signaled` | `INT` |
| TERM | 143 | 0 | 143 | `signaled` | `TERM` |
| HUP | 129 | 0 | 129 | `signaled` | `HUP` |

保留 fake runtime evidence：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-a-w0-offline/
  p7-td-a-w0-20260721-054106/runtime-cases
```

### 15.2 W0-002 paired input manifest

- `analyze_td_a_pair()` 现在要求调用者显式提供 `code_checkpoint` 与实际 `feature_ids_path`；
- paired CLI 新增必填 `--code-checkpoint`，成功时打印 combined analysis、summary、manifest 三个路径；
- 新 schema 为 `p7_td_a_input_manifest_v1`，decision owner 固定为 `Planner`；
- manifest 从 retained bytes 重算 Ray/strip plan/run、feature policy、combined analysis 与 summary hash；
- feature file 必须同时是两源 plan 的 frozen policy input，不能用另一个有效 feature 文件替换；
- 同一 analyzer module 的 `validate_td_a_input_manifest()` 独立重放 exact schema、source owner、绝对路径、
  plan/run/hash、frozen inputs、timing、feature policy 与 output owner；finalizer 返回前重载验证；
- 已覆盖未知/缺失 key、空/非法 checkpoint、hash 单字符漂移、source 颠倒/重复、plan/run/feature/output
  byte tamper、existing output 与 manifest 写入失败；single-run CLI 不要求 checkpoint；
- 成功和失败路径均保持默认 operating envelope byte-identical：
  `d553a32fdb5ad0bba1fcfc1dbee4cc2e96cc8ffa151a289de810cd55c316fc25`。

保留 fake pair：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-a-w0-offline/
  p7-td-a-w0-20260721-054106/manifest-fake-pair

td-a-combined-analysis.json sha256 = 8c52890727f0b7bbb5108a0e0bcae8c474b57984610d00c2e419b08b8bdc6cd6
EXPERIMENT_SUMMARY.md sha256 = 259c0faa95553103b719598e84c1d6e992b5042b9e78dd0d901d66cf8fd2c116
input-manifest.json sha256 = 1b7bc3bf45e3d2a598aece551f0ccb243c9c057df9f0c1934e2611eb1ffdf16e
```

### 15.3 验证与副作用

```text
focused = 48/48 pass, 4.299 s
focused log sha256 = a371201fc424ec44c6da3f9ef5b4c26a225f996304d85d15f717c6af65296ba8
full suite = 493/493 pass, 111.405 s
full log sha256 = 1da49246f4796e193faa4884250df50e626312076e839d892b242a1b0dbd0bbd
compileall = pass
all tmp/*.zsh syntax = pass
git diff --check = pass
CodeGraph sync = pass / already up to date
residual fake process = 0
```

Validation summary：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-a-w0-offline/
  p7-td-a-w0-20260721-054106/validation-summary.json
sha256 = 94ce883c689fed4dc43f1ce1db0396fe41f11846d167604fa9cc8a6c017647af
```

```text
device = 0
network = 0
.env = 0
remote API = 0
camera = 0
Ray = 0
ESPHome = 0
real all_off = 0
real CR3 capture = 0
real run directory = 0
heartbeat = 0
```

Analyzer replay 使用 `30` 个仅含 `b"raw"` 的 3-byte synthetic `.CR3` fixture；它们位于上述 fake
pair，未由相机产生，不属于实拍 CR3。零 `.npy` 被保留。

### 15.4 授权与停止点

```text
p7_td_a_cold_settling_v1 authorization = not_consumed_but_suspended
TD-A retry = not performed
TD-B / TD-C / sentinel / remaining / boundary / holdout / Gate-6 / P8 = locked
```

已到达 active PLAN 唯一 Planner stop。下一步仅允许 Planner 验收；Executor 不执行 preflight、Ray、
strip、capture、`all_off` probe 或 TD-A retry。
