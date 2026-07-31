# REF-P7-25-R2-B2-P3-C1：provenance I/O fail-closed linkage correction

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-P3-C1`

**Parent reference task：** `REF-P7-25-R2-B2-P3`

**Contract ID：** `P7-TD-B-RETAINED-R3-PROVENANCE-IO-BOUNDARY-CORRECTION-V1`

**当前唯一动作：** Orchestrator独立审核、同步FULL并激活后，Executer只修复现有provenance I/O helper的
non-following capability和root/direct-child linkage，并补齐dedicated negative matrix；不得读取C1或retained-R3 artifacts，
不得运行real B2。

**预计时长：** `<10 minutes`；不使用visible Terminal、automation或后台长任务流程。

**唯一执行 stop：** `B2_P3_C1_REPAIR_WAITING_PLANNER_REVIEW`。

**本次P3 rejection review archive：**
`.agent-work/PLANS/20260730-2128-p7-retained-r3-provenance-io-p3-review-rejection.md`，
bytes `6137`，SHA-256
`8e31d05374a0fc7ff4e10f648fc470239f1259add7d9bc15e921b6aa5cf73793`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_provenance_io_boundary_correction_plan_v1","reference_task_id":"REF-P7-25-R2-B2-P3-C1","parent_reference_task_id":"REF-P7-25-R2-B2-P3","contract_id":"P7-TD-B-RETAINED-R3-PROVENANCE-IO-BOUNDARY-CORRECTION-V1","execution_authorized":true,"activation_required":true,"activation_commit":{"expected_parent":"96b1feb7ebf2b9f8f65c0aafce24ccaa7f26e39c","expected_subject":"chore(plan): activate retained r3 provenance io correction","exact_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260730-2128-p7-retained-r3-provenance-io-p3-review-rejection.md"]},"rejected_candidate":"77b9e85c1064cb6ba8d3a8fe0932b7eae488c945","implementation_commit":{"expected_subject":"fix(p7): harden retained r3 provenance io boundary","exact_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py","tests/test_p7_retained_r3_provenance_io.py"],"commit_count":1},"scope":{"production":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py","test":"tests/test_p7_retained_r3_provenance_io.py","exact_path_count":2},"validation":{"targeted":1,"focused":1,"full":1,"compileall":1,"codegraph_sync":1,"precommit_diff_check":1,"postcommit_targeted":1,"retry":0,"fallback":0},"zero_budgets":{"external_evidence_reads":0,"external_root_creation":0,"retained_release_audit":0,"canonical_validator":0,"eligibility":0,"release_operation":0,"network":0,"environment":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"planner_stop":"B2_P3_C1_REPAIR_WAITING_PLANNER_REVIEW"}`

## 1. Activation、frozen inputs与pre-edit gate

Executer不得在Orchestrator activation前执行。Activation commit必须满足machine contract的exact parent、subject和exact
three-path topology；激活后的FULL必须有exact一个active task/contract为本包，且继续声明
`retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`、P3 rejected、P3-C1 active、real B2/B3/B4 locked。

执行前记录HEAD、activation topology、stage/worktree；确认两个target都与rejected candidate `77b9e85c...`完全一致：

- production bytes `17505`、SHA-256
  `b1ea702fedaaf085c2f32850fc78c05ac54253a143c327a3280b34b804e3824d`、blob
  `4b28a480f642548314424e0465f6fc27add9d9f1`；
- test bytes `18617`、SHA-256
  `a86333e3daba4c7c9544a43edea0aea6ed879e0da2462d45fcbe7b150b748c9f`、blob
  `a1a3bbbe44be0ed4bcd50e1c5af1bc30dd450e7f`。

PLAN、FULL和archive应已committed且工作区clean。任一不符即pre-edit hard failure：edit/test/CodeGraph/commit为0，
只向ER追加真实handoff并stop；不得接管ambient work。

本包可读取repo source、tests、docs、Git object database和CodeGraph index。禁止读取
`/Volumes/4T/temp/rgbww-optimizer`中的C1、retained-R3、release或旧run artifact；tests自己的disposable test
directory不算external evidence root，且必须按现有tearDown回收。

## 2. Exact correction scope

Changed paths exact为：

1. `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py`；
2. `tests/test_p7_retained_r3_provenance_io.py`。

不得新增第三path、wrapper、CLI、package、fixture、config或generated source。保持现有public API、typed immutable values、
dependency injection、canonical JSON、Git grammar及non-ownership不变；只做以下三个accepted findings的最小修复。

### REV-P3-001：required open flags必须fail closed

集中验证`O_NOFOLLOW`和root-directory open所需的`O_DIRECTORY`为可用的nonzero integer capability。Exact read和target
exclusive open必须使用`O_NOFOLLOW`；root fsync open必须同时使用`O_DIRECTORY|O_NOFOLLOW`。不得继续使用
`getattr(..., 0)`静默退化。能力缺失、非整数或zero时，在任何相关open前抛带稳定machine-readable code的
`ProvenanceIOError`；不得尝试follow-capable fallback。

保持exact flags：

- read：`O_RDONLY|O_NOFOLLOW`；
- target persist：`O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`，mode `0600`；
- root fsync：`O_RDONLY|O_DIRECTORY|O_NOFOLLOW`。

### REV-P3-002：root必须与target形成exact direct-child linkage

`read_exact_file(..., root=root)`在任何target lstat/open前必须验证：root identity仍exact；target为absolute、lexically
safe、且exactly one direct child of `root.path`。拒绝outside、nested、`.`/`..` segment、empty/alternate separator和
不等价root spelling；不得用`resolve()`、follow symlink、parent search或递归。无root的generic input read行为保持不变。

`persist_canonical_json`构造的target及其reload必须通过同一linkage gate。返回`FileIdentity.root`只能在该证明通过后赋值；
`require_same_target`继续比较所有字段。不得引入retained schema或SealTargetIdentity import。

### REV-P3-003：补齐明确negative matrix

新增或增强behavioral tests，至少逐项证明：

1. 三类open使用exact flags；`O_NOFOLLOW`或`O_DIRECTORY`缺失/zero/non-int时pre-open拒绝，call count为0；
2. root-bound read对outside、nested、dot/parent/alternate spelling在file lstat/open前拒绝，合法direct child成功；
3. failing exact read仍close descriptor exactly once，并保留原typed failure；close自身失败保持可见；
4. general target-open failure、opened target mode/device/inode drift分别typed reject，已创建target不被repair/rewrite；
5. root-open、root-fsync和root-close failure分别typed reject，证明file已close且physical target保留；
6. reload阶段的lstat/open/read failure至少各一项，证明target已完成file/root fsync后仍原位保留且没有第二次写入；
7. success继续证明partial write、write EINTR、file fsync、file close、directory fsync、root close、strict reload和
   exact call order/count；existing test的canonical/Git/import/immutability覆盖不得削弱。

每项核对error code、调用是否发生、次数/顺序、identity或physical bytes。不得只加source-token assertion，测试不得读取冻结
external evidence。

## 3. Explicit non-ownership和锁零

Helper/test仍不得包含retained artifact absolute paths、C1 hashes、Advisor/GUIDE facts、B2 manifest schema/payload、release
checkpoint、five-path facts或eligibility policy；不得import audit owner、controller/preparation、canonical validator、release
producer/consumer、network、DNS、credential/`.env`、camera、Ray、ESPHome、strip、cleanup、formal或public analyzer模块。

本包不拥有phase ordering、terminal/ER lifecycle、retained semantics、validator、eligibility、release或device state。P3 green
facts只作为rejected predecessor；不得声称已accepted。

## 4. Validation与exact commit sequence

所有步骤fail-fast、各exact一次、retry/fallback `0`：

1. 编辑后核对changed path set exact two、stage empty，运行`git diff --check`；
2. targeted：`.venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io`；
3. focused：`.venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_release_audit tests.test_p7_retained_r3_controller_preparation tests.test_p7_retained_r3_controller_integration`；
4. full：`.venv/bin/python -m unittest discover -s tests -p 'test_*.py'`，同一session捕获terminal exit与完整summary；
5. compileall：`.venv/bin/python -m compileall -q src/camera_based_rgbww_optimizer tests/test_p7_retained_r3_provenance_io.py`；
6. `codegraph sync` exact一次，再次核对exact two-path diff与`git diff --check`；
7. 只stage exact two targets；证明cached exact two、unstaged/untracked extra为0、cached diff check通过；
8. 创建唯一successor repair commit，subject exact
   `fix(p7): harden retained r3 provenance io boundary`；不得amend/rebase/merge/tag/push/PR；
9. 证明direct parent为activation commit、subject/paths exact，记录before/after blob OID、bytes/SHA和canonical binary
   patch SHA-256；worktree/stage clean；
10. postcommit targeted exact一次并pass；只向`.agent-work/EXECUTION_RESULT.md`追加完整handoff并stop。

Executer不得把ER加入implementation commit。任何gate失败保留现状，禁止retry、替代commit、repair evidence或修改PLAN/FULL，
如实append ER并回Planner。

## 5. Acceptance evidence

ER至少记录activation/implementation topology、pre/post status、两文件before/after identity、diff/stage sets、全部validation
argv/count/exit/summary、patch SHA、每个REV关闭证据、negative matrix、所有zero budgets及preserved state。

Planner仅在以下全部满足时接受：exact two-path successor；REV-P3-001/002/003均以behavioral test关闭；targeted/focused/full/
compileall/CodeGraph/diff/postcommit全部pass；无owner泄漏；worktree/stage在ER前clean；所有machine-contract zero budgets为0。

即使P3-C1接受，也只允许Orchestrator把`REF-P7-25-R2-B2-R2`重新标为`READY_FOR_PLANNING`。不得直接运行real
B2/B3/B4，不得声称retained R3 validated、eligible或consumable。

## 6. Locks与授权

external evidence reads/root、retained release audit、canonical validator、eligibility、release generation/qualification/copy/
consumption、network/DNS/`.env`/credentials、设备、相机、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、
sentinel、P8、firmware和deployment全部hard locked at zero。

这是纯离线工程纠偏，不涉及科学分支或高风险设备操作，不需要Advisor或Human授权。唯一stop为
`B2_P3_C1_REPAIR_WAITING_PLANNER_REVIEW`；到达后必须由Planner独立验收，再由Orchestrator决定FULL状态。

## 维护性判断

纠偏保留单一helper/test owner，只加fail-closed capability和direct-child invariant，不扩展controller、manifest、validator或release
边界。测试矩阵会增加，但复杂度仍集中于高风险I/O owner；P3-C1后不建议重构，直到出现第三个稳定consumer。
