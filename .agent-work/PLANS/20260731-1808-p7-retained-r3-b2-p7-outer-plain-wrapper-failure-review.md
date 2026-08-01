# REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1 Planner review archive

**Reviewed contract:** `P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-C1-OUTER-PLAIN-PHYSICAL-NUL-CORRECTION-V1`

**Reviewed stop:** `B2_P7_C1_C1_C1_C1_V1_C1_OUTER_PLAIN_PHYSICAL_NUL_CORRECTION_WAITING_PLANNER_REVIEW`

**Planner decision:** `REJECTED_PRE_GATE_LOGICAL_EXIT_PERSISTENCE_WRAPPER_FAILURE_CANDIDATE_IMMUTABLE_NON_CONSUMABLE`

## 1. Reviewed scope and frozen inputs

The package activated at commit
`44fb7295f0f71030833476225350da01ce3c71d3`, direct parent
`11eba96e2c971b2c6da1e0a7e3bdf9dd574d20d0`, subject
`chore(plan): activate p7 outer plain nul correction`, with the exact three
activation paths required by the reviewed PLAN. Activation identities, archive
identity, candidate topology, FULL machine state, source/test baselines and
clean-porcelain requirement all passed before edits.

The authorized implementation scope was exactly:

- `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py`
- `tests/test_p7_retained_r3_controller_domain_template.py`

The package was forbidden from changing the template, replacement statement,
serializer, semantic matrix, owner APIs/dataclasses, adding helpers/fallbacks,
or touching a third path. External controller/source/root/process work,
synthetic integration, retained R3/candidate payload reads, validator,
eligibility, every release operation, network, DNS, environment, credentials,
device, camera, Ray, strip, cleanup, capture, FORMAL, public analyzer, TD-C,
sentinel, P8, firmware and deployment were all locked at zero.

## 2. Implementation and evidence reviewed

The Executer formed the exact two-path correction. The module changed the
existing outer `_plain` guard from the literal four-character backslash-`x00`
test to a physical-NUL semantic test. Existing physical LF/CR and stable
field-specific error behavior stayed intact. Existing public test07 gained a
physical-NUL negative specimen for `source_path` and a literal backslash-`x00`
positive specimen that proves exact runtime-request preservation.

The Orchestrator retained this uncommitted result as immutable candidate:

- candidate commit: `864f08cc5436519a37e41d553e49ebde4a3c8bb2`
- direct parent: `44fb7295f0f71030833476225350da01ce3c71d3`
- subject: `chore(p7): retain rejected outer plain nul candidate`
- exact changed paths: the two source/test paths listed above
- canonical binary diff SHA-256:
  `b03b1a049a407e2049f049b6f2514497e6d5bb82675f14dc750f00cc09ce6bd4`
- source blob/bytes/SHA-256:
  `5529ec27b3893c20995e9a8cb3a9fa5c0a87a3b5` / `19753` /
  `10969de79f5afece8018f094823efcf6f60237670ed1eeb54135f451ef0425c2`
- test blob/bytes/SHA-256:
  `d0f733426673aa9a57fcb1195ecea014f8c48062` / `27386` /
  `4c3b93d4a2f5967b91cb48a2dea1c0a0f8994fb687f6109830d24602bb93083e`

The sole Python pre-gate body passed every semantic assertion and emitted its
canonical pass payload. It proved strict UTF-8; module/test AST parse and
compile; exact eleven methods; outer `_plain` physical NUL/LF/CR AST constants
`1/1/1`; module physical-NUL bytes `0`; public physical-NUL rejection with the
stable field code; literal backslash-`x00` acceptance and preservation;
canonical template bytes/SHA-256 `11999` /
`0369231f11bc968ebc343bac57acab236d75faf5d5d6e2b9c3d82918df19a467`;
template literal escape counts `8/3`; replacement bytes/SHA-256 `1907` /
`502c303e6257d8f59a4d5bbd39b0339371e210a8c10c9e8fa3fd0d2530160807`;
and exact bounded source/test reconstruction. `git diff --check` passed.

After the Python body returned logical exit `0`, the same zsh wrapper attempted
`status=$?`. `status` is a read-only special zsh parameter. The wrapper failed
before printing or persisting `PRE_GATE_LOGICAL_EXIT`, so the reviewed PLAN's
independent logical-exit evidence contract was not met. The wrapper was not
corrected or rerun. Retry/fallback remained exact `0/0`.

The authoritative handoff is the final
`REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1` section of
`.agent-work/EXECUTION_RESULT.md` at evidence commit
`7d8a12178372ee34428665273086497da98f9099`; complete ER bytes/SHA-256 at that
commit are `1129308` /
`87885ec12320ad0dae7835766d8fddaf71d19de6f7514de3da3b6b52b445a68d`.

## 3. Validation quality and decision

Validation quality is strong for the candidate's local semantics but
insufficient for package acceptance. The Python pre-gate body passed, yet the
owning wrapper failed to preserve the logical exit. Therefore targeted11,
focused93, compileall, unified full778, implementation commit and postcommit
targeted were exact `0`. Tests cannot be inferred from the green pre-gate body.

The result is rejected as an execution-packaging failure. It does not identify
a new source/test defect, does not invalidate the exact semantic correction,
and does not justify another code edit. Candidate `864f08c...` is preserved
unchanged but remains non-consumable until a fresh validation-only package
passes. Retained R3 remains unvalidated/unconsumed and no integration or later
stage is unlocked.

## 4. Exact successor branch

The sole next branch is a validation-only closure over immutable candidate
`864f08c...`:

1. code/test writes and implementation commits remain exact `0`;
2. run one fresh semantic pre-gate only;
3. the zsh wrapper captures `$?` only in ordinary non-special variable
   `pregate_exit`, prints `PRE_GATE_LOGICAL_EXIT=<value>`, immediately verifies
   exact `0`, and records that exact line in the sole ER append;
4. `status`, `pipestatus`, `path`, `PATH`, `argv`, `ARGC`, `commands`,
   `functions`, `options`, `signals`, and `parameters` are prohibited as shell
   assignment targets; no alternative exit-capture variable is permitted;
5. after the gate passes, run fresh targeted `11/11`, focused `93/93`,
   compileall exit `0`, and one unified full `778/778`;
6. CodeGraph sync/query, implementation commit, postcommit test, retry and
   fallback remain `0`;
7. append ER exactly once and stop for independent Planner review.

The successor remains offline and validation-only. External/retained/device
effects stay exact `0`; no Human authorization or Advisor scientific decision
is required.

## 5. Residual risks and locks

The candidate is not consumable merely because the semantic pre-gate body was
green. The successor must prove the full fresh regression sequence without
altering candidate bytes or topology. Any identity drift, special-parameter
assignment, missing/mismatched logical-exit marker, test failure, extra gate,
retry, fallback, write, commit, CodeGraph invocation or external effect must
fail closed and return to Planner.

Maintenance assessment: the candidate remains confined to the single
deterministic template owner and dedicated test; the successor introduces no
code, helper, abstraction or parallel owner.
