# Advisor handoff — GUIDE 4 Ray R6 history fail

## 请求

请 Advisor 基于本次完整新 Ray R6 的有效科学负结果，决定下一步应采用的
history/thermal model 或新的有界科学实验。当前 GUIDE 8.3 已规定在 Ray history
fail 时停止，因此本轮不请求工程架构、门禁或重采建议。

## 科学结论

```text
science_delta = valid_ray_r6_history_negative
status = history_dependent_at_operational_dwell_600
formal_pass = false
quality = 16/16 pass
return_anchor_history = fail
steady_status = not_demonstrated
operational_endpoint_600_valid = false
```

唯一 blocking pair：

| left | right | whitened score | guarded limit | decision |
| --- | --- | ---: | ---: | --- |
| A0 | A_after_D | 4.2731286812 | 9.5439242182 | pass |
| A0 | A_after_B | 8.8556161492 | 9.5439242182 | pass |
| A0 | A_after_C | 11.3712740731 | 9.5439242182 | **fail** |
| A_after_D | A_after_B | 5.0117231349 | 9.5439944365 | pass |
| A_after_D | A_after_C | 7.3852895807 | 9.5439944365 | pass |
| A_after_B | A_after_C | 2.6891287860 | 9.5440375500 | pass |

D/B/C 的单周期 60/120/300/600 chronology 使用 frozen same-state
per-capture diagonal variance。trend 与 dominance 只按 GUIDE 8.2 报告，未被
改写为 operational-600 hard gate：

| state | trend | limit | dominance | limit | dominant direction |
| --- | ---: | ---: | ---: | ---: | --- |
| D | 6.2989992683 | 4.0 | 0.4009237037 | 0.5 | `block_19::G1`, signed slope `-0.0002465393` |
| B | 8.1503454161 | 4.0 | 0.4733067736 | 0.5 | `block_16::R`, signed slope `-0.0004471119` |
| C | 12.2215869835 | 4.0 | 0.4548462651 | 0.5 | `block_06::B`, signed slope `+0.0005672071` |

Analyzer 仍输出 D/B/C `t_settle_s=60`，但 GUIDE 冻结解释保持
`steady_status=not_demonstrated`；三个 trend 均高于 4.0，不能解释为已证明 steady。

## 实验与复现身份

唯一 retained root：

```text
/Volumes/4T/temp/rgbww-optimizer/guide4-ray-r6-20260808-20260808-153400-post-fix-valid/ray-r6
```

```text
guide experiment = P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6
internal experiment = p7_td_b_command_switch_history_v1
sequence = A -> D -> A -> B -> A -> C -> A
formal/physical = 16/16
launch/retry = 1/0
acquisition commit = 3e80e5fd30e079782b27a3545513de5821dbc4d2
acquisition dirty = false
exposure validator commit = b73fe2433f6800e99f62140a9a216ac9adabd4bb
diagnostic analyzer commit = a3f2b864860a3b524999bd003c2b01f26748086a
feature policy sha256 = db9ebef1503c5e54c989649c719c4a5f75445bbd5487edb14c274e1b2894f3b4
```

Analyzer argv：

```text
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.analyze_p7_thermal_diagnostics \
  /Volumes/4T/temp/rgbww-optimizer/guide4-ray-r6-20260808-20260808-153400-post-fix-valid/ray-r6 \
  --feature-ids config/hsi/strip-hsi-policy-v2-waiting.json \
  --revalidate-exposure-failure \
  --validator-commit b73fe2433f6800e99f62140a9a216ac9adabd4bb
```

## Small-artifact hashes

| artifact | SHA-256 |
| --- | --- |
| `experiment-spec.json` | `b8a8274b2c786c5c896acfeb39f45c1501eefbd526606e60ded64d7db0f0c616` |
| `input-checkpoint.json` | `df63b7d92b2d25fb534a33047548d8ffeee9094b019953774da77faca8076d7a` |
| `run.json` | `ef1367a2078c9c95f9900cda066ce5a030d59ec1ce5e48e1ffde22905812a062` |
| `failure.json` | `c60964f5d6f5a67207876ec8bd369502db8939dc4916e1f63c71991392d3529a` |
| `wrapper-result.json` | `f6b2c8e2781a531b2fb0ca391dac3a1eb761386f7455b078c1d545a710d2c20f` |
| `captures.jsonl` | `a9c324c22d1240835302d29e79b95d2338324abda36fb41cbd258c0f532f9599` |
| `physical-returns.jsonl` | `f71c26797bf925fa1ab81066757e74edd4156fe00eb8d84c62e1b3ea37294b8a` |
| `commands.jsonl` | `8f27841f01df776066e64b21d6f3311ba99cbf3eb463f9ec3ed55fd6751c410f` |
| `commands-audit.json` | `98a1df5311ce789b6eff0e20a9ada8521efda83efbf3d999d71c0d566c298178` |
| `isolation-gates.jsonl` | `7acdb527dca1668a5f0d9b8120f687a8e561d9c5fdcf85572498df4a092b468d` |
| `thermal-covariates.jsonl` | `7f434a6349344092f9114d7e30ec515c1c84067de799eeaee2f2736e11678162` |
| `quality.json` | `ed4050b4cba2b53133ec9cb4e51c139ba6128e3051ca3dd541183b4df6915b3f` |
| `post-fix-revalidation.json` | `9d531419ed94bcc1a0c5af29933eb82131082dbe0eea0d9f05f9dcfdec473e2e` |
| `analysis.json` | `7cb6ef267496342ae1145bb83295510438ea9bf45946187168ffb21e8b0e267b` |
| `all-off-python.json` | `60bb673d7f07fdfcbf22e804da03982a32a9b8b07496daaa85cafba67d21d517` |
| `all-off-shell.json` | `d254329059b2e6553210c19418ef0977b56a833d2d0884adfd3ac464408da4d7` |

原 `run/failure/wrapper` 保持 child failed 事实；显式 revalidation 仅证明旧
exact-float exposure gate 已被当前 setting-consistency gate 取代，并未重写原执行结果。

## 安全状态与未进入范围

- acquisition 后 Python cleanup 与 shell cleanup 均为 pass；原证据 hash 如上。
- 本轮离线 revalidation/analyzer 未访问 camera、Ray、strip 或 network。
- 新 strip TD-B：未进入，locked。
- combined operational-600：未进入，locked。
- TD-C core：未进入，locked。
- endpoint expansion、sentinel、remaining 9、boundary、holdout、Gate-6、P8、default LUT install：全部 locked。
- 不允许从本 handoff 推导重采、改阈值、删帧、跨 root pooling 或设备授权。

## Advisor 需要回答的科学问题

在保持 frozen observer、58 features、uncertainty、source isolation、固定曝光档位、
600 秒非 steady 语义与本次完整 16-frame evidence 的前提下：

1. `A0` 与 `A_after_C` 的单一 history split 应采用何种 thermal/history 模型解释？
2. 下一项最小有界科学动作是什么；是否需要新的 Ray history experiment，还是应先改变分析模型？
3. 在获得新的科学指导前，是否继续保持 strip/combined/TD-C 锁定？

本请求不要求 Advisor 设计工程 runtime、release、lineage、stage-gate 或治理层。
