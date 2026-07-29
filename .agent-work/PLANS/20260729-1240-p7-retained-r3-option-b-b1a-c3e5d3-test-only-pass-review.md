# REF-P7-25-R2-B1A-C3E5D3 / Test-only correction pass review

**Planner 日期：** 2026-07-29

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E5D3-LINEAGE-TEST-OWNER-V1`

**Decision：**
`ACCEPTED_TEST_ONLY_CORRECTION_REQUIRES_NEW_EXACT_CANDIDATE_FREEZE`

## 1. Frozen evidence

```text
root = /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-retained-r3-option-b-b1a-c3e5d3-offline/20260729T183511Z
lineage-owner-diagnostic.json SHA-256 =
  5f2134eeb9f2a3197d9c6ecba986f76f5221dc99a94239c964ff29b01a69161d
targeted-summary.json SHA-256 =
  3debf6feddc0509078aba9b315c2807e3081e9bff1420841339d761e63680973
focused-summary.json SHA-256 =
  79eba7a0e3bab63459874b8e74222086887af8e0e74e5b97bd97621170f97468
validation-summary.json SHA-256 =
  66b0b6845122929de4cf5e52af80f45e8507a2ab914ed1eeeef87ae903c1cc3d
terminal-summary.json SHA-256 =
  b12a92e318b3842f1e23f4dbb1e1b28a367e6d888cd4c911f64dbf0c79c58f15
EXECUTION_RESULT.md §61 SHA-256 =
  bb4d34856bc2cf2e524b0fbf87a4b19135038e52f829a62e16506902b7e61e69
reviewed PLAN SHA-256 =
  7bee332612dadb7e275831914195df5162e063e46102b0731a1858b54a5cd106
HEAD = 9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
staged paths = 0
```

Lineage diagnostic明确使用existing owners：old `9c804ab...`、new `161094f...`、derived path set 59、prohibited empty；
`ambient_head_used=false`、`hardcoded_path_count_used=false`。Targeted 2/2与focused 102/102通过。Production edit、full、stage、commit、
manifest、R3、device与network均0。

Final test file：

```text
tests/test_p7_thermal_diagnostics.py
bytes = 207433
SHA-256 = d8f65ba9a0dea0cc2c699afd913bddda276912e4c0bb1af3194756f2e02ee97c
```

## 2. New exact candidate

C3E5D3是validated test-only correction candidate，不是old five-path candidate的commit credit。旧candidate SHA
`5b9408f2...468c2`绑定旧test hash `a126c60d...9da7`，现已superseded，禁止直接用于commit或manifest。

Planner独立把原四个unchanged exact files与C3E5D3 final test合并，在同一parent、同一sorted five paths上重算：

```text
git diff --binary --full-index 9303aa22... -- <five sorted paths>
bytes = 53230
SHA-256 = 7b71f9db1ef5a56c6065a255f35b34e9ca7d625699ff31a07cfa7fadb1f75f35
new canonical candidate object SHA-256 =
  3c5847fcbe0af85833c901f6f01058d000a3cecdc0f84e6ae331ed24e138c225
```

New candidate path set仍恰好五路径；前四路径从C1 immutable source读取，final test从C3E5D3 immutable cleanroom读取。每个path
source、bytes、SHA、category/scope均由new canonical object唯一拥有。旧candidate只作为superseded identity，不得混用其patch/test hash。

## 3. Successor

下一包必须从new candidate object逐path evidence-before-compare materialize一个fresh cleanroom；运行focused与full unittest各一次；全部
通过后只创建一个direct child commit，并写一个immutable subordinate exact provenance manifest。Manifest绑定new child/parent、exact
five paths、before/after blob OIDs、new full-index patch、new per-file identities、original R3 three hashes、validation-only scope与rollback
`32b9e67`。

Canonical validator仍是sole eligibility owner。本包只允许subordinate seal，不运行real retained-R3 audit、eligibility emission或release
consumption。失败retry0并停Planner。无Advisor/Human gate。

建议FULL将C3E5D3标记accepted test-only pass，并只激活绑定new candidate SHA的successor；旧candidate标记superseded，checkpoint、release与
`RETAINED_UNVALIDATED_UNCONSUMED`不变。
