# REF-P7-25-R2-C1 / Retained R3 audit pre-persistence parent-root review

**Planner decision:** `REJECTED_PRE_PERSISTENCE_PARENT_ROOT_CONTRACT`

**Planner date:** 2026-07-27

**Reviewed contract:** `P7-TD-B-RETAINED-R3-RELEASE-AUDIT-ADAPTER-C1`

**Reviewed reference task:** `REF-P7-25-R2-C1`

## 1. Frozen review inputs

```text
HEAD =
  32b9e670ff3bbea0cd1505528c2ca87c2935446c
PLAN SHA-256 =
  1c2a9c17a9a26b14f487a205bf4da9517a4abf23e1d04660b7b0ef5872558b1f
FULL_PLAN_REFERENCE SHA-256 =
  1cfd8d2266fe7587244a5d77ce1610069c5d97532494bdd927c97385e3508958
EXECUTION_RESULT SHA-256 =
  95fd2ff851b9369162e4ee34979629a0688d96bdaaa812eb91c244ecc2cb0fc4
```

Reviewed evidence was the execution handoff in
`.agent-work/EXECUTION_RESULT.md` section 159. The planned intermediate parent
and exact child root were independently confirmed absent:

```text
/Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-lineage-release-r3-r2-c1-offline

/Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-lineage-release-r3-r2-c1-offline/20260727T2241
```

No fresh evidence artifact exists for this failed attempt because failure
preceded the first permitted persistence.

## 2. Accepted execution facts

Dynamic Git/PLAN/FULL/ER/archive checks and retained-package preflight passed.
The exact counters are:

```text
controller source build / SHA compute = 1 / 1
intermediate-parent acquisition = undefined and unauthorized
exact-root acquisition attempt / success = 1 / 0
controller source / identity persistence = 0 / 0
compile / exec = 0 / 0
internal / public / fake / final / strict / terminal = 0 / 0 / 0 / 0 / 0 / 0
```

The source value and its SHA computation, and the failed exact-root attempt,
are consumed lifecycle events and must not be reused or retrospectively counted
by a successor package.

The following stayed at absolute zero:

```text
production qualification / release generation / release retry = 0 / 0 / 0
release repair / copy / consumption = 0 / 0 / 0
retained package writes = 0
repo production/test/config/docs/skill/wrapper edits = 0
Git stage/commit/amend/push = 0/0/0/0
device/network/DNS/.env/camera/Ray/strip/cleanup/capture = all 0
formal/public analyzer/TD-C/firmware/deployment = all 0
residual owned process = 0
```

The retained R2 three-artifact family remains unchanged, unvalidated and
unconsumed.

## 3. Blocking finding

### REV-R3-R2-C1-001 — Nested evidence-root acquisition had no parent owner

The active plan required the exact nested `EVIDENCE_ROOT` to be absent and
acquired once, but neither froze nor authorized creation of its missing
intermediate parent. The one exact-root acquisition therefore hard-failed:

```text
FileNotFoundError: [Errno 2] No such file or directory
```

The Executer correctly stopped rather than creating an undeclared parent,
retrying the child root, choosing an alternate root, or executing a second
controller. The failure is a Planner contract defect, not evidence against the
production classifier, release generator, public validator, retained release
or schema-aware adapter design.

Decision:

```text
REF-P7-25-R2-C1 = REJECTED_PRE_PERSISTENCE_PARENT_ROOT_CONTRACT
retained release = RETAINED_UNVALIDATED_UNCONSUMED
REF-P7-25 = BLOCKED_ON_C1R1_OFFLINE_AUDIT_CORRECTION
```

## 4. Corrective branch

The successor must use a new, frozen intermediate parent and a new exact child
root. It must separately prove both absent/non-symlink, acquire the intermediate
parent once with mode `0700`, then acquire the exact child once with mode
`0700`. It must build and hash a new controller source after those acquisitions,
persist source/identity once with mode `0600`, and continue the original
schema-aware retained-release validation.

The failed C1 source value, source SHA event, parent name, exact child name and
root attempt are historical evidence only and cannot be reused, repaired or
credited to the successor.

## 5. Residual risks and locks

- Retained artifacts remain unvalidated and cannot be consumed as authority.
- Existing retained package and every earlier evidence root remain read-only.
- Production qualification, release generation/regeneration/repair/copy and
  release consumption remain prohibited.
- Repository source/config/test/docs/skill/wrapper edits and Git operations
  remain prohibited.
- Device/network/DNS/.env/camera/Ray/strip/cleanup/capture/formal/public
  analyzer/TD-C/firmware/deployment remain prohibited.

## 6. Next branch

```text
next reference task = REF-P7-25-R2-C1R1
next contract =
  P7-TD-B-RETAINED-R3-RELEASE-AUDIT-ADAPTER-C1R1
single action =
  validate the retained exact R3 three-artifact family through one fresh
  two-level evidence-root and one fresh persisted schema-aware controller
Planner stop = mandatory after failure or terminal seal
Advisor/Human decision = not required
```

## 7. 维护性判断

纠偏只补齐外置 evidence-root owner 的两级目录生命周期，不改变 production、release
或 scientific owner。新计划将 parent/root acquisition 与 controller lifecycle 分别计数，
避免隐式目录创建和事件复用；无需架构重构。
