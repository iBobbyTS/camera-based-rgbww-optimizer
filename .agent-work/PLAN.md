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
