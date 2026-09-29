"""GUIDE11 final deliverable packager - processed data only."""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

repo = Path(__file__).resolve().parent.parent
work = repo / ".agent-work"
tmp = repo / "tmp"

results = sorted(work.glob("GUIDE11-*.md"))
derived = [
    p for p in sorted(tmp.glob("*-2026092*.json"))
    if "lut" not in p.name
] + [tmp / "guide11-final-coverage-20260929.json"]
scripts = sorted(tmp.glob("analyze_*_2026092*.py")) + [
    tmp / "build_final_coverage_20260929.py",
    tmp / "fit_c3_model_20260928.py",
    tmp / "recompute_w8_guide11_20260928.py",
    tmp / "assess_c2_reachability_20260928.py",
]

items: list[tuple[str, Path]] = []
seen: set[Path] = set()
for sub, paths in (("results", results), ("derived", derived), ("scripts", scripts)):
    for p in paths:
        if p.exists() and p.resolve() not in seen:
            seen.add(p.resolve())
            items.append((sub, p))

manifest = []
zpath = work / "GUIDE11-FINAL-PACKAGE-20260929.zip"
with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
    for sub, p in items:
        arc = f"{sub}/{p.name}"
        z.write(p, arc)
        manifest.append({
            "path": arc,
            "source": str(p.resolve()),
            "byte_count": p.stat().st_size,
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
        })

zip_sha = hashlib.sha256(zpath.read_bytes()).hexdigest()
(work / "GUIDE11-FINAL-PACKAGE-MANIFEST-20260929.json").write_text(
    json.dumps({
        "schema": "guide11_final_package_manifest_v1",
        "zip": str(zpath.resolve()),
        "zip_sha256": zip_sha,
        "zip_byte_count": zpath.stat().st_size,
        "file_count": len(manifest),
        "excludes": "raw CR3/RAW/DNG, NPY/NPZ, TIFF/JPEG/PNG derivatives, decoded arrays, firmware, build output, credentials",
        "raw_payload_root": "D:/rgbww-optimizer (per-experiment run roots, retained)",
        "files": manifest,
    }, indent=2) + "\n",
    encoding="utf-8",
)

with zipfile.ZipFile(zpath) as z:
    bad = z.testzip()
print(f"zip: {zpath} {zpath.stat().st_size} bytes | files: {len(manifest)} | integrity: {'FAIL:' + str(bad) if bad else 'ok'}")
print(f"zip sha256: {zip_sha}")
