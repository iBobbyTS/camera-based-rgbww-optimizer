# Advisor/3 之后的提交与证据索引

## 1. 边界说明

`advisor/3` 已报告的最后科学状态是 P7-R1 repeatability/reference instability。对应代码历史中，
`fbe65b2` 已记录该 R1 结果；后续相关工作从 `5572aa2` 开始。当前 `HEAD` 为：

```text
1e3b107b8fbfe97bae5624ef638c4883a0faee1d
```

共有 47 个相关提交。`9c804ab` 同时打包了 `advisor/3`、早期 `advisor/4` 草稿、camera bridge 和已经进行中的
thermal/TD-B 资料，所以它不是可靠的正式汇报分界；主报告已按执行语义重新纳入全部任务。

## 2. 完整相关提交序列

### 2.1 Thermal diagnostics 与 TD-A

| Commit | Subject |
| --- | --- |
| `5572aa2` | `feat(p7): close thermal diagnostic evidence contracts` |
| `dd9c1a4` | `docs(p7): record exposure-start adapter gap` |
| `cb9db30` | `feat(p7): add local v2 capture timing evidence` |
| `8689da7` | `fix(p7): harden local v2 timing evidence` |
| `f788b8d` | `docs(p7): record r0c validation evidence` |
| `3da1304` | `docs(p7): align final r0c validation evidence` |
| `c1c273a` | `docs(p7): clarify r0c artifact provenance` |
| `18408d0` | `docs(p7): record td-a offline entry blocker` |
| `3cbc72a` | `fix(p7): bind thermal capture settings` |
| `7874e7b` | `docs(p7): record td-a r0d evidence` |
| `d5cc596` | `feat(p7): finalize td-a completion evidence` |
| `6e4d108` | `docs(p7): record td-a e0 evidence` |
| `ae98e1c` | `docs(p7): record td-a ray wrapper failure` |
| `960484e` | `fix(p7): close td-a wrapper evidence gaps` |
| `1c592c9` | `docs(p7): record td-a w0 evidence` |
| `8711083` | `docs(p7): record td-a ray timing failure` |
| `0344a46` | `fix(p7): use observed elapsed for thermal timing` |
| `4901f81` | `fix(p7): close timing v2 review gaps` |
| `8b3f24f` | `docs(p7): record pending TD-A authorization` |
| `ed732b5` | `docs(p7): record TD-A Ray run start` |
| `a0cae5c` | `docs(p7): record TD-A completion` |

### 2.2 Developer dwell、TD-B setup/production 与 evidence owner

| Commit | Subject |
| --- | --- |
| `7e8ebaa` | `feat(p7): add developer dwell TD-B offline contract` |
| `2030b9f` | `feat(p7): add TD-B exposure setup contract` |
| `87f1e32` | `feat(p7): close TD-B production orchestration` |
| `e025b38` | `docs(p7): record TD-B setup gate failure` |
| `0deac80` | `fix(p7): canonicalize TD-B prerequisite identity` |
| `35db043` | `docs(p7): record TD-B setup finalization failure` |
| `9c804ab` | `fix(camera): trust Canon MakerNote exposure metadata` |
| `78099ef` | `docs(plan): define p7 td-b ambient ledger correction` |
| `8b80c87` | `fix(p7): close td-b ambient and physical ledgers` |
| `a599767` | `docs(plan): advance p7 td-b lineage formal run` |
| `3db7ae2` | `feat(p7): add lineage-qualified TD-B release` |
| `b38caa4` | `fix(p7): dispatch lineage formal release first` |
| `c4a2724` | `fix(p7): retain sidecar evidence on rejected captures` |
| `e5cd079` | `fix(p7): preserve sidecar failure evidence atomically` |
| `fa6c95d` | `fix(p7): bind td-b formal statistic owner` |

### 2.3 Orchestration、local-lab policy、lineage 与 public protocol default

| Commit | Subject |
| --- | --- |
| `f92cd47` | `docs(workflow): add full guide plan reference` |
| `8cd04d8` | `docs(workflow): assign roadmap to orchestrator` |
| `3f8fb5c` | `fix(workflow): clarify local calibration context` |
| `db85e18` | `chore(workflow): checkpoint orchestrator state` |
| `0387bcf` | `test(p7): isolate lineage baseline fixtures` |
| `6c42c6e` | `fix(p7): qualify frozen agents lineage policy` |
| `0c878cb` | `fix(p7): bind workflow lineage paths exactly` |
| `a87b09f` | `fix(p7): bind cleanup test provenance exactly` |
| `e7ccdda` | `fix(ray120c): restore public protocol default` |
| `52a7168` | `fix(p7): bind public default successor lineage` |
| `1e3b107` | `fix(p7): add evidence-only lineage qualification adapter` |

完整 SHA 可由 `git rev-parse <abbrev>` 在当前仓库唯一解析。关键执行 checkpoint 已在主报告和 retained artifact 中使用完整 SHA。

## 3. 仅看提交无法覆盖的外置 work packages

Git 提交列表不包含 `/Volumes/4T/temp/rgbww-optimizer` 下所有一次性 validation/evidence package，也不包含当前未提交的
Planner review archives。完整执行顺序必须同时查看 `.agent-work/EXECUTION_RESULT.md`：

| Sections | Package family |
| --- | --- |
| 1–22 | thermal contract、timing、TD-A gates 与实际 acquisition |
| 23–36 | TD-B R0/R0S/E0X/PATH/CANON/F0A/F0B/C1/C2/C3/E1/L1 |
| 37–49 | E2 root/hostname/progressive corrections、workflow context、baseline lineage |
| 50–82 | Z0-R2/R3/R4、real zero-only、Wi-Fi 恢复后的 REAL-R3 与 E2 readiness |
| 83–100 | lineage qualify、policy/path/provenance、predevice oracle、Terminal/env accounting |
| 101–118 | public-default implementation、successor lineage、evidence-only R1/R2 harness |
| 119–125 | R2 D1–D5 与唯一 lineage release generation |
| 126–132 | FORMAL-R5 launcher、activation、Human Terminal dispatch、liveness、terminal audit |

## 4. 关键 retained evidence

### 4.1 TD-A

| Artifact | Path / SHA-256 |
| --- | --- |
| Ray run | `/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-ray-debug` |
| Ray analysis | `13fac6336e95e6900003ff5ced50051b1b9ce2102af9d95729117eab3f46f69d` |
| strip run | `/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-strip-20260722-001426` |
| strip analysis | `3d265f9e57e92552f7dfb2b28c455373eb655911dec2e4e4bb8c59c013302155` |
| paired analysis | `99550214c619160b39cbf7f393e6b8dc3a5b3feae8f91d0a1765c272283c3160` |
| final independent zero | `b83d96e000293f7413372b297b97a49fc676f437e099f8ad6d52f2b401824dc2` |

### 4.2 Early TD-B corrective evidence

| Package | Evidence |
| --- | --- |
| F0B-R1 C1 | `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-r1-offline/20260723-142254/validation-summary.json` |
| F0B-R1 C2 | `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-r1-c2-offline/20260723-202736/validation-summary.json` |
| F0B-R1 C3 | `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-r1-c3-offline/20260724-061143/validation-summary.json` |
| C3 E1 | `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-r1-c3-e1-offline/20260724-172355/validation-summary.json` |
| C3 L1 | `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-r1-c3-l1-offline/20260724-180618/validation-summary.json` |

### 4.3 Accepted R2 lineage release

```text
release root = /Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r2-r1/20260726T200000Z
setup-lineage-release SHA-256 = 36a2ecd7c68bda35b4f722548b3c7a3bbafc880fc012af28c8fc501eed19d519
generation = 1/1
production subprocess = 1/1
release consumption = 0
device / formal = 0
```

### 4.4 FORMAL-R5

```text
root = /Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-r5/formal-r5-1e3b107-20260726T220000Z
failure.json = 2984ec745f2b7cddad1549535b730ae75397cdf7f1fa8602f71010f6613a9a65
011-ray-c-t60.patch-statistics.json = 98b792f0ef2d89718102c054fa4c4ad43206cf3cce82855d9c67900b6223a8be
run.json = dfba25366d6deb093170ceb21ee2fa259143f0da4ba0628216de0d6f23f03079
physical-returns.jsonl = d6569f121c7a31ac1dfb427fe2de1dccc8b46fe3be6e4f3d7ba007d8019e6e02
terminal-audit.json = 4bee490fa83bad33830cf5e8941ccc7fa0ca83191903639c617af5fe9d5e7d79
returned-summary.json = 5e97023d84d91f0037b096bf84e1102a8b786aa174a383b65087669fb5401955
all-off-python.json = 982cee95d59cc18ae1270fdc02f3c8947008796593fa22deb07f925ebd5327dc
all-off-shell.json = 3c4ea47739e009cef740791e86195f8e76ec8ddb805b3a937efee75c01cf3381
```

## 5. 当前 orchestration evidence

| File | SHA-256 at this audit cutoff |
| --- | --- |
| `.agent-work/PLAN.md` | `e28a1d4cd8c0af5a8dd2d3bf3eb7dcbf7d6b57900b62cf99561fd42f88f09bf9` |
| `.agent-work/FULL_PLAN_REFERENCE.md` | `cba7c8d66b9aacbbf0b431e7dc8972f5f37699a94f125d6fd19052cadfec992d` |
| `.agent-work/EXECUTION_RESULT.md` | `cc4627828f97d41951945561bf82a22c491693eb9e894957d9964da08d4f1ff9` |

这些文件在本次 Advisor audit 整理中只读；未修改 GUIDE、PLAN、FULL 或 retained evidence。
