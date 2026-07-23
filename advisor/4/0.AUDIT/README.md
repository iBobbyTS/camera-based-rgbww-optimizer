# Stage 6 P7-TD-A Advisor 第四轮审计包

## 目的

本审计包在 `advisor/3/` 的第三轮 RESEARCH、GUIDE 和 AUDIT 基础上增量提交，不覆盖任何旧文件。
第三轮 GUIDE 要求 TD-A 在 600 秒仍未证明稳定时停止并请求 900/1200 秒扩展；本轮到达了该精确
分支。随后 Human/Developer 明确决定不继续扩展，并选择 600 秒作为产品 operational dwell。该人工
决定已取代原 Advisor extension request，不是 Planner 擅自放行，也不把 600 秒改称科学稳定。

## 文件导航

1. [01-td-a-completed-method-and-quality.md](01-td-a-completed-method-and-quality.md)：已完成范围、方法、
   retained evidence、独立复验和质量边界。
2. [02-thermal-extension-decision-request.md](02-thermal-extension-decision-request.md)：需要 Advisor
   决定的 900/1200 秒扩展合同与继续锁定项；现保留为 Human 决定前的历史请求。
3. [03-human-decision-no-extension.md](03-human-decision-no-extension.md)：Human/Developer 拒绝扩展、
   选择 600 秒 operational dwell 的权属、语义和后续代码边界。

## 当前结论

```text
TD-A acquisition/evidence = accepted
Ray result = settling_not_demonstrated_by_600
strip result = settling_not_demonstrated_by_600
t_formal_provisional = null
thermal extension 900/1200 = rejected by Developer/Human
developer_selected_operational_dwell_s = 600
TD-B device execution = locked pending offline contract update and Planner review
TD-C / sentinel / P8 = locked
next = offline developer-dwell contract package
```

本轮不是采集失败。24 formal、6 ambient、30 个 physical CR3、remote timing evidence、source
isolation、readback、ownership、budget、wrapper 和 cleanup 均通过。失败是两个 source 在三轮中均
超过冻结 trend 门，属于有效的非稳定性证据。
