# REF-P7-25-R2-B1A-C2 / False source-identity rejection review

**Planner 日期：** 2026-07-29

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C2-UNITTEST-CARRY-FORWARD-V1`

**Decision：**
`ACCEPTED_FALSE_REJECTION_REQUIRES_CANDIDATE_OWNERSHIP_REASSESSMENT`

## 1. Evidence replay

```text
reviewed PLAN SHA-256 =
  097c4309a3ede5c1f52293692e90231d781fb653dccb5685970d1cd5fc9ef193
C2 root =
  /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-retained-r3-option-b-b1a-c2-offline/20260729T171606Z
validation SHA-256 =
  03453245d14cd51238b05c62ee9de1ae9c1f7daca03e539ca6ee2d7c93cd10a3
terminal SHA-256 =
  11eeae2f25567b270eb8453acc9a53b7bcdf304e790f9e163c9823202e4d1d60
EXECUTION_RESULT.md SHA-256 =
  aee196393ccaf7cd2445d1e2fc89f760bc5517caa36edb7eabf74bd685b79b04
```

Planner独立确认8/8 top-level JSON通过strict duplicate-key/non-finite parse；terminal列出的7项pre-terminal evidence
bytes/SHA全部匹配；validation/terminal mode0600、nlink1、hash exact。C2 clean-room HEAD=`9303aa2`、tree=`c67473c...`、
staged0，只materialize前两个exact paths。

## 2. False rejection finding

C2 temporary controller使用的third-path expected SHA为：

```text
7b5b5e134b42bfa9cd30807d1c20377ba53ae9fc952ae02c3e808f20bb9cfd29
```

Authoritative reviewed PLAN冻结的是：

```text
7b5b07568f452447faf645f69b7a02482d095284daab44f6fd87ddf5a189fd29
```

Controller在raise前没有持久化observed digest，只写
`observed_sha256=not_persisted_before_fail_closed_raise`。因此C2 evidence不能支持source mutation结论。

Planner在terminal后只读重算C1 original candidate third path：bytes=`194497`、mode0644、nlink1、SHA-256 exact为
`7b5b07568f452447faf645f69b7a02482d095284daab44f6fd87ddf5a189fd29`。C1 source与PLAN一致，未证明任何漂移。

故C2是`false_source_identity_rejection`：accepted fail-closed stop，但拒绝其mismatch语义，不计为candidate invalid，也不
允许继续C2。C2 content opens/verified/unopened=`3/2/2`；import identity/focused/full/stage/commit/manifest/R3 reads均0。

## 3. Three-failure ownership reassessment

连续三个工程失败分别为：

1. B1A：preflight exception后compound shell仍clone——lifecycle owner不唯一；
2. C1：不存在的pytest executable——runtime/test-command事实未由环境owner绑定；
3. C2：candidate SHA手工转录错误——PLAN与temporary controller形成duplicate candidate owner。

继续逐字符串修补会保留相同结构性风险。C3必须让machine-readable PLAN object成为candidate facts唯一owner；controller
只能从exact PLAN bytes解析，禁止hardcode、copy/paste或另行构造expected path/bytes/SHA/patch/parent/tree/subject。

此外，任何source read必须在mismatch raise之前持久化path、expected、observed SHA与metadata，避免再次产生无法区分
source drift与controller drift的证据缺口。

## 4. Preserved state and next branch

C1 immutable source仍绑定exact five hashes与canonical patch
`775b07fecfd65ba278ee174d4ae64772e8b2cfc83d794b6c89c259f4b8eadee0`。C1/C2 roots均immutable，不得same-root
reuse/repair/test/commit。

Original R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。Tests、stage、commit、manifest、canonical verifier、R3 reads、
eligibility、release、network、DNS、env、device、camera、Ray、strip、cleanup、capture、analyzer、FORMAL、firmware、deployment
均0。

下一分支`REF-P7-25-R2-B1A-C3`：fresh root、single fail-fast owner、PLAN内唯一strict duplicate-free
`CANDIDATE_MACHINE_CONTRACT`，PLAN machine绑定其exact-byte SHA。保持unittest clean-room identity、candidate edit0、retry0、
single commit/manifest/R3 three-hash合同。无Advisor/Human gate。

