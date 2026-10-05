

def validate_direct_guide12_w122_post_capture(
    run_root: str | Path,
    plan: Mapping[str, Any],
    runtime_evidence: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Validate one GUIDE12 W12-2 LUT verification batch.

    Self-contained structural contract: capture and physical order against
    the frozen plan, formal count, verified source isolation on every frame
    (Ray-zero before strip frames, strip-zero before Ray frames), strip
    commands byte-identical to the frozen LUT, and a per-frame direct-quality
    histogram. Scientific E evaluation against the W12 tolerances belongs to
    the offline verification analyzer, not this gate.
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
        raise ValueError("GUIDE12 W12-2 capture order differs from its frozen plan")
    if [str(row.get("capture_id")) for row in physical] != expected_ids:
        raise ValueError("GUIDE12 W12-2 physical order differs from its frozen plan")
    formal_count = sum(bool(row.get("formal_measurement")) for row in captures)
    if formal_count != int(plan["budgets"]["formal_cap"]):
        raise ValueError("GUIDE12 W12-2 formal count differs from its spec")
    plan_by_id = {str(step["capture_id"]): step for step in plan["captures"]}
    quality_status: dict[str, int] = {}
    strip_frames = ray_frames = 0
    for row in captures:
        step = plan_by_id.get(str(row.get("capture_id")))
        if step is None or row.get("plan_step") != step:
            raise ValueError("GUIDE12 W12-2 capture set differs from its frozen plan")
        capture = row.get("capture")
        if not isinstance(capture, Mapping):
            raise ValueError(
                f"GUIDE12 W12-2 capture lacks its payload: {row.get('capture_id')}"
            )
        if str(row.get("run_root", str(root))) != str(root):
            raise ValueError("GUIDE12 W12-2 artifact crossed its run root")
        direct_quality = capture.get("direct_quality")
        status = (
            str(direct_quality.get("status")) if isinstance(direct_quality, Mapping)
            else "missing"
        )
        quality_status[status] = quality_status.get(status, 0) + 1
        if status not in ("pass", "near_noise_only", "rejected", "missing"):
            raise ValueError(
                f"GUIDE12 W12-2 unexpected direct-quality status: {status}"
            )
        source = str(step["source_id"])
        if source == "strip":
            strip_frames += 1
            ray_zero = capture.get("ray_zero_before_capture")
            ray_data = (
                ray_zero.get("data")
                or ((ray_zero.get("response") or {}).get("data"))
                if isinstance(ray_zero, Mapping) else None
            )
            if not isinstance(ray_data, Mapping) or int(ray_data.get("intensity", -1)) != 0:
                raise ValueError(
                    "GUIDE12 W12-2 strip frame lacks verified Ray-zero evidence: "
                    f"{step['capture_id']}"
                )
            readback = capture.get("strip_command_readback")
            observed = (
                readback.get("device_snapshot")
                if isinstance(readback, Mapping) else None
            ) or (row.get("applied", {}).get("device_snapshot")
                  if isinstance(row.get("applied"), Mapping) else None)
            if isinstance(observed, Mapping):
                requested = step["command"]
                for channel in ("red", "green", "blue", "warm_white", "cold_white"):
                    if int(observed.get(channel, -1)) != int(
                        requested["r" if channel == "red" else
                                   "g" if channel == "green" else
                                   "b" if channel == "blue" else
                                   "ww" if channel == "warm_white" else "cw"]
                    ):
                        raise ValueError(
                            "GUIDE12 W12-2 strip readback differs from the frozen "
                            f"LUT command: {step['capture_id']}"
                        )
        elif source == "ray":
            ray_frames += 1
            strip_zero = capture.get("strip_zero_before_capture")
            observed_zero = (
                strip_zero.get("device_snapshot") if isinstance(strip_zero, Mapping) else None
            )
            if (
                not isinstance(observed_zero, Mapping)
                or any(int(observed_zero.get(key, -1)) != 0 for key in esphome.PAYLOAD_CHANNELS)
            ):
                raise ValueError(
                    "GUIDE12 W12-2 Ray frame lacks verified strip-zero evidence: "
                    f"{step['capture_id']}"
                )
        else:
            raise ValueError(
                f"GUIDE12 W12-2 unexpected source: {step['capture_id']}"
            )
    quality = {
        "schema": "guide12_w122_verification_quality_v1",
        "status": "pass",
        "frames": len(captures),
        "formal_frames": formal_count,
        "direct_quality_histogram": quality_status,
        "strip_frames": strip_frames,
        "ray_frames": ray_frames,
        "guide_experiment_id": plan.get("guide_experiment_id"),
    }
    _write_json(root / "quality.json", quality)
    return quality
