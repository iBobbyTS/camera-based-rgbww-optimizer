"""GUIDE12 C12-2 block analyzer (offline, frozen).

Reads one or more C12-2 solving-block run roots for a single request,
recomputes block_06 z = (ln(R/G), ln(B/G)) per frame, and produces:

- per candidate: dz = z_strip - z_reference (reference = same-target Ray
  HSI bracket mean) plus the bracket drift check;
- probe secants: per-channel dz slopes from single-axis probes against
  the same-block base repeat (plateau/near-noise frames never feed
  slopes - only quality-pass base/probe pairs are used);
- a proposed next-block candidate from the frozen z face step on the
  current best command (box-constrained, face pinned, projected to true
  fullscale by the caller-side rule encoded here: winner to 4095);
- the request budget ledger: new unique commands used (cap 8, 12 only
  with measured improvement), distinct faces used, confirmations banked
  toward the required 3;
- the S0 gate evaluation (|dz| <= 0.01 per log ratio). Color requests
  report dz directly; the Hue/SAT product conversion belongs to the
  campaign-level result analyzer with its local-Jacobian uncertainty.

Usage:
  python tmp/analyze_c12_2_block_20261009.py <run_root> [<run_root> ...]
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from camera_based_rgbww_optimizer.optimization import guide12_c122

TOL_S0 = 0.01
FULLSCALE = 4095
CHANNELS = guide12_c122.CHANNELS


def z_of(run_root: Path, capture_id: str) -> tuple[float, float]:
    stats = json.loads(
        (run_root / "measurements" / f"{capture_id}.patch-statistics.json").read_text(
            encoding="utf-8"
        )
    )
    block = next(p for p in stats["patches"] if p.get("index") == 6)
    planes = {
        plane: float(
            block["planes"][plane]["statistics"]["normalized_per_second"]["trimmed_mean"]
        )
        for plane in ("R", "G1", "G2", "B")
    }
    g = 0.5 * (planes["G1"] + planes["G2"])
    return (math.log(planes["R"] / g), math.log(planes["B"] / g))


def project_fullscale(command: dict[str, int]) -> dict[str, int]:
    peak = max(command.values())
    if peak <= 0:
        raise ValueError("cannot project a zero command")
    scaled = {ch: int(round(v * FULLSCALE / peak)) for ch, v in command.items()}
    winner = max(scaled, key=lambda ch: scaled[ch])
    scaled[winner] = FULLSCALE
    return scaled


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    request = None
    blocks: list[dict] = []
    for arg in argv[1:]:
        root = Path(arg)
        rows = [
            json.loads(line)
            for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        block_rows = []
        for row in rows:
            step = row["plan_step"]
            if "c122_request" not in step:
                continue
            if request is None:
                request = str(step["c122_request"])
            elif str(step["c122_request"]) != request:
                raise SystemExit("all run roots must belong to one C12-2 request")
            quality = (row.get("capture", {}).get("direct_quality") or {}).get("status")
            block_rows.append({
                "run": root.name,
                "tag": str(step.get("c122_tag") or ""),
                "source": str(step["source_id"]),
                "role": str(step["role"]),
                "block": int(step["c122_block"]),
                "command": step.get("command"),
                "new_unique": step.get("c122_new_unique"),
                "face": tuple(step.get("c122_face_channels") or ()),
                "probe_channel": (
                    row.get("candidate_probe_channel")
                    or step.get("candidate_probe_channel")
                    or (step.get("probe_channel"))),
                "quality": quality,
                "z": z_of(root, str(row["capture_id"])),
            })
        blocks.append({"root": str(root), "rows": block_rows})

    hue, sat = (int(x) for x in request.split("/"))
    print(f"request H{hue}/S{sat}, blocks: {[b['root'] for b in blocks]}")

    unique_commands: set[str] = set()
    faces_used: set[tuple[str, ...]] = set()
    confirmations: dict[str, int] = {}
    best = None  # (|dz| worst component, command, dz, face, run, tag)
    secants: dict[str, dict[str, float]] = {"z_r": {}, "z_b": {}}
    for block in blocks:
        rows = block["rows"]
        refs = [r for r in rows if r["source"] == "ray" and r["quality"] == "pass"]
        if len(refs) < 2:
            print(f"  !! {block['root']}: incomplete Ray bracket")
            continue
        before, after = refs[0], refs[-1]
        drift = (after["z"][0] - before["z"][0], after["z"][1] - before["z"][1])
        ref = ((before["z"][0] + after["z"][0]) / 2, (before["z"][1] + after["z"][1]) / 2)
        print(f"  block {rows[0]['block']} ({block['root']}): bracket drift "
              f"dz=({drift[0]:+.5f}, {drift[1]:+.5f})")
        base_z = None
        base_cmd = None
        block_rows = [r for r in rows if r["source"] == "strip"]
        for r in block_rows:
            if r["quality"] != "pass":
                print(f"    {r['tag']:16s} quality={r['quality']} (excluded from slopes)")
                continue
            dz = (r["z"][0] - ref[0], r["z"][1] - ref[1])
            cmd_key = json.dumps(r["command"], sort_keys=True)
            if r["new_unique"]:
                unique_commands.add(cmd_key)
            if r["face"]:
                faces_used.add(tuple(r["face"]))
            worst = max(abs(dz[0]), abs(dz[1]))
            print(f"    {r['tag']:16s} dz=({dz[0]:+.5f}, {dz[1]:+.5f}) worst={worst:.5f}")
            if r["role"] == "base_repeat" or r["tag"] == "u0_repeat":
                base_z, base_cmd = r["z"], dict(r["command"])
                confirmations[cmd_key] = confirmations.get(cmd_key, 0)
            if r["role"] == "confirmation":
                confirmations[cmd_key] = confirmations.get(cmd_key, 0) + 1
            if best is None or worst < best[0]:
                best = (worst, dict(r["command"]), dz, r["face"], block["root"], r["tag"])
        # probe secants vs same-block base
        probes = [
            r for r in block_rows
            if r["quality"] == "pass" and r["role"] == "single_axis_probe"
            and r.get("probe_channel") and base_z is not None
        ]
        for r in probes:
            ch = str(r["probe_channel"])
            base_val = int(base_cmd[ch])
            step_codes = int(r["command"][ch]) - base_val
            if step_codes == 0:
                continue
            for i, name in enumerate(("z_r", "z_b")):
                slope = (r["z"][i] - base_z[i]) / step_codes
                secants[name][ch] = slope
            print(f"    secant {ch}: step {step_codes:+d} -> "
                  f"dz/dcode=({(r['z'][0]-base_z[0])/step_codes:+.6f}, "
                  f"{(r['z'][1]-base_z[1])/step_codes:+.6f})")

    print(f"ledger: unique={len(unique_commands)}/{guide12_c122.C122_UNIQUE_COMMAND_CAP}"
          f" (expand to {guide12_c122.C122_UNIQUE_COMMAND_CAP_EXPANDED} on measured"
          f" improvement), faces={sorted(faces_used)} "
          f"(cap {guide12_c122.C122_FACE_CAP}), "
          f"confirmations={sum(confirmations.values())} "
          f"(need {guide12_c122.C122_CONFIRMATIONS_REQUIRED})")
    if best is None:
        print("no quality-pass strip candidate yet")
        return 0
    worst, command, dz, face, run, tag = best
    print(f"best: {tag} from {run}: worst |dz|={worst:.5f} command={command}")
    if sat == 0:
        gate = worst <= TOL_S0
        print(f"S0 gate |dz|<=0.01: {'PASS' if gate else 'FAIL'}")
    if len(secants["z_r"]) >= 1 or len(secants["z_b"]) >= 1:
        sensitivity = {
            name: {
                ch: slopes.get(ch, 0.0)
                for ch in CHANNELS
            }
            for name, slopes in secants.items()
        }
        try:
            step = guide12_c122.solve_guide12_c122_face_step(
                command, {"z_r": dz[0], "z_b": dz[1]}, sensitivity,
                face_channels=face, sat=sat,
            )
        except ValueError as exc:
            print(f"step not available: {exc}")
            return 0
        proposed = project_fullscale(step["command"])
        print(f"proposed next candidate: {proposed}")
        print(f"  predicted normalized error: {step['predicted_error_normalized']}"
              f" E={step['predicted_E']:.3f}")
        out = {
            "request": request,
            "best_command": command,
            "best_dz": dz,
            "proposed_next": proposed,
            "predicted": step["predicted_error_normalized"],
            "ledger": {
                "unique_commands": len(unique_commands),
                "faces": sorted(faces_used),
                "confirmations": sum(confirmations.values()),
            },
        }
        Path("D:/rgbww-optimizer/guide12-c122/derived").mkdir(
            parents=True, exist_ok=True)
        target = Path("D:/rgbww-optimizer/guide12-c122/derived/"
                      f"c122-next-{request.replace('/', '-')}.json")
        target.write_text(json.dumps(out, indent=1, ensure_ascii=False),
                          encoding="utf-8")
        print(f"written: {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
