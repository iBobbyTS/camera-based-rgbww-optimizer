# REF-P7-25-R2-B2-R2：repo-owned real B2 manifest-only re-entry

**计划状态：** `PLANNER_READY_WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-R2`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-REAL-MANIFEST-ONLY-V1`

**当前唯一动作：** Orchestrator先独立审核本PLAN并更新其独占FULL machine state；只有Orchestrator把
本PLAN的`execution_authorized`改为exact `true`、以exact parent/subject提交该activation且FULL同时绑定本task/contract/candidate
identity后，Executer才可运行一次下面冻结的pure-offline real-input manifest-only controller。

**预计时长：** `<10 minutes`；不得使用visible Terminal、automation或后台长任务流程。

**唯一执行stop：** `B2_R2_TERMINAL_WAITING_PLANNER_REVIEW`。

**本次transition archive：**
`.agent-work/PLANS/20260730-1352-p7-retained-r3-option-b-b2-r2-real-manifest-transition.md`，
bytes `4410`，SHA-256
`9e255b0dbe9a8f4cbb431906d65ce396601469c21f1b3cae60cd814edc2c859a`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_r2_real_manifest_plan_v1","reference_task_id":"REF-P7-25-R2-B2-R2","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-REAL-MANIFEST-ONLY-V1","execution_authorized":false,"activation_required":true,"activation_commit":{"expected_parent":"d490d707f6bdc7c8acfa98f224d0ab332083a844","expected_subject":"chore(plan): activate retained r3 real b2 manifest","exact_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260730-1352-p7-retained-r3-option-b-b2-r2-real-manifest-transition.md"]},"candidate_contract":{"schema":"p7_td_b_b2_r2_real_manifest_candidate_v1","accepted_owner_commits":{"preparation":"4678a3e6f93704912952776bc11fa2b0945d80b1","integration":"4e82a7d089ff8bc4baef653a4a19f85d23d0b882"},"c1_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z","c1_evidence":[{"name":"path-owner-index.json","bytes":12195,"sha256":"b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35"},{"name":"path-owner-index.sha256.json","bytes":682,"sha256":"867d1ffad5bd29f24dc81b24a58ce66393dd688833d3a4516fe7f45ef50875e9"},{"name":"terminal-evidence.json","bytes":13455,"sha256":"c21a691272ca7466271349daa5b10236c9f36dfeb481d592e9c368a87e7a4763"},{"name":"terminal-evidence.sha256.json","bytes":772,"sha256":"4bfebf4ad40e8c2e65ad2470faaed184f21d39eda73c13e689b09769d280752f"}],"retained_artifacts":[{"name":"current-lineage-candidate.json","path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3/current-lineage-candidate.json","sha256":"3a2ff5a2af200c55c925b954488c5c5dd31a35a481440d17dfcdd8b68419f2e0"},{"name":"resolved-formal-plan.json","path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3/resolved-formal-plan.json","sha256":"cf7c78b6a6cfda4055d05f5e9bbe9914161213b380dc7736ee09e257dd45eb6b"},{"name":"setup-lineage-release.json","path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3/setup-lineage-release.json","sha256":"0bacf1878a97fcdc4436259e132e89f6e56611df6d7fb5d5a7da28f62c98ad3e"}],"output_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-real-manifest-4e82a7d-20260730T1952Z","output_names":["progressive-00-acquisition.json","retained-r3-audit-provenance-manifest-v2.json","retained-r3-audit-provenance-manifest-v2.sha256.json","terminal-evidence.json","terminal-evidence.sha256.json"],"manifest_schema":"p7_retained_r3_audit_provenance_manifest_v2","manifest_status":"sealed_subordinate_provenance_evidence","retained_status":"RETAINED_UNVALIDATED_UNCONSUMED","retry":0,"fallback":0},"candidate_identity_sha256":"859177dbad53bd2118b1c537af36dcaf1f9cf7b59490ee2806ab3f7166c59b8a","launcher":{"kind":"single_external_python_io_wiring_source","source_generates_source":false,"direct_owner_imports":["camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_preparation","camera_based_rgbww_optimizer.utils.p7_retained_r3_exact_five_controller"],"preexecution_ast_parse":1,"preexecution_compile":1,"controller_invocations":1},"read_budgets":{"c1":{"lstat":4,"open":4,"read":4,"hash":4},"retained":{"lstat":3,"open":3,"read":3,"hash":3}},"write_budgets":{"root_mkdir":1,"progressive":1,"manifest":1,"manifest_seal":1,"terminal":1,"terminal_seal":1,"execution_result_append":1},"actual_zero_budgets":{"run_retained_release_audit":0,"canonical_validator":0,"eligibility":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"git_mutation":0,"tests":0,"compileall":0,"codegraph":0,"network":0,"env":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"planner_stop":"B2_R2_TERMINAL_WAITING_PLANNER_REVIEW"}`

## 1. Frozen owners and activation gate

Executer不得在Orchestrator activation前执行。Activation后先通过committed machine-contract parser各exact一次读取PLAN/FULL，要求：

- actual activation child的direct parent/subject/changed-path set与machine contract exact一致；
- FULL `active_task_count=1`、task/contract exact本PLAN、`retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`；
- FULL candidate SHA等于本PLAN `candidate_identity_sha256`且`candidate_contract_orchestrator_verified=true`；
- HEAD仍包含accepted preparation commit `4678a3e...`、integration commit `4e82a7d...`及其已接受owner/test bytes；
- worktree不得有PLAN/FULL/ER之外的ambient drift，stage必须为空。本包不修改、不stage、不commit repository内容。

任一gate失败必须在external root创建前停止，只追加一次truthful ER；不得建立alternate root、repair PLAN/FULL或retry。

## 2. Single launcher and no-second-state-machine contract

唯一允许的external launcher是一个短Python I/O wiring source。Executer先在output root之外的固定external staging path物化一次，随后：

1. non-following lstat/open/read冻结source path、bytes、SHA-256、dev/inode/mode；
2. 对exact frozen bytes执行一次UTF-8 strict decode、`ast.parse`与`compile(..., mode="exec")`；
3. static AST要求只直接import standard-library I/O/Git primitives与machine contract parser、上述两个committed owners；禁止import
   `p7_retained_release_audit` real audit entry、canonical TD-B validator、release consumer、camera/Ray/ESPHome/network modules；
4. source不得包含`exec`/`eval`/`compile`/`ast.parse`/source template/heredoc writer，不得生成、patch或执行第二段source；
5. 用同一冻结source恰好启动一次controller。执行中launcher自核source identity与outer freeze一致。

Launcher只实现callback所需的local file descriptor、canonical JSON persistence与local read-only Git plumbing；它不得自行排序阶段、catch后继续、
dispatch第二controller、实现retry/fallback或决定eligibility。唯一phase/failure/terminal owner必须是
`execute_prepared_exact_five_controller`；terminal canonical bytes、target linkage与ER admission必须调用preparation owner的
`canonical_terminal_bytes`、`SealTargetIdentity`、`validate_and_emit_execution_result`。

Exact-five callback字段沿用committed API，但本包语义必须在manifest/terminal中明确区分：

| Lifecycle callback | 本包唯一允许语义 |
| --- | --- |
| `acquire` | 读取/验证四件C1 evidence，再读取三件retained artifact并冻结identity |
| `materialize_one_entry` ×5 | 从本地Git object database重算并核对exact five accepted integration path facts；不写repo |
| `import_static_gate` | launcher source/import/static forbidden-surface gate |
| `targeted_gate` | manifest payload schema/authority-negative pure self-check；不运行test |
| `focused_gate` | C1/retained read ledger、identity和hash pure self-check；不运行test |
| `full_gate` | complete integration-chain/Git-object recomputation self-check；不运行test |
| `single_commit` | exact guard `git_mutation=stage=commit=0`；不得调用Git mutation |
| `subordinate_manifest_seal` | exclusive persist/reload/seal唯一v2 manifest |
| `canonical_validator` | **仅** exact guard `actual_canonical_validator_calls=0`；不得import/call validator，不得emit eligibility |
| `terminal_seal` | exclusive persist terminal+terminal seal，并经preparation owner admission一次ER |

因此terminal必须同时记录`lifecycle_callback_counts.canonical_validator=1`和
`actual_operations.canonical_validator_calls=0`；禁止把前者表述为validator运行或eligibility证据。

## 3. Exact C1 and retained read contract

Root创建前C1四件和retained三件均不得probe。Controller以`os.mkdir(mode=0700)`对machine contract exact output root调用一次；若非ENOENT、
symlink、已有entry或mode/dev/inode异常则fail closed，不得删除/清空/复用。

Root建立后先exclusive persist `progressive-00-acquisition.json`，记录activation、launcher freeze、root identity、预算初值和
`retained_r3_status`。随后严格按machine contract顺序读取四件C1 evidence：每件exact一次non-following lstat、一次
`os.open(O_RDONLY|O_NOFOLLOW)`、一次`os.read(fd, lstat_size+1)`、一次SHA-256；open前lstat、open后/读取后fstat的
dev/inode/mode/size必须exact相等，regular non-symlink mode0600，bytes/hash与冻结值相等。严格JSON parse必须拒绝duplicate key、NaN/
Infinity、non-UTF8、非canonical compact sorted JSON+exact one LF；四件schema/status依次须等于accepted C1 review。Exact bytes已绑定
resolved records，因此launcher不得recursive search、alternate pointer猜测或目录枚举。

只有四件全通过后，才按PLAN冻结的三个absolute path顺序读取retained artifacts。每件同样只允许一次lstat/open/read/hash，使用
`os.read(fd, lstat_size+1)`并做lstat/fstat-before/fstat-after exact identity；必须regular non-symlink mode0600、basename/path/hash exact。
不得parse其scientific/release payload、mmap、copy、rewrite、touch或follow sibling/parent。Before/after identity指同一open file description
读前/读后fstat，不允许为“after”增加第二次path probe。

## 4. Manifest facts and local Git recomputation

Manifest必须是canonical compact sorted UTF-8 JSON+exact one LF，schema/status exact machine contract且只能表示sealed subordinate evidence。
它至少绑定：

- GUIDE SHA `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`、decision evidence SHA
  `842cfad090549ebf6379df4551bd4f051267e4bf93014f899c5e329c57085620`、Advisor attachment SHA
  `91a88e5467e13c811794c2149b6a8d5669e613c3e259d8f4091ba08c048733d6`与Human engineering-governance override；
- setup checkpoint `9c804abdeabbc5da18a66d0acf25a1f13128bc2d`和rollback/release checkpoint
  `32b9e670ff3bbea0cd1505528c2ca87c2935446c`；
- helper v1 `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`及exact disposition
  `retained_release_audit_prerequisite_v1_superseded_before_real_validation`、unconsumable/unauthorized negatives；
- integration baseline `3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c`、parent `9303aa2...`、181-path ledger SHA
  `9596c3fa8aee58259aff13b44badcc7d448e0555c80f166b20706dcd1e321118`；helper/test categories/scopes和其
  SHA `48c0...f8`/`c8d6...b3f`，其余179 paths exact classification
  `present_in_commit_not_authorized_by_this_manifest`；
- canonical chain commits `0682cd8...`、`ba81621...`、`a9a8171...`、`3a14fe0...`、`7c31c1b...`的full SHA、direct parent、
  subject、exact changed paths、before/after blob OIDs与canonical binary patch SHA；
- governance manifest path/SHA `69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e`；
- C1四件physical identities/read ledgers和三件retained path/bytes/hash/before-after identity；
- `production_runtime=false`、validation-only scope、generation/copy/consumption/device/formal authority all false/none；
- actual validator/audit/eligibility/release/Git mutation/tests/network/device等zero counters。

所有commit/path/blob/patch/file facts必须由launcher使用local read-only Git命令从object database独立重算，并与PLAN/FULL accepted constants核对；
不得从ambient working-tree bytes替代historical object。Git command argv/output/exit必须落manifest ledger。任一unknown/extra path、prefix match、
generic allowlist、worktree substitution或identity mismatch失败。

## 5. Persistence, terminal and ER ordering

所有五个output files只能在同一root中用`O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`, mode0600写入；必须handle partial writes、file fsync、close、
directory fsync，再non-following lstat/open/read strict reload核验canonical bytes和SHA。Reload是output validation，不计input read budgets。
Manifest seal必须绑定manifest path/bytes/SHA/dev/inode/mode/schema/status及writer-return fact；manifest/manifest seal一旦返回不得rewrite、replace、
relocate或repair。

成功或任何post-root failure均必须由exact-five owner走唯一terminal callback。Terminal记录phase结果、truthful pre-terminal counters、root/launcher/
input/output identities、manifest seal（若存在）、actual zero budgets与唯一Planner stop；terminal seal独立绑定physical terminal target。只有
`validate_and_emit_execution_result`验证terminal bytes内target与physical terminal `SealTargetIdentity` exact相等后，才允许向
`.agent-work/EXECUTION_RESULT.md`追加一次。若terminal writer或seal失败，ER append必须0并保留已有physical evidence；不得以stderr或手写ER代替。

## 6. Acceptance branches and locks

Planner只接受以下success：五件output exact、C1 `4/4/4/4`、retained `3/3/3/3`、全部identity/hash/Git facts通过、manifest与terminal seal有效、
ER在seal后exact一次，retry/fallback0，所有actual zero budgets exact0。接受也只解锁B3；不得报告retained R3 validated、eligible或consumable。

任一pre-root gate失败：root/output/input reads全0，ER一次记录pre-root stop。任一post-root失败：保留root与已写evidence，尽力terminal+seal；
无retry、fallback、alternate root、repair/rewrite/second manifest。失败后回Planner，不得进入B3。

Canonical validator、`run_retained_release_audit`、eligibility、release generation/qualification/copy/consumption、repo edit/stage/commit、tests、
compileall、CodeGraph、network/DNS/`.env`/credentials、设备、相机、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、
firmware与deployment全部hard locked at zero。本包无科学分支或高风险设备操作，不需要Advisor或Human授权。

## 维护性判断

本PLAN复用单一repo-owned lifecycle与preparation/seal gate；唯一外置source只提供必要I/O callbacks，不拥有phase transition、eligibility或release。
没有新增production path、generated controller或第二state machine，真实I/O预算与后续B3/B4职责分离清楚。
