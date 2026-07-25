# P7-TD-B-F0B-R1-C3-E2-R1-Z0-R2 pre-device failure Planner 验收归档

**验收时间：** `2026-07-25T12:40:25-0600`

**验收角色：** Planner

**被审 active PLAN SHA-256：**
`46f2fa6c9c85858f1876c66c5cba737d8a044bd2b2e4ff8f694a8bc27df18056`

**Planner 决定：** `rejected_pre_device; offline_engineering_correction_required`

**精确下一分支：** `P7-TD-B-F0B-R1-C3-E2-R1-Z0-R2-C1_OFFLINE_OWNER_CORRECTION`

## 被审范围与停止点

被审 PLAN 只在 mandatory no-device self-check 全绿后才允许一次 real zero-only wrapper。Executor 在唯一 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r2/20260725T183318Z`

启动 self-check 一次并 exit `1`。失败发生在首个 accepted C2 old-tree before-manifest gate；source manifest、compile、PLAN
freeze、三组 matrix、pre-device pass、real wrapper与五个assigned ESPHome stages均未开始。Executor未修补、未重跑并按停止点返回。

## Canonical evidence

| evidence | bytes | SHA-256 |
| --- | ---: | --- |
| `validation-summary.json` | 627 | `03e5900ffa495e5958be34283007fc13f950a25a0d53db0ba761a11b9c576046` |
| `pre-device-failure.json` | 2315 | `7f2c259e5973ce5e6554874e3c52ea8c0667b47abef5633a6e66e7f57e725d8a` |
| `terminal-failure-snapshot.json` | 430 | `80d4f1952d3c31aaf43d9d910d08aaf0abb3309152c18ba1cf8c322d7b9c753b` |
| `logs/self-check.stderr.log` | 1070 | `c0bad20d521781751a6e5b980340979e526f5986c5506f613226fe5e50bacb7c` |
| `logs/self-check.stdout.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `.agent-work/EXECUTION_RESULT.md` at review | 161760 | `6407ae6b1479f7e5af02d7a85a3eb0d55e12907d7f8652444817391ddc7de40d` |

## Planner 独立重放

1. direct validation 与 `EXECUTION_RESULT.md` hashes、bytes均匹配；三个structured JSON可strict parse，failure status与contract ID
   一致。root中只有三个source、两个logs和三个failure artifacts；stdout为0 bytes，owned process为0。
2. accepted C2 root确实保留两个计划负例symlink：case 05 file symlink与case 06 source-directory symlink。R2
   `tree_manifest()` 对任意symlink直接抛错，因此把immutable evidence tree中的planned-negative fixture错误当成executable source
   污染。报错path与live tree一致。
3. R2 `run_wrapper.zsh` 为1672 bytes、SHA
   `15dfa4a3631d82dc3bf1c23887d788344c86f13f267272edccb5d8e2d71f5522`；accepted C2 wrapper为1671 bytes、SHA
   `890caf867a4f5630c52bd59b8c7d078daf0f59cd75dfc7b32c79879fe93354e6`。`cmp`只报告accepted source EOF，R2在末尾多
   一个`0a`；即使首个gate修复，wrapper exact gate仍会fail closed。
4. self-check runs恰为1、rerun 0；real wrapper、assigned attempts、production import、secret read、hostname/network/device均为0。
   camera、Ray、nonzero、E2、formal、firmware、network config、git stage/commit均为0；HEAD保持
   `8cd04d847d42ff5c7bcf7501f46be97cbbef429d`，production-scope diff为空。
5. 本次Planner review只读evidence/source；未执行source、compile、network/device、Z0、E2、capture、formal、release或commit。

## Findings

### `REV-Z0-R2-EVIDENCE-TREE-005` — Open

同一个无条件symlink policy被错误用于两类不同资产。Executable source owner必须严格拒绝任何file/parent symlink；immutable
evidence-tree owner则必须no-follow记录symlink自身，并仅把已冻结、路径和target均匹配的planned-negative fixtures分类为允许。
不得follow symlink、不得对任意symlink放宽，也不得把negative-fixture例外带入source/PLAN/secrets/production owner。

### `REV-Z0-R2-WRAPPER-BYTE-COPY-006` — Open

wrapper通过text/newline语义落盘，未保持accepted bytes。复制必须收敛为single binary no-follow owner：source
`O_RDONLY|O_NOFOLLOW` + regular/fstat-read-fstat，destination `O_CREAT|O_EXCL|O_NOFOLLOW`，完整写入、fsync、重开验证exact
bytes/hash；任何追加/删除尾换行或partial write均fail closed。preflight必须在syntax/lifecycle前验证accepted exact hash，并加入只差
trailing `0a`的回归。

## 重复失败分类与升级决定

这是pre-device evidence/source packaging边界的连续第三类失败：Z0-R1常量冻结、C1 source pollution、Z0-R2 evidence-tree
classification与wrapper byte-copy。real设备边界尚未执行，科学统计、采集策略、ESPHome production owner和实验方向均未改变。

因此暂停再次real Z0，要求一次offline-only engineering ownership重评与纠偏；**不升级Advisor**，因为没有科学问题或GUIDE方向
冲突。若纠偏仍不能用两个明确owner和single binary-copy owner通过fresh adversarial matrix，下一次Planner应停止继续堆叠harness，
转为工程架构重定向；这仍是engineering ownership问题，除非届时出现科学合同变化才请求Advisor。

## 下一分支

下一份active PLAN只能构建一个fresh offline package：关闭上述两个findings，明确immutable evidence-tree与executable source的policy
边界，证明wrapper byte-exact copy和trailing-newline负例，重跑final no-device source/identity/lifecycle/adapter matrices并回Planner。
不得同包运行real Z0、读取secrets、import production ESPHome owner或访问hostname/network/device；E2/formal继续锁定。
