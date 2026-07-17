from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from camera_based_rgbww_optimizer.measurement.chart_response_basis import analyze_chart_response_basis
from camera_based_rgbww_optimizer.optimization.analyze_raw_observer_validation import load_validation_reports


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze a complete P2 chart response basis run offline.")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--random-seed", type=int, default=20260716)
    args = parser.parse_args(argv)
    reports = load_validation_reports(args.run_dir)
    result = analyze_chart_response_basis(
        reports,
        bootstrap_samples=args.bootstrap_samples,
        random_seed=args.random_seed,
    )
    output = args.output or args.run_dir / "basis-analysis.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
