# P7 retained-R3 Option B：B3-C3-C3-S1 EOF supersession 验收归档

**审核时间：** `2026-08-01 06:47 America/Edmonton`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C3-S1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C3-S1-GIT-ER-TERMINAL-SUPERSESSION-V1`

**Activation：** `8d12497af46b8dcf66f5ea258e54664487c922e0`

**Evidence commit：** `c54af2de7d59d025f4ec198ba2087bb7bdb39be8`

**Planner decision：**
`ACCEPTED_COMPLETE_PHYSICAL_EOF_SUPERSESSION_AND_BINDING_FAILURE_SEALED`

## 1. 审核范围与方法

Planner只读核对committed Git topology、active PLAN以及Git object中的ER parent/child bytes。没有读取fresh/external package、
accepted real manifest/source、C1、retained R3、生产源码或测试源码；没有运行tests、controller、CodeGraph、canonical validator、
retained audit、release、network、DNS或任何device入口。`FULL_PLAN_REFERENCE.md`保持只读。

## 2. Activation 与 exact path topology

- activation是`fb5b1f3b939a70b6a6c4779ea8e9286663cb1c36`的direct child；subject exact为
  `chore(plan): activate B3-C3-C3 ER supersession`；changed paths exact为FULL、PLAN及
  `.agent-work/PLANS/20260801-0633-p7-retained-r3-b3-c3-c3-binding-eof-review.md`；
- evidence是activation的direct child；subject为`chore(evidence): seal B3-C3-C3 ER supersession`；changed path exact one
  `.agent-work/EXECUTION_RESULT.md`；
- activation ER blob OID为`744720bf87aa9a7ce98823049fe15f2aeb248cc4`，与PLAN precondition一致。

## 3. 独立 physical EOF 验收

Planner从Git blobs独立重算：

- activation/parent ER：bytes `1337266`，SHA-256
  `ec8a1f8385f90b49318a122d4142a6e1af831ddf5a8c1f99c77a31947166314b`；
- evidence/child ER：bytes `1340617`，SHA-256
  `e2cc3c5fc8a28bcb17262a25e23a2472b9f6a66db5fd326530733f477513e3ac`；
- child以parent全部bytes为完整prefix；唯一physical EOF suffix bytes `3351`，SHA-256
  `dd8b7c439e317fa357859c2ad019eff2578e10f428112c8bc806ac9711bfa5cd`；
- suffix只含一个heading、一个strict duplicate-free/non-finite-safe JSON object和closing fence，文件以LF结束；
- payload冻结一次successful append、`postappend_operations=0`及Executer未提交。

因此S1满足physical EOF canonical supersession合同，不需要再次进行Git/ER修复。

## 4. 被supersede的错位事实与binding失败

S1 payload准确记录了B3-C3-C3旧handoff不是EOF：

- old parent ER bytes `1332706`、SHA-256
  `0b5514770f001f329b84922789820f37c9c01f2763579653df253f0cf81602e1`；
- old evidence ER bytes `1337266`、SHA-256
  `ec8a1f8385f90b49318a122d4142a6e1af831ddf5a8c1f99c77a31947166314b`；
- `parent_is_evidence_prefix=false`，LCP `2583` bytes；
- preserved common suffix `1330123` bytes；
-错位 insertion `4560` bytes，SHA-256
  `c69f63b45d54d5faab7f52c3c9d37e5336c0c732bcb2b00171daad732571fda6`；
- Planner独立复算确认preserved suffix byte-identical。

Durable failure继续被接受为
`CONTROLLER_POSITIONALLY_BOUND_ADMISSION_AS_MANIFEST`：旧controller使用
`real_manifest_reference.files[0]`推断manifest角色，而该位置实际是`execution-result-admission.json`。这不是manifest defect。
后继必须从PLAN的五个明确basename建立exact unique map并按basename绑定artifact identity；禁止位置、排序、generic selector、guess或
fallback。

## 5. Verification、locks 与决定

B3-C3-C3 verification没有完成：focused/full/synthetic实际均为`0`，failed root不可复用。S1没有运行测试、controller或synthetic，
也没有读取real/external/retained inputs。Retained R3继续`RETAINED_UNVALIDATED_UNCONSUMED`；canonical lineage validator未调用，
eligibility未发出，release不可消费，B4未解锁。Network、DNS、environment、credentials、device、camera、Ray、strip、cleanup、capture、
formal、public analyzer、TD-C、sentinel、P8、firmware及deployment保持0。

因此本包接受为完整的evidence-governance closure。下一唯一分支为fresh byte-stable verification；它必须保留corrected
immutable-disposition/artifact-schema分层和derived-only pass semantics，并严格按self-check→focused exact`83`→full exact`800`→
brand-new synthetic exact`1`执行。

**Next reference task：** `REF-P7-25-R2-B3-C3-C4`

**Next contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-BASENAME-BOUND-BYTE-STABLE-POSTCOMMIT-VERIFICATION-V1`

**Next Planner stop：**
`B3_C3_C4_BASENAME_BOUND_BYTE_STABLE_POSTCOMMIT_VERIFICATION_WAITING_PLANNER_REVIEW`

维护性判断：S1只修复ER证据位置；后继把五个artifact语义角色收敛为PLAN basename exact map，不新增production owner、generic
selector、schema allowlist或eligibility路径。
