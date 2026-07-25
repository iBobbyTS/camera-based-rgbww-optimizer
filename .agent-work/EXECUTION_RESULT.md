# Executor 执行结果

**记录日期：** 2026-07-23

**执行角色：** Executer

**输入计划：** `.agent-work/PLAN.md`

**结果状态：** `p7_td_b_f0a_offline_pass_waiting_for_planner`

**设备授权消费：** F0A 为纯离线纠偏，不消费也不恢复任何设备授权

**设备访问：** 本轮设备、网络、`.env`、相机、Ray、ESPHome、灯光与 `all_off` 调用均为 0

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

## 16. P7 TD-A Cold Settling 授权执行（进行中）

**当前结果：** `ray_run_running_waiting_for_sparse_heartbeat`

**PLAN 所有权：** Executor 未修改 `.agent-work/PLAN.md`；本轮只读 SHA-256 为
`f3df0e06b45de7fa254cae7e3313f17e85afc30ae01dfae94e93f01291a42ff0`。

### 16.1 离线进入门

```text
entry = /Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-entry-20260721-150200
offline-entry.json sha256 = 84fe544f891d30494ee3304dfca31c0d108d59f6fe93bb42d4d40631f9218cd5
ray dry plan sha256 = 1a9874bde3c94afb4c0e1fb2b60179353ccbb4b6bf0c7928abb171f9487f5fe3
strip dry plan sha256 = ec01fff713eac4480493a92a0b459d7ac96655b7ab34949f8b9017be9bc99b76
focused thermal = 48/48 pass
wrapper syntax = pass
git diff --check = pass
```

- accepted commits `3cbc72a`、`d5cc596`、`960484e`、`1c592c9` 均存在；
- production wrapper SHA-256 为
  `4f776135b18df57897011d6c37f7683768d772cd5a9ee7f73c07f2ffae0d7dfb`；
- frozen input hash、R1 retained plan/commands、W0 validation 和 operating-envelope hash 全部一致；
- operating-envelope 四个 settle/formal 字段仍为 `null`；
- 旧失败 run `p7-td-a-ray-20260721-040137` 已只读保留，未复用；
- 没有其他 calibration、gphoto2、camera、Ray、ESPHome 或 thermal wrapper process；
- 新 Ray、strip、combined path 在进入时均不存在；
- 两个 dry plan 均为 exact TD-A、3 cycles、`60/120/300/600`、12 formal、3 ambient、physical cap
  22、cold proxy 1800 秒；Ray shutter 仅 `1/5000`，strip 仅 `1/320`，
  `exposure_setup_required=[]`，无 `ray-h120-s50`。

### 16.2 实机 preflight

```text
device-preflight.json sha256 = 9cbeff9c5d64bb74020ce7e447547b2f2fd54532f2d9c0a69cc8c812fd483b50
preflight Python cleanup sha256 = 48b4b4d46ceb55f737f94e00670f8794f032d96dfe613dfe43de3a7fe17a5670
preflight shell cleanup sha256 = bb9ad3719f4e284e0817d02e4145596c054e8660bd433466d56130b575da8956
shell cleanup exit = 0
```

- remote health/config 通过，v2 capability 为 `remote_v2_capture_timing_v1`；
- resolved settings 为 ISO `100`、aperture `implicit auto`、format `RAW`；
- Ray independent readback 为 CCT `5600` / GM `100` / intensity `0`；
- strip identity 为 `bedroom-rgbww-strip` / `E0:8C:FE:63:C9:40`，generation `2 -> 3`，五通道全零；
- capture `0`、nonzero probe `0`，Python/shell cleanup 均通过。

### 16.3 Ray 长跑与 heartbeat

```text
run = /Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-ray-20260721-150200
Terminal window = 159069
TTY = ttys002
wrapper PID = 30196
child PID = 30379
PGID = 30195
started_at = 2026-07-21T15:06:27Z
runner log = /Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-ray-20260721-150200.runner.log
wrapper log = /Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-ray-20260721-150200.wrapper.log
wrapper state = /Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-ray-20260721-150200.wrapper-state.json
```

约 3 分钟健康检查：wrapper state `running`，PID/PPID/PGID/TTY ownership 一致，进程已由独立
Terminal 持有，没有 `failure.json`。当前 `1 ambient / 0 formal / 1 physical`，一张 CR3 非空；仍在
首次 cold proxy，非零 source command 尚未成功发送，因此 Human 授权在该健康点仍未消费。

已创建当前同一 task 的 sparse heartbeat：

```text
automation_id = p7-td-a-ray
target_thread = 019f71b5-53fa-7f41-a15c-7335051aa944
schedule = 40 minutes
estimated_next_run = 2026-07-21T15:52:51Z
estimated_ray_remaining = approximately 115 minutes at health check
```

下一次恢复先删除该 heartbeat；仍运行则按实际进度重建单次 heartbeat，不短轮询。失败时审计双
cleanup 并按需 independent recovery，禁止自动重跑或启动 strip；Ray 结构合法完成后才运行单源
analyzer 并继续唯一 strip run。TD-B 及全部后续阶段继续锁定。

### 16.4 Ray hard-invalid：首次 t60 timing miss

heartbeat `p7-td-a-ray` 已在恢复时删除，没有残留重复调度。Ray wrapper 在
`2026-07-21T15:38:35Z` 完整退出：

```text
run status = failed
failure = RuntimeError: missed timing for 001-ray-a-t60
wrapper status = child_failed
child exit = 1
shell cleanup exit = 0
wrapper exit = 1
residual wrapper/child process = 0
```

首次非零 Ray command 于 `2026-07-21T15:37:20.829299+00:00` 成功发送并精确读回：

```text
H = 120
S = 100
INT raw = 1000 / 100%
command hash = 88de37b2161c25b401d616a34c105199243afe21c15545fe5a27691adbdbc96c
```

因此 Human 的 exact `p7_td_a_cold_settling_v1` 一次性授权已在该时间点消费。禁止自动重跑 Ray、
启动 strip 或复用本 run。

失败 capture 的 remote-v2 timing evidence：

```text
capture = 001-ray-a-t60
tier = tier_b
status = accepted_best_effort_anchor
requested elapsed = 60.0 s
best_effort elapsed = 64.40580299403518 s
timing error = +4.40580299403518 s
allowed error = +/-2.0 s
bridge relative delay = 4.402104535 s
local round trip = 8.251924375072122 s
```

当前 scheduler 在 readback 后等到 nominal `t=60` 才发起 remote request；bridge 的曝光起点估计再晚
约 `4.402 s`，因此实际 best-effort exposure-start 超出冻结误差。runner 按合同 fail closed，没有把
附近帧静默替代为正式 t60。

保留的物理事实：

```text
ambient retained ledger = 1
formal retained ledger = 0
run.json physical_cr3_count = 1
actual nonempty physical CR3 on disk = 2
failed t60 CR3 exists and is not entered into accepted capture ledger
retained NPY = 0
```

关键 SHA-256：

```text
plan.json = ebbe657c4b9b11b2dee0f93dd9d38d8fbeffc9d577e3dfc30675677153943c88
run.json = e15c7834c036f12df8c9a819f7d3ce33beda17323c88162f2928e4fe7f17a04f
failure.json = a002378287807d353849048eabd40eace1a38ef25aba107d9838751358b81a91
captures.jsonl = 6ea1676d27cfcc563aa70854ab1f3365de97f8cb7729d3d3c1c0eba8488d6563
commands.jsonl = d2c969652cf83e17fbd555ff23f80459da49b63b5bf3b91ba8f37cc80862a039
isolation-gates.jsonl = c7d83c1888e24628a62581d1cda3c823bbea640c4132344d38ea8d8bb7c43029
all-off-python.json = cf9c45b3cc3d7c4a89f61653b5c57876020c4e87aab90ecfe365d09f8c35a1f4
all-off-shell.json = 86ff1100dcb07dc5579079f6a7d22b81711e4655983e96b90d73df21c4a96427
wrapper-result.json = 461e9f288859658da2d7571716673858c6bf6fb119ea76f3270a80344fe620a1
failed t60 CR3 = 2c44295d5d949ef6f0b652b596173d2c177bb115e64f87efa061dc383b2c303c
failed t60 sidecar = 168d7cf616d5f95d3ef4851c1288370fcb5beec3040b54663fb481592c488fef
runner log = 7c2a11661c6e1b44804257e2e59cd4b12a86e085b45f7b06c7a624dfaf62868c
```

Python cleanup 与 shell cleanup 都记录两源 off 成功。由于失败后没有独立 Ray state readback，Executor
额外执行一次 recovery all-off；结果：

```text
recovery-all-off.json sha256 = 7271ef39a4e245a58c280bb425fb0b96e50225662b5a17349aaa18ef2f1a8cb5
strip identity = bedroom-rgbww-strip / E0:8C:FE:63:C9:40
strip generation = 4 -> 5
strip cw/ww/r/g/b = 0/0/0/0/0
Ray readback = CCT 5600 / GM 100 / intensity 0
recovery status = pass
```

**停止分支：** `TD-A-RAY-HARD-INVALID`。未运行单源 analyzer，未创建 strip run，未运行 paired
finalizer，未执行 retry。需要 Planner 归档本次已消费授权的 timing hard-invalid，并制定仅离线的
scheduler/remote timing 纠偏与新 Human 授权决策；TD-B/C、sentinel、remaining、boundary、holdout、
Gate-6、P8、firmware、remote deployment 和默认安装继续锁定。

## 17. P7-TD-A-T0 observed-elapsed timing v2 离线纠偏

执行日期：2026-07-21。严格遵守当前 `PLAN.md`：未访问设备、网络、`.env`、remote API、相机、Ray、
ESPHome、真实 `all_off`，未创建新 CR3，未启动 heartbeat；`PLAN.md` 保持 Planner-owned 未修改。

实现范围：

- `p7_thermal_diagnostics.py` 新增共享 `PLAN_SCHEMA_V2`、`TIMING_CONTRACT_V2` 和 observed-elapsed 字段；nominal slot 仅为 scheduler target，不再生成 proximity tolerance。
- `measure_p7_thermal_diagnostics.py` production execute 只接受 v2；Tier A/B finite observed elapsed 无论 offset 大小均保留；同 cycle chronology 非递增 fail closed。
- capture adapter 返回非空 CR3 后立即增加 `physical_cr3_count`；后续 timing/quality 失败保留 capture/CR3/sidecar 路径与 hash 到 `failure.json.rejected_capture`。
- `analyze_p7_thermal_diagnostics.py` 显式分派 v1 只读兼容与 v2 replay；v2 从 retained sidecar 重算 observed elapsed、offset、tier、provenance、chronology 和 slot summary，并在 paired 输出中生成 observed settle max。
- `docs/README.md` 与 `.agents/skills/camera-based-rgbww-optimizer/SKILL.md` 已记录 nominal/observed 分离、无 proximity gate、best-effort 非绝对 timing 和 produced-CR3 accounting。

验证：`focused=50/50`；`full suite=495/495 (127.257s)`；`compileall=pass`；全部 `tmp/*.zsh` 语法通过；`git diff --check=pass`；`codegraph sync=pass`。

离线 artifact 根目录：`/Volumes/4T/temp/rgbww-optimizer/p7-td-a-timing-v2-offline/p7-td-a-t0-20260721-114338`。`retained-t60-forensic-replay.json` 独立重放得到 `64.40580299403518s`、offset `+4.40580299403518s`、Tier B，decision 为 `timing_evidence_would_be_accepted_under_v2`，旧 run 未修改且未作为 settling evidence。fake single/paired analyzer、summary、manifest 和 `validation-summary.json` 均已生成；设备/网络/`.env`/remote/camera/Ray/ESPHome/all_off/new CR3/heartbeat 副作用均为 0。

代码与测试已完成 focused commit，等待 Planner 按 T0-PASS/T0-CONTRACT-FAIL 门验收；本轮不申请或消费新的实拍授权，不解锁 TD-A 实机、TD-B、TD-C 或后续阶段。

## 18. P7-TD-A-T0-R1 timing v2 review gaps 离线闭环

执行日期：2026-07-21。仅执行新 `PLAN.md` 冻结的 `T0-REV-001..005`；未修改 Planner-owned
`PLAN.md`。第 17 节写入的 `focused=50/50` 是旧交接误写，保留的 T0 log/summary 实际为
`51/51`；本轮 R1 新 focused log 的真实计数为 `58/58`。

五个 finding 闭环：

- `T0-REV-001`：v1/v2 contract、single analysis、paired combined/manifest 均显式分派。v1 settled
  与 non-settled 保持 legacy schema，不输出 observed claims；mixed pair 在创建 output 前拒绝。
- `T0-REV-002`：`p7_thermal_diagnostics.timing_sequence_identity()` 成为 runner/analyzer/_formal_groups
  共用 owner；TD-A 按 cycle、TD-B 按 switch/return role、TD-C 按 session 分组。两个 TD-C session
  使用相同 `64.4s` observed elapsed 合法。
- `T0-REV-003`：runner 在计数前验证 exact current-run unique nonempty CR3；missing/empty/outside/
  symlink escape 均为 physical 0；有效 CR3 后 sidecar 失败保持 physical 1；重复 path 不重复计数。
- `T0-REV-004`：v2 row、analyzer slot summary 和 paired source report保留 recognized estimate method；
  retained t60 replay 为 exact `gphoto_capture_return_minus_recorded_exposure`。
- `T0-REV-005`：v1/v2 JSON contract 由 deep-copy factory生成，internal accepted tiers为 frozenset，
  module public owner为 nested-immutable mapping；修改 plan A 的 accepted tier list不影响 plan B或validation。

验证：

```text
focused = 58/58 (5.328s unittest; wrapper duration 5.613s)
full suite = 502/502 (116.709s unittest; wrapper duration 116.960s)
compileall = pass
all tmp/*.zsh syntax = pass
git diff --check = pass
codegraph sync = pass
```

最终离线 evidence root：
`/Volumes/4T/temp/rgbww-optimizer/p7-td-a-timing-v2-offline/p7-td-a-t0-r1-20260721-124200`

`validation-summary.json` SHA-256：
`3c38698ded093a734c708b27f0cbf13080ae3439382a5505055c1c2ef9918048`。该目录同时保留
legacy v1 single/pair、v2 pair/manifest、TD-C session chronology、physical negative cases 和带 exact method
的 retained t60 forensic replay。旧 failed run、default operating envelope 与活动 PLAN 的 before/after hash
均一致。

副作用审计：

```text
device/network/.env/remote_api/camera/ray/esphome/all_off/new_real_cr3/heartbeat = 0
remote subproject modified = false
remote subproject tests claimed = false
```

状态：`timing_v2_r1_complete_waiting_for_planner`。未申请或消费新的实拍授权，TD-A 实机及后续阶段
继续锁定。

## 19. Human TD-A authorization received; Planner plan gate still open

执行日期：2026-07-21T21:07:17Z。Human 明确授权开始执行当前活动计划所命名的
`p7_td_a_cold_settling_v1`。该授权与 PLAN 第 3 节冻结范围一致：Ray120c 后 bedroom-rgbww-strip，
每个 source 三个独立 cold cycle，timed points 为 `60/120/300/600s`，每 source `12 formal + 3 ambient`、
physical cap `22`，非并发顺序，约四小时窗口，高输出状态，remote v2 camera，以及 Python finally +
shell EXIT/INT/TERM/HUP + independent recovery cleanup。

本轮未启动设备动作。当前 `PLAN.md` 仍为 `waiting_for_new_exact_human_authorization`，并明确要求
Planner 先把授权原文、时间、范围、预算、恢复路径写入新的 active PLAN，之后 Executor 才可消费一次授权。
Executor 按角色边界不得自行修改或替换 Planner-owned `PLAN.md`，因此在该计划门完成前停止，不执行
preflight、网络请求、source command、camera capture、Ray/ESPHome 或 `all_off`。

状态：`human_authorization_received_pending_planner_plan_update`。
请求 Planner：归档当前等待授权计划并重写 active `PLAN.md`，明确记录上述授权后再交还 Executor；在此之前
不得启动 TD-A 实拍。副作用审计：`device/network/.env/remote_api/camera/ray/esphome/all_off/new_real_cr3/heartbeat = 0`。

## 20. TD-A authorized execution started: Ray run

执行日期：2026-07-21。Planner 已将 active plan 更新为 `execute_authorized_waiting_for_executor`，Human
授权可由 Executor 直接消费。本轮完成正式 preflight：remote `/health`、认证 `/v1/config`、Ray node
config/readback、ESPHome `bedroom-rgbww-strip` identity/generation/zero readback，以及现有
`all_off` 和独立双源 zero readback 均通过。remote settings 为 RAW、ISO `100`、非空 aperture；未打印凭据。

首次 `nohup` launcher 没有留下 wrapper state/run/log，PID 立即退出；该空启动目录未产生 command、capture
或 CR3，保留为启动证据，未据此重跑完整实验。随后只启动一个正式 wrapper-owned Ray run：

```text
run_dir = /Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-ray-debug
wrapper_pid = 90615
child_pid = 90626
wrapper_state = /Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-ray-debug.wrapper-state.json
runner_log = /Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-ray-debug.runner.log
wrapper_log = /Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-ray-debug.wrapper.log
started_at = 2026-07-21T21:21:36Z
```

三分钟健康检查通过：wrapper/child 已脱离当前 TTY，状态仍为 `running`，无 `failure.json`；run ledger
持续落盘，当前 `ambient=1 / formal=0 / physical_cr3=1`，CR3 非空且 capture settings provenance 完整。
按长任务规则已为当前 thread 创建一次性 10 分钟 heartbeat，恢复提示包含上述目录、PID、日志与失败/cleanup
检查规则。当前 goal 状态为等待后台 Ray run 完成，未启动 strip。

## 21. TD-A Ray complete; strip run started

Ray run `/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-ray-debug` 已于
`2026-07-21T23:24:42Z` 正常完成：`12 formal + 3 ambient = 15 physical CR3`，低于 cap `22`，零 NPY，
无 `failure.json`。child/wrapper/Python cleanup/shell cleanup exit 均为 `0`，ESPHome generation-bearing
zero 与 Ray intensity `0` 均有独立证据。

正式单源 analyzer 使用冻结 feature artifact `config/hsi/strip-hsi-policy-v2-waiting.json` 成功生成
`analysis.json`，SHA-256 `13fac6336e95e6900003ff5ced50051b1b9ce2102af9d95729117eab3f46f69d`。
capture、timing、source isolation、covariate、cleanup、wrapper 合同均 pass，15 张均为 Tier B；科学结果为
`settling_not_demonstrated_by_600`，三个 cycle trend score 为 `17.7369 / 16.8013 / 16.7317`，高于冻结
阈值 `4.0`。按 PLAN 的结构合法未稳定分支继续完成 strip 诊断，不把该结果解释为 steady 或进入 TD-B。

唯一 strip run 已启动：

```text
run_dir = /Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-strip-20260722-001426
terminal_tty = ttys003
wrapper_pid = 27283
child_pid = 27363
started_at = 2026-07-22T00:14:27Z
```

三分钟健康检查通过：`ambient=1 / formal=0 / physical_cr3=1`，无 failure，remote settings、isolation、
CR3 和 wrapper state 持续落盘；正在 cycle 1 cold wait。已为当前 thread 创建一次性 10 分钟 heartbeat。
未启动 TD-B/C、sentinel、remaining、boundary、holdout、Gate-6 或 P8。

## 22. TD-A acquisition and paired analysis complete

Strip run `/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-strip-20260722-001426`
已于 `2026-07-22T02:17:49Z` 正常完成：`12 formal + 3 ambient = 15 physical CR3`，低于 cap `22`，
零 NPY、无 `failure.json`。child/wrapper/Python cleanup/shell cleanup exit 均为 `0`；ESPHome
generation-bearing zero 与 Ray intensity `0` 均有独立证据。

Strip 单源 analyzer 生成 `analysis.json`，SHA-256
`3d265f9e57e92552f7dfb2b28c455373eb655911dec2e4e4bb8c59c013302155`。capture、timing、source
isolation、cleanup 和 wrapper 合同均 pass；15 张均为 Tier B。科学结果为
`settling_not_demonstrated_by_600`，cycle trend score 为 `16.8865 / 10.3106 / 11.8856`，均高于
冻结阈值 `4.0`。

Paired finalizer 输出目录：
`/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-paired-20260722-022200`。

```text
td-a-combined-analysis.json = 99550214c619160b39cbf7f393e6b8dc3a5b3feae8f91d0a1765c272283c3160
EXPERIMENT_SUMMARY.md = 21470015f92eb3981753ad398abfdb9f73444e93bc303272cdde9ed717453ee3
input-manifest.json = a938e6f1bc84fee96635a11fcacc8cd2707a322c6b8f18ceedfb2dc8e97f710c
independent-final-zero.json = b83d96e000293f7413372b297b97a49fc676f437e099f8ad6d52f2b401824dc2
```

Paired contract 为 `24 formal + 6 ambient / 30 physical CR3 <= 44`，input/capture/timing/cleanup/wrapper
全部 pass，default operating envelope 未修改。Ray 与 strip 都是 `settling_not_demonstrated_by_600`，
因此 combined status 同名，`t_settle_ray_s`、`t_settle_strip_s`、`t_formal_provisional_s`、`t_formal_s`
全部为 null。最终独立零读回确认 strip generation `7 -> 8` 且五通道全零，Ray intensity `0`；相关采集
进程均不存在。

状态：`td_a_complete_not_settled_by_600_waiting_for_planner_advisor`。停止在 Planner 门，不启动 TD-B、
TD-C、sentinel、remaining 9、boundary、holdout、Gate-6 或 P8。按 PLAN，需要 Planner/Advisor 决定是否
另行设计并授权 `900/1200s` 扩展；本轮不自动扩展或重拍。

---

## 23. P7-TD-B-R0：Developer operational dwell 离线交付

本轮严格消费当前 `PLAN.md` 的离线授权，没有访问设备、网络、`.env`、remote API、相机、Ray、ESPHome，
也没有调用 `all_off`。`PLAN.md` 未被修改。

### 23.1 实现

- 新增 `config/hsi/p7-operating-envelope-v2.json`，保留 Ray/strip 的
  `settling_not_demonstrated_by_600` 与全部 measured settle 字段 `null`；600 仅标记为
  `developer_human_override` / `selected_time_limit_not_proven_steady`。
- 在 `p7_thermal_diagnostics.py` 建立共享 v1/v2 envelope validator 和 TD-B operational-dwell
  provenance validator。旧 v1 仍走 deferred/TD-A prerequisite 路径；v2 只有显式 decision owner、审计
  artifact hash、600 dwell 和 TD-A 未稳定状态全部一致时才可进入 TD-B plan。
- TD-B v2 生成 16 formal、0 ambient、physical cap 24；A0、D/B/C return anchors 为 600，switch
  chronology 为 `60/120/300/600`。Analyzer 输出只能是
  `td_b_operational_600_complete_waiting_for_planner` 或
  `history_dependent_at_operational_dwell_600`，并显式报告
  `dwell_is_scientifically_settled=false` 与 nonstationarity states，不会输出 `td_b_pass` 或自动推进 TD-C。
- `measure_p7_thermal_diagnostics` 新增 `--prerequisite-artifact`，dry-run 不构造设备 owner、不加载
  `.env`、不启动 runner。
- 更新 `docs/README.md` 与 `.agents/skills/camera-based-rgbww-optimizer/SKILL.md`，新增 regression tests。

### 23.2 证据与哈希

| Artifact | Path | SHA-256 |
| --- | --- | --- |
| v2 envelope | `config/hsi/p7-operating-envelope-v2.json` | `7012f254e5fa5182dd51b72624f64ce03645fd3d8b7227ab9144f5c7767cfc16` |
| Ray dry-run | `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-operational-dwell-offline/td-b-ray-v2-dry/plan.json` | `c43e6e460d5ed00ac38ae96f9dd5ee11cf1a61670e2e4d471b6b4f7f57856e5d` |
| strip dry-run | `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-operational-dwell-offline/td-b-strip-v2-dry/plan.json` | `fcf1041023cdc9468d8de0ec70951e284b02115135485486fede8dbea5aa9739` |
| fake analyzer replay | `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-operational-dwell-offline/fake-replay/fake-analyzer-replay.json` | `60d21d716b96daf3d5909828807dc071ccd00b34fbd80fbf71ff9ca624626fa0` |
| validation summary | `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-operational-dwell-offline/validation-summary.json` | `d5b97af6a0b4d4e72df14c57c1d6efe6b1988bc45ff6e5980931d41db3320f9d` |
| readiness | `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-operational-dwell-offline/readiness/readiness.json` | `94298771314b03d8a74c54838f304e648d294af234c3118e93c55d6d43fec3c8` |

The Ray dry-run retains `ray-h120-s50` as an explicit required shutter key with `null` value and
`exposure_setup_required=["ray-h120-s50"]`; the key is present in the frozen ledger, but retained P7-R1 has
no Ray H120/S50 capture from which to claim a shutter. Historical contract permits a separate non-formal setup
before a cold cycle. No auto-exposure value was invented. Strip has `exposure_setup_required=[]`. Planner should
decide whether the phrase “no missing shutter key” accepts this explicit setup-required state or requires a new
bounded offline artifact; Executor will not choose or run that branch.

### 23.3 Validation

```text
focused: 66/66 pass
full suite: 511/511 pass, 110.390s
compileall: pass
all tmp/*.zsh syntax: pass
git diff --check: pass
CodeGraph sync: pass
device/network/.env/remote/camera/Ray/ESPHome/all_off calls: 0
real CR3: 0; NPY: 0; PID/heartbeat/cleanup side effects: 0
```

状态：`p7_td_b_r0_offline_complete_waiting_for_planner_review`。TD-B 实拍、900/1200 扩展、TD-C、sentinel、
remaining、boundary、holdout、Gate-6、P8、firmware、remote deployment 和默认安装均保持锁定。

---

## 24. P7-TD-B-R0S：Ray H120/S50 非正式曝光 setup 离线合同

执行日期：2026-07-21。严格消费当前 `PLAN.md` 的纯离线工作包；未修改 `PLAN.md`，未访问设备、网络、
`.env`、remote API、相机、Ray 或 ESPHome，也未调用 `all_off`。所有临时证据位于：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-setup-offline/20260721-231909
```

### 24.1 实现结果

- 在现有 `p7_thermal_diagnostics.py` owner 内实现 `p7_td_b_exposure_setup_v1` schema、producer、严格
  validator、历史 seed audit、resolved-plan builder 和 public offline replay；未建立平行采集框架。
- P6 `0047-ray-hsi_coarse` 证据可独立重建：Ray set/readback 为 H120/S50/raw INT1000（对应
  `intensity_percent=100`），CR3 hash/byte count、recorded exposure `1/6400`、location、ISO 100、
  implicit-auto aperture、RAW 和当前 58/58 feature 均通过。该 capture 使用 legacy `/v1/capture`、
  quality rejected、无 v2 sidecar，因此固定为 `historical_seed_usable=true`、`seed_only=true`、
  `formal_capture_eligible=false`；`1/6400` 未写入 formal shutter ledger。
- Setup 使用 1..8 张 remote-v2 physical CR3 的独立账本，逐张重放 CR3/sidecar path、hash、byte count、
  capture/request ID、parser receipt、Tier A/B timing、recorded exposure、trial/final disposition、唯一 owner
  和 zero NPY。第 9 张或 ledger drift 为 `physical_budget_accounting_violation`，失败证据保留 attempts。
- Setup source isolation 不信任自报布尔值：Ray set/readback 必须逐字段匹配 H120/S50/INT100；strip
  必须通过 generation-bearing independent zero device-state schema。Cleanup 独立重放 Python、shell、
  child exit、signal、cleanup exit 和最终双源 zero evidence；冷代理必须 monotonic 满 1800 秒。
- Setup artifact 是 `ray-h120-s50` 唯一 resolver。fake resolved plan 仍为
  `fake_resolved_device_locked` / `formal_capture_eligible=false`；production runner 在 backend connect 前
  拒绝 unresolved、fake、hash drift 或 formal-ineligible setup。
- 正式 synthetic round-trip 证明原预算未扩大：setup 8 + formal 16 = physical 24；public analyzer 从
  retained setup/plan/run 独立重算，setup 不进入 formal 16、58-feature fit、repeatability covariance 或
  TD-B history aggregates。Legacy TD-A v1/v2 和 strip TD-B replay 保持通过。

### 24.2 Artifact 和哈希

| Artifact | SHA-256 |
| --- | --- |
| `historical-seed-audit.json` | `66a7b5af31874e4626fc1927080fcdac55dd5f85f438040aaf117bc3b5192ec7` |
| `setup-schema-fake-success.json` | `b64c46bcc74e3c3c721addb9860715505b1a7bf47f2d9d4a1d40745fa8fc67f8` |
| `setup-schema-negative-cases.json` | `3efda7df1c1380e858ac28d9a49fee841c295fe4c9d641317272229aa88ecdb5` |
| `resolved-plan-fake.json` | `e77d8d63211091f81348c3ba68a4dd9db4ef45ac21e2d59f0e1ae210a4442e04` |
| `fake-analyzer-replay.json` | `78d74f57003392cf1d6fc1e51dd3605dabdcdee56f08c1a53429c932fc08b0c7` |
| `readiness.json` | `9144122523d2ebd203bbf07fdf43239445ebd7ce0e41959bc55ee8d5eb2908ed` |
| `focused-tests.log` | `c9dc91d95cd046be8384c8a09547e09d991e3bf30f9ea1cea223a2ecca0b8bd2` |
| `full-tests.log` | `c02ce76d05cac196e869253f1b4e8f0131fd9d104dfff2ba2b53ce4544c0d886` |
| `validation-summary.json` | `7ef454eed34c4de43f7cb065102b2e09dbc24c7567aad0349b33b824838edbfb` |

Fake artifact 目录包含 8 个极小的离线 CR3 byte fixtures 及对应 v2 sidecar，仅用于 parser/ledger
重放，均标记 `fake_only=true`；真实 CR3 数为 0，retained NPY 数为 0。

### 24.3 Validation

```text
focused: 97/97 pass, 5.060s
full suite: 521/521 pass, 112.375s
compileall: pass
tmp/run-p7-thermal-diagnostics.zsh zsh -n: pass
git diff --check: pass
CodeGraph sync: pass
frozen input hashes: 6/6 match PLAN
device/network/.env/remote/camera/Ray/ESPHome/all_off calls: 0
```

状态：`p7_td_b_r0s_offline_complete_waiting_for_planner_review`。没有未解决的 Executor 分支。TD-B setup
实拍、Ray/strip TD-B、TD-C、sentinel、remaining、boundary、holdout、Gate-6、P8、firmware、remote
deployment 和默认安装继续锁定；Planner 必须另写 exact execution PLAN 后才可进入任何实机步骤。

---

## 25. P7-TD-B-E0X：生产回环、精确 checkpoint 与 release gate

执行日期：2026-07-22。严格消费当前 `PLAN.md` 的 E0X 离线门；未修改 `PLAN.md`。离线阶段没有访问
设备、网络、`.env`、remote API、相机、Ray 或 ESPHome，也没有调用 `all_off`。

### 25.1 实现结果

- 正式 TD-B CLI 必须显式选择 `--phase setup|formal`；缺失 phase、授权或 remote-v2 capability 时在
  backend 构造前 fail closed。
- 复用 `camera_gphoto2.auto_expose_capture` 的单一搜索算法，通过 attempt observer 保留 setup 的每张
  remote-v2 CR3/sidecar、ID、hash、byte count、recorded exposure、timing 和 disposition；上限 8 张，
  第 9 张在 capture 前拒绝，retained NPY 为 0。
- setup 在第一张 CR3 前重放 checkpoint/tree、冻结 inputs/budgets、历史 seed、run-start 双零、remote
  health/config/RAW settings、Ray H120/S50/INT100 和 generation-bearing strip zero。
- child 只产生 provisional。生产 wrapper 完成 Python/shell cleanup 并真正退出后，显式外层 orchestrator
  才写 `wrapper-observed-exit.json`、执行独立双零并原子生成 canonical setup、resolved formal plan 和
  release；child/shell/signal/actual wrapper exit 任一失败均不产生 formal release。
- Ray formal 只从相同 checkpoint 的 on-disk release 恢复；paired TD-B finalizer重放两个 public source
  analysis、`32 formal + 1..8 setup = 33..40 physical`、input manifest 和 independent final zero，且保留
  `scientifically_settled=false`。

### 25.2 验证与 checkpoint

```text
focused: 159/159 pass, 8.879s
full suite: 529/529 pass, 148.356s
post-checkpoint production round-trip: 4/4 pass
compileall: pass
all tmp/*.zsh syntax: pass
git diff --check: pass
CodeGraph sync: pass
frozen experiment inputs: 5/5 exact hash match
production src/tests/config/docs/skill/tmp relative to HEAD: clean
offline device/network/.env/remote/camera/Ray/ESPHome/all_off calls: 0
```

实现 checkpoint：`87f1e3244fa0f2a597780a7b0bacb98632c76774`

### 25.3 离线 artifacts

Root：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-production-offline/20260722-090000
```

| Artifact | SHA-256 |
| --- | --- |
| `negative-case-matrix.json` | `8d306882b8e288bf648067f3f843ce581a5e5cafa478a0abcfaff9f86d2f6c8a` |
| `validation-summary.json` | `381387f6430cd811fef186662799079f6785dd67b14c31adf7b76f477dd679c2` |
| `production-fake-manifest.sha256` | `7449fd6813fca64e22645bfaaf300c7ac42b669b1b7bb1708391e63d1493ecb7` |
| `readiness.json` | `8b853f38a09d6a87c235d137e4106f8860e6c15d59b19b9969ccbf5cd3048655` |

状态：`p7_td_b_e0x_release_gate_pass_ready_for_authorized_setup`。根据活动计划，这里没有普通 Planner 停点；
下一动作是启动唯一的 setup outer orchestrator，完成 1..8 张 setup 后双关灯并等待完整 1800 秒 cold proxy。

### 25.4 实机 setup 启动结果：preflight 前 fail closed，停止并请求 Planner 决策

Run owner：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-b-setup-20260722-073500
```

首次 `nohup` launcher 被 Codex 命令宿主在进入 Python main 前回收，launcher log 为 0 bytes、没有 run
directory、command、capture 或 CR3。随后按 PLAN 的 launcher-only分支用 Terminal-owned 方式消费同一 run
identity；生产 wrapper 成功启动，但 child 在任何 setup preflight device/camera action 前被 frozen-input gate
拒绝：

```text
PermissionError: TD-B setup frozen input references differ before device access
child_exit_code = 1
shell_cleanup_exit_code = 0
wrapper_exit_code = 1
CR3 = 0
NPY = 0
```

离线重建确认唯一差异是 CLI 传入相对 prerequisite path：plan 保存
`config/hsi/p7-operating-envelope-v2.json`，production gate 则与同一文件的绝对 path reference 比较。两者
SHA-256 都是 `7012f254...cfc16`，但 path string 不同。其余 location/policy/uncertainty/manifold/curve refs
逐字段一致。这是 producer/validator path canonicalization 缺口，不是实验输入漂移。

Wrapper 的 shell trap随后执行了 `all_off`，且另执行一次 independent recovery：strip
`rgbww_commanded_state` generation `2 -> 3`、五通道全零、device `bedroom-rgbww-strip`、MAC
`E0:8C:FE:63:C9:40`；Ray independent readback intensity `0`。当前无 residual thermal/wrapper process。

| Evidence | SHA-256 |
| --- | --- |
| `wrapper-result.json` | `aa5eff6ebe4b39857295a701fce2c35f7760de02f159eab09c7c278e8e57ddc0` |
| `wrapper-observed-exit.json` | `619f3474175013d83ad888cd36fc1908891d80603326ba16371da8af17cb610c` |
| `all-off-shell.json` | `388736d378cfa69da8846d8b48f75d476055f9af1a2b95fffd18fa8ac85e8de1` |
| `independent-recovery-zero.json` | `29b08bd449b80ad8392f280253a7098fa15b5a0ae9ff5689bec68f023965683e` |
| adjacent runner log | `796c114303b7a3bf7dffb3eb6e0c2261993bdd45f959901ed93e72b77eb81306` |
| Terminal launcher log | `06a496574bd56dcf5deaf4b2bd93a0956b891d3ef849df0f176e336a9b411664` |

PLAN 的 launcher-only 自动重试例外要求“任何 device command 前失败”。本次虽然没有非零 source command、
camera request 或 CR3，但 wrapper recovery 已发送全零 device commands，因此 Executer不自行把它解释为
可自动重试。状态：`blocked_for_planner_relative_path_gate_and_retry_decision`。请求 Planner 冻结：

1. 是否批准离线规范化 prerequisite artifact path 并增加 relative/absolute production CLI round-trip；
2. 独立双零已证实且非零 command/capture 均为 0 的本次失败，是否允许在新目录重试唯一 setup。

Ray formal、strip formal、paired finalizer、TD-C 及后续阶段均未启动。

---

## 26. P7-TD-B-PATH-R1：受信 prerequisite 身份纠偏

执行日期：2026-07-22。严格执行 active `PLAN.md` 的 PATH-R1 离线包，未修改 `PLAN.md`。本阶段未读取
`.env`，未访问设备、网络、remote API、相机、Ray 或 ESPHome，未调用 `all_off`，真实 CR3 为 0。

### 26.1 实现与证据边界

- 在 `optimization.p7_thermal_diagnostics` 增加单一 trusted operating-envelope resolver；相对路径固定
  相对于 `PROJECT_ROOT`，新 plan 始终保存 exact canonical absolute path 和冻结 SHA-256。
- Resolver 在读取 JSON 前拒绝 traversal、项目根外路径、missing、directory、symlink 和同内容 copy；
  v2 再逐字节校验冻结 hash `7012f254...cfc16`。
- plan producer、production setup frozen gate 和 public analyzer/replay 共用该 owner；通用
  `file_reference()` 未修改，既有 v1/retained artifact path schema 未全局迁移。
- Production fake round-trip 覆盖 relative CLI plan build、setup frozen gate、fake backend、2 张
  `fake_only` CR3/sidecar retained ledger 和 public replay；path/hash tamper 在 backend inspection/output
  owner 前拒绝。

### 26.2 验证与 checkpoint

```text
focused: 164/164 pass, 11.884s
full suite: 534/534 pass, 187.852s
compileall: pass
all tmp/*.zsh syntax: pass
git diff --check: pass
CodeGraph sync: pass
relative/absolute canonical reference: equal
negative path/hash/owner matrix: pass
post-checkpoint real frozen gate: pass, deliberate fake-capability stop, output not created
post-checkpoint fake retained/public replay: 1/1 pass
frozen experiment inputs: 5/5 exact hash match
device/network/.env/camera/Ray/ESPHome/all_off calls: 0
```

Focused commit/checkpoint：

```text
0deac80b0a2c794bfbfdd798de428e5d9cf77728
fix(p7): canonicalize TD-B prerequisite identity
```

### 26.3 离线 artifacts

Root：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-path-r1-offline/20260722-112452
```

| Artifact | SHA-256 |
| --- | --- |
| `validation-summary.json` | `3007ad1958d67b0d819b8f87608a9e1e5db329476cbd1b44d780c24270007255` |
| `artifact-sha256.txt` | `1949c6c83a598fd9c912c918a0f62c5713a35852dd0b412a78859e5bea131930` |
| `negative-case-matrix.json` | `6ce0dbe5c7598b470a05fe4d1586d9139c8dfeb0305b4016f183c7d735aa14de` |
| `canonical-reference-comparison.json` | `684feb9b5a97adbeb5a52284df0a2404824dca3fd7bc52c684b2d38e8e412d45` |

状态：`path_r1_offline_pass_single_fresh_setup_retry_authorized`。下一动作严格按 PLAN 使用新目录和项目相对
prerequisite 启动唯一 setup outer orchestrator；setup失败不得第二次重试，成功则连续 Ray formal、strip
formal、两份 public analysis、paired finalizer和独立双源 zero。

### 26.4 唯一 fresh setup 启动与 3 分钟健康检查

Run owner：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-b-setup-20260722-173504
```

```text
started_at = 2026-07-22T17:35:04Z
outer PID = 76855
wrapper PID = 76938
child PID = 76942
PGID = 76855
TTY = ttys004
code checkpoint = 0deac80b0a2c794bfbfdd798de428e5d9cf77728
terminal owner = p7-td-b-setup-20260722-173504.terminal-owner.json
wrapper state = p7-td-b-setup-20260722-173504.wrapper-state.json
runner log = p7-td-b-setup-20260722-173504.runner.log
wrapper log = p7-td-b-setup-20260722-173504.wrapper.log
terminal log = p7-td-b-setup-20260722-173504.terminal-launch.log
```

启动时 AppleScript 只在把 Terminal window id格式化为 text时返回 `-1700`；实际命令已唯一启动，owner、
PID、TTY和进程树均存在，因此未做第二次启动。

3 分钟健康点：

```text
process ownership = pass, Terminal ttys004, independent from Codex PTY
canonical operating envelope = exact absolute owner + 7012f254...cfc16
setup preflight = pass
remote health = ok
camera settings = ISO 100 / implicit auto aperture / RAW
setup physical = 2 CR3 + 2 sidecar, both nonempty
final shutter = 1/6400
timing = Tier B / gphoto_capture_return_minus_recorded_exposure
NPY = 0
failure.json = absent
setup-attempts.json landed = 2026-07-22T11:36:33-0600
phase = setup captures complete, 1800-second cold proxy running
independent safety readback = strip generation 4 -> 5 all zero; Ray intensity 0
```

健康证据：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-b-setup-20260722-173504.health-3m.json
```

同一 task heartbeat 已创建并核对：

```text
Automation ID = p7-td-b-setup
target thread = 019f71b5-53fa-7f41-a15c-7335051aa944
expected next run = 2026-07-22T18:09:50Z / 12:09:50-0600
```

当前状态：`blocked_waiting_for_setup_cold_proxy_and_post_wrapper_finalize`。预计 cold proxy约
`2026-07-22T18:06:33Z`结束；不短间隔轮询。唤醒后按 PLAN 审计 canonical setup/release和双 cleanup，成功
则连续进入 Ray formal，失败则 recovery并停止，且不得再次 setup。

### 26.5 Setup post-wrapper finalization fail closed

Heartbeat 于 `2026-07-22T18:09:03Z` 恢复同一 task 后已删除。Setup wrapper、child 和 outer process 均已
退出；wrapper 本身为完整成功退出：

```text
child_exit_code = 0
shell_cleanup_exit_code = 0
wrapper_exit_code = 0
physical setup CR3 = 2
sidecar = 2
NPY = 0
failure.json = absent
cold proxy elapsed = 1800.003s
```

但是 outer orchestrator 在读取 `setup-provisional.json` 并构造 canonical setup artifact 时由冻结 validator
拒绝：两次 remote v2 capture均请求 `1/6400`，CR3记录曝光均为 `0.0011548225103294601s`，约
`1/865.934`，recorded/nominal ratio为 `7.390864`，超出冻结 `0.8..1.2`。Production exception：

```text
ValueError: TD-B setup shutter differs materially from recorded exposure
```

因此 `setup.json`、`setup-release.json`、`resolved-plan.json` 均未生成，public setup replay没有合法输入，
Ray formal和strip formal均未启动。这是计划内 setup hard failure；本计划唯一 fresh setup权限已消费，
Executer不会重试或绕过 recorded exposure gate。

Cleanup与停止证据完整：Python cleanup、shell trap均 exit 0；orchestrator随后生成独立 final zero，strip
device `bedroom-rgbww-strip` / MAC `E0:8C:FE:63:C9:40` generation `3 -> 4` 且五通道全零，Ray
independent readback intensity `0`。检查时无 residual thermal/wrapper进程，原 heartbeat已删除。

| Evidence | SHA-256 |
| --- | --- |
| `setup-provisional.json` | `095d0a1a1412217bbfb993f44fa325fd132799ea1e721e6b20b64caecd496291` |
| `setup-attempts.json` | `7267322c8f6a4fa82f9d8d1aa400a28b2e9a37b5d72b3fc02e2abc7f114113d1` |
| `wrapper-result.json` | `a969b9d815827b21d25f285672d21b7510e1851edf4e6f658fe1cda3e18b09da` |
| `wrapper-observed-exit.json` | `8d6015cf3d7c8d12bd039e97380c90561a0ab4791b7232e28f18e792a0d2aaaa` |
| `all-off-python.json` | `22e0d86c2dd28c72348748b13181ac6ceb61ecdc2687644821543af3d1fa2337` |
| `all-off-shell.json` | `eab9df5e56830906dcd0555885c1a4057faa84b49ee09c76a2904bcf1a0ab0e0` |
| `independent-final-zero.json` | `b2112547d5782d17f53c40c8a976f51253da2ced22f04be16efd863dbd4204dd` |
| `orchestration-failure.json` | `256e91ece94fe4b639144a00ec8e62ca011b9063342d696de9ebf34c3b3cce45` |
| Terminal launcher log | `91854e8fd77223d600d0e3abb6855d5601b91776846cf7d3734b671d208d289c` |
| adjacent wrapper state | `43de195313e6b6fe00d0a90e5088bae142036eb9fb541e9522661c17a917b86d` |

新增机器可读失败摘要：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/
  p7-td-b-setup-20260722-173504/orchestration-failure.json
```

Planner 决策请求：审查请求 shutter与recorded exposure不一致的相机/adapter证据，冻结后续纠偏分支。
在新 active PLAN前，TD-B formal、TD-C、sentinel、remaining、boundary、holdout和P8全部停止。

---

## 27. P7-TD-B-CANON-R2：E1 与唯一 additional setup

执行日期：2026-07-22。严格消费 active `PLAN.md` 的 Canon-R2 授权，未修改 `PLAN.md`。

### 27.1 E1 离线门

```text
PLAN SHA-256 = 855a019520462c3b6900c06ce126d4a53171142ab10f71a5e5e9562557b5778f
archive SHA-256 = d9a3fa75ea44c971b037d1e5813d3631c512e1b3268ae66f92a50b53edd2bf61
HEAD = 9c804abdeabbc5da18a66d0acf25a1f13128bc2d
production scope relative to HEAD = clean
five frozen experiment input hashes = exact
four remote-controller source hashes = exact
old failed setup evidence hashes = exact
focused P7 thermal/analyzer/remote-client = 114/114 pass
remote r6_timing local tests = 8/8 pass
remote bridge local test import = Flask unavailable; per PLAN no dependency install
compileall = pass
all tmp/*.zsh syntax = pass
git diff --check = pass
device/network/.env/all_off calls during E1 = 0
```

E1 root：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-canon-r2-preflight/20260723-041821
```

`e1-offline-preflight.json` SHA-256：

```text
ef2ee445e6c2e058fc76ea7c39b65a0e45d458dac82ad7f9f7079f6eb244c9cc
```

### 27.2 Terminal-owned setup 启动

Run owner：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/
  p7-td-b-canon-r2-setup-20260723-042002
```

```text
Terminal window = 213571
TTY = ttys003
outer PID = 56749
wrapper PID = 56772
child PID = 56776
PGID = 56749
code checkpoint = 9c804abdeabbc5da18a66d0acf25a1f13128bc2d
terminal owner = p7-td-b-canon-r2-setup-20260723-042002.terminal-owner.json
wrapper state = p7-td-b-canon-r2-setup-20260723-042002.wrapper-state.json
```

启动时 `setup-preflight.json` 和 `unresolved-plan.json` 已落盘，进程树由 Terminal `ttys003` 独立持有。
3 分钟健康检查 heartbeat：

```text
Automation ID = p7-td-b-canon-r2-setup-health
target thread = 019f71b5-53fa-7f41-a15c-7335051aa944
```

当前不短间隔轮询。健康检查必须验证每张新 capture 的
`Canon:ExposureTime/recorded`、ratio `0.8..1.2`、Tier A/B、ID/hash/byte count、零 NPY和双源隔离；
失败则 cleanup/recovery并停止，禁止第三次 setup。

### 27.3 Setup 3 分钟健康检查

原健康检查 heartbeat 已先删除。检查结果：

```text
process tree = outer/wrapper/child 56749/56772/56776 active
PGID/TTY = 56749 / ttys003
wrapper state = running
physical CR3 = 2 nonempty
sidecar = 2 nonempty
NPY = 0
failure.json = absent
attempt 1 = trial
attempt 2 = final
requested shutter = 1/6400
recorded source/status = Canon:ExposureTime / recorded
recorded seconds = 0.000153798956285995
recorded/nominal ratio = 0.9843133202303679
timing = Tier B / gphoto_capture_return_minus_recorded_exposure
CR3/sidecar hash, bytes, capture ID, request ID = public parser replay pass
strip independent zero = generation 5, five channels all zero
Ray independent readback = intensity 0
```

健康 artifact：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/
  p7-td-b-canon-r2-setup-20260723-042002.health-3m.json
SHA-256 = bf1032d2ffa959b191f182b8ff7c14d8c5b67584c3bc25dd24c78ea8ff6f1be1
```

`setup-attempts.json` 于 `2026-07-23T04:21:24Z` 落盘，当前处于完整 1800 秒 cold proxy。已为当前
thread 创建稀疏恢复 heartbeat：

```text
Automation ID = p7-td-b-canon-r2-setup-complete
target thread = 019f71b5-53fa-7f41-a15c-7335051aa944
estimated cold-proxy completion = approximately 2026-07-23T04:51:30Z
```

当前不进行固定频率轮询。Setup finalization通过后才会启动 Ray formal。

### 27.4 Setup finalization 与 public replay

```text
child/shell/wrapper exit = 0/0/0
failure.json = absent
physical setup CR3 = 2
Canon source = 2/2
recorded/nominal ratio = 0.9843133202303679
Tier B = 2/2
NPY = 0
cold proxy elapsed = 1800.0010467909742 s
Python cleanup = pass
shell cleanup = pass
independent final zero = pass
canonical setup = pass
resolved formal plan = pass
setup release = pass
public retained setup replay = pass
formal_capture_eligible = true
```

| Artifact | SHA-256 |
| --- | --- |
| `setup.json` | `2399b62cc310d525e88dcd1d6be81f08abf3c93daa35d54ca14d7023d9c1cd77` |
| `resolved-formal-plan.json` | `215aa359c162b3d154749753394a96a0adb80559d913a1d84b9063ee70ad92e3` |
| `setup-release.json` | `401926bbdefa1a359db03042319acbf9b95f12047cb60f55f7055ed8505c261d` |
| `setup-public-replay.json` | `625ec24bc8c4c879c06f859b31185bb73f70cbf0fc0aa9fb61965e3824004ca7` |

### 27.5 Ray formal 启动

Run owner：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/
  p7-td-b-canon-r2-ray-20260723-045514
```

```text
Terminal window = 214088
TTY = ttys002
wrapper PID = 46018
child PID = 46028
PGID = 46018
code checkpoint = 9c804abdeabbc5da18a66d0acf25a1f13128bc2d
setup release = .../p7-td-b-canon-r2-setup-20260723-042002/setup-release.json
```

Ray formal 已通过 production wrapper 启动。初始 A 状态按计划持续到 600 秒，因此 3 分钟健康点可能尚无
formal CR3。健康 heartbeat：

```text
Automation ID = p7-td-b-canon-r2-ray-health
target thread = 019f71b5-53fa-7f41-a15c-7335051aa944
```

健康检查期间不得关闭正在按计划工作的 Ray；只核对 readback 与 strip zero。失败则 cleanup/recovery并
停止，不启动 strip。

### 27.6 Ray formal 3 分钟健康检查

原健康 heartbeat 已先删除。检查结果：

```text
wrapper/child = 46018/46028 active
PGID/TTY = 46018 / ttys002
wrapper state = running
run status = running
failure.json = absent
NPY = 0
run-start isolation = pass
command ledger = A / H120/S100/INT100 exact readback
independent Ray readback = H120/S100/raw intensity 1000
independent strip zero = generation 6, five channels all zero
formal captures = 0, expected during initial A 600-second dwell
```

健康 artifact：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/
  p7-td-b-canon-r2-ray-20260723-045514.health-3m.json
SHA-256 = 9943219113250fe36d25fe3dd4eba3ad09847d3f1cdb820dfc127bfb71b59a74
```

已为当前 thread 创建按完整 chronology ETA 恢复的稀疏 heartbeat：

```text
Automation ID = p7-td-b-canon-r2-ray-complete
target thread = 019f71b5-53fa-7f41-a15c-7335051aa944
estimated completion = approximately 2026-07-23T06:09Z
```

当前不进行固定频率轮询，也不改变正在运行的 Ray command。

### 27.7 Ray formal hard-invalid 与停止分支

`p7-td-b-canon-r2-ray-complete` heartbeat 已先删除。恢复检查时 wrapper/child 均已退出，Ray
formal 在首个 A/t600 capture 已生成非空 CR3 后失败：

```text
failure type = ValueError
failure message = non-ambient capture requires the preceding ambient capture
child / shell cleanup / wrapper exit = 1 / 0 / 1
completed formal = 0
ambient = 0
strip run = not created
paired finalizer = not run
automatic formal retry = false
```

TD-B frozen plan 没有 ambient capture，但共享 native RAW report writer 要求每张 non-ambient capture
前必须存在 ambient。该冲突发生在真实 `/v2/capture` 已成功返回之后，因此保留了 1 张首个
Ray A/t600 CR3 与 sidecar：

```text
CR3 bytes = 15007444
CR3 SHA-256 = 2cf5d680d694eb9c0d2e36bf8144dcf2f1fe02cd902bc4c202cf92ce1a699608
sidecar SHA-256 = 9952bf79094d7d93b21a9864e841359d0195c423c3dc8464e0250231bc1721ee
capture ID = bfc876fa-9a69-445d-bfc2-298f42baf3af
request ID = 36d2a813-8d35-4f9a-b860-c58cc1ba12e9
recorded exposure source = Canon:ExposureTime
recorded exposure = 0.000193774542476587 s
requested shutter = 1/5000
recorded / requested ratio = 0.968872712382935
timing = Tier B / gphoto_capture_return_minus_recorded_exposure
best-effort observed elapsed = 604.7503857329721 s
NPY = 0
```

这同时暴露 physical ledger 不一致：setup 已有 2 张，formal 又实际生成 1 张，因此可观察总数为
3；但失败后的 `run.json` 仍为 `physical_cr3_count=2`，且未生成 `captures.jsonl`。该 capture
不能被重新标成成功 formal observation，但必须作为 retained physical evidence 计数。

Python cleanup 和 shell trap 均报告两源 off 成功。由于原 cleanup 没有形成两源独立最终读回闭环，
Executor 另执行一次独立 recovery：

```text
recovery status = pass
strip identity = bedroom-rgbww-strip / E0:8C:FE:63:C9:40
strip generation = 2 -> 3
strip five channels = all zero
Ray readback = CCT 5600 / GM 100 / intensity 0
residual wrapper/child process = 0
```

| Evidence | SHA-256 |
| --- | --- |
| `failure.json` | `c9933f6513ef260db920eea99ac85099e93b6c4ff9df71502027ede1a71a3303` |
| `run.json` | `7e370a675160f70078a00a0962ea878e5ede6466b666331269963c052a17fc2b` |
| `all-off-python.json` | `ef631348a4181ec92a793a7ff4e9eaee67bf4b76c97e28067ed5ea20657e3965` |
| `all-off-shell.json` | `ff1951142132b7cb9d2a5203a7b565f081737138186ff296180ea57d3182c55e` |
| `wrapper-result.json` | `da9a976c4e3bebc19d979c4f4e29bc296ef150d42e468c5e78b9f38740154c3f` |
| `independent-recovery-zero.json` | `759a9a2768b72b9a559b764f9077caa647b81c0ec904b9e0b8834c09e6b870c0` |
| adjacent runner log | `9260fdca0cae1dc01ddfa8607bbf3fd442a010704f57d7af8867dbbc8a68fb65` |
| `ray-hard-invalid-summary.json` | `e4a0eeafbadebd4fc8307b2739c72dfa454c154115655cdeeb586467c02daa6e` |

停止分支为 `td_b_formal_ambient_contract_conflict`。按 PLAN，Ray hard-invalid 后禁止启动 strip、
禁止自动重跑 formal，也不运行 public analyzer 或 paired finalizer。请求 Planner 决定一个仅离线
纠偏包：

1. 冻结 TD-B 是否允许 non-ambient formal capture，或是否改变 capture/physical 协议；Executer 不自行
   将 ambient 加入冻结计划。
2. 修复 shared native RAW report owner 对 TD-B 的 experiment-aware ambient 语义。
3. 确保真实 CR3 一旦非空落盘，即使后续 report/feature/timing 失败也先进入 physical ledger 与 retained
   evidence。

TD-C、sentinel、remaining 9、boundary、holdout、Gate-6 与 P8 继续锁定。

## 28. P7-TD-B-F0A 离线纠偏交接

### 28.1 结果

按 active PLAN 的唯一工作包完成 F0A，未修改 `.agent-work/PLAN.md`。实现提交：

```text
commit = 8b80c87939ee9aed31ce0dfaa08a5a936bdc56cb
message = fix(p7): close td-b ambient and physical ledgers
```

闭合内容：

1. 共享 native RAW 默认继续要求 preceding ambient；唯一例外严格绑定
   `p7_td_b_command_switch_history_v1 / formal / p7_thermal_diagnostic_plan_v2`。
2. TD-B v2 每 source 固定 `16 formal / 0 ambient`，使用
   `statistics.normalized_per_second.trimmed_mean`，plan、capture payload 与
   patch-statistics policy 必须一致。
3. 新增 `physical-returns.jsonl`：camera adapter 返回非空 CR3 后立即记录 path、hash、
   bytes 和 capture owner；`captures.jsonl` 只记录通过全部后处理的 accepted measurement。
4. 每次 camera request 前独立检查 physical cap；post-return 的 exposure、RAW、feature、
   timing 或 covariate 失败保留 physical row，accepted counters 不增加。
5. public analyzer 从两份 ledger 独立重算 physical/accepted 数量，并拒绝 duplicate owner、
   hash、counter、policy/report 和 cross-ledger 篡改。
6. 保留的首张 Ray CR3 只生成新的 forensic derived artifact，固定 CR3/sidecar hash、
   capture/request ID、Ray A command/readback、`1/5000`、`Canon:ExposureTime`、Tier B；
   结果显式为 `forensic_only=true / accepted_formal=false / reusable_capture=false`。
7. setup checkpoint lineage 仅生成 Planner candidate；candidate 始终
   `production_release_usable=false`，production runner 继续只接受原 release schema。

### 28.2 Production round-trip 与反例

TD-B strip synthetic production-ledger round-trip：

```text
native_raw_ambient_policy = unsubtracted_no_ambient
physical_returned = 16
accepted_formal = 16
accepted_ambient = 0
physical_total = 16
retained NPY = 0
public analyzer = pass
```

九个独立反例均 fail closed：

```text
cross-experiment no-ambient policy
physical-return CR3 hash tamper
accepted counter tamper
native RAW report policy tamper
prohibited lineage path
empty lineage changed-path ledger
retained CR3 hash tamper
retained capture ID tamper
lineage candidate used as production release
```

### 28.3 Setup lineage

真实 checkpoint diff：

```text
old = 9c804abdeabbc5da18a66d0acf25a1f13128bc2d
new = 8b80c87939ee9aed31ce0dfaa08a5a936bdc56cb
changed paths = 13
prohibited paths = 0
candidate status = eligible_waiting_for_planner
production_release_usable = false
planner_acceptance_required = true
```

该结论只是候选证据，不授权 formal runner，不恢复旧 setup release，也不启动 Ray/strip。

### 28.4 验证

```text
focused = 116/116 pass, 10.885 s
post-commit focused = 116/116 pass, 10.876 s
full suite = 541/541 pass, 155.946 s
compileall = pass
all tmp/*.zsh syntax = pass
git diff --check = pass
CodeGraph sync/explore = pass
device/network/.env/real camera/Ray/ESPHome/light/all_off = 0
new physical CR3 = 0
synthetic validation CR3 = 16, all under external validation root
```

### 28.5 Artifact

根目录：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-f0a-offline/p7-td-b-f0a-20260723-100606
```

| Artifact | SHA-256 |
| --- | --- |
| `validation-summary.json` | `f017deef28e4b8a618525616addb351743b61e8eaa37b8fadbecc3fb11efc6b5` |
| `focused.log` | `d4d44aeccd4a11808bcfadd57338a020f8c8270c47658ad5995b8c7ce6b5722f` |
| `full-suite.log` | `b410322417dffa5247b1ca898b4fcd5bb710494704413d51c47fef6362ba5bd2` |
| `negative-case-matrix.json` | `0a9c29cd1bd0026f74772e11b93e77de8585948954a3b7e9cdf92cf592782a3b` |
| `retained-first-capture-replay.json` | `5e3acbf8efa732c5f27624ae7b9d0b71cdf18fd2b5c616b9829d1e37eebf278e` |
| `physical-ledger-roundtrip.json` | `5ee75475ac1fe827a839b559f56dbb32414f0771e1501af23f4b1fc2440e5238` |
| `setup-release-lineage-candidate.json` | `6d74f2b0fa563147bad00d8c9a89985d3b5de97034288cdd242f10b1d52dc2f1` |

保留证据再次核对：

```text
PLAN SHA-256 = 40859665d742e1e0703ae0390f39169de20af71970214af0bdb0288e1e3f8456
retained Ray CR3 = 2cf5d680d694eb9c0d2e36bf8144dcf2f1fe02cd902bc4c202cf92ce1a699608
retained sidecar = 9952bf79094d7d93b21a9864e841359d0195c423c3dc8464e0250231bc1721ee
setup-release.json = 401926bbdefa1a359db03042319acbf9b95f12047cb60f55f7055ed8505c261d
```

### 28.6 Planner stop

F0A 已停在 Planner 门。请求 Planner：

1. 验收 ambient policy、双 ledger、forensic replay 与负例矩阵。
2. 独立复核 `setup-release-lineage-candidate.json`。
3. 决定 lineage candidate 是否可形成新的 formal release；在 Planner 明确决定前，
   Executor 不得消费 candidate、启动 Ray/strip、重跑 setup 或进入 TD-C/后续阶段。

## 29. P7-TD-B-F0B：lineage formal dispatch failure and offline repair

### 29.1 E2 and the single formal attempt

F0B 离线 release 在 checkpoint `3db7ae25efab74cc800d87ac0a97aead0990ecc1` 生成并通过
public replay；随后 E2 设备前门通过。E2 没有调用相机 capture，且保存了两层 cleanup 与独立
零读回：

```text
E2 = pass
remote health = ok
authenticated /v1/config = pass (ISO 100, RAW, non-empty aperture)
remote v2 capability = remote_v2_capture_timing_v1
Ray node-config/get-cct = pass, intensity 0
strip = bedroom-rgbww-strip, generation-bearing zero readback
Python cleanup = 0
shell cleanup = 0
camera capture / CR3 / NPY = 0
```

E2 evidence:

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2/e2-20260723-171320
```

唯一 Ray formal wrapper 尝试使用：

```text
run = /Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-ray-20260723-172000
wrapper result = child_failed
child exit = 1
shell cleanup exit = 0
```

失败发生在 runner 构造 generic unresolved plan 时：

```text
PermissionError: TD-B execute plan is locked until TD-A passes
```

带 accepted lineage release 的 formal CLI 本应直接 dispatch
`run_resolved_td_b_formal`，但旧入口在 release dispatch 前错误执行了 TD-B prerequisite gate。
该尝试在任何 command、Ray 非零输出、strip 非零输出或相机请求前停止；retained physical CR3 为 0。
失败发生在 Python `run_authorized_plan` 建立 `run.json` 和 Python `finally` owner 之前，因此该 formal
run 没有 `run.json`、`failure.json` 或 `all-off-python.json`；原始 runner log、wrapper、child-exit、
shell cleanup 和 wrapper-result 证据均保留。E2 的 Python/shell cleanup 属于独立 preflight evidence，
不得冒充 formal-run cleanup。

失败后再次执行独立 recovery zero：strip generation `5 -> 6` 且五通道全零，Ray
`get-cct.intensity=0`；无残留 formal 进程。

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-ray-20260723-172000/
  independent-recovery-zero.json
SHA-256 = acd37f19ef2fa0a2fafdfef20b5ac0be53e27426a02e7ef2054d0064f2b5cc59
```

### 29.2 离线修复

修复提交前未重跑设备。CLI 现在在 `--setup-release` 存在时先校验 exact Ray TD-B formal
参数、构造 backend 并 dispatch resolved runner，跳过未使用的 unresolved plan。新增回归
用例锁定该顺序，防止旧 prerequisite gate 再次抢先触发。

修复提交：`b38caa4 fix(p7): dispatch lineage formal release first`

离线修复验证：

```text
focused thermal = 64/64
full suite = 545/545
compileall = pass
all tmp/*.zsh syntax = pass
git diff --check = pass
CodeGraph sync = pass
```

post-commit focused log：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-f0b-offline/
  f0b-20260723-165652/post-fix-post-commit-focused.log
SHA-256 = 904dd04ab03d10dccdab1699bad0d358ff334d8f106b374a856aa5a39fca4516
```

本轮修复尚未形成新的 lineage release：代码 checkpoint 已变化，旧的
`3db7ae25...` release 因此不能继续使用。必须由 Planner 验收该失败和修复，并在新 checkpoint
下重新生成 release；本次未自动重跑 Ray formal，也未启动 strip。

### 29.3 当前停止点

```text
hardware_retry = not_started
new_setup = forbidden
Ray formal = locked pending Planner review and new lineage release
strip formal = locked
TD-C/sentinel/P8 = locked
```

下一次执行前必须使用全新 formal run 目录，并重新通过 lineage release validator、E2 和
Python/shell 双 cleanup 门。旧失败 run 只作启动边界证据，不得改写或当作 formal data。

## 30. P7-TD-B-F0B-R1：new lineage release, E2, and Ray formal start

### 30.1 New lineage release

Planner accepted F0B and rewrote active `PLAN.md`; the old `3db7ae25...` lineage release was not reused.
Using current HEAD `b38caa489754b76cbab616da275517cffa403a83`, the Executor generated a fresh release:

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release/
  lineage-release-r1-20260723-182211/setup-lineage-release.json
SHA-256 = 918bf922c2f9408bad8bb8d9800de0e8f8f9913dbc55359e876cd1227bcb6779
schema = p7_td_b_setup_lineage_release_v2
production_release_usable = true
formal = 16
ambient = 0
physical cap = 24
setup physical = 2
```

Public release replay and fake production runner both passed without backend connection.

### 30.2 E2 preflight

E2 run:

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2/e2-r1-20260723-182330
```

Result:

```text
status = pass
camera capture = 0
remote health = ok
remote v2 capability = remote_v2_capture_timing_v1
remote config = ISO 100, RAW, aperture "implicit auto"
Ray get-cct intensity = 0
strip = bedroom-rgbww-strip / E0:8C:FE:63:C9:40, generation-bearing all-zero
Python cleanup = 0
shell cleanup = 0
```

### 30.3 Ray formal start and 3-minute health

Ray-only formal run started in a fresh directory:

```text
run = /Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-ray-r1-20260723-182500
wrapper PID = 56609
python PID = 56613
release = /Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release/lineage-release-r1-20260723-182211/setup-lineage-release.json
checkpoint = b38caa489754b76cbab616da275517cffa403a83
```

After a 3-minute health observation:

```text
wrapper/python = running
run.json status = running
completed formal = 0
accepted formal = 0
ambient = 0
physical_cr3_count = 2 (setup only)
physical_returned_cr3_count = 0
first command = Ray H120/S100/INT100, readback exact
strip formal = not started
failure.json = absent
```

No short polling is active. A current-thread one-shot heartbeat was created:

```text
automation id = p7-td-b-ray-formal-r1-completion
interval = 75 minutes
```

Executor must not start strip in the completion heartbeat; it may only check Ray completion, run Ray public analyzer if complete,
confirm cleanup/final-zero, and return to Planner.

## 31. P7-TD-B-F0B-R1：Ray formal post-capture hard failure

### 31.1 Result

Ray formal stopped after the first scheduled capture `A = H120/S100/INT100 @ 600s`.
The remote capture returned a non-empty CR3 and v2 sidecar, and the physical-return ledger was
written before feature extraction. Post-return HSI feature extraction then failed closed:

```text
HsiRejectedFeaturesError: 58 required HSI observer features were rejected
```

This is a measurement-quality failure, not a timing or recorded-exposure failure:

```text
recorded exposure = 0.000193774542476587 s
requested shutter = 1/5000
recorded/requested ratio = 0.9688727123829349
timing tier = tier_b / accepted_best_effort_anchor
```

The rejected plane features were:

```text
black/B      near_noise_floor_fraction = 0.9989177134
black/R      near_noise_floor_fraction = 0.9998688396
neutral_3_5/R = 0.8547838598
red/B        = 0.7685270806
blue/R       = 0.9999325008
purple/R     = 0.4281372549
```

All six were rejected by `near_noise_floor_fraction_exceeded`; no feature correction,
threshold widening, or re-exposure was attempted.

### 31.2 Ledgers and cleanup

```text
run = /Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-ray-r1-20260723-182500
status = failed
completed formal = 0
accepted formal = 0
ambient = 0
setup physical = 2
physical returned = 1
physical total = 3
CR3 = 1, non-empty
sidecar = 1, non-empty
NPY = 0
wrapper child exit = 1
shell cleanup exit = 0
Python cleanup = pass
independent final zero = pass
strip formal = not started
```

The retained CR3 is immutable evidence and is not accepted formal data. It remains linked by
capture ID, remote request ID, byte count and CR3 hash in `physical-returns.jsonl` and the sidecar.
The failure payload's `rejected_capture.sidecar_path` and `sidecar_sha256` are `null`, even though
the canonical sibling sidecar file exists and is separately hashed below; this association is
therefore retained evidence, not a completed formal-owner claim.

Independent final-zero artifact:

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-ray-r1-20260723-182500/
  independent-final-zero.json
SHA-256 = a39c742c83e3137a6cb0d1d801e8c0371b5e986cb948643a018b9cea1c858f3f
```

### 31.3 Analyzer and next stop

Ray public analyzer was not run because the acquisition run is structurally hard-invalid after
post-capture feature rejection. No strip, TD-C, sentinel, or any follow-up capture was started.
The active PLAN hard-failure branch is consumed; Planner must decide whether this is an offline
observer/exposure-policy correction package or whether the retained first CR3 is sufficient for
analyzer diagnostics. Executor did not modify thresholds, covariance, 58-feature policy, timing,
or the current PLAN.

Evidence hashes:

```text
run.json = dc24373391d7b39729750c8dfaa2c0b4db7dbbfac36fa962d433335397b0348e
failure.json = eea02c17ffc87b7fa99c339040de0ca9a35d7e8ba35e7a5e7b37c417b62f65ec
physical-returns.jsonl = 6e10bf6a67bc469b9980e13dc03fc3bd0c9b2473f83e48ba9f8c6ca682287484
CR3 = 0778e98d46d05e6bf13e218b79ee644178629076e4d9e6d8a1545fcb54a03889
sidecar = 93d0e64f612ab591da717d99af25dc5606a98148729e1988cc43f667375b4e68
patch statistics = 64a84ea2b6169c11eb457adc54b8a0839895afc5b2ac9a0729d17e62888ed5bd
```

## 32. P7-TD-B-F0B-R1-C1：post-return sidecar evidence 离线收口

### 32.1 实现结果

按 active PLAN 的唯一离线动作完成现有 thermal `execute_plan`/capture owner 修复，没有建立平行 runner：

- physical-return owner 在 CR3 返回后立即验证 canonical same-run sidecar；
- physical ledger 现在同时保留 CR3/sidecar path、byte count、SHA-256、remote capture/request ID；
- report、feature、timing 或 covariate 后处理失败时，`failure.json.rejected_capture` 继承同一已验证证据；
- sidecar 缺失、空文件、越界、symlink、非 canonical sibling、CR3 hash、capture ID 或 metadata schema
  篡改均 fail closed；已返回 CR3 仍计入 physical ledger，但 accepted formal 保持 `0`；
- 新增只读 `audit_post_return_failure()`，只重放旧 R1 evidence，不修改旧 run，也不将 capture 标为 formal/reusable。

本轮没有修改 shutter、quality threshold、58-feature、timing、covariance、formal schedule、预算或低信号策略。

提交：

```text
c4a27242a60278a913b86929e4f0a79e6dfad755
fix(p7): retain sidecar evidence on rejected captures
```

### 32.2 回归与完整验证

```text
focused P7 thermal/analyzer/remote/native-RAW = 148/148 pass
full unittest = 547/547 pass, 152.293 s
post-commit focused = 148/148 pass
compileall = pass
all tmp/*.zsh syntax = pass
git diff --check = pass
CodeGraph sync = pass
```

Fake production-order 回归严格经过：

```text
CR3 return -> sidecar association -> HsiRejectedFeaturesError -> failure.json
```

并验证 `setup physical=2`、新 returned physical `=1`、physical total `=3`、accepted formal `=0`。

### 32.3 旧 R1 只读 replay

新 evidence 目录：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-r1-offline/20260723-142254
```

Artifacts：

```text
post-return-failure-audit.json
SHA-256 = 57a5b3ad32ee1ae0ef53d42d4598933585b7b77464305d4e6aa7bf4d5be36575

validation-summary.json
SHA-256 = 57f7ae903ea7b38e7e4cf53a76b03821842ab5d529bfea7262654ebf1ea1de49
```

Replay 独立验证：CR3/sidecar canonical owner 与冻结 hash、capture/request ID、
`Canon:ExposureTime`、Tier B timing、六个 `near_noise_floor_fraction_exceeded` plane rejection、
Python cleanup、shell cleanup、independent final zero 和零 NPY。旧 `failure.json`、physical ledger、CR3 和
sidecar hash 均保持原值，旧 capture 继续为 `forensic_only=true`、`accepted_formal=false`、
`reusable_capture=false`。

### 32.4 安全边界与 Planner 决策请求

```text
device/network/.env/camera/Ray/ESPHome/all_off calls = 0
new CR3 = 0
public analyzer = not run
old R1 files modified = 0
strip/TD-C/sentinel/P8 = not started
```

当前状态：`offline_c1_complete_waiting_for_planner`。C1 证据 owner 缺陷已闭合；低信号后是否调整 shutter、
增加 weak-signal reacquire、修改质量阈值、改变 formal 数量/预算，或分类为 `measurement_unreachable`，仍属于
Advisor/Planner 科学合同决策，本轮未处理。Planner 必须先验收 C1，再决定新的 lineage/E2/Ray formal 分支；旧 R1
capture 和旧 release 均不得复用。

维护性判断：sidecar schema/owner 校验集中在一个共享 helper，physical-return ledger、failure payload 与只读
forensic audit 各自保持单一责任；新增负例覆盖高风险证据边界，当前不建议额外重构。

## 33. P7-TD-B-F0B-R1-C2：sidecar failure atomicity 离线纠偏

### 33.1 实现结果

按 active PLAN 关闭 `REV-C1-001` 与 `REV-C1-002`，没有改变任何科学合同：

- 已返回且通过 unique/nonempty/current-run 验证的 CR3 先读取并形成稳定 byte/hash 证据；
- sidecar path/stat/read 的预期 `OSError` 被转换为结构化 `sidecar_association` failure；
- post-stat read failure、删除或替换均保留恰好一行 physical ledger，returned physical `=1`、accepted formal `=0`；
- sidecar remote-v2/CR3 binding 验证成功后立即保留 capture/request ID；
- 后续 adapter `timing_metadata` 或 `timing_evidence` drift 继续 fail closed，但 ledger 与
  `failure.json.rejected_capture` 不再丢失已验证 remote IDs；
- 旧 R1 forensic audit 扩展为对 run 下全部 retained regular files 做前后哈希比较，覆盖 CR3、sidecar、
  patch statistics、ledgers、logs 与 cleanup evidence。

未修改 shutter、quality threshold、58-feature、timing、covariance、formal schedule、预算或低信号策略。

### 33.2 回归与完整验证

```text
negative matrix = 14/14 pass
focused P7 thermal/analyzer/remote/native-RAW = 150/150 pass
full unittest = 549/549 pass, 158.732 s
compileall = pass
all tmp/*.zsh syntax = pass
git diff --check = pass
CodeGraph sync = pass
```

新增确定性反例覆盖：

```text
post-stat sidecar read OSError
sidecar removal after stat
sidecar replacement after stat
valid sidecar + adapter timing metadata drift
valid sidecar + adapter timing evidence drift
```

现有 missing/empty/outside/symlink/noncanonical/hash/ID/schema 八类负例及
`CR3 return -> valid sidecar -> HsiRejectedFeaturesError -> failure.json` 顺序回归继续通过。

### 33.3 旧 R1 只读 replay 与证据

证据目录：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-r1-c2-offline/20260723-202736
```

关键 artifacts：

```text
negative-matrix.json
SHA-256 = 94a58b9a2a1149277c8bdcdd9f2f2c95fbfb66b93a43c84d96bb3c7d8a893bc3

old-r1-replay/post-return-failure-audit.json
SHA-256 = c96e9f111ff26f67c056238218fc06d0b3df0a82f280e5cf0d7b52c712cd39e2
```

Replay 证明旧 R1 capture 继续为：

```text
forensic_only = true
accepted_formal = false
reusable_capture = false
```

旧 run 全部 retained regular files 在 replay 前后哈希一致；冻结 CR3 与 sidecar SHA-256 保持：

```text
CR3 = 0778e98d46d05e6bf13e218b79ee644178629076e4d9e6d8a1545fcb54a03889
sidecar = 93d0e64f612ab591da717d99af25dc5606a98148729e1988cc43f667375b4e68
```

### 33.4 安全边界与 Planner 停止点

```text
device/network/.env/camera/Ray/ESPHome/all_off calls = 0
new CR3 = 0
public analyzer = not run
old R1 files modified = 0
lineage release/E2/retry = not run
strip/TD-C/sentinel/P8 = not started
```

当前状态：`offline_c2_complete_waiting_for_planner`。C2 只解决证据 owner/atomicity；低信号后的曝光、
bounded reacquire、质量阈值、formal 数量/预算或 `measurement_unreachable` 分类仍必须在 C2 被 Planner
接受后交由 Advisor/Human 决定。

提交与最终汇总：

```text
implementation commit = e5cd0792c308c444064fd621622f0dead1140a8b
post-commit focused = 150/150 pass
validation-summary.json SHA-256 = bec837bc307f1590b9794e858346303d0ef2bf6e20ab246baaf3b7a7a361ee27
```

维护性判断：修复继续集中在现有 sidecar helper、physical-return ledger 与 forensic audit owner，没有新增
runner、validator 或 ledger；14 类负例、完整测试和只读 replay 覆盖了本轮新增的高风险证据边界。

## 34. P7-TD-B-F0B-R1-C3：formal statistic owner 离线纠偏

### 34.1 实现结果

已关闭 `REV-C2-003`。R1 hard failure 的根因是 TD-B runner 未显式传入冻结 statistic，共享 helper 因此读取
ambient-subtracted 默认路径，将 58 个 required features 全部误判为 `missing_statistic`。

本轮实现：

- feature helper 新增 keyword-only `statistic`，默认仍为
  `ambient_subtracted.trimmed_mean_per_second`；
- `TD_B_FORMAL_FEATURE_STATISTIC` 单一持有
  `statistics.normalized_per_second.trimmed_mean`；
- 仅 validated exact TD-B v2 formal plan 且 no-ambient policy、owner、report context 全部一致时使用该值；
- TD-A、TD-C、legacy/unknown owner 保持 ambient default，无 report-driven fallback；
- retained analyzer 使用同一常量/helper，并拒绝 policy、subtraction、phase、formal-role drift；
- selected frozen feature 的真实 quality rejection 仍结构化失败，weak-signal 仅由 selected feature 的真实
  metrics 决定；
- lineage allowlist 仅新增该 feature owner 与测试，其他路径继续 prohibited。

提交：

```text
fa6c95dbf79f4c0828e8633560d2828e3646204b
fix(p7): bind td-b formal statistic owner
```

### 34.2 验证质量

```text
targeted = 113/113 pass
focused = 197/197 pass
full unittest = 553/553 pass, 109.209 s
negative matrix = 13/13 pass
post-commit lineage regression = 3/3 pass
compileall = pass
all tmp/*.zsh syntax = pass
git diff --check = pass
CodeGraph sync = pass
```

首次 focused 命令误列两个不存在的 test modules，原始失败日志已保留；该命令已运行的断言没有功能失败。
使用实际模块清单重跑为 `197/197`，最终提交态完整套件为 `553/553`。

### 34.3 旧 R1 retained replay

证据目录：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-r1-c3-offline/20260724-061143
```

```text
runner-analyzer-agreement.json SHA-256 = 6adf6a1a046d9b1d334c25647939fa92a3b4c453f68908cacd79e8c179b6bdc2
retained-r1-replay.json SHA-256 = ccc52d1eb5a125df58071fd619b1f3a87080efc74ef8a77fc50a9f2aebdb4cec
negative-matrix.json SHA-256 = 94945851d0994bca0edb5d6636d25a1f929c11fb09b8490bf6955fb976d479b4
validation-summary.json SHA-256 = 3dc83c0d98d7f76549724ebc92548ee8eca39e49ccf95846d6e5497a22256daa
```

Replay 结论：

```text
selected/finite/quality accepted = 58/58
missing statistic = 0
selected quality rejected = 0
diagnostic raw rejected planes = 6
diagnostic/frozen intersection = 0
runner/analyzer same order and values = true
feature-map SHA-256 = 549d76837ae351f87649ee922a1e065c8eb0cd211ea6a8fbc4b53b07a262e303
retained files = 16, all hashes unchanged
forensic_only = true
accepted_formal = false
reusable_capture = false
```

### 34.4 安全边界与停止点

```text
device/network/.env/camera/Ray/ESPHome/all_off calls = 0
new CR3 = 0
public analyzer actual run = 0
lineage release/E2 = 0
Ray/strip/TD-C/sentinel/P8 = not started
```

当前状态：`offline_c3_complete_waiting_for_planner`。正确 statistic 已证明旧 R1 report 的冻结 58 features
不存在低信号 rejection，因此当前不需要 Advisor 决定曝光、threshold、reacquire 或
`measurement_unreachable`。是否生成新 lineage release、重过 E2 或重启 Ray formal 仍由 Planner 下一计划
决定。

维护性判断：statistic 选择由单一 feature owner 持有，runner/analyzer 仅在 exact TD-B contract 下显式引用；
共享默认值与其他 caller 未改变，lineage allowlist 只扩展到该 owner 及其测试，无需后续架构重构。

## 35. P7-TD-B-F0B-R1-C3-E1：C3 evidence manifest 离线补正

### 35.1 交付结果

按 active PLAN 仅补齐证据治理，关闭 `REV-C3-EVID-001` 与 `REV-C3-DEBUG-001`；production code、测试、
C3 原始 artifact 和科学合同均未修改。

E1 证据目录：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-r1-c3-e1-offline/20260724-172355
```

`evidence-manifest.json` 以 absolute/root-relative path、bytes、SHA-256 和证据角色唯一绑定：

```text
canonical logs = 7
canonical JSON artifacts = 4
superseded logs = 19
```

其中 targeted `113/113`、focused `197/197`、full `553/553` 由 C3 validation summary 中的冻结 hash 唯一
定位；compileall、全部 wrapper syntax、`git diff --check` 与 CodeGraph sync 如实记录 C3 summary 缺少 path/hash
的 provenance gap，并绑定 retained post-commit 原始日志。无法由 retained evidence 证明具体原因的 superseded log
统一标记 `reason_not_recorded`，没有推断、删除或重写。

### 35.2 只读源树与独立审计

C3 source root 在 E1 写入前后均递归验证为 root 内普通非 symlink 文件：

```text
entry count = 30
before tree SHA-256 = 605e0ab6335b29047f5f7afd1b0477a1302d4630897c560286fed7f93b3e4ecf
after tree SHA-256  = 605e0ab6335b29047f5f7afd1b0477a1302d4630897c560286fed7f93b3e4ecf
source tree equal = true
```

独立只读 audit 从零重算 JSON、`lstat`、路径边界、bytes/hash、canonical/superseded 完备集合和冻结事实；结果：

```text
status = pass
source_tree mismatches = []
canonical_logs mismatches = []
canonical_artifacts mismatches = []
superseded_logs mismatches = []
frozen_facts mismatches = []
```

旧 R1 继续严格保持：

```text
forensic_only = true
accepted_formal = false
reusable_capture = false
REV-C2-003 = closed
C3 code = accepted
stage progression = waiting_for_e1_planner_acceptance
```

### 35.3 Debug index 与 workspace 边界

`.agent-work/debug/INDEX.md` 中 C3 path 现全局恰好出现一次：

```text
Unresolved count = 0
Resolved count = 1
resolved note content SHA-256 = c687e55b50f693cdaba462cc39d78b4eb56eeffceeacfcb1ea06bb9f14ea1ff1
```

仓库边界验证：

```text
HEAD = fa6c95dbf79f4c0828e8633560d2828e3646204b
git diff --name-only HEAD -- src tests docs .agents/skills tmp = empty
Markdown structure/unique-row checks = pass
JSON/schema/checksum audit = pass
git diff --check = pass
```

E1 未重跑 C3 行为测试或 CodeGraph；`113/113`、`197/197`、`553/553` 和 retained CodeGraph log 仅作为 C3
历史证据，不宣称为 E1 fresh validation。

### 35.4 Artifact hashes 与停止点

```text
source-tree-before.json SHA-256 = 8d28bc146f5c49a9cd698c79a1b22b24367b3cc35aca06996332584629e9a3f2
evidence-manifest.json SHA-256 = aae0f100d6f39cfb92c787839bb08f61fb1cef7c27eaef014acd670ddb88e55d
source-tree-after.json SHA-256 = 4f180e7455a5e94b60b5a5ef2734b2465e558f460d6653b76b3fbb3d2e898ddb
evidence-manifest-audit.json SHA-256 = bfbff503ecca1a2066972f3257504e4f0828a08bed44aafdded098280f12fc95
validation-summary.json bytes = 3271
validation-summary.json SHA-256 = 096a1f7a6664fdcea9f9cf97b3408f1ee56f41158994046bc03fc5464e01f58a
```

```text
device/network/.env/camera/Ray/ESPHome/all_off calls = 0
new CR3/public analyzer actual run/lineage release/E2 = 0
production code/test edit = 0
commit = 0
```

当前状态：`offline_c3_evidence_manifest_e1_complete_waiting_for_planner`。E1 不授权 lineage release、E2、设备
或重拍；必须由 Planner 验收后重写下一工作包。

维护性判断：本轮仅建立一次性的只读证据 manifest/audit 并修正 debug 索引，没有新增 production owner、runner
或验证框架；证据角色和 provenance 缺口已显式记录，无需后续重构。

## 36. P7-TD-B-F0B-R1-C3-L1：当前 checkpoint lineage release

### 36.1 Qualification 结果

按 active PLAN 仅执行一次 production qualification CLI，成功生成绑定 exact checkpoint
`fa6c95dbf79f4c0828e8633560d2828e3646204b` 的新 lineage release：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release/
lineage-release-fa6c95d-20260724-180618/setup-lineage-release.json
```

CLI 不包含 `--execute`、`--allow-device-control` 或 `--human-authorization`：

```text
qualification execution count = 1
exit code = 0
started/ended = 2026-07-24T18:07:20Z / 2026-07-24T18:07:20Z
stderr bytes = 0
release SHA-256 = 1d3fffd82b66dcbca033a6d47bf13af4bbf98f10e9e544f308f4959047532529
```

新 release 目录恰好包含三个 root 内普通非 symlink JSON：

```text
current-lineage-candidate.json
  bytes = 3726
  SHA-256 = 1fd452d2816380cdf7de19a787490e3b7c4d5a9940a6770b782af979f738ced0

resolved-formal-plan.json
  bytes = 15137
  SHA-256 = 7fa13300ca39571801b8c51c7b14ba4e21c646b263712c2ae75341897212424a

setup-lineage-release.json
  bytes = 1495
  SHA-256 = 1d3fffd82b66dcbca033a6d47bf13af4bbf98f10e9e544f308f4959047532529
```

### 36.2 Lineage 与 resolved plan

Fresh production candidate 从 `9c804ab...` 到 `fa6c95d...` 重建出恰好 18 个 unique changed paths：

```text
planner_or_execution_audit_only = 7
bounded_validation_or_documentation = 6
ambient_and_physical_ledger_contract = 5
prohibited_paths = []
canonical_setup_replay = pass
production_release_usable = false
planner_acceptance_required = true
```

Fresh resolved Ray TD-B v2 plan 通过 `validate_td_b_lineage_resolved_plan()`：

```text
formal captures = 16
ambient captures = 0
physical CR3 cap = 24
setup physical CR3 = 2
native RAW policy = unsubtracted_no_ambient
formal_capture_eligible = true
setup_lineage_release_required = true
```

`setup-lineage-release.json` 通过公开 `validate_td_b_setup_lineage_release()` 重放，五个 references 的实际
canonical path/hash 均匹配 immutable legacy release、accepted F0A candidate、同目录 current candidate、canonical
setup 与同目录 fresh resolved plan。

### 36.3 Public replay 与 fake consumer

Public replay：

```text
status = pass
backend_constructed = false
backend_connected = false
network_calls = 0
device_calls = 0
```

Fake-only production consumer roundtrip：

```text
run_resolved_td_b_formal validator = pass
sentinel reached = true, exactly once
delivered plan matches release = true
formal run owner created = false
backend connect/settings/capture calls = 0/0/0
Ray/strip/all_off calls = 0/0/0
CR3 created = 0
```

四个 PLAN 指定的现有 lineage regressions：

```text
4/4 pass
exit code = 0
targeted-tests.log bytes = 158
targeted-tests.log SHA-256 = bbbb881dd4e130a9cedd972935ebedb00830e441a70333b3f7b4d0049ca68480
```

未运行 full suite 或 CodeGraph，符合 L1 合同。

### 36.4 冻结输入与 workspace 审计

Legacy release、canonical setup、legacy resolved plan、accepted F0A candidate、operating envelope 与 E1 manifest
在 qualification 前后 path/bytes/hash 完全一致。Strict release audit 通过：

```text
exactly-three-files = true
JSON parse/schema/checksum = pass
HEAD = fa6c95dbf79f4c0828e8633560d2828e3646204b
staged paths = []
production changed paths = []
git diff --check = pass
old artifact mutation = 0
```

L1 evidence：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-r1-c3-l1-offline/20260724-180618

validation-summary.json bytes = 9717
validation-summary.json SHA-256 = fa0bd82d49ceff571053ff706a73bc6fa8e92a02482e58272591738e960f528d
```

### 36.5 安全边界与停止点

```text
device/network/.env/camera/Ray/ESPHome/all_off calls = 0
new CR3/public analyzer actual run/E2/formal actual execution/strip = 0
production/test/docs/skill/wrapper edit = 0
stage/commit = 0
```

当前状态：`offline_current_lineage_release_l1_complete_waiting_for_planner`。Release 内部的
`production_release_usable=true` 只表示 production consumer 可以验证其 lineage contract；在 Planner 接受 L1
并另写 fresh E2 工作包前，不授权 E2、formal 或设备操作。

维护性判断：本轮复用现有 qualification writer、公开 validator 和 resolved-release consumer，仅生成外部 release
与审计证据；没有新增 production 代码、状态 owner 或平行执行路径，无需后续重构。

## 37. P7-TD-B-F0B-R1-C3-E2-A0：bounded E2 preflight 失败交接

### 37.1 执行范围与结果

按 PLAN 只启动了一次 fresh E2 wrapper，未启动 formal、capture 或 public analyzer：

```text
run = /Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2/e2-fa6c95d-undefined
fresh_e2_runs = 1
wrapper exit = 1
child exit = 1
automatic retry = 0
```

失败发生在 child 的 workspace checkpoint 检查阶段：一次性外置脚本错误使用
`Path(__file__).parents[4]` 推导 Git root，实际执行到 `/Volumes/...` run directory 时无法找到仓库，
`git rev-parse HEAD` 以 exit `128` 失败。因此本次 E2 没有进入 release/remote/backend 访问，也不能解释为设备、相机或科学结果。

```text
failure_class = executor_preflight_root_resolution_error
release_access_reached = false
remote_access_reached = false
camera_capture = 0
new_cr3 = 0
npy = 0
formal_capture = 0
ray_nonzero_output = 0
strip_nonzero_output = 0
```

### 37.2 双层 cleanup 与最终零状态

虽然 child 在主 preflight 前失败，Python `finally` 仍执行；shell `EXIT` trap 随后再次执行，独立最终零读回通过：

```text
Python cleanup = pass
child final zero = pass
shell all_off cleanup = pass
independent final zero = pass
residual E2 processes = 0
```

零状态证据：

```text
strip = bedroom-rgbww-strip
MAC = E0:8C:FE:63:C9:40
state entity = rgbww_commanded_state
strip generation transitions = 1->2, 2->3, 3->4, 4->5
five channels = 0
Ray CCT/GM = 5600/100
Ray intensity = 0
```

没有发出任何非零灯光命令。Shell cleanup 的 ESPHome payload 五通道全零，Ray `set_cct` response 的 intensity 为 `0`；
独立 final-zero 进程再次确认同一 identity、generation-bearing state 和全零状态。

### 37.3 证据完整性修复

一次性 evidence writer 误把两个 JSON 的结尾写成字面量 `\\n`，导致原始文件不可解析；未重跑设备或实验，仅做离线
字节级证据修复，并在 `e2-artifact-repair.json` 保留原始 hash：

```text
e2-preflight.json original SHA-256 = 6ece5bf1ce4290f2c77996901ebfed3b0478f0fda1c10ea055957535a79be595
e2-preflight.json repaired SHA-256 = 33f51ac0b5040ac179bc8ebd9af19b83371a1158c04cd68f9af41a10f25fa404
wrapper-process.json original SHA-256 = 606804c2e82b1a5eb0b441f62bd37c642f1c124fbf1adbf176de8e856f8a4409
wrapper-process.json repaired SHA-256 = 80a12a4255e7c0a02db42d153a40f97d1dd49ea00e2518123e17b0b3d7d4a90b
```

最终 bounded summary：

```text
e2-execution-summary.json bytes = 4733
e2-execution-summary.json SHA-256 = 12e41cd773c9ea955b4251c300ebdfcaf4fbaceadb6162be6f8c456535b63414
```

证据目录：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2/e2-fa6c95d-undefined
```

### 37.4 安全边界与 Planner 停止点

```text
device/network/.env/camera/Ray/ESPHome nonzero operation = 0
remote health/config/capture requests = 0
public analyzer/E2 formal/strip formal/firmware/deployment = 0
旧 release/checkpoint mutation = 0
```

当前状态：`bounded_e2_failure_waiting_for_planner`。按 active PLAN 已停止；不重试、不修复后自动重跑、
不进入 formal。下一步需要 Planner 决定是否建立新的 bounded corrective package，修复外置 runner 的仓库 root
解析与证据 writer 后再申请新的 E2 run。

维护性判断：缺陷局限于本轮一次性 E2 wrapper/证据生成脚本，production code、release、设备控制 owner 和科学合同均未改动；
Python/shell 双 cleanup 与独立 zero readback 已证明安全边界有效，后续只需 Planner 评估是否授权新的离线纠偏包。

## 38. P7-TD-B-F0B-R1-C3-E2-C1：外置 harness 离线纠偏交接

### 38.1 执行范围与结论

按 active PLAN 只执行了一次全新外置 offline correction matrix；未运行 fresh E2、remote/device preflight、真实 cleanup、
capture、formal 或 public analyzer。最终状态：

```text
status = offline_correction_pass_waiting_for_planner
offline_correction_runs = 1
matrix = 22/22 pass
exit code = 0
```

correction root：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-c1-offline/20260724T230534Z
```

冻结 source manifest：

```text
source-manifest.json bytes = 1446
source-manifest.json SHA-256 = c6d782c7d62a4ffc9476d0357f580e02494c938f7700186b56f8e5dcd03c2426
source files = 5
post-run source drift = 0
```

单一 owner 边界为 `strict_json.py`、`e2_child.py`、`e2_wrapper.py`、`fake_git.py` 与
`tests/run_matrix.py`。Project root 只由 wrapper/runner 的显式 `--project-root` 参数传入；child 使用
`git -C <canonical-root> rev-parse --show-toplevel` 验证 exact root，不从 `__file__`、cwd 或外置目录层级推导 repository
identity。Harness source 不嵌入 canonical project-root 绝对路径。

### 38.2 Fake/runtime matrix

```text
external depth = 2/2 pass
root rejection = 5/5 pass
release/checkpoint = 8/8 pass
wrapper lifecycle = 7/7 pass
```

Root 负例覆盖 non-repository、resolved-root mismatch、wrong HEAD、staged paths、production-scope diff；release 负例覆盖
wrong path、symlink、bytes drift、hash drift、schema mismatch、checkpoint mismatch 与 resolved-contract mismatch。所有负例均在
fake backend/device owner 前 fail closed，child 的 backend/network/device 等真实调用计数保持零。

Wrapper lifecycle 的冻结退出结果：

```text
success = 0
child validation failure = 1
child unexpected exception = 1
SIGINT = 130
SIGTERM = 143
SIGHUP = 129
cleanup-only failure = 70
```

每条路径只调用一次 injected fake cleanup 与一次 fake final-zero owner；signal 优先于 child，child failure 优先于
cleanup-only failure。没有调用 repository `all_off`、Ray、ESPHome、camera 或 remote owner。

### 38.3 Strict JSON、redaction 与 provenance

所有 JSON 由单一 atomic strict writer 写入：同目录临时文件、UTF-8、确定性序列化、真实 trailing newline、flush/fsync、
atomic replace 与立即 strict replay。Runner 内审计 60 个 summary 前 JSON；交接前独立复核 correction root 的 62 个 JSON：

```text
strict parse failures = 0
literal backslash-n negative test = rejected
repair artifacts = 0
redaction secret hits = 0
```

最终 summary：

```text
validation-summary.json bytes = 82792
validation-summary.json SHA-256 = 5008c546d620956ed102bf35b296f16c15e4fb9d2f281bfa62573810261fdde0
validation-summary-metadata.json bytes = 331
validation-summary-metadata.json SHA-256 = 57718cd4884daab387e2326da9f907a91073a3e71bfea3b6dc14eb0675286060
```

Summary 记录 exact release path/hash/schema、checkpoint、Planner archive path/hash、source manifest、所有 case result、
stdout/stderr、real/fake counters、strict JSON/redaction/source/old-run/workspace audits 以及 canonical artifact path/bytes/hash。

### 38.4 旧 run 与 workspace 不变性

旧失败 run 只读 tree manifest 完全相同：

```text
files = 13
old-run-before-manifest.json bytes = 2458
old-run-before-manifest.json SHA-256 = 36a49cec031db7ce9b45be97cac2bc0f86303999d13fba2b553903cd80e42e9a
old-run-after-manifest.json bytes = 2458
old-run-after-manifest.json SHA-256 = 36a49cec031db7ce9b45be97cac2bc0f86303999d13fba2b553903cd80e42e9a
```

冻结输入再次匹配：release SHA-256
`1d3fffd82b66dcbca033a6d47bf13af4bbf98f10e9e544f308f4959047532529`；旧 E2 summary SHA-256
`12e41cd773c9ea955b4251c300ebdfcaf4fbaceadb6162be6f8c456535b63414`；Planner archive SHA-256
`1083a48d38c0aa0d91f1a1ea156d4d63d514c50ecf1f39acc06c48efe3f6dca1`。

```text
HEAD = fa6c95dbf79f4c0828e8633560d2828e3646204b
staged paths = []
production-scope changed paths = []
git diff --check = pass
old run mutation = 0
new CR3 = 0
NPY = 0
```

### 38.5 安全边界、停止点与维护性

```text
fresh E2 / automatic retry = 0 / 0
network / .env / remote / camera / Ray / ESPHome / real all_off calls = 0
camera capture / formal / public analyzer actual run = 0
nonzero Ray / strip output = 0 / 0
firmware upload / deployment / destructive hardware change = 0
production-scope edit / stage / commit = 0
```

已停在 Planner 门；C1 离线通过不表示 E2、formal 或 scientific result 通过，未自动进入 fresh E2。按 PLAN 的
“不得修改已有 archive/debug history”约束，active debug record 保持原位，等待 Planner 验收后决定 closure。

维护性判断：C1 把 root gate、release/checkpoint gate、strict evidence writer 与 wrapper lifecycle 分为四个明确的外置 owner，
以 22 个 fake/runtime case 覆盖边界；production coordinator、设备 owner 与科学合同均未改动，无需架构重构。下一步只需
Planner 判断是否接受该冻结 harness 并另行放行一次 fresh E2。

## 39. P7-TD-B-F0B-R1-C3-E2-R1：fresh bounded E2 retry 失败交接

### 39.1 Package freeze 与 no-device self-check

按 active PLAN 创建并冻结唯一 fresh run root：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1/e2-fa6c95d-20260725T152859Z
```

最终 package 组合 byte-exact C1 writer/root-release gate 与 repository remote/Ray/ESPHome/all_off owners；未修改 production
paths。冻结 source manifest：

```text
execution-source-manifest.json bytes = 4346
execution-source-manifest.json SHA-256 = 64ead10f96f0d846a841d8bd65841468d9ff4296af7938f0821f44fb08e3a8af
package source files = 9
C1 source files = 5
```

唯一 no-device self-check：

```text
run count = 1
cases = 6/6 pass
success = 0
root fail-closed = 1
release fail-closed = 1
child failure = 1
SIGTERM = 143
cleanup-only failure = 70
real network/.env/remote/camera/Ray/ESPHome/all_off calls = 0
```

`no-device-self-check.json` bytes `4951`，SHA-256
`d045f17101a3bf4298488deb71d9a4e358b8f1ba6fc521f381a0d8c140234a89`。Post-self-check pre-device audit
以 `pass` 完成，bytes `560`，SHA-256
`be639501272d214bf979331748c75034219983e08749cedf3233df8856efd3b7`；source/release/C1/旧 E2/workspace 无漂移，
无 owned residual process，device calls 仍为零。

### 39.2 唯一 real E2 与失败点

self-check 与 pre-device audit 通过后只启动一次 real wrapper；没有 retry：

```text
package attempts = 1
no-device self-check runs = 1
fresh E2 runs = 1
automatic retry = 0
wrapper PID = 82094
child PID = 82098
wrapper observed exit = 1
```

Byte-exact C1 root/release gate 通过；`real/root-release-gate.json` bytes `2848`，SHA-256
`63eac30211d5b208cf64fbfa120017b99f703411f0e4eaec875320eda82944a0`。

real child 随后完成 remote `/health`、authenticated `/v1/config` 与 Ray node/CCT 零状态调用而未抛错；首个 strip
`esphome.verified_light(0,0,0,0,0, curve_path=thermal.CURVE_PATH)` 在 hostname resolution 阶段失败：

```text
ResolveTimeoutAPIError: Timeout while resolving IP address for ['bedroom-rgbww-strip.local']
failure stage = gate_or_primary
primary status = absent / not passed
```

同一 hostname resolution failure 继续出现在 Python cleanup strip owner、child final-zero、shell all_off strip owner 与
independent final-zero。没有成功取得任何本次 strip generation-bearing snapshot，因此 E2 必须 hard-fail，不能证明最终双零。

外层 shell cleanup 的 retained raw stdout 证明 Ray cleanup 独立成功：

```text
Ray set_cct response code = 0
CCT / GM / intensity = 5600 / 100 / 0
ESPHome step = false, DNS resolution timeout
```

关键 artifacts：

```text
real/child-result.json bytes = 6431
SHA-256 = 9535e0279e4c3b835d9820c45534d985d9e331ced98ddac98f9717cdac0807ef

real/wrapper-process.json bytes = 3887
SHA-256 = cc6e9360e9f430e637dce92b09276186c28cc74fdd3d62fc406207c3b400a2ec

real/all-off-shell.stdout.log bytes = 645
SHA-256 = a76aabff5799945d10f60ea5c4269a8b26374f72631eace992688415d1ee9dc0

real/independent-final-zero.json bytes = 290
SHA-256 = eb8a6c224feb7b746e8ff46902df74f8582a018124f4353c30d8fafa093b964e
```

### 39.3 Finalizer 与不可忽略的 evidence findings

Frozen finalizer 状态：`bounded_e2_failure`。Final summary：

```text
e2-execution-summary.json bytes = 47906
e2-execution-summary.json SHA-256 = 63599437885c25c040f91001d7f2de5341d1389406c0d5e57febab72c39701a8
canonical artifacts = 140
strict JSON at finalization = 57/57 pass
fresh independent strict JSON audit after finalization = 59/59 pass
```

Finalizer findings 为 `child`、`wrapper`、`independent_final_zero`、`shell_cleanup`、`generation_evidence`；C1、旧 E2、release、
source manifest、workspace 与 residual-process audits 均通过。C1 before/after manifests byte-identical；旧 E2 before/after
manifests byte-identical。

还发现两个必须由 Planner 纳入后续判断的 package evidence 缺口；本轮没有修改 frozen source：

1. child 只在 strip zero 成功后才把已经完成的 remote/Ray detail 赋给 `primary`。因此 strip DNS 失败后，retained child
   artifact 仅以控制流和 `remote_calls=2`、`ray_calls=4` 证明这些步骤已运行，没有保留 remote config/capability 与 Ray
   preflight 的详细响应字段。
2. `RealOwners.strip_zero()` 只在 `verified_light()` 成功返回后增加 `esphome_calls`。本轮至少五次 strip zero/cleanup
   connection attempt 均在 DNS resolution 失败，故 child counter 仍显示 `esphome_calls=0`；该值表示成功返回次数，不是
   attempted calls。实际 attempts 由 child failure、Python cleanup、shell stderr 与 independent final-zero artifacts 证明。

这两个缺口不改变 E2 fail 结论，也没有掩盖 capture/nonzero/formal；但当前 summary 不足以作为 successful E2 的完整
provenance/accounting contract。不得用它宣告 remote/Ray详细 gate或 device-call ledger 完整通过。

### 39.4 安全边界与 Planner 停止点

```text
camera capture / new CR3 / NPY = 0 / 0 / 0
Ray nonzero / strip nonzero = 0 / 0
formal / public analyzer actual run = 0 / 0
lineage release create or modify = 0
firmware / deployment / destructive hardware change = 0
production-scope edit / staged paths / commit = 0
owned residual process = 0
HEAD = fa6c95dbf79f4c0828e8633560d2828e3646204b
```

唯一 E2 已消费，已停止在 Planner 门；未因 DNS failure 修补、重跑、capture 或进入 formal。Planner 需要决定是否先处理
`bedroom-rgbww-strip.local` 的 hostname reachability，以及是否建立新的 offline corrective package，把 progressive
remote/Ray provenance 与 attempted-call accounting 修正后，才考虑任何新 E2 授权。

维护性判断：production owners 与科学合同未改；失败暴露的是外置 package 的 progressive evidence ownership 和 failed-attempt
counter semantics 两个局部缺口。最小后续纠偏应先增加设备前逐阶段原子 evidence 与 attempt-before-call 计数，再通过
no-device failure matrix 验证；无需重构 repository device-control modules。

## 40. P7-TD-B-F0B-R1-C3-E2-R1-C2 Executor 离线纠偏结果（2026-07-25）

### 40.1 结论与停止点

已按 active PLAN 在唯一新 external correction root 执行一次纯离线 C2：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-c2-offline/20260725T161556Z`

最终 injected fake matrix 的 14 个规定 case 全部通过，progressive attempt/result、artifact-only accounting、四组
strip/Ray failure isolation、signal unknown-result、post-seal mutation rejection 与正常 terminal seal 均得到实证。
但 Executor 的独立终验发现 `validation-summary.json` 将 progressive stage JSON 总数记录为 `239`，实际 live count 为
`265`：生成表达式漏计 `10-independent-strip-fails/stages/` 的 26 个 JSON。各 case 内的 `stage_artifacts` 与
`semantic_owner_calls` 都正确，26 个 artifacts 也均存在、strict parse 且已进入 terminal inventory；这是 validation
summary 的 aggregate count 缺口。

因为 PLAN 要求任一 stage artifact / summary audit 不满足即 fail closed，且同一 PLAN 同时禁止修补首次落盘 JSON、重跑
offline correction 或产生 repair artifact，本轮不能将 C2 报为验收通过。已保留 evidence，未修改 summary，立即停止在
Planner 门。Planner 需要决定是否接受可由 per-case totals 重放的 `265`，或放行一个仅重建 validation index 的新离线包；
不得据此进入 hostname/ESPHome zero-only gate。

### 40.2 Corrected source 与一次性 fake matrix

corrected source 在 matrix 前冻结，共 `6/6` source 匹配：

```text
corrected-source-manifest.json bytes = 2193
SHA-256 = a0943df78756dfd3417f94765f06ca8731a3427b5a67efd67f5d1bf5f846d2b9
strict_json.py SHA-256 = 73de82c664cb2ad7dfcf4f2b82b5a75202d447d584f74b1112a49b771b2ccf9c
progressive_evidence.py SHA-256 = 2ae0a988ae3c3a3ad1b27949b4b51d5438f3514c8c2338f99faa3360f3e674cb
terminal_seal.py SHA-256 = dc869e8fa9599e20d6d87e06b63a8e78b59e3d899ec38a8a72b9f02f89247d2b
forensic_replay.py SHA-256 = 0c94af694a7e057269dcf205c7f55ea8d0dd6b2576ddb50de1d43a16bffefd95
build_source_manifest.py SHA-256 = baa6ef06bb6cac299bf27354ef6effbeb40220ccc5a23b61b127993717f9123e
run_c2.py SHA-256 = 60eb31884e5e772646546d0e4a8451e4aaa4a9d69662c53cab4c1027f2638f98
```

一次 matrix process exit `0` 且无 stdout；case 结果 `14/14`：

```text
full success = pass
remote health raises = fail closed / retained evidence
remote config raises after health = fail closed / health retained
Ray node raises after remote = fail closed / remote retained
Ray CCT raises after node = fail closed / node retained
primary strip ResolveTimeoutAPIError = fail closed / remote and Ray retained
Python cleanup strip failure + Ray success = pass
child final-zero strip failure + Ray success = pass
shell cleanup strip failure + Ray success = pass
independent final-zero strip failure + Ray success = pass
signal result unknown = exactly 1 attempted_result_unknown
duplicate/missing/misbound/result-before-attempt/success-with-exception = 5/5 rejected
post-seal mutation = rejected with exactly 1 mismatch
normal terminal seal = 301/301
```

full-success artifact replay 得到 exact semantic accounting：remote `2/2`、Ray `6/6`、ESPHome `5/5`
attempted/returned-success。primary strip injected DNS failure 则为 ESPHome `attempted=5`、`returned_success=4`、
`raised_failure=1`，不再把失败 attempt 表示为 calls `0`。四个 cleanup/final-zero pair 在 strip failure 后均继续尝试 Ray，
整体 case 仍 fail closed。所有 aggregate 只引用 immutable stage artifacts。

### 40.3 Forensic replay、terminal seal 与独立终验

R1 只读 forensic reconstruction 未合成 remote/Ray response，相关 detail 明确为 `not_retained`：

```text
r1-forensic-attempt-reconstruction.json bytes = 2007
SHA-256 = 0671e2e92a003899ba08ec768c95a2a2198d70cdf661f41df178247d2fc9f11f
forensic_only = true
synthesized_responses = 0
minimum proven strip attempts = 5
```

terminal sealer 在 producer 关闭后静默运行，stdout/stderr 均为 `0` bytes 且 explicit noncanonical。独立 auditor：

```text
terminal-summary.json bytes = 62695
SHA-256 = 87c0190d2bbc89249c15de31895c06d83f322004e02715739545e3b91b78f682
summary-metadata.json bytes = 906
SHA-256 = 3cffaa501452a593299a03a0cf18b2f20d7fd44a304f8c1ed13cd24c244e94db
canonical live replay = 301/301
mismatches = []
post-seal mutation negative = rejected
```

validation summary 首次落盘后未修改：

```text
validation-summary.json bytes = 76713
SHA-256 = a0e0f1ec6027ba6adb7850d5a3cb1a5f8a49ecdf2c69d8e13a0073ded25ec58c
embedded status = pass_waiting_for_planner
embedded matrix = 14/14
embedded progressive_stage_artifacts = 239  # incorrect aggregate
independent actual progressive stage JSON = 265
independent strict JSON = 296/296
secret hits = 0
repair artifacts = 0
```

`265` 可由 case artifacts 独立求和：`26+18+20+22+24+26+26+26+26+26+25`。因此 embedded pass status
不能覆盖 Executor 的独立终验 finding；handoff 状态为 `C2 evidence implemented, validation index mismatch, Planner decision required`。

### 40.4 冻结输入、预算与维护性判断

old E2 `142/142` files、C1 `126/126` files、lineage release、review archive 和 corrected source 在 before/after replay
中全部 byte-identical。最终 workspace gate：

```text
HEAD = fa6c95dbf79f4c0828e8633560d2828e3646204b
PLAN SHA-256 = 9d7198877ea90e0257fbd3db446d718b5cdeab0961bc9ac934872f25eb9b96f9
staged paths = 0
production-scope diff = 0
git diff --check = pass
git commit = 0
```

所有真实预算均为 `0`：network、`.env`、remote、camera、Ray、ESPHome、repository all_off、hostname resolution、fresh
E2/retry、capture/CR3/NPY、nonzero、formal、public analyzer、firmware/deployment/destructive hardware operation。没有访问或
控制设备；lineage release 保持有效且未重建。

维护性判断：C2 将 stage evidence、artifact accounting 与 terminal sealing 分成三个清晰 external owner，failure-isolated
pair 和 injected matrix 覆盖充分，无需 repository 架构重构。唯一缺口是 validation index 的局部 glob 计数表达式遗漏
case 10；因 frozen-first-landing 约束，本轮正确处理是保留证据并交 Planner，而不是原地修补或重跑。

## 41. P7-TD-B-F0B-R1-C3-E2-R1-Z0-R1 Executor pre-device hard failure（2026-07-25）

### 41.1 结论与停止点

已按 active PLAN 创建唯一 fresh external Z0 root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0/20260725T173840Z`

本包在任何 production ESPHome import、secrets read、hostname resolution、network/device access 或 real wrapper 之前，于
frozen-input gate fail closed。新建 external source 将 active PLAN 的 expected bytes 常量误写为 `3000000`，而冻结 PLAN
实际为 `12933` bytes；PLAN SHA-256 则精确匹配
`3b7abe5e06013e29a2e65608137177d618dc51485c54965895a4fc41f2fe5f56`。因此 package 自身正确拒绝继续，但根因是本轮
external source constant error，不是 repository、PLAN、production owner 或历史 evidence 漂移。

依据 PLAN 的 fail-closed 与一次性 package 约束，本轮没有修补 source、复用 root、重跑 prepare、启动 14-case matrix、import
production owner、读取 secrets 或启动唯一 real wrapper。所有五个 real semantic stage attempts 均为 `0`，已封存当前 evidence
并立即停止在 Planner 门。

### 41.2 Evidence 与独立封存

```text
validation-summary.json bytes = 2981
SHA-256 = abbb92b922ebc145bebb60734ba05f884325d037a6129e87febeced6f14d38d0
status = hard_failure_waiting_for_planner

frozen-inputs/before.json bytes = 4203
SHA-256 = 50bdb258bc351c2eae74ca841de8b1292ecc4daea2833662ff827c2d08cd52a4

source-manifest.json bytes = 553
SHA-256 = 22b276fb40d7eae79a4e617dd6ec63319a93a0f0fea9438f4bdbc03e5c28e665

pre-device-hard-failure.json bytes = 158
SHA-256 = d94533b3185900eeae3cd961529cfdb4657178917fc8eb251a565ae93154a641

terminal-summary.json bytes = 1545
SHA-256 = e19229567e37993cd36761f7c781862e7b2d60e12a2885318a99365fe5dde45f

terminal-metadata.json bytes = 549
SHA-256 = c2376511a84a38cae3937b64f8fece1cc92f889b444bc80e9edfdf51826a08c0
```

独立终验得到 canonical replay `6/6`、mismatches `[]`、symlinks `[]`、strict JSON `6/6`。由于失败发生在 matrix 前，
explicit stage list、per-stage sum 与 sealed stage count 三路均为 `0` 且一致；该一致性只证明没有 real stage 被消费，不能解释为
Z0 reachability pass。source manifest 冻结 external `run_z0.py` 与 `run_z0_wrapper.zsh`；失败后两者均未修改。

### 41.3 冻结输入与硬预算

```text
HEAD = 8cd04d847d42ff5c7bcf7501f46be97cbbef429d
active PLAN SHA-256 = 3b7abe5e06013e29a2e65608137177d618dc51485c54965895a4fc41f2fe5f56
production ESPHome owner SHA-256 = 37cb552524fa06d04ffde2d4cb2ba12f02b448041bfebe0ec63db9982dc638be
secrets input SHA-256 = 908cae88a314de3d932286fae7c5a607f34156cdd0c2ee6ea4647e91edc5d8fc
production-scope staged/unstaged diff = 0

z0 external package builds = 1
no-device self-check runs = 0
real Z0 wrapper runs = 0
assigned ESPHome semantic attempts = 0
production ESPHome imports / secrets reads = 0 / 0
hostname probes / network / device access = 0 / 0 / 0
camera remote / camera / capture / CR3 / NPY = 0 / 0 / 0 / 0 / 0
Ray calls / Ray nonzero / strip nonzero = 0 / 0 / 0
E2 / formal / public analyzer = 0 / 0 / 0
lineage release rebuild or consumption = 0
firmware / deployment / destructive hardware / network configuration change = 0
git stage / commit = 0 / 0
```

历史 lineage release 仍只作为冻结 evidence anchor，未重绑或消费。E2、formal、Ray、nonzero strip 与第二次 Z0 全部保持锁定。

### 41.4 Planner decision request

Planner 需验收并归档本 pre-device hard failure，然后决定是否发布一个新的、仅纠正 external source 中 active PLAN expected-bytes
常量的 bounded offline corrective package；在新 PLAN 明确放行前，不得重建或重跑 Z0，更不得进入 E2 或 formal。该失败不需要
Advisor 科学纠偏，也不是 Human device authorization 问题。

维护性判断：repository production owner 与科学合同完全未改；根因局限于一次性 external package 的冻结常量录入错误。最小后续
纠偏应加入“expected bytes/hash 从 PLAN/frozen manifest 机械提取并在 no-device source validation 中交叉检查”，无需重构生产模块。

## 42. P7-TD-B-F0B-R1-C3-E2-R1-Z0-R1-C1 Executor pre-matrix hard failure（2026-07-25）

### 42.1 结论与停止点

已按 active PLAN 创建唯一 fresh offline correction root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-c1-offline/20260725T175533Z`

本包在 mechanical PLAN freeze 成功后、source manifest 落盘前 hard-fail。Executor 的预检为了单独验证 external
`plan_identity` owner，使用 import 执行了 `harness.py`；Python 因而在 external `source/` 下生成
`__pycache__/harness.cpython-313.pyc`。正式 builder 按冻结合同要求 source entries 必须为普通文件，发现
`source/__pycache__/` 目录后正确 fail closed：

```text
ValueError: source invalid: .../source/__pycache__
```

该失败发生在 identity matrix、wrapper lifecycle matrix、fake adapter 或任何 production owner 之前。依据 PLAN 的首次落盘与
不得同包修补/重跑约束，本轮未删除 `__pycache__`、未修改 source、未重跑 builder、未启动任何 matrix，三个 REV ID 均保持
open；已封存现状并立即停止在 Planner 门。

### 42.2 已完成 evidence 与独立封存

mechanical no-follow PLAN owner 已从同一 fd 实际读取并写入：

```text
plan-freeze.json bytes = 714
SHA-256 = 4157073c687234005618740f5e96038dddc3de9f00c9870ca8a27b430dc0179c
PLAN bytes = 11523
PLAN SHA-256 = 15cdfa3455817b4b69d964b4cdc131b16f9696ce45cda97d5b62e2bc0193c90f
contract ID = P7-TD-B-F0B-R1-C3-E2-R1-Z0-R1-C1
Reference = REF-P7-01
Package kind = offline_external_correction_only
HEAD = 8cd04d847d42ff5c7bcf7501f46be97cbbef429d
```

旧 Z0-R1 root 的 before/after tree manifests 均为 `8` files 且 byte-identical：

```text
frozen/failed-root-before.json bytes = 1371
frozen/failed-root-after.json bytes = 1371
SHA-256（两者）= 2e230418e91ef778d2e7c2c60952a97b130db7630d4d5b3c71f1fa231659a741
```

失败与封存证据：

```text
hard-failure.json bytes = 795
SHA-256 = ac80c428aa67595581f0ac3681ab6dd6497fd4fc1b072b57c79ceb9a131e0d3c

validation-summary.json bytes = 1952
SHA-256 = 59472a77c8dcf8aa5ae1e93b83257fcd00e84bd9de6b60bbf3f19ef0ad69fc62
status = hard_failure_waiting_for_planner

terminal-summary.json bytes = 2173
SHA-256 = 3575a75fe5f27ee85e7f29648f094bab1fea4642e81c8e4a11d8a585fc90b6ca

terminal-metadata.json bytes = 669
SHA-256 = 823ff190d8425f94e1d3177302304b265ffbc17939c0fc5229281df886f5ce09
```

独立 replay 得到 canonical `10/10`、mismatches `[]`、strict JSON `7/7`、symlink `0`、repair artifact `0`；sealer
stdout/stderr 均为 `0` bytes。identity cases、lifecycle cases、per-case stages 与 sealed stages 均为 `0` 且一致；这只证明
matrix 未被消费，不能关闭任何 REV ID 或宣告 correction pass。

### 42.3 硬预算与锁

```text
offline correction package builds = 1
PLAN identity matrix runs = 0
wrapper lifecycle matrix runs = 0
fresh Z0 package / real Z0 wrapper = 0 / 0
assigned real ESPHome attempts = 0
production ESPHome imports / secret reads / .env reads = 0 / 0 / 0
hostname resolution / network / device calls = 0 / 0 / 0
repository all_off / Ray / camera remote / camera = 0 / 0 / 0 / 0
capture / CR3 / NPY / strip nonzero / Ray nonzero = 0 / 0 / 0 / 0 / 0
E2 / formal / public analyzer = 0 / 0 / 0
lineage release rebuild or consumption = 0
firmware / deployment / destructive hardware / network configuration change = 0
production-scope edit / git stage / git commit = 0 / 0 / 0
```

旧失败 root、PLAN、FULL_PLAN_REFERENCE、debug/review、production scope 均未修改。fresh Z0、E2、Ray、camera、formal 与后续阶段
继续锁定。

### 42.4 Planner decision request

Planner 需归档并验收本 pre-matrix hard failure，然后决定是否发布新的 bounded offline correction package。最小纠偏应同时冻结：

1. 所有 preflight 使用 `compile()` 读取源码或设置 `PYTHONDONTWRITEBYTECODE=1`，不得 import 后污染 source root；
2. source manifest 使用显式 source-file inventory，并在 matrix 前拒绝额外 entry；
3. 新包重新机械冻结当前 PLAN，不得复用本包 root 或 evidence。

本失败是 external harness packaging 问题，不需要 Advisor 科学指导或 Human device authorization。

维护性判断：repository production modules 与科学合同未改；问题局限于 external source packaging/preflight ownership。最小后续修复是
隔离 bytecode side effect 并显式冻结 source entries，无需生产架构重构。

## 43. P7-TD-B-F0B-R1-C3-E2-R1-Z0-R1-C2 Executor offline correction pass（2026-07-25）

### 43.1 结论与停止点

已在唯一 fresh offline root 完成一次 C2：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-c2-offline/20260725T181230Z`

最终状态为 `offline_z0_harness_correction_pass_waiting_for_planner`：source hygiene `10/10`、mechanical PLAN identity
`14/14`、真实 injected child/zsh trap/post-wrapper lifecycle `18/18` 全部通过，四个 findings 均由对应 evidence 关闭：

```text
REV-Z0-R1-PLAN-ID-001
REV-Z0-R1-WRAPPER-SIGNAL-002
REV-Z0-R1-MATRIX-003
REV-Z0-R1-C1-SOURCE-HYGIENE-004
```

本 pass 只证明 offline external harness 的 source/identity/lifecycle 合同满足；没有生成或运行 fresh Z0，也不授权 E2、camera、Ray、
capture、nonzero strip 或 formal。已按 PLAN 停在 Planner 门。

### 43.2 Source hygiene 与 mechanical PLAN identity

actual source 从显式两文件 allowlist 逐项 no-follow 冻结；matrix、seal 与独立 audit 后仍为 exact 两文件，无 `.pyc` 或
`__pycache__`：

```text
source-manifest.json bytes = 781
SHA-256 = 24524e8a17f7e4dd1f2d87cb4a9a5b2931d288049a8798fb3082499e3b01d6ce
harness.py bytes/SHA = 52113 / c077b0ea69f91450a06bfaf8427dd330b25608d3566a87a3e35c3ff063033dae
run_wrapper.zsh bytes/SHA = 1671 / 890caf867a4f5630c52bd59b8c7d078daf0f59cd75dfc7b32c79879fe93354e6
```

`compile-preflight.json` bytes `1061`、SHA-256
`8928e72a1743701419ecfaa346d9d61d50dfecadfde8b64fb7dd297fb73877c2`：Python 仅调用 `compile(..., "exec")`，
`python_execution=0`；zsh exact source `-n` exit `0`，stdout/stderr `0/0`；preflight 前后 source manifest 全字段一致。
builder、wrapper children、sealer 与 auditor 均设置 `PYTHONDONTWRITEBYTECODE=1`，Python entry 同时设置
`sys.dont_write_bytecode=True`。

source-hygiene matrix 恰好一次 `10/10`，覆盖 exact inventory、`__pycache__`、`.pyc`、unknown file、file/parent symlink、missing、
bytes mutation、same-content inode replacement、manifest duplicate/tamper。两个 symlink 负例 fixture 保留并在 terminal 中明确分类；
unexpected symlink 为 `[]`，actual source symlink 为 `0`。

PLAN identity 通过单一 no-follow fd owner 机械取得：

```text
plan-freeze.json bytes = 714
SHA-256 = bdbf1babf3193d8f3244f41c41143c1b638b540488623c39e52b50664f5feedf
PLAN bytes = 11767
PLAN SHA-256 = c056fd40de61de20f3927484762b58c983491f6e43a2104ff048e3bf2f5f8728
contract = P7-TD-B-F0B-R1-C3-E2-R1-Z0-R1-C2
HEAD = 8cd04d847d42ff5c7bcf7501f46be97cbbef429d
```

identity matrix 恰好一次 `14/14`，包括 mutation、inode、PLAN/parent symlink、outside-root、missing/FIFO/directory、contract
missing/duplicate、reference/package/head drift、freeze tamper 与 source-binding tamper；负例均在 lifecycle/fake adapter 前拒绝。

### 43.3 真实 injected wrapper lifecycle

lifecycle matrix 由真实 external `harness.py` child、参数化 `run_wrapper.zsh`、EXIT trap 和 wrapper 完全退出后的 independent
finalizer 执行；不是直接合成 aggregate。恰好一次 `18/18`，每 case 五 stages，共 `90` stage bundles；每 bundle 均为 attempt
先于 adapter call，result 绑定 attempt path/hash且无 retry。

```text
lifecycle-matrix.json bytes = 123816
SHA-256 = 24e995ec6ad8bd862784ec89689d9a2466d4925135dbadf71d4f2c8b24c86db7
SIGINT / SIGTERM / SIGHUP exits = 130 / 143 / 129
signal-precedence exit = 143
all signal trap_count = 1
watchdog attempted_result_unknown = 1
explicit stages / sealed attempts / sealed results / sealed adapter calls = 90 / 90 / 90 / 90
```

除 PLAN 要求的 12 个 lifecycle branches 外，wrong name/MAC/state object、nonzero snapshot、per-call/global generation drift 六个
真实 injected subcases 全部 fail closed。child PID/exit、signal name/code、shell cleanup、wrapper final exit 与 independent finalizer
exit 均持久化并通过交叉绑定。

### 43.4 Terminal seal、冻结 roots 与预算

所有 producer/log handles 关闭后 silent seal；sealer stdout/stderr `0/0` bytes。独立 auditor 与 post-audit replay：

```text
terminal-summary.json bytes = 102700
SHA-256 = 832425e1ba10ab881a3693ca49639167efe3bbe62a08b8baf9ceb8c558faf1d9
terminal-metadata.json bytes = 1469
SHA-256 = 57f1eb0bb71216a465eb08a3a8cdbfa637d50d5452364278b676f93a8eb9ab50
canonical live replay = 527/527
mismatches = []
seal-time strict JSON = 451/451
post-audit strict JSON = 453/453
source drift / bytecode / unexpected symlink / repair artifact / production diff = 0 / 0 / 0 / 0 / 0
C1 root unchanged = true
Z0-R1 root unchanged = true
```

最终 summary：

```text
validation-summary.json bytes = 4087
SHA-256 = 63ef3caaf8636366d0bb5dd047e6f32693b4a9fb6893df1afe5191279fe5bd35
status = offline_z0_harness_correction_pass_waiting_for_planner
```

所有禁止预算为 `0`：fresh/real Z0、real ESPHome attempt、production import、secrets/`.env`、hostname/network/device、repository
all_off、Ray、camera remote/camera、capture/CR3/NPY、nonzero、E2/formal/public analyzer、lineage、firmware/deployment/destructive/
network config、production edit、git stage/commit。HEAD 保持 `8cd04d847d42ff5c7bcf7501f46be97cbbef429d`，无残留 owned process。

Planner 下一步只能验收/归档本 offline correction，并决定是否另写一个新的单一 fresh Z0 PLAN；本轮不得自行进入 Z0。

维护性判断：harness 的 source inventory、compile owner、PLAN identity、stage accounting 与 wrapper precedence 各有明确单一 owner，
三组 adversarial matrix 覆盖完整；repository production 代码零改动，暂不需要进一步架构重构。

## 44. P7-TD-B-F0B-R1-C3-E2-R1-Z0-R2 — mandatory self-check pre-device hard failure（2026-07-25）

严格执行 active PLAN SHA-256
`46f2fa6c9c85858f1876c66c5cba737d8a044bd2b2e4ff8f694a8bc27df18056` 的唯一 fresh package：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r2/20260725T183318Z`

### 44.1 结论与停止点

mandatory no-device self-check 恰好启动一次并 exit `1`，在第一个 old-root before-manifest gate hard-fail：

```text
ValueError: tree symlink rejected:
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-c2-offline/20260725T181230Z/
fixtures/source-hygiene/05-source-symlink/source/harness.py
```

根因是新 Z0-R2 before-manifest owner 对已接受 C2 tree 使用了无条件 symlink 拒绝，而 C2 的 source-hygiene case 05 按设计保留
负例 symlink。失败发生在 source manifest、compile、PLAN freeze、三组 matrix 与 immutable pre-device pass 之前。依据 PLAN，未修补
source、未重跑 self-check、未启动 real wrapper，立即停止在 Planner 门。

只读封存同时发现独立的后续 exact gate failure：fresh `run_wrapper.zsh` 为 `1672` bytes、SHA-256
`15dfa4a3631d82dc3bf1c23887d788344c86f13f267272edccb5d8e2d71f5522`，不等于 PLAN 冻结的 C2 wrapper `1671` bytes、
SHA-256 `890caf867a4f5630c52bd59b8c7d078daf0f59cd75dfc7b32c79879fe93354e6`。本 root 未修正该尾换行漂移。

### 44.2 安全边界与预算

```text
fresh package build / self-check runs = 1 / 1
self-check rerun = 0
real wrapper / assigned real attempts = 0 / 0
production ESPHome import / secret read = 0 / 0
hostname resolution / network / device = 0 / 0 / 0
camera / Ray / nonzero strip / E2 / formal = 0 / 0 / 0 / 0 / 0
.env / firmware / network config / git stage / commit = 0 / 0 / 0 / 0 / 0
bytecode entries / residual owned processes = 0 / 0
```

HEAD 保持 `8cd04d847d42ff5c7bcf7501f46be97cbbef429d`；production-scope staged/unstaged diff为空。未读取 secrets
内容；未 import production owner；未访问 hostname、network或device。

### 44.3 封存 evidence

- `pre-device-failure.json`：bytes `2315`，SHA-256
  `7f2c259e5973ce5e6554874e3c52ea8c0667b47abef5633a6e66e7f57e725d8a`；
- `terminal-failure-snapshot.json`：bytes `430`，SHA-256
  `80d4f1952d3c31aaf43d9d910d08aaf0abb3309152c18ba1cf8c322d7b9c753b`；
- `validation-summary.json`：bytes `627`，SHA-256
  `03e5900ffa495e5958be34283007fc13f950a25a0d53db0ba761a11b9c576046`；
- self-check stderr：bytes `1070`，SHA-256
  `c0bad20d521781751a6e5b980340979e526f5986c5506f613226fe5e50bacb7c`；stdout `0` bytes；
- structured JSON strict replay `3/3`，source inventory恰好三个普通文件，`__pycache__`/`.pyc` 为 `0`。

Planner 下一步只能验收/归档本 pre-device hard failure，并决定是否建立新的离线 corrective package；本 Z0-R2 root不得修改、
重放或进入 real gate。

维护性判断：失败位于外置 evidence-tree分类和source复制边界，production owner与科学合同均未执行或修改；后续应以离线负例树
分类规则和byte-exact复制回归为最小纠偏范围，无需生产架构重构。

## 45. REF-WORKFLOW-01 / WORKFLOW-LOCAL-LAB-CONTEXT-R1 — implementation完成但full-suite baseline阻塞（2026-07-25）

严格执行 active PLAN SHA-256
`da05e560d00024a4cd7205c014a76fd7b11fb8b2f0569cac04b522fa5ea9e5c1` 的纯离线 package，evidence root：

`/Volumes/4T/temp/rgbww-optimizer/workflow-local-lab-context-r1/20260725T195112Z`

### 45.1 实现结果

- 新增 `control/local_lab_context.py` 作为三个CLI的单一正向context owner；ESPHome、camera bridge、Ray help均复用同一
  user-owned local photography and lighting calibration lab context，同时保留各自action差异。
- Ray production default secret与`DEFAULT_OPENAPI_SECRET`已删除；新增非secret常量`OPENAPI_SECRET_ENV`。
  `OpenAPISettings.secret`为required、`repr=False`；单一strict-base64/exact-32-byte helper同时服务settings与token。
- `from_env`支持显式mapping，missing/empty在连接前只报告环境变量名；`generate_token` secret参数required；CLI删除
  `--secret`并只从process environment取得真实command credential，help不读取credential。
- tests只在runtime由`bytes(range(32))`生成fake key；未读取开发机实际environment或credential。
- `AGENTS.md`在Language前新增正向local-lab scope；新增`docs/local-lab-connection-boundary.md`并由README/skill链接。
- P7 TD-B详细历史迁到`docs/engineering/p7-td-b-contract-history.md`，明确paused/not authorized；skill从`41300`缩至
  `4678` bytes并改为progressive routing入口。

本包实际changed paths共13个，全部在PLAN授权清单内：三个control modules加新context owner、`test_ray120c.py`、
`test_all_off.py`、两个新结构/context tests、`AGENTS.md`、README、central boundary doc、P7 history note和project skill。
未修改protocol、payload、timeout、cleanup、experiment runner、PLAN、FULL、GUIDE、debug或archives。

### 45.2 Ray API/CLI与静态验收

```text
old exact value count in current source/tests/docs/skill/AGENTS = 0
DEFAULT_OPENAPI_SECRET count = 0
CLI --secret registration count = 0
OpenAPISettings.secret required / repr disabled = true / true
generate_token secret positional defaults = 0
skill bytes = 4678 <= 12000
```

三个module `--help`均exit `0`、包含shared context与各自RGBWW/camera/Ray action，且不包含credential value、default或
`--secret`。credential/leak audit确认current authorized content与external logs的旧exact-value hits均为`0`；diff仅按预期包含
被删除baseline行，未把其值写入任何新artifact或交接文本。

### 45.3 Tests与检查

focused/control首轮`46/51`，发现4个all_off fake-call tests未注入required fake key及1个argparse换行断言；仅修测试注入/断言后：

```text
focused/control rerun = 51/51 pass
full rerun with runtime-generated fake 32-byte key = 557/559
compileall with external PYTHONPYCACHEPREFIX = exit 0
three module help = 0/0/0
CodeGraph sync = exit 0
git diff --check = exit 0
repo-produced bytecode = 0（既有ignored bytecode未删除）
```

CodeGraph同步后确认`cli_description`只有一个owner并由三个CLI调用；`_decode_secret`是settings/token共同校验owner；
`OpenAPISettings.from_env`的production caller仍为Ray/all_off。

full suite剩余两个error：

1. `test_lineage_release_rebuilds_current_plan_and_reaches_formal_runner`；
2. `test_lineage_release_rejects_candidate_and_resolved_plan_tampering`。

两者均在本包逻辑前由TD-B lineage allowlist拒绝current HEAD `8cd04d8`从setup checkpoint继承的既有
`AGENTS.md`/`FULL_PLAN_REFERENCE.md`路径。第二次full run已通过runtime fake key消除本包相关的5个cleanup failures，稳定只剩这两个
current-HEAD baseline-coupled errors。修复需要修改未授权的P7 production或`tests/test_p7_thermal_diagnostics.py`，不能在本package安全
处理。

### 45.4 Evidence、预算与Planner请求

- `validation-summary.json`：bytes `1590`，SHA-256
  `5f273d4ead876e45493042a24f63881a16423e9f49f3ed16640f0bf2c10bee53`；
- focused pass log：SHA-256 `b930c1c153c7d9176e7983326928b6932065cc8f55fd66c533cea089edeb42cf`；
- full-r2 log：SHA-256 `9c71b2f71ab338667eb7dda1161e988cff1ea11f25afaecffb7d0c19fc24f4c0`；
- static audit：SHA-256 `a461484112b68efa1c95c178e2026c5535b2a966e400b971f58c6f82a9bd6388`；
- leak audit：SHA-256 `d8c63b627112f5ff1b8a77683716de31dcc458c6f1e013caf07d3032c6107a2f`；
- CodeGraph sync log：SHA-256 `1aed90cec4e39f362899eb84dd4bb3fc7e02d924d24eeb9976617245e5f9beb3`。

hostname/network/device/camera/Ray/strip/nonzero/Z0/E2/capture/formal/firmware/deployment/actual credential或secret reads全部为`0`。
由于PLAN明确要求full suite全绿才算implementation complete并创建commit，本轮`git stage=0`、`git commit=0`；没有把未验收diff或
任何unrelated user/Orchestrator work加入index。

Planner需决定：接受`557/559`并将两个current-HEAD lineage tests列为独立baseline纠偏，或另发一个允许修复其checkpoint/allowlist
测试合同的bounded package。在Planner决定前不得stage/commit，也不得恢复Z0/E2/formal。

维护性判断：shared CLI context和Ray credential validation各有单一owner，三CLI只保留action差异；新增测试覆盖required secret、
redaction、strict validation、help和docs/skill结构。实现未引入平行client或credential路径，后续只需处理独立的TD-B baseline test
耦合，无需重构本workflow实现。

## 46. REF-WORKFLOW-01 / WORKFLOW-LOCAL-LAB-CONTEXT-R1-COMMIT — exact commit完成（2026-07-25）

严格执行 active PLAN SHA-256
`b1e8b381f0448efd016a55117fb4ccc4bccbf52e95fe0eb8532b0f8c63c76362` 的commit-only package。未编辑或格式化任何
implementation、documentation、skill或test文件；未运行tests、module、compile或CodeGraph。

### 46.1 Pre-stage与cached gate

- parent HEAD exact：`8cd04d847d42ff5c7bcf7501f46be97cbbef429d`；初始index为空；
- accepted review archive SHA-256：`b48b2405dfd753e2834f6aa19328675b880081c48eeafd8e4bf3d9ad1207dbcc`；
- accepted validation SHA-256：`5f273d4ead876e45493042a24f63881a16423e9f49f3ed16640f0bf2c10bee53`；
- 13个frozen paths逐项为repository内普通non-symlink file，working tree与cached blob的mode、bytes、SHA-256均exact；
- scoped status恰好8个modified与5个untracked，全部相对parent有实际diff；
- pre-stage和cached `git diff --check`通过；
- 使用一次explicit 13-path `git add -- ...`；cached path set无missing、extra或duplicate，全部mode `100644`。

冻结13项在pre-stage、cached与commit tree的bytes/SHA均一致：

| path | bytes | SHA-256 |
| --- | ---: | --- |
| `.agents/skills/camera-based-rgbww-optimizer/SKILL.md` | 4678 | `4619c131e1e733b9a9763312dfa463fecd45db80f7ea95476f2bbae4e46aa159` |
| `AGENTS.md` | 13909 | `a035e6955ea113100031bf411f30abad3b84a9dd260fde848f1b1cfbd194c8a5` |
| `docs/README.md` | 71254 | `38518c0c8d7524d17a036852f1854f757d1afc0f1b0100d1f21541b75d86a302` |
| `docs/engineering/p7-td-b-contract-history.md` | 4346 | `972ec515978f064a7339f7a2cbf028e794109c7d79cc95355456537e1c05c2c2` |
| `docs/local-lab-connection-boundary.md` | 2807 | `c33e78bc0b0fb23352a37b75c347d1a602a85d674e601d1c113c5712a823c84e` |
| `src/camera_based_rgbww_optimizer/control/camera_remote.py` | 34204 | `8fbe882c686606eda28e72c9b5d270681142bec262ff3f7f2fd4f7fe7657d097` |
| `src/camera_based_rgbww_optimizer/control/esphome.py` | 12538 | `0a5b6258fe3ea8519f697c4351eac9ac4243bbbabe0d30530f4c30564c972872` |
| `src/camera_based_rgbww_optimizer/control/local_lab_context.py` | 328 | `8c94d96b1dc9f9a959ee4988a89e80a68ac27faa2f132bf2d3aaed95a2bcd193` |
| `src/camera_based_rgbww_optimizer/control/ray120c.py` | 25132 | `16bc57834885a813e7b990b213513fb19ea7bd3ad935f59cd2ce44cd38b61c5d` |
| `tests/test_all_off.py` | 4013 | `1ef519f2098caed526df03f53eed9f4fe0e87cf24296246b4c1f40a71128258f` |
| `tests/test_local_lab_context.py` | 1152 | `81964d6bf13e6dace447f2d1686386f6128af2f9295f9e0184e99d870b256ea7` |
| `tests/test_project_context_docs.py` | 2042 | `1b5622d659d42ec29807e6fec4f1ec68d1e52bc83ba227ab4edffb60b7ac9e39` |
| `tests/test_ray120c.py` | 8430 | `b411e854effc0b21af05ba81671dccdd66e919429d1116b5d4fa10c9df30e956` |

### 46.2 Commit与post-audit

唯一commit成功：

```text
commit = 3f8fb5c2f046ad5c75eab200005331acd5f2cc27
parent = 8cd04d847d42ff5c7bcf7501f46be97cbbef429d
subject = fix(workflow): clarify local calibration context
body = Remove the built-in Ray credential default and document the user-owned local calibration boundary.
changed paths = 13
insertions / deletions = 400 / 211
```

post-commit `diff-tree`恰好13项；commit tree全部为`100644`且内容SHA与PLAN exact；13项相对new HEAD无working-tree diff；index
为空。remaining worktree `git diff --check`通过。PLAN、FULL、EXECUTION_RESULT、PLANS、debug及所有unrelated user/Orchestrator
改动均未stage、未commit、未revert，状态与pre-stage ownership snapshot一致。

### 46.3 预算与停止点

```text
implementation/documentation/skill/test edits = 0
test/module/compile/CodeGraph executions = 0
git stage operations = 1
git commit operations = 1
push/tag/branch/PR = 0
network/device/credential/secret reads = 0
camera/Ray/strip/nonzero/Z0/E2/capture/formal/firmware/deployment = 0
```

本commit仅完成`REF-WORKFLOW-01`已验收diff的Git object finalization；不解锁P7、Z0、E2或formal。当前停止在Planner验收门。

维护性判断：本轮未改变实现结构，仅将Planner冻结并验收的单一context/credential ownership提交为exact tree；无新增复杂度或后续
重构需求。
