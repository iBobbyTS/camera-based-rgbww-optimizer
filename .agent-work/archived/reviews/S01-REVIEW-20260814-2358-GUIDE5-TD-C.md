# S01 review — TD-C core corrected contrasts

- scope：source-specific covariance、source-level null Monte Carlo、immutable derived CLI。
- initial：生产计算无数学 blocker；发现 CLI immutability 与 MC path 两项行为证据缺口。
- repair：新增旧 helper fail-on-call 测试、合理 guard/absolute diagnostic 断言，以及
  temp-copy CLI one-shot/legacy bytes/derived bytes immutability 测试。
- checks：2 targeted tests pass；`tests.test_p7_direct_r6` 25 tests pass（repair 前，
  repair 后 targeted覆盖新增路径）。
- final：`CLEAN`；没有 S02、solver 或额外科学范围扩张。
