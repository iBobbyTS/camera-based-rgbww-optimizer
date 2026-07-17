from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Sequence

from camera_based_rgbww_optimizer.measurement import raw_response_candidate
from camera_based_rgbww_optimizer.optimization import analyze_raw_observer_validation


DEFAULT_OUTPUT_NAME = "raw-response-candidate.json"


def analyze_run(run_dir: str | Path) -> dict[str, object]:
    reports = analyze_raw_observer_validation.load_validation_reports(run_dir)
    result = raw_response_candidate.fit_response_candidate(reports)
    result["run_dir"] = str(Path(run_dir))
    return result


def evaluate_run(
    run_dir: str | Path,
    candidate_path: str | Path,
    *,
    expected_candidate_sha256: str,
    repeatability_run: str | Path | None = None,
) -> dict[str, object]:
    reports = analyze_raw_observer_validation.load_validation_reports(run_dir)
    repeatability_reports = (
        None
        if repeatability_run is None
        else analyze_raw_observer_validation.load_validation_reports(repeatability_run)
    )
    candidate, candidate_sha256 = load_frozen_candidate(
        candidate_path,
        expected_sha256=expected_candidate_sha256,
    )
    result = raw_response_candidate.evaluate_holdout(
        reports,
        candidate,
        repeatability_reports=repeatability_reports,
    )
    result["run_dir"] = str(Path(run_dir))
    result["candidate_path"] = str(Path(candidate_path))
    result["candidate_sha256"] = candidate_sha256
    result["repeatability_run"] = None if repeatability_run is None else str(Path(repeatability_run))
    return result


def load_frozen_candidate(
    candidate_path: str | Path,
    *,
    expected_sha256: str,
) -> tuple[dict[str, object], str]:
    path = Path(candidate_path)
    payload = path.read_bytes()
    actual_sha256 = hashlib.sha256(payload).hexdigest()
    if actual_sha256 != expected_sha256.lower():
        raise ValueError(
            f"candidate SHA-256 mismatch: expected {expected_sha256.lower()}, got {actual_sha256}"
        )
    candidate = json.loads(payload)
    if not isinstance(candidate, dict):
        raise ValueError("candidate JSON root must be an object")
    return candidate, actual_sha256


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fit a candidate-only monotonic RAW response model.")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--candidate", type=Path, help="Evaluate frozen coefficients instead of fitting.")
    parser.add_argument("--candidate-sha256", help="Required SHA-256 for a frozen --candidate artifact.")
    parser.add_argument(
        "--repeatability-run",
        type=Path,
        help="Completed full P1 run supplying paired-repeat noise for a boundary-only holdout.",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        if bool(args.candidate) != bool(args.candidate_sha256):
            raise ValueError("--candidate and --candidate-sha256 must be provided together")
        if args.repeatability_run is not None and args.candidate is None:
            raise ValueError("--repeatability-run requires --candidate")
        result = (
            evaluate_run(
                args.run_dir,
                args.candidate,
                expected_candidate_sha256=args.candidate_sha256,
                repeatability_run=args.repeatability_run,
            )
            if args.candidate
            else analyze_run(args.run_dir)
        )
        default_name = "raw-response-holdout.json" if args.candidate else DEFAULT_OUTPUT_NAME
        output = args.output or args.run_dir / default_name
        output.write_text(
            json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n",
            encoding="utf-8",
        )
        print(output)
    except Exception as exc:
        print(f"analyze_raw_response_candidate: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
