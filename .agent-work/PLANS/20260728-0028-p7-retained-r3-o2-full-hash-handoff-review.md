# REF-P7-25-R2-O2 / Orchestrator FULL-hash handoff review

**Planner decision：** `REJECTED_DYNAMIC_FULL_BYTES_BINDING`

**Planner date：** 2026-07-28 00:28 MDT

**Reviewed reference task：** `REF-P7-25-R2-O2`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-REAL-READ-ONLY-AUDIT-O2`

**Exact next branch：** `REF-P7-25-R2-O2-C1`

## 1. Frozen review inputs

```text
HEAD =
  9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
reviewed PLAN SHA-256 =
  237c9a94341ad8c2d672549d46914f10a363d713909057d02429e9eed75f46d7
reviewed EXECUTION_RESULT SHA-256 =
  3d0dc0289b91634f5f14b55288b14071bd317a28fb88a56800439ff17971b8ab
reviewed FULL_PLAN_REFERENCE SHA-256 =
  308a1512480b3de7c88f274ea9ee07e648e5df1547149da51015adbbbbfa24cb
GUIDE SHA-256 =
  659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35
```

## 2. Finding and decision

O2 froze the pre-dispatch FULL bytes SHA
`7408b4764b9f165588e484efaec427ad4d39e19ed38b8ab3eb9569eda4636a74`.
After PLAN creation, the Orchestrator performed its required ownership update
and marked O2 active/dispatched, producing FULL SHA
`308a1512480b3de7c88f274ea9ee07e648e5df1547149da51015adbbbbfa24cb`.

Every other dynamic input matched. This is a Planner contract defect: exact
FULL-file equality conflicts with the Orchestrator's required post-PLAN
dispatch update. It is not retained-source drift.

```text
REF-P7-25-R2-O2 = REJECTED_DYNAMIC_FULL_BYTES_BINDING
retained audit credit = 0
retained R3 = RETAINED_UNVALIDATED_UNCONSUMED
```

## 3. Consumed and unconsumed lifecycle

The Executer read only the exact retained source root and its three children
for preflight. Their exact type, device, inode, mode, bytes and SHA matched the
frozen contract. This source preflight is not helper audit credit.

```text
helper invocation = 0
evidence parent/root acquisition = 0/0
progressive/terminal = 0/0
public lineage validator = 0
fake consumer = 0
independent replay = 0
qualification/generation/retry/repair/copy/consumption = 0/0/0/0/0/0
device/network/formal/public analyzer = 0/0/0/0
```

The original O2 evidence parent/root remain absent and must never be reused.

## 4. Exact correction

`REF-P7-25-R2-O2-C1` must remove FULL whole-file SHA equality and instead parse
exactly one `FULL_PLAN_MACHINE_STATE` JSON object. At execution it must bind：

- schema, GUIDE path/hash and current checkpoint;
- one active task and the exact C1 task/contract;
- release checkpoint, accepted Option A owner and retained-R3 status;
- Human/authorization provenance plus device/release authorization locks;
- `executer_dispatched=true`, which the Orchestrator is explicitly allowed to
  set during dispatch.

All non-FULL hashes, exact retained source, single helper/validator/consumer/
replay caps and zero-operation boundaries remain unchanged. C1 uses a new
fresh evidence parent/root and stops at Planner review.

## 5. Residual risks and locks

- Real retained schema/semantic compatibility remains untested.
- A helper, validator, consumer, terminal or replay failure in C1 remains a
  valid hard stop and cannot be retried or repaired in-place.
- No release, device or formal route is unlocked.

No Human authorization or Advisor decision is required because C1 remains a
strict offline read-only source audit with fresh evidence writes.

## 6. 维护性判断

The correction removes an ownership-layer hash cycle without weakening the
execution contract: FULL remains bound by a unique fail-closed machine state,
while immutable code, GUIDE, archive and source bytes retain exact hash gates.
