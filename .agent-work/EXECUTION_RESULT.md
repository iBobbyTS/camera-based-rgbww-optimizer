# GUIDE7 H120/S100 F1 — strip reference observation missing

## Classification

- Failure class: `DEVICE_OR_SAFETY_FAILURE` pending physical confirmation.
- Unresolved stop: `HUMAN_GATE_REQUIRED`.
- `science_delta=none`: the intended local-controllability block did not reach
  probes or solver observations.
- Fresh retry: justified only after Human confirms normal physical strip emission
  and an unobstructed chart illumination path.

## Exact evidence

- Run status: failed; `completed_formal=1`, `physical_returned_cr3_count=2`,
  `cleanup=pass`.
- Accepted Ray `Q_before`: 58/58 features at nominal `1/5000`.
- Rejected strip base: nominal `1/1600`, recorded exposure
  `0.000615195825143981 s`, exact logical command
  `CW=518, WW=0, R=0, G=4095, B=0`, hash
  `f70a07889065ad105bf25a9fda103ec2a708ef056f4ae17b0279ef3886b5cfde`.
- Verified physical readback after the code-duty curve:
  `cold_white=481, green=4095, red=0, blue=0, warm_white=0`.
- Current optimization-plane quality: 48 accepted, 44 rejected; 19/58 required
  features missing. Normalized feature range approximately `0.815..83.97 /s`,
  median `10.00 /s`.
- Two accepted same-command roots had all 92 optimization planes accepted and
  normalized ranges approximately `14.77..1190 /s`, median `183.7..183.9 /s`.
- No strip probe, finite-difference Jacobian, solver-generated command, backtrack,
  Broyden update or confirmation was executed.

## Artifact identities

- `run.json`: `f10f4a91947f6cdfea34b66fceff2814a7f551c9eb3b53c74a37b3edfd42bfa3`
- `failure.json`: `fe58105341e8db8df527b5e9ada55e3cced50852aa071bdea9205429b445f8c9`
- Current strip patch report:
  `1c076db0340ffb9d9ba889b285a9f40143a84bc2df596967200cfc2668c181f5`
- Accepted reference-repeat report:
  `4291398ffef04b3118916bd8d9be210ba1a8f6aa25bbe7e579e1c79604e5da10`
- Accepted solver-repeat report:
  `cd4f2f13c17b12c8bd8a139f9bcc850fdc803f819f8778390164d093fcac1557`

Raw CR3 payloads remain only under the retained experiment roots and are not
tracked by Git.
