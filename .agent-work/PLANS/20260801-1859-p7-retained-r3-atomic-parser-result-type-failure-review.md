# P7 retained-R3 Option B：atomic parser-result type failure review

**Planner decision：** `ACCEPTED_FAIL_CLOSED_LIFECYCLE_ONLY_REJECTED_REAL_EXECUTION_PARSER_RESULT_ADAPTER_AND_SPEC_CONTRACT_INCOMPLETE`

**Reviewed activation：** `8746f031a43281025cd1aa2a4adb8720355b44c9`（短 SHA `8746f03`）

**Reviewed evidence：** `253eaa4`，full SHA `253eaa4a23db1e7c9862606b8212e41c71371b22`；该提交只改 `.agent-work/EXECUTION_RESULT.md`。

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-FRESH-REAL-SELF-CHECK-ATOMIC-SOURCE-TYPE-RAW-BYTES-CORRECTIVE-V1`

## 1. Evidence identity 与质量

- Activation ER blob：bytes `1609346`，SHA-256 `613ee77aa70a9fa604843b73eed8bf901be813d5d7103f7e8cd60e5253b64f3c`。
- Evidence ER blob：bytes `1613221`，SHA-256 `bdf94f8ab1b1f8fc45acd7d96cc09642cc10474bcb0c9fcb2a978cf0126cc97e`。
- Evidence严格以activation blob为prefix；唯一true-physical-EOF suffix bytes `3875`，SHA-256 `de8bc03fa66c84ee4855dbb6b8f9a14d46f440785f534c6506eebe94b743cc6b`。
- Fresh source `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-atomic-controller-8746f03-20260802T005100Z-11861.py` 为exclusive-created、non-symlink regular file、mode `0600`、bytes `13916`、SHA-256 `c5f3d0dd1e9a0521e0ed84fd7723137e95fb0bfc351256494b2dc4dbf0012f59`。
- Fresh root `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-fresh-real-self-check-atomic-source-type-8746f03-20260802T005100Z-11861` 为exclusive-created、non-symlink directory、mode `0700`，并在任何PLAN/FULL raw read前完成验证。
- 三个terminal artifacts均为regular、non-symlink、mode `0600`且strict JSON：`00-controller-failure.json` bytes `2078` / SHA-256 `ba98ee776f516deb6e5e836a909a97b3bca7912c3ec2c4265db0f3a1aed39148`；`01-terminal-summary.json` bytes `1118` / SHA-256 `024aed75867943ddf6194ed3cfb0250dd5a33e5617587e120e89c7304bb5f0bc`；`02-terminal-seal.json` bytes `1454` / SHA-256 `882710929ca0ee03ec591d83930ec7a986789393929f93db64b4b1dd94c1ea7d`。

## 2. Planner findings

### 接受的部分

Controller exact one次建立并验证fresh source/root，然后各读取activation PLAN/FULL raw Git-object exact一次。传入PLAN accepted parser的是同一个raw `bytes`对象；decode/re-encode/read_text/worktree reads均为0。Failure artifacts与ER一致记录：accepted PLAN parser `1`、accepted FULL parser `0`、physical input activity `0`、owner `0`、retry `0`、fallback `0`。所有release、validator、eligibility、network、device、camera、Ray、strip、cleanup、formal、public analyzer与production/test/docs/skill/GUIDE writes均为0。因此本轮fail-closed lifecycle及source/root+raw-bytes原子门证据可信。

### 拒绝的部分

真实failure为 `ACCEPTED_PARSER_RESULT_TYPE_UNSUPPORTED`：controller把accepted parser返回值当作mapping或不受支持的wrapper处理，在PLAN parser结果unwrap时抛出 `TypeError`。因此FULL parser、topology、required-FULL-subset、14 physical inputs、typed owner spec与owner call均未发生；本轮不得获得real self-check execution、production-owner、lineage、eligibility或release-consumable credit。

### 独立源码/测试核对

当前repo accepted parser源码明确返回冻结dataclass `ParsedMachineContract`；公开访问方式是 `result.value` 与 `result.evidence`。其中 `.value` 是deep-frozen `MappingProxyType`/tuple树，`.evidence` 是 `MachineContractEvidence`，可用 `.to_mapping()`序列化。Dedicated tests也直接断言 `.value`、`.evidence`与嵌套immutability。下一包不得猜测、duck-type或维护自制mapping adapter，必须按这个公开返回类型读取。

源码identity：

- `src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py` bytes `9414`，SHA-256 `a02a30c026fba548c81c04a277e2f235385ddb8a459c4ff2f73c91ee87c3737e`，blob `ce2200181bd2a493cfaab621daa17b89a13bdf1f`。
- `tests/test_agent_work_machine_contract.py` bytes `14638`，SHA-256 `8f9ba840cc0846cdb4c82edf9ebf8540a748c86a6331227a7a0e2d8e27e328a0`，blob `be1d5e955edf38566f274bedcac02b1a4fa93e44`。

### RealManifestSelfCheckSpec completeness audit

当前PLAN没有冻结 `RealManifestSelfCheckSpec` 的完整typed construction：缺少完整 `artifacts` typed identities、`activation` 的full patch identity、`baseline`与seam chain全部typed值、`c1_inputs`/`retained_inputs` typed field映射，以及owner所需 `git_file_bytes` exact `(commit, repo_path, bytes)`集合。只有14 physical path/bytes/SHA和activation package metadata不足以无猜测构造spec。因此下一包必须只完成纯离线spec construction contract，不得直接调用owner。

Owner源码公开spec字段顺序为：`reference_task_id, contract_id, repo_root, artifacts, activation, baseline, c1_inputs, retained_inputs, git_file_bytes`。所有nested value必须使用repo公开dataclasses `RealManifestCommitIdentity`、`RealManifestBaselineIdentity`、`RealManifestGitPathIdentity`、`RealManifestInputIdentity`、`RealManifestGitFileBytes`及provenance IO的`FileIdentity`/`DirectoryIdentity`，不得用list/dict替代typed objects。

## 3. Decision 与下一唯一分支

接受本轮terminal failure lifecycle，拒绝real execution。下一唯一分支为pure-offline `SPEC_CONTRACT_COMPLETION`：只读核对parser/self-check/domain-template源码及dedicated tests，以冻结14 inputs为事实源生成一个strict JSON spec-construction contract与matching seal，明确parser公开unwrap方式，并完整列出每个spec/nested field的exact value、type、顺序、provenance source和future activation-bound字段规则。该包不得读取后直接调用owner；不得进入canonical validator、lineage、eligibility或release。

只有Planner验收该contract完整、无猜测且可机械构造typed spec后，Orchestrator才能另开fresh real self-check owner package。

## 4. Residual risks 与 locks

- 当前retained R3继续 `RETAINED_UNVALIDATED_UNCONSUMED`。
- 本轮证据只证明subordinate wrapper failure；production owner、lineage、eligibility与release consumable均为false。
- FORMAL-R6、strip、TD-C、sentinel与P8继续锁定。
- 无科学分支；不需要Advisor。无设备操作；不需要Human授权。

维护性判断：下一包只补齐既有typed owner入口的不可变构造合同，不改production/test代码、不新增adapter或并行owner；可降低重复wrapper误判与维护复杂度。
