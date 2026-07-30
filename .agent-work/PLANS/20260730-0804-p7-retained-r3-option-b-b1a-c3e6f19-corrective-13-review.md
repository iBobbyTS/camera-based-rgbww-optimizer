# F19 Corrective-13 Planner Review

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-13`

**Contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-13-PROGRAMMATIC-HEAD-VALIDATION`

**Review date：** `2026-07-30`

**Decision：** `REJECTED_SOURCE_TOPOLOGY_CONTRACT_MISMATCH`

## Reviewed scope

本次验收只读检查 active PLAN、committed FULL、C13 terminal evidence 与
`.agent-work/EXECUTION_RESULT.md` 的 C13 append。未运行测试、controller、Git验证命令或任何外部调用；未读取
candidate、retained R3、release 或旧 execution root；未访问网络、设备、相机、Ray、strip、cleanup、formal 或
public analyzer。

审查时仓库 HEAD 为 `88d46061a50f0e8a89b2a6cc51ca9399d75f4347`，除
`.agent-work/EXECUTION_RESULT.md` 外无 dirty path。

## Evidence

- Terminal：
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-13-offline/20260730T140212.594373Z/terminal-evidence.json`
- Terminal bytes：`6711`
- Terminal SHA-256：`94190eee0df9f0d49ea60b100fa4b0c77d24e2050fe3ad3f0b70e70604e3c02e`
- Terminal mode：`0600`；exclusive-create、single-fd、fsync 与 strict JSON reload 均为 true。
- Dispatch HEAD owner：`controller_git_rev_parse_single_read_freeze`；Git read `1`，second read `0`，
  human-transcribed expected child SHA `0`。
- Activation：commit `88d46061a50f0e8a89b2a6cc51ca9399d75f4347`，parent
  `6daa1e44eb842974d77030ef52ffb979b8d57bdb`，subject
  `chore(plan): activate f19 programmatic validation recovery`，changed paths exact
  `[.agent-work/PLAN.md]`。
- Retained source bytes identity passed：blob `efcb4b05877e857b47eebcb3d7e07dbf5979698f`，bytes
  `193853`，SHA-256 `0a688f31728f8c7d072419b8a75a7d9b4b04315e906cde6daa17a80556f56b64`，
  working equals committed。
- Retained test与config bytes identity均通过；C12 evidence supersession已按PLAN append记录，旧ER和旧artifact
  rewrite count `0`。

## Finding

唯一失败是 active PLAN 的 retained source topology 合同错误：PLAN要求 controller 将 production commit
`ba816216af9d37397873e054f44dbb7eea0f9b10`推导为exact one-path source commit，但真实、可重放的Git topology和
C13 terminal均显示它恰好包含两个路径：

1. `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`
2. `tests/test_p7_thermal_diagnostics.py`

其direct parent仍为`c0c51d9bc340da40ab5e95027e999962d2bd723e`，subject仍为
`fix(p7): separate historical lineage checkpoint ownership`。因此 controller 的
`RuntimeError: source topology mismatch`属于PLAN冻结错误，不是retained source/test/config漂移。

Root按合同exclusive-create为mode `0700`，但 validation item executed `0`；compileall、targeted、focused、full、
CodeGraph与diff均未调用。Repository implementation edits、staged paths、implementation commits、retry与fallback均为
`0`。Candidate、retained R3、canonical validator、eligibility、release、network、`.env`、device、camera、Ray、strip、
cleanup、formal、public analyzer、TD-C、sentinel、P8调用全部为`0`。Retained R3继续为
`RETAINED_UNVALIDATED_UNCONSUMED`。

## Decision and residual risk

C13不能验收为validation green，因为完整链一次也没有运行；但 programmatic HEAD修复、activation identity、三项
retained bytes identity与C12 supersession均可保留，不应修改或重跑C13 root。

残余风险只限于下一controller再次把历史commit的whole-commit changed-path topology与单个retained文件identity混为一谈。
Corrective-14必须由PLAN直接明示：若核验`ba81621…` commit topology，则exact set必须是上述两个路径；或者只核验
retained source path在该commit/dispatch HEAD中的blob、bytes与SHA identity，不得再推导one-path commit。

## Exact next branch

下一分支为`REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-14`。先由Orchestrator验收本review、更新FULL并创建focused
reviewed-state commit；随后Planner在该clean parent上签发一个PLAN-only activation。Executer使用brand-new C14 root，
programmatic single-read/freeze dispatch HEAD，按修正后的two-path topology或retained-path identity gate运行与C13相同的
one-shot 13-selector、focused、full、CodeGraph和diff链。Repository implementation edits/commits、retry、fallback和全部
后续阶段调用继续为`0`；成功也只回到Planner验收门。
