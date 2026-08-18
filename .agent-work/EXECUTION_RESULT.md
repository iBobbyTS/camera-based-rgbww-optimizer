# GUIDE6 evidence correction — no device execution

## Disposition

- `device_health = normal`
- `historical_183_8_strip_baseline = invalid_cross_source_contamination`
- `old_two_guide6_roots = historical_only_not_scientific_input`
- `current_F1 = strip_reference_unobservable_under_unqualified_historical_shutter`
- `human_physical_gate = resolved`
- `science_delta = none`
- `next_branch = GUIDE6_S_MEASUREMENT_strip_exposure_qualification`

The two retained roots and their original analysis artifacts were not modified or
deleted. Their strip candidate capture lacks capture-level Ray-zero evidence and
matches isolated Ray H120/S100, so the legacy
`repeatable_target_local_seed_mismatch` conclusion is disabled.

The current device-health evidence remains the isolated five-channel/Ray baseline
documented at commit `99730c4`. It establishes same-source device health and
cross-source color-shape context only; it does not assert absolute-brightness
matching between Ray and strip.

The next direct spec is prepared but no light, camera, solver, probe or device
operation was started in this correction batch.
