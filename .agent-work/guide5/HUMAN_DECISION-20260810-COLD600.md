# Human decision — session cold proxy 600 s

On 2026-08-10, Human changed the Ray history experiment's between-session
cold-proxy minimum from 3600 seconds to 600 seconds to reduce elapsed time and
power consumption. Human explicitly accepts the additional thermal error.

This decision applies to the current restart and future similar experiments. It
does not claim cold equilibrium, settling, or steady state. The analysis must
retain the frozen observer, 58 features, uncertainty, covariance, guarded
coverage, exposure, frame selection, and the 120-second operational dwell. The
600-second interval is a protocol minimum selected by Human, not a scientifically
fitted thermal threshold.

The previous OP120 root with Session 1 completed under the 3600-second condition
is preserved as historical evidence and is not pooled with the restarted COLD600
experiment. The restart uses a new experiment identity and a fresh Session 1 so
all three sessions share one cold-proxy contract.

```text
previous cold proxy = 3600 s
current cold proxy = 600 s
operational dwell = 120 s
thermal error = human_accepted
settled_or_steady_claim_allowed = false
decision_owner = Human
```
