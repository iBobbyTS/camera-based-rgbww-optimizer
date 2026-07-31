# REF-P7-25-R2-B2-P3：repo-owned provenance I/O boundary

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-P3`

**Contract ID：** `P7-TD-B-RETAINED-R3-PROVENANCE-IO-BOUNDARY-V1`

**当前唯一动作：** Orchestrator 独立审核并激活后，Executer只实现、测试并提交一个repo-owned、可依赖注入的
local provenance file/Git I/O helper及其dedicated test。不得读取C1或retained-R3 artifacts，不得运行real B2。

**预计时长：** `<10 minutes`；不使用visible Terminal、automation或后台长任务流程。

**唯一执行 stop：** `B2_P3_IMPLEMENTATION_WAITING_PLANNER_REVIEW`。

**本次 rejection review archive：**
`.agent-work/PLANS/20260730-2107-p7-retained-r3-option-b-b2-r2-maintainability-rejection.md`，
bytes `4000`，SHA-256
`7caaabac760b9248b4476d45ae1888e2ada964e024328c40f9320b8eddc8a78c`。

**保留的 predecessor transition archive：**
`.agent-work/PLANS/20260730-1352-p7-retained-r3-option-b-b2-r2-real-manifest-transition.md`，
bytes `4410`，SHA-256
`9e255b0dbe9a8f4cbb431906d65ce396601469c21f1b3cae60cd814edc2c859a`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_provenance_io_boundary_plan_v1","reference_task_id":"REF-P7-25-R2-B2-P3","contract_id":"P7-TD-B-RETAINED-R3-PROVENANCE-IO-BOUNDARY-V1","execution_authorized":true,"activation_required":true,"activation_commit":{"expected_parent":"38cd2452433d449ab0b6476f3336d92ca19d9143","expected_subject":"chore(plan): activate retained r3 provenance io","exact_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260730-2107-p7-retained-r3-option-b-b2-r2-maintainability-rejection.md"]},"implementation_commit":{"expected_subject":"feat(p7): add retained r3 provenance io boundary","exact_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py","tests/test_p7_retained_r3_provenance_io.py"],"commit_count":1},"scope":{"production":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py","test":"tests/test_p7_retained_r3_provenance_io.py","exact_path_count":2},"validation":{"targeted":1,"focused":1,"full":1,"compileall":1,"codegraph_sync":1,"precommit_diff_check":1,"postcommit_targeted":1,"retry":0,"fallback":0},"zero_budgets":{"external_evidence_reads":0,"external_root_creation":0,"retained_release_audit":0,"canonical_validator":0,"eligibility":0,"release_operation":0,"network":0,"environment":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"planner_stop":"B2_P3_IMPLEMENTATION_WAITING_PLANNER_REVIEW"}`

## 1. Activation、输入与工作区 gate

Executer不得在Orchestrator activation前执行。Activation commit必须满足machine contract的exact parent、subject和
exact three-path plan/archive topology；激活后的FULL必须同时满足：

- `active_task_count=1`，active task/contract exact为本包；
- `retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`；
- P1 accepted commit `4678a3e6f93704912952776bc11fa2b0945d80b1`与P2 accepted commit
  `4e82a7d089ff8bc4baef653a4a19f85d23d0b882`均为HEAD ancestors；
- `REF-P7-25-R2-B2-R2`仍为maintainability rejection，real B2/B3/B4均未解锁。

执行前记录HEAD、activation parent/subject/changed paths、stage和worktree。PLAN、FULL与review archive activation已经committed后，工作区必须clean；
两个target path必须均不存在于HEAD、index与worktree。任一不符即pre-edit hard failure：edit/test/CodeGraph/commit均为0，只向
`.agent-work/EXECUTION_RESULT.md`追加一次真实handoff并停下；不得修PLAN/FULL、不得删除或接管ambient work。

本包可读取repo source、tests、docs、Git object database和CodeGraph index。禁止读取
`/Volumes/4T/temp/rgbww-optimizer`中的任何C1、retained-R3、release或旧run artifact；禁止创建external evidence root。

## 2. Exact ownership and public behavior

实现范围exact two paths：

1. `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py`；
2. `tests/test_p7_retained_r3_provenance_io.py`。

Production helper是通用local provenance I/O boundary。它可以定义少量frozen dataclass、一个带稳定machine-readable code的typed error、
明确的public functions和一个集中式dependency bundle；不得新增package、wrapper、CLI、config、fixture、generated source或第三repo path。
所有返回的identity、seal和Git ledger必须是detached immutable values；不得把mutable dependency-owned buffer/mapping直接暴露给caller。

Helper只拥有以下primitive behavior：

- exclusive创建一个exact root：单次`mkdir(mode=0700)`，随后non-following identity验证为directory、mode `0700`；不得递归建parent、
  删除、清空、chmod或复用existing path；
- exact file read：non-following `lstat`，`O_RDONLY|O_NOFOLLOW` open，fstat-before，循环read至冻结size再额外探测1 byte，fstat-after，
  SHA-256与mode验证；lstat/fstat的device、inode、type、mode、size必须一致，truncation/growth/rebind/symlink均fail closed；
- canonical JSON：UTF-8 strict、compact sorted keys、`ensure_ascii=False`、`allow_nan=False`、exact one terminal LF；strict decode拒绝BOM、
  duplicate key、NaN/Infinity、non-canonical bytes、额外LF或trailing bytes，并以re-encode exact equality完成reload验证；
- exclusive canonical JSON persist：target filename必须是一个安全的direct child；以
  `O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`, mode `0600`写入，正确处理partial write与`EINTR`，file fsync、close、root directory fsync，
  再用同一read primitive reload并核对bytes/hash/identity；不得replace、repair或rewrite已创建target；
- physical target/seal linkage：把path、bytes、SHA-256、device、inode、mode与root identity冻结成typed identity，并提供exact comparison gate，
  使future caller可安全构造现有preparation owner的`SealTargetIdentity`；本helper不生成terminal payload、不append ER；
- local read-only Git runner：只接受下面冻结的command grammar，始终使用argv、`shell=False`、exact repo cwd、closed stdin与captured byte output；
  返回包含immutable argv、exit code、stdout/stderr bytes及其SHA-256的ledger，不吞掉nonzero exit。process launch/OS failure抛typed error。

允许的Git grammar仅为：

- `git rev-parse --verify <full-lowercase-sha>^{commit}`；
- `git show -s --format=%H%x00%P%x00%s <full-lowercase-sha>`；
- `git diff-tree --no-commit-id --name-only -r -z <full-lowercase-sha>`；
- `git rev-parse <full-lowercase-sha>:<exact-safe-repo-relative-path>`；
- `git diff --binary --full-index --no-ext-diff <full-parent-sha> <full-child-sha> -- <one-or-more-exact-safe-repo-relative-paths>`。

SHA必须exact 40 lowercase hex。Repo-relative path必须非空、非absolute、无NUL、无`.`/`..` segment、无重复slash；patch path tuple必须
nonempty、sorted且unique。禁止prefix/path glob allowlist、shell string、`-C`、config override、revision range、worktree-content command、Git mutation
subcommand或任何未列shape。Runner只证明command execution事实，不解释commit、path、blob或patch是否符合retained manifest；这些facts由future B2 caller核对。

## 3. Explicit non-ownership

Helper和test均不得包含retained artifact absolute paths、C1 hashes、Advisor/GUIDE facts、B2 manifest schema/payload、release checkpoint、
five-path facts或eligibility policy。不得import或调用：

- `optimization.p7_retained_release_audit`的private/public audit entry；
- exact-five controller或controller preparation owner（类型转换留给future composition caller）；
- canonical TD-B validator、release generator/qualifier/consumer；
- network、DNS、credential/`.env`、camera、Ray、ESPHome、strip、cleanup、formal或public analyzer modules。

本helper不拥有phase ordering、retry/fallback、manifest scientific semantics、terminal lifecycle、ER ordering、canonical validation、eligibility、release或
device state。不得复制或重构旧audit private helpers；可以遵循其dependency-injection设计原则，但实现必须是本module内独立、tested public boundary。

## 4. Dedicated negative/positive test matrix

Dedicated test必须用dependency injection与disposable test directories验证真实行为，不访问任何冻结external evidence。至少覆盖：

1. exclusive root成功的0700 identity；existing file/directory、symlink、错误type/mode、mkdir/lstat identity drift均拒绝；
2. exact read成功并冻结path/bytes/hash/dev/inode/mode/size；symlink、non-regular、错误mode/hash/size、lstat-open rebind、fstat before/after drift、
   read-time growth、truncation、short/partial reads与read `EINTR`；fd close在success/failure路径恰好一次，close failure可见；
3. canonical encode/decode/reload成功；duplicate keys、NaN、Infinity、BOM、invalid UTF-8、unsorted/pretty JSON、missing LF、double LF、trailing bytes、
   unsupported non-JSON value全部拒绝；
4. exclusive persist成功覆盖partial writes和write `EINTR`，验证0600、file fsync、close、directory fsync、strict reload与physical target identity；
   unsafe child、existing target、symlink、root identity drift、open/mode/dev/inode mismatch、zero-progress write、fsync/close/reload failure均拒绝，且无repair/rewrite；
5. target/seal exact comparison成功；path/bytes/hash/device/inode/mode/root任一漂移均拒绝；
6. 每个允许Git shape的argv、cwd、shell/stdin/capture参数exact，completed exit `0`与nonzero均返回truthful immutable ledger和byte hashes；
   malformed SHA/path、unsorted/duplicate path set、extra/missing token、unknown/read-write command、shell syntax均在process invocation前拒绝；
7. mutation attempts不改变input dataclass/identity/ledger；unknown或non-callable dependency override fail closed；
8. AST/import guard证明production module无network/env/device/retained-specific owner imports，不使用`os.environ`、shell、temp root或write-capable Git命令。

测试不得仅断言“调用未抛异常”；每项必须核对result identity/ledger、错误code、call count/order或preserved physical target等真实语义。

## 5. Validation and exact commit sequence

所有步骤fail-fast、各exact一次、retry/fallback `0`：

1. 编辑后先核对changed/untracked path set exact为两个target，stage为空；运行`git diff --check`；
2. targeted：
   `.venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io`；
3. focused owner compatibility：
   `.venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_release_audit tests.test_p7_retained_r3_controller_preparation tests.test_p7_retained_r3_controller_integration`；
4. full：
   `.venv/bin/python -m unittest discover -s tests -p 'test_*.py'`，必须在同一session捕获完整summary与exit `0`；
5. compileall：
   `.venv/bin/python -m compileall -q src/camera_based_rgbww_optimizer tests/test_p7_retained_r3_provenance_io.py`；
6. 因repo存在`.codegraph/`，运行一次`codegraph sync`并记录exit；随后再次核对exact two-path diff与`git diff --check`；
7. 只stage两个target，证明staged path set exact two、unstaged/untracked extra path为0；创建唯一implementation commit，subject exact
   `feat(p7): add retained r3 provenance io boundary`；
8. commit后证明direct parent为activation commit、subject exact、changed path set exact two，记录before/after blob OID、file bytes/SHA-256和
   canonical binary patch SHA-256；worktree/stage clean；
9. postcommit targeted exact一次并要求pass；随后只向`.agent-work/EXECUTION_RESULT.md`追加一次完整handoff并停在Planner gate。

Executer不得把ER包含进implementation commit，不得amend、rebase、merge、tag、push或创建PR。若CodeGraph sync产生target外repo diff，视为scope failure，
保留并报告，不得删除他人/既有内容；由Orchestrator整理。

## 6. Evidence, acceptance and failure branches

ER handoff至少记录：activation/implementation topology；pre/post status；两文件before/after存在性、bytes、SHA、blob OID；diff/stage path sets；
targeted/focused/full/compileall/CodeGraph/diff/postcommit的argv、invocation count、exit与test summary；Git patch SHA；negative matrix coverage；所有zero budgets；
以及任何preserved uncommitted/physical target状态。

Planner只有在以下条件全部满足时才可接受：

- exact two-path helper/test commit，no additional path；全部required validation及postcommit targeted pass；
- test matrix证明file identity、canonical persistence、seal linkage和Git grammar fail closed；
- helper保持generic validation-only I/O boundary，无retained scientific/eligibility/release/device owner泄漏；
- worktree/stage在ER append前clean，ER只作为review handoff保留；
- external evidence reads/root、actual audit/validator/eligibility/release/network/device等machine-contract zero budgets全为0。

失败分支：

- pre-edit/scope gate失败：不编辑target、不运行validation或commit，ER一次后stop；
- implementation、targeted、focused、full、compileall、CodeGraph或precommit gate失败：保留exact diff与日志，不commit、不retry，ER一次后stop；
- stage/commit topology失败：不创建替代commit、不amend，保留状态并回Planner；
- postcommit targeted失败：保留该commit，不revert/amend/retry，记录为rejected candidate并回Planner；
- ER append失败：不得以修改PLAN/FULL、stderr success claim或另一个evidence root代替，如实回报Orchestrator。

即使P3被接受，也只允许Orchestrator把`REF-P7-25-R2-B2-R2`重新标为`READY_FOR_PLANNING`。不得直接运行real B2/B3/B4，
不得声称retained R3 validated、eligible或consumable。

## 7. Locks and authorization

`run_retained_release_audit`、canonical validator、eligibility、release generation/qualification/copy/consumption、C1/retained artifact reads、external root、
network/DNS/`.env`/credentials、设备、相机、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware与deployment全部hard locked at zero。

本包是纯离线工程实现，不包含科学分支或高风险设备操作，不需要Advisor或Human授权。唯一stop为
`B2_P3_IMPLEMENTATION_WAITING_PLANNER_REVIEW`；到达后必须由Planner独立验收，再由Orchestrator决定FULL状态与real B2 re-entry。

## 维护性判断

P3将原本散落在一次性external launcher中的高风险filesystem/process细节收敛到一个generic、dependency-injected、dedicated-tested owner；
exact-five仍独占phase lifecycle，preparation仍独占terminal/ER admission，未来B2仍独占retained manifest facts。新增复杂度限制在一个helper和一个test，
并以严格negative matrix保护；当前不建议重构旧audit，待B2/B3/B4出现第三个稳定consumer后再评估共享抽象。
