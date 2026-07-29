# P7 FORMAL-R5 activation C1 Planner review

**Review date：** 2026-07-26

**Reference task：** `REF-P7-04`

**Reviewed PLAN contract：** `P7-TD-B-RAY-PUBLIC-DEFAULT-FORMAL-R5-ACTIVATION-C1`

**Reviewed PLAN SHA-256：** `9ab87d2c8c0ed814fce0752a43f6f86a2a04e0e5ac4684a991f54157803972d2`

**FULL_PLAN_REFERENCE SHA-256：** `45d218601850b9ef98bc5bdae184260e7031418ea1fee68120aacab69a0fb3ff`

**EXECUTION_RESULT §127 SHA-256：** `efa459814e9da145c95edafaf9027f9bc5cfa9dd7d801f5e431cffd5de516f97`

## Reviewed evidence

- Evidence root：`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-r5-activation-c1-offline/20260726T223000Z`。
- Corrected candidate / lifecycle owner / validator / non-authorizing template SHA-256：
  `8bf9c351d05e26199c6ad90556d560b326ee4a7891de78c416b155730f7fb782` /
  `24e24323e0219d0a9bbc46addbc48cab516140e4457125bd44775f6544b1eece` /
  `b8a2c360c490916b3b0932cf0c7d652fa0f672e3808b7b23419d17d575c43448` /
  `4b99509e8ae65a40aab98d54f289ee51f0771370ab88537c0e64a788ce5a1fcb`。
- Legacy corrected-owner matrix `30/30`；new shared-entrypoint matrix `11/11`；combined `41/41`。Shared/combined SHA-256：
  `3e35943fcab5edabae8f85517584147a850b30c29698e0dca1908981c4858039` /
  `bb6f9b98086a7749c8862282fc7741d466ea62cbc5b9abfd1de0036ac253aa6a`。
- Validation summary / final audit / terminal strict audit SHA-256：
  `66f36aaf55a56fc59d50bc82ac1d37e033193263caf8a8190e8d49d3f0844865` /
  `7242e4976d6f4fe713c12664d8560a695dbe6285996d06b69968312eb5610252` /
  `5338d71a5b505f7f774098bcad0908d7814320723c0b3c34bd8ed676dec09b6d`。Terminal strict覆盖305个regular JSON，mismatches为空。
- JSON inventory 302个regular JSON，parse/literal-backslash-n/secret-like mismatches为空，SHA-256
  `7cffdaf4665422befbaded3fec9652b0056aabdd3815cc90eef3bc8aaf034d14`。

## Findings closure

### REV-R5-001 closed

Corrected real activation是future package的lexical sibling：
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-r5/formal-r5-1e3b107-20260726T220000Z.activation.json`；不再位于package subtree。
Valid sibling case在package不存在时通过同一`main -> validator.validate -> run_lifecycle`，达到`activation_accepted`并terminal seal；实际
injected adapter ledger为7个ordered calls。测试替换的仅是child side effects，没有替换activation、state或lifecycle owner。

### REV-R5-002 closed

Canonical current C1 PLAN通过同一shared entrypoint返回`rejected_pre_child`，adapter object实测ledger `[]`，package/evidence root前后不变。
Missing、inside-package、preexisting-package、wrong-path、symlink、nonregular、wrong-mode、candidate-hash drift和later-PLAN drift同样均为实测
zero calls；不再使用常量`0 == 0`。

## Outer zsh status error disposition

首次且唯一C1 matrix与independent audit均成功，final audit和validation summary已在`2026-07-26T22:20:31-0600`封存。其外层临时zsh
bookkeeping随后试图写zsh只读变量`status`并报错；错误不在candidate、owner、validator、matrix或auditor内部，没有改变任何case/code/
fixture，也没有触发matrix或independent audit重跑。`2026-07-26T22:21:15-0600`生成的terminal strict audit只是读取既有JSON并加入最终三份
顶层JSON的strict inventory，未调用执行路径。

因此该外层shell非零是handoff编排噪声，不改变已经原子封存的C1 scientific/authorization evidence，也不要求重跑。后续actual formal
不得复用该临时bookkeeping片段；只执行冻结candidate的零参数命令，并以candidate/package terminal evidence作为结果owner。

## Decision

**结论：** `accepted_and_release_single_actual_formal_r5`。

- C1关闭`REV-R5-001/002`；candidate可作为exact later FORMAL-R5 active PLAN的冻结输入。
- Release generation历史预算保持1/1；截至本review release consumption、device/network/live/formal仍为0。
- Human设备总暂停已解除；GUIDE/FULL的formal进入条件、current-checkpoint production-usable lineage release、fresh roots与continuous
  fail-closed candidate均已满足。无需Advisor补充即可放行一次actual FORMAL-R5。
- 下一PLAN只授权一次continuous Terminal launch：Ray 16 formal → Ray public gate → conditional strip 16 formal → strip public gate →
  independent final-zero → paired finalizer → terminal seal。任一失败停止，不重试、不自动进入TD-C。
- Firmware upload、remote deployment与破坏性硬件操作继续禁止。

**Residual risks：** 实际formal预计数小时；必须由可见Terminal拥有，三次稀疏liveness后交由Orchestrator automation唤醒。Hostname、camera、
quality、sidecar、timing、cleanup或final-zero仍可hard-fail；任何返回都只交Planner review。`REF-P7-05`在actual evidence接受前继续blocked。

维护性判断：C1保持single validator/single lifecycle owner并关闭真实入口分叉；actual plan无需新增实现，只冻结并消费已验收的外置candidate。
