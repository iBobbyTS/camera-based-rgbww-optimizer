# S01 Contract — Seed-negative immutable reclassification

- Feature: `guide6-h120-s100-local-controllability-v1`
- Section base: `3e81a3202b091c19c7109638ca9087a9fb60f1a3`
- Outcome: derive the exact two-root `repeatable_target_local_seed_mismatch` disposition without modifying legacy analyses.
- Authority: Advisor decision REQ-001 and exact fixture values in `.agent-work/PLAN-FULL.md`.
- Allowed edits: analyzer local derived function/CLI, `tests/test_p7_direct_r6.py`, current feature artifacts.
- Inspect-only: two exact retained roots and frozen policy.
- Excluded: device execution, solver implementation, feature/covariance/threshold changes, legacy mutation, new framework.
- Acceptance: exact roots/SHA/hash/scores/brackets; zero probes/solver candidates/confirmations; one candidate; immutable output; legacy bytes unchanged.
- Review: `BOUNDED`, assurance `ONE`.
- Targeted test: `tests.test_p7_direct_r6.DirectR6Tests.test_guide6_seed_negative_derivation_is_exact_and_immutable`.
- Reset triggers: scientific estimand/covariance/feature or legacy semantics change.
