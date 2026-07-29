# P7 FORMAL-R5 offline preparation Planner review

**Review date：** 2026-07-26

**Reference task：** `REF-P7-04`

**Reviewed PLAN contract：** `P7-TD-B-RAY-PUBLIC-DEFAULT-FORMAL-R5-OFFLINE-PREPARATION`

**Reviewed PLAN SHA-256：** `8cc1beeecc4d0287dfb85036f2a386c54fa51f401001e6a8f78c9338211dcd53`

**FULL_PLAN_REFERENCE SHA-256：** `d151d807a368bcf3fe5097dcaaa24146786ceefee657163a090eb76522ebf6e4`

**EXECUTION_RESULT §126 SHA-256：** `8a7cedfcabb3626540745f247521d3cf49ae29e16308d51486f51f13c269b517`

## Reviewed result and evidence

- Evidence root：`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-r5-offline-preparation/20260726T210000Z`。
- Candidate SHA-256 `22324b51076ab82ce7fc3aa93822c8a5214c1ad945471e5f01d6e1e6d0bab150`；single lifecycle owner
  `5f290d8b8af80aa1ef5281d5ed7db15d048f517aa39fcea2764f86c1dc30d128`；activation validator
  `1f4de6175725675f02be48916195b9436077ad62d02c9c8ebf0b29fd9525f764`；non-authorizing template
  `ade91ca8f84147910282e4888da87ca13ea5e6cfb029328b855c2183cf04c28f`。
- Final matrix `30/30`，SHA-256 `9c373cf9a42f5ea7949094ac5763b1ff524d53c766e3002d7108f04e34250479`；validation summary
  `9317f62371dd55e50facf04a779065ebc3e45ba015ea445aa4e8c9a7b214b4bc`；final audit
  `5831025419719b9a51f683544c085b081ac8f72711e7ce4851687c946d7ac533`；terminal strict audit覆盖754个regular JSON且mismatches为空，SHA-256
  `07dd5649f6c518c9f448174087be834e89aa344c1db5c2f893cf1cd8e6015a27`。
- Attempt 1 `29/30`因static literal-path断言失败而superseded；attempt 2 `30/30`在activation hardening前完成而superseded；最终
  post-hardening `30/30`是canonical matrix。首次independent audit错误要求writer-failure负例仍生成terminal audit；纠正为15个实际
  terminal audit加该负例显式absence后，final audit全空 mismatch。所有superseded artifacts均保留，disposition清楚。
- Candidate regular/non-symlink/mode0700、无runtime args；production inner wrapper/analyzer均以冻结path/hash复用；candidate/owner/
  validator中`AMARAN_OPENAPI_SECRET`、`launchctl`、`.env` reader、hostname probe均为0。
- Future package/Ray/strip/paired roots保持不存在；release generation历史1/1，新generation/validation/consumption均0；candidate real
  invocation、production child/import、device/network/Terminal/automation/camera/Ray/strip/all_off/capture/CR3/NPY/formal/commit均0；无残留进程。

## Planner findings

### REV-R5-001 — real activation contract 与 fresh package root 不可同时满足

**Severity：** blocking correctness / authorization gate

Lifecycle owner硬编码：

```text
PACKAGE = .../formal-r5-1e3b107-20260726T220000Z
ACTIVATION = PACKAGE / "formal-r5-activation-contract.json"
```

`main()`只在`ACTIVATION.is_file()`时调用validator；否则返回`activation_contract_missing`。同一validator又在任何child前要求
`PACKAGE`不存在且非symlink，否则返回`fresh_package_root`。由于regular activation file存在必然意味着其parent `PACKAGE`存在，real
activation没有可满足状态：文件缺失时被拒绝，文件存在时仍因package不fresh被拒绝。

Final 30/30没有覆盖该真实布局。`activation-valid-fixture`把contract写在case root下、把future package写在另一个子路径；因此测试通过不
能证明candidate真实常量组合可激活。该缺口与release/device安全无关，但会使已授权FORMAL-R5在设备前必然失败，不能放行真实包。

### REV-R5-002 — current-PLAN pre-child zero-call assertion 未度量 shared real entrypoint

Matrix中的current-plan rejection直接调用validator，并把`child_calls`写成常量表达式`0 == 0`；它没有通过candidate/main/shared lifecycle
owner收集真实adapter call count。这可证明validator会拒绝当前PLAN，但不能证明production-shaped entrypoint在真实路径布局下保持pre-child
zero-call。该项必须随REV-R5-001一起用共享owner的注入式计数路径关闭，禁止另造平行simulator。

## Decision

**结论：** `rejected_for_bounded_offline_correction`。

科学合同、release、public-default/secret边界、连续Ray→gate→conditional strip状态机和final evidence均未被否定；attempt history也已妥善
保留。但真实activation gate结构上不可达，因此本结果不能成为actual FORMAL-R5 frozen executable input。不得消费release或进入设备/formal。

**Exact next branch：** 单一pure-offline `FORMAL-R5-ACTIVATION-C1`：把activation contract移到future package root之外的exact sibling
authorization path，在shared owner/validator中冻结并动态验证其path/bytes/hash/0600；通过同一candidate/main/shared lifecycle owner验证
valid production-shaped activation可到达activation-accepted边界但由injected pre-child stop截断，并验证current PLAN/缺失/漂移合同时child
calls精确为0。必须重新跑全部既有30-case matrix、增加真实布局正负例、terminal strict audit和独立final audit。无release consumption、
device/network/live/formal、future package creation或commit。

**Residual risks：** C1接受前actual formal继续locked；`REF-P7-05`继续blocked。C1不得改变checkpoint、release、scientific contract、
capture/physical caps、source order或cleanup/no-retry语义。

维护性判断：缺口位于外置activation path owner与真实入口测试，不需要改repository production架构；最小纠偏应继续保持一个validator和一个
lifecycle owner。
