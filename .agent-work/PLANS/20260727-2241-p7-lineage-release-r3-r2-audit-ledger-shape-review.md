# REF-P7-25-R2 / Successor R3 release audit-ledger shape review

**Planner decision:** `REJECTED_RELEASE_AUDIT_LEDGER_SHAPE`

**Planner date:** 2026-07-27

**Reviewed contract:** `P7-TD-B-SUCCESSOR-LINEAGE-RELEASE-R3-R2`

**Reviewed reference task:** `REF-P7-25-R2`

## 1. Frozen review inputs

```text
HEAD =
  32b9e670ff3bbea0cd1505528c2ca87c2935446c
PLAN SHA-256 =
  866f58337bba036d7d58ba473ba5bb779e5cb10a8345341311f0b2c80dad3a7a
FULL_PLAN_REFERENCE SHA-256 =
  e77a321a592bc49c59fd0428b9d9d301f112dc1dcd9eabbf6c5753fcf8d381f4
EXECUTION_RESULT SHA-256 =
  b2a24c510002802426e5608ed39caa56594413c056e30db19df5eba4420884d9
```

Package：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/
lineage-release-32b9e67-r2-20260727T2227

11-terminal-summary.json SHA-256 =
  eddd6dc8f5974155e56f302326b5b88fdbf565884b6c90433c9cf351af55c7ac
```

## 2. Accepted execution facts

- Frozen Git、owners、inputs、old-R2 manifest、failed-C1 manifests 与 fresh-root absence
  preflight 均通过。
- 唯一持久化 controller lifecycle 的 build/SHA/compile/exec 为 `1/1/1/1`，
  preacquisition/package acquisition 为 `1/1`。
- Production qualification start/completion 为 `1/1`，exit `0`；release generation
  为 `1`，retry/repair/alternate root/second controller/second release 均为 `0`。
- Exact three-artifact family 已生成并保留：

```text
current-lineage-candidate.json
  9819 bytes
  3a2ff5a2af200c55c925b954488c5c5dd31a35a481440d17dfcdd8b68419f2e0
resolved-formal-plan.json
  15137 bytes
  cf7c78b6a6cfda4055d05f5e9bbe9914161213b380dc7736ee09e257dd45eb6b
setup-lineage-release.json
  1567 bytes
  0bacf1878a97fcdc4436259e132e89f6e56611df6d7fb5d5a7da28f62c98ad3e
```

- Current candidate 的 `changed_paths` 是 59 个
  `{"classification": <str>, "path": <str>}` row，`prohibited_paths=[]`。
- Setup/candidate、old R2 与两个 failed-C1 roots before/after 全部相等，
  mismatches 为空；10 个 retained JSON 均可严格解析。
- Device/network/DNS/.env/camera/Ray/strip/capture/formal/public analyzer 与 release
  consumption 均为 `0`，residual owned process 为 `0`。

## 3. Blocking finding

### REV-R3-R2-001 — External release audit assumes obsolete `changed_paths` shape

R2 controller 的第一次 internal release audit 执行：

```python
changed_paths != sorted(set(changed_paths))
```

Production owner 当前输出 dict ledger，而不是字符串数组。因此该表达式在 audit source
line 326 抛出：

```text
TypeError: unhashable type: 'dict'
```

失败发生在 qualification exit `0` 与三 artifact 生成之后、`05-release-audit.json`
写入之前。Public validation、fake consumer、final audit 与 strict audit 的实际计数均为
`0`。因此：

```text
qualification = PASS_ONCE
generated release family = RETAINED_UNVALIDATED_UNCONSUMED
REF-P7-25-R2 = REJECTED_RELEASE_AUDIT_LEDGER_SHAPE
REF-P7-25 = BLOCKED_ON_R2_OFFLINE_AUDIT_CORRECTION
```

Production classifier、scientific policy 和 release generator 没有被此证据证明失败；
阻塞 owner 是外置 audit adapter。

## 4. Executor-local bootstrap checks finding

ER 报告在 source 持久化之前发生过两个 Executor-local bootstrap 检查，二者因额外断言/
模板锚点退出；当时 fresh roots absent，且没有持久化、compile、exec、qualification 或
release generation。

Planner 裁决：

```text
finding = NONCOMPLIANT_UNLEDGERED_PREFLIGHT_VARIANCE
qualification/release budget consumed by these checks = 0
second persisted controller = 0
scientific/device impact = 0
```

它们不是第二次 qualification 或第二个已持久化 controller，也不改变三 artifact 的
retained provenance；但 active PLAN 已把 source build、controller lifecycle 与其 evidence
规定为单一 owner/cap。未持久化的模板/断言执行无法由 canonical evidence 独立重放，不能被
追认成合规的 PLAN preflight，也不能以“fresh roots absent”替代 lifecycle accounting。
因此 R2 即使没有 ledger-shape 崩溃，也不能据此直接验收。下一包明确禁止任何未持久化
bootstrap/controller smoke check，并要求先持久化唯一 source/identity 后才 compile/exec。

## 5. Branch decision

不重新生成 release。理由：

1. Production qualification 已成功执行一次；
2. exact three-artifact family 已完整保留且 hashes 已冻结；
3. failure 在外置 audit consumer 的 row-shape adapter；
4. release generation retry 会降低 provenance 清晰度且没有修复根因的必要。

下一包只读验证 retained artifacts：在独立 fresh correction root 中，使用唯一持久化
schema-aware audit controller，验证 dict row schema、path 排序/唯一性、classification
与 release internal references；随后运行尚未消费的 public validator、fake consumer、
final audit 与 strict audit。Retained R2 package 与 release artifacts 必须 before/after
byte-identical，不能回填缺失的 `05`–`10` 文件。

## 6. Residual risks and locks

- Retained release remains unvalidated and unconsumed until the corrective package passes Planner review.
- Existing release must not be consumed, copied as authority, edited, regenerated or retried.
- Device/network/DNS/.env/camera/Ray/strip/capture/formal/public analyzer/TD-C remain locked.
- No production/test/config/docs/skill/wrapper change or Git commit is authorized.

## 7. Next branch

```text
next reference task = REF-P7-25-R2-C1
next contract =
  P7-TD-B-RETAINED-R3-RELEASE-AUDIT-ADAPTER-C1
single action =
  validate retained exact three-artifact family with one schema-aware
  external audit controller in a fresh offline evidence root
Planner stop = mandatory after terminal seal
Advisor/Human decision = not required
```

## 8. 维护性判断

问题局限在外置 release-audit adapter 对 ledger row shape 的旧假设。下一包复用 production
public validator 与既有 fake-consumer seam，只新增一次性 schema-aware evidence owner，
不修改 production classifier 或引入平行 release generator；无需架构重构。
