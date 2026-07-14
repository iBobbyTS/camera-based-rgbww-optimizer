## Active

| file | summary |
| --- | --- |
| active/20260714-p1-raw-black-level-linearity.md | P1 CR3 brackets show a shared fixed raw intercept because CR3 black-level metadata is implausible; validate a black-level fallback offline before another capture. |
| active/20260712-white-lut-repeatability-and-strict-anchors.md | Measure repeatability, validate strict anchors, and explain the cross-day regression of near-boundary 14x5 nodes. |

## Unresolved

| file | summary |
| --- | --- |

## Resolved

| file | summary |
| --- | --- |
| resolved/20260710-white-lut-bounded-feedback-solver.md | Bounded feedback and a ten-round early-stopping budget passed hardware retries for all three previously unmet 14x5 targets. |
| resolved/20260709-white-lut-light-isolation-exposure-cache.md | Formal white LUT now enforces mutually exclusive Ray/strip captures, independent exposure caches, and compensation-channel high-output ownership; isolated 12-point LUT completed. |
| resolved/20260709-location-picker-dcraw-bounds.md | Web UI was still using the linear NPY preview path and could show out-of-bounds automatic detections; picker now uses dcraw visual preview and rejects out-of-bounds results. |
