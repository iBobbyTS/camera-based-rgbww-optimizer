# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-14：retained source topology contract correction

**计划状态：** `WAITING_ORCHESTRATOR_ALIGNMENT`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-14`

**Proposed contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-14-SOURCE-TOPOLOGY-VALIDATION`

**唯一当前动作：** Orchestrator只读验收C13 rejection，更新其独占的
`.agent-work/FULL_PLAN_REFERENCE.md`，将C13结果、下方exact C14 topology correction与review evidence一起创建一个
focused reviewed-state commit，然后停止并交Planner签发PLAN-only activation。当前PLAN不授权Executer、controller、
root创建、validation、implementation edit、Git commit、candidate/R3/release/device或后续阶段调用。

**C13 review archive：**
`.agent-work/PLANS/20260730-0804-p7-retained-r3-option-b-b1a-c3e6f19-corrective-13-review.md`，
bytes `4434`，SHA-256
`c2018931bdb35e6424829177b0111a831bfbeab46f44ba7c69e5f7259f87f924`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_14_orchestrator_alignment_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-14","proposed_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-14-SOURCE-TOPOLOGY-VALIDATION","dispatch_state":"waiting_orchestrator_alignment","single_current_action":"orchestrator_accept_c13_review_and_freeze_corrected_source_topology","review_archive":{"path":".agent-work/PLANS/20260730-0804-p7-retained-r3-option-b-b1a-c3e6f19-corrective-13-review.md","bytes":4434,"sha256":"c2018931bdb35e6424829177b0111a831bfbeab46f44ba7c69e5f7259f87f924"},"c13":{"dispatch_head":"88d46061a50f0e8a89b2a6cc51ca9399d75f4347","terminal_path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-13-offline/20260730T140212.594373Z/terminal-evidence.json","terminal_bytes":6711,"terminal_sha256":"94190eee0df9f0d49ea60b100fa4b0c77d24e2050fe3ad3f0b70e70604e3c02e","verdict":"rejected_source_topology_contract_mismatch","validation_items_executed":0,"retry":0},"corrected_source_topology":{"commit":"ba816216af9d37397873e054f44dbb7eea0f9b10","parent":"c0c51d9bc340da40ab5e95027e999962d2bd723e","subject":"fix(p7): separate historical lineage checkpoint ownership","exact_changed_paths":["src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py","tests/test_p7_thermal_diagnostics.py"],"additional_paths":0,"single_path_derivation_forbidden":true},"retained_source_identity":{"path":"src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py","blob_oid":"efcb4b05877e857b47eebcb3d7e07dbf5979698f","bytes":193853,"sha256":"0a688f31728f8c7d072419b8a75a7d9b4b04315e906cde6daa17a80556f56b64"},"next_planner_activation_requirements":{"plan_only_commit":true,"programmatic_dispatch_head_single_read":true,"brand_new_root_count":1,"targeted_selector_count":13,"one_shot_chain":true,"repository_implementation_edits":0,"implementation_commits":0,"retry":0,"fallback":0},"locks":{"executer_dispatch":0,"controller":0,"root_create":0,"validation":0,"candidate":0,"retained_r3":0,"canonical_retained_validator":0,"eligibility_emission":0,"release":0,"network":0,"env":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"F19_CORRECTIVE_14_WAITING_ORCHESTRATOR_ALIGNMENT"}`

## 1. C13 review decision

C13被拒绝，不得表示为validation通过。Programmatic dispatch HEAD gate与activation identity通过；retained
source/test/config bytes identity通过；C12 supersession append通过。失败唯一来自PLAN错误要求controller把
`ba816216af9d37397873e054f44dbb7eea0f9b10`推导成exact one-path commit。

Git与C13 terminal均证明该commit的exact changed-path set为：

1. `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`
2. `tests/test_p7_thermal_diagnostics.py`

其parent为`c0c51d9bc340da40ab5e95027e999962d2bd723e`，subject为
`fix(p7): separate historical lineage checkpoint ownership`，additional paths `0`。C13 validation items `0`，因此
不得从identity gate推断测试通过；也不得重试、复用或修改C13 root。

## 2. Orchestrator alignment package

Orchestrator应亲自：

1. 复核C13 terminal path、bytes、SHA与review archive identity；
2. 在FULL中将C13标记为`REJECTED_SOURCE_TOPOLOGY_CONTRACT_MISMATCH`；
3. 将C14设为唯一active reference task并冻结本PLAN的corrected two-path topology；
4. 将ER append、C13 review archive、当前PLAN与FULL组成focused reviewed-state commit；
5. 保持source、test、config、GUIDE、旧archive与旧evidence byte-exact不变；
6. 在clean reviewed-state HEAD停止并交Planner编写PLAN-only activation。

不得把本次失败上升到Advisor：这是Planner工程topology合同错误，不是色彩科学或测量科学分支。它不涉及高危设备
操作，也不需要Human授权。

## 3. 下一Planner必须冻结的C14 executable contract

下一Planner仅在Orchestrator完成alignment commit后签发一个PLAN-only activation，并将activation direct parent冻为
该exact reviewed-state HEAD。Executer随后只能执行validation-only C14；implementation source/test/config edits、stage、
commit全部为`0`。

Controller必须以一次`git rev-parse --verify HEAD^{commit}`读取并冻结dispatch HEAD，human-transcribed child SHA与
second read均为`0`。Activation topology核验后，对`ba81621…`只能选择以下合同之一；下一Planner必须选定并写死，
不得让Executer临时推导：

- **首选：whole-commit exact topology。** 核验parent、subject及上述exact two-path set，additional paths `0`；随后分别
  核验当前retained source与retained test的blob、bytes、SHA identity。
- **允许的更窄替代：retained-path identity only。** 不声称`ba81621…`是one-path commit；只证明retained source path
  在该commit与dispatch HEAD中的blob、bytes、SHA identity。若采用此项，test topology仍由其独立commit
  `a9a817137969d9d2692fdd0b244d08e26e8a025d`合同核验。

任何形式的`ba81621… exact one-path`断言均禁止。旧policy、workflow、public-default payload、canonical candidate
builder、canonical validator、旧manifest与retained R3均不可读取、修复或重建。

## 4. 下一C14 execution outline

下一PLAN须沿用C13的validation-only边界：

- root prefix改为
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-14-offline/`；
- brand-new exclusive-created child root恰好`1`，mode `0700`；retry `0`，fallback `0`，旧root读取`0`；
- 每个log由单一owner以`O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`只open一次，stdout/stderr同fd，close后digest；
- 依次且每项exactly once、fail-fast运行compileall、C13相同且顺序固定的exact 13 selectors、相同focused四模块、
  full suite、`codegraph sync`、reviewed-state-to-dispatch exact PLAN-only diff check与working-tree diff check；
- terminal最后single-fd exclusive-create、fsync、strict reload、digest、seal；ER只append一次；
- C12 supersession无需再次新增或改写，只应引用C13已完成的权威append；
- 成功仍只表示retained source/test/config validation green，停止在Planner验收门，不得调用canonical retained validator、
  产生eligibility、消费release或进入FORMAL-R6/TD-C/P8。

若下一Planner预计完整链超过10分钟，必须在可见macOS Terminal中执行并遵循三次稀疏liveness、automation与goal
blocked流程；不得拆包规避。

## 5. Locks与停止点

当前alignment包中，Executer dispatch、controller、root create、validation、repository implementation edit、stage、
implementation commit均为`0`。Candidate、retained R3、canonical retained validator、eligibility emission、release、
network、`.env`、device、camera、Ray、strip、cleanup、formal、public analyzer、TD-C、sentinel与P8全部为`0`。
Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

**Planner stop：** `F19_CORRECTIVE_14_WAITING_ORCHESTRATOR_ALIGNMENT`。
