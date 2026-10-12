"""GUIDE12 final deliverable packager - processed evidence only.

Builds GUIDE12-COMPLETE-PROCESSED-EVIDENCE-20261012.zip per
advisor/12/GUIDE12_DATA_PACKAGE_REQUIREMENTS.md:
- README / FINAL-REPORT / MANIFEST / RUN_INDEX / OBSERVATIONS /
  RAW_INDEX / COMMANDS ledgers assembled from every GUIDE12 run root;
- all per-frame patch statistics (measurements/), the frozen models and
  test vectors (models/), every analysis JSON (results/), the frozen
  implementation and analyzers (source/), frozen config inputs
  (config/), and a replay script that recomputes the key color/white
  numbers from packaged data only (replay/).
Raw CR3 payloads stay on D:/rgbww-optimizer (referenced by hash and
byte count, never copied); credentials and caches are not included.
"""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WORK = REPO / ".agent-work" / "guide12"
DATA = Path("D:/rgbww-optimizer")
OUT_ZIP = WORK / "GUIDE12-COMPLETE-PROCESSED-EVIDENCE-20261012.zip"
DATE = "20261012"

CAMPAIGNS = [
    "guide12-n2", "guide12-c12", "guide12-w12", "guide12-w122",
    "guide12-w123", "guide12-w124", "guide12-c122", "guide12-c124",
]

RESULTS_FILES = [
    DATA / "guide12-n2/derived/n2-repeatability-analysis-20261005.json",
    DATA / "guide12-c12/derived/c12-1-offline-tables-20261005.json",
    DATA / "guide12-c12/derived/c12-1-frozen-targets-20261005.json",
    DATA / "guide12-c12/derived/c12-1-mapping-20261005.json",
    DATA / "guide12-c12/derived/p6-node-brightness.json",
    DATA / "guide12-w122/derived/w12-2-frozen-lut-20261005.json",
    DATA / "guide12-w122/derived/w12-2-verification-analysis.json",
    DATA / "guide12-w122/derived/w122-node-strip-brightness.json",
    DATA / "guide12-w122/derived/w123-strip-shutters-20261008.json",
    DATA / "guide12-w123/derived/w12-3-interpolation-analysis-20261008.json",
    DATA / "guide12-w124/derived/w12-4-order-reverification-analysis-20261009.json",
    DATA / "guide12-c124/derived/c124-adopted-20261012.json",
    DATA / "guide12-c124/derived/c12-4-holdout-analysis-20261012.json",
]

SOURCE_FILES = [
    REPO / "src/camera_based_rgbww_optimizer/optimization/guide12.py",
    REPO / "src/camera_based_rgbww_optimizer/optimization/guide12_n2.py",
    REPO / "src/camera_based_rgbww_optimizer/optimization/guide12_c12.py",
    REPO / "src/camera_based_rgbww_optimizer/optimization/guide12_w123.py",
    REPO / "src/camera_based_rgbww_optimizer/optimization/guide12_w124.py",
    REPO / "src/camera_based_rgbww_optimizer/optimization/guide12_c122.py",
    REPO / "src/camera_based_rgbww_optimizer/optimization/guide12_c124.py",
    REPO / "src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py",
    REPO / "tests/test_guide12_w122.py",
    REPO / "tests/test_guide12_w123.py",
    REPO / "tests/test_guide12_w124.py",
    REPO / "tests/test_guide12_c12.py",
    REPO / "tests/test_guide12_c122.py",
    REPO / "tests/test_guide12_c124.py",
    REPO / "tmp/analyze_guide12_n2_20261005.py",
    REPO / "tmp/analyze_c12_1_mapping_20261005.py",
    REPO / "tmp/analyze_w12_2_20261007.py",
    REPO / "tmp/analyze_w12_3_20261008.py",
    REPO / "tmp/analyze_w12_4_20261009.py",
    REPO / "tmp/analyze_c12_2_block_20261009.py",
    REPO / "tmp/analyze_c12_4_20261012.py",
    REPO / "tmp/build_w12_2_lut_20261005.py",
    REPO / "tmp/run_w124_campaign_20261008.sh",
]

DOC_FILES = sorted(WORK.glob("GUIDE12-*.md"))

CONFIG_FILES = [
    REPO / "config/rgbww-code-duty-curve.json",
    REPO / "config/workflow-local-lab-context.json",
    REPO / ".env.example",
]

# validated samples for the replay check: request -> expected 2D numbers
REPLAY_EXPECTED = {
    "S0": {"command": {"cw": 4095, "ww": 2240, "r": 658, "g": 1681, "b": 1425},
            "mean_dz": [-0.00019, 0.00217]},
    "H0/S50": {"command": {"cw": 282, "ww": 1818, "r": 4095, "g": 180, "b": 480},
               "mean_dz": [-0.0313, 0.0399]},
    "H60/S100": {"command": {"cw": 0, "ww": 0, "r": 4095, "g": 3390, "b": 80},
                 "mean_dz": [0.0076, 0.0008]},
    "H120/S50": {"command": {"cw": 282, "ww": 1818, "r": 368, "g": 4095, "b": 1024},
                 "mean_dz": [0.0005, 0.0023]},
    "H240/S50": {"command": {"cw": 796, "ww": 547, "r": 1031, "g": 2048, "b": 4095},
                 "mean_dz": [0.0021, -0.0014]},
    "H300/S25": {"command": {"cw": 3111, "ww": 4095, "r": 4095, "g": 1804, "b": 4095},
                 "mean_dz": [0.0041, 0.0425]},
}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    run_index = []
    observations = []
    raw_index = []
    commands = []
    manifest = []
    zfiles: list[tuple[str, Path]] = []
    zmem: list[tuple[str, str]] = []

    for campaign in CAMPAIGNS:
        for root in sorted((DATA / campaign).glob("formal-*")):
            cj = root / "captures.jsonl"
            if not cj.exists():
                continue
            runj = {}
            try:
                runj = load(root / "run.json")
            except Exception:
                pass
            alias = f"{campaign}/{root.name}"
            rows = [json.loads(l) for l in cj.read_text(encoding="utf-8").splitlines() if l.strip()]
            phys = []
            pr = root / "physical-returns.jsonl"
            if pr.exists():
                phys = [json.loads(l) for l in pr.read_text(encoding="utf-8").splitlines() if l.strip()]
            cap_count = 0
            for row in rows:
                cap = row.get("capture") or {}
                q = (cap.get("direct_quality") or {}).get("status")
                saved = cap.get("saved_file")
                entry = {
                    "run_alias": alias,
                    "capture_id": str(row.get("capture_id")),
                    "source": row["plan_step"].get("source_id"),
                    "command": row["plan_step"].get("command"),
                    "role": row["plan_step"].get("role"),
                    "guide_tags": {k: v for k, v in row["plan_step"].items()
                                   if k.startswith(("w12", "w122", "w123", "w124",
                                                    "c12", "c124", "target_"))},
                    "nominal_shutter": row["plan_step"].get("nominal_shutter"),
                    "direct_quality": q,
                    "measurement": f"measurements/{alias}/{row.get('capture_id')}.patch-statistics.json",
                }
                observations.append(entry)
                cap_count += 1
            for row in phys:
                cap = row.get("capture") or {}
                raw_index.append({
                    "run_alias": alias,
                    "capture_id": str(row.get("capture_id")),
                    "sha256": cap.get("sha256"),
                    "byte_count": cap.get("byte_count"),
                    "retained_path": cap.get("saved_file"),
                    "note": "raw payload retained on D:/rgbww-optimizer; not packaged",
                })
            cmd_file = root / "commands.jsonl"
            if cmd_file.exists():
                for l in cmd_file.read_text(encoding="utf-8").splitlines():
                    if not l.strip():
                        continue
                    c = json.loads(l)
                    c["run_alias"] = alias
                    commands.append(c)
            run_index.append({
                "run_alias": alias,
                "status": runj.get("status"),
                "started_at": runj.get("started_at"),
                "finished_at": runj.get("finished_at"),
                "git": runj.get("git"),
                "captures": cap_count,
                "cleanup": runj.get("cleanup"),
                "experiment": runj.get("schema"),
                "source_root": str(root),
            })
            # package every patch-statistics file
            for ms in sorted((root / "measurements").glob("*.patch-statistics.json")):
                zfiles.append((f"measurements/{alias}/{ms.name}", ms))

    # ---- ledgers ----
    zmem.append(("OBSERVATIONS.jsonl", "\n".join(json.dumps(o, ensure_ascii=False) for o in observations) + "\n"))
    zmem.append(("RAW_INDEX.jsonl", "\n".join(json.dumps(r, ensure_ascii=False) for r in raw_index) + "\n"))
    zmem.append(("COMMANDS.jsonl", "\n".join(json.dumps(c, ensure_ascii=False) for c in commands) + "\n"))
    zmem.append(("RUN_INDEX.json", json.dumps(run_index, indent=1, ensure_ascii=False)))

    # ---- models ----
    lut = load(DATA / "guide12-w122/derived/w12-2-frozen-lut-20261005.json")
    zmem.append(("models/white-final-lut.json", json.dumps(lut, indent=1)))
    adopted = load(DATA / "guide12-c124/derived/c124-adopted-20261012.json")
    zmem.append(("models/strip-hsi-command-model.json", json.dumps({
        "schema": "strip_hsi_adopted_commands_v1",
        "note": "adopted validated commands; interpolation models NOT adopted (see results)",
        "adopted": adopted,
    }, indent=1)))
    from camera_based_rgbww_optimizer.optimization.guide12_w123 import (
        W123_REQUESTS, interpolate_fullscale_command,
    )
    vectors = {}
    for cct, gm in W123_REQUESTS[:5]:
        vectors[f"{cct}/{gm}"] = interpolate_fullscale_command(lut["nodes"], cct, gm)
    zmem.append(("models/white-runtime-model.json", json.dumps({
        "schema": "white_runtime_interpolation_v1_NOT_ADOPTED",
        "order": "bilinear(mired,gm) -> fullscale projection -> round -> clip",
        "adoption": "not adopted (W12-3 holdout 1/20)",
        "test_vectors": vectors,
    }, indent=1)))
    ray_map = load(DATA / "guide12-c12/derived/c12-1-mapping-20261005.json")
    zmem.append(("models/ray-hsi-map.json", json.dumps({
        "schema": "ray_hsi_map_v1_unqualified_global",
        "note": "global inverse map unqualified; per-target direct references used instead",
        "records": ray_map.get("records"),
        "s0_hue_consistency": ray_map.get("s0_hue_consistency"),
    }, indent=1)))

    # ---- results / source / config / docs ----
    for p in RESULTS_FILES:
        if p.exists():
            zfiles.append((f"results/{p.name}", p))
    for p in SOURCE_FILES:
        if p.exists():
            zfiles.append((f"source/{p.name}", p))
    for p in CONFIG_FILES:
        if p.exists():
            zfiles.append((f"config/{p.name}", p))
    for p in DOC_FILES:
        zfiles.append((f"results/{p.name}", p))

    # ---- replay ----
    replay = '''#!/usr/bin/env python3
"""Recompute key GUIDE12 numbers from packaged data only.

Reads measurements/ + models/ from the package root, recomputes the
adopted-sample dz means for the replay set, and compares them with
results/ expectations. No raw CR3 access.
"""
import json, math, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
expected = json.loads((root / "replay/expected-results.json").read_text(encoding="utf-8"))

def z_of(rel):
    st = json.loads((root / rel).read_text(encoding="utf-8"))
    b = next(p for p in st["patches"] if p.get("index") == 6)
    pl = {k: float(b["planes"][k]["statistics"]["normalized_per_second"]["trimmed_mean"])
          for k in ("R", "G1", "G2", "B")}
    g = 0.5 * (pl["G1"] + pl["G2"])
    return (math.log(pl["R"] / g), math.log(pl["B"] / g))

obs = [json.loads(l) for l in (root / "OBSERVATIONS.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
by_run_strip = {}
for o in obs:
    if o.get("source") == "strip" and o.get("direct_quality") == "pass":
        by_run_strip.setdefault(o["run_alias"], []).append(o)

def ray_ref_mean(run_alias):
    zs = [z_of(o["measurement"]) for o in obs
          if o["run_alias"] == run_alias and o.get("source") == "ray"
          and o.get("direct_quality") == "pass"]
    return ([sum(z[i] for z in zs) / len(zs) for i in (0, 1)]
            if zs else None)

failures = []
for name, spec in expected["adopted_samples"].items():
    cmd = json.dumps(spec["command"], sort_keys=True)
    rows = [o for o in obs if json.dumps(o.get("command"), sort_keys=True) == cmd
            and o.get("direct_quality") == "pass"]
    dzs = []
    for o in rows:
        ref = ray_ref_mean(o["run_alias"])
        if ref is None:
            continue
        z = z_of(o["measurement"])
        dzs.append((z[0] - ref[0], z[1] - ref[1]))
    mean = [sum(d[i] for d in dzs) / len(dzs) for i in (0, 1)]
    ok = all(abs(mean[i] - spec["mean_dz"][i]) <= spec["tol"][i] for i in (0, 1))
    print(f"{name}: n={len(dzs)} mean_dz=({mean[0]:+.5f},{mean[1]:+.5f}) "
          f"expected=({spec['mean_dz'][0]:+.5f},{spec['mean_dz'][1]:+.5f}) {'OK' if ok else 'FAIL'}")
    if not ok or len(dzs) < 3:
        failures.append(name)
print("REPLAY", "PASS" if not failures else f"FAIL: {failures}")
sys.exit(0 if not failures else 1)
'''
    zmem.append(("replay/reproduce.py", replay))
    exp = {"adopted_samples": {}}
    for name, spec in REPLAY_EXPECTED.items():
        exp["adopted_samples"][name] = {**spec, "tol": [0.004, 0.004]}
    zmem.append(("replay/expected-results.json", json.dumps(exp, indent=1)))

    # ---- README / FINAL-REPORT ----
    final_report = """# GUIDE12 FINAL REPORT (2026-10-12)

Stage-complete processed evidence for advisor/12/12.GUIDE.md.

## Headline results
- White LUT: 38/70 nodes verified_qualified at W12 tolerances
  (results/w12-2-verification-analysis.json); 5 gamut-limited corners
  documented; 20000K carries a persistent Ray drift characteristic.
- White runtime interpolation: NOT adopted (W12-3 holdout 1/20,
  results/w12-3-interpolation-analysis-20261008.json).
- FAST/LONG protocol: warm/mid DiD near tolerance, 20000/100
  inseparable (W12-4, results/w12-4-order-reverification-analysis-20261009.json).
- N2 repeatability: three power-separated sessions, excellent
  repeatability, biases quantified (results/n2-repeatability-analysis-*.json).
- Ray HSI true mapping: global inverse map_unqualified; S0 three-session
  consistency |dz|<=0.0021 (results/c12-1-mapping-20261005.json).
- Color solving (C12-2): 8/13 qualified (S0 + all five S50 + H60/S100);
  5 gamut_limited corners (4 radial + 1 tangential lock).
- Coverage (C12-3): 17 validated_samples; no continuous-interval claims;
  6/6 S25 anchors qualified.
- Runtime color model (C12-4): NOT adopted (holdout 2/10); SAT
  monotonicity holds; near-anchor requests (~<=2 deg) stay in gate.
- Closure (C12-5): support ranges / bounded-approximation / measurement
  limits / unqualified-inverse classes delivered in
  results/GUIDE12-C122-RESULT-20261009.md.

## Package layout
See MANIFEST.json. Raw CR3 payloads remain under D:/rgbww-optimizer
(referenced by SHA-256 + byte count in RAW_INDEX.jsonl). Replay:
python replay/reproduce.py (packaged data only).

Generated by tmp/build_guide12_package_20261012.py at repo HEAD recorded
in RUN_INDEX.json entries.
"""
    zmem.append(("FINAL-REPORT.md", final_report))
    readme = """# GUIDE12-COMPLETE-PROCESSED-EVIDENCE-20261012

Processed evidence package for GUIDE12. Contents: ledgers
(OBSERVATIONS/RAW_INDEX/COMMANDS/RUN_INDEX), per-frame patch statistics
(measurements/), frozen models + test vectors (models/), analysis
outputs and stage documents (results/), frozen implementation and
analyzers (source/), config inputs (config/), replay
(replay/reproduce.py). Excludes raw CR3/RAW/DNG payloads (retained on
D:/rgbww-optimizer, hash-referenced), credentials, caches, firmware.
"""
    zmem.append(("README.md", readme))

    # ---- write the zip ----
    with zipfile.ZipFile(OUT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for arc, p in zfiles:
            z.write(p, arc)
            manifest.append({"path": arc, "source": str(p),
                             "byte_count": p.stat().st_size,
                             "sha256": sha(p.read_bytes())})
        for arc, text in zmem:
            data = text.encode("utf-8")
            z.writestr(arc, data)
            manifest.append({"path": arc, "source": "generated",
                             "byte_count": len(data),
                             "sha256": sha(data)})
        man = {
            "schema": "guide12_complete_processed_evidence_manifest_v1",
            "date": DATE,
            "file_count": len(manifest),
            "excludes": ("raw CR3/RAW/DNG, NPY/NPZ, TIFF/JPEG/PNG derivatives, "
                         "decoded arrays, firmware, build output, credentials, caches"),
            "raw_payload_root": "D:/rgbww-optimizer",
            "files": manifest,
        }
        mdata = json.dumps(man, indent=1).encode("utf-8")
        z.writestr("MANIFEST.json", mdata)

    bad = None
    with zipfile.ZipFile(OUT_ZIP) as z:
        bad = z.testzip()
    zip_sha = sha(OUT_ZIP.read_bytes())
    (WORK / "GUIDE12-COMPLETE-PROCESSED-EVIDENCE-20261012-MANIFEST.json").write_text(
        json.dumps({"zip": str(OUT_ZIP), "zip_sha256": zip_sha,
                    "zip_byte_count": OUT_ZIP.stat().st_size,
                    "file_count": len(manifest)}, indent=1) + "\n",
        encoding="utf-8")
    print(f"zip: {OUT_ZIP.name} {OUT_ZIP.stat().st_size} bytes | files: {len(manifest)} "
          f"| integrity: {'FAIL:' + str(bad) if bad else 'ok'}")
    print(f"zip sha256: {zip_sha}")
    print(f"runs: {len(run_index)} | observations: {len(observations)} "
          f"| raw entries: {len(raw_index)} | commands: {len(commands)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
