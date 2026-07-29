# REF-P7-25-R2-B1A-C3E6F4 review / pre-root machine-row parser hard failure

**Planner review date:** 2026-07-29

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F4-CLEANUP-TEST-SUCCESSOR-PREREQUISITE-V1`

**Decision:** `rejected_pre_root_exact_markdown_machine_row_parser`

**Next branch:** `REF-P7-25-R2-B1A-C3E6F5`

## Reviewed scope and method

C3E6F4 retained the accepted acquisition-first, non-self-referential topology: acquire and
seal a fresh evidence root before any budgeted content read; persist five first-acquisition
observed records before comparison; create one exact raw-shutter test-only direct-child
commit; prove the old canonical validator still rejects it; then seal one immutable,
unconsumable exact successor manifest.

Planner reviewed the active PLAN and FULL machine rows, `EXECUTION_RESULT.md` section 65,
shared Git state and the active persistent debug note. The fixed C3E6F4 container is absent,
so section 65 is the terminal evidence owner.

## Terminal evidence

The temporary pre-root controller searched for a physical line beginning with the bare
characters `PLAN_MACHINE_CONTRACT=`. The authoritative PLAN publishes exactly one machine
assignment as Markdown inline code: the physical line begins with a backtick, contains the
complete assignment and strict JSON object, and ends with a backtick. The controller counted
zero markers and raised:

```text
RuntimeError: /Users/ibobby/Projects/WLED-RGBWW/.agent-work/PLAN.md: marker count 0
```

This happened before FULL parsing, controller Git validation, any budgeted-path `lstat`,
fixed-container creation, fresh-root acquisition or content read. The parser was not changed
or rerun.

Verified zero counters include root acquisition, retry, failed-root reuse, all five content
reads, clone, checkout, materialization, pre/post tests, stage, external commit, canonical
validator call, successor-manifest write/rewrite and verifier. Candidate materialization,
production changes, full suite, original retained-R3 reads, real audit, eligibility, consumer
and release were zero. Network, DNS, `.env`, credentials, devices, camera, Ray, strip,
cleanup, capture, public analyzer, FORMAL, firmware and deployment were also zero.

Shared HEAD remains `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`; staged paths remain zero.
Reviewed PLAN and FULL SHA-256 values are
`6205457e4a7885e7006c447f89d048f2b3209869738cb7b5e87d3fccd01be1ba` and
`5b4f15f79d76456058a168b05ee85ef2c6856446cd492dee70bf359c2e52fa9a`.
The execution handoff file SHA-256 is
`71129b43e5dad3f83c07ce1ee9e769d1475105b64769f3048fba5215a14aabeb`.

## Finding and decision

C3E6F4 is rejected solely as a pre-root exact Markdown machine-row parser failure. It
receives no FULL/Git/root/acquisition/materialization/test/commit/manifest/validator/R3/
eligibility/release/device credit. Its absent container must not be created or reused.

No scientific contract, acquisition-order rule, provenance topology, test scope or safety
lock was contradicted. The one-path child plus immutable/unconsumable successor manifest
topology remains accepted; a later separately reviewed package remains the only place that
may bind that successor into the production canonical validator.

## Exact next branch

C3E6F5 changes one controller predicate only. PLAN machine extraction must accept exactly one
physical line matching this complete encoding:

```text
`PLAN_MACHINE_CONTRACT={...complete strict JSON object...}`
```

The parser must require the opening backtick as the first character, the exact
`PLAN_MACHINE_CONTRACT=` marker immediately after it, one complete JSON object, and the
closing backtick as the final character. It must reject zero or multiple rows, leading or
trailing characters, an unwrapped assignment, partial/truncated JSON, multiple concatenated
objects, duplicate keys and non-finite numbers. It must not alter PLAN serialization or use a
permissive substring/startswith parser.

After extraction, every C3E6F4 rule remains byte-for-byte semantic policy: FULL exact subset,
Git gates, fresh-root-first ordering, five observed-before-compare records, one-path child,
old-validator expected rejection, immutable unconsumable successor manifest, and all zero
operation locks. C3E6F4 may not be retried or read as an execution input.

No Advisor or Human authorization is required.

## Residual risks

- The test-only child and successor manifest still do not exist.
- The acquisition-first protocol and tests have not yet executed.
- Full clean-room discovery remains unpassed.
- The production validator has not yet been extended to the exact successor.
- Original retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`; rollback remains
  `32b9e670ff3bbea0cd1505528c2ca87c2935446c`.

**Planner stop:** archive complete. Activate only C3E6F5 after Orchestrator synchronizes its
required FULL machine state.
