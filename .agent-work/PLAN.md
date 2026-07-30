# REF-P7-25-R2-B2-C1：retained R3 exact path-owner index

**计划状态：** `EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-C1`（`REF-P7-25-R2-B2` 的 bounded corrective branch；等待 Orchestrator 同步 FULL）

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C1-PATH-OWNER-INDEX-V1`

**预计时长：** `1–3 分钟`；不得运行测试、validator、audit 或设备任务，不属于预计超过 10 分钟的长任务。

**唯一当前动作：** Executer 使用一个本地 Python controller、一次 invocation 和一个 brand-new external root，只验证历史证据已明确命名的 retained package 三层 exact directory chain，通过 non-following `lstat` 与受控 direct-entry listing 建立 artifact name/type/absolute-path index；不得打开、读取、hash 或解析三个 artifact 的内容。

**Planner stop：** `B2_C1_PATH_OWNER_INDEX_WAITING_PLANNER_REVIEW`。成功也不得重试 B2 manifest seal、运行 canonical validator/audit、读取 artifact 内容、发出 eligibility、消费 release 或进入任何后续阶段。

**被拒收计划 archive：**
`.agent-work/PLANS/20260730-1547-p7-retained-r3-option-b-b2-modern-manifest-failure-review.md`，bytes `5916`，SHA-256
`1c0cf905e468bad0a3349fe884775aa70ffb5201af74cddce8c4a770007e3c50`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_c1_path_owner_plan_v1","reference_task_id":"REF-P7-25-R2-B2-C1","parent_reference_task_id":"REF-P7-25-R2-B2","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-C1-PATH-OWNER-INDEX-V1","dispatch_state":"execution_authorized","execution_authorized":true,"single_current_action":"single_controller_exact_directory_chain_path_owner_index","evidence_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z","controller_invocations":1,"evidence_root_creations":1,"directory_lstat":3,"directory_scandir":3,"artifact_content_open":0,"artifact_content_read":0,"artifact_content_hash":0,"artifact_content_parse":0,"path_owner_index_writes":1,"index_seal_writes":1,"terminal_writes":1,"terminal_seal_writes":1,"retry":0,"fallback":0,"canonical_validator_calls":0,"audit_calls":0,"manifest_seal_calls":0,"er_appends":1,"planner_stop":"B2_C1_PATH_OWNER_INDEX_WAITING_PLANNER_REVIEW"}`

## 1. Frozen review inputs and disposition

1. B2 failure archive exact：
   `.agent-work/PLANS/20260730-1547-p7-retained-r3-option-b-b2-modern-manifest-failure-review.md`，bytes `5916`，SHA-256
   `1c0cf905e468bad0a3349fe884775aa70ffb5201af74cddce8c4a770007e3c50`。
2. Historical package review exact：
   `.agent-work/PLANS/20260727-2241-p7-lineage-release-r3-r2-audit-ledger-shape-review.md`，bytes `6090`，SHA-256
   `90521d3e6c4461dbf1816ab894b46e33d536ba38ba47727f887d2495ab3231e6`。
3. Historical exact source review exact：
   `.agent-work/PLANS/20260727-2313-p7-retained-r3-c1r2-third-failure-reassessment-stop-review.md`，bytes `9695`，SHA-256
   `e02b169a9b8ec84d113461695b7d68f4552ce4f2973b982cf5589dc444c575ae`。
4. 三个 archive 各只允许 regular/non-symlink identity check 与一次 `O_RDONLY|O_NOFOLLOW` open/read/hash；必须验证 bytes/SHA 与本节 exact 值。历史文本必须分别包含 frozen package root、exact source chain、三个 artifact name 和预期 SHA。它们仅是 path-owner 选择依据，不是当前 artifact content identity 的替代证明。
5. 被拒 B2 root、terminal、错误 frozen path 与 retained artifact 均不得再次访问。本包不得把旧 B2 的 `lstat=1` 解释为 retry budget，也不得复用其 root、controller 或任何 partial evidence。
6. Retained state 继续是 `RETAINED_UNVALIDATED_UNCONSUMED`。历史 expected SHA 只能以 `historical_expected_sha256` 标签写入 index；本包不得声称 observed/current hash、validated、eligible、consumable 或 release usable。

## 2. Dispatch and fresh evidence owner

1. Executer 开始时只读取一次 symbolic `git rev-parse HEAD` 并绑定 full SHA。工作区必须 staged/unstaged/untracked 均为 `0`；否则在 evidence root 创建前停止并向 Planner 报告，不得自行提交、清理或修改任何用户/Orchestrator work。
2. Active PLAN 必须是本 contract，且 `git show HEAD:.agent-work/PLAN.md` 与 working bytes 一致。Executer不得手工冻结或猜测 activation child SHA；programmatic dispatch HEAD 是唯一 dispatch owner。
3. Exact brand-new evidence root：
   `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z`。
   Controller invocation 前必须 absent；只允许 controller 以一次 `os.mkdir(mode=0700)` 创建。禁止预创建、复用、删除、repair、rename、second root 或 timestamp fallback。
4. 只允许一个本地 Python controller process/invocation。禁止第二 Python/shell controller、inline probe、preflight path listing、manual path test、retry 或 fallback。Executer可在 dispatch 后构造并一次启动 inline controller；不得把 controller source 写入 repository 或创建 Git commit。
5. Repository 唯一允许的执行后变更是 terminal seal durable 后向 `.agent-work/EXECUTION_RESULT.md` append exactly once。Executer不得编辑 PLAN、FULL、archive、GUIDE、source、test、config、docs、skill 或 wrapper；repository implementation edit/commit=`0/0`。

## 3. Exact retained path-owner chain

Historical immutable reviews无歧义选择下列 chain；本包只验证此 chain，不做全盘搜索：

1. package root：
   `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227`
2. candidate child directory：
   `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output`
3. retained source directory：
   `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3`

对每层 exact directory 只执行：

- `os.lstat` exactly once，要求 directory、non-symlink；记录 mode、uid、gid、dev、inode、size、mtime_ns、ctime_ns；
- `os.scandir` exactly once，只读取 direct entry，不递归；每个 `DirEntry` 只允许一次 `stat(follow_symlinks=False)`，记录 exact UTF-8 name、mode/type、uid、gid、dev、inode、size、mtime_ns、ctime_ns；
- entry 按 UTF-8 name byte order 排序后写入 index；禁止 glob、`rglob`、`walk`、parent listing、sibling listing、basename search、Spotlight、`find`、shell `ls`、network/DNS 或 alternate-root discovery。

Path chain acceptance：

- package root direct entries 必须包含 exact `child-output` 且其 entry type 为 non-symlink directory；其他 direct entries只可被记录，不得打开或遍历；
- `child-output` direct entries必须包含 exact `lineage-release-r3` 且其 entry type为 non-symlink directory；其他 direct entries只可被记录，不得打开或遍历；
- retained source direct-entry name set必须 exact：
  `current-lineage-candidate.json`、`resolved-formal-plan.json`、`setup-lineage-release.json`；additional/missing entry=`0`；三者 entry type均须 regular、non-symlink；
- 由已验证的 retained source directory 与三个 exact names 机械构造并记录三个 exact absolute paths。不得对三个 artifact 另行 `lstat`，不得 open/read/hash/parse/mmap/copy 它们，也不得跟随 symlink。

Historical expected content identities只能作为未复算的 reference metadata：

| Artifact | Historical expected bytes | Historical expected SHA-256 |
| --- | ---: | --- |
| `current-lineage-candidate.json` | `9819` | `3a2ff5a2af200c55c925b954488c5c5dd31a35a481440d17dfcdd8b68419f2e0` |
| `resolved-formal-plan.json` | `15137` | `cf7c78b6a6cfda4055d05f5e9bbe9914161213b380dc7736ee09e257dd45eb6b` |
| `setup-lineage-release.json` | `1567` | `0bacf1878a97fcdc4436259e132e89f6e56611df6d7fb5d5a7da28f62c98ad3e` |

Entry-stat size可与 historical expected bytes比较并写 `entry_size_matches_historical_expected`，但这不等价于 content hash或immutability验证，不能提升 authority。

## 4. Path-owner index and terminal seal

### 4.1 Index

成功时 exclusive-create `path-owner-index.json`，schema exact
`p7_retained_r3_path_owner_index_v1`，status exact
`path_owner_resolved_waiting_for_planner`，top-level keys exact：

`schema,status,created_at_utc,scope,authority,dispatch,historical_sources,directory_chain,direct_entry_manifests,resolved_artifact_paths,content_read_budget,counters,planner_stop`。

Required authority：

```text
scope = path_owner_and_entry_type_evidence_only
artifact_content_opened = false
artifact_content_read = false
artifact_content_hashed = false
artifact_content_parsed = false
retained_r3_validated = false
eligibility_authority = false
eligibility_emitted = false
consumable = false
release_authority = false
device_authority = none
formal_authority = none
```

`resolved_artifact_paths`必须恰为三个 absolute paths，并对每项记录name、entry stat/type、historical expected bytes/SHA、当前 content identity字段明确为`not_observed_by_this_package`。不得出现`eligible=true`、`validated=true`、`production_release_usable=true`或任何消费授权。

Canonical JSON使用 UTF-8、sorted keys、compact separators、`ensure_ascii=false`、`allow_nan=false`、single LF EOF；以 `O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`、mode0600写入，file fsync、close、directory fsync。随后新只读fd strict duplicate-key/non-finite reject reload并验证 canonical byte equality；这是读取新 index，不是读取 retained artifact。

### 4.2 Index seal, terminal, and terminal seal

同 root 按顺序 exclusive-create mode0600：

1. `path-owner-index.sha256.json`：绑定 index relative path、bytes、SHA-256、schema/status与evidence-root identity；strict reload并fsync。
2. `terminal-evidence.json`：schema exact `p7_retained_r3_b2_c1_path_owner_terminal_v1`；成功status exact `pass_waiting_for_planner`，失败status exact `hard_failure_waiting_for_planner`；绑定dispatch、historical source reads、directory lstat/scandir/entry-stat budgets、artifact content zero counters、index/seal identities、所有locks及Planner stop。Terminal须区分`terminal_write_budget=1`与物理写回后的confirmed状态，不得再次制造旧B2的自相矛盾`terminal_writes=0`实际计数字段。
3. `terminal-evidence.sha256.json`：在 terminal writer return 后创建，绑定terminal relative path、bytes、SHA-256、schema/status、terminal write returned=true及root identity。此文件是terminal物理完成的non-circular seal；不得声称它自证自身write return。

四个JSON writer共用同一个 no-clobber canonical owner；每个均 file+directory fsync、strict reload、canonical byte equality。Index seal后任何后续错误不得改写index/seal，只能写一次 failure terminal及terminal seal后停止。任何已存在目标、partial write、reload mismatch或fsync error均hard failure，不得repair/rewrite/delete/replace。

## 5. Exact budgets and acceptance criteria

成功验收必须同时满足：

```text
controller process/invocation = 1/1
evidence root create = 1
historical archive regular/non-symlink open/read/hash = 3/3/3
directory lstat = 3
directory scandir = 3
direct-entry stat = exactly one per observed direct entry
artifact separate lstat = 0
artifact content open/read/hash/parse/mmap/copy = 0/0/0/0/0/0
path-owner index/index seal/terminal/terminal seal writes = 1/1/1/1
retry/fallback/alternate root/parent listing/sibling listing/recursive search = 0
repository implementation edit/commit = 0/0
EXECUTION_RESULT append = 1
```

Success evidence必须证明：三个 frozen archive identity exact；三层 directory chain各自是现存regular directory/non-symlink；两层owner child name/type relation成立；retained source direct entries exact three regular/non-symlink artifacts；三个resolved absolute paths无歧义；四个新JSON strict canonical并durably sealed；所有content与locked operations为零。

任何 archive/path/type/name/cardinality/identity/listing/budget/serialization/persistence mismatch立即 fail closed。失败可写一次truthful terminal+terminal seal并append ER，但不得尝试第二路径、列举上级目录、读取artifact、运行B2 manifest controller或继续后续步骤。

## 6. Hard locks

- B2 manifest writer/seal、canonical retained validator、retained audit helper、public replay、consumer、eligibility emission、release generation/qualification/copy/consumption均为`0`。
- Tests、compileall、CodeGraph、Git mutation、source/test/config/doc/skill/wrapper edit均为`0`。
- Network、DNS、`.env`、credential、device、camera、Ray、strip、cleanup、capture、CR3、NPY、FORMAL-R6、public analyzer、TD-C、sentinel、P8、firmware、deployment均为`0`。
- 本包是pure-offline path ownership，不需要Advisor科学指导或Human危险设备授权。

## 7. Executer handoff

Terminal seal durable后，Executer只向`.agent-work/EXECUTION_RESULT.md` append exactly once，至少绑定：

- contract/reference/PLAN SHA与programmatic dispatch HEAD；
- evidence root identity；
- 三个 historical archive path/bytes/SHA与read counts；
- 三层 directory lstat、direct-entry manifests及exact counters；
- 三个resolved artifact absolute paths和`content_identity=not_observed_by_this_package`；
- index/index-seal/terminal/terminal-seal path、bytes、SHA、mode；
- artifact content zero counters、所有hard locks、retry/fallback=`0/0`；
- retained state `RETAINED_UNVALIDATED_UNCONSUMED`；
- decision request：Planner仅验收path-owner index，不得将其解释为B2 manifest pass、R3 content validation、eligibility或release authority。

Append后立即停止，不修改PLAN/FULL/archive/GUIDE，不提交。Planner将独立只读验收；仅在Planner接受且Orchestrator更新FULL后，才能另行设计corrected B2 manifest seal package。

## 维护性判断

本包把stale path selection收敛为一次性、无artifact content access的外置index owner；不修改production、validator或科学合同，不引入平行eligibility owner。复杂度局限于三层exact directory证据和durable JSON封装，无需架构重构。
