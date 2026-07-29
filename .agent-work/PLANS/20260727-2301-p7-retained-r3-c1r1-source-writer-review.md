# REF-P7-25-R2-C1R1 source persistence writer failure review

**Planner decision：** `REJECTED_SOURCE_PERSISTENCE_WRITER_FAILURE`

**Review time：** 2026-07-27 23:01 MDT

**Reviewed reference task：** `REF-P7-25-R2-C1R1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-RELEASE-AUDIT-ADAPTER-C1R1`

**Exact next branch：** `REF-P7-25-R2-C1R2`

## 1. Frozen review inputs

```text
HEAD =
  32b9e670ff3bbea0cd1505528c2ca87c2935446c
parent =
  cc6dbd356dec20eca1437b6c282358c3f2a5e5c7
tree =
  494b24c70b8cd5c3a4e06f82de3511b3d63dd0a9
subject =
  test(p7): bind post-eq checkpoint drift injection

reviewed PLAN SHA-256 =
  fb5c670e9a8c6f903ed09420d1c4e01e473bfeda60b9ad4a5b6a4b506290e109
reviewed FULL_PLAN_REFERENCE SHA-256 =
  bc686dec274bb724c9525b5da95ad4048c8d74058204863c70051a1ebdd16296
reviewed EXECUTION_RESULT SHA-256 =
  36b2fefb16bcf8c672f936a079f7169646519eecd2c8ab75a0a76fb4a7358eae
predecessor review archive SHA-256 =
  cc7a5dbd8ed2741c9fd9b628c79ee2cc05158760e2d8c6b8b2f735b19f27d220
```

Planner independently checked the current files, Git identity, empty exact child root and no staged or
production-scope worktree drift. `FULL_PLAN_REFERENCE.md`, `EXECUTION_RESULT.md`, GUIDE, production,
config, tests, docs, skills and wrappers were not edited during this review.

## 2. Reviewed execution and evidence quality

The fresh two-level evidence owner was acquired exactly as planned：

```text
INTERMEDIATE_PARENT =
  /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-lineage-release-r3-r2-c1r1-offline
device/inode/mode = 16777241 / 2069110 / 0700
attempt/success = 1/1

EVIDENCE_ROOT =
  /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-lineage-release-r3-r2-c1r1-offline/20260727T2251
device/inode/mode = 16777241 / 2069111 / 0700
attempt/success = 1/1
root entries after failure = []
```

The only source-build invocation then failed before source bytes, SHA event or persistence because the
outer exclusive writer referenced `os` without importing it：

```text
failure owner = outer source persistence writer
failure type/message = NameError / name 'os' is not defined
source build/SHA/persist/identity/compile/exec = 1/0/0/0/0/0
internal/public/fake/final/strict/terminal = 0/0/0/0/0/0
alternate source/second controller/retry/repair = 0/0/0/0
```

This is a valid fail-closed result, not a successful retained-release audit. There is no canonical controller
source, identity, progressive JSON or terminal seal to accept. The directory identities and empty exact
root independently corroborate that no post-build stage ran.

## 3. Boundary and immutability findings

The retained R3 release family remains unchanged, unvalidated and unconsumed. No qualification, generation,
copy, repair or consumption occurred. Repository source/config/test/docs/skill/wrapper edits, tests,
compileall, CodeGraph, Git operations, device/network/DNS/`.env`, camera/Ray/strip/cleanup/capture,
CR3/NPY/nonzero output, public analyzer, formal and TD-C are all zero. Residual owned process count is zero.

The acquired C1R1 parent/root are historical failed-run evidence. They must not be deleted, reused, repaired,
continued or credited by the next package.

## 4. Planner findings

### REV-R3-C1R1-001 — source persistence dependency was outside the validated owner

The controller body was correctly limited to one build, but the outer persistence writer that must save that
body depended on an undeclared `os` binding. The plan validated root ownership before first persistence yet
did not freeze the writer's own standard-library bindings before consuming those roots.

### REV-R3-C1R1-002 — an unpersisted controller smoke check remains prohibited

The correction must not execute, compile or inspect a freshly built controller before persistence. That would
restore a parallel lifecycle and consume or vary the single controller owner. The dependency check must be
owned by the outer launcher and completed before any fresh parent/root acquisition, without constructing
controller source.

## 5. Decision and exact next branch

```text
REF-P7-25-R2-C1R1 = REJECTED_SOURCE_PERSISTENCE_WRITER_FAILURE
two-level acquisition result = accepted factual evidence only
retained release family = unchanged / unvalidated / unconsumed
release retry = prohibited
next = REF-P7-25-R2-C1R2
```

C1R2 may use one entirely new intermediate parent and exact child root. Before either acquisition, the outer
launcher must freeze the exact standard-library imports required by its exclusive writer and perform one
explicit dependency-owner preflight that does not build controller source, write a file or consume any
controller lifecycle counter. It may then run the same one-source persisted schema-aware retained audit.

## 6. Acceptance criteria for C1R2

Planner may accept C1R2 only if：

1. the old C1R1 directories remain immutable and the new parent/root names were absent and acquired once;
2. writer dependency preflight passes once before acquisition and controller source build remains zero at
   that point;
3. one controller source alone is built, hashed, persisted, identified, compiled and executed;
4. retained manifest and exact three-artifact family remain byte-identical;
5. schema-aware internal audit, public validator, fake consumer, final/strict audit and terminal seal each
   pass once with empty mismatch arrays;
6. qualification/generation/retry/repair/copy/consumption, repository edits, device/network and formal routes
   remain zero;
7. all evidence is progressively persisted and independently replayable.

## 7. Residual risk and maintainability

Residual risk is confined to the external one-shot evidence controller and its outer writer lifecycle.
Production lineage classification, release generation and public validation owners were not entered.
Freezing one dependency owner and retaining the single persisted controller path adds no production
abstraction or parallel serializer; no architecture refactor is needed.
