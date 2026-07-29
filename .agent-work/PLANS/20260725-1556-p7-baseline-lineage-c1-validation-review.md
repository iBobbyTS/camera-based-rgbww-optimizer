# REF-P7-BASELINE-01 / P7-BASELINE-LINEAGE-TEST-C1 Planner验收归档

**验收时间：** `2026-07-25T15:56:49-0600`

**验收角色：** Planner

**被审 active PLAN SHA-256：**
`ef4d73ba033c5782dfd203ee7b46cef73fcf61e543e1341a590ee8cd6326220f`

**Planner决定：** `accepted_lineage_test_contract; validation_only_full_rerun_required`

**精确下一分支：** `REF-P7-BASELINE-01_C2_VALIDATION_ONLY_FAKE_RAY_ENV_AND_EXACT_COMMIT`

## 执行范围与结果

Executor继续只修改`tests/test_p7_thermal_diagnostics.py`，完成C1合同修正：writer、直接validator与fake formal sentinel使用同一
test-local changed-path fixture；current-HEAD test准确断言`AGENTS.md=prohibited_or_unreviewed`且进入prohibited，
`.agent-work/FULL_PLAN_REFERENCE.md=planner_or_execution_audit_only`且不进入prohibited。production classifier、allowlist、checkpoint、
release schema、formal runner与科学合同均未修改。

Evidence root：
`/Volumes/4T/temp/rgbww-optimizer/p7-baseline-lineage-r1-c1/20260725T215156Z/`

## Canonical evidence与Planner验收

- focused lineage恰好一次：`4/4 pass`，1.281s，log SHA-256
  `6c3fc13cbd49dfc3da811545d03e90fa42cc85805cf8579a92add81964dddd5b`。
- 完整TD-B module恰好一次：`70/70 pass`，6.668s，log SHA-256
  `6c596d7dcb72372f0c04919b0418145662402474643e9c22884923433f22d977`。
- full suite恰好一次：`555/560`，原两个lineage errors已消失；full log SHA-256
  `658a823241e1ee03e233feb1d5edc441eb0c4bcc23aa148a36c1d3b46d638f53`。
- 唯一test diff current bytes/SHA-256：`153769` / 
  `1bca571c42f5de51a27d183b831e75f8b98c4484ecbeab5f64a491a7f480a912`；本归档以hash为冻结owner，下一PLAN重新记录live bytes。
- `EXECUTION_RESULT.md` at review bytes/SHA-256：`179588` / 
  `c2b549d9438858e10118961e91aea4886397d6ccfc596d0a93edb2ba1b6881a0`。
- production owner hashes保持`7606ded631...93fc`与`86a2c99924...669a`；HEAD保持
  `db85e18b9738cfbe973187671111b6460388b385`，index为空，test path `git diff --check`通过。

## Full-suite五个failures归因

full runner为证明actual credential read为0而unset`AMARAN_OPENAPI_SECRET`。五个失败均来自既有measurement tests的fake cleanup路径：
`OpenAPISettings.from_env()`在fake Ray cleanup前要求secret，导致run/cleanup assertions失败。它们不经过C1 lineage helper或classifier；
此前workflow验收中使用runtime-generated fake 32-byte key时，这五项已通过，full仅剩现已被C1消除的两个lineage errors。

新增current-HEAD test使当前suite总数为`560`，因此旧PLAN的`559/559`目标已过时。正确下一验收是保持所有文件不变，在新process内部用
`bytes(range(32))` runtime生成fake key并设置`AMARAN_OPENAPI_SECRET`，完整full suite预期`560/560`。

## 决定与下一分支

接受C1 lineage test合同与`4/4 + 70/70`，不要求修改其他measurement tests或production credential handling。当前仍未stage/commit；
下一包严格validation-only：test/source hashes必须exact，不能编辑文件；只运行一次带runtime fake key的full suite。若`560/560`，完成
diff/path/offline audit后只stage并commit唯一test path；否则保留证据回Planner。

network/device/.env/actual credential/camera/Ray/strip/Z0/E2/capture/formal/firmware/deployment与git stage/commit本轮均为0。
