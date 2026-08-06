# Advisor GUIDE 4 当前阶段科学路线图

**Document status:** `RAY_R6_SCIENTIFIC_ACTION_WAITING_HUMAN_RELEASE_NO_ACTIVE_PLAN`

**Executable authority:** `false`

**Active task count:** `0`

**Current milestone:** `G4-R6-SCIENTIFIC-ACTION`

**Frozen scientific prerequisite:** `config/hsi/p7-ray-td-b-exposure-policy-v2.json`，`qualified_1_2500`，SHA-256 `c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681`

**Accepted engineering reference:** `REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION`

`PLAN_FULL_MACHINE_CONTRACT={"schema":"g4_scientific_stage_plan_full_v3","document_status":"RAY_R6_SCIENTIFIC_ACTION_WAITING_HUMAN_RELEASE_NO_ACTIVE_PLAN","executable":false,"active_task_count":0,"active_task":null,"current_milestone":"G4-R6-SCIENTIFIC-ACTION","frozen_eq_r6":"qualified_1_2500","accepted_successor_release":true,"accepted_predevice":true,"accepted_zero_readiness":true,"accepted_fresh_e2":true,"allowed_next_action":"WAIT_FOR_EXPLICIT_HUMAN_FORMAL_DEVICE_RELEASE","engineering_only_plan_budget_before_science":0,"engineering_only_plan_budget_consumed":1,"package_prepare_authorized":false,"formal_execution_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"td_c_authorized":false,"human_goal_complete":false,"guide_complete":false,"scientific_stage_complete":false}`

EQ-R6 `1/2500`、successor policy/release、predevice、zero/readiness 与 fresh E2 均已有 accepted/frozen evidence，不得重跑、补拍、重建或修改。历史 formal attempt 的 captures 为 0，是工程 invalidation，不是科学质量结果。当前唯一 engineering blocker 是 accepted tree 上 runtime materialization/consumer chain 尚未通过已 inventory 的真实测试体；Candidate 2、所有 historical rejected candidate 与无效 selector 记录只能作证据，禁止作为实现输入。R5 11 帧仍 diagnostic-only，禁止 old/new pooling。

## G4-FORMAL-ENTRY-RUNTIME-CONSUMER-CLEARANCE — 解除 formal 前唯一工程 blocker（当前）

- **scientific_target:** 让 GUIDE 要求的完整新 Ray R6 16-frame 实验成为下一项可执行科学动作；不再重复 EQ-R6 或扩大 owner/framework/provenance 设计。
- **next_scientific_action:** `P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6`（本 milestone 完成后直接进入）。
- **science_delta:** 真正解锁 Ray R6 16-frame acquisition；本 milestone 的代码、测试、checkpoint、release 或 Git 记录本身不计科学进展。
- **最小 engineering prerequisite:** 使用已完成 inventory 的真实 class/method/module identities，在 accepted tree 上批量验证并最小修复 runtime materialization/consumer chain，使既有 successor release/readiness 能安全到达 formal capture；仅保留现有 owner，禁止创建新的 owner-seam candidate、framework、attestation/provenance 层或泛化 coordinator。不得修复、重试、读取或复制 Candidate 2/历史 rejected candidate。
- **safety/authorization lock:** 当前 package、release consumption、formal、device、network、camera、Ray、strip、capture 与 analysis 全部未授权。active PLAN 必须单独声明 exact release/root/launch bounds；不得由 release eligibility 推导 Human authorization。selector 不进入真实测试体时立即停止，只做一次 read-only reconciliation，不猜 selector。
- **acceptance evidence:** 已 inventory 的精确测试身份与实际测试体结果、runtime materialization/consumer chain targeted evidence、accepted-tree source/test scope、既有 successor/readiness artifact hashes 的只读绑定、`git diff --check` 与 focused accepted commit；仅当这些证据证明下一 PLAN 能安全释放一次 Ray formal launch 才算解锁。一个 engineering-only PLAN 后仍有新 blocker，才允许一次额外 bounded correction；第三次禁止。

## G4-R6 — 完整新 Ray 16-frame acquisition 与 Ray-only analysis（等待 Human formal/device release）

- **scientific_target:** 依据 frozen EQ-R6 shutter 和 GUIDE exact sequence，取得 Ray-only operational-600 的完整新 16 帧并判断 quality、chronology 与 A-return history compatibility。
- **next_scientific_action:** 在新 unique root 按 exact `000..015` 顺序运行一次 formal R6；仅 16/16 quality pass 后运行 Ray analyzer。
- **science_delta:** 新的 16 张 Ray captures 及 Ray-only chronology/history analysis，或首次 hard-failure 的科学有效 negative result；出口为 acquisition fail、`stop_history_model_required` 或 `accepted_for_strip_entry`。
- **最小 engineering prerequisite:** G4-FORMAL-ENTRY-READINESS accepted；active PLAN 固定 A/D/B exact frozen shutters、C=`1/2500`、16-frame physical cap、launch=1、retry=0、no auto-exposure/reacquire、strip zero 与 cleanup。
- **safety/authorization lock:** 当前等待明确 Human formal/device release；在 release 到达并写入 active PLAN 前，不得创建 formal root、启动 visible-Terminal、访问 Ray/相机或 capture。获得 release 后仅该 active PLAN 可释放一次 visible-Terminal Ray/camera formal operation；任一 capture failure 即终止、strip 保持 zero，不得复用 R5 frame、从中间恢复或重试。
- **acceptance evidence:** formal root、每帧 CR3/sidecar/hash/MakerNote/state/readback/quality、physical chronology、双 cleanup/final-zero/terminal seal，以及 600 s return-anchor compatibility 与 `steady_status=not_demonstrated` chronology report。

## G4-STRIP-TD-B — 条件执行新 strip 16-frame TD-B

- **scientific_target:** 仅在 Ray R6 quality 与 history pass 后，测量 strip 在同一 operational-600 transient 合同下的 TD-B quality、chronology 与 A-return history。
- **next_scientific_action:** 在全新 root 运行 strip TD-B 16 帧及 source-specific analyzer。
- **science_delta:** 新的 16 张 strip captures 及 strip chronology/history analysis，或科学有效 hard-failure evidence，决定 combined gate 是否可进入。
- **最小 engineering prerequisite:** Ray R6 已 `accepted_for_strip_entry`；只复用 frozen strip command、observer、exposure/setup、no-ambient statistic 与 600 s semantics，不添加泛化实现。
- **safety/authorization lock:** Ray R6 未通过时不可激活；active PLAN 固定 source isolation、16-frame cap、retry=0、abort、cleanup。若需改变 observer/threshold/feature/exposure/command，停止并请求 Advisor scientific decision。
- **acceptance evidence:** 新 experiment/root、16/16 quality 或 sealed failure、A-return anchors、chronology、source/readback/physical ledger、Python/shell cleanup/final-zero；旧 R5/R6 frames 仅 immutable-manifest reference，禁止 pooling。

## G4-COMBINED-TD-B — operational-600 combined analysis

- **scientific_target:** 综合 Ray 与 strip 的 accepted TD-B evidence，判定 operational-600 envelope，并解锁 TD-C core 或形成科学有效 negative result。
- **next_scientific_action:** 运行 GUIDE 定义的 combined analyzer，生成 `p7-operating-envelope-v3.json` 与 `p7-td-b-operational600-analysis-v1.json`。
- **science_delta:** combined pass 才解锁 TD-C core；combined fail 将 `REF-P7-05` blocked 且 TD-C locked。任何结果都必须保留 `selected_fixed_time_transient_not_proven_steady`，不得声称 steady 或 TD-A pass。
- **最小 engineering prerequisite:** Ray 与 strip 两个 source 的 acquisition、quality、history、cleanup 与 immutable identity evidence 全部 accepted；仅执行 GUIDE 已定义的 combined computation。
- **safety/authorization lock:** 仅允许离线 analysis；不授权 TD-C execution、sentinel、boundary、holdout、Gate-6、P8 或 default LUT/runtime install。
- **acceptance evidence:** 两个 named artifacts 及 hashes、双 source 16/16 与 history inputs、exact exposure/source/physical ledger checks、no-pooling assertion、明确 pass/fail 与 TD-C lock/unlock 状态。
