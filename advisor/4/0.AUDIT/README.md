# Stage 6 P7-TD-A / TD-B Advisor 第四轮审计包

## 基线与完整性声明

上一次已经正式交给 Advisor 的材料是 `advisor/3/`。本目录此前已有的 `01` 至 `03` 是路线尚未完成时形成的
局部草稿，从未作为第四轮完整审计包提交，因此不能据它们推断 `advisor/3` 之后的全部工作。

本次按任务语义重新审阅了：

- `advisor/3/0.AUDIT/` 已报告的 P7-R1 终态；
- `advisor/3/1.GUIDE.md` 下发后的全部 thermal diagnostic 工作；
- `.agent-work/EXECUTION_RESULT.md` 第 1 至 132 节；
- P7-R1 之后、当前 `HEAD` 之前的 47 个相关提交；
- FORMAL-R5 的原始 retained package、progressive/terminal evidence、physical-return ledger 和 cleanup evidence。

由于 `advisor/3`、早期 `advisor/4` 草稿和部分后续实现被一起写入提交 `9c804ab`，Git 提交边界本身不能代表
正式汇报边界。本包以 `advisor/3` 已报告的 P7-R1 科学结论为语义截止点；其后的完整增量以 `04` 为准。

## 文件导航

1. [01-td-a-completed-method-and-quality.md](01-td-a-completed-method-and-quality.md)：TD-A 方法与有效负结果；保留为
   早期局部报告。
2. [02-thermal-extension-decision-request.md](02-thermal-extension-decision-request.md)：已被 Human 决定取代的
   900/1200 秒历史请求。
3. [03-human-decision-no-extension.md](03-human-decision-no-extension.md)：Human 选择 600 秒 operational dwell 的
   权属和科学语义。
4. [04-advisor3-to-formal-r5-completed-work.md](04-advisor3-to-formal-r5-completed-work.md)：**本轮完整增量主报告**；
   覆盖 Advisor/3 之后全部执行节、科学结果、工程纠偏和当前锁。
5. [05-formal-r5-observer-quality-decision-request.md](05-formal-r5-observer-quality-decision-request.md)：**当前唯一
   R5 科学决策的历史输入**；按原始 R5 evidence 精确描述两个 clipping feature，而不是沿用“low-signal”简称。
6. [06-commit-and-evidence-index.md](06-commit-and-evidence-index.md)：47 个相关提交、外置 work package 和关键 artifact
   的索引。
7. [07-guide4-to-retained-r3-lineage-owner-decision.md](07-guide4-to-retained-r3-lineage-owner-decision.md)：**当前唯一
   Advisor 决策门**；覆盖 GUIDE 4 后的 EQ-R6、successor R3、repo-owned helper、真实 schema audit 与 exact
   lineage-owner 缺口。

## 当前结论

| 项目 | 结论 | 状态 |
| --- | --- | --- |
| Advisor/3 P7-R1 | 有效失败证据；原 60 秒协议未证明 reference stationarity | 保留，不重跑 |
| TD-A | Ray 与 strip 均 `settling_not_demonstrated_by_600` | 有效负结果 |
| Human dwell 决定 | 600 秒是产品时间上限，不是 `t_formal` 或科学 settled time | 继续有效 |
| TD-B 工程合同 | exact experiment、timing、lineage、physical/sidecar ledger、双 cleanup 和可见 Terminal owner 已建立 | 工程可审计 |
| 早期 TD-B formal | 首张 Ray `A@600s` 因 6 个低信号 plane-feature hard-fail | 历史失败；证据保留 |
| FORMAL-R5 | Ray 在 `011-ray-c-t60` 因白块 `G1/G2` clipping hard-fail | `accepted_hard_failed_formal_attempt` |
| R5 数量 | 11/16 accepted formal；12 returned CR3；physical total 14 = setup 2 + returned 12 | 非 formal pass |
| R5 后续 | strip、paired、public analyzer、NPY、retry 均为 0 | 正确停止 |
| FORMAL-R5 路线 | GUIDE 4 已选择 exposure qualification 路线；R5 clipping 不再是当前 active 决策门 | 历史输入 |
| EQ-R6 | `1/2500` qualified；`1/3200` fallback 未进入 | accepted |
| Retained R3 | 三 artifacts 已生成，但尚未完成真实只读审计或消费 | `RETAINED_UNVALIDATED_UNCONSUMED` |
| Helper correction | schema-owner Branch A focused `21/21`；两文件 diff 未提交 | 等待 lineage owner |
| 当前路线 | active task count `0`；等待 Advisor 选择 exact helper commit lineage owner | Advisor decision required |

## 当前证据边界

```text
historical FORMAL-R5 checkpoint = 1e3b107b8fbfe97bae5624ef638c4883a0faee1d
FORMAL-R5 launch = 1/1
FORMAL-R5 retry = 0
run classification = accepted_hard_failed_formal_attempt
public analyzer = 0
strip formal = 0
feature deletion / threshold relaxation = 0
new device action after terminal seal = 0
current code HEAD = 9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
release checkpoint = 32b9e670ff3bbea0cd1505528c2ca87c2935446c
retained R3 = RETAINED_UNVALIDATED_UNCONSUMED
active executable task count = 0
current decision evidence SHA-256 =
  842cfad090549ebf6379df4551bd4f051267e4bf93014f899c5e329c57085620
```

本次审计整理本身只读检查既有 evidence 并写入本目录；没有访问设备、网络、相机或 `.env`，没有执行
`all_off`、重拍、release、public analyzer 或科学计算，也没有修改任何 GUIDE。
