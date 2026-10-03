# GUIDE12 N2 会话 2 Ray120c 无物理出光故障报告（2026-10-03）

分类：**DEVICE_OR_SAFETY_FAILURE**（设备状态异常，安全方向——灯灭而非误亮）。
未决问题：Ray120c 断电重启后 API 应答正常但物理无光的确切物理原因（需人工检查）。
处置门：**HUMAN_GATE_REQUIRED**（需要物理干预：检查 Ray120c 供电/开关/与 Amaran Desktop 的链接）。

## 事件概要

- 会话 2（`formal-n2-session2`，2026-10-03 15:45–20:37 UTC）按冻结计划完整运行：
  24/24 formal 帧、24 张 CR3 回传、清理 pass、run.json `status=complete`。
- 但**全部 12 个 Ray 帧为实拍黑帧**：RAW 域全平面 max≈531–534（黑电平 512 + 噪声），
  而会话 1 同名帧 max 9258–16383。12 个 strip 帧逐态正确（两会话一致）。
- 质量直方图：8 pass（全部 strip 白态）+ 16 near_noise_only（8 Ray 白态 + 4 Ray 彩态
  + 4 strip 彩态；strip 彩态的 near_noise_only 与会话 1 相同属预期记录）。
  N2 校验器按记录态放行是设计行为，但 Ray 白态黑帧不是科学数据——Ray 参考态
  **物理上从未发生**。

## 证据链（按判定顺序）

1. **会话 2 Ray 帧黑、strip 帧正常**：`measurements/*.patch-statistics.json`
   逐平面统计；Ray 帧 trimmed_mean≈0、observed_max≈531–534 全状态一致；
   strip 3200/0 c1 帧平面 max 7046–10724 健康。
2. **黑帧是实拍而非陈旧帧**：三帧不同状态 Ray CR3（1800c1 / 3200c1 / 20000c1）
   图像阵列互不相同（max|diff| 32–33 = 独立读出噪声）→ 相机在会话期间是活的；
   交错的 strip 帧逐态正确（000/005/013…）排除相机整段故障。
3. **API 状态机与物理输出解耦**：会话内每条 `set_cct`（含 intensity 1000=100%）
   均返回 code 0，独立 `get_cct` 读回与命令一致；但相机实测零光。
4. **判别诊断**（`D:/rgbww-optimizer/guide12-n2/diag-ray-emission-20261003/`，
   20:41–20:44 UTC，每次点亮 ~6 秒 @20% 强度，共 4 帧 CR3）：
   - A：CCT 5600/gm100/INT200 → RAW max 534（黑）
   - B：HSI 240/100/INT200 → RAW max 534（黑）
   - C：全灭对照 → RAW max 534（黑，符合预期）
   - D：1/4000 快门判别 → RAW max 534（黑；证明各帧为独立实拍）
   - 结论：**CCT 与 HSI 两模式均无物理出光**；相机桥全程健康（D 与 A 内容同为
     黑帧且各帧噪声独立，此前"相机回放陈旧帧"的中间假设被 RAW 域数据推翻）。
5. **API 状态存活于应用侧**：HSI 槽位跨 10–12 小时断电仍记忆会话 1 阶梯的
   hue 240 → OpenAPI 状态模型在 Amaran Desktop（工作站本机回环）侧，
   灯本体断链时应用仍正常应答。

## 最可能根因（待人工确认）

灯本体未与 Amaran Desktop 建立实际链接：断电重启后未重新配对/灯未真正上电/
物理开关未开，Desktop 以本地状态模型一致地应答全部命令。确切原因需物理检查。

## 处置

- **会话 2 根保留**（不覆盖、不重跑同根、不并入任何统计）：strip 半程帧数据有效
  但 §3.2 配对设计（同会话同状态 Ray/strip 成对）已被破坏。
- Ray 物理恢复并经一次出光验证后，以**全新根**重跑会话 2（fresh attempt；
  实质修正 = 物理恢复 + 出光预检，非盲重试）。
- 会话 2 的会话分隔证据（断电 10–12h + generation=1 重启证据，提交 07c5284）
  仍然有效，适用于重跑。
- 后续会话运行前增加 Ray 出光预检（1 帧 RAW 域判读）作为启动门槛，
  防止整会话黑帧浪费（~5 小时）。

## 清理与零态（故障后确认）

- Ray：CCT 5600/gm100/intensity 0 读回确认；HSI 240/100/intensity 0 读回确认。
- 灯带：commanded state 全零（generation 51）读回确认。
- 相机：闲置（无未完成传输）；诊断 4 帧 CR3 已归档于诊断目录。

## 工具注记（曝光判读教训）

`frame_exposure` 的 `rendered_rgb_postprocess` 域会把全黑帧归一化渲染为
"classification: normal" 且均值看似很亮（R 16445 等），四帧统计逐位一致即此伪影；
**黑帧判别必须用 RAW 域**（rawpy `raw_image` max ≈ 黑电平 512+噪声）。
候选小改进：frame_exposure 在 RAW 域 max 接近黑电平时强制输出 dark 分类。

## science_delta

- 会话 2 尝试本身：Ray 半程设备 void，非有效科学阴性；strip 半程帧为有效测量
  但不构成 §3.2 会话单元。会话 2 整体计为设备失败，等待恢复后重跑。
- 会话 1（36/36 认证）不受影响。

## Git / 工件

- 失败时 HEAD：`07c5284`（工作树干净）。
- 原始载荷保留于 `D:/rgbww-optimizer/guide12-n2/`（会话根 + 诊断目录），
  不入 Git；本报告与既有证据文件入 Git。
- 诊断工件 SHA-256（CR3）：
  - A `a92073c0ee871ae3d30b9a1a675e7f0934d9b866322bf1350212e42f9aa67b1f`
  - B `78fb5113dd1c975345e4f376d7188dcbc3223b1c8a2a3b770804137d3005c6a7`
  - C `781a6e071a951991e3fbaedcd12d1bfd401986e6f38403ab1dfa77907ae830cf`
  - D `39fc06f49a7650d6093f6ed453b953e63979ab9d4e4d91ed0650ed97255cee23`
