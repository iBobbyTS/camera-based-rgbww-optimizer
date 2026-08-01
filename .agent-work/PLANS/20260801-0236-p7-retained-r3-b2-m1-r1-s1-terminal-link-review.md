# REF-P7-25-R2-B2-M1-R1-S1 terminal-link failure review

**Reviewed reference task:** `REF-P7-25-R2-B2-M1-R1-S1`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S1-FRESH-REAL-INPUT-STRICT-RETAINED-V1`

**Planner decision:** `REJECTED_EXECUTION_ASSERTION_SELECTOR_NOT_CONTRACTUAL`

**Planner review date:** `2026-08-01`

## Reviewed immutable Git/ER scope

- Activation: `8e5eeb134a18fc8c90627304fcff40e608dd897c`, direct parent
  `cb59091d67683ae0b31f3790bf8e110f610791ef`, exact subject
  `chore(plan): activate strict retained real input successor`.
- Evidence commit: `5d4e903b0d747be169d68032066b023d77f3a8f9`, direct parent the activation,
  exact subject `chore(evidence): record strict retained terminal link stop`, changed path exact
  `.agent-work/EXECUTION_RESULT.md`.
- Committed ER identity: blob `4ebbaef274da8ed2f90ae071f55e92cc2e178000`, bytes `1243874`, SHA-256
  `64274bd4a8c1f493914d18320488d9d1ff87b070d0ececa22465ca13688ca5dd`.
- This review used committed repository evidence only. It did not probe either external root, rerun the controller,
  read retained-R3 bytes, invoke tests or CodeGraph, or call validator/release/device owners.

## Independently checked result boundary

The committed handoff is one strict JSON block under the expected heading/schema and preserves the complete partial
ledger. The two root identities are present: C1 root device/inode/mode
`16777240/2188341/0700` and retained root `16777240/2069081/0700`. The seven ordered file rows are complete:

| Label | Bytes | SHA-256 |
| --- | ---: | --- |
| `path_owner_index` | 12195 | `b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35` |
| `path_owner_index_seal` | 682 | `867d1ffad5bd29f24dc81b24a58ce66393dd688833d3a4516fe7f45ef50875e9` |
| `terminal_evidence` | 13455 | `c21a691272ca7466271349daa5b10236c9f36dfeb481d592e9c368a87e7a4763` |
| `terminal_evidence_seal` | 772 | `4bfebf4ad40e8c2e65ad2470faaed184f21d39eda73c13e689b09769d280752f` |
| `current_lineage_candidate` | 9819 | `3a2ff5a2af200c55c925b954488c5c5dd31a35a481440d17dfcdd8b68419f2e0` |
| `resolved_formal_plan` | 15137 | `cf7c78b6a6cfda4055d05f5e9bbe9914161213b380dc7736ee09e257dd45eb6b` |
| `setup_lineage_release` | 1567 | `0bacf1878a97fcdc4436259e132e89f6e56611df6d7fb5d5a7da28f62c98ad3e` |

Recorded decoding reached C1 canonical `4/4` and retained strict JSON `3/3`, with retained canonical re-encode,
schema validation and scientific validation all `0`. The exact first failure was
`RuntimeError("c1_terminal_link")`; builder/runtime/controller/source/output remained `0`. Fresh absence checks were
`2/2`, retry/fallback `0/0`, and the sole ER append is the only evidence-commit path. The record declares ER append
last and post-append operations `0`; Git independently proves only the one-path append boundary, while the external
operation ordering remains executor-recorded evidence rather than a fresh Planner probe.

## Root-cause classification

The accepted C1 review archive
`.agent-work/PLANS/20260730-1000-p7-retained-r3-option-b-b2-c1-path-owner-index-review.md` already records an
independent strict/canonical read of the same exact four C1 files and accepted all four schemas/statuses, index-seal
binding, terminal-to-index/index-seal binding, and terminal-seal-to-terminal binding. C1 is therefore not reopened.

The reviewed S1 PLAN required semantic linkage validation but did not freeze a concrete terminal JSON key path or
selector. The original C1 owner contract likewise specifies that terminal binds index/seal identities, without
publishing a stable consumer selector API. The failing outer invocation introduced its own exact field-path
assumption. Its `c1_terminal_link` rejection therefore proves an execution assertion mismatch, not a malformed or
drifted C1 artifact. No production/test/runner owner is defective, because this one-off outer assertion is not
repository-owned behavior.

## Decision, credit, and residual locks

S1 is rejected as a complete real-input manifest run: no builder/runtime/output evidence exists and no eligibility or
release credit is granted. Its read-only input ledger and strict-decode boundary are retained as truthful failure
evidence only. The two fresh targets derived from activation `8e5eeb134a18...` remain immutable and non-consumable;
they may not be probed, reused, repaired, deleted, or treated as absence evidence for a successor.

The smallest next package is one Git/ER-only supersession. It records the corrected failure classification and freezes
the successor rule: a later fresh S2 may rely on the already accepted C1 archive plus exact four-file identity and
canonical decode; it must not invent an unversioned terminal field selector. No old C1/retained file is modified and
no external read is needed for this correction. Validator, release, device and later stages remain locked.

## Exact next branch

- Reference task: `REF-P7-25-R2-B2-M1-R1-S1-C1`.
- Contract: `P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S1-C1-GIT-ER-ONLY-TERMINAL-ASSERTION-SUPERSESSION-V1`.
- Single action: append one canonical Git/ER-only supersession record after Orchestrator activation.
- Planner stop: `B2_M1_R1_S1_C1_GIT_ER_ONLY_SUPERSESSION_WAITING_PLANNER_REVIEW`.

## 维护性判断

The correction removes a non-contractual one-off selector instead of adding a parser, helper, runner, or test-only
framework. Existing C1, P3, M1 and P5 ownership boundaries remain unchanged; no refactor is indicated.
