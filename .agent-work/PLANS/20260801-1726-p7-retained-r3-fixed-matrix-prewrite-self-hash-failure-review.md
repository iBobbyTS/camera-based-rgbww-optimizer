# P7 retained-R3 Option B：fixed-matrix prewrite activation self-hash failure review

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-C1-C1-C1-C1-C1-C1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-FIXED-MATRIX-READ-ONLY-PHYSICAL-EOF-SUPERSESSION-V1`

**Decision：** `REJECTED_PREWRITE_ACTIVATION_SELF_HASH_MEMBERSHIP_ASSERTION_ZERO_WRITE_NO_EVIDENCE_CHILD`。

## 1. Reviewed scope、topology 与 immutable identities

Planner 独立读取 project skill、active PLAN/FULL machine state、activation Git metadata、固定 report/seal 与 Executer 的 exact prewritten process/traceback；未运行 controller、selector、ledger、validator、tests、CodeGraph、network 或设备路径，未读取 terminal/source/physical inputs，未修改 ER、FULL、代码、测试、skill、docs 或 GUIDE。

Activation `0309b66d2a7731325e495319915c548788f124f4` 是 `94f161f56c96f4fdff7df8ae3a25072b62cc691c` 的 direct child，subject exact `chore(plan): freeze fixed matrix at EOF`，changed paths exact 且有序为：

1. `.agent-work/FULL_PLAN_REFERENCE.md`
2. `.agent-work/PLAN.md`
3. `.agent-work/PLANS/20260801-1711-p7-retained-r3-exact-offset-eof-acceptance-review.md`

Activation committed identities：PLAN `15768` bytes / SHA-256 `479985668d7a23a555a39a7e9a7458247164cb35e30dbca45940c3586ccc237e`；FULL `469297` bytes / SHA-256 `3d8b38e0c4f3008c69928d3b9fa30c16920bf70e758d5b0510bb2b579229f4a0`；ER `1561559` bytes / SHA-256 `6468ae28195ad5ae37bdb7cc4e821905b78467d2bca34b5bd0d8d9d061166b44`。Review 开始时 HEAD exact activation、无 evidence child、worktree clean；worktree ER 与 activation ER exact 相同。

## 2. Exact first failure 与 effect accounting

Executer 启动唯一预写 local process。Accepted PLAN/FULL parser各成功调用一次，随后 Git metadata gate `actual_parent == PARENT` 通过。首个失败是 `<stdin>:110`：

```python
assert ACTIVATION.encode() in plan_raw and PARENT.encode() in plan_raw
```

Exact values：`ACTIVATION == 0309b66d2a7731325e495319915c548788f124f4`，该 bytestring **不在** activation committed PLAN raw bytes；`PARENT == 94f161f56c96f4fdff7df8ae3a25072b62cc691c`，该 bytestring在 PLAN raw bytes。复合断言因此由左半项首先为 `false` 而触发无 message 的 `AssertionError`。当前 activation commit 在该 PLAN 被写入并提交之后才存在，故 PLAN 自含 current activation SHA 是不可满足且非契约性的 self-hash gate；activation topology 的 owner 应是 Git metadata，不是 activation PLAN content membership。

失败发生在 heading/status/`must_include` marker gate之前，也在 fixed report/seal raw read之前。Executer observed counters：唯一预写 process `1`；activation PLAN/FULL Git-object raw reads `1/1`；accepted parser calls `1/1`；activation parent Git metadata read `1`；report/seal reads `0/0`；strict loads `0/0`；matrix freeze/canonicalization `0/0`；worktree ER read/tail extraction/apply_patch append `0/0/0`；retry/fallback `0/0`。ER unchanged、artifact writes `0`、controller/selector/ledger/device effects全 `0`，且无 evidence child。

## 3. Independent fixed report/seal audit

Planner audit 对固定 report/seal各 raw-read并 strict-load一次。Report exact `41685` bytes / SHA-256 `923f32afae0f375469d03a6b6a18a71261c19e7bcfefcd0bb041bdfde11b849a`；seal exact `166` bytes / SHA-256 `068ee79657f4765928b80909514d37b431d779fc2a6ccd914c127e1453c08c49`，seal exact value为 `{"bytes":41685,"schema":"sha256_seal_v1","sha256":"923f32afae0f375469d03a6b6a18a71261c19e7bcfefcd0bb041bdfde11b849a","target":"01-owner-expectation-attribution.json"}`。

真实 report schema为 `p7_td_b_corrected_ledger_attribution_report_v1`；top-level `$.matrix` 是 `builtins.list` / `18` rows。每 row exact keys为 `argv, detail, expected_selection, git_exit_code, git_stderr_sha256, index, match, owner_returned_kind, plan_expected_kind, role`；`match` 是 boolean，不存在 string status owner。Ordered indices为 `1..18`，match `15`，mismatch indices exact `[7,15,18]`，first mismatch `7`。Canonical JSON exact `24981` bytes / SHA-256 `4e051f1d8a3e5849d7d0a856f2517371e7cd0d49f6efe192984518ade94e95b5`。

Report **无** top-level `$.ledger_rows`。Path binding只由 `$.ledger_binding_proof.frozen_path == "$.ledger_rows"` 验证；proof真实字段为 `owner="PLAN_MACHINE_ROOT"`、`exact_type="builtins.tuple"`、`cardinality=18`、`binding_identity_same_object=true`、ordered indices `1..18`。Selector calls、ledger Git attempts/processes为 `18/18/18`；retry/fallback为 `0/0`；zero_locks全部为 `0`；production owner、lineage、eligibility、release consumable均为 `false`；Retained R3为 `RETAINED_UNVALIDATED_UNCONSUMED`。因此 report、matrix canonical identity、required report facts与path binding本身无 mismatch；本轮失败完全发生在非契约性的 pre-report self-hash assertion。

## 4. Decision、credit boundary 与 exact next branch

本轮拒绝 execution，仅接受“零写 prewrite self-hash failure”的诊断事实；不接受 synthetic engineering attribution facts，且不把 Planner 的只读 report audit冒充 Executer execution credit。Original execution contract继续 rejected；production owner、lineage、manifest truth、eligibility与release无信用；Retained R3保持 `RETAINED_UNVALIDATED_UNCONSUMED`。

唯一 successor 是同 reference chain下一 `C1`：删除 current activation SHA 必须存在于 activation PLAN raw bytes 的 membership gate；activation/parent/subject/ordered paths/archive均由 Git metadata exact owner验证。继续 same-process accepted parser、固定 report/seal各读一次、仅冻结 top-level `$.matrix`、按 boolean `match` 统计并核对 canonical bytes/hash、只验证 ledger proof 的 frozen path而不读取不存在的 `$.ledger_rows`，最后以完整 current `2058`-byte tail为唯一 context在 true EOF append。每个 assert必须带 field/path、expected、actual/type 的 deterministic message，以便首个失败可精确归因。

**Exact next Planner stop：** `B3_C3_C4_R5_R1_C1_R2_R1_C2_S1_C1_R1_D1_D2_C1_R2_C1_S1_C1_C1_C1_C1_C1_C1_C1_C1_C1_FIXED_MATRIX_PREWRITE_SELF_HASH_CORRECTIVE_WAITING_PLANNER_REVIEW`。

维护性判断：本轮不改代码；corrective只移除不可满足的 activation self-hash gate并冻结真实 evidence schema与诊断格式，不新增 repository abstraction 或后续清理债务。
