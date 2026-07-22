# Human/Developer 决定：不扩展，使用 600 秒 operational dwell

## 1. 原始决定

Human/Developer 在当前 thread 明确要求：

```text
不要继续扩展。使用目前的600秒。
记录下来这是人工的决定，不是planner的擅自决定，开发者不希望在这一点上拖长时间。
```

决定权属：

```text
decision_owner = Developer/Human
planner_inference = false
thermal_extension_900_1200 = rejected
developer_selected_operational_dwell_s = 600
```

## 2. 保留的测量事实

该决定不推翻或重写 TD-A：

- Ray 与 strip 仍均为 `settling_not_demonstrated_by_600`；
- Ray trend 为 `17.7369 / 16.8013 / 16.7317`；
- strip trend 为 `16.8865 / 10.3106 / 11.8856`；
- 冻结 trend limit 仍为 `4.0`；
- `t_settle_ray_s`、`t_settle_strip_s`、`t_formal_provisional_s` 仍为 null；
- 600 秒没有被证明为 steady 或 settled。

因此正式术语必须为：

```text
developer_selected_operational_dwell_s = 600
operational_dwell_claim = selected_time_limit_not_proven_steady
```

禁止写成：

```text
t_formal_provisional_s = 600
td_a_pass = true
settled_at_600 = true
```

## 3. 后续执行含义

项目不再采集 900/1200 秒，不再为确定更长稳定时间拖延 P7。下一步应离线实现一个显式 Developer
override contract，使 TD-B 的 A0 和 return anchors 使用 600 秒，并让 analyzer 同时报告：

1. 600 秒 operational protocol 下的 return-to-A history compatibility；
2. D/B/C 的 60/120/300/600 chronology 和未稳定警告；
3. 产品 operational dwell 与科学 settle status 的独立字段；
4. 不因 Developer 选择而扩大 covariance 或降低原门限。

离线实现和 dry-run 通过后必须回到 Planner 门；本决定不自动启动 TD-B 实拍，也不授权 TD-C、
sentinel、remaining、boundary、holdout、Gate-6 或 P8。
