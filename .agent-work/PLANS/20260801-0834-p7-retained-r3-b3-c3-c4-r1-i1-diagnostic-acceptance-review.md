# P7 retained-R3 Option B：B3-C3-C4-R1-I1 stable diagnostic acceptance review

**Planner review date：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R1-I1`

**Decision：** `ACCEPTED_COMPLETE_STABLE_OWNER_CANONICAL_PATCH_EXACT_MATCH`

**Exact next branch：** `REF-P7-25-R2-B3-C3-C4-R2`；恢复B3 engineering remainder：real manifest/Git/input self-check → focused83 →
updated full810 → fresh synthetic/replay。B4继续blocked，直至该完整顺序经Planner接受。

## 1. Topology与EOF evidence

- Activation `5bcc8d36488da366d717e5abd5b600a18e38fbf5`是parent
  `22712bf901da2ad1002514363796cf38ba941507`的direct child，subject exact
  `chore(plan): activate stable offline patch diagnostic`，tree `5ce7f2404ab7c7e1404558d6291593457d5ad184`，changed paths exact
  FULL/PLAN/R1 acceptance archive。
- Evidence `6b2df9a376e30b971d3b021d868cc0cc4022b3bc`是activation direct child，subject exact
  `chore(evidence): record stable offline patch diagnostic`，only ER。
- ER prefix blob/bytes/SHA-256为`8e663b925dcb8ce50d234994adab9f4374d4c652` / `1370795` /
  `253eebf0a33c84ae452d2015c0767b3f7a15a84a869c40372f1faceebaffc863`；physical EOF suffix为4605 bytes、SHA-256
  `35e4bbe3939eb194d7367058bc0c644bcf23fbe0ced516bf3e3c27af29ebaf3d`；after blob/bytes/SHA为
  `71f2a9a210e02af2b8ac980139334ebff5840805` / `1375400` /
  `d6f429e69136b240a867920525c0cad4709b15245d39a6a2f99be840cfae645c`。旧ER为exact prefix。

## 2. Stable owner invocation review

Minimal launcher exact1；以`git show`读取activation committed PLAN/FULL各一次并把raw bytes原样传给accepted owner。Launcher自身machine-row parse与subset
checks均0。Accepted owner exact1、default P3 `run_read_only_git` exact1；PLAN/FULL schemas正确且required FULL subset type-exact true。

Expected/observed argv逐项相等：`git diff --binary --full-index --no-ext-diff`、parent
`f2b38c530a6cbac5c29d761036eb3cd2a159f3b9`、child `0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8`、M1 source/test sorted
paths。Exit0；stdout expected/observed均6006 bytes、SHA-256
`4044c62434109516e16e1fe3daad5c56d1f3ea4558f092f2976aaaec02fc94c5`；stderr0、empty SHA exact。Canonical report
classification exact `CANONICAL_PATCH_EXACT_MATCH`，provenance drift false。

Launcher/owner/helper/report counts1/1/1/1，retry/fallback0；process scan1、owned0、single ER append后operations0。No one-off parser/controller、source/root/artifact
writes。

## 3. Locks与route decision

Tests/CodeGraph、working-tree files、failed/external roots、real manifest/C1/retained、synthetic、validator/callback/audit/eligibility/release、network/device/science/
firmware/deployment均0。Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

I1只解决M1 patch attribution并证明committed object graph无drift。FULL明确要求B3通过后才能提出B4；B3剩余的real manifest/Git/input self-check、focused、durable full与
fresh synthetic/replay此前全部仍为0。因此不可直接B4。下一包必须恢复C4 basename-bound verification remainder，沿用accepted schema/identity contracts与retry0，
并将full基线从旧800更新为当前810（新增owner dedicated10）；focused原九模块仍为83。

维护性判断：stable diagnostic已关闭临时parser分支；下一包只完成既有B3验证链，不修改production、manifest或validator owner。
