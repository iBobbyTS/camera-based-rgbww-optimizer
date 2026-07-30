# F19 Corrective-14 Planner Review

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-14`

**Contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-14-SOURCE-TOPOLOGY-VALIDATION`

**Review date：** `2026-07-30`

**Decision：** `REJECTED_FULL_SUITE_EQ_R6_MANIFEST_METADATA_DRIFT`

## Reviewed scope and method

本次验收只读检查active PLAN、`.agent-work/EXECUTION_RESULT.md`的C14 append、C14 terminal seal与其
full-suite log，并只读检查canonical EQ-R6 manifest builder、qualification owner、对应dedicated test和accepted root
顶层目录项。未运行测试、controller、CodeGraph、Git mutation、retained-R3 validator、release、网络、设备、相机、Ray、
strip、cleanup、formal或public analyzer；未修改、删除或重建accepted root、C14 root及任何旧证据。

审查时仓库HEAD为`d61accd5b1eac975874a128db949fddb594d34e8`；除
`.agent-work/EXECUTION_RESULT.md`外无dirty path。被中断后的替代Executer在发现ER已dirty后pre-root停止，未创建root、
未调用validation，也不是C14 retry evidence；本review只消费下述原C14 one-shot terminal。

## Authoritative evidence

- Active PLAN：`.agent-work/PLAN.md`，bytes `15867`，SHA-256
  `8121cffd49130a3ceee62aad6aaad5720b2b996b3c4ef068c5a8d39539f57cf7`。
- Root：
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-14-offline/20260730T141613Z`，
  mode `0700`，exclusive-create count `1`。
- Terminal：同root下`terminal-evidence.json`，bytes `9185`，mode `0600`，SHA-256
  `0439ff6136737d41b168409a113f7df12e0794638eed39777cdfdf6f8b27e8fe`；strict JSON可解析。
- Full log：同root下`04-full.log`，bytes `140521`，mode `0600`，SHA-256
  `a28a70a866858cb0dc54561f6eb33d3fa9c9e521cf5d96960f0036991d3f515f`。
- Programmatic dispatch HEAD：`d61accd5b1eac975874a128db949fddb594d34e8`；Git read `1`，second read `0`，
  human-transcribed expected SHA count `0`。
- Activation topology、`ba816216af9d37397873e054f44dbb7eea0f9b10` exact source+test two-path topology、
  retained source/test/config identities与test canonical patch均通过。
- Compileall exit `0`；exact targeted `13/13`，log SHA-256
  `20aceda4304fa1cf9bff51f2b899290f3d36c7490dce9999b92d2d5a15e87d53`；focused `125/125`，
  log SHA-256 `b0c0b6fe254033a80854a52f7f3d4751000460e8c45489feb4b56cc3bb477649`。
- Full suite运行`687`项、exit `1`、failures `2`；按fail-fast合同，CodeGraph与diff均未运行。
- Repository implementation edits、staged paths、implementation commits、retry、fallback均为`0`；ER append `1`。
- Candidate、retained R3、canonical validator、eligibility、release、network、`.env`、device、camera、Ray、strip、
  cleanup、formal、public analyzer、TD-C、sentinel、P8调用全部为`0`。Retained R3保持
  `RETAINED_UNVALIDATED_UNCONSUMED`。

## Finding

C14正确关闭了此前的retained production topology误判，且targeted与focused均通过；但完整套件不能验收。两项失败均来自
`tests/test_p7_td_b_r6_contract.py::EqFamilyManifestTests`：

1. frozen accepted-family manifest期望`(entries, files, directories, symlinks, other, payload_bytes)`为
   `(47, 42, 5, 0, 0, 7980)`，实际为`(48, 43, 5, 0, 0, 8119)`；
2. artifact-hash drift负例预期到达`artifact drifted`，但先被同一family manifest drift以
   `EQ-R6 accepted evidence manifest drifted`截断。

Accepted root
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-f37517a-20260727T1928`顶层存在一个新普通文件
`.DS_Store`：bytes `6148`，mode `0644`，SHA-256
`c1249bc621a24778654848bfca63249d4e79c6f9bf93bb3b0337fe53e33541b6`。现有builder使用`rglob("*")`
把整个树的所有普通文件加入rows；该非实验Finder metadata由此增加一个file/entry，并令canonical payload序列化增加
`139` bytes。它不在`TD_B_EQ_R6_ARTIFACT_SHA256`的四个资格artifact中，也不证明任何资格artifact被改写。

## Decision and residual risk

C14以`REJECTED_FULL_SUITE_EQ_R6_MANIFEST_METADATA_DRIFT`结束，不得将targeted/focused green解释为完整验证、eligibility或
release可消费。C14 root与accepted root均保持只读，不得删除`.DS_Store`来伪造短期green，也不得更新frozen manifest digest
以吸收无关metadata。

工程上正确的最小纠偏是：在既有单一`build_planner_eq_family_manifest`owner内精确分类accepted root顶层的普通文件
`.DS_Store`为非证据metadata，并在生成rows/counters/payload前排除；原47-entry digest、四个artifact hashes与
`audit_td_b_eq_r6_qualification`单一eligibility owner必须不变。为避免扩大忽略面，symlink、目录、嵌套
`subdir/.DS_Store`、AppleDouble `._*`及任何其他未知路径仍须fail closed或进入manifest造成drift。

残余风险是宽泛basename过滤会隐藏未来证据路径或unsafe filesystem types；C15必须用exact root-relative equality并在
忽略前完成`lstat`/type检查，以meaningful negative tests固定该边界。这是provenance engineering问题，不需要Advisor
科学指导或Human设备授权。

## Exact next branch

下一分支为`REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-15`：Orchestrator先验收本review、更新只读reference并创建focused
reviewed-state commit；Planner再冻结该parent并签发PLAN-only activation。Executer只可修改
`src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`与
`tests/test_p7_td_b_r6_contract.py`，创建exact one implementation commit，然后在brand-new C15 root运行targeted、
focused、full、CodeGraph与diff one-shot链并停止在Planner门。不得修改accepted root或frozen artifacts/digests；所有
retained-R3、release、设备与后续阶段继续锁定。
