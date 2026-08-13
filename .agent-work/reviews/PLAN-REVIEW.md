# PLAN review — GUIDE5 TD-C FAST endpoint holdout

- scope：只读复核 S01 corrected contrasts 与 S02 FAST B/C endpoint holdout。
- verdict：`APPROVED_AFTER_BOUNDED_CORRECTION`。
- admitted blocker：S02 原文未冻结 holdout residual 的三项独立 covariance 求和；已补
  `new endpoint mean + core A mean + combined local-coordinate state mean`，并禁止
  用新 endpoint 回填既有模型。
- admitted contract clarification：S01 已明确 `2ΣR`、`2ΣS_A`、
  `2(ΣR+ΣS_A)`、`ΣR+ΣS_A` 与 `(ΣR+ΣS_A)/4`，并要求 source-level MC。
- scope correction：删除双重 review 仪式；更新旧 WAITING_ADVISOR 状态。
- rejected expansion：无新架构、额外实验、legacy expansion 或 solver。
