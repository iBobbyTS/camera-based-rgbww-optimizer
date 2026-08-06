# Advisor GUIDE 4 当前阶段科学路线图

**Document status:** `TERMINAL_ENGINEERING_RUNTIME_ALIGNMENT_MISMATCH_REPORT_TO_HUMAN`

**Executable authority:** `false`

**Active task count:** `0`

**Current milestone:** `G4-RUNTIME-ALIGNMENT-TERMINAL-STOP`

**Frozen scientific prerequisite:** `config/hsi/p7-ray-td-b-exposure-policy-v2.json`，`qualified_1_2500`，SHA-256 `c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681`

**Accepted engineering reference:** `REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION`

`PLAN_FULL_MACHINE_CONTRACT={"schema":"g4_scientific_stage_plan_full_v4","document_status":"TERMINAL_ENGINEERING_RUNTIME_ALIGNMENT_MISMATCH_REPORT_TO_HUMAN","executable":false,"active_task_count":0,"active_task":null,"current_milestone":"G4-RUNTIME-ALIGNMENT-TERMINAL-STOP","frozen_eq_r6":"qualified_1_2500","accepted_successor_release":true,"accepted_predevice":true,"accepted_zero_readiness":true,"accepted_fresh_e2":true,"accepted_runtime_consumer_package_commit":"21754a3","allowed_next_action":"REPORT_EXACT_RUNTIME_ALIGNMENT_MISMATCH_TO_HUMAN_NO_EXECUTION","engineering_only_plan_budget_before_science":0,"engineering_only_plan_budget_consumed":1,"engineering_only_correction_budget":1,"second_engineering_package_allowed":false,"package_prepare_authorized":false,"formal_execution_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"td_c_authorized":false,"human_goal_complete":false,"guide_complete":false,"scientific_stage_complete":false}`

EQ-R6 `1/2500`、successor policy/release、predevice、zero/readiness 与 fresh E2 均已有 accepted/frozen evidence，不得重跑、补拍、重建或修改。runtime materialization/consumer chain 曾由四个真实测试体 `Ran 4 / OK` 并在提交 `21754a3` 接受；后续唯一 PLAN/PLAN-FULL runtime-alignment correction 已 terminal rejected：69 tests、83.091 s、exit 1、1 failure + 213 errors。exact mismatches 是 production import migration 移除了 `build_stage_gate_input` 仍需的旧 parser，触发 `NameError`，且新 parser wrapper 未加入 `__all__`。retry=0，engineering budget 已消耗 1，第二 correction/package 禁止。该结果没有 capture 或 science delta；Ray R6 保持 locked。Candidate 2 与所有 historical rejected candidate 仍只能作证据，禁止作为实现输入。

## G4-RUNTIME-ALIGNMENT-TERMINAL-STOP — exact mismatch 回报 Human（当前）

- **scientific_target:** 保持 GUIDE 科学输入与下一 Ray R6 目标冻结，同时向 Human 精确报告唯一 runtime-alignment correction 的 terminal engineering mismatch。
- **next_scientific_action:** 无可执行科学动作；仅 `REPORT_EXACT_RUNTIME_ALIGNMENT_MISMATCH_TO_HUMAN_NO_EXECUTION`，Ray R6 保持 locked。
- **science_delta:** `none`；69-test terminal engineering rejection、PLAN/PLAN-FULL 状态或 Git/evidence 都不是科学进展。
- **最小 engineering prerequisite:** 不再执行 engineering prerequisite。保留 exact mismatch：旧 parser 被 production import migration 移除导致 `build_stage_gate_input` `NameError`，新 parser wrapper 缺少 `__all__` export；不得修复、retry、重跑、开启第二 correction 或改换 package。
- **safety/authorization lock:** PLAN-FULL non-executable、active=0；package、formal、release consumption、device、network、camera、Ray、strip、capture、analysis 与 TD-C 权限全部 false。Ray R6 不得启动；只有新的 Human direction 才能改变 terminal stop，但本文件不推导任何新执行权。
- **acceptance evidence:** terminal evidence 固定为 69 tests / 83.091 s / exit 1 / 1 failure + 213 errors，且 exact mismatches 为 `build_stage_gate_input` 的旧 parser `NameError` 与新 parser wrapper 缺少 `__all__`；engineering budget consumed=1、retry=0、second package=false、science result=0。Human report 完成即停止，不创建 repair PLAN。

## G4-R6 — 完整新 Ray 16-frame acquisition 与 Ray-only analysis

- **scientific_target:** 依据 frozen EQ-R6 shutter 和 GUIDE exact sequence，取得 Ray-only operational-600 的完整新 16 帧并判断 quality、chronology 与 A-return history compatibility。
- **next_scientific_action:** 在新 unique root 按 exact `000..015` 顺序运行一次 formal R6；仅 16/16 quality pass 后运行 Ray analyzer。
- **science_delta:** 新的 16 张 Ray captures 及 Ray-only chronology/history analysis，或首次 hard-failure 的科学有效 negative result；出口为 acquisition fail、`stop_history_model_required` 或 `accepted_for_strip_entry`。
- **最小 engineering prerequisite:** 当前 terminal engineering stop 未解除；本 milestone 不可进入。
- **safety/authorization lock:** Ray R6 locked；formal、device、camera、Ray、capture 与 analysis 权限均为 false，不得创建 root、启动 visible-Terminal、连接设备或执行 capture。
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
