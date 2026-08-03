# REF-G4-04-E2：等待 fresh-root binding activation

**状态：** `DRAFT_PLAN_WRITTEN_WAITING_ORCHESTRATOR_ACTIVATION`

**Executable before activation：** `false`

**Active task before activation：** `null`

**Draft reference task：** `REF-G4-04-E2`

**Contract：** `G4-E2-FRESH-ROOT-BINDING-ENABLING-V1`

**唯一 Planner stop：** `RETURN_FOR_G4_04_E2_FRESH_ROOT_BINDING_ENGINEERING_REVIEW`

Planner独立确认current owner仍把output root固定到已拒root，因此本PLAN只做explicit fresh-root binding engineering unit，不在dirty code上生成
evidence package。只有Orchestrator验证parent`ce4eaab9e06bdb1c6092b2ab104b7f2931a7fb44`、对齐FULL并创建subject
`docs(plan): activate e2 fresh root binding`且changed paths exact为PLAN/ER/FULL的activation commit后才可执行。

Planner已修正draft中的test-root可达性矛盾：测试不使用嵌套`TemporaryDirectory`，而由test-owned context在TEMP_PARENT下选择最多两个
exact合法、预先不存在的direct-child roots。Fixture记录repo provenance DirectoryIdentity，并在`finally`验证exact path/identity、历史root
排除及allowlisted regular-file inventory后，仅逐项unlink exact children并`rmdir` exact root；禁止glob、rmtree、prefix scan或parent cleanup。
Durable root budget仍为0，test root residual必须为0。

当前未修改source/test/FULL/archive，未运行tests，未访问旧root/external payload/device/network/release/formal，未创建root/package，未生成
G4-05/06 PLAN。Executer开始后必须覆盖本文件写完整handoff；不得修改PLAN或FULL。
