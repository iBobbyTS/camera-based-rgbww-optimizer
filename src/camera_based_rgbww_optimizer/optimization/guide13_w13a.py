"""GUIDE13 W13-A: bounded white-node correction on the W12-1 machinery.

GUIDE13 W13-A corrects the W12-2 LUT nodes whose verification exceeded
tolerance, reusing the frozen W12-1 measurement contract verbatim (same
block structure: Ray before/after sandwich around base repeat + three
single-axis probes; same box-constrained face-step solver; same
exposure pre-check): the W12-1 owner already implements "local z
constrained step on the shared working face, model proposes, new photos
verify". Only the queue source and the record identity differ.

The block plan is built by build_guide12_w12_block_plan and then carries
the GUIDE13 experiment identity (guide_experiment_id/variant/stage/
source and the authorization experiment_id). The execution schema stays
the frozen W12-1 schema so authorization, isolation, near-noise
classification and post-capture validation semantics are exactly the
ones W12-1 itself ran under.
"""
from __future__ import annotations

from typing import Any, Mapping

from camera_based_rgbww_optimizer.optimization.guide12 import (
    W122_STRIP_SHUTTER_OVERRIDES,
    build_guide12_w12_block_plan,
    guide12_w12_face_channels,
    guide12_w12_probe_candidates,
)

W13A_EXPERIMENT_ID = "GUIDE13_W13_A_WHITE_NODE_CORRECTION_V1"
W13A_VARIANT = "guide13_w13_a_bounded_node_correction_v1"
W13A_STAGE = "GUIDE13-W13-A-NODE-CORRECTION"
W13A_SOURCE = "guide13_w13a_open_queue_20261013"


def w13a_node_from_queue_row(row: Mapping[str, Any]) -> dict[str, Any]:
    """Adapt one W13-A open-queue row to the W12-1 block-plan node shape."""
    command = {k: int(v) for k, v in row["command"].items()}
    e = None
    if row.get("E_max") is not None:
        e = float(row["E_max"])
    return {
        "cct": int(row["node"].split("/")[0]),
        "gm": int(row["node"].split("/")[1]),
        "E_vs_fresh_ray": e,
        "base_command": command,
        "face_channels": guide12_w12_face_channels(command),
        "mean_signed_eK": row.get("mean_signed_eK"),
        "verdict": row.get("verdict"),
    }


def w13a_first_block_candidates(
    row: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """First-block candidates for a queue row: W12-1 frozen probe block
    (base repeat + single-axis probes on the three most-leveraged
    non-face channels)."""
    return guide12_w12_probe_candidates(
        w13a_node_from_queue_row(row)["base_command"])


def w13a_strip_shutter(cct: int, gm: int) -> str | None:
    """Node-level strip shutter override from the frozen W12-2 table
    (bright families measured during verification); None keeps the W12-1
    white-line anchor 1/100."""
    return W122_STRIP_SHUTTER_OVERRIDES.get((cct, gm))


def build_guide13_w13a_block_plan(
    row: Mapping[str, Any],
    candidates: list[dict[str, Any]],
    *,
    block_index: int,
    inputs_references: Mapping[str, Mapping[str, Any]] | None = None,
    predicted_raw_max: Mapping[str, float] | None = None,
    command_budget: Mapping[str, Any] | None = None,
    strip_shutter: str | None = None,
) -> dict[str, Any]:
    """One W13-A correction block: the frozen W12-1 block contract with
    GUIDE13 record identity. ``strip_shutter`` overrides the frozen W12-2
    node table when the offline pre-check trips the raw-max ceiling."""
    from camera_based_rgbww_optimizer.optimization.guide12_w123 import (
        resolve_w123_ray_shutter,
    )

    node = w13a_node_from_queue_row(row)
    cct, gm = node["cct"], node["gm"]
    plan = build_guide12_w12_block_plan(
        node, candidates,
        block_index=block_index,
        inputs_references=inputs_references,
        predicted_raw_max=predicted_raw_max,
        command_budget=command_budget,
        strip_shutter=strip_shutter or w13a_strip_shutter(cct, gm),
        # W12-2 transfer rule for grid nodes outside the W2 anchor table
        ray_shutter=resolve_w123_ray_shutter(cct, gm),
    )
    plan["guide_experiment_id"] = W13A_EXPERIMENT_ID
    plan["variant"] = W13A_VARIANT
    plan["stage"] = W13A_STAGE
    plan["source"] = W13A_SOURCE
    plan["execution_authorization"] = {
        **plan["execution_authorization"],
        "experiment_id": W13A_EXPERIMENT_ID,
    }
    plan["analysis_contract"] = {
        **plan["analysis_contract"],
        "method": "guide13_w13_a_bounded_node_correction_block",
        "w13a_queue_row": {
            "node": row["node"], "verdict": row.get("verdict"),
            "mean_signed_eK": row.get("mean_signed_eK"),
        },
        "budget_rules": (
            "8 new unique commands per open node; extend to 12 only if a "
            "measured improvement matches the direction prediction; at most "
            "2 distinct actual-fullscale faces; <=30 active nodes this stage"
        ),
    }
    return plan
