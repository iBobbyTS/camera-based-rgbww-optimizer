# P7 retained-R3 Option B：M1 existing-root identity owner gap review

**Planner review date:** `2026-07-31`

**Reviewed reference task:** `REF-P7-25-R2-B2-M1`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-REAL-MANIFEST-DOMAIN-TEMPLATE-V1`

**Decision:**
`REJECTED_EXISTING_ROOT_IDENTITY_OWNER_MISSING_M1_NOT_IMPLEMENTED`

## Reviewed scope and evidence

Planner independently reviewed the active PLAN, clean HEAD
`195afbe54caeda01fcf65af4d97604665d5e7adb`, its ER-only evidence commit, the activation parent
`535e5e115233213d5d55859f40e021b5bb6ab850`, and current P3/P4 owner source through CodeGraph.

Executer passed the exact activation gate, ran the required pre-edit CodeGraph sync/query, and stopped before any source or test read/edit. The first failure is an existing-owner contract contradiction:

- P3 `read_exact_file(..., root=...)` safely revalidates a typed `DirectoryIdentity`, requires an absolute exact direct child, and rejects identity drift, but P3 has no public way to acquire a `DirectoryIdentity` for an already-existing `0700` root.
- P4 registers a live read root only when a `DirectoryIdentity` is returned by a recognized effect-owned call. Current registration is therefore reachable only through `create_exclusive_root`; directly constructing an identity is deliberately a fixture and cannot authorize a physical read.
- M1 requires seven existing C1/retained roots plus one new output root, while freezing output-root creation to exactly one and prohibiting P3/P4 edits. Binding existing reads to the output root violates P3 direct-child checks; constructing or aliasing identities fails P4 with `read_root_not_live_identity` or an existing transport rejection.

The ER handoff records source writes `0`, test writes `0`, implementation commits `0`, tests `0`, accepted/retained physical reads `0`, external controller/root/process effects `0`, and every validator/release/network/device/science route `0`. The result is therefore strong fail-closed pre-edit evidence. It cannot prove M1 implementation acceptance, and the missing owner cannot be repaired inside M1's exact two-path scope.

## Planner finding

The failure is accepted as an engineering security/I/O boundary gap. It does not require Advisor color-science guidance or Human device authorization. The smallest coherent repair extends the two existing single owners only:

1. P3 gains one public dependency-injected `read_existing_root` operation that performs one no-follow `lstat`, rejects noncanonical/nonabsolute paths, symlinks, non-directories, and modes other than `0700`, and returns the existing frozen `DirectoryIdentity`. It must not create, chmod, repair, open, enumerate, or read a child.
2. P4 recognizes only the direct result of that exact owner call as an effect-owned live existing root. It may then be used directly as the `root=` name of `read_exact_file`; constructors, aliases, reflection, generic calls, nested calls, containers, and rootless reads remain rejected. Multiple independently acquired existing roots are permitted, while output-root creation and root-chain validation semantics remain unchanged.

No third owner or generic path/call allowlist is justified.

## Residual risks and exact next branch

The correction must freeze lexical canonical-path handling and stable P3 errors; prove lstat failure, symlink/non-directory/mode rejection, valid typed identity, and later `read_exact_file` drift revalidation; and freeze P4's exact owner name, direct assignment, multiple-root behavior, negative transport surface, root-read report, and unchanged created-output-root/root-chain behavior.

The exact successor is `REF-P7-25-R2-B2-M1-C1`, a pure-offline exact four-path owner correction. It may modify only P3/P4 source and their dedicated tests, uses one implementation commit, and runs CodeGraph plus targeted/focused/compileall/full/postcommit validation. It must not edit or implement M1, read real C1/retained evidence, run external processes, or enter any validator/release/device/science route. A green correction only unlocks a newly planned fresh M1 successor; it does not accept the rejected M1 package.

Planner stop after the correction execution is
`B2_M1_C1_EXISTING_ROOT_IDENTITY_OWNER_WAITING_PLANNER_REVIEW`.

维护性判断：该分支只扩展现有 P3 physical-I/O owner 与 P4 static-conformance owner，避免把文件系统能力复制进 M1 template；新增 API 单一、effect provenance 精确，回归覆盖安全边界后无需架构重构。
