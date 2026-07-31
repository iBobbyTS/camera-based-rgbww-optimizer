# REF-P7-25-R2-B2-P3-C1 provenance I/O correction review

**Review date:** `2026-07-30`

**Reviewed reference task:** `REF-P7-25-R2-B2-P3-C1`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-PROVENANCE-IO-BOUNDARY-CORRECTION-V1`

**Planner decision:**
`REJECTED_ONLY_FULL_SUITE_TERMINAL_EVIDENCE_UNAVAILABLE_P3_C2_REQUIRED`

**Reviewed PLAN identity:** bytes `11051`, SHA-256
`1b513e2ca13da8260f5e8dfc96afd584ef3c5b7851903146ab5851be54293391`.

**Reviewed stop:** `B2_P3_C1_REPAIR_WAITING_PLANNER_REVIEW`.

## 1. Reviewed scope and method

本次独立审核覆盖 rejected P3 candidate `77b9e85c1064cb6ba8d3a8fe0932b7eae488c945`
到 correction commit `1f88cf42d95c00c7db5692e78ed1d663732d5701` 的 exact-two-path repair
delta、dedicated behavioral tests、Git topology、Executer handoff 和 active PLAN acceptance contract。

该 delta 位于高风险 filesystem/provenance trust boundary，因此按 Large depth 审核。触发并完成的 lens
包括 intent fidelity、filesystem/path trust、failure atomicity、descriptor cleanup、validation integrity、
scope/ownership 和 maintainability。未触发 persistence schema、network、device、UI、concurrency、dependency 或
deployment lens。

Planner 先读取当前 Git/PLAN/ER/FULL context，用 CodeGraph 定位当前 helper，再直接审查 raw repair delta、
dedicated tests 和提交对象。没有重跑 unittest、compileall 或 CodeGraph sync，没有读取
`/Volumes/4T/temp/rgbww-optimizer` 下的 C1、retained-R3、release 或旧 run evidence，也没有访问 network、
`.env`、设备、camera、Ray、strip、cleanup、formal 或 public analyzer。

## 2. Independently reconstructed repository evidence

Activation topology exact：

- activation `a736e95b968ffef813024a67c0cbcfbd67e971e4`；
- direct parent `96b1feb7ebf2b9f8f65c0aafce24ccaa7f26e39c`；
- subject `chore(plan): activate retained r3 provenance io correction`；
- exact paths为 FULL、PLAN和前次 P3 rejection archive。

Implementation topology exact：

- child `1f88cf42d95c00c7db5692e78ed1d663732d5701`；
- direct parent为上述 activation；
- subject `fix(p7): harden retained r3 provenance io boundary`；
- exact changed paths仅
  `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py`和
  `tests/test_p7_retained_r3_provenance_io.py`；
- canonical binary patch SHA-256
  `df29a921b774010db020fdebfc12809feb2c92c293c247b14733a6e39e8595e1`。

Post identities independently match the handoff：

| Path | Bytes | Blob OID | SHA-256 |
| --- | ---: | --- | --- |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py` | `18853` | `492f31f5f6999e28a1f0eb60240780e2c4826f4f` | `f603721fb8b90510e2a09b199701c3f3358574d1247b5883ebdccc6f585b0a48` |
| `tests/test_p7_retained_r3_provenance_io.py` | `28525` | `a796e1ac336d58a0120dd6b99a3842c5c7b03a6b` | `59a6d87164abf6abc89c50ab7d899f94126fc949512d38b34967cae8f4e6d4e9` |

Evidence handoff commit `c0e20d1afe9e363f646fc5723be721d3b907deeb` is a direct child of the
implementation commit and changes only `.agent-work/EXECUTION_RESULT.md`. Review-start worktree/stage were clean。

## 3. Finding closure review

### REV-P3-001 — closed in code and behavioral coverage

`_required_open_flag` rejects absent/default-`None`、zero、non-exact-`int` capability with stable
`required_open_flag_unavailable:<name>` codes. Exact read uses `O_RDONLY|O_NOFOLLOW`；exclusive
target open uses `O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW` mode `0600`；root fsync open uses
`O_RDONLY|O_DIRECTORY|O_NOFOLLOW`。Persist resolves both required capabilities before target creation，
so no follow-capable fallback exists。Tests verify exact flags and pre-open rejection with zero calls；the missing
attribute path shares the directly visible `getattr(..., None)` branch。

### REV-P3-002 — closed in code and behavioral coverage

Root-bound reads first revalidate exact root identity, then `_require_direct_child` requires an absolute string spelling,
rejects empty/dot/parent/doubled/backslash segments and requires lexical parent equality with `root.path` before any
target lstat/open。Persist reload calls the same root-bound read path；only a proven path receives `FileIdentity.root`。
Tests cover legal direct child plus outside、nested、dot、parent、double-separator、backslash and relative forms，and
show only the root lstat occurs before rejection。

### REV-P3-003 — closed in the dedicated negative matrix

Dedicated tests increase from 18 to 24 test methods and materially cover exact flags/capability failure、direct-child
linkage、failed-read close-once and primary/close visibility、target open/mode/device/inode failures、root
open/fsync/close failures、reload lstat/open/read/decode failures、physical target preservation and no second write。
Existing partial I/O/EINTR、canonical JSON、Git grammar、immutability and owner guards remain present。No assertion-only
or external-evidence substitute was introduced。

No new Must Fix or Should Fix root-cause finding was found in the repair delta or invalidated impact cone。

## 4. Validation evidence quality

The handoff records these one-shot passing gates, and current source/topology does not contradict them：

- targeted `24/24`；
- focused `71/71`；
- compileall exit `0`；
- `codegraph sync` exit `0`, `Already up to date`；
- exact-two-path pre/post scope and diff checks；
- postcommit targeted `24/24`, final `OK`；
- retry/fallback `0/0`。

The full command was invoked exactly once, but the only retained output fragment ends in progress dots. The tool cell
reached a structured completed state and no failure text is retained, yet neither the unittest terminal `Ran ...`/`OK`
summary nor an explicit child exit code is available. Active PLAN section 4 and section 5 require that complete same-session
terminal evidence. Absence of visible failure is not positive proof of a passing full suite，so this gate cannot be accepted。

The gap is validation observability only；it does not reopen REV-P3-001/002/003 or justify any source/test edit、targeted/
focused rerun、compileall rerun、CodeGraph rerun、second implementation commit or patch regeneration。

## 5. Decision and exact next branch

Decision：
`REJECTED_ONLY_FULL_SUITE_TERMINAL_EVIDENCE_UNAVAILABLE_P3_C2_REQUIRED`。

Exact next branch：`REF-P7-25-R2-B2-P3-C2`，contract
`P7-TD-B-RETAINED-R3-PROVENANCE-IO-OBSERVABLE-FULL-VALIDATION-V1`。

P3-C2 must preserve implementation commit/file/patch identities and run exactly one low-output full-suite invocation whose
same shell/session exposes both the real child exit and terminal `Ran 741 tests ...` plus `OK` summary. It may not edit、
stage or commit；it may not rerun any accepted gate. A real exit `0` and exact terminal summary permit only a new Planner
acceptance decision and later Orchestrator FULL update。

## 6. Residual locks and risks

- A fresh quiet full suite may reveal a real regression；any nonzero、missing summary or count mismatch must fail closed
  without retry or repair。
- retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`；this review does not validate、qualify or consume it。
- external C1/retained/release evidence、real B2/B3/B4、canonical validator、eligibility、release operations、network、
  `.env`、device、camera、Ray、strip、cleanup、FORMAL、public analyzer、TD-C、sentinel、P8、firmware and deployment
  remain hard locked at zero。
- This is an engineering validation branch；Advisor scientific guidance and Human device authorization are not required。

**Exact stop:** `B2_P3_C1_REJECTED_WAITING_ORCHESTRATOR_P3_C2_ACTIVATION`。

## 维护性判断

Repair remains contained in one provenance I/O helper and its dedicated test owner；the next package adds no code or
abstraction and only closes terminal observability。No follow-up refactor is indicated。
