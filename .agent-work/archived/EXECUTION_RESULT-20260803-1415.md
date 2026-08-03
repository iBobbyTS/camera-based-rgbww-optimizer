# Archive metadata

- archive_status: `HISTORICAL_NON_EXECUTABLE_REVIEWED_G4_03_READINESS_PASS_OVERALL_CLEANUP_FAIL_EVIDENCE`
- archived_at: `2026-08-03T14:15:48-06:00`
- source_owner: `Executer`
- source_type: `EXECUTION_RESULT`
- reviewed_scope: `REF-G4-03-ZERO-READINESS / sealed-pass root and owned-app cleanup mismatch`
- source_checkpoint: `663c873e79708c91c4f788144ef2987d880e7a37`
- original_body_bytes: `9377`
- original_body_sha256: `9df3bf1601ae8d13819841188a16f474367d1efdcb907f48f8d23dfd8c3fd287`
- terminal_disposition: `REJECTED_G4_03_PASS_APP_GRACEFUL_QUIT_EXIT_MISMATCH_DESPITE_RESIDUAL_ZERO`
- reviewed_plan_pointer: `.agent-work/archived/PLAN-20260803-1415.md`
- exact_next_stop: `RETURN_ORCHESTRATOR_APP_LIFECYCLE_CONTRACT_REASSESSMENT`
- historical_non_executable: `true`

该archive正式保留readiness sealed-pass与cleanup-command failure的全部事实；它不把residual zero改写为graceful quit success，
不授权重发quit、force-kill、retry、alternate root、G4-04或任何后续stage。下方逐字节保留reviewed ER body。

---

# REF-G4-03-ZERO-READINESS：bounded listener recovery handoff

**状态：** `READINESS_SEALED_PASS_APP_QUIT_EXIT_MISMATCH_WAITING_PLANNER_REVIEW`

**PLAN contract：** `G4-ZERO-READINESS-BOUNDED-LISTENER-RECOVERY-V1`

**Reference task：** `REF-G4-03-ZERO-READINESS`

**Planner stop：** `RETURN_FOR_G4_03_BOUNDED_LISTENER_RECOVERY_READINESS_REVIEW`

## 1. 结论

本轮按PLAN完成了一次bounded Amaran Desktop listener recovery，并仅运行一次既有zero/readiness wrapper。listener在本轮唯一launch后由exact owned PID `79395`于`127.0.0.1:33782`建立；readiness wrapper exit `0`，fresh root完整生成14项0700/0600 canonical evidence，terminal为`sealed_pass_waiting_planner_review`。strip、Ray、camera health/config、source-isolation及三层zero/cleanup全部通过，call ledger与PLAN成功路径exact。

唯一需要Planner裁决的mismatch是owned-app graceful quit attestation：exact bundle-id AppleScript只调用一次，返回
`-128 / 用户已取消`、exit `1`；但owned PID在0秒仍存在、1秒起消失，并在2/4/8/15秒持续为零，最终exact app process、listener与owned residual均为`0`。Executer未重发quit、未force-kill，也未用第二种退出方式。由于PLAN的PASS bullet同时写了“graceful quit成功且owned residual为0”，Executer不把命令非零自行解释为PASS或FAIL，保留事实交Planner。

未调用capture、nonzero light、config write、retained/legacy release、formal R6、TD-C、firmware或deployment；未重试wrapper、未换root、未修改service/endpoint/config/secret，未创建Terminal或automation。

## 2. Activation与immutable-owner intake

- HEAD：`663c873e79708c91c4f788144ef2987d880e7a37`
- parent：`d957a89a84d39f5d6533a2c829093c9059cb9822`
- branch：`main`
- activation subject：`docs(plan): activate bounded ray listener recovery`
- activation changed paths exact：
  - `.agent-work/EXECUTION_RESULT.md`
  - `.agent-work/FULL_PLAN_REFERENCE.md`
  - `.agent-work/PLAN.md`
- intake worktree：clean。
- PLAN/FULL repo-owned strict parser：PASS；contract均为
  `G4-ZERO-READINESS-BOUNDED-LISTENER-RECOVERY-V1`；active task/count均为
  `REF-G4-03-ZERO-READINESS / 1`；canonical next为同一task。
- existing owner：bytes `28288`，SHA-256
  `fea119e6a49825cf5858732c5a27dd0187020b70bc6fa5d6e8e2b3c428dacc8c`。
- existing tests：bytes `16311`，SHA-256
  `5e2efcbab079b46ca18e874ee5d684a73586517b58560d793d4bff6fc060a6b7`。
- existing wrapper：bytes `2969`，SHA-256
  `13c61af94a8c3e326447fe59103db074b9c707d8670120e10c82d974c09ab62a`。
- fresh root在app/listener动作前及wrapper前两次均证明`lexists=0`。
- owner/test/wrapper、PLAN、FULL、archives、GUIDE、RESEARCH全程只读。

## 3. Pre-existing与owned process分类

冻结owner：

```text
bundle=/Applications/amaran Desktop.app
bundle_id=com.sidus.amaran-desktop
executable=/Applications/amaran Desktop.app/Contents/MacOS/amaran Desktop
listener=127.0.0.1:33782
```

preflight只读`ps`/`lsof`结果：

- exact app process：空；`app_preexisting=false`。
- TCP 33782 LISTEN：空。
- 未发送WebSocket探针。

因此执行唯一一次：

```text
/usr/bin/open "/Applications/amaran Desktop.app"
```

- launch exit：`0`
- launch count：`1`
- 新出现且归属于exact executable的owned PID：`79395`，PPID `1`
- service variant：`0`
- endpoint variant：`0`

六次固定listener观察：

| elapsed | exact app PID | 127.0.0.1:33782 LISTEN | owner判定 |
|---:|---:|---|---|
| 0s | 79395 | absent | app present / listener not ready |
| 1s | 79395 | absent | app present / listener not ready |
| 2s | 79395 | absent | app present / listener not ready |
| 4s | 79395 | present | exact PID 79395 |
| 8s | 79395 | present | exact PID 79395 |
| 15s | 79395 | present | exact PID 79395 |

listener ready条件在4秒首次满足，并在8/15秒保持：exact app process存在、loopback LISTEN存在且`lsof` PID与owned app PID exact一致。

## 4. 唯一 readiness执行

wrapper前再次验证PLAN/FULL contract、active task/count、三个immutable hash与fresh root absent，均PASS。随后仅执行一次：

```text
zsh tmp/run-g4-zero-readiness.zsh /Volumes/4T/temp/rgbww-optimizer/g4-zero-readiness-d957a89a84d3-20260803T200550Z
```

exit状态：

- child exit：`0`
- shell cleanup exit：`0`
- wrapper status：`complete`
- wrapper exit：`0`
- signal：none
- terminal status：`sealed_pass_waiting_planner_review`
- retry：`0`
- alternate root：`0`

实际chronology：main strip verified-zero、Ray exact zero/readback/node、camera health/config、第一次repo-owned
`validate_both_off`均PASS；Python finally strip/Ray zero PASS；shell trap中的strip/Ray all-off PASS；independent final strip/Ray zero与第二次`validate_both_off` PASS；最终terminal seal引用此前13项且不自引用。

最终call ledger exact：

```text
strip_verified_zero=3
strip_shell_zero=1
strip_nonzero=0
ray_set_zero=4
ray_get_cct=2
ray_get_node_config=1
ray_nonzero=0
camera_health_get=1
camera_config_get=1
camera_capture=0
camera_config_write=0
source_isolation_validation=2
release_consumption=0
formal_r6=0
td_c=0
```

readiness结果：

- strip identity稳定；三次verified observed generation依次为`2`、`3`、`5`，五通道最终均为零。
- Ray node/client为`40165-560387 / 1`；main、Python finally、shell与independent final均返回CCT `5600`、GM `100`、intensity `0`；最终zero已证明。
- camera backend `remote`、model `Canon EOS R6 Mark III via r6-camera-bridge`、capability
  `remote_v2_capture_timing_v1`；health/config PASS，capture `0`，config write `0`。
- source isolation两次均由repo-owned validator通过。

## 5. Frozen root与artifact identity

```text
path=/Volumes/4T/temp/rgbww-optimizer/g4-zero-readiness-d957a89a84d3-20260803T200550Z
device=16777244
inode=2506552
mode=0700
inventory_count=14
```

| artifact | device | inode | mode | bytes | SHA-256 |
|---|---:|---:|---:|---:|---|
| `all-off-shell.exit-status.txt` | 16777244 | 2506562 | 0600 | 2 | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `all-off-shell.json` | 16777244 | 2506560 | 0600 | 457 | `25cc7b1e6791e1f28333205de8bd87a3e7f1e29b3b7f5a215a0feb32b456b7d3` |
| `all-off-shell.stderr.log` | 16777244 | 2506561 | 0600 | 54 | `dd5bb9263c3887df927111beb4855bcc6e460ec7856ff0f8ad4815d5787ad994` |
| `camera-readiness.json` | 16777244 | 2506556 | 0600 | 558 | `437dbb3bad4f8dfaccaf944db21a7c202e4e7f52b6976eb9e798f79fb46a630d` |
| `frozen-inputs.json` | 16777244 | 2506553 | 0600 | 879 | `b5d5b342c0a8b46d38151a2b71019794f67358163d0b16f543859f6adb5fb0de` |
| `independent-final-zero.json` | 16777244 | 2506563 | 0600 | 1093 | `129d6c0bcb70a7704485b8d8f6a1f562ae50ef023a243abc41567e53d511bfed` |
| `python-finally-zero.json` | 16777244 | 2506558 | 0600 | 1086 | `8e90a1a87ee828299028de4f19f348fe46cfd87f9bd878e38c1038d5f5f9fece` |
| `ray-readiness.json` | 16777244 | 2506555 | 0600 | 459 | `a19661a388e1f18453255e7497ded43acc1d476b3d880e6fe2b1c321ec7be018` |
| `runner.log` | 16777244 | 2506564 | 0600 | 54 | `dd5bb9263c3887df927111beb4855bcc6e460ec7856ff0f8ad4815d5787ad994` |
| `source-isolation.json` | 16777244 | 2506557 | 0600 | 156 | `91f7e46e58a6c561c3a03113e89b1728f44bb6683d243a5429e62ee6b40bbaef` |
| `strip-readiness.json` | 16777244 | 2506554 | 0600 | 666 | `335d8732bbb01b3a5ddc1a3339b1aae17eb0452c63f133b44444d8015c91b763` |
| `terminal-seal.json` | 16777244 | 2506567 | 0600 | 2936 | `c6fc7b2a14cfce2474e1a1369721ebbdf660aa60baccb4caf237873a1af2a39d` |
| `wrapper-result.json` | 16777244 | 2506566 | 0600 | 578 | `97011647634426f2ad89bf7b960bb0ab8ed29d1349947e52673287c9f926009d` |
| `wrapper.log` | 16777244 | 2506565 | 0600 | 119 | `4cf45638f9c62c9f000e156e02d2ad86bbb27644486b805e56f54f0b8519b392` |

全部JSON由repo-owned canonical decoder重读成功；root mode 0700、artifact mode均0600、inventory exact、terminal
`artifact_count_before_terminal=13`且`terminal_self_reference=false`。wrapper sibling scratch最终为`0`。

## 6. Owned app cleanup与最终状态

terminal seal完成后，仅执行一次exact PLAN命令：

```text
/usr/bin/osascript -e 'tell application id "com.sidus.amaran-desktop" to quit'
```

- quit count：`1`
- osascript exit：`1`
- stderr：`execution error: “amaran Desktop”遇到一个错误：用户已取消。 (-128)`
- force-kill count：`0`
- alternate quit mechanism count：`0`

六次fixed owned-exit observation：

| elapsed | owned PID 79395 residual |
|---:|---|
| 0s | present |
| 1s | absent |
| 2s | absent |
| 4s | absent |
| 8s | absent |
| 15s | absent |

最终只读检查：exact app process `0`、owned residual `0`、TCP 33782 LISTEN `0`、wrapper scratch `0`、readiness相关child/all-off process `0`。没有Terminal session、background owner或automation。

## 7. Planner decision request

readiness evidence自身满足terminal PASS、exact 14项、strip/Ray final zero、camera health/config与全部zero-call ledger；listener owner也exact。请Planner重点裁决唯一的cleanup attestation mismatch：graceful quit命令返回exit `1/-128`，但同一owned PID在1秒内退出且之后持续为零。

Executer没有权限重发quit、force-kill、重跑wrapper、换root、生成corrective suffix或解锁G4-04。请Planner按PLAN独立验收、先归档PLAN/ER并把判定交Orchestrator。
