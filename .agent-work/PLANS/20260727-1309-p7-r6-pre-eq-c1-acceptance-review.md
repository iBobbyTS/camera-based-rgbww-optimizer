# REF-P7-18-C1 / pre-EQ offline acceptance review

**归档时间：** 2026-07-27 13:09 MDT

**Reviewed PLAN：** `P7-TD-B-R6-PRE-EQ-OFFLINE-EVIDENCE-C1`

**Reviewed PLAN SHA-256：** `e1baa5877e4d6b74b50dce92e7fa06e11af684bcb6f60bed985fd0f991e270f2`

**Execution handoff SHA-256：** `aa08b4ba9a2b5301880fa4097d3d557d22817b5bc63f54e4a88e4533907a2807`

**Reviewed FULL SHA-256：** `5fff0f9a11f4b1bdff6e25919f6f9c702458dd77ba360b6ebf73210063cb71c9`

**Planner decision：** `accepted`

**Completed tasks：**

```text
REF-P7-18-C1
REF-P7-18
REF-P7-19
REF-P7-20
REF-P7-21
```

## 1. Reviewed scope and method

Planner只读验收 C1 是否修复首次 package的三个明确缺口：

1. baseline-known private override名称被全文件扫描误报；
2. 11/12/13 artifact计数与terminal self-hash owner不一致；
3. Executer handoff把 machine fail误报为pass。

同时核对 pre-EQ implementation candidate、R5/首次 root immutability、13项 correction evidence、
secret/path/network fail-closed matrix、focused/full/static validation、exact五路径 checkpoint和 staged-clean
终态。没有重跑设备、实验、release、commit或科学分析。

## 2. Correction evidence

Unique correction root：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-r6-pre-eq-c1-offline/1e3b107b8fbfe97bae5624ef638c4883a0faee1d-20260727T190405Z
```

| Artifact / property | Evidence |
| --- | --- |
| Actual canonical JSON | `13` |
| Sorted JSON SHA ledger digest | `446a7b57513e78b319a3c7998b842b8c4a0d9b20c990bd225d96c0ee709297c5` |
| `validation-summary.json` | `045e8e098b2a2b4a852b16b6d77a2298f4f734295c955d5d32bab0d06f1f9ada` |
| `terminal-summary.json` | `9807e7307337780d555bcdee236c1c5a60ad7a880ef28336d94384703e1503cd` |
| `secret-path-scan.json` | `35f5480accdde7cd63584bb1eac0001cfe3566badb9282003fe39b6321bb50de` |
| Strict JSON | `13/13 pass` |
| Validation status/index | `pass`, indexed preterminal `11` |
| Terminal status/count | `pass`, canonical root `13` |
| Terminal self hash owner | `external_execution_handoff` |
| Secret scan | `pass`, `findings=[]` |
| Broad allowlist | `false` |

Phase owner正确区分：

```text
11 preterminal artifacts
+ 1 validation-summary referenced by terminal path/bytes/SHA
+ 1 terminal self externally hashed
= 13 canonical root JSON
```

terminal不递归自嵌自己的SHA；外部 handoff记录 terminal bytes `607` 与 exact SHA。

## 3. Findings closed

### REV-R6-PRE-EQ-001 — closed

Correction summary明确 `indexed_preterminal_count=11`，terminal明确
`canonical_root_json_count=13`、validation `1`、self `1`。独立枚举exact13且无extra。

### REV-R6-PRE-EQ-002 — closed

Root cause冻结为 `baseline_false_positive`。Scanner只有在 exact starting HEAD path、baseline blob和
occurrence count全匹配时，把既有名称分类为 `known_identifier_not_secret_value`。新增hunk/路径、baseline
drift、额外 occurrence、fabricated private value、environment serialization、hostname/IP/URL、repo外path与
symlink escape继续fail closed；value只记录redacted hash，不回显。

### REV-R6-PRE-EQ-003 — closed

C1 machine matrix检测到首次 handoff矛盾。新 truthfulness owner要求 handoff从 frozen terminal artifacts派生；
validation/terminal/scan均pass，handoff consistency `pass`、mismatches `[]`。

### REV-R6-PRE-EQ-004 — retained

首次 root与R5 root均未修改；first-root manifest canonical SHA
`9972d155cf9cb414371aec3376000adf414f2b4aee05b40d3bc90f61dcd40a99`。

## 4. Implementation and validation

Reported validation：

```text
original contract = 22/22 pass
new C1 matrix = 12/12 pass
focused = 146/146 pass
full suite = 607/607 pass
post-stage focused = 146/146 pass
post-commit focused = 146/146 pass
compileall = 0
P7 wrapper syntax = 1/1 pass
public synthetic validator = 22/22 pass
strict JSON = 13/13 pass
first root immutable replay = pass
R5 immutable replay = pass
secret/path/network scan = pass
git diff --check = 0
CodeGraph sync/targeted explore = pass
```

Orchestrator另用正确 unittest入口独立运行 new contract + C1 matrix：

```text
34/34 pass
```

此前误试 pytest因 `.venv`没有 pytest而无法启动；它没有执行测试、修改文件或改变 acceptance evidence。
Planner不把该命令当测试失败，也不声称本 review重跑了 full suite。

## 5. Focused checkpoint

```text
commit = 98de1a91c264d4b72c4a97fc499ae7d39a67dacc
parent = 1e3b107b8fbfe97bae5624ef638c4883a0faee1d
subject = fix(p7): prepare exposure-guarded td-b r6
staged after commit = empty
```

Exact five paths：

```text
config/hsi/p7-ray-td-b-exposure-policy-v2.json
src/camera_based_rgbww_optimizer/optimization/analyze_p7_thermal_diagnostics.py
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py
tests/test_p7_td_b_r6_contract.py
```

Changed-path list digest：

```text
fa5e7a416f4f77cb6313dfb2157e18f0e325a10783de860a3ed6b69f67674511
```

`.agent-work/**`、`advisor/**`与其他 pre-existing改动没有进入commit。

## 6. Scientific and safety decision

C1没有改变 observer、58 features、clipping threshold、near-noise/valid-pixel、covariance、joint coverage、
no-ambient statistic、A/D/B shutter、C candidates、EQ/R6 budget或600-second transient语义。

所有禁止调用均为0：

```text
device/network/.env/camera/capture/Ray/strip/light/all_off
release/predevice/readiness/E2/EQ-R6/formal R6/TD-C
retry/second correction root/first-root mutation/R5 mutation
firmware/deployment/destructive hardware
```

因此无需 Advisor科学决定。

## 7. Acceptance and residual risks

接受：

- `REF-P7-18-C1` evidence correction；
- parent `REF-P7-18`完整 pre-EQ umbrella；
- `REF-P7-19` exposure policy v2与 EQ runner/validator offline owner；
- `REF-P7-20` full Ray R6 validator/analyzer/downstream locks；
- `REF-P7-21` integrated validation与pre-EQ checkpoint。

Residual risks：

- state C仍 `pending_qualification`、formal shutter `null`；
- pre-EQ成功不证明曝光资格、settled、TD-B pass或device readiness；
- successor R3 release尚未生成且必须在EQ通过、selected policy finalize后生成；
- actual EQ是约20–40分钟的分阶段实机实验，仍需 4.GUIDE 明确要求的 Human stage checkpoint；
- Ray R6、strip、TD-C及以后继续锁定。

## 8. Exact next branch

唯一下一步是 `REF-P7-22` Human EQ-R6 checkpoint：

```text
request explicit Human confirmation for
P7-TD-B-RAY-C-EXPOSURE-QUAL-R6 only
-> stop
```

该 checkpoint PLAN不可供 Executer启动设备、创建EQ root或launch。Human明确确认后，Planner才可另写
一个 exact `REF-P7-23` execution PLAN。既有一般性“允许调用设备”或“恢复循环”不构成本科学stage的
明确checkpoint批准。

维护性判断：pre-EQ实现复用现有 thermal plan/measurement/analyzer owners，C1又把scan/index/status收敛为
单一合同；现有测试与独立34/34核对覆盖关键边界，当前无需进一步架构重构。
