# P7 FORMAL-R5 hard-failure Planner review

**Review date：** 2026-07-27

**Reference task：** `REF-P7-04`

**Reviewed PLAN contract：** `P7-TD-B-RAY-PUBLIC-DEFAULT-FORMAL-R5`

**Reviewed PLAN SHA-256：** `8e083d2f5ed291e39a972627d6a2c72df5770b60dfa5df3e5eea872d007f41cb`

**FULL_PLAN_REFERENCE SHA-256：** `010dd77e9223ff8a22cf0b9e1f98872c0386f20a9dfdd95455814f4185c0c167`

**EXECUTION_RESULT §132 SHA-256：** `cc4627828f97d41951945561bf82a22c491693eb9e894957d9964da08d4f1ff9`

## Evidence reviewed

- Exact run root：`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-r5/formal-r5-1e3b107-20260726T220000Z`。
- Launch was consumed exactly once (`1/1`), retry `0`; Ray wrapper and child both exited `1`, with terminal decision
  `rejected_fail_closed` and terminal seal present. PID/process chain is empty.
- `ray-formal/failure.json` SHA-256 `2984ec745f2b7cddad1549535b730ae75397cdf7f1fa8602f71010f6613a9a65` records
  `HsiRejectedFeaturesError`, message `2 required HSI observer features were rejected`, capture `011-ray-c-t60`,
  `rejection_stage=post_return_processing`; rejected CR3/sidecar path, bytes, SHA-256, remote capture ID, remote request ID and
  `sidecar_validation_status=pass` are retained.
- `ray-formal/run.json` SHA-256 `dfba25366d6deb093170ceb21ee2fa259143f0da4ba0628216de0d6f23f03079` reports
  `completed_formal=11`, `accepted_formal_count=11`, `ambient=0`, `physical_cr3_count=14` (`setup=2`, `returned=12`), status `failed`.
- `physical-returns.jsonl` SHA-256 `d6569f121c7a31ac1dfb427fe2de1dccc8b46fe3be6e4f3d7ba007d8019e6e02` contains 12 returned CR3 records;
  all 12 CR3/sidecar files are present and all remote IDs/hash/sidecar validation fields pass. No NPY or `analysis.json` exists.
- Python cleanup SHA-256 `982cee95d59cc18ae1270fdc02f3c8947008796593fa22deb07f925ebd5327dc`; shell cleanup SHA-256
  `3c4ea47739e009cef740791e86195f8e76ec8ddb805b3a937efee75c01cf3381`; terminal audit SHA-256
  `4bee490fa83bad33830cf5e8941ccc7fa0ca83191903639c617af5fe9d5e7d79`; returned summary SHA-256
  `5e97023d84d91f0037b096bf84e1102a8b786aa174a383b65087669fb5401955`; progressive/stage-terminal seal SHA-256
  `2a450ee2014fd566415775dfcad40841c4ffd4b7d20e9cf4cd6ca869b7e24ff6`。
- Strip wrapper, strip capture, paired finalizer, public analyzer, independent final-zero, retry and additional cleanup were all `0`.

## Planner finding and decision

**Classification：** `accepted_hard_failed_formal_attempt`。

This is a valid hard failure after physical return, not a formal acceptance. The Ray quality/observer gate rejected two required features; the
11 accepted formal frames cannot be silently promoted to the required 16. Cleanup and physical evidence are sound, but they do not repair the
scientific quality failure. The run cannot unlock strip or TD-B scientific review as a passing formal result.

The applicable GUIDE requires stopping on quality/measurement failure, forbids automatic reshoot, threshold relaxation, feature deletion and
compensating analyzer paths, and requires Advisor involvement when the scientific branch is not determined. It does not specify whether these
two low-signal observer-feature rejections permit a targeted repeat, an exposure/observer strategy change, or a stop route. The existing FULL
reference likewise preserves the hard-failure/no-retry rule but does not choose among those low-signal strategies.

**Result:** no offline code correction is justified and no device retry is authorized. Preserve all 12 returned physical records and stop at an
Advisor scientific decision gate.

## Exact next branch

The next active PLAN must only assemble the retained evidence and submit a bounded Advisor decision request covering:

1. whether `011-ray-c-t60` and the second rejected observer feature represent an invalid formal attempt or a scientifically interpretable partial;
2. whether any targeted repeat is allowed, and if so the exact feature gate, exposure/observer change, capture IDs, new root, physical budget,
   retry count and cleanup contract;
3. whether changing observer features, thresholds, exposure envelope, covariance, statistic or quality semantics requires a new GUIDE,
   checkpoint and lineage release;
4. if no repeat is justified, the exact stop/hold route and treatment of the retained 11 accepted frames.

Until Advisor answers and Planner writes a new exact executable PLAN: no reshoot, no public analyzer, no strip, no release regeneration/consumption,
no formal retry, no threshold/feature/exposure edits, no commit and no TD-C/sentinel entry.

维护性判断：本轮仅完成终态证据审计与科学分支封锁；生产 owners、sidecar ledger、cleanup和terminal seal均无需重构。
