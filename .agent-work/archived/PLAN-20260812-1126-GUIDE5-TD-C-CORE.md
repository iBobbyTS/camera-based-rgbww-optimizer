# PLAN — GUIDE5 TD-C core

## 目标

在已接受的 bridge-v2 与 combined TD-B canonical pass 基础上，执行四个顺序平衡的
TD-C core session，建立 fast envelope 下的 absolute warm-A cross-source anchor。

## 冻结合约

- 四 session：Ray→strip、strip→Ray、Ray→strip、strip→Ray。
- 每个 source capture：both-off reset 600 s，D 120 s，A 120 s，随后仅 capture A。
- 总计 8 张正式 CR3；不采 ambient；不声称 steady/settled。
- 只检验 within-session difference、source-order effect、warm-A anchor。
- TD-C expansion、solver、sentinel 和 later stages 保持锁定。
- bounded light/camera operation 无需额外 Human authorization；所有路径 all_off。

## 执行

1. 运行 focused tests、compileall、diff-check 和 CodeGraph sync。
2. 创建 clean checkpoint commit。
3. 在外置盘新建唯一 TD-C core root，通过 visible Terminal 运行四 session。
4. 每个 session 成功 2/2 后才进入下一 session；失败先 cleanup/zero、保留 root并按
   AGENTS.md 分类修复。
5. 长任务完成三次 liveness 后设置 automation。
6. 8/8 完成后运行一次 direct analyzer；不执行 expansion 或 solver。

## Attempt 1 — ENGINEERING_OR_HARNESS_FAILURE

- root：`/Volumes/4T/temp/rgbww-optimizer/guide5-td-c-core-20260812-055130`
- checkpoint：`541c323b0d4e0ef4dd35859c5bea83ae09b90539`
- 结果：`0/8` accepted；`1/8` physical CR3 returned；quality 未生成。
- primary cause：TD-C 新计划声明 0 ambient，但 `expected_native_raw_ambient_policy()`
  仍只为 TD-B formal 返回 `unsubtracted_no_ambient`，导致共享 RAW owner 在首张
  CR3 返回后以 `non-ambient capture requires the preceding ambient capture` 拒绝。
- cleanup：Python pass、shell pass、final zero pass。
- science_delta：none；该 CR3 未进入 feature/capture ledger，不作为科学证据。
- recovery：原始 CR3、sidecar、physical ledger 保留，但 accepted feature artifact未生成；
  在失败 root 中补写半条 observation 会使证据所有权含糊，因此不恢复该 capture，
  不池化，并在修复后使用 fresh root。
- substantive correction：把 no-ambient RAW policy 精确扩展到 TD-B/TD-C P7 v2
  formal owners；其他 owner 仍 fail closed，并新增真实 behavior regression。

## Attempt 2 — ACCEPTED_VALID_TD_C_CORE

- root：`/Volumes/4T/temp/rgbww-optimizer/guide5-td-c-core-20260812-151638-noambient-fix`
- acquisition checkpoint：`7ba81b3e55f06f7e4427442b65e63fd8ea66849b`
- 结果：`8/8` accepted、`8/8` physical CR3、quality pass、wrapper exit `0`、
  Python/shell cleanup pass、Ray/strip final zero pass。
- direct analyzer 首次调用在科学计算前被旧 aperture provenance equality gate 拒绝；
  classification=`ENGINEERING_OR_HARNESS_FAILURE`，`science_delta=none`。
- correction：`3304da6439b4746757f324302040565ae25cd902` 允许 analyzer 对账计划
  `f/4` 与远程 backend 逐帧统一的 `implicit auto` 报告；ISO、RAW、逐帧一致性、
  physical/quality/cleanup 门禁不变。direct-path tests `24/24` pass。
- retained 8 captures 未修改、未重采集；恢复后的 analyzer 成功生成 `analysis.json`：
  SHA-256 `a4f4303b391c6eca5bf4a59fd1e95bf1b505b28bad4eda1c081f5d54d98a6aa0`。
- scientific result：`td_c_core_pass_waiting_for_planner`；within-session compatibility、
  order effect、stable center、warm-A cross-source anchor 全部 pass。
- `science_delta=accepted_valid_td_c_core`；TD-C expansion、solver、sentinel 与 later
  stages 仍锁定，下一步为 `ADVISOR_GATE_REQUIRED` 科学复核。
