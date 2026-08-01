# P7 retained-R3 Option B：B3-C3-C4-R1 offline patch preflight owner acceptance review

**Planner review date：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R1`

**Decision：** `ACCEPTED_COMPLETE_REPO_OWNED_OFFLINE_PATCH_PREFLIGHT_OWNER`

**Exact next branch：** `REF-P7-25-R2-B3-C3-C4-R1-I1`；仅调用accepted stable entry一次，对activation committed PLAN/FULL bytes做
preflight并运行one helper-compatible canonical patch diagnostic；不得生成新的parser/controller或外置root。

## 1. Git topology、paths与identities

- Activation `a91b1ca059ab0265678e2bd64c1447c90f67e59a`是parent
  `9e865683b718d1954582bc6ca17489d4582572a4`的direct child，subject exact
  `chore(plan): activate offline patch preflight owner`，tree `4f1642ad5470a351c7ae9234a2e4a27012171fee`，changed paths exact
  FULL/PLAN/上一C2 archive。
- Implementation `b929582521aa9e35a3bc1dcf163f1c22f1b7e2ae`是activation direct child，subject exact
  `feat(p7): own offline patch preflight diagnostic`，tree `2f4e592e660ae355b9a4cc44b67d1823dc337516`，changed paths exact only：
  `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_offline_patch_preflight.py`与
  `tests/test_p7_retained_r3_offline_patch_preflight.py`。
- Source blob/bytes/SHA-256为`f310d108872724ab07870696528706878e42e5dc` / `10603` /
  `ba5b9c178238ea70a07013aecfcf38888b207812a8972d7bfaaa1aef170a92f4`；test为
  `b4b43edfbcd17bc3c870d4735e768207120f26c3` / `9741` /
  `a0320587dd38ec15bf6e09477111760c095e03be7d80c75f15cc330d500d9529`。
- Canonical helper-compatible implementation diff exact21590 bytes，SHA-256
  `3861e40ddea21c76503c539e4aad444eed1fef79ff04b1759d32ce5e10e7c1f8`。
- Evidence `22712bf901da2ad1002514363796cf38ba941507`是implementation direct child，subject exact
  `chore(evidence): record offline patch preflight owner`，只改ER。ER prefix blob/bytes/SHA为
  `686578122ac102d165371f5d79810c1da178cb9f` / `1365584` /
  `3e3414808aa54a10fc4523dcbcc1b50235708ef21b8379699145932ed7585126`；EOF-only suffix6行/5211 bytes/SHA
  `ab9203835a0cea0178ad664209e00bc276da69bf8c971f037caf941daa3e82ed`；after blob/bytes/SHA为
  `8e663b925dcb8ce50d234994adab9f4374d4c652` / `1370795` /
  `253eebf0a33c84ae452d2015c0767b3f7a15a84a869c40372f1faceebaffc863`。

## 2. Independent API与owner review

Exact exports、three frozen dataclasses和single entrypoint符合PLAN。Entry先解析PLAN与FULL，再type-exact比较PLAN required subset；任何UTF-8/CR/row count/
duplicate/nonfinite/subset失败均发生在Git runner选择和调用前。Fixed-index algorithm只看首尾字符、`row[1:-1]`与inner prefix，不扫描内部backtick。

Patch spec只产生P3 allowlisted exact argv：`git diff --binary --full-index --no-ext-diff <sha40 parent> <sha40 child> -- <sorted unique
repo paths>`。Default runner直接引用`run_read_only_git`，report encoder直接引用`canonical_json_bytes`。Ledger argv/cwd/types/stdout/stderr及SHA全部复核后才分类；
result/report immutable且canonical。Owner无persist/root/external/network/device/validator/eligibility能力，也没有CLI或second generic Git/JSON framework。

Dedicated 10 methods覆盖合同全部关键边界，特别证明embedded backticks、FULL omission/subset mismatch时Git0、helper-compatible argv exact once、classification与no-I/O。
未发现需纠偏的实现缺陷。

## 3. Validation与locks

冻结ledger全部通过且无retry：targeted10、focused38、compileall exit0、full810、postcommit targeted10；pre/post CodeGraph sync/query exact2/2，
post-edit graph显示10 methods且external/device/validator/eligibility calls0，diff-check通过。Implementation commits1、ER append1、retry/fallback0。

真实Git diagnostic、external/failed roots、real manifest/C1/retained、remaining checks/synthetic、validator/audit/eligibility/release、network/device/science/
firmware/deployment均0。Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

## 4. Authoritative next diagnostic identity

Planner在验收中以repo Git object database只读执行exact helper-compatible argv一次（不读worktree/external evidence）：parent
`f2b38c530a6cbac5c29d761036eb3cd2a159f3b9`、child `0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8`、paths为M1 source/test UTF-8 sorted
tuple。Exit0；stdout6006 bytes/SHA-256 `4044c62434109516e16e1fe3daad5c56d1f3ea4558f092f2976aaaec02fc94c5`；stderr0 bytes/SHA
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。Exact commits、`--full-index`与`--no-ext-diff`使结果独立于worktree
和external diff drivers；此identity可由下一PLAN冻结，stable owner运行结果仍须独立比较。

维护性判断：owner把三轮失败的临时parser/controller收敛为单一typed entry且复用P3 owners；接受后只需最小launcher获取committed bytes并调用入口，不再扩展框架。
