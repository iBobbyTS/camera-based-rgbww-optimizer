# GUIDE6 fresh F1 — valid LC-B result

- Root:
  `/Volumes/4T/temp/rgbww-optimizer/guide6-direct-target-local-f1-20260818/20260818-005758-strip-1over400-fresh`
- Captures: 13/13 accepted; Ray 2, strip 11; solver candidates 4;
  confirmations 0.
- All Ray captures used `1/5000`; all strip captures used fixed `1/400`.
- Guard `1/320` was not consumed.
- Classification: `H120_S100_local_controllable_but_not_yet_faithful` (`LC-B`).
- Measurement valid: true; faithful: false; gamut inference: prohibited.
- Ray bracket score/guard: `7.578398793600923 / 9.54298912856529`, pass.
- Strip anchor scores: `4.801721464065255`, `5.015452126809423`, pass.
- Base score: `1471.8684202769587`; best candidate score:
  `1468.2674910054316`.
- Best command: `CW0 / WW0 / R377 / G4095 / B107`.
- Analysis SHA-256:
  `1dd0a994749a41f2b649e64af5c75c46959f1e828599955dc1fc6ae81948e7b5`.
- Cleanup and independent final Ray/strip zero: pass; Git clean.
- `science_delta`: local controllability produced a small repeatable direction of
  improvement, but no candidate met the frozen direct guard.

The first analyzer invocation exposed a Python-direct/wrapper-artifact mismatch.
No analysis was written. The analyzer was corrected to accept an all-Python direct
run only when `run.status=complete`, `run.cleanup=pass`, and every Python cleanup
step is `ok=true`; partial wrapper artifacts still fail closed. The focused behavior
test passed and the same root was analyzed once successfully without reacquisition.

Next: one centered generation-1 continuation under the same scientific contract.
