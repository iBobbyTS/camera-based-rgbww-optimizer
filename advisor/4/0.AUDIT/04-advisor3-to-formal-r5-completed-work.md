# Advisor/3 之后至 FORMAL-R5 的完整增量工作与结果

## 0. 报告范围与事实来源

`advisor/3/0.AUDIT/` 已正式报告 P7-R1：短 off、on 60 秒协议下 reference/strip 均存在 chronology
non-stationarity，candidate 为 `formal_capture_eligible=false`。`advisor/3/1.GUIDE.md` 随后冻结路线：

```text
TD-A cold settling
-> TD-B command-switch/history
-> TD-C balanced source comparison
-> Advisor review
```

本文只报告该基线之后的新工作。事实源按优先级为：原始 retained artifact、
`.agent-work/EXECUTION_RESULT.md` 第 1 至 132 节、Planner review archives、当前 PLAN/FULL、Git 提交。
早期 `advisor/4/0.AUDIT/01..03` 只覆盖 TD-A 和 Human dwell 决定，本文取代它们的“完整性”含义，但不删除或
改写其历史内容。

Git 历史有一个结构性特殊点：`advisor/3`、早期 `advisor/4` 草稿和部分后续实现一起进入了 `9c804ab`。
因此本文不用“`9c804ab` 之后”错误截断工作，而以 Advisor/3 已报告的 P7-R1 结果为语义边界。完整相关提交从
`5572aa2` 到当前 `1e3b107`，见 `06-commit-and-evidence-index.md`。

## 1. 路线总览

```text
Advisor/3: P7-R1 valid failure / stationarity unresolved
  -> thermal protocol、timing、evidence owner 实现
  -> TD-A Ray + strip 实拍：均未在 600 秒内证明 settled
  -> Human 拒绝 900/1200 扩展，选择 operational dwell = 600 秒
  -> TD-B exact contract、exposure setup、production/release/cleanup gates
  -> 早期 Ray formal 首张返回后 6 个低信号 plane-feature hard failure
  -> physical/sidecar/remote-ID atomic evidence 与 no-ambient statistic owner 纠偏
  -> E2/Z0/lineage/visible-Terminal/evidence-only qualification 多轮 fail-closed 收口
  -> Wi-Fi 恢复后 real zero/readiness gates 通过
  -> 唯一 lineage release R2 生成并独立验收
  -> Human 在可见 Terminal 中唯一 dispatch FORMAL-R5
  -> Ray 完成 11 个 accepted formal 后，011-ray-c-t60 的两个必需 feature 因 clipping hard-fail
  -> cleanup/terminal seal 通过；strip/analyzer/retry 未进入
  -> 当前停在 Advisor 科学决策门
```

## 2. 全部执行任务账本

下表覆盖 `.agent-work/EXECUTION_RESULT.md` 的全部 132 节。内部 hard-fail 是 fail-closed 工程门的有效结果，
不等于 132 次设备失败；只有明确标记的 acquisition/formal 行涉及实机科学证据。

| 执行节 | 完成的任务 | 结果与后续含义 |
| --- | --- | --- |
| 1–10 | thermal diagnostics exact schema、evidence contract、actual exposure-start 能力核查、local v2 timing 与两轮离线纠偏 | 建立 monotonic/remote timing、source/state/cycle owner 和 derived analysis；确认 remote API 没有绝对 exposure-start，采用明确标注的 best-effort observed elapsed，未伪造绝对时间 |
| 11–18 | TD-A 离线进入门、settings/shutter、production completion、Ray wrapper、observed-elapsed timing v2 与 review-gap 修复 | 多个 pre-device/wrapper/timing 门按合同失败后离线修复；未把工程失败当成科学数据；最终形成可运行的 exact TD-A package |
| 19–22 | Human 授权记录、Ray run、strip run、paired analysis | 完成 24 formal + 6 ambient = 30 CR3；两个 source 均未通过 600 秒 settling trend；cleanup/final zero 通过 |
| 23 | Developer 600 秒 operational dwell 的 TD-B 离线合同 | 建立 `p7-operating-envelope-v2`；冻结 16 formal、0 ambient、每 source physical cap 24；持续报告“产品 600 秒、科学未 settled” |
| 24 | Ray H120/S50 exposure setup 合同 | 缺失正式 shutter 时只允许有界 setup；setup physical cap 8，并计入 formal 总 cap；不得把 setup 当 formal |
| 25 | E0X production round-trip、checkpoint/release、wrapper/cleanup gate | focused 159/159、full 529/529；首次 setup 因相对/绝对 prerequisite 路径不一致在设备前失败，cleanup/final-zero evidence 通过 |
| 26 | PATH-R1 canonical prerequisite identity | 统一 trusted path owner；focused 164/164、full 534/534；随后唯一 setup 返回 2 个 CR3/sidecar，最终 shutter 1/6400 |
| 27 | CANON-R2 setup finalization、release/E1、首次 Ray formal | 修复 Canon MakerNote exposure 后 setup release 可用；首张 `A@600` 返回后 generic writer 错误要求 ambient，且 physical ledger 漏记返回 CR3；立即停止 |
| 28 | F0A ambient/physical ledger 纠偏 | exact TD-B v2 才允许 0 ambient；physical return 在 post-processing 前持久化，accepted ledger 分离；focused 116/116、full 541/541 |
| 29–31 | F0B release dispatch 顺序、new release、E2、早期 Ray formal | 修复 release 应先于 unresolved gate 的顺序；新 release 与 E2 通过；首张 Ray `A@600` 随后因 6 个低信号 plane-feature hard-fail，physical total 3、accepted 0、strip/analyzer 0 |
| 32–34 | C1 sidecar retention、C2 atomicity、C3 exact statistic owner | rejection 也保留 CR3/sidecar path、bytes、SHA、remote IDs；缺失/越界/symlink/篡改 fail closed；exact TD-B formal 显式使用冻结 no-ambient statistic，runner/analyzer feature map 完全一致；full suite 547、549、553 依次通过 |
| 35–36 | E1 self-describing manifest、L1 checkpoint lineage release | 建立 canonical/superseded evidence 分类；源目录不变；新 lineage release qualification 一次通过、18 changed paths、public validator/fake consumer 通过、device calls 0 |
| 37–40 | E2 外置 Git-root failure、C1 harness 修复、fresh E2 hostname failure、C2 progressive/accounting 修复 | 第一次 E2 在设备前因 child Git root 推导失败；修复后唯一 fresh E2 因 Wi-Fi/hostname 解析失败；capture/nonzero/formal 0；C2 将 progressive evidence 和 attempted-call accounting fail-closed，实际 265 artifacts 与错误 index 239 的差异被明确保留 |
| 41–44 | Z0-R1/C1/C2 与 Z0-R2 pre-device gate | 修复 root、plan identity、JSON/seal/self-check 等外置 owner；所有失败均在设备前停止，没有隐式 retry |
| 45–46 | local-lab / cyber-risk workflow 文档 | 明确目标仅为 Human-owned 本地摄影灯光实验室，减少把本地设备控制误表述为通用网络操作；该阶段暂时移除 Ray default 的决定后来被 Human 的“公开协议默认值”决定取代 |
| 47–49 | baseline lineage fixture 隔离 | 修正 production 分类合同和环境 fixture；validation-only full suite 560/560，提交 `0387bcf` |
| 50–59 | Z0-R2-C1R1..R10 offline lifecycle/seal/FIFO/signal/accounting chain | 逐门验证 package identity、bootstrap、pre-driver owner、historical FIFO、signal forwarding/late result、adapter-call 与 primary-call accounting；R10 完成离线通过，旧 evidence 不被改写 |
| 60–65 | Z0-R3 及 C1..C5 | 唯一 fresh zero-only gate 暴露 runtime editable owner、AF_UNIX fixture、terminal negative 和 accounting oracle 问题；逐个离线修复，C5 matrix fail-stop 通过 |
| 66–73 | Z0-R4/C1/C1A/C1B/C1C/C1C1/C1C1A/C1C2 | 完成 exact contract parser、binding/failure seal、metadata replay、typed negative path 和 full offline replay；所有异常文件类型、path drift 与 evidence mutation 均 fail closed |
| 74–82 | REAL Z0 gates、event/seal 修复、watchdog/reachability、E2 readiness | 前几次 real gate 分别暴露外部可达性/事件一致性问题；Human 修复 Wi-Fi 后 REAL-R3 全零 gate 与 E2 readiness/final-zero 通过；这只证明当前 reachability、zero state 和 cleanup，不是 formal 科学通过 |
| 83–100 | formal prerequisite、lineage qualification、policy/path/provenance、predevice oracle、visible-Terminal launcher、environment accounting | 多轮 qualification/consumer/owner/post-seal/preexec 问题均先失败再离线纠偏；建立精确 frozen hashes、pre-child oracle、可见 Terminal 长跑边界和实际 call-accounting；没有用测试绿替代 release 或 device 权限 |
| 101 | Human 指定的 Ray public protocol default 恢复 | `e7ccdda` 恢复公开共享协议默认值；环境变量只作显式 override；空/非法显式 override fail closed；CLI/log 不输出值 |
| 102–118 | public-default successor lineage、evidence-only qualification adapter、R1 forensic disposition、R2 H1–H4 | successor full suite 571/571；首个 evidence-only invocation 因 child exit/accounting 缺口被永久拒绝；随后建立 activation、terminal owner、real-output/atomic-audit 单一共享 owner，唯一 R2 offline evidence invocation 被接受 |
| 119–125 | R2 D1–D5 evidence-to-release 与唯一 lineage release generation | D1 保持 non-authorizing；D2–D5 验证 frozen hash、real-mode evidence 与五视图共享 owner；唯一 R2 generation 1/1，production subprocess 1/1，public/final/strict validation 通过，release consumption/device/formal 仍为 0 |
| 126–127 | FORMAL-R5 offline continuous launcher 与 activation C1 | 首版 fake matrix 30/30 但 Planner 发现 activation 路径不可达、zero-call 为常量断言；C1 改为 sibling activation 与同一 `main -> validator -> run_lifecycle`，legacy 30/30 + new 11/11 通过 |
| 128–129 | actual R5 prelaunch 与 Human Terminal rebind | Computer Use 被平台禁止控制 Terminal，launch 仍 0/1；未绕过。随后只做离线 provenance rebind，把唯一 visible-Terminal dispatch 明确交给 Human |
| 130–131 | Human 唯一 dispatch、三次稀疏 liveness、automation wake | Human 启动一次，PID 5562，launch 1/1、retry 0；三个稀疏检查和一次 automation wake 均只读，确认同一 Ray process chain 存活，未 probe/re-dispatch |
| 132 | FORMAL-R5 terminal audit | Ray wrapper/child exit 1；11 accepted formal 后 `011-ray-c-t60` 两个必需 feature 被拒；12 returned CR3 全保留；Python/shell cleanup 和 terminal seal 通过；strip/analyzer/retry 0；归类为 `accepted_hard_failed_formal_attempt` |

## 3. TD-A：完成的方法和科学结果

TD-A 对 Ray 与 strip 各执行 3 个 independent cold-proxy cycles，每轮连续点亮并在 nominal
60/120/300/600 秒采集。总计：

| 项目 | Ray | strip | 合计 |
| --- | ---: | ---: | ---: |
| formal | 12 | 12 | 24 |
| ambient | 3 | 3 | 6 |
| physical CR3 | 15 | 15 | 30 |
| retained NPY | 0 | 0 | 0 |

冻结门是 trend `<=4.0`、single-frame dominance `<=0.5`：

| source | cycle 1 trend | cycle 2 trend | cycle 3 trend | max dominance |
| --- | ---: | ---: | ---: | ---: |
| Ray | 17.7369 | 16.8013 | 16.7317 | 0.2003 |
| strip | 16.8865 | 10.3106 | 11.8856 | 0.2059 |

因此两个 source 均为 `settling_not_demonstrated_by_600`；`t_settle_ray_s`、`t_settle_strip_s`、
`t_formal_provisional_s` 和 `t_formal_s` 均为 null。该结果是采集、source isolation、timing provenance、
CR3、readback 和 cleanup 均完整的有效负结果。

Advisor/3 GUIDE 原分支要求申请 900/1200 秒扩展。Human/Developer 随后明确拒绝扩展，并选择：

```text
developer_selected_operational_dwell_s = 600
operational_dwell_claim = selected_time_limit_not_proven_steady
```

该决定只改变产品时间预算，不改变科学事实，不得写成 `td_a_pass`、`settled_at_600` 或 `t_formal=600`。

## 4. TD-B：两次不同的 observer-quality hard failure

### 4.1 早期 F0B-R1：低信号失败

早期 Ray formal 在首张 `A@600s` 返回 CR3 后，由 6 个 plane-feature 的低信号质量拒绝而 hard-fail：

```text
exposure ratio = 0.9689
Tier B timing = valid
setup physical = 2
returned physical = 1
physical total = 3
accepted formal = 0/16
ambient = 0
strip / public analyzer = 0
```

这一失败暴露的证据缺口随后由 C1/C2/C3 修复：rejected CR3/sidecar/remote IDs 原子保留，physical-return
与 accepted ledger 分离，exact TD-B formal 绑定冻结 no-ambient 58-feature statistic。C3 replay 证明旧 run 的 frozen
58/58 features 均 finite 且 quality accepted，原先 6 个 raw rejected plane-feature 与这 58 个必需 features 的交集为 0；
旧 run 原始 evidence 未被修改。

### 4.2 最终 FORMAL-R5：clipping 失败，不是低信号重演

最终 retained root：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-r5/formal-r5-1e3b107-20260726T220000Z
```

唯一 Human visible-Terminal launch 被消耗一次。Ray 接受了 capture `000` 至 `010`，在第 12 个返回的
`011-ray-c-t60` 进入 post-return processing 后 hard-fail。原始 patch-statistics 显示两个被拒的**必需** feature 为：

| patch | plane | failure | clipped fraction | frozen maximum |
| --- | --- | --- | ---: | ---: |
| `block_06 / white` | `G1` | `clipped_fraction_exceeded` | `0.0007981642222887359` | `0.0` |
| `block_06 / white` | `G2` | `clipped_fraction_exceeded` | `0.000598503740648379` | `0.0` |

该 capture 是 Ray state C，即 `H300/S100/INT100`，nominal `t60`；recorded Canon exposure 为
`0.00048828125 s`，nominal shutter `1/2000`，recorded/nominal ratio `0.9765625`。因此 R5 的准确分类是
“两个 required white-patch green-plane features 因 clipping 被拒”，不是“六个低信号 features”。当前 PLAN 标题仍使用
`low-signal` 作为旧分支简称，Advisor 应以 immutable R5 evidence 的 clipping 原因为准。

R5 终态数量：

```text
planned Ray formal = 16
completed / accepted formal = 11
ambient = 0
returned captures = 12
physical total = 14 = setup 2 + returned 12
retained CR3 = 12
retained NPY = 0
analysis.json = 0
strip / paired / public analyzer = 0
retry = 0
```

这 11 帧不能称为 TD-B formal pass；第 12 张返回证据也不能删除。是否允许 11 帧作有限 diagnostic、是否重拍以及
如何冻结 exposure/quality contract，均超出当前 GUIDE，必须由 Advisor 决定。

## 5. 工程与证据治理成果

这些成果提高可审计性，但不增加科学通过率，也不授权新实验：

1. Canon exposure 以 MakerNote `Canon:ExposureTime` 为权威，缺失时 fail closed；Exif nominal 只作 provenance。
2. physical-return ledger 在 post-processing 前持久化；formal accepted、ambient 和 setup 独立计数。
3. rejected capture 仍保存 CR3/sidecar path、bytes、SHA-256、remote capture/request IDs；缺失、越界、symlink 或篡改
   均 fail closed。
4. exact TD-B v2 显式使用 no-ambient statistic；其他 caller 保持 ambient-subtracted 默认值；无自动 fallback。
5. runner 与 public analyzer 的 58-feature map 顺序、值和 SHA-256 由同一 owner 冻结。
6. release generation、qualification、consumption、device access 和 formal execution 权限互相分离；offline evidence 绿不自动放行
   release 或设备。
7. external harness 的 root、activation、progressive evidence、terminal seal、signal forwarding、attempted-call accounting 和
   cleanup 由明确 owner 逐阶段落盘。
8. 长跑必须由 Human 可见 Terminal 启动；Codex 只做三次稀疏 liveness 和 automation 终态审计，不持有后台运行。
9. 本地实验室文档已明确这些目标是 Human-owned local lab fixture/camera/reference light，不是第三方网络目标。
10. Human 已把历史 Ray key 分类为公开共享协议默认值；`e7ccdda` 恢复该默认值并保留显式 override 的 fail-closed 校验。

## 6. 当前锁与未完成路线

```text
REF-P7-04 = ADVISOR_DECISION
REF-P7-05 = BLOCKED (TD-B scientific acceptance / envelope freeze)
REF-P7-06 = CONDITIONAL (only if a later exact GUIDE branch selects it)
REF-P7-07 = ADVISOR_DECISION (600-second override vs TD-C prerequisite)
TD-C / reference classification / sentinel / remaining 9 / boundary / holdout / P8 = locked
```

在 Advisor 决定前：不得重拍或 retry R5，不得进入 strip，不得运行 public analyzer，不得删除 feature、放宽 clipping/quality
threshold、改变 exposure/covariance/statistic，也不得把 600 秒重新命名为科学 steady。

当前唯一请求见 `05-formal-r5-observer-quality-decision-request.md`。
