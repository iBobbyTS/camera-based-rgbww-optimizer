

def validate_direct_guide12_w123_post_capture(
    run_root: str | Path,
    plan: Mapping[str, Any],
    runtime_evidence: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Validate one GUIDE12 W12-3 interpolation holdout run.

    Self-contained structural contract mirroring the W12-2 validator:
    capture/physical order against the frozen plan, formal count, verified
    source isolation per frame, strip readback byte-identical to the frozen
    interpolated command, and a per-frame direct-quality histogram. The
    scientific E evaluation belongs to the offline analyzer.
    """
    root = Path(run_root).resolve()
    expected_ids = [str(step["capture_id"]) for step in plan["captures"]]
    captures = [
        json.loads(line)
        for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    physical = [
        json.loads(line)
        for line in (root / "physical-returns.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if [str(row.get("capture_id")) for row in captures] != expected_ids:
        raise ValueError("GUIDE12 W12-3 capture order differs from its frozen plan")
    if [str(row.get("capture_id")) for row in physical] != expected_ids:
        raise ValueError("GUIDE12 W12-3 physical order differs from its frozen plan")
    formal_count = sum(bool(row.get("formal_measurement")) for row in captures)
    if formal_count != int(plan["budgets"]["formal_cap"]):
        raise ValueError("GUIDE12 W12-3 formal count differs from its spec")
    plan_by_id = {str(step["capture_id"]): step for step in plan["captures"]}
    quality_status: dict[str, int] = {}
    for row in captures:
        step = plan_by_id.get(str(row.get("capture_id")))
        if step is None or row.get("plan_step") != step:
            raise ValueError("GUIDE12 W12-3 capture set differs from its frozen plan")
        capture = row.get("capture")
        if not isinstance(capture, Mapping):
            raise ValueError(
                f"GUIDE12 W12-3 capture lacks its payload: {row.get('capture_id')}"
            )
        if str(row.get("run_root", str(root))) != str(root):
            raise ValueError("GUIDE12 W12-3 artifact crossed its run root")
        direct_quality = capture.get("direct_quality")
        status = (
            str(direct_quality.get("status")) if isinstance(direct_quality, Mapping)
            else "missing"
        )
        quality_status[status] = quality_status.get(status, 0) + 1
        if status not in ("pass", "near_noise_only", "rejected", "missing"):
            raise ValueError(
                f"GUIDE12 W12-3 unexpected direct-quality status: {status}"
            )
        source = str(step["source_id"])
        if source == "strip":
            ray_zero = capture.get("ray_zero_before_capture")
            ray_data = (
                ray_zero.get("data")
                or ((ray_zero.get("response") or {}).get("data"))
                if isinstance(ray_zero, Mapping) else None
            )
            if not isinstance(ray_data, Mapping) or int(ray_data.get("intensity", -1)) != 0:
                raise ValueError(
                    "GUIDE12 W12-3 strip frame lacks verified Ray-zero evidence: "
                    f"{step['capture_id']}"
                )
            if max(int(v) for v in step["command"].values()) != 4095:
                raise ValueError(
                    "GUIDE12 W12-3 strip command is not actual fullscale: "
                    f"{step['capture_id']}"
                )
        elif source == "ray":
            strip_zero = capture.get("strip_zero_before_capture")
            observed_zero = (
                strip_zero.get("device_snapshot") if isinstance(strip_zero, Mapping) else None
            )
            if (
                not isinstance(observed_zero, Mapping)
                or any(int(observed_zero.get(key, -1)) != 0 for key in esphome.PAYLOAD_CHANNELS)
            ):
                raise ValueError(
                    "GUIDE12 W12-3 Ray frame lacks verified strip-zero evidence: "
                    f"{step['capture_id']}"
                )
        else:
            raise ValueError(
                f"GUIDE12 W12-3 unexpected source: {step['capture_id']}"
            )
    quality = {
        "schema": "guide12_w123_interpolation_quality_v1",
        "status": "pass",
        "frames": len(captures),
        "formal_frames": formal_count,
        "direct_quality_histogram": quality_status,
        "guide_experiment_id": plan.get("guide_experiment_id"),
    }
    _write_json(root / "quality.json", quality)
    return quality
