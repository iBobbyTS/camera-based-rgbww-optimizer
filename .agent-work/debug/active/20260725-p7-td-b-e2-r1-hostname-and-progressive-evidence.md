# P7 TD-B E2-R1 hostname 与 progressive evidence

**状态：** active / C2 harness accepted; Z0-R2 valid pre-device failure; real reachability gate still unconsumed

**失败 run：**
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1/e2-fa6c95d-20260725T152859Z`

**最终 summary：** `e2-execution-summary.json`，SHA-256
`63599437885c25c040f91001d7f2de5341d1389406c0d5e57febab72c39701a8`。

## 已确认事实

1. no-device self-check `6/6` 通过，随后只执行一次 real E2；wrapper exit `1`、retry `0`。
2. byte-exact C1 root/release gate 通过。remote health/config 和 Ray node/CCT 控制流在首个 strip call 前完成，但 child 没有
   逐阶段保存其 detail。
3. primary `esphome.verified_light(0,0,0,0,0)`、Python cleanup strip、child final-zero strip、shell cleanup strip 与
   independent final-zero strip 均报：
   `ResolveTimeoutAPIError: Timeout while resolving IP address for ['bedroom-rgbww-strip.local']`。
4. 本 run 没有任何 generation-bearing strip evidence，不能证明 strip 当前全零。shell cleanup raw stdout 独立证明 Ray
   `set_cct` 成功且 intensity `0`。
5. 同一 checkpoint 的前一 E2 cleanup 曾通过相同 hostname，取得 exact identity
   `bedroom-rgbww-strip / E0:8C:FE:63:C9:40`、state object `rgbww_commanded_state` 与 generation `4->5`。当前 failure
   只能证明本次 reachability 失败，不能区分 mDNS、fixture power/Wi-Fi 或其他本地状态。
6. CR3/NPY/capture/nonzero/formal/public analyzer 均为 `0`，无残留 owned process；C1、旧 E2、release、source 与 workspace
   无漂移。
7. child 只在完整 primary 成功后写 remote/Ray/strip aggregate；strip failure 使 remote/Ray detail 丢失。
8. ESPHome、remote 与 Ray counters 在成功返回后才增加。本次至少五个 strip attempts 被汇总为 `esphome_calls=0`，该字段
   实际是成功返回次数而不是 attempted calls。
9. Planner live replay 的 JSON `59/59` strict parse、source `14/14` 匹配，但 canonical inventory 仅 `139/140` 匹配：
   finalizer 在 inventory empty stdout 后打印 `bounded_e2_failure\n`，使 `logs/finalizer.stdout.log` 从 bytes `0` 变成
   bytes `19`、SHA-256
   `37c07449f3ab252ae78e920ee0eaa80d1115615d23290b7dd2d71ab59cdc0d93`。
10. C2 offline correction 的 fake matrix `14/14`、terminal inventory `301/301`、strict JSON `296/296`。11 个有效 case
    的 progressive stage artifacts 可由 per-case totals 与 sealed inventory 独立重放为 `265`；case 10 的 `26/26` 均已
    seal。`validation-summary.json` 的 `239` 只因 `0*/stages/*.json` 漏掉目录 `10-*`，已由 Planner 明确标为
    non-authoritative，不代表 evidence 缺失。
11. Planner 接受 C2，关闭 `REV-E2R1-PROG-002`、`REV-E2R1-ATTEMPT-003` 与 `REV-E2R1-SEAL-004`；
    `REV-E2R1-HOST-001` 仍 open。review archive 为
    `.agent-work/PLANS/20260725-1031-p7-td-b-r1-c3-e2-r1-c2-review.md`。

## 当前假设

C2 已解决 package evidence owner，剩余根因边界是 external hostname/ESPHome reachability。下一次 diagnostic 必须只发送
exact zero，通过 generation-bearing state 证明当前状态，并把五个预分配 stage 各自记录为 immutable attempt/result；无论
成功或失败均不能解释为 E2 retry。

## 已拒绝的做法

- 不得直接重跑完整 E2、进入 formal，或修改旧 run 内 frozen source。
- 不得用历史 zero、Ray zero 或“发出的命令是 zero”替代当前 strip generation-bearing zero proof。
- 不得把 `.local` 改成未冻结 IP、写 `/etc/hosts`、重启 mDNS/network service 或实施其他环境变更来绕过证据门。
- 不得继续把 success-return counters 命名为 calls/attempts。
- 不得让 strip failure 短路 Ray cleanup/final-zero evidence。
- 不得在 terminal inventory 后写入任何 listed artifact。

## 下一步与验收

1. 按 active PLAN 在唯一新 external root 先运行 no-device matrix；任一 fake case 不通过则不得访问 secrets/network/device。
2. matrix 通过后最多执行一次 real Z0 wrapper；五个 assigned stages 均只调用 exact
   `verified_light(0,0,0,0,0)` 一次，禁止 nonzero、Ray、camera、E2 与 standalone hostname probe。
3. pass 要求 exact name/MAC/state object、每次 baseline-to-observed generation 增加、跨 stage generation 单调、五通道全零，
   且 terminal live replay `N/N`。
4. primary 或任何 cleanup/final stage 失败均 overall fail closed；later zero success 不能重解释 earlier failure。不得重跑 Z0。
5. 若 hostname/ESPHome 仍失败，由 Human 检查 fixture power、Wi-Fi 与本机 local-network/mDNS；不得自动改 IP/hosts/network
   或刷固件，无需 Advisor。

**Planner review archive：**
`.agent-work/PLANS/20260725-0956-p7-td-b-r1-c3-e2-r1-failure-review.md`。

**C2 acceptance archive：**
`.agent-work/PLANS/20260725-1031-p7-td-b-r1-c3-e2-r1-c2-review.md`。

## Second-pass reset：Z0 harness 与 evidence-tree boundary（2026-07-25）

### 新确认事实

1. Z0-R1 因 external source 手填 PLAN bytes `3_000_000`（实际 `12933`）在 matrix/device 前 valid-fail；real gate未消费。
2. Z0-R1-C1 因 compile preflight import生成 `source/__pycache__/` 在 matrix 前 valid-fail；未删除、修补或重跑。
3. Z0-R1-C2 offline correction已通过 hygiene `10/10`、PLAN identity `14/14`、真实 injected lifecycle `18/18`
   （90 stages）和 terminal `527/527`，关闭 PLAN identity、signal、lifecycle与source-hygiene四个 findings。
4. Z0-R2 mandatory self-check在第一个 old-C2-tree before-manifest gate fail closed：C2 accepted tree按设计保留
   `fixtures/source-hygiene/05-source-symlink/source/harness.py` 和 directory-symlink负例，但新 owner无条件拒绝tree内任意symlink。
5. Z0-R2 fresh wrapper另有独立 byte-exact drift：accepted C2 wrapper为 `1671` bytes、SHA-256
   `890caf867a4f5630c52bd59b8c7d078daf0f59cd75dfc7b32c79879fe93354e6`；fresh copy为 `1672` bytes、SHA-256
   `15dfa4a3631d82dc3bf1c23887d788344c86f13f267272edccb5d8e2d71f5522`。`cmp`证明差异是末尾多一个 `0a`。
6. Z0-R2 self-check恰好一次、exit `1`；real wrapper、assigned real attempts、production import、secret read、hostname、
   network和device均为 `0`。root：
   `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r2/20260725T183318Z`。

### 当前根因假设

根因不是 hostname、production ESPHome或C2 accepted harness，而是Z0-R2 producer把两种不同语义合并成一个无条件tree owner：

- immutable evidence tree需要保留并hash所有 planned negative symlink entries；
- executable actual source tree必须严格拒绝任何symlink/extra entry。

同时 wrapper producer使用文本重写而非byte-for-byte copy，破坏了PLAN冻结的exact artifact identity。

### 下一最小验证面

1. 对accepted C2 root建立manifest时，显式分类 planned-negative symlinks并记录link text与non-follow identity；unknown symlink仍拒绝。
2. 对actual Z0 source继续执行strict no-symlink exact inventory，不复用evidence-tree allowlist。
3. wrapper只用no-follow byte copy/exclusive write，并在任何preflight前比较bytes/hash/inode；增加trailing-newline正负例。
4. 新纠偏必须offline-only，先复现上述两个原始症状并验证修复；不得同包启动real Z0。
5. 若该针对同一 evidence-tree/source-copy boundary 的纠偏再次失败，停止继续叠加一次性owner，重新评估producer/state ownership与
   test fixture contract，而不是直接发布下一次real gate。
