# REF-P7-04 / R2-D2 release-harness Planner review

**Review decision:** `rejected_future_plan_activation_structurally_impossible`

**Reviewed PLAN SHA-256:** `b0e08825caaa08b0cb156510312bd4a6ad3934fb1fa62fdfb6c65f73ccb6ee1b`

**Reviewed root:**
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r2-d2-offline-harness-preparation/20260726T160000Z`

## Verified result

- Final fake/adversarial matrix `62/62`，SHA-256
  `9a5badd320c5dc6d4c71d43f10ddc1df850466cf040c45dcb62ebfe4be52214a`。
- Final strict audit `19/19`，SHA-256
  `650128a2cd6da258eb8367989ecf095323dfe89ba66ccd472aeba49b7584e4fe`；final residual audit SHA-256
  `5ece78e91abafc412d491bf0c70099d3a41c6112bb28f38e512c89f78f19a872`，finding arrays为空。
- `EXECUTION_RESULT.md` §120 handoff SHA-256
  `54267e0ecd500966b9648849da2537cc5b7c1ecec7c4376dc563af42103d29d5`。
- Positive injected child产生exact three regular JSON：candidate为eligible、resolved plan为execute_authorized、release为
  formal_plan_lineage_qualified；terminal、three-artifact、internal-reference和public-validator语义在fake路径通过。
- Authority scan仅分类两个已知fake positive：首次superseded fixture与final R2 fixture；两处
  `production_release_usable=true`均位于显式fixture路径，`unexpected_true_hits=[]`、real authority true count `0`。
- Production release import/call/invocation `0`；future release `0/1`；authorized real contract artifacts `0`；D1/R2/legacy/
  candidate与workspace frozen inputs保持不变；device/network/live/formal均为`0`。

## Superseded evidence disposition

1. 首次matrix因terminal audit helper把整数raw child status当JSON object而异常。原始child/status与
   `classified-positive-fixture`完整保留；未发生production invocation。
2. 首次strict scan只分类final fake true、漏分类上述保留的首次fake true；superseded strict failure record SHA-256
   `a1ec1518eea0b55adae53bf10593184cc90cbbba88fc16bc79e565086eb2757b`。Final scan精确分类两处，无第三处true hit。

两项失败均被保存并由最终离线证据解释，不是本次拒绝原因。

## Planner finding

### REV-D2-001 — real later-PLAN activation is structurally impossible

`candidate/d2-later-plan-gate.py`把当前D2 PLAN SHA
`b0e08825caaa08b0cb156510312bd4a6ad3934fb1fa62fdfb6c65f73ccb6ee1b`硬编码为`PLAN_SHA`，real mode又要求实际
`.agent-work/PLAN.md`等于该hash。Planner写入任何later active PLAN后hash必然改变，gate必报`actual_plan_hash`并在child前拒绝。
Matrix positive使用`fixture=True`绕过real PLAN检查，因此`62/62`不能证明later activation可用。

同一激活边界还需收紧：real gate必须校验run-contract exact schema/status及future PLAN exact contract ID；terminal owner不得依赖
另一个可与current Markdown PLAN分离漂移的plan JSON。Current PLAN应由gate直接读取并绑定其machine contract与activation binding。

## Decision and next branch

D2不验收，不得据此生成真实lineage release。下一包为唯一纯离线D3 activation correction：保留D2全部证据只读，修复动态
later-PLAN/run-contract绑定并做production-shaped injected regression；production invocation保持0，future release保持0/1。

Human已解除旧的全设备暂停，但这不改变D3纯离线边界。任何后续release generation、device/live/formal动作仍须由其active PLAN
精确冻结授权、目标、范围、abort和cleanup；firmware/deployment/destructive operation仍须Human显式授权。

建议Orchestrator把REF-P7-04的D2标记为rejected、D3标为current；release generation继续locked 0/1。

维护性判断：三artifact validator与terminal owner的职责可保留；D3只需修复单一activation owner，删除对superseded PLAN hash及
分离plan JSON的依赖，无需改production架构。
