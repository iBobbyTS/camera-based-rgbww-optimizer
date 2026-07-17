from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Sequence

from camera_based_rgbww_optimizer.measurement.chart_basis_validation import analyze_chart_basis_validation
from camera_based_rgbww_optimizer.optimization.analyze_raw_observer_validation import load_validation_reports


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze a complete P3 chart-basis mixture run offline.")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--basis-analysis", type=Path, required=True)
    parser.add_argument("--basis-sha256", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    payload = args.basis_analysis.read_bytes()
    actual_hash = hashlib.sha256(payload).hexdigest()
    if actual_hash != args.basis_sha256:
        raise ValueError(f"basis SHA-256 mismatch: expected {args.basis_sha256}, got {actual_hash}")
    basis = json.loads(payload)
    reports = load_validation_reports(args.run_dir)
    result = analyze_chart_basis_validation(reports, basis)
    result["basis_provenance"] = {"path": str(args.basis_analysis), "sha256": actual_hash}
    output = args.output or args.run_dir / "basis-validation.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
