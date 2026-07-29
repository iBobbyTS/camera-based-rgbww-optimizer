# REF-P7-25-R2-B1A-C1 / Focused-launch hard-failure review

**Planner 日期：** 2026-07-29

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C1-FAILFAST-ACQUISITION-V1`

**Decision：**
`ACCEPTED_HARD_FAILURE_WITH_CANDIDATE_CARRY_FORWARD_REJECTED_FOR_COMMIT_OR_SEAL`

## 1. Reviewed evidence

```text
reviewed PLAN SHA-256 =
  2d719972eac7b22cd3aea01eb9b8621bb31358b7d45df31940fd4d1cbbb7f13b
C1 root =
  /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-retained-r3-option-b-b1a-c1-offline/20260729T165352Z
validation SHA-256 =
  2e5430c4adee245d074e67c0af38a99e8481fa7f8bfc20ab52fefd124ff08b5f
terminal SHA-256 =
  46a9af0b5799b6e604d12e561f394ced9bd6eda35676879221858e151f05e0a0
EXECUTION_RESULT.md after append SHA-256 =
  701a782b340d585421a6aa75a8718c2c48b9b9e4761b41bf4ab2ed0b9e7e9e45
```

Planner独立验证：top-level JSON `15/15` strict duplicate-key/non-finite parse；terminal preceding ledger `17/17`
逐项path/name/bytes/mode/nlink/SHA匹配；top-level file set恰为17 preceding + terminal。Validation/terminal bytes、mode0600、
nlink1与hash exact。

## 2. Accepted execution results

C1已关闭前一包lifecycle defect：

- single Python acquisition owner、timestamp mkdir、local clone、detached checkout均恰好1；
- preclone barrier在clone前持久化；synthetic preclone failure matrix证明clone/checkout0/0；
- clean-room HEAD=`9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`、tree=
  `c67473c6c8b4fbf799f9e74cd71f89493e18ce4d`；
- source materialization及exact-five candidate完成，staged paths=0；
- CodeGraph 1次，bounded lines1140/1200；single owner/no-generic static gate、`git diff --check`均pass；
- compileall仅对三production owners运行1次并pass；evidence SHA
  `73b082c83d633de131fd93677123aaadb3139fd4e443ed72ec396fed7c15f6d0`；
- shared pre/post在ER append前相等，shared HEAD/index/source未被C1修改。

## 3. Failure and test-credit decision

Focused controller冻结了不存在的
`/Users/ibobby/Projects/WLED-RGBWW/.venv/bin/pytest`。一次subprocess launch attempt在child process启动前抛出
`FileNotFoundError`：pytest processes、tests collected/executed/passed/failed均0。Focused evidence SHA：
`411ddfb456a6b70ad11cf23949065488a64758f7297998989661322e7d1ece2c`。

Planner另独立确认：

```text
shared .venv/bin/pytest = absent
shared .venv/bin/python importlib.find_spec("pytest") = None
stdlib unittest loader = present
```

所以不能把纠正描述成`python -m pytest`。Focused credit=`0`，full=`0`。Full/precommit/stage/commit/manifest/R3
metadata/content/canonical verifier均未运行。

同一shared Python的editable import在未显式设置clean-room source identity时会解析到shared repository的三个production
owners。C2必须以new clean-room/src为leading PYTHONPATH，并在任何test credit前验证三个resolved `__file__`都属于new
clean-room；否则可能测试错误代码。

## 4. Frozen C1 candidate

C1 clean-room只读candidate exact paths/bytes/SHA：

```text
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
  bytes 188631
  SHA-256 33756700bf68841cad039e726f46abe62485e319964abb723499b1ee4cebaea3
src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py
  bytes 42164
  SHA-256 48c0c57fb95c08205c3fef7b23e6df3729928352cd23e1722e8693b9f3634cf8
src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py
  bytes 194497
  SHA-256 7b5b07568f452447faf645f69b7a02482d095284daab44f6fd87ddf5a189fd29
tests/test_p7_retained_release_audit.py
  bytes 30841
  SHA-256 c8d6c7c99815d823871ecfddce79eadd5d5def918affbcd7e4ce86de691d1b3f
tests/test_p7_thermal_diagnostics.py
  bytes 207330
  SHA-256 a126c60d97d0cb19eb96ce1665da357e69cdad2650a68a89ed129f93d25d9da7
```

Against parent `9303aa2`, exact sorted-five canonical patch算法
`git diff --binary --full-index <parent> -- <five sorted paths>`的SHA-256为：
`775b07fecfd65ba278ee174d4ae64772e8b2cfc83d794b6c89c259f4b8eadee0`。

Candidate numstat：

```text
+2/-0   measure_p7_thermal_diagnostics.py
+186/-33 p7_retained_release_audit.py
+342/-1 p7_thermal_diagnostics.py
+159/-0 test_p7_retained_release_audit.py
+228/-0 test_p7_thermal_diagnostics.py
```

这五个bytes与patch作为C2唯一carry-forward source接受，但C1 root本身必须immutable；C2不得在旧root运行Git、Python、
tests或任何实现，也不得修改、stage、commit、seal或same-root rerun。C2只能各读取一次exact candidate file并在new clone
materialize；若new clone重算任一file/patch不同或需要edit，立即fail。

## 5. Preserved zero facts and next branch

Tests/process、full、stage、commit、manifest、canonical verifier、original R3 metadata/content/semantic、helper real audit、
eligibility、consumer、replay、release、network、DNS、`.env`、device、camera、Ray、strip、cleanup、capture、analyzer、FORMAL、
firmware、deployment均0。R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

下一分支`REF-P7-25-R2-B1A-C2`使用fresh root与single fail-fast owner，carry forward上述exact candidate；focused/full改用
stdlib unittest，且test process env的leading PYTHONPATH必须为new clean-room/src。无Advisor或Human gate。

