# REF-P7-BASELINE-01 / P7-BASELINE-LINEAGE-TEST-R1 Planner验收归档

**验收时间：** `2026-07-25T15:39:51-0600`

**验收角色：** Planner

**被审 active PLAN SHA-256：**
`b4b1c10ebb924bdd4daa5c4b4359b26e1be2764589725592daad0a6b3bba3770`

**Planner决定：** `rejected_test_contract_mismatch; bounded_test_only_correction`

**精确下一分支：** `REF-P7-BASELINE-01_R1-C1_TEST_CONTRACT_CLASSIFICATION_CORRECTION`

## 执行范围与停止点

Executor只修改了PLAN授权的`tests/test_p7_thermal_diagnostics.py`，未修改production、FULL、GUIDE、docs、archives、debug或其他路径；
未stage/commit、未访问network/device/credential。focused four cases恰好运行一次，结果为`1 pass / 1 error / 2 failures`，按计划停在
Planner门，未运行TD-B完整module或full suite。

Evidence root：
`/Volumes/4T/temp/rgbww-optimizer/p7-baseline-lineage-r1/20260725T213655Z/`

## Canonical evidence

| evidence | bytes | SHA-256 |
| --- | ---: | --- |
| `EXECUTION_RESULT.md` at review | 175462 | `ea6f017e6c09942a82a4276aa9c739b27028fc18d397f97b6126953634c53351` |
| focused stdout | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| focused stderr | recorded in section 47 | `820d7a68c3473f9f2caef7c0561f048ee145c177634bf6b6952fbf5cccac5a37` |
| focused exit record | recorded in section 47 | `c280dd348441f0a131ab4032a44bd96bd33003114155f2ed21ec4399036f37cd` |
| changed test path | 152405 | `075105b1125ce36b7fbe26a6b4a13b4fc923bdab167c752842f75641b26f8b61` |

## Planner独立结论

1. 三处 release construction 已使用`changed_paths_fn`注入最小allowed fixture，但success test后续直接调用
   `validate_td_b_setup_lineage_release`，没有传入同一`changed_paths_fn`；validator因此重新读取真实current HEAD并抛出
   `TD-B setup current lineage candidate differs`。这是现有test-only seam可修复的合同遗漏，不需要production改动。
2. production classifier的实际合同为：`.agent-work/*`分类为`planner_or_execution_audit_only`，不进入`prohibited_paths`；`AGENTS.md`
   仍分类为`prohibited_or_unreviewed`并进入`prohibited_paths`。原PLAN错误要求FULL path进入prohibited，因此导致baseline test failure。
3. 该分类是有意的audit/provenance policy，不应为满足测试而修改production classifier或扩大TD-B allowlist。正确测试应显式断言：
   `AGENTS.md`在`prohibited_paths`，`.agent-work/FULL_PLAN_REFERENCE.md`不在`prohibited_paths`且其classification为
   `planner_or_execution_audit_only`。
4. 当前HEAD保持`db85e18b9738cfbe973187671111b6460388b385`；workflow context commit、production source hashes与FULL均未漂移。

## 决定与下一分支

拒绝本轮“测试合同已通过”的结论，但不升级为production classifier correction；建立一个仍只修改
`tests/test_p7_thermal_diagnostics.py`的bounded C1：为validator补齐同一注入fixture，并按实际audit classification改写baseline断言。通过
focused后才允许运行TD-B完整module与full suite；任何production classifier/allowlist、科学合同或设备需求都必须停止并请求Planner。

维护性判断：问题完全位于测试fixture注入和断言语义，production classifier已有单一owner且行为正确；不需要架构重构或Advisor介入。
