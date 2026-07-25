# P7 TD-B E2 external root 与 JSON writer

**状态：** resolved / C1 accepted by Planner

**首个失败 run：**
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2/e2-fa6c95d-undefined`

**最终 summary：** `e2-execution-summary.json`，SHA-256
`12e41cd773c9ea955b4251c300ebdfcaf4fbaceadb6162be6f8c456535b63414`。

## 已确认事实

1. E2 wrapper/child 只启动一次，child exit `1`、wrapper exit `1`、retry `0`。
2. `e2_preflight.py:101` 使用 `Path(__file__).parents[4]` 推导 Git root；该文件位于外置 run directory，所得路径不是
   `/Users/ibobby/Projects/WLED-RGBWW`。随后 `git rev-parse HEAD` exit `128`，failure class 为
   `executor_preflight_root_resolution_error`。
3. 失败发生在 release、remote health/config、backend 与相机访问前；capture/CR3/NPY/formal/Ray nonzero/strip
   nonzero 均为 `0`。
4. Python cleanup、child final zero、shell cleanup 与独立 final zero 均通过；strip identity 为
   `bedroom-rgbww-strip` / `E0:8C:FE:63:C9:40`，generation `1->2->3->4->5`，五通道全零；Ray intensity `0`。
5. `e2_preflight.py:196` 与 `e2-wrapper.zsh:34` 使用 `+ "\\n"`，在 JSON 后写入字面量 backslash-n。失败后只做
   离线尾字节修复；`e2-artifact-repair.json` 保留原始 bytes/hash。由 repaired bytes 重构原始尾字节后，两份原始
   SHA-256 均与 repair artifact 精确匹配。
6. 当前未发现残留 E2 wrapper/child；HEAD 仍为
   `fa6c95dbf79f4c0828e8633560d2828e3646204b`，production-scope diff 与 staged paths 均为空。

## 根因

根因不是 Git、release 或设备，而是当时 E2 没有单一冻结、可测试、可复用的执行 owner。外置一次性 child 把代码文件
位置误当仓库身份 owner，并复制了未经回归保护的 JSON writer；因此 root resolution 与 evidence serialization 在同一
临时边界同时失效。

## 已拒绝的修复方式

- 不得修改失败 run 内的 `e2_preflight.py` 后直接重跑；旧 run 必须保持 forensic-only。
- 不得只把 `parents[4]` 改成另一个 magic index、依赖外置脚本的当前工作目录，或把本机 repo path 嵌入 source；
  canonical project root 必须作为 PLAN 冻结的显式参数传入并独立验证。
- 不得继续用 post-run 尾字节 repair 作为正常 evidence 路径。
- 不得在离线修复完成后自动执行第二次 E2 或进入 formal。

## C1 resolution

- correction root：
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-c1-offline/20260724T230534Z`。
- validation summary SHA-256：
  `5008c546d620956ed102bf35b296f16c15e4fb9d2f281bfa62573810261fdde0`。
- frozen source manifest SHA-256：
  `c6d782c7d62a4ffc9476d0357f580e02494c938f7700186b56f8e5dcd03c2426`。
- fake/runtime matrix `22/22`；root rejection、release/checkpoint、wrapper success/failure/signals/cleanup 全部通过。
- correction root 的 `62/62` JSON strict parse，真实 newline 结尾，无 repair 或 secret；`124/124` canonical artifacts
  的 bytes/hash 经 Planner 独立复算匹配。
- 旧失败 run `13/13` 文件在 before/after manifest 与 Planner live replay 中均未改变。
- findings `REV-E2-ROOT-001`、`REV-E2-JSON-002` 与 `REV-E2-OWNER-003` 已在 C1 scope 关闭。
- Planner 验收归档：`.agent-work/PLANS/20260725-0857-p7-td-b-r1-c3-e2-c1-review.md`。

## 保留边界

C1 wrapper 只验证 injected fake cleanup/final-zero lifecycle，不是可直接访问设备的 production wrapper。后续 fresh E2
必须先冻结组合 package，复用 byte-exact C1 root/release/writer owner 与现有 repository remote、Ray、ESPHome、all-off
owners；source/self-check 任一不一致均在设备访问前停止。C1 关闭不表示 E2 或 formal 已通过。
