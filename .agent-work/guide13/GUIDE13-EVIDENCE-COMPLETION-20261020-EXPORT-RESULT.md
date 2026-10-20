# GUIDE13 既有证据定向补齐 — 导出结果（2026-10-20）

本机时间：2026-10-20 14:51（UTC-6）。全程纯离线：未操作设备/相机/Ray/灯带/网络控制接口，未新拍、未补做确认、未改旧结果、未生成 GUIDE14。

## 交付物

| 文件 | 位置 |
|---|---|
| 增量包 `GUIDE13-EVIDENCE-COMPLETION-20261020.zip` | `D:\rgbww-optimizer\guide13\package\` |
| 字节数 / 成员数 / SHA-256 | 1,034,922 / 360 / `8e8c5234c71e7c919cfcdf3348439efa9fa3c0838acf1268bc6b4a33af89d1ce` |
| CRC + 往返 | `testzip` PASS；重放报告解压回读 PASS |
| 外部 MANIFEST / VALIDATION / 本文件 | 与 ZIP 同目录 |

原始三包未复制（按 SHA 引用）：GUIDE13 原包 919ef2ad…（本地字节复核一致）、GUIDE12-COMPLETE 3ed20b16…、GUIDE12-COMPLETION 85a61c4e…（两者在 `.agent-work/guide12/` 本地复核一致）。

## 各请求项去向（全部落为明确终态）

**D1 矩阵与 RAW 索引** — `exported_existing` + 本次实测：626/626 CR3 本地重哈希全部匹配（0 缺失 0 读错）；`rawpy.rgb_xyz_matrix[:3,:3]` 逐帧提取，**全 626 帧唯一矩阵 `mtx_d7f573d010a0e041`，与 GUIDE12 旧矩阵逐位一致——由逐帧证据证明，不再靠假设**。`RAW_INDEX_COMPLETE.jsonl` 含采集/物理账本行哈希、sidecar 引用、重哈希时间与 rawpy 版本。ISO/光圈数值= `NOT_APPLICABLE`（计划为 implicit auto，sidecar 仅记快门秒；不装 EXIF 工具、不补拍）。

**D2 小运行文件与中断** — `exported_existing`：88/88 根补齐 `input-checkpoint.json`（含每次启动的 git commit+dirty+冻结输入哈希）与 `thermal-covariates.jsonl`；46 个 `-plan` 干跑 spec 根、全部 launch 日志、PRE-RUN 清单、campaign 结果笔记一并导出。`failure.json`/`wrapper-result.json`/`all-off-shell.json` = `not_created_by_runtime`（GUIDE13 运行器从不写这三类；两中断根的手动 all_off 证据在暂停 commit 0e71f6c/914da9d）。中断叙事（`INTERRUPTIONS.json`）：W13-B s2(7帧)→s2r-a(2帧假启动)→s2r-b(46帧)，UTC 间隔 19249.9s/737.1s；C13-D 主(56)→尾(7)，7505.2s；钟域规则如实记录（跨根只用 returned_at UTC）。`PAIRINGS_COMPLETE.json` 316 条 strip 配对（含跨根/跨暂停标志）；`PRIMARY_SECONDARY_QUALITY.jsonl` 626 帧三层质量 + 下发/回读 PWM + 冻结 code-duty 转换身份（f519dd5c 复核一致）。

**D3 计算来源** —
- C13-D：verdict 的 5 个 H/S 数值**全部从留存输入复现**（J⁻¹dz，最大差 0.0057）；但 **"10/10" 成员名单不可从留存记录复原**（J 可用低 SAT 点仅 7 个：5 门内、周期对 1/37 与 359/37 超门且 verdict 自己披露为边缘）；并披露：verdict 未使用已实测的 300/50 J，若按其 H75 式迁移套用，H300 轨道 S20/S37 将超 ±2°/±2pp（−5.09°/−12.48°）。H/S 步骤生成器 = `original_generator_not_retained`；CI/PI = `not_calculated`；所有跨锚 J 使用 = `transfer_validation_not_performed`。
- C13-B：H0/S50 的 dH=0.41°/dS=−1.05pp **精确复现**（0.4064/−1.0493）；H300/S50 两块实测 dz 方向与"J 理论方向错误"结论可从帧复算；reference_drifted 三目标的源级 Ray 值已导出（基线口径如实注明）；资格命令 `cw132/ww1968/r4095/g180/b480` 全库仅 1 次物理观测（开发选择帧）→ 确认 = `not_acquired`。
- W13-A/B/C：corrected LUT v2 **按文档规则重建 70/70 全同**（27 替换=23新+4重验）；W13-B **20 节点三配对确认精确复现**（s1=10+s2=2+s4=8），三观测身份（capture id）入账；W13-C v2 回归调用参数 = `original_generator_not_retained`（脚本硬编码 v1 LUT），输出留存并在重放中做命令身份核验；C13-C 逐 Hue 父源表 + C124 采用档位导出，无合格映射处不填测得值。报告 ~236/~35 等计数已注口径（~236 无留存分母定义，账本事实 308/296/180 并存；~35=strip 帧精确一致；W13-B 48+55+16+27+3 与账本一致）。
- 70 白光节点引用表：随 LUT 重建文件输出（最终命令、变更位、证据指针、W13-B 跨会话状态、CI/PI=not_calculated）。

**D4 源码版本绑定** — 88 根的 git 绑定共 N 个 commit（见 DEPENDENCY_STATUS.json），39 个模块（顾问点名依赖 + 原包 source 传递闭包）逐一绑定到 当时的commit 字节；与两基础包/原包成员字节相同处记 `(ZIP SHA, member, member SHA)`；**任何包都没有的 10 个版本已复制进增量 source/**（含 guide12.py、guide12_w123.py、p7 执行 owner、camera_remote、paths）。打包脚本与排除规则随包（原 20261019 打包器 + 本次全部构建/再分析脚本）。

**第 5 节离线重放** — 干净目录解压三包 + 增量：9 项中 8 项 PASS（第 7 项 PASS_WITH_DISCLOSURE，第 9 项 NOT_APPLICABLE——留存结果无生成的 CI/PI 字段，不事后安装统计模型）。数值核验：W13-B s1 全部 24 配对 E 复算 **max |ΔE| = 0.0**；W13-A 冷/暖块候选 E 复现到 1e-4；C13-A 三目标中心均值复现到 1e-6；矩阵读取全部替换为已验证逐帧引用（无 rawpy 依赖）。

## 未找回项（合法终态，均已写入 MISSING_OR_UNIDENTIFIABLE.json）

请求附件 5 个索引文件本机未找到（`lost_after_documented_search`）→ 已在 `reconciliation/` 提供本地等价推导（成员索引 2158、运行索引、帧身份、471 处 path+sha 解析、源依赖候选）；ISO/光圈数值、历史温度、H0/S50 确认、~236 分母等按 `not_recorded`/`not_acquired` 登记。

## 科学备注（给 Advisor）

本增量不改变任何原结论；但 C13-D 的"10/10"表述建议在审阅中按本增量的逐点表重新表述：可复现的门内 J 点为 5 个（H60×3 + H75 族×2），周期对超门为 verdict 已披露事实，H300 轨道在 H/S 语义下的表现依赖是否接受 300/50 J 的跨 SAT 迁移——该迁移未被任何实验验证。
