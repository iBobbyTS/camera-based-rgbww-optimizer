# REF-P7-25-R2-B1A-C3 / Pre-root FULL machine-state hard-failure review

**Planner 日期：** 2026-07-29

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3-SINGLE-CANDIDATE-OWNER-V1`

**Decision：**
`ACCEPTED_PRE_ROOT_ORCHESTRATOR_ACTIVATION_FAILURE_CANDIDATE_UNTOUCHED`

## 1. Evidence

本次failure按PLAN发生在任何external package root之前，唯一terminal evidence为
`.agent-work/EXECUTION_RESULT.md`第54节：

```text
EXECUTION_RESULT.md SHA-256 =
  00b7b98be98bb7d20773f0439d67635ca8746150eca9218afb153f6ecf03ada4
reviewed PLAN SHA-256 =
  a6d4cb8d121e334017fc47a5be07fd03cd84366bb9c9c2d5531e0b1e31f78497
reviewed FULL SHA-256 =
  9b92a553e1fd78728fcd4dc3adc26473640061224f0272e7a2b2322f0fefc5a5
```

Planner独立解析FULL确认machine row恰好1条；以下现有字段均匹配C3：active count/task/contract、checkpoint、release
checkpoint、retained status、dispatched、device/release authorization false。但machine object缺少：

```text
candidate_machine_contract_sha256
candidate_contract_orchestrator_verified
```

C3 container不存在；因此没有package-local evidence是contract-compliant事实，不是evidence缺口。

## 2. Decision quality

C3严格执行PLAN gate，没有用FULL prose、handoff文本或另一个手工常量替代missing machine fields。Root、clone、source read、
candidate materialization/edit、import identity、focused/full、stage/commit、manifest、original R3 reads全部0；network/device/
FORMAL等副作用全部0。

失败owner是Orchestrator activation：它在FULL prose/dispatch中掌握candidate verification事实，却没有把两个字段写入唯一machine
object。Candidate object本身未读取或改变，science contract未进入。故接受hard failure并拒绝将其计为candidate、test或实现失败。

## 3. Successor design

仅靠再次提醒Orchestrator手工补字段仍会保留漏项风险。Successor `REF-P7-25-R2-B1A-C3E1`必须在
`PLAN_MACHINE_CONTRACT`内嵌一个`required_full_machine_state` object，成为activation subset的唯一machine-readable owner。

Orchestrator只能从该nested object程序化merge到FULL，再按exact key/value subset检查；Executer也从同一nested object解析并
gate。不得在prose维护第二份required key/value表。

唯一candidate object及其SHA、C1 immutable bytes/patch、unittest identity、fresh root、candidate edit0、retry0、single
commit/manifest、original R3 three-hash和所有zero side-effect合同不变。无Advisor/Human gate。

