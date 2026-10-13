"""GUIDE12 evidence-completion phase A: offline RAW identity + matrix sweep.

Walks every GUIDE12 campaign directory on D:/rgbww-optimizer, and for each
retained RAW payload (CR3 plus the extension-less diagnostic captures)
records byte_count, a fresh SHA-256, the rawpy rgb_xyz_matrix[:3] actually
used by the white-point chain, and the sidecar identity when present.

Pure offline file reads; no device, camera or network access. Output:
.agent-work/guide12/completion-workspace/raw-scan.json
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

DATA = Path("D:/rgbww-optimizer")
REPO = Path(__file__).resolve().parent.parent
OUT = REPO / ".agent-work/guide12/completion-workspace/raw-scan.json"
CAMPAIGNS = [
    "guide12-batch1", "guide12-n2", "guide12-c12", "guide12-w12",
    "guide12-w122", "guide12-w123", "guide12-w124", "guide12-c122",
    "guide12-c124",
]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    import rawpy

    records: list[dict] = []
    t0 = time.time()
    for campaign in CAMPAIGNS:
        croot = DATA / campaign
        if not croot.exists():
            continue
        raws: list[tuple[Path, str]] = []
        # CR3s inside run-root camera/ dirs plus campaign-level prechecks
        for p in croot.rglob("*.cr3"):
            raws.append((p, "cr3"))
        # extension-less diagnostic payloads (bridge saved with {{counter}})
        for sub in croot.iterdir():
            if sub.is_dir():
                for p in sub.iterdir():
                    if p.is_file() and p.suffix == "" and "{{counter}}" in p.name:
                        raws.append((p, "extensionless_diag"))
        for p, kind in raws:
            rec = {
                "campaign": campaign,
                "path": str(p),
                "kind": kind,
                "byte_count": p.stat().st_size,
            }
            rec["recomputed_sha256"] = sha256_file(p)
            sidecar = p.with_name(p.name + ".metadata.json") if kind == "cr3" else None
            if sidecar and sidecar.exists():
                sb = sidecar.read_bytes()
                rec["sidecar_path"] = str(sidecar)
                rec["sidecar_byte_count"] = len(sb)
                rec["sidecar_sha256"] = hashlib.sha256(sb).hexdigest()
            try:
                with rawpy.imread(str(p)) as raw:
                    m = [[float(v) for v in row] for row in raw.rgb_xyz_matrix[:3]]
                rec["rgb_xyz_matrix_first3"] = m
                rec["matrix_read"] = "ok"
            except Exception as exc:  # pragma: no cover - diagnostic payloads
                rec["matrix_read"] = f"failed: {type(exc).__name__}: {exc}"
            records.append(rec)
        print(f"{campaign}: cumulative raws={len(records)} "
              f"elapsed={time.time()-t0:.0f}s", flush=True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
    n_matrix_ok = sum(1 for r in records if r.get("matrix_read") == "ok")
    mats = {json.dumps(r["rgb_xyz_matrix_first3"]) for r in records
            if r.get("matrix_read") == "ok"}
    print(f"raws={len(records)} matrix_ok={n_matrix_ok} unique_matrices={len(mats)}")
    print(f"written: {OUT} elapsed={time.time()-t0:.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
