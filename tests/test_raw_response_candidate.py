from __future__ import annotations

import unittest
import copy
import hashlib
import json
import tempfile
from pathlib import Path

from camera_based_rgbww_optimizer.optimization import analyze_raw_response_candidate

from camera_based_rgbww_optimizer.measurement import raw_response_candidate


def _plane(value: float) -> dict:
    return {
        "metrics": {"clipped_fraction": 0.0},
        "statistics": {"black_corrected_normalized": {"trimmed_mean": value}},
    }


def _report(capture_id: str, *, source: str, purpose: str, factor: float | None, values: dict[str, float]) -> dict:
    exposure = 0.1 if factor is None else 0.1 * factor
    context = {
        "capture_id": capture_id,
        "source": source,
        "purpose": purpose,
        "exposure_factor": factor,
        "exposure_seconds": exposure,
        "exposure_status": "recorded",
    }
    patches = [
        {
            "name": name,
            "optimization_eligible": True,
            "planes": {"R": _plane(value)},
        }
        for name, value in values.items()
    ]
    ambient = [
        {
            "name": name,
            "optimization_eligible": True,
            "planes": {"R": _plane(0.0)},
        }
        for name in values
    ]
    return {
        "source": {"path": f"{capture_id}.cr3", "sha256": capture_id.zfill(64)},
        "location_config": {"sha256": "location"},
        "analysis_context": context,
        "ambient_exposure_metadata": {"seconds": 1.0},
        "ambient_reference": {"exposure_seconds": 1.0, "patches": ambient},
        "patches": patches,
    }


def _compressed(value: float) -> float:
    return value / (1.0 + 0.8 * value)


def _reports() -> list[dict]:
    reports: list[dict] = []
    base = {"dark": 0.3, "middle": 0.7, "bright": 1.4}
    for source_scale, source in ((1.0, "ray"), (0.8, "strip")):
        for repeat in range(3):
            reports.append(
                _report(
                    f"{source}-repeat-{repeat}",
                    source=source,
                    purpose="paired_repeat",
                    factor=None,
                    values={name: _compressed(value * source_scale * 0.1) for name, value in base.items()},
                )
            )
        for factor in (0.5, 1.0, 1.5):
            for repeat in range(2):
                reports.append(
                    _report(
                        f"{source}-{factor}-{repeat}",
                        source=source,
                        purpose="linearity_bracket",
                        factor=factor,
                        values={
                            name: _compressed(value * source_scale * 0.1 * factor)
                            for name, value in base.items()
                        },
                    )
                )
    return reports


class RawResponseCandidateTests(unittest.TestCase):
    def test_ignores_ambient_report_without_ambient_provenance(self):
        reports = _reports()
        reports.insert(
            0,
            {
                "source": {"path": "ambient.cr3", "sha256": "a" * 64},
                "location_config": {"sha256": "location"},
                "analysis_context": {
                    "capture_id": "ambient",
                    "source": "ambient",
                    "purpose": "ambient",
                    "exposure_seconds": 1.0,
                },
                "patches": [],
            },
        )

        candidate = raw_response_candidate.fit_response_candidate(reports)

        self.assertEqual(candidate["status"], "candidate_only_waiting_for_cross_day_holdout")

    def test_fit_is_monotonic_and_improves_shape_residual(self):
        candidate = raw_response_candidate.fit_response_candidate(_reports())

        identity = candidate["comparisons"]["identity_full_envelope"]["summary"]
        corrected = candidate["comparisons"]["candidate_full_envelope"]["summary"]
        identity_p95 = identity["absolute_shape_relative_residual_non_reference"]["p95"]
        corrected_p95 = corrected["absolute_shape_relative_residual_non_reference"]["p95"]
        self.assertLess(corrected_p95, identity_p95)
        self.assertGreaterEqual(
            candidate["model"]["constraints"]["minimum_derivative_observed_on_0_to_1"],
            0.05,
        )
        self.assertEqual(candidate["model"]["out_of_range_policy"], "reject_outside_training_range")
        ray = candidate["comparisons"]["candidate_full_envelope"]["sources"]["ray"]
        self.assertEqual(set(ray["by_plane"]), {"R"})
        self.assertEqual(set(ray["by_factor"]), {"0.5", "1.5"})
        self.assertEqual(ray["worst_features_by_repeatability_sigma"][0]["plane"], "R")
        self.assertIn(
            ray["worst_features_by_repeatability_sigma"][0]["patch_name"],
            {"dark", "middle", "bright"},
        )

    def test_rejects_nominal_exposure_provenance(self):
        reports = _reports()
        reports[0]["analysis_context"]["exposure_status"] = "fallback_nominal"

        with self.assertRaisesRegex(ValueError, "recorded exposure"):
            raw_response_candidate.fit_response_candidate(reports)

    def test_derivative_checks_internal_vertex(self):
        self.assertLess(raw_response_candidate.response_derivative_minimum(a=-1.0, b=1.0), 1.0)

    def test_holdout_uses_frozen_coefficients_without_refitting(self):
        training = _reports()
        candidate = raw_response_candidate.fit_response_candidate(training)
        holdout = copy.deepcopy(training)
        for report in holdout:
            report["source"]["sha256"] = "f" * 64

        result = raw_response_candidate.evaluate_holdout(holdout, candidate)

        self.assertEqual(result["status"], "holdout_ready_for_manual_branch_review")
        self.assertEqual(result["model"]["coefficients"], candidate["model"]["coefficients"])

    def test_holdout_rejects_training_input(self):
        reports = _reports()
        candidate = raw_response_candidate.fit_response_candidate(reports)

        with self.assertRaisesRegex(ValueError, "identical"):
            raw_response_candidate.evaluate_holdout(reports, candidate)

    def test_boundary_holdout_can_use_independent_repeatability_reports(self):
        training = _reports()
        candidate = raw_response_candidate.fit_response_candidate(training)
        boundary = [
            copy.deepcopy(report)
            for report in training
            if report["analysis_context"]["purpose"] == "linearity_bracket"
        ]
        for report in boundary:
            report["source"]["sha256"] = "e" * 64
        repeatability = copy.deepcopy(training)
        for report in repeatability:
            report["source"]["sha256"] = "f" * 64

        result = raw_response_candidate.evaluate_holdout(
            boundary,
            candidate,
            repeatability_reports=repeatability,
        )

        sigma = result["candidate_full_envelope"]["summary"][
            "shape_residual_repeatability_sigma_non_reference"
        ]
        self.assertGreater(sigma["count"], 0)
        self.assertEqual(result["repeatability_input_sha256"], raw_response_candidate._reports_sha256(repeatability))

    def test_frozen_candidate_requires_matching_file_hash(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = Path(tempdir) / "candidate.json"
            payload = json.dumps({"status": "candidate_only"}).encode()
            path.write_bytes(payload)
            expected = hashlib.sha256(payload).hexdigest()

            candidate, actual = analyze_raw_response_candidate.load_frozen_candidate(
                path,
                expected_sha256=expected,
            )

            self.assertEqual(candidate["status"], "candidate_only")
            self.assertEqual(actual, expected)
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                analyze_raw_response_candidate.load_frozen_candidate(
                    path,
                    expected_sha256="0" * 64,
                )


if __name__ == "__main__":
    unittest.main()
