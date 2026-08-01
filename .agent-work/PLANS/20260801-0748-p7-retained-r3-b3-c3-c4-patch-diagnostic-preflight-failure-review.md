# P7 retained-R3 Option B：B3-C3-C4 patch diagnostic preflight failure review

**Planner review date：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-M1-PATCH-BYTE-PURE-GIT-DIAGNOSTIC-V1`

**Decision：**
`REJECTED_PRE_INVOCATION_MARKDOWN_MACHINE_ROW_PARSE_AND_NON_FAIL_FAST_ROOT_CREATION`

**Exact next branch：** `REF-P7-25-R2-B3-C3-C4-C1`；先以独立pre-root process只读committed PLAN/FULL并按exact Markdown
backtick delimiter机械切片，pre-root root touch/create exact0；只有process exit0且machine-state gate通过后，才由第二个独立phase创建全新root并运行exact一次
canonical Git diff diagnostic。旧failed root不得读、写、删、修复或复用。

## 1. Reviewed activation、ER topology 与 physical EOF

- Activation `a859217aefe6cbcb421cce5aa1a178f688c899ad`是parent
  `7d2e9ac93f388f5d9204ed3243f4cf8b16dfc83f`的direct child，subject exact
  `chore(plan): diagnose B3-C3-C4 M1 patch bytes`，tree `074ed3af29ea47c4add151621e0377e35940e4fe`；changed paths exact
  `.agent-work/FULL_PLAN_REFERENCE.md`、`.agent-work/PLAN.md`与
  `.agent-work/PLANS/20260801-0737-p7-retained-r3-b3-c3-c4-v3-m1-patch-byte-review.md`。Activation archive bytes/SHA-256
  exact `5725` / `b53d451c88c999d8bb1e6a1becc17c18c40e253a4730f23acf83954d9badf6af`。
- Evidence `e0b0e34116ddb3c09a7072f1c3782786ee6ad9d0`是activation direct child，subject exact
  `chore(evidence): record patch diagnostic preflight stop`，tree `bcd871e8d9b4f24695086c54cf0d92e202165526`，changed path exact仅ER。
- ER prefix blob/bytes/SHA-256为`bce93488e3c1d815767ced3f62b1cae1f189b241` / `1354521` /
  `50fd97882b243d926ab7f4fd7b083c82068917aa7293f06a6d659b2449cb7ee9`。Evidence在physical EOF只追加6行、4354 bytes，suffix
  SHA-256 `6947626b0531160e25fbab7cd6f6a157a702e32db8b625a22af73ec675cb7637`；after blob/bytes/SHA-256为
  `cde8e55036f9368c2f17821d5559faa6b6171208` / `1358875` /
  `d5a8b60c676a6cd9f4d8eb39dd7f05a2bbdf28b2a4a38274d9d462677f6220fb`。旧ER是exact prefix，没有rewrite或interior insertion。

## 2. First failure 与 secondary effect

First failure是`PLAN_MACHINE_ROW_MARKDOWN_DELIMITER_PARSE_FAILURE`，不是M1 patch-byte mismatch：

- committed/current PLAN与FULL分别匹配，strict UTF-8 decode各一次；
- wrapper却搜索bare `PLAN_MACHINE_CONTRACT=` line prefix，而committed row真实格式是
  `` `PLAN_MACHINE_CONTRACT={...}` ``；因此machine-row parse attempt1、success0、reported count0；
- failure发生在controller source creation、controller invocation和canonical Git command之前。Observed argv/stdout/exit/stderr均为null；canonical Git
  diagnostic invocation exact0，不能据此归因M1 patch bytes或声称provenance drift。

同一shell没有在preflight Python nonzero后立即终止，继续完成fresh package absence check1与mkdir1，创建了mode0700 root
`...-m1-patch-diagnostic-a859217aefe6`。这是次生lifecycle越界effect：原PLAN要求preflight失败即停，而root本不应出现。Controller和diagnostic均未创建，
root必须标为failed、immutable、non-consumable；本审核未读取该root，successor也不得读取、复用、删除、repair、rename或把它视为absence-gate candidate。

Process scan报告match1且`self_wrapper_match=true`；这是扫描命中执行wrapper自身，不证明有残留owned controller。由于first failure与non-fail-fast root effect已经
成立，本结果仍须reject，不能用process scan重分类为diagnostic evidence。

## 3. Budget与hard-lock review

Actual controller source writes/controller invocations/canonical Git diff/diagnostic writes均`0/0/0/0`；retry/fallback `0/0`。Remaining manifest
self-check、focused、full、synthetic均0。Failed V3/V2/earlier roots、real manifest/source、C1与retained artifacts、working-tree source/test reads均0。

Canonical lineage validator/callback、retained audit、eligibility、release generation/qualification/copy/consumption、network/DNS/environment/credentials、device/
camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment全部0。Retained R3仍为
`RETAINED_UNVALIDATED_UNCONSUMED`，release non-consumable。Executer commit0。

因此failure是pure-offline execution-wrapper sequencing defect，不需要Advisor科学判断或Human设备授权。

## 4. Planner findings 与 minimal correction boundary

1. Markdown machine row不能按bare prefix找。机械算法必须逐行匹配含opening backtick的exact prefix和closing backtick，切片只去掉这两个已冻结delimiter；不得regex、
   strip、bare-prefix alternative、generic scanner、canonical reencode、repair或fallback。
2. Pre-root parser必须是一个独立process/command，只通过`git show <activation>:<path>`读取committed PLAN与FULL；它不得读取working-tree copies、external
   roots、source/test或任何evidence payload，也不得lstat/absence-check/mkdir/write root。
3. Phase1失败必须由command boundary fail-fast：nonzero、stderr、row count、JSON、required FULL subset或output-envelope mismatch时，第二phase invocation exact0，root
   touch/create exact0，只做single ER failure handoff。
4. 只有Phase1 exit0并输出一个strict success envelope，Executer才可发起另一个独立Phase2 command。Phase2使用activation short派生不同的fresh root，做一次
   absence gate和mkdir，运行原冻结canonical Git argv exact一次并写single diagnostic；不得复用旧shell或旧root。
5. Diagnostic classification仍只区分V3 controller rendering/comparison mismatch、current canonical Git rendering mismatch和Git command failure；actual provenance
   drift claim继续禁止。

## 5. Residual risks与next acceptance boundary

Current canonical Git stdout identity仍完全未观察；M1 patch-byte difference既未被证明也未被反证。Successor必须首先证明machine-row extraction本身正确，再取得exact
argv/stdout identity。不得恢复remaining self-check、focused/full/synthetic，也不得进入real retained/validator/release/device stage。

若Phase1失败，root creation必须可由actual count证明为0；若Phase2失败，保留new root但不retry。只有exact canonical argv exit0、stdout bytes5874、SHA-256
`6b26e49359f944bceafe5129b0b81a3d5600d400eae7d3b739c2baba12d6a5ca`匹配，才能分类为
`M1_PATCH_BYTE_EXACT_CANONICAL_GIT_DIAGNOSTIC_MATCH_NO_PROVENANCE_DRIFT`并停在Planner门。

维护性判断：问题局限于一次性wrapper的machine-row delimiter和phase ordering；用两个独立process建立hard boundary即可，不应新增持久化parser framework或修改生产
代码、测试、manifest、validator。
