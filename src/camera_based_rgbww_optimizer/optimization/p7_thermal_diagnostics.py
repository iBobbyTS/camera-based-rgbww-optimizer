from __future__ import annotations

import hashlib
import json
import math
import re
import stat
import subprocess
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence
from types import MappingProxyType

import numpy as np

from camera_based_rgbww_optimizer.measurement.hsi_policy_v2 import (
    AUDIT_THRESHOLDS,
    ordered_unit_shape,
    summarize_within_groups,
)
from camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation import (
    AMBIENT_POLICY_REQUIRE_PRECEDING,
    AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
)
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT


TD_A = "p7_td_a_cold_settling_v1"
TD_B = "p7_td_b_command_switch_history_v1"
TD_C = "p7_td_c_balanced_source_comparison_v1"
EXPERIMENT_IDS = (TD_A, TD_B, TD_C)
TIMED_POINTS = (60, 120, 300, 600)
SELECTABLE_SETTLE_POINTS = (60, 120, 300)
PLAN_SCHEMA_V1 = "p7_thermal_diagnostic_plan_v1"
PLAN_SCHEMA_V2 = "p7_thermal_diagnostic_plan_v2"
ANALYSIS_SCHEMA_V2 = "p7_thermal_diagnostic_analysis_v2"
_TIMING_CONTRACT_V1_TEMPLATE = {
    "name": "best_effort_gphoto2_v1",
    "decision_owner": "Developer/Human",
    "network_assumption": "wired_lan_latency_negligible_developer_decision",
    "accepted_tiers": ["tier_a", "tier_b"],
    "absolute_exposure_start_required": False,
    "absolute_exposure_start": False,
    "provenance": "best_effort_gphoto2_exposure_start_estimate",
}
_TIMING_CONTRACT_V2_TEMPLATE = {
    "name": "best_effort_gphoto2_observed_elapsed_v2",
    "decision_owner": "Developer/Human",
    "network_assumption": "wired_lan_latency_negligible_developer_decision",
    "accepted_tiers": ["tier_a", "tier_b"],
    "absolute_exposure_start_required": False,
    "absolute_exposure_start": False,
    "provenance": "best_effort_gphoto2_exposure_start_estimate",
    "nominal_slot_semantics": "scheduler_target_only",
    "acceptance_basis": "evidence_integrity_not_nominal_proximity",
    "nominal_offset_gate": "none_developer_decision",
}
ACCEPTED_TIMING_TIERS = frozenset(("tier_a", "tier_b"))
TIMING_CONTRACT_V1 = MappingProxyType({
    **_TIMING_CONTRACT_V1_TEMPLATE,
    "accepted_tiers": tuple(_TIMING_CONTRACT_V1_TEMPLATE["accepted_tiers"]),
})
TIMING_CONTRACT_V2 = MappingProxyType({
    **_TIMING_CONTRACT_V2_TEMPLATE,
    "accepted_tiers": tuple(_TIMING_CONTRACT_V2_TEMPLATE["accepted_tiers"]),
})


def timing_contract(version: int) -> dict[str, Any]:
    if version == 1:
        return deepcopy(_TIMING_CONTRACT_V1_TEMPLATE)
    if version == 2:
        return deepcopy(_TIMING_CONTRACT_V2_TEMPLATE)
    raise ValueError(f"unsupported thermal timing contract version: {version}")
ACTUAL_EXPOSURE_START_PROVENANCE = "camera_adapter_actual_exposure_start_monotonic"
CHANNELS = ("cw", "ww", "r", "g", "b")
R1_RUN = Path(
    "/Volumes/4T/temp/rgbww-optimizer/hsi-reference-repeatability/"
    "p7-r1-20260719-091000-terminal-retry1"
)
POLICY_PATH = PROJECT_ROOT / "config/hsi/strip-hsi-policy-v2-waiting.json"
OBSERVER_PATH = PROJECT_ROOT / "config/camera/raw-observer.json"
UNCERTAINTY_PATH = PROJECT_ROOT / "config/hsi/strip-hsi-uncertainty.json"
MANIFOLD_PATH = PROJECT_ROOT / "config/hsi/ray-hsi-manifold.json"
LOCATION_PATH = PROJECT_ROOT / "config/location/locations-20260714-211759.json"
CURVE_PATH = PROJECT_ROOT / "config/channel/code-duty-curve.json"
OPERATING_ENVELOPE_PATH = PROJECT_ROOT / "config/hsi/p7-operating-envelope-v1.json"
OPERATING_ENVELOPE_V2_PATH = PROJECT_ROOT / "config/hsi/p7-operating-envelope-v2.json"
OPERATING_ENVELOPE_V2_SHA256 = "7012f254e5fa5182dd51b72624f64ce03645fd3d8b7227ab9144f5c7767cfc16"
OPERATING_ENVELOPE_V2_SCHEMA = "p7_operating_envelope_v2"
TD_B_EXPOSURE_POLICY_V2_PATH = PROJECT_ROOT / "config/hsi/p7-ray-td-b-exposure-policy-v2.json"
TD_B_EXPOSURE_POLICY_V2_SCHEMA = "p7_ray_td_b_exposure_policy_v2"
TD_B_EQ_R6_EXPERIMENT_ID = "P7-TD-B-RAY-C-EXPOSURE-QUAL-R6"
TD_B_EQ_R6_LIVE_PLAN_SCHEMA = "p7_td_b_eq_r6_live_plan_v1"
TD_B_R6_EXPERIMENT_ID = "P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6"
TD_B_R5_PLAN_SHA256 = "94da09f240e2d0ca84ce545c52748522dfbaa9a674bf96ffcef5c8e74473ba9f"
TD_B_R5_SHUTTERS_SHA256 = "b49dd52ebc1eabc8ae6ae0e3713884e5e939428d0682e6d7234eea8c17626e71"
TD_B_FEATURE_IDS_SHA256 = "4a37bf13a1dcfa6b652bd4ce6a7793aa8ac0344c293d1a7fc73ff7fad763ab86"
TD_B_R5_FAILURE_CLASS = (
    "state_specific_exposure_policy_failure_with_required_feature_observer_saturation"
)
TD_B_EQ_CANDIDATES = ("1/2500", "1/3200")
TD_B_EQ_R6_ACCEPTED_ROOT = Path(
    "/Volumes/4T/temp/rgbww-optimizer/"
    "p7-td-b-exposure-qual-r6-f37517a-20260727T1928"
)
TD_B_EQ_R6_QUALIFICATION_CHECKPOINT = "f37517af3ae25efb41f085904fd48f037980ed04"
TD_B_EQ_R6_MANIFEST_SCHEMA = "planner_eq_family_manifest_v1"
TD_B_EQ_R6_MANIFEST_SHA256 = "41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9"
TD_B_EQ_R6_ARTIFACT_SHA256 = {
    "run/outer-result.json": "20a4ee42c931e7df74b7fdd756eab3077530726e8ae5c03d3d48b45e8b562f0a",
    "run/candidate-1-outer-terminal.json": (
        "6401f0f162ce3efcd1ca6139e8394ed17411df7552fb1722e2db3eb7a8e4cd16"
    ),
    "run/candidate-1/candidate-result.json": (
        "7db4d60627c9a63304945664b4ba2e7918dafb12495f5fbf1d45500a46748612"
    ),
    "run/candidate-1/terminal-seal.json": (
        "8baa46bc6431e9e79c035a6f83954d810c25def2c8b662a761784fd1d81417a3"
    ),
}
TD_B_EQ_CAPTURE_IDS = (
    ("000-ray-c2500-t60", "001-ray-c2500-t120", "002-ray-c2500-t300", "003-ray-c2500-t600"),
    ("004-ray-c3200-t60", "005-ray-c3200-t120", "006-ray-c3200-t300", "007-ray-c3200-t600"),
)
TD_B_R6_CAPTURE_IDS = (
    "000-ray-a0-t600",
    "001-ray-d-t60", "002-ray-d-t120", "003-ray-d-t300", "004-ray-d-t600",
    "005-ray-a-after-d-t600",
    "006-ray-b-t60", "007-ray-b-t120", "008-ray-b-t300", "009-ray-b-t600",
    "010-ray-a-after-b-t600",
    "011-ray-c-t60", "012-ray-c-t120", "013-ray-c-t300", "014-ray-c-t600",
    "015-ray-a-after-c-t600",
)
TD_B_R6_PRE_EQ_CANONICAL_ARTIFACTS = (
    "r5-source-manifest-before.json",
    "r5-source-manifest-after.json",
    "r5-partial-diagnostic-analysis-v1.json",
    "exposure-policy-v2-validation.json",
    "eq-r6-fake-matrix.json",
    "ray-r6-validator-matrix.json",
    "ray-r6-analyzer-matrix.json",
    "locks-matrix.json",
    "secret-path-scan.json",
    "source-diff.json",
    "strict-json-audit.json",
    "validation-summary.json",
    "terminal-summary.json",
)
TD_B_R6_PRE_EQ_PRE_SUMMARY_ARTIFACTS = TD_B_R6_PRE_EQ_CANONICAL_ARTIFACTS[:11]
TD_B_R6_PRIVATE_OVERRIDE_IDENTIFIER = "AMARAN_OPENAPI_" + "SECRET"
_TD_B_R6_NETWORK_TARGET_RE = re.compile(
    r"https?://[^\s\"']+|(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])|"
    r"\b[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.local\b"
)
_TD_B_R6_LITERAL_PRIVATE_VALUE_RE = re.compile(
    r"""(?ix)
    \b(?:password|private[_\s-]*value|access[_\s-]*token|api[_\s-]*key)
    \s*[:=]\s*["'][^"'\n]{8,}["']
    """
)
_TD_B_R6_ENV_READ_RE = re.compile(
    r"\bos\.(?:environ|getenv)\b|\bdotenv\b|(?:^|/)\.env(?:\b|$)"
)
_TD_B_R6_ABSOLUTE_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_.-])/(?:Users|Volumes|private|tmp|synthetic)/"
    r"[A-Za-z0-9_./-]+"
)
DEVELOPER_OPERATIONAL_DWELL_S = 600
DEVELOPER_DWELL_DECISION_AUDIT = PROJECT_ROOT / "advisor/4/0.AUDIT/03-human-decision-no-extension.md"
DEVELOPER_DWELL_DECISION_AUDIT_SHA256 = "c917c54473aa3c5cc4da9098ddeb81fb109fe9a4186fb71e994c447c63d0454a"
TD_B_SETUP_SCHEMA = "p7_td_b_exposure_setup_v1"
TD_B_SETUP_SCHEMA_V2 = "p7_td_b_exposure_setup_v2"
TD_B_SETUP_PROVISIONAL_SCHEMA = "p7_td_b_exposure_setup_provisional_v1"
TD_B_SETUP_RELEASE_SCHEMA = "p7_td_b_exposure_setup_release_v1"
TD_B_SETUP_RELEASE_LINEAGE_CANDIDATE_SCHEMA = (
    "p7_td_b_setup_release_lineage_candidate_v1"
)
TD_B_SETUP_LINEAGE_RELEASE_SCHEMA = "p7_td_b_setup_lineage_release_v2"
TD_B_SETUP_CHECKPOINT = "9c804abdeabbc5da18a66d0acf25a1f13128bc2d"
TD_B_F0A_CHECKPOINT = "8b80c87939ee9aed31ce0dfaa08a5a936bdc56cb"
TD_B_SETUP_RELEASE_PATH = Path(
    "/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/"
    "p7-td-b-canon-r2-setup-20260723-042002/setup-release.json"
)
TD_B_F0A_LINEAGE_CANDIDATE_PATH = Path(
    "/Volumes/4T/temp/rgbww-optimizer/p7-td-b-f0a-offline/"
    "p7-td-b-f0a-20260723-100606/setup-release-lineage-candidate.json"
)
TD_B_F0A_LINEAGE_CANDIDATE_SHA256 = (
    "6d74f2b0fa563147bad00d8c9a89985d3b5de97034288cdd242f10b1d52dc2f1"
)
TD_B_AGENTS_POLICY_FREEZE_PATH = Path(
    "/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-policy-freeze-c1/"
    "20260726T230000Z/policy-freeze.json"
)
TD_B_AGENTS_POLICY_FREEZE_SHA256 = (
    "833b4229986dbe1e551cc4da36d2eeaeb7b55c6ae0bab34e887e7ee63cfe746b"
)
TD_B_AGENTS_CURRENT_SHA256 = (
    "a035e6955ea113100031bf411f30abad3b84a9dd260fde848f1b1cfbd194c8a5"
)
TD_B_AGENTS_PREVIOUS_SHA256 = (
    "f4a4a9edffb563c0ea7709382b53eed919c4a5528c69ffa9878a4c32348ee99b"
)
TD_B_AGENTS_DIFF_SHA256 = (
    "96785b5569cf420440666912944a471baad1d2d0a39743990eee5714c0f60918"
)
TD_B_AGENTS_POLICY_SCOPE = (
    "workflow roles plus Human authorization boundary; release/off/on exceptions; "
    "no scientific or device-contract changes"
)
TD_B_AGENTS_HUMAN_DECISION = (
    "explicit instruction to clarify only remote firmware and comparable dangerous "
    "operations require Human authorization; release and light on/off do not"
)
TD_B_WORKFLOW_PATH_MANIFEST_PATH = Path(
    "/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-workflow-path-c1/"
    "20260727T010000Z/workflow-path-manifest.json"
)
TD_B_WORKFLOW_PATH_MANIFEST_SHA256 = (
    "8f9189edfb1520be2e08913678d7e046b93cb0a3c42a0034331e16b39d982e94"
)
TD_B_WORKFLOW_PATH_COMMIT = "3f8fb5c2f046ad5c75eab200005331acd5f2cc27"
TD_B_WORKFLOW_PATH_PARENT = "8cd04d847d42ff5c7bcf7501f46be97cbbef429d"
TD_B_WORKFLOW_PATH_CLASSIFICATIONS = MappingProxyType({
    "docs/engineering/p7-td-b-contract-history.md":
        "bounded_validation_or_documentation",
    "docs/local-lab-connection-boundary.md":
        "bounded_validation_or_documentation",
    "src/camera_based_rgbww_optimizer/control/camera_remote.py":
        "human_directed_local_lab_cli_boundary",
    "src/camera_based_rgbww_optimizer/control/esphome.py":
        "human_directed_local_lab_cli_boundary",
    "src/camera_based_rgbww_optimizer/control/local_lab_context.py":
        "human_directed_local_lab_cli_boundary",
    "src/camera_based_rgbww_optimizer/control/ray120c.py":
        "human_directed_credential_boundary",
    "tests/test_all_off.py": "bounded_validation_or_documentation",
    "tests/test_local_lab_context.py": "bounded_validation_or_documentation",
    "tests/test_project_context_docs.py": "bounded_validation_or_documentation",
    "tests/test_ray120c.py": "bounded_validation_or_documentation",
})
TD_B_WORKFLOW_PATH_HUMAN_INSTRUCTION = (
    "clarify the user-owned local calibration context and remove the built-in Ray "
    "credential default to reduce cybersecurity-risk false positives without weakening "
    "local-lab safety"
)
TD_B_WORKFLOW_PATH_SCOPES = MappingProxyType({
    "bounded_validation_or_documentation": (
        "Human-directed local-lab documentation and exact regression coverage only; "
        "no scientific, device, payload, host, default, timeout, or cleanup behavior changes"
    ),
    "human_directed_local_lab_cli_boundary": (
        "exact CLI description, user-owned local-lab context, and argv testability changes "
        "only; no capture, parser, payload, host, default, timeout, or cleanup semantic changes"
    ),
    "human_directed_credential_boundary": (
        "remove built-in credential, require strict secret decode and explicit environment "
        "input only; with a valid key Ray mode, command payload, node/client, timeout, cleanup, "
        "and off-command semantics remain equivalent"
    ),
})
TD_B_PUBLIC_DEFAULT_SUCCESSOR_MANIFEST_PATH = Path(
    "/Volumes/4T/temp/rgbww-optimizer/"
    "p7-td-b-ray-public-default-lineage-c1/20260726T144421Z/"
    "successor-workflow-manifest.json"
)
TD_B_PUBLIC_DEFAULT_SUCCESSOR_MANIFEST_SHA256 = (
    "6915c68cbb9436a8aa96ee5384751be6f9405c6f5330d19112cab2b77e898cd3"
)
TD_B_PUBLIC_DEFAULT_SUCCESSOR_COMMIT = "e7ccdda672b7d5902d81627ff98268160ff141cd"
TD_B_PUBLIC_DEFAULT_SUCCESSOR_PARENT = "a87b09fc4a701a76e5214d6ff6d3a4e3de090521"
TD_B_PUBLIC_DEFAULT_SUCCESSOR_HUMAN_DECISION = (
    "Human classified the exact Ray key as a public shared protocol default and "
    "AMARAN_OPENAPI_SECRET as an optional explicit private runtime override"
)
TD_B_PUBLIC_DEFAULT_SUCCESSOR_PROVENANCE = (
    "Human decision and repository history only; not external-vendor documentation, "
    "protocol specification, or security review verification; implemented by exact "
    f"commit {TD_B_PUBLIC_DEFAULT_SUCCESSOR_COMMIT}"
)
TD_B_PUBLIC_DEFAULT_SUCCESSOR_CLASSIFICATIONS = MappingProxyType({
    ".agents/skills/camera-based-rgbww-optimizer/SKILL.md":
        "bounded_validation_or_documentation",
    "docs/README.md": "bounded_validation_or_documentation",
    "docs/local-lab-connection-boundary.md":
        "bounded_validation_or_documentation",
    "src/camera_based_rgbww_optimizer/control/ray120c.py":
        "human_directed_public_shared_protocol_default_boundary",
    "tests/test_all_off.py": "bounded_validation_or_documentation",
    "tests/test_project_context_docs.py": "bounded_validation_or_documentation",
    "tests/test_ray120c.py": "bounded_validation_or_documentation",
})
TD_B_PUBLIC_DEFAULT_SUCCESSOR_SCOPES = MappingProxyType({
    "bounded_validation_or_documentation": (
        "Bounded tests, documentation, and project-skill coverage for the exact "
        "public-default/private-override contract only"
    ),
    "human_directed_public_shared_protocol_default_boundary": (
        "Human-directed public shared protocol default and optional private override "
        "boundary; strict validation and nondisclosure preserved; no device, network, "
        "payload, timeout, or cleanup widening"
    ),
})
TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PATH = (
    PROJECT_ROOT / "config/hsi/p7-governance-lineage-successor-v1.json"
)
TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_SHA256 = (
    "69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e"
)
TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_COMMIT = (
    "3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c"
)
TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PARENT = (
    "9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e"
)
TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_CLASSIFICATIONS = MappingProxyType({
    ".agents/skills/camera-based-rgbww-optimizer/SKILL.md":
        "bounded_validation_or_documentation",
    "AGENTS.md": "bounded_validation_or_documentation",
})
TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_CURRENT_SHA256 = MappingProxyType({
    ".agents/skills/camera-based-rgbww-optimizer/SKILL.md":
        "3a77c8a0f7b02b0c8b15d31b625273e88a0ee38fca5bb739dbdaaacb40dfe81e",
    "AGENTS.md": "604b10bedeac6c9285f6448f94323521bf021a58275cce84d64163e16a2f07a0",
})
TD_B_QUALIFICATION_PREPARATION_R1_PATH = Path(
    "/Volumes/4T/temp/rgbww-optimizer/"
    "p7-td-b-ray-public-default-lineage-c3-r1-offline-correction/"
    "20260726T094349Z/qualification-preparation-r1.json"
)
TD_B_QUALIFICATION_PREPARATION_R1_SHA256 = (
    "c6200a2307a8a3e95e82328f73acdcbc1d6746d9ff9365fe4b8d7a9ef92006de"
)
TD_B_QUALIFICATION_PREPARATION_R1_BYTES = 14163
TD_B_QUALIFICATION_AUDIT_CHECKPOINT = "52a7168cd2510e9730e30101fc8fbf6f6d8153c1"
TD_B_QUALIFICATION_PREPARATION_R1_SCHEMA = (
    "p7_td_b_ray_public_default_lineage_c3_r1_preparation_v2"
)
TD_B_QUALIFICATION_EVIDENCE_SCHEMA = (
    "p7_td_b_lineage_qualification_evidence_only_v1"
)
TD_B_QUALIFICATION_EVIDENCE_STATUS = (
    "qualification_evidence_ready_waiting_for_planner"
)
TD_B_CLEANUP_TEST_PROVENANCE_MANIFEST_PATH = Path(
    "/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-cleanup-test-provenance-c1/"
    "20260727T020000Z/cleanup-test-provenance-manifest.json"
)
TD_B_CLEANUP_TEST_PROVENANCE_MANIFEST_SHA256 = (
    "753f00f15a9c40dd0e3a0c34773f063a2cd44605d7c1f5507f375d87f56ea0d0"
)
TD_B_CLEANUP_TEST_PROVENANCE_OLD = "6c42c6eafd51b441ab911b13115c5bceae2a39d9"
TD_B_CLEANUP_TEST_PROVENANCE_NEW = "0c878cbf3c7d94dadef2a64446c08ba01931a0d2"
TD_B_CLEANUP_TEST_PROVENANCE_CLASSIFICATIONS = MappingProxyType({
    "tests/test_measure_chart_response_basis.py":
        "bounded_validation_or_documentation",
    "tests/test_measure_raw_shutter_response.py":
        "bounded_validation_or_documentation",
})
TD_B_CLEANUP_TEST_PROVENANCE_SCOPES = MappingProxyType({
    "tests/test_measure_chart_response_basis.py": (
        "test-owned fake AMARAN_OPENAPI_SECRET injection around one cleanup execution test"
    ),
    "tests/test_measure_raw_shutter_response.py": (
        "test-owned fake AMARAN_OPENAPI_SECRET injection around two cleanup execution tests"
    ),
})
TD_B_CLEANUP_TEST_PROVENANCE_HUMAN_INSTRUCTION = (
    "use a test-owned valid fake Ray credential only around cleanup execution tests "
    "while preserving production credential, payload, cleanup, and .env behavior"
)
TD_B_POST_EQ_POLICY_COMMIT = "161094ffa2bf1f84ed1fc787e708e8c3463f10db"
TD_B_POST_EQ_POLICY_PARENT = "f37517af3ae25efb41f085904fd48f037980ed04"
TD_B_POST_EQ_POLICY_SUBJECT = "feat(p7): finalize eq-r6 state-c exposure policy"
TD_B_POST_EQ_POLICY_PATHS = (
    "config/hsi/p7-ray-td-b-exposure-policy-v2.json",
    "src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py",
    "tests/test_p7_td_b_r6_contract.py",
)
TD_B_POST_EQ_POLICY_PATHS_SHA256 = (
    "fdd774e4686b3ebe45296880d6407666dd4ef6cc633e7f9cc891e62bd5480ac2"
)
TD_B_POST_EQ_POLICY_BLOB_SHA256 = MappingProxyType({
    "config/hsi/p7-ray-td-b-exposure-policy-v2.json":
        "c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681",
    "src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py":
        "87efa4ff026b4433ff00b40876bdb6a0b96ec181190f8d288e1f3fea6ad41b90",
    "tests/test_p7_td_b_r6_contract.py":
        "10374ec2366fc8cbe928953690defc31c83dc5c04da192f599f59591ec196f23",
})
TD_B_POST_EQ_POLICY_CLASSIFICATIONS = MappingProxyType({
    "config/hsi/p7-ray-td-b-exposure-policy-v2.json":
        "accepted_post_eq_exposure_policy_contract",
    "tests/test_p7_td_b_r6_contract.py":
        "accepted_post_eq_exposure_policy_validation",
})
TD_B_LINEAGE_ALLOWED_PRODUCTION_PATHS = frozenset({
    "src/camera_based_rgbww_optimizer/optimization/hsi_objective.py",
    "src/camera_based_rgbww_optimizer/optimization/measure_raw_observer_validation.py",
    "src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py",
    "src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py",
    "src/camera_based_rgbww_optimizer/optimization/analyze_p7_thermal_diagnostics.py",
})
TD_B_LINEAGE_ALLOWED_VALIDATION_PATHS = frozenset({
    "tests/test_hsi_objective.py",
    "tests/test_measure_raw_observer_validation.py",
    "tests/test_p7_thermal_diagnostics.py",
    "tests/test_analyze_p7_thermal_diagnostics.py",
    "docs/README.md",
    ".agents/skills/camera-based-rgbww-optimizer/SKILL.md",
})
TD_B_SETUP_STATE = "H120_S50_INT100"
TD_B_SETUP_CACHE_KEY = "ray-h120-s50"
TD_B_SETUP_COMMAND = MappingProxyType({"hue": 120, "sat": 50, "intensity_percent": 100.0})
TD_B_SETUP_PHYSICAL_CAP = 8
P6_SETUP_SEED_RUN = Path(
    "/Volumes/4T/temp/rgbww-optimizer/ray-hsi-manifold/"
    "p6-ray-hsi-remote-20260717-0403-retry1"
)
P6_SETUP_SEED_CAPTURE_ID = "0047-ray-hsi_coarse"
PHYSICAL_RETURN_LEDGER_SCHEMA = "p7_thermal_physical_return_v1"

RAY_STATES = {
    "A": {"hue": 120, "sat": 100, "intensity_percent": 100.0},
    "D": {"hue": 120, "sat": 50, "intensity_percent": 100.0},
    "B": {"hue": 0, "sat": 0, "intensity_percent": 100.0},
    "C": {"hue": 300, "sat": 100, "intensity_percent": 100.0},
}
STRIP_COMMAND_KEYS = {
    "A": "h120-s100-fullscale",
    "D": "h120-s50-fullscale",
    "B": "h0-s0-fullscale",
    "C": "h300-s100-fullscale",
}
REQUIRED_COVARIATES = (
    "monotonic_timestamp_ns", "wall_clock_timestamp", "session_elapsed_s",
    "source_id", "state_id", "exact_command_hash", "source_on_elapsed_s",
    "state_on_elapsed_s", "off_duration_before_s", "previous_state_id",
    "previous_state_dwell_s", "sequence_index", "capture_order", "source_order",
    "ambient_temperature_c", "source_surface_temperature_c", "fan_mode", "power_mode",
    "shutter_seconds", "raw_black_levels", "raw_white_level",
    "load_history_proxy_60s", "load_history_proxy_300s", "load_history_proxy_900s",
)


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    ).hexdigest()


def build_planner_eq_family_manifest(root: str | Path) -> dict[str, Any]:
    """Serialize one EQ evidence family using the frozen Planner schema."""
    target = Path(root)
    root_stat = target.lstat()
    if stat.S_ISLNK(root_stat.st_mode) or not stat.S_ISDIR(root_stat.st_mode):
        raise ValueError("EQ family root must be a real directory")
    if stat.S_IMODE(root_stat.st_mode) != 0o700:
        raise ValueError("EQ family root mode must be 0o700")
    rows: list[dict[str, Any]] = []
    files = directories = symlinks = other = 0
    paths = sorted(
        target.rglob("*"),
        key=lambda path: path.relative_to(target).as_posix(),
    )
    for path in paths:
        row_stat = path.lstat()
        relative = path.relative_to(target).as_posix()
        mode = oct(stat.S_IMODE(row_stat.st_mode))
        if stat.S_ISLNK(row_stat.st_mode):
            symlinks += 1
            raise ValueError(f"EQ family symlink is prohibited: {relative}")
        if stat.S_ISDIR(row_stat.st_mode):
            directories += 1
            rows.append({"mode": mode, "path": relative, "type": "dir"})
            continue
        if stat.S_ISREG(row_stat.st_mode):
            if relative == ".DS_Store":
                continue
            files += 1
            payload = path.read_bytes()
            if len(payload) != row_stat.st_size:
                raise ValueError(f"EQ family file changed during manifest: {relative}")
            rows.append({
                "bytes": row_stat.st_size,
                "mode": mode,
                "path": relative,
                "sha256": hashlib.sha256(payload).hexdigest(),
                "type": "file",
            })
            continue
        other += 1
        raise ValueError(f"EQ family unsupported filesystem type: {relative}")
    payload = json.dumps(
        rows,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return {
        "schema": TD_B_EQ_R6_MANIFEST_SCHEMA,
        "entries": len(rows),
        "files": files,
        "directories": directories,
        "symlinks": symlinks,
        "other": other,
        "payload_bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "rows": rows,
        "payload": payload,
    }


def audit_td_b_eq_r6_qualification(root: str | Path) -> dict[str, Any]:
    """Re-derive the accepted EQ-R6 Branch A result from retained evidence."""
    target = Path(root)
    if target != TD_B_EQ_R6_ACCEPTED_ROOT:
        raise ValueError("EQ-R6 qualification requires the exact accepted evidence root")
    manifest = build_planner_eq_family_manifest(target)
    expected_manifest = {
        "entries": 47,
        "files": 42,
        "directories": 5,
        "symlinks": 0,
        "other": 0,
        "payload_bytes": 7980,
        "sha256": TD_B_EQ_R6_MANIFEST_SHA256,
    }
    if any(manifest[key] != value for key, value in expected_manifest.items()):
        raise ValueError("EQ-R6 accepted evidence manifest drifted")
    artifacts: dict[str, dict[str, Any]] = {}
    for relative, expected_sha256 in TD_B_EQ_R6_ARTIFACT_SHA256.items():
        path = target / relative
        payload = path.read_bytes()
        actual_sha256 = hashlib.sha256(payload).hexdigest()
        if actual_sha256 != expected_sha256:
            raise ValueError(f"EQ-R6 qualification artifact drifted: {relative}")
        artifacts[relative] = json.loads(payload)
    outer = artifacts["run/outer-result.json"]
    outer_terminal = artifacts["run/candidate-1-outer-terminal.json"]
    result = artifacts["run/candidate-1/candidate-result.json"]
    seal = artifacts["run/candidate-1/terminal-seal.json"]
    classification = outer.get("classification")
    if (
        outer.get("status") != "qualified_1_2500"
        or classification != {
            "candidate_2_call_count": 0,
            "selected_shutter": "1/2500",
            "status": "qualified_1_2500",
        }
        or outer.get("retry") != 0
        or len(outer.get("candidate_launches", ())) != 1
        or outer["candidate_launches"][0].get("candidate_index") != 1
        or outer["candidate_launches"][0].get("return_code") != 0
        or (target / "run/candidate-2").exists()
    ):
        raise ValueError("EQ-R6 Branch A launch/classification contract failed")
    expected_counts = (4, 4, 4)
    for owner in (outer, result, seal):
        counts = (
            owner.get("attempted_capture_calls"),
            owner.get("physical_returned_cr3_count"),
            owner.get("accepted_capture_count"),
        )
        if counts != expected_counts:
            raise ValueError("EQ-R6 4/4/4 accounting contract failed")
    if (
        result.get("candidate_index") != 1
        or result.get("retry") != 0
        or seal.get("status") != "pass"
        or seal.get("classification") != "candidate_pass"
        or seal.get("code_checkpoint") != TD_B_EQ_R6_QUALIFICATION_CHECKPOINT
        or seal.get("wrapper_return_code") != 0
        or outer_terminal.get("status") != "pass"
        or outer_terminal.get("candidate_2_remained_locked") is not True
        or outer_terminal.get("final_zero", {}).get("status") != "pass"
    ):
        raise ValueError("EQ-R6 terminal seal contract failed")
    required_ids = tuple(
        json.loads(POLICY_PATH.read_text(encoding="utf-8"))["feature_set"]["ids"]
    )
    captures = result.get("captures")
    if (
        not isinstance(captures, list)
        or tuple(row.get("capture_id") for row in captures) != TD_B_EQ_CAPTURE_IDS[0]
    ):
        raise ValueError("EQ-R6 accepted capture IDs drifted")
    exposure_seconds: list[float] = []
    ratios: list[float] = []
    feature_counts: list[int] = []
    for capture in captures:
        failures = td_b_eq_capture_quality_failures(
            capture,
            required_feature_ids=required_ids,
        )
        if failures:
            raise ValueError(f"EQ-R6 accepted capture quality failed: {failures}")
        for evidence_name in ("cr3", "sidecar"):
            evidence = capture[evidence_name]
            evidence_path = Path(evidence["path"])
            if (
                evidence_path.is_symlink()
                or not evidence_path.resolve(strict=True).is_relative_to(
                    target.resolve(strict=True)
                )
            ):
                raise ValueError("EQ-R6 physical evidence path escaped or is unsafe")
            payload = evidence_path.read_bytes()
            if (
                len(payload) != evidence["bytes"]
                or hashlib.sha256(payload).hexdigest() != evidence["sha256"]
            ):
                raise ValueError("EQ-R6 physical evidence content drifted")
        recorded = capture["recorded_exposure"]
        if (
            recorded.get("source") != "Canon:ExposureTime"
            or recorded.get("nominal_shutter_speed") != "1/2500"
            or recorded.get("seconds") != 0.000387549084953174
            or recorded.get("recorded_to_nominal_ratio") != 0.9688727123829349
        ):
            raise ValueError("EQ-R6 recorded exposure contract drifted")
        exposure_seconds.append(recorded["seconds"])
        ratios.append(recorded["recorded_to_nominal_ratio"])
        feature_counts.append(len(capture["feature_quality"]))
    python_cleanup = json.loads(
        (target / "run/candidate-1/all-off-python.json").read_text(encoding="utf-8")
    )
    shell_cleanup = json.loads(
        (target / "run/candidate-1/all-off-shell.json").read_text(encoding="utf-8")
    )
    final_zero = json.loads(
        (target / "run/candidate-1/independent-final-zero.json").read_text(encoding="utf-8")
    )
    if (
        python_cleanup.get("status") != "pass"
        or any(step.get("ok") is not True for step in python_cleanup.get("steps", ()))
        or any(step.get("ok") is not True for step in shell_cleanup)
        or final_zero.get("status") != "pass"
        or final_zero.get("ray_verified_off") is not True
        or final_zero.get("strip_verified_off") is not True
    ):
        raise ValueError("EQ-R6 cleanup/final-zero contract failed")
    return {
        "status": "qualified_1_2500",
        "selected_shutter": "1/2500",
        "candidate_launch_count": 1,
        "candidate_2_call_count": 0,
        "attempted_capture_calls": 4,
        "physical_returned_cr3_count": 4,
        "accepted_capture_count": 4,
        "capture_ids": list(TD_B_EQ_CAPTURE_IDS[0]),
        "feature_counts": feature_counts,
        "recorded_exposure_owner": "Canon:ExposureTime",
        "recorded_exposure_seconds": exposure_seconds,
        "recorded_exposure_min_seconds": min(exposure_seconds),
        "recorded_exposure_max_seconds": max(exposure_seconds),
        "recorded_to_nominal_ratio": ratios[0],
        "retry": 0,
        "manifest": {
            key: manifest[key]
            for key in (
                "schema", "entries", "files", "directories", "symlinks",
                "other", "payload_bytes", "sha256",
            )
        },
    }


def expected_native_raw_ambient_policy(
    experiment_id: str,
    *,
    plan_schema: str,
    phase: str = "formal",
) -> str:
    if (
        experiment_id == TD_B
        and plan_schema == PLAN_SCHEMA_V2
        and phase == "formal"
    ):
        return AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT
    return AMBIENT_POLICY_REQUIRE_PRECEDING


def file_reference(path: str | Path) -> dict[str, str]:
    target = Path(path)
    return {"path": str(target), "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}


def _redacted_finding(kind: str, *, path: str, value: str) -> dict[str, str]:
    return {
        "path": path,
        "kind": kind,
        "redacted_sha256": hashlib.sha256(value.encode("utf-8")).hexdigest(),
    }


def scan_td_b_r6_offline_sources(
    current_sources: Mapping[str, str],
    *,
    baseline_sources: Mapping[str, str],
    expected_baseline_sha256: Mapping[str, str],
    allowed_paths: Sequence[str],
    allowed_absolute_roots: Sequence[str | Path],
    symlink_paths: Sequence[str] = (),
) -> dict[str, Any]:
    """Fail-closed source scan with one exact baseline identifier exception.

    The exception is deliberately limited to an identifier name already present
    in the exact HEAD blob. Literal values, environment access, network targets,
    unsafe paths and symlinks are always findings.
    """
    allowed = set(allowed_paths)
    roots = tuple(Path(root).resolve(strict=False) for root in allowed_absolute_roots)
    findings: list[dict[str, str]] = []
    classifications: list[dict[str, Any]] = []
    for relative, text in sorted(current_sources.items()):
        if relative not in allowed:
            findings.append({"path": relative, "kind": "path_outside_changed_allowlist"})
            continue
        baseline = baseline_sources.get(relative)
        expected_hash = expected_baseline_sha256.get(relative)
        baseline_hash = (
            hashlib.sha256(baseline.encode("utf-8")).hexdigest()
            if baseline is not None else None
        )
        current_identifier_count = text.count(TD_B_R6_PRIVATE_OVERRIDE_IDENTIFIER)
        baseline_identifier_count = (
            baseline.count(TD_B_R6_PRIVATE_OVERRIDE_IDENTIFIER)
            if baseline is not None else 0
        )
        if current_identifier_count:
            exact_baseline = (
                baseline is not None
                and expected_hash is not None
                and baseline_hash == expected_hash
                and current_identifier_count == baseline_identifier_count
            )
            classification = {
                "path": relative,
                "kind": "private_override_name",
                "occurrences": current_identifier_count,
                "baseline_occurrences": baseline_identifier_count,
                "baseline_sha256": baseline_hash,
                "expected_baseline_sha256": expected_hash,
                "classification": (
                    "known_identifier_not_secret_value"
                    if exact_baseline else "new_or_unproven_identifier"
                ),
            }
            classifications.append(classification)
            if not exact_baseline:
                findings.append({
                    "path": relative,
                    "kind": "new_or_unproven_private_override_name",
                })
        for match in _TD_B_R6_LITERAL_PRIVATE_VALUE_RE.finditer(text):
            findings.append(_redacted_finding(
                "literal_credential_or_private_value",
                path=relative,
                value=match.group(0),
            ))
        for match in _TD_B_R6_ENV_READ_RE.finditer(text):
            findings.append({
                "path": relative,
                "kind": "environment_value_read_or_serialization",
                "redacted_sha256": hashlib.sha256(
                    match.group(0).encode("utf-8")
                ).hexdigest(),
            })
        for match in _TD_B_R6_NETWORK_TARGET_RE.finditer(text):
            findings.append(_redacted_finding(
                "network_target",
                path=relative,
                value=match.group(0),
            ))
        for match in _TD_B_R6_ABSOLUTE_PATH_RE.finditer(text):
            candidate = Path(match.group(0)).resolve(strict=False)
            if not any(candidate == root or root in candidate.parents for root in roots):
                findings.append({
                    "path": relative,
                    "kind": "absolute_path_outside_allowed_local_roots",
                    "redacted_sha256": hashlib.sha256(
                        str(candidate).encode("utf-8")
                    ).hexdigest(),
                })
    for relative in sorted(symlink_paths):
        findings.append({"path": relative, "kind": "symlink_escape_or_unsafe_path"})
    return {
        "schema": "p7_td_b_r6_baseline_aware_secret_path_scan_v2",
        "status": "pass" if not findings else "fail",
        "scanned_paths": sorted(current_sources),
        "baseline_identifier_classifications": classifications,
        "findings": findings,
        "private_override_values_read": False,
        "environment_values_serialized": False,
        "network_targets_added": False,
    }


def build_td_b_r6_pre_eq_validation_summary(
    artifact_references: Sequence[Mapping[str, Any]],
    *,
    case_results: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Derive the pre-terminal summary from exactly eleven frozen artifacts."""
    names = tuple(Path(str(item.get("path", ""))).name for item in artifact_references)
    child_failures = [
        {"case": str(item.get("case")), "status": str(item.get("status"))}
        for item in case_results if item.get("status") != "pass"
    ]
    reference_failure = (
        len(artifact_references) != 11
        or names != TD_B_R6_PRE_EQ_PRE_SUMMARY_ARTIFACTS
        or any(
            not isinstance(item.get("bytes"), int)
            or item["bytes"] <= 0
            or not re.fullmatch(r"[0-9a-f]{64}", str(item.get("sha256", "")))
            for item in artifact_references
        )
    )
    if reference_failure:
        child_failures.append({"case": "pre_summary_artifact_index", "status": "fail"})
    return {
        "schema": "p7_td_b_r6_pre_eq_validation_summary_v2",
        "status": "pass" if not child_failures else "fail",
        "indexed_preterminal_count": 11,
        "artifacts": [dict(item) for item in artifact_references],
        "cases": [dict(item) for item in case_results],
        "failures": child_failures,
    }


def build_td_b_r6_pre_eq_terminal_summary(
    validation_reference: Mapping[str, Any],
    *,
    validation_status: str,
) -> dict[str, Any]:
    """Build the non-recursive terminal record; its own hash stays external."""
    validation_ok = (
        Path(str(validation_reference.get("path", ""))).name == "validation-summary.json"
        and isinstance(validation_reference.get("bytes"), int)
        and validation_reference["bytes"] > 0
        and re.fullmatch(r"[0-9a-f]{64}", str(validation_reference.get("sha256", "")))
        and validation_status == "pass"
    )
    return {
        "schema": "p7_td_b_r6_pre_eq_terminal_summary_v2",
        "status": "pass" if validation_ok else "fail",
        "canonical_root_json_count": 13,
        "indexed_preterminal_count": 11,
        "validation_summary_count": 1,
        "terminal_self_count": 1,
        "validation_summary": dict(validation_reference),
        "terminal_self": {
            "path": "terminal-summary.json",
            "hash_owner": "external_execution_handoff",
        },
    }


def validate_td_b_r6_pre_eq_terminal_seal(
    root: str | Path,
    *,
    external_terminal_sha256: str,
) -> dict[str, Any]:
    """Independently validate the exact thirteen-file terminal package."""
    target = Path(root)
    findings: list[str] = []
    if target.is_symlink() or not target.is_dir():
        findings.append("unsafe_or_missing_root")
        names: tuple[str, ...] = ()
    else:
        entries = sorted(target.iterdir(), key=lambda item: item.name)
        names = tuple(item.name for item in entries)
        if any(item.is_symlink() or not item.is_file() for item in entries):
            findings.append("unsafe_or_non_file_entry")
    if names != tuple(sorted(TD_B_R6_PRE_EQ_CANONICAL_ARTIFACTS)):
        findings.append("canonical_name_or_count_mismatch")
    parsed: dict[str, Any] = {}
    if not findings:
        for name in names:
            try:
                parsed[name] = json.loads((target / name).read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError):
                findings.append(f"strict_json_failure:{name}")
    validation = parsed.get("validation-summary.json", {})
    for item in validation.get("artifacts", ()):
        path = target / Path(str(item.get("path", ""))).name
        if (
            path.name not in TD_B_R6_PRE_EQ_PRE_SUMMARY_ARTIFACTS
            or not path.is_file()
            or path.stat().st_size != item.get("bytes")
            or hashlib.sha256(path.read_bytes()).hexdigest() != item.get("sha256")
        ):
            findings.append(f"stale_preterminal_reference:{path.name}")
    terminal_path = target / "terminal-summary.json"
    if terminal_path.is_file():
        actual_terminal_hash = hashlib.sha256(terminal_path.read_bytes()).hexdigest()
        if actual_terminal_hash != external_terminal_sha256:
            findings.append("external_terminal_hash_mismatch")
    terminal = parsed.get("terminal-summary.json", {})
    if validation.get("indexed_preterminal_count") != 11:
        findings.append("validation_count_mismatch")
    if terminal.get("canonical_root_json_count") != 13:
        findings.append("terminal_root_count_mismatch")
    if terminal.get("indexed_preterminal_count") != 11:
        findings.append("terminal_indexed_count_mismatch")
    if terminal.get("validation_summary_count") != 1 or terminal.get("terminal_self_count") != 1:
        findings.append("terminal_phase_count_mismatch")
    if terminal.get("terminal_self") != {
        "path": "terminal-summary.json",
        "hash_owner": "external_execution_handoff",
    }:
        findings.append("terminal_self_owner_mismatch")
    validation_path = target / "validation-summary.json"
    validation_ref = terminal.get("validation_summary", {})
    if validation_path.is_file() and (
        validation_ref.get("bytes") != validation_path.stat().st_size
        or validation_ref.get("sha256")
        != hashlib.sha256(validation_path.read_bytes()).hexdigest()
    ):
        findings.append("terminal_validation_reference_mismatch")
    if terminal.get("status") != validation.get("status"):
        findings.append("terminal_cannot_override_validation_status")
    return {
        "schema": "p7_td_b_r6_pre_eq_external_terminal_seal_v1",
        "status": "pass" if not findings else "fail",
        "canonical_root_json_count": len(names),
        "terminal_sha256": external_terminal_sha256,
        "findings": findings,
    }


def validate_td_b_r6_pre_eq_handoff(
    validation_summary: Mapping[str, Any],
    terminal_summary: Mapping[str, Any],
    handoff: Mapping[str, Any],
) -> dict[str, Any]:
    """Reject any prose handoff that contradicts the frozen machine status."""
    expected = {
        "validation_status": validation_summary.get("status"),
        "indexed_preterminal_count": validation_summary.get("indexed_preterminal_count"),
        "terminal_status": terminal_summary.get("status"),
        "canonical_root_json_count": terminal_summary.get("canonical_root_json_count"),
    }
    mismatches = [
        key for key, value in expected.items() if handoff.get(key) != value
    ]
    if expected["validation_status"] != "pass" and handoff.get("first_sentence_kind") != "failure":
        mismatches.append("first_sentence_kind")
    return {
        "schema": "p7_td_b_r6_pre_eq_handoff_consistency_v1",
        "status": "pass" if not mismatches else "fail",
        "expected": expected,
        "mismatches": sorted(set(mismatches)),
    }


def load_td_b_exposure_policy_v2(
    path: str | Path = TD_B_EXPOSURE_POLICY_V2_PATH,
) -> dict[str, Any]:
    """Load and validate the single versioned R6 exposure-policy owner."""
    target = Path(path)
    if target.resolve(strict=True) != TD_B_EXPOSURE_POLICY_V2_PATH.resolve(strict=True):
        raise ValueError("TD-B exposure policy must use the repository-owned v2 artifact")
    policy = json.loads(target.read_text(encoding="utf-8"))
    if policy.get("schema") != TD_B_EXPOSURE_POLICY_V2_SCHEMA:
        raise ValueError("unsupported TD-B exposure policy schema")
    if policy.get("supersedes") != TD_B_R5_SHUTTERS_SHA256:
        raise ValueError("TD-B exposure policy does not supersede the exact R5 shutter ledger")
    superseded = policy.get("superseded_plan")
    if not isinstance(superseded, Mapping) or superseded.get("sha256") != TD_B_R5_PLAN_SHA256:
        raise ValueError("TD-B exposure policy lacks exact R5 plan provenance")
    if policy.get("iso") != 100 or policy.get("aperture") != "implicit_auto":
        raise ValueError("TD-B exposure policy camera settings drifted")
    if policy.get("actual_exposure_owner") != "Canon:ExposureTime":
        raise ValueError("TD-B recorded exposure owner drifted")
    states = policy.get("states")
    expected = {"A": "1/5000", "D": "1/6400", "B": "1/8000"}
    if not isinstance(states, Mapping) or any(
        not isinstance(states.get(state), Mapping)
        or states[state].get("formal_shutter") != shutter
        or states[state].get("source") != "exact_r5_frozen_plan"
        for state, shutter in expected.items()
    ):
        raise ValueError("TD-B A/D/B shutters differ from exact R5 provenance")
    c_state = states.get("C")
    if (
        not isinstance(c_state, Mapping)
        or c_state.get("status") != "qualified"
        or tuple(c_state.get("nominal_candidates", ())) != TD_B_EQ_CANDIDATES
        or c_state.get("formal_shutter") != "1/2500"
    ):
        raise ValueError("TD-B C exposure differs from exact accepted EQ qualification")
    if (
        policy.get("r5_failure_class") != TD_B_R5_FAILURE_CLASS
        or policy.get("exposure_qualification_status") != "qualified_1_2500"
        or policy.get("selected_state_c_nominal_shutter") != "1/2500"
        or policy.get("selected_state_c_recorded_exposure_range") != {
            "owner": "Canon:ExposureTime",
            "min_seconds": 0.000387549084953174,
            "max_seconds": 0.000387549084953174,
        }
    ):
        raise ValueError("TD-B selected C exposure qualification drifted")
    provenance = policy.get("provenance")
    policy_ids = json.loads(POLICY_PATH.read_text(encoding="utf-8"))["feature_set"]["ids"]
    if (
        not isinstance(provenance, Mapping)
        or provenance.get("observer_sha256") != hashlib.sha256(OBSERVER_PATH.read_bytes()).hexdigest()
        or provenance.get("hsi_policy_sha256") != hashlib.sha256(POLICY_PATH.read_bytes()).hexdigest()
        or provenance.get("operating_envelope_sha256") != OPERATING_ENVELOPE_V2_SHA256
        or provenance.get("uncertainty_sha256") != hashlib.sha256(UNCERTAINTY_PATH.read_bytes()).hexdigest()
        or provenance.get("feature_count") != 58
        or provenance.get("feature_ids_sha256") != canonical_sha256(policy_ids)
        or provenance.get("feature_ids_sha256") != TD_B_FEATURE_IDS_SHA256
    ):
        raise ValueError("TD-B exposure policy scientific provenance drifted")
    eq_provenance = provenance.get("eq_r6_qualification")
    expected_artifacts = [
        {"path": path, "sha256": sha256}
        for path, sha256 in TD_B_EQ_R6_ARTIFACT_SHA256.items()
    ]
    if (
        not isinstance(eq_provenance, Mapping)
        or eq_provenance.get("root") != str(TD_B_EQ_R6_ACCEPTED_ROOT)
        or eq_provenance.get("qualification_checkpoint") != "f37517a"
        or eq_provenance.get("code_checkpoint") != TD_B_EQ_R6_QUALIFICATION_CHECKPOINT
        or eq_provenance.get("artifacts") != expected_artifacts
        or tuple(eq_provenance.get("capture_ids", ())) != TD_B_EQ_CAPTURE_IDS[0]
        or eq_provenance.get("manifest") != {
            "schema": TD_B_EQ_R6_MANIFEST_SCHEMA,
            "entries": 47,
            "files": 42,
            "directories": 5,
            "symlinks": 0,
            "other": 0,
            "payload_bytes": 7980,
            "sha256": TD_B_EQ_R6_MANIFEST_SHA256,
        }
    ):
        raise ValueError("TD-B EQ-R6 qualification provenance drifted")
    prohibited_claims = {
        "formal_pass", "td_b_pass", "history_pass", "release_usable",
        "production_release_usable", "product_ready", "state_c_settled",
    }
    if prohibited_claims.intersection(policy):
        raise ValueError("TD-B exposure policy contains a prohibited downstream claim")
    if policy.get("old_new_frame_combination") != "prohibited":
        raise ValueError("TD-B exposure policy must prohibit old/new pooling")
    return policy


def build_td_b_eq_r6_plan(
    policy: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the non-executable EQ-R6 contract consumed by the existing runner."""
    exposure = dict(policy or load_td_b_exposure_policy_v2())
    validate_td_b_exposure_policy_v2(exposure)
    candidates = []
    for index, (shutter, capture_ids) in enumerate(zip(TD_B_EQ_CANDIDATES, TD_B_EQ_CAPTURE_IDS), start=1):
        candidates.append({
            "candidate_index": index,
            "nominal_shutter": shutter,
            "capture_ids": list(capture_ids),
            "slots_s": list(TIMED_POINTS),
            "precondition": {
                "strip_generation_bearing_zero": True,
                "ray_a_command": dict(RAY_STATES["A"]),
                "ray_a_dwell_s": 600,
                "ray_a_capture_count": 0,
                "transition_to_c": dict(RAY_STATES["C"]),
            },
        })
    return {
        "schema": "p7_td_b_eq_r6_plan_v1",
        "status": "offline_contract_only",
        "executable": False,
        "experiment_id": TD_B_EQ_R6_EXPERIMENT_ID,
        "source": "ray",
        "strip": "generation_bearing_zero",
        "formal": 0,
        "ambient": 0,
        "retry": 0,
        "candidate_count_cap": 2,
        "candidate_physical": 4,
        "setup_physical_cap": 8,
        "candidates": candidates,
        "cleanup": {
            "python": "required",
            "shell": "required",
            "independent_final_zero": "required",
            "terminal_seal": "required",
        },
        "policy_sha256": hashlib.sha256(TD_B_EXPOSURE_POLICY_V2_PATH.read_bytes()).hexdigest(),
    }


def validate_td_b_exposure_policy_v2(policy: Mapping[str, Any]) -> None:
    """Validate an in-memory policy without permitting a compatibility variant."""
    owner = load_td_b_exposure_policy_v2()
    if dict(policy) != owner:
        raise ValueError("in-memory TD-B exposure policy differs from the repository owner")


def validate_td_b_eq_r6_plan(plan: Mapping[str, Any]) -> None:
    expected = build_td_b_eq_r6_plan(load_td_b_exposure_policy_v2())
    if dict(plan) != expected:
        raise ValueError("EQ-R6 plan differs from the exact bounded offline contract")


def activate_td_b_eq_r6_live_plan(
    offline_plan: Mapping[str, Any],
    *,
    code_checkpoint: str,
    output_root: str | Path,
    wrapper_path: str | Path,
    measurement_runner_path: str | Path,
) -> dict[str, Any]:
    """Bind the exact offline EQ contract to one fresh production owner.

    Activation is intentionally side-effect free: the output root must not yet
    exist, and callers remain responsible for creating it only after validating
    this returned contract.
    """
    validate_td_b_eq_r6_plan(offline_plan)
    if not isinstance(code_checkpoint, str) or len(code_checkpoint) != 40:
        raise ValueError("EQ-R6 activation requires an exact Git checkpoint")
    try:
        int(code_checkpoint, 16)
    except ValueError as exc:
        raise ValueError("EQ-R6 activation checkpoint is not hexadecimal") from exc
    root = Path(output_root)
    if not root.is_absolute() or root.exists() or root.is_symlink():
        raise ValueError("EQ-R6 activation requires one fresh absolute non-symlink root")
    resolved_root = root.resolve(strict=False)
    allowed_root = Path("/Volumes/4T/temp/rgbww-optimizer").resolve(strict=True)
    if not resolved_root.is_relative_to(allowed_root):
        raise ValueError("EQ-R6 output owner is outside the approved temporary root")
    for parent in (root, *root.parents):
        if parent.resolve(strict=False) == allowed_root.parent:
            break
        if parent.exists() and parent.is_symlink():
            raise ValueError("EQ-R6 output owner has a symlink ancestor")
    wrapper = Path(wrapper_path).resolve(strict=True)
    measurement_runner = Path(measurement_runner_path).resolve(strict=True)
    if wrapper.is_symlink() or measurement_runner.is_symlink():
        raise ValueError("EQ-R6 production owner source cannot be a symlink")
    return _build_td_b_eq_r6_live_plan(
        offline_plan,
        code_checkpoint=code_checkpoint,
        resolved_root=resolved_root,
        wrapper=wrapper,
        measurement_runner=measurement_runner,
    )


def _build_td_b_eq_r6_live_plan(
    offline_plan: Mapping[str, Any],
    *,
    code_checkpoint: str,
    resolved_root: Path,
    wrapper: Path,
    measurement_runner: Path,
) -> dict[str, Any]:
    return {
        "schema": TD_B_EQ_R6_LIVE_PLAN_SCHEMA,
        "status": "live_bound_not_started",
        "executable": True,
        "experiment_id": TD_B_EQ_R6_EXPERIMENT_ID,
        "code_checkpoint": code_checkpoint,
        "output_root": str(resolved_root),
        "offline_plan": dict(offline_plan),
        "offline_plan_sha256": canonical_sha256(offline_plan),
        "exposure_policy": file_reference(TD_B_EXPOSURE_POLICY_V2_PATH),
        "thermal_contract": file_reference(Path(__file__)),
        "measurement_runner": file_reference(measurement_runner),
        "production_wrapper": file_reference(wrapper),
        "candidate_order": [1, 2],
        "physical_cr3_cap": 8,
        "candidate_physical_cap": 4,
        "formal": 0,
        "ambient": 0,
        "retry": 0,
        "candidate_2_unlock": "candidate_1_first_failure_exactly_clipping_after_terminal_seal",
        "cleanup": {
            "python": "required",
            "shell": "required",
            "independent_final_zero": "required",
            "terminal_seal": "required",
        },
    }


def validate_td_b_eq_r6_live_plan(
    plan: Mapping[str, Any],
    *,
    require_fresh_root: bool,
) -> None:
    """Reject any live binding or scientific-contract drift before adapters."""
    if plan.get("schema") != TD_B_EQ_R6_LIVE_PLAN_SCHEMA:
        raise ValueError("unsupported EQ-R6 live plan schema")
    offline = plan.get("offline_plan")
    if not isinstance(offline, Mapping):
        raise ValueError("EQ-R6 live plan lacks its offline contract")
    validate_td_b_eq_r6_plan(offline)
    wrapper_ref = plan.get("production_wrapper")
    runner_ref = plan.get("measurement_runner")
    policy_ref = plan.get("exposure_policy")
    thermal_ref = plan.get("thermal_contract")
    for name, reference in (
        ("production wrapper", wrapper_ref),
        ("measurement runner", runner_ref),
        ("exposure policy", policy_ref),
        ("thermal contract", thermal_ref),
    ):
        if not isinstance(reference, Mapping) or set(reference) != {"path", "sha256"}:
            raise ValueError(f"EQ-R6 {name} reference is malformed")
        path = Path(str(reference["path"]))
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"EQ-R6 {name} owner is missing or unsafe")
        if hashlib.sha256(path.read_bytes()).hexdigest() != reference["sha256"]:
            raise ValueError(f"EQ-R6 {name} hash drifted")
    root = Path(str(plan.get("output_root", "")))
    if not root.is_absolute() or root.is_symlink():
        raise ValueError("EQ-R6 live root is invalid")
    allowed_root = Path("/Volumes/4T/temp/rgbww-optimizer").resolve(strict=True)
    if not root.resolve(strict=False).is_relative_to(allowed_root):
        raise ValueError("EQ-R6 live root is outside the approved temporary root")
    checkpoint = plan.get("code_checkpoint")
    if (
        not isinstance(checkpoint, str)
        or len(checkpoint) != 40
        or any(character not in "0123456789abcdef" for character in checkpoint)
    ):
        raise ValueError("EQ-R6 live checkpoint is invalid")
    if require_fresh_root and root.exists():
        raise ValueError("EQ-R6 live root is not fresh")
    expected = _build_td_b_eq_r6_live_plan(
        offline,
        code_checkpoint=str(plan.get("code_checkpoint", "")),
        resolved_root=root.resolve(strict=False),
        wrapper=Path(str(wrapper_ref["path"])).resolve(strict=True),
        measurement_runner=Path(str(runner_ref["path"])).resolve(strict=True),
    )
    if dict(plan) != expected:
        raise ValueError("EQ-R6 live plan differs from its unique production binding")


def td_b_eq_capture_quality_failures(
    capture: Mapping[str, Any],
    *,
    required_feature_ids: Sequence[str],
) -> tuple[str, ...]:
    """Apply the frozen 58-feature and engineering gates to one EQ return."""
    required = tuple(str(value) for value in required_feature_ids)
    if len(required) != 58 or canonical_sha256(list(required)) != TD_B_FEATURE_IDS_SHA256:
        raise ValueError("EQ-R6 requires the exact ordered 58-feature owner")
    failures: list[str] = []
    if capture.get("physical_return_persisted_before_postprocessing") is not True:
        failures.append("physical_return_evidence")
    for evidence_name in ("cr3", "sidecar"):
        evidence = capture.get(evidence_name)
        if (
            not isinstance(evidence, Mapping)
            or not isinstance(evidence.get("path"), str)
            or not evidence.get("path")
            or int(evidence.get("bytes", 0)) <= 0
            or not isinstance(evidence.get("sha256"), str)
            or len(evidence.get("sha256", "")) != 64
        ):
            failures.append(f"{evidence_name}_evidence")
    if not capture.get("remote_capture_id") or not capture.get("remote_request_id"):
        failures.append("remote_ids")
    recorded = capture.get("recorded_exposure")
    if (
        not isinstance(recorded, Mapping)
        or recorded.get("source") != "Canon:ExposureTime"
        or recorded.get("status") != "recorded"
        or not math.isfinite(float(recorded.get("seconds", math.nan)))
    ):
        failures.append("recorded_exposure")
    if capture.get("nominal_recorded_ratio_gate") != "pass":
        failures.append("nominal_recorded_ratio")
    for gate in (
        "ray_command_readback", "strip_zero", "source_isolation",
        "timing_chronology", "no_stale", "budget_accounting",
    ):
        if capture.get(gate) != "pass":
            failures.append(gate)
    quality = capture.get("feature_quality")
    if not isinstance(quality, Mapping) or tuple(quality) != required:
        failures.append("required_58_features")
        return tuple(failures)
    for feature_id in required:
        row = quality[feature_id]
        if not isinstance(row, Mapping):
            failures.append("required_58_features")
            continue
        value = row.get("value")
        if value is None or not math.isfinite(float(value)):
            failures.append("nonfinite")
        if float(row.get("clipped_fraction", math.inf)) != 0.0:
            failures.append("clipping")
        if float(row.get("near_noise_floor_fraction", math.inf)) > 0.05:
            failures.append("near_noise")
        if int(row.get("valid_pixel_count", -1)) < 29000:
            failures.append("valid_pixel")
    return tuple(sorted(set(failures)))


def classify_td_b_eq_r6(
    candidate_results: Sequence[Sequence[Mapping[str, Any]]],
    *,
    required_feature_ids: Sequence[str],
) -> dict[str, Any]:
    """Classify the exact two-candidate gate, including the sole C2 unlock."""
    if not candidate_results or len(candidate_results) > 2:
        raise ValueError("EQ-R6 requires one or at most two candidate result ledgers")
    first_failures = [
        td_b_eq_capture_quality_failures(row, required_feature_ids=required_feature_ids)
        for row in candidate_results[0]
    ]
    if not first_failures or len(first_failures) > 4:
        raise ValueError("candidate 1 must contain one to four returned slots")
    first_bad = next((item for item in first_failures if item), None)
    if first_bad is None:
        if len(first_failures) != 4 or len(candidate_results) != 1:
            raise ValueError("qualified candidate 1 requires 4/4 and zero candidate 2 calls")
        return {"status": "qualified_1_2500", "selected_shutter": "1/2500", "candidate_2_call_count": 0}
    if set(first_bad) != {"clipping"}:
        if len(candidate_results) != 1:
            raise ValueError("non-clipping candidate 1 failure prohibits candidate 2")
        return {"status": "run_invalid", "selected_shutter": None, "candidate_2_call_count": 0}
    if first_failures.index(first_bad) != len(first_failures) - 1:
        raise ValueError("candidate 1 continued after its first clipping failure")
    if len(candidate_results) != 2:
        return {"status": "candidate_2_required", "selected_shutter": None, "candidate_2_call_count": 0}
    second_failures = [
        td_b_eq_capture_quality_failures(row, required_feature_ids=required_feature_ids)
        for row in candidate_results[1]
    ]
    if not second_failures or len(second_failures) > 4:
        raise ValueError("candidate 2 requires one to four returned slots")
    second_bad = next((item for item in second_failures if item), None)
    if second_bad is not None:
        if second_failures.index(second_bad) != len(second_failures) - 1:
            raise ValueError("candidate 2 continued after its first failure")
        return {
            "status": "exposure_window_unresolved",
            "selected_shutter": None,
            "candidate_2_call_count": len(second_failures),
        }
    if len(second_failures) != 4:
        raise ValueError("qualified candidate 2 requires exactly four returned slots")
    return {"status": "qualified_1_3200", "selected_shutter": "1/3200", "candidate_2_call_count": 4}


def build_td_b_r6_formal_plan(
    policy: Mapping[str, Any] | None = None,
    *,
    selected_c_shutter: str | None = None,
) -> dict[str, Any]:
    exposure = dict(policy or load_td_b_exposure_policy_v2())
    validate_td_b_exposure_policy_v2(exposure)
    if selected_c_shutter is not None:
        raise ValueError("caller cannot override the repository-selected C shutter")
    shutters = {
        "A": exposure["states"]["A"]["formal_shutter"],
        "D": exposure["states"]["D"]["formal_shutter"],
        "B": exposure["states"]["B"]["formal_shutter"],
        "C": exposure["states"]["C"]["formal_shutter"],
    }
    return {
        "schema": "p7_td_b_ray_r6_formal_plan_v1",
        "status": "selected_exposure_policy_non_executable",
        "executable": False,
        "experiment_id": TD_B_R6_EXPERIMENT_ID,
        "source": "ray",
        "strip": "zero_throughout",
        "ambient": 0,
        "formal_logical": 16,
        "formal_physical_cap": 16,
        "setup_in_formal_root": 0,
        "launch": 1,
        "retry": 0,
        "capture_ids": list(TD_B_R6_CAPTURE_IDS),
        "state_shutters": shutters,
        "c_policy_status": "qualified",
        "old_new_frame_combination": "prohibited",
        "failure_contract": {
            "classification": "accepted_hard_failed_formal_attempt",
            "formal_pass": False,
            "strip_call_count": 0,
            "retry": 0,
        },
    }


def validate_td_b_r6_formal_plan(plan: Mapping[str, Any]) -> None:
    expected = build_td_b_r6_formal_plan()
    if dict(plan) != expected:
        raise ValueError("Ray R6 plan differs from the exact selected-policy contract")


def validate_td_b_r6_capture_ledger(
    rows: Sequence[Mapping[str, Any]],
    *,
    required_feature_ids: Sequence[str],
    selected_c_shutter: str,
) -> None:
    if selected_c_shutter not in TD_B_EQ_CANDIDATES:
        raise ValueError("Ray R6 requires one exact EQ-selected C shutter")
    if len(rows) != 16 or tuple(str(row.get("capture_id")) for row in rows) != TD_B_R6_CAPTURE_IDS:
        raise ValueError("Ray R6 requires exact 000..015 order with no skip/resume")
    roots = {str(row.get("run_root")) for row in rows}
    if len(roots) != 1 or "" in roots:
        raise ValueError("Ray R6 capture ledger cannot pool roots")
    if any(row.get("origin") != "ray_r6" for row in rows):
        raise ValueError("R5 or cross-run frame pooling is prohibited")
    policy = load_td_b_exposure_policy_v2()
    expected_shutters = {
        state: policy["states"][state]["formal_shutter"] for state in ("A", "D", "B")
    }
    expected_shutters["C"] = selected_c_shutter
    for row in rows:
        capture_id = str(row["capture_id"])
        if "-ray-a" in capture_id:
            state = "A"
        elif "-ray-d-" in capture_id:
            state = "D"
        elif "-ray-b-" in capture_id:
            state = "B"
        elif "-ray-c-" in capture_id:
            state = "C"
        else:
            raise ValueError("Ray R6 capture ID has no exact state owner")
        if (
            row.get("state_id") != state
            or row.get("nominal_shutter") != expected_shutters[state]
            or row.get("exposure_mode") != "fixed"
            or row.get("weak_reacquire") is not False
            or row.get("mid_run_shutter_change") is not False
        ):
            raise ValueError("Ray R6 state/shutter contract drifted")
        failures = td_b_eq_capture_quality_failures(
            row, required_feature_ids=required_feature_ids,
        )
        if failures:
            raise ValueError(f"Ray R6 capture failed required gates: {failures}")


def td_b_r6_machine_status() -> dict[str, Any]:
    return {
        "r5": {
            "failure_class": TD_B_R5_FAILURE_CLASS,
            "formal_pass": False,
            "retained_11_use": "diagnostic_only",
            "old_new_combination": "prohibited",
        },
        "exposure_qualification": {
            "status": "pending", "slots_s": list(TIMED_POINTS), "physical_cap": 8,
        },
        "ray_r6": {
            "formal_planned": 16, "formal_accepted": 0, "retry": 0,
            "return_anchor_history": "not_evaluated",
        },
        "operating_envelope": {
            "dwell_s": 600,
            "claim": "selected_fixed_time_transient_not_proven_steady",
            "steady_status": "not_demonstrated",
        },
        "locks": {
            "strip": "blocked_until_ray_r6_pass",
            "td_c": "blocked_until_combined_td_b_pass",
            "sentinel": True,
            "p8": True,
        },
    }


def resolve_trusted_operating_envelope(
    path: str | Path, *, require_v2: bool = False,
) -> dict[str, Any]:
    """Resolve the repo-owned operating envelope without trusting caller path spelling."""
    requested = Path(path)
    if ".." in requested.parts:
        raise ValueError("operating envelope path traversal is prohibited")

    project_root = PROJECT_ROOT.resolve()
    candidate = requested if requested.is_absolute() else PROJECT_ROOT / requested
    if not candidate.is_relative_to(project_root):
        raise ValueError("operating envelope path is outside the project")

    current = project_root
    for part in candidate.relative_to(project_root).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("operating envelope path cannot contain a symlink")
    if not candidate.exists():
        raise ValueError("operating envelope artifact is missing")
    if not candidate.is_file():
        raise ValueError("operating envelope artifact is not a regular file")

    canonical = candidate.resolve(strict=True)
    expected_v1 = OPERATING_ENVELOPE_PATH.resolve(strict=True)
    expected_v2 = OPERATING_ENVELOPE_V2_PATH.resolve(strict=True)
    allowed = {expected_v2} if require_v2 else {expected_v1, expected_v2}
    if canonical not in allowed:
        raise ValueError("operating envelope path differs from the trusted repository owner")

    sha256 = hashlib.sha256(canonical.read_bytes()).hexdigest()
    if canonical == expected_v2 and sha256 != OPERATING_ENVELOPE_V2_SHA256:
        raise ValueError("operating envelope frozen hash drift")
    try:
        envelope = json.loads(canonical.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("operating envelope artifact is not valid JSON") from exc
    if not isinstance(envelope, dict):
        raise ValueError("operating envelope artifact must be a JSON object")
    mode = validate_operating_envelope(
        envelope, artifact_path=canonical, require_v2=require_v2,
    )
    return {
        "path": canonical,
        "reference": {"path": str(canonical), "sha256": sha256},
        "envelope": envelope,
        "mode": mode,
    }


def validate_trusted_operating_envelope_reference(
    reference: Mapping[str, Any], *, require_v2: bool = False,
) -> dict[str, Any]:
    """Replay a plan reference against the trusted path owner and retained hash."""
    if not isinstance(reference, Mapping) or set(reference) != {"path", "sha256"}:
        raise ValueError("operating envelope reference schema differs")
    resolved = resolve_trusted_operating_envelope(
        str(reference["path"]), require_v2=require_v2,
    )
    if reference.get("sha256") != resolved["reference"]["sha256"]:
        raise ValueError("operating envelope reference hash differs")
    return resolved


def validate_operating_envelope(
    envelope: Mapping[str, Any], *, artifact_path: str | Path | None = None,
    require_v2: bool = False,
) -> dict[str, Any]:
    """Validate the sole v1/v2 operating-envelope trust boundary."""
    schema = envelope.get("schema")
    if schema == "p7_operating_envelope_v1":
        if require_v2:
            raise ValueError("TD-B developer dwell requires the explicit v2 operating envelope")
        return {"mode": "legacy_v1", "operational_dwell_s": None, "scientifically_settled": False}
    if schema != OPERATING_ENVELOPE_V2_SCHEMA:
        raise ValueError("unsupported P7 operating envelope schema")
    required_nulls = ("t_settle_ray_s", "t_settle_strip_s", "t_formal_provisional_s", "t_formal_s")
    if any(envelope.get(field) is not None for field in required_nulls):
        raise ValueError("developer dwell envelope must keep all measured settle fields null")
    if (
        envelope.get("status") != "td_a_developer_dwell_override"
        or envelope.get("decision_owner") != "Developer/Human"
        or envelope.get("planner_inference") is not False
        or envelope.get("thermal_extension_900_1200") != "rejected"
        or envelope.get("developer_selected_operational_dwell_s") != DEVELOPER_OPERATIONAL_DWELL_S
        or envelope.get("operational_dwell_claim") != "selected_time_limit_not_proven_steady"
    ):
        raise ValueError("developer dwell decision metadata is invalid")
    if envelope.get("td_a_status") != {
        "ray": "settling_not_demonstrated_by_600",
        "strip": "settling_not_demonstrated_by_600",
    }:
        raise ValueError("developer dwell envelope rewrites the retained TD-A result")
    audit = envelope.get("decision_audit")
    if not isinstance(audit, Mapping) or set(audit) != {"path", "sha256"}:
        raise ValueError("developer dwell decision audit reference is missing")
    audit_path = Path(str(audit["path"]))
    if not audit_path.is_absolute():
        audit_path = PROJECT_ROOT / audit_path
    audit_path = audit_path.resolve()
    if not audit_path.is_relative_to(PROJECT_ROOT.resolve()) or not audit_path.is_file():
        raise ValueError("developer dwell decision audit path is outside the project")
    if audit_path != DEVELOPER_DWELL_DECISION_AUDIT.resolve():
        raise ValueError("developer dwell decision audit path differs from the frozen artifact")
    audit_sha256 = hashlib.sha256(audit_path.read_bytes()).hexdigest()
    if audit_sha256 != DEVELOPER_DWELL_DECISION_AUDIT_SHA256 or audit.get("sha256") != audit_sha256:
        raise ValueError("developer dwell decision audit hash drift")
    if artifact_path is not None:
        path = Path(artifact_path).resolve()
        if not path.is_file():
            raise ValueError("operating envelope artifact is missing")
    return {
        "mode": "developer_human_override",
        "operational_dwell_s": DEVELOPER_OPERATIONAL_DWELL_S,
        "scientifically_settled": False,
        "decision_owner": "Developer/Human",
        "decision_audit_sha256": audit_sha256,
    }


def td_b_operational_dwell_metadata(envelope: Mapping[str, Any]) -> dict[str, Any]:
    mode = validate_operating_envelope(envelope)
    return {
        "source": mode["mode"],
        "seconds": mode["operational_dwell_s"],
        "scientifically_settled": mode["scientifically_settled"],
        "measured_t_formal_provisional_s": envelope.get("t_formal_provisional_s"),
    }


def validate_td_b_operational_dwell_plan(
    plan: Mapping[str, Any], envelope: Mapping[str, Any],
) -> dict[str, Any]:
    expected = td_b_operational_dwell_metadata(envelope)
    if plan.get("operational_dwell") != expected:
        raise ValueError("TD-B developer dwell provenance differs from frozen operating envelope")
    return expected


def load_r1_commands(run_dir: str | Path = R1_RUN) -> dict[str, dict[str, int]]:
    plan = json.loads((Path(run_dir) / "plan.json").read_text(encoding="utf-8"))
    commands = plan.get("commands")
    if not isinstance(commands, Mapping):
        raise ValueError("retained P7-R1 plan lacks its canonical command map")
    output = {
        str(name): {channel: int(command[channel]) for channel in CHANNELS}
        for name, command in commands.items()
    }
    required = set(STRIP_COMMAND_KEYS.values()) | {"h0-s0-scale-relaxed-3072"}
    if set(output) != required:
        raise ValueError("retained P7-R1 command set differs from the frozen five-command set")
    return output


def load_r1_shutters(run_dir: str | Path = R1_RUN) -> dict[str, str | None]:
    rows = [
        json.loads(line) for line in (Path(run_dir) / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    output: dict[str, str | None] = {}
    for row in rows:
        source = row.get("source")
        if source == "ray":
            state = row["plan_step"]["state"]
            key = f"ray-h{int(state['hue'])}-s{int(state['sat'])}"
        elif source == "strip":
            key = f"strip-{row['plan_step']['command_key']}"
        else:
            continue
        capture = row.get("capture") or {}
        final = (capture.get("auto_exposure_audit") or {}).get("final") or (capture.get("capture") or {})
        shutter = final.get("shutter_speed")
        if shutter:
            if key in output and output[key] != str(shutter):
                raise ValueError(f"retained P7-R1 shutter cache is inconsistent for {key}")
            output[key] = str(shutter)
    required = {
        "ray-h120-s100", "ray-h0-s0", "ray-h300-s100",
        *(f"strip-{name}" for name in STRIP_COMMAND_KEYS.values()),
    }
    if not required.issubset(output):
        raise ValueError("retained P7-R1 lacks a required source/state shutter cache")
    output.setdefault("ray-h120-s50", None)  # TD-B requires a separate non-formal setup capture.
    return output


def _command(source: str, state: str, commands: Mapping[str, Mapping[str, int]]) -> dict[str, Any]:
    if source == "ray":
        return dict(RAY_STATES[state])
    return {channel: int(commands[STRIP_COMMAND_KEYS[state]][channel]) for channel in CHANNELS}


def shutter_cache_key_for_step(step: Mapping[str, Any]) -> str | None:
    source = str(step.get("source_id"))
    if source == "ambient":
        return None
    state = str(step.get("state_id"))
    command = step.get("command")
    if not isinstance(command, Mapping):
        raise ValueError("formal thermal capture lacks a command for its shutter cache")
    if source == "ray":
        try:
            return f"ray-h{int(command['hue'])}-s{int(command['sat'])}"
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("Ray thermal capture lacks a valid HSI shutter owner") from exc
    if source == "strip":
        if state not in STRIP_COMMAND_KEYS:
            raise ValueError(f"strip thermal capture has unknown state: {state}")
        return f"strip-{STRIP_COMMAND_KEYS[state]}"
    raise ValueError(f"thermal capture has unknown source: {source}")


def required_shutter_cache_keys(captures: Sequence[Mapping[str, Any]]) -> tuple[str, ...]:
    return tuple(sorted({
        key
        for step in captures
        if (key := shutter_cache_key_for_step(step)) is not None
    }))


def audit_td_b_historical_seed(
    run_dir: str | Path = P6_SETUP_SEED_RUN,
    *, capture_id: str = P6_SETUP_SEED_CAPTURE_ID,
) -> dict[str, Any]:
    """Rebuild the legacy P6 shutter seed decision from retained evidence."""
    root = Path(run_dir).resolve()
    reasons: list[str] = []
    evidence: dict[str, Any] = {}
    try:
        captures = [
            json.loads(line) for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        commands = [
            json.loads(line) for line in (root / "commands.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        rows = [row for row in captures if row.get("capture_id") == capture_id]
        command_rows = [
            row for row in commands
            if row.get("capture_id") == capture_id and row.get("event") == "ray_on_readback_verified"
        ]
        if len(rows) != 1 or len(command_rows) != 1:
            raise ValueError("P6 seed capture/command owner is missing or duplicated")
        row, command_row = rows[0], command_rows[0]
        expected_raw = {"hue": 120, "sat": 50, "intensity": 1000}
        if command_row.get("expected") != expected_raw:
            reasons.append("command_mismatch")
        for owner in ("set_response", "readback"):
            if (command_row.get(owner) or {}).get("data") != expected_raw:
                reasons.append(f"{owner}_mismatch")
        ray_state = row.get("ray_state")
        if ray_state != dict(TD_B_SETUP_COMMAND):
            reasons.append("capture_state_mismatch")
        capture = (row.get("capture") or {}).get("capture") or {}
        raw_value = capture.get("saved_file")
        raw = Path(str(raw_value)).resolve() if raw_value else None
        if raw is None or not raw.is_relative_to(root) or not raw.is_file() or raw.stat().st_size <= 0:
            reasons.append("cr3_missing_or_outside_run")
            raw_sha = None
            raw_bytes = None
        else:
            raw_sha = hashlib.sha256(raw.read_bytes()).hexdigest()
            raw_bytes = raw.stat().st_size
            if capture.get("sha256") != raw_sha or capture.get("byte_count") != raw_bytes:
                reasons.append("cr3_hash_or_byte_count_mismatch")
        report_value = (row.get("capture") or {}).get("patch_statistics")
        report_path = Path(str(report_value)).resolve() if report_value else None
        if report_path is None or not report_path.is_relative_to(root) or not report_path.is_file():
            reasons.append("patch_statistics_missing_or_outside_run")
            report = {}
        else:
            report = json.loads(report_path.read_text(encoding="utf-8"))
        exposure = report.get("exposure_metadata") or {}
        if exposure.get("status") != "recorded" or not exposure.get("seconds"):
            reasons.append("recorded_exposure_missing")
        if raw is not None and Path(str(exposure.get("raw_file"))).resolve() != raw:
            reasons.append("recorded_exposure_raw_owner_mismatch")
        if capture.get("shutter_speed") != "1/6400" or exposure.get("nominal_shutter_speed") != "1/6400":
            reasons.append("shutter_mismatch")
        if capture.get("iso") != "100" or capture.get("aperture") != "implicit auto" or capture.get("image_format") != "RAW":
            reasons.append("capture_settings_mismatch")
        expected_location = file_reference(LOCATION_PATH)["sha256"]
        if (report.get("location_config") or {}).get("sha256") != expected_location:
            reasons.append("location_mismatch")
        feature_ids = json.loads(POLICY_PATH.read_text(encoding="utf-8"))["feature_set"]["ids"]
        from camera_based_rgbww_optimizer.optimization.hsi_objective import required_hsi_features_from_report
        features = required_hsi_features_from_report(report, feature_ids) if report else {}
        if set(features) != set(feature_ids):
            reasons.append("required_58_features_missing")
        if capture.get("remote_endpoint") != "/v1/capture":
            reasons.append("legacy_endpoint_mismatch")
        evidence = {
            "capture_path": None if raw is None else str(raw),
            "capture_sha256": raw_sha,
            "capture_byte_count": raw_bytes,
            "patch_statistics_path": None if report_path is None else str(report_path),
            "recorded_exposure": exposure,
            "location_sha256": (report.get("location_config") or {}).get("sha256"),
            "feature_count": len(features),
            "quality": (row.get("capture") or {}).get("quality"),
            "remote_endpoint": capture.get("remote_endpoint"),
            "command_scale_mapping": "ray_raw_intensity_1000_equals_intensity_percent_100",
            "v2_sidecar_present": False,
        }
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        reasons.append(f"audit_error:{type(exc).__name__}:{exc}")
    return {
        "schema": "p7_td_b_historical_seed_audit_v1",
        "run_dir": str(root),
        "capture_id": capture_id,
        "historical_seed_usable": not reasons,
        "seed_only": True,
        "formal_capture_eligible": False,
        "initial_shutter_seed": "1/6400" if not reasons else None,
        "reasons": reasons,
        "evidence": evidence,
    }


def validate_td_b_exposure_setup(
    artifact: Mapping[str, Any], *, artifact_path: str | Path | None = None,
) -> dict[str, Any]:
    """Validate one retained non-formal Ray exposure setup and its physical ledger."""
    if artifact.get("schema") == TD_B_SETUP_SCHEMA_V2:
        return validate_td_b_exposure_setup_v2(artifact, artifact_path=artifact_path)
    from camera_based_rgbww_optimizer.control import camera_remote_v2

    required_keys = {
        "schema", "experiment_id", "source", "state_id", "command", "command_sha256",
        "capture_role", "formal_measurement", "counts_as_physical", "enters_58_feature_fit",
        "enters_repeatability_covariance", "enters_td_b_history_aggregate", "setup_method",
        "historical_seed", "camera", "attempts", "final_capture_id", "resolved_shutter_speed",
        "setup_physical_cr3_count", "setup_physical_cr3_cap", "input_hashes", "code_checkpoint",
        "isolation", "cold_proxy", "cleanup", "failure", "fake_only",
    }
    if set(artifact) != required_keys:
        raise ValueError("TD-B setup artifact schema keys differ from frozen contract")
    expected_command = dict(TD_B_SETUP_COMMAND)
    if (
        artifact.get("schema") != TD_B_SETUP_SCHEMA
        or artifact.get("experiment_id") != TD_B
        or artifact.get("source") != "ray"
        or artifact.get("state_id") != TD_B_SETUP_STATE
        or artifact.get("command") != expected_command
        or artifact.get("command_sha256") != canonical_sha256(expected_command)
        or artifact.get("capture_role") != "exposure_setup"
        or artifact.get("formal_measurement") is not False
        or artifact.get("counts_as_physical") is not True
        or artifact.get("enters_58_feature_fit") is not False
        or artifact.get("enters_repeatability_covariance") is not False
        or artifact.get("enters_td_b_history_aggregate") is not False
        or artifact.get("setup_method") != "bounded_remote_v2_auto_exposure"
        or artifact.get("failure") is not None
    ):
        raise ValueError("TD-B setup artifact identity or role is invalid")
    seed = artifact.get("historical_seed")
    if (
        not isinstance(seed, Mapping)
        or set(seed) != {
            "schema", "run_dir", "capture_id", "historical_seed_usable", "seed_only",
            "formal_capture_eligible", "initial_shutter_seed", "reasons", "evidence",
        }
        or seed.get("schema") != "p7_td_b_historical_seed_audit_v1"
        or seed.get("seed_only") is not True
        or seed.get("formal_capture_eligible") is not False
        or not isinstance(seed.get("reasons"), list)
        or not isinstance(seed.get("evidence"), Mapping)
    ):
        raise ValueError("TD-B setup historical seed contract is invalid")
    if seed.get("historical_seed_usable") is True:
        if (
            Path(str(seed.get("run_dir"))).resolve() != P6_SETUP_SEED_RUN.resolve()
            or seed.get("capture_id") != P6_SETUP_SEED_CAPTURE_ID
            or seed.get("initial_shutter_seed") != "1/6400"
            or seed.get("reasons") != []
            or not seed["evidence"].get("capture_sha256")
            or seed["evidence"].get("remote_endpoint") != "/v1/capture"
            or seed["evidence"].get("feature_count") != 58
        ):
            raise ValueError("TD-B setup historical seed is stale or differs from frozen P6 evidence")
    elif seed.get("historical_seed_usable") is not False or seed.get("initial_shutter_seed") is not None or not seed.get("reasons"):
        raise ValueError("TD-B setup no-seed fallback is not deterministic")
    camera = artifact.get("camera")
    if (
        not isinstance(camera, Mapping)
        or camera.get("backend") != "remote"
        or camera.get("v2_capture_capability") != "remote_v2_capture_timing_v1"
        or camera.get("capture_settings_owner") != "remote_backend.resolve_capture_settings"
        or any(not isinstance(camera.get(key), str) or not camera[key].strip() for key in ("iso", "aperture", "image_format"))
        or camera.get("image_format") != "RAW"
    ):
        raise ValueError("TD-B setup camera capability/settings provenance is invalid")
    attempts = artifact.get("attempts")
    count = artifact.get("setup_physical_cr3_count")
    if (
        not isinstance(attempts, list) or not attempts
        or type(count) is not int or count != len(attempts)
        or not 1 <= count <= TD_B_SETUP_PHYSICAL_CAP
        or artifact.get("setup_physical_cr3_cap") != TD_B_SETUP_PHYSICAL_CAP
    ):
        raise ValueError("TD-B setup physical ledger is outside the frozen 1..8 budget")
    artifact_root = None if artifact_path is None else Path(artifact_path).resolve().parent
    owned_ids: set[str] = set()
    owned_paths: set[Path] = set()
    final_rows: list[Mapping[str, Any]] = []
    for index, attempt in enumerate(attempts, start=1):
        if not isinstance(attempt, Mapping) or set(attempt) != {
            "attempt_index", "capture_id", "disposition", "cr3_path", "cr3_sha256", "cr3_byte_count",
            "sidecar_path", "sidecar_sha256", "request_id", "timing_tier", "timing_method",
            "recorded_exposure", "shutter_speed", "npy_paths", "npy_deleted",
        }:
            raise ValueError("TD-B setup attempt schema differs from frozen contract")
        capture_id = attempt.get("capture_id")
        if attempt.get("attempt_index") != index or not isinstance(capture_id, str) or not capture_id or capture_id in owned_ids:
            raise ValueError("TD-B setup attempt owner is duplicated or reordered")
        owned_ids.add(capture_id)
        raw_candidate = Path(str(attempt.get("cr3_path")))
        raw = raw_candidate.resolve()
        sidecar_candidate = Path(str(attempt.get("sidecar_path")))
        sidecar = sidecar_candidate.resolve()
        if (
            artifact_root is not None and (not raw.is_relative_to(artifact_root) or not sidecar.is_relative_to(artifact_root))
        ) or raw_candidate.is_symlink() or sidecar_candidate.is_symlink() or raw in owned_paths or sidecar in owned_paths:
            raise ValueError("TD-B setup evidence owner is outside artifact root or duplicated")
        owned_paths.update((raw, sidecar))
        if not raw.is_file() or raw.stat().st_size <= 0 or not sidecar.is_file() or sidecar.stat().st_size <= 0:
            raise ValueError("TD-B setup evidence file is missing or empty")
        payload = raw.read_bytes()
        if hashlib.sha256(payload).hexdigest() != attempt.get("cr3_sha256") or len(payload) != attempt.get("cr3_byte_count"):
            raise ValueError("TD-B setup CR3 hash or byte count mismatch")
        if hashlib.sha256(sidecar.read_bytes()).hexdigest() != attempt.get("sidecar_sha256"):
            raise ValueError("TD-B setup sidecar hash mismatch")
        try:
            metadata = json.loads(sidecar.read_text(encoding="utf-8"))
            remote, receipt = camera_remote_v2.split_and_validate_sidecar(metadata, payload=payload)
        except (OSError, UnicodeError, json.JSONDecodeError, camera_remote_v2.RemoteCaptureV2Error) as exc:
            raise ValueError("TD-B setup sidecar replay failed") from exc
        if (
            remote.get("capture_id") != capture_id
            or remote.get("request_id") != attempt.get("request_id")
            or (remote.get("recorded_exposure") or {}) != attempt.get("recorded_exposure")
            or (remote.get("recorded_exposure") or {}).get("status") != "recorded"
            or (receipt.get("timing_evidence") or {}).get("tier") != attempt.get("timing_tier")
            or (remote.get("exposure_start_estimate") or {}).get("method") != attempt.get("timing_method")
            or attempt.get("timing_tier") not in ACCEPTED_TIMING_TIERS
        ):
            raise ValueError("TD-B setup metadata ID/exposure/timing association mismatch")
        from camera_based_rgbww_optimizer.measurement.recorded_exposure import parse_nominal_exposure
        try:
            nominal_seconds = parse_nominal_exposure(str(attempt.get("shutter_speed")))
        except (TypeError, ValueError, ZeroDivisionError) as exc:
            raise ValueError("TD-B setup shutter speed is invalid") from exc
        recorded_seconds = float((remote.get("recorded_exposure") or {}).get("seconds", 0.0))
        if recorded_seconds <= 0 or not 0.8 <= recorded_seconds / nominal_seconds <= 1.2:
            raise ValueError("TD-B setup shutter differs materially from recorded exposure")
        if attempt.get("npy_paths") != [] or attempt.get("npy_deleted") is not True:
            raise ValueError("TD-B setup attempt retained NPY evidence")
        if attempt.get("disposition") == "final":
            final_rows.append(attempt)
        elif attempt.get("disposition") not in {"trial", "rejected_final"}:
            raise ValueError("TD-B setup attempt disposition is invalid")
    if len(final_rows) != 1 or artifact.get("final_capture_id") != final_rows[0].get("capture_id"):
        raise ValueError("TD-B setup final capture owner is missing or ambiguous")
    final = final_rows[0]
    if not isinstance(artifact.get("resolved_shutter_speed"), str) or not artifact["resolved_shutter_speed"].strip() or artifact["resolved_shutter_speed"] != final.get("shutter_speed"):
        raise ValueError("TD-B setup resolved shutter is empty or differs from final capture")
    isolation = artifact.get("isolation")
    if not isinstance(isolation, Mapping) or set(isolation) != {
        "ray_set_response", "ray_readback", "strip_device_evidence",
    }:
        raise ValueError("TD-B setup source isolation evidence is invalid")
    from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import (
        validate_ray_readback,
        validate_strip_device_evidence,
    )
    expected_ray = {"hue": 120, "sat": 50, "intensity": 1000}
    validate_ray_readback(isolation["ray_set_response"], expected_ray)
    validate_ray_readback(isolation["ray_readback"], expected_ray)
    curve = json.loads(CURVE_PATH.read_text(encoding="utf-8"))
    validate_strip_device_evidence(
        isolation["strip_device_evidence"], {channel: 0 for channel in CHANNELS}, curve,
    )
    cold = artifact.get("cold_proxy")
    if not isinstance(cold, Mapping) or cold.get("required_wait_s") != 1800:
        raise ValueError("TD-B setup cold proxy contract is missing")
    start, end = cold.get("start_monotonic_s"), cold.get("end_monotonic_s")
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)) for value in (start, end)) or float(end) - float(start) < 1800:
        raise ValueError("TD-B setup cold proxy wait is shortened or clock-reversed")
    validate_td_b_setup_cleanup(artifact.get("cleanup"))
    inputs = artifact.get("input_hashes")
    if not isinstance(inputs, Mapping) or any(
        key not in inputs or inputs[key] != file_reference(path)["sha256"]
        for key, path in {"location": LOCATION_PATH, "policy": POLICY_PATH, "operating_envelope": OPERATING_ENVELOPE_V2_PATH}.items()
    ):
        raise ValueError("TD-B setup frozen input hashes differ")
    return {"physical_count": count, "resolved_shutter_speed": artifact["resolved_shutter_speed"], "final_capture_id": final["capture_id"]}


def validate_td_b_exposure_setup_v2(
    artifact: Mapping[str, Any], *, artifact_path: str | Path | None = None,
) -> dict[str, Any]:
    required = {"schema", "status", "base", "bindings"}
    if set(artifact) != required or artifact.get("status") != "setup_canonical_complete":
        raise ValueError("TD-B setup v2 canonical schema or status differs")
    base = artifact.get("base")
    bindings = artifact.get("bindings")
    if not isinstance(base, Mapping) or not isinstance(bindings, Mapping):
        raise ValueError("TD-B setup v2 canonical payload is incomplete")
    if base.get("schema") != TD_B_SETUP_SCHEMA or base.get("fake_only") is not False:
        raise ValueError("TD-B setup v2 requires a non-fake v1 measurement ledger")
    expected_binding_keys = {
        "code_checkpoint", "unresolved_plan", "provisional", "wrapper_source",
        "wrapper_result", "wrapper_observed_exit", "all_off_python", "all_off_shell", "final_zero",
    }
    if set(bindings) != expected_binding_keys:
        raise ValueError("TD-B setup v2 binding schema differs")
    checkpoint = bindings.get("code_checkpoint")
    if (
        not isinstance(checkpoint, str) or len(checkpoint) != 40
        or any(ch not in "0123456789abcdef" for ch in checkpoint)
        or base.get("code_checkpoint") != checkpoint
    ):
        raise ValueError("TD-B setup v2 checkpoint binding differs")
    root = None if artifact_path is None else Path(artifact_path).resolve().parent
    for name in expected_binding_keys - {"code_checkpoint"}:
        reference = bindings.get(name)
        if not isinstance(reference, Mapping) or set(reference) != {"path", "sha256"}:
            raise ValueError(f"TD-B setup v2 {name} reference schema differs")
        path = Path(str(reference.get("path"))).resolve()
        if root is not None and name != "wrapper_source" and not path.is_relative_to(root):
            raise ValueError(f"TD-B setup v2 {name} path owner differs")
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != reference.get("sha256"):
            raise ValueError(f"TD-B setup v2 {name} hash differs")
    result = validate_td_b_exposure_setup(base, artifact_path=artifact_path)
    return {**result, "schema": TD_B_SETUP_SCHEMA_V2, "code_checkpoint": checkpoint}


def validate_td_b_setup_release(
    release: Mapping[str, Any], *, release_path: str | Path,
) -> dict[str, Any]:
    path = Path(release_path).resolve()
    required = {"schema", "status", "code_checkpoint", "canonical_setup", "resolved_formal_plan"}
    if set(release) != required or release.get("schema") != TD_B_SETUP_RELEASE_SCHEMA or release.get("status") != "formal_plan_resolved":
        raise ValueError("TD-B setup release schema or status differs")
    checkpoint = release.get("code_checkpoint")
    for name in ("canonical_setup", "resolved_formal_plan"):
        reference = release.get(name)
        if not isinstance(reference, Mapping) or set(reference) != {"path", "sha256"}:
            raise ValueError("TD-B setup release reference schema differs")
        target = Path(str(reference.get("path"))).resolve()
        if target.parent != path.parent or not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != reference.get("sha256"):
            raise ValueError(f"TD-B setup release {name} owner or hash differs")
    canonical_path = Path(str(release["canonical_setup"]["path"])).resolve()
    canonical = json.loads(canonical_path.read_text(encoding="utf-8"))
    validated = validate_td_b_exposure_setup(canonical, artifact_path=canonical_path)
    if checkpoint != validated.get("code_checkpoint"):
        raise ValueError("TD-B setup release checkpoint differs from canonical")
    resolved_path = Path(str(release["resolved_formal_plan"]["path"])).resolve()
    resolved = json.loads(resolved_path.read_text(encoding="utf-8"))
    if resolved.get("exposure_setup_artifact") != file_reference(canonical_path):
        raise ValueError("TD-B setup release resolved plan differs from canonical")
    return {**validated, "resolved_plan": resolved, "canonical_path": str(canonical_path)}


def changed_paths_between_checkpoints(
    old_checkpoint: str,
    new_checkpoint: str,
    *,
    project_root: str | Path = PROJECT_ROOT,
) -> list[str]:
    """Return the exact repository paths changed between two full checkpoints."""
    for value in (old_checkpoint, new_checkpoint):
        if (
            len(value) != 40
            or any(character not in "0123456789abcdef" for character in value)
        ):
            raise ValueError("TD-B lineage requires full lowercase Git checkpoints")
    completed = subprocess.run(
        ["git", "diff", "--name-only", f"{old_checkpoint}..{new_checkpoint}"],
        cwd=Path(project_root),
        check=True,
        capture_output=True,
        text=True,
    )
    paths = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    if len(paths) != len(set(paths)):
        raise ValueError("TD-B lineage changed-path ledger contains duplicates")
    return paths


def _validate_td_b_agents_policy_lineage(
    *,
    old_checkpoint: str,
    new_checkpoint: str,
    project_root: str | Path = PROJECT_ROOT,
    policy_freeze_path: str | Path = TD_B_AGENTS_POLICY_FREEZE_PATH,
    require_canonical_policy_owner: bool = True,
) -> None:
    """Validate the one Human-policy AGENTS.md lineage exception fail-closed."""
    root = Path(project_root).resolve()
    governance_successor = _td_b_checkpoint_contains(
        new_checkpoint,
        TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_COMMIT,
        project_root=root,
    )
    historical_new_checkpoint = (
        TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PARENT
        if governance_successor
        else new_checkpoint
    )
    policy_requested = Path(policy_freeze_path)
    if policy_requested.is_symlink():
        raise ValueError("TD-B AGENTS policy freeze cannot be a symlink")
    policy_path = policy_requested.resolve()
    if require_canonical_policy_owner and policy_path != TD_B_AGENTS_POLICY_FREEZE_PATH.resolve():
        raise ValueError("TD-B AGENTS policy freeze owner differs")
    if not policy_path.is_file():
        raise ValueError("TD-B AGENTS policy freeze is missing")
    policy_bytes = policy_path.read_bytes()
    if hashlib.sha256(policy_bytes).hexdigest() != TD_B_AGENTS_POLICY_FREEZE_SHA256:
        raise ValueError("TD-B AGENTS policy freeze hash differs")
    policy = json.loads(policy_bytes)
    required = {
        "schema", "status", "path", "classification", "current_blob_sha256",
        "expected_current", "previous_blob_sha256", "scope", "human_decision",
        "rollback", "provenance", "diff_sha256", "extra_paths",
        "qualification_runs", "release_generation", "replay_runs",
        "candidate_builds", "device_calls", "network_calls", "formal_calls",
        "git_mutations",
    }
    if (
        set(policy) != required
        or policy.get("schema") != "p7_td_b_lineage_policy_freeze_c1"
        or policy.get("status") != "pass"
        or policy.get("path") != "AGENTS.md"
        or policy.get("classification") != "bounded_validation_or_documentation"
        or policy.get("current_blob_sha256") != TD_B_AGENTS_CURRENT_SHA256
        or policy.get("expected_current") != TD_B_AGENTS_CURRENT_SHA256
        or policy.get("previous_blob_sha256") != TD_B_AGENTS_PREVIOUS_SHA256
        or policy.get("diff_sha256") != TD_B_AGENTS_DIFF_SHA256
        or policy.get("scope") != TD_B_AGENTS_POLICY_SCOPE
        or policy.get("human_decision") != TD_B_AGENTS_HUMAN_DECISION
        or policy.get("extra_paths") != []
        or not isinstance(policy.get("rollback"), str)
        or not policy["rollback"].startswith("restore previous AGENTS.md blob hash")
        or not isinstance(policy.get("provenance"), str)
        or "Human instruction recorded in task history" not in policy["provenance"]
        or any(policy.get(name) != 0 for name in (
            "qualification_runs", "release_generation", "replay_runs",
            "candidate_builds", "device_calls", "network_calls", "formal_calls",
            "git_mutations",
        ))
    ):
        raise ValueError("TD-B AGENTS policy freeze contract differs")
    agents_path = root / "AGENTS.md"
    if agents_path.is_symlink() or not agents_path.is_file():
        raise ValueError("TD-B AGENTS policy owner differs")
    if governance_successor:
        successor = _validate_td_b_governance_lineage_successor(
            new_checkpoint=new_checkpoint,
            project_root=root,
        )
        if successor.get("AGENTS.md") != "bounded_validation_or_documentation":
            raise ValueError("TD-B AGENTS governance successor classification differs")
    elif hashlib.sha256(agents_path.read_bytes()).hexdigest() != TD_B_AGENTS_CURRENT_SHA256:
        raise ValueError("TD-B AGENTS current bytes differ")
    previous = subprocess.run(
        ["git", "show", f"{old_checkpoint}:AGENTS.md"], cwd=root, check=True,
        capture_output=True,
    ).stdout
    current = subprocess.run(
        ["git", "show", f"{historical_new_checkpoint}:AGENTS.md"], cwd=root, check=True,
        capture_output=True,
    ).stdout
    diff = subprocess.run(
        ["git", "diff", old_checkpoint, historical_new_checkpoint, "--", "AGENTS.md"],
        cwd=root, check=True, capture_output=True,
    ).stdout
    if hashlib.sha256(previous).hexdigest() != TD_B_AGENTS_PREVIOUS_SHA256:
        raise ValueError("TD-B AGENTS previous bytes differ")
    if hashlib.sha256(current).hexdigest() != TD_B_AGENTS_CURRENT_SHA256:
        raise ValueError("TD-B AGENTS checkpoint bytes differ")
    if hashlib.sha256(diff).hexdigest() != TD_B_AGENTS_DIFF_SHA256:
        raise ValueError("TD-B AGENTS diff scope differs")


def _validate_td_b_qualification_preparation_r1(
    *,
    preparation_path: str | Path,
    code_checkpoint: str,
    require_canonical_owner: bool = True,
    expected_payload_sha256: str | None = None,
    expected_payload_bytes: int | None = None,
) -> Mapping[str, Any]:
    """Validate the exact C3-R1 evidence preparation without release authority."""
    requested = Path(preparation_path)
    if requested.is_symlink():
        raise ValueError("TD-B qualification preparation cannot be a symlink")
    path = requested.resolve()
    canonical_path = TD_B_QUALIFICATION_PREPARATION_R1_PATH.resolve()
    if require_canonical_owner and path != canonical_path:
        raise ValueError("TD-B qualification preparation owner differs")
    if not path.is_file():
        raise ValueError("TD-B qualification preparation is missing or non-regular")
    if stat.S_IMODE(path.stat().st_mode) != 0o600:
        raise ValueError("TD-B qualification preparation mode differs")
    payload = path.read_bytes()
    expected_bytes = (
        TD_B_QUALIFICATION_PREPARATION_R1_BYTES
        if expected_payload_bytes is None
        else expected_payload_bytes
    )
    if len(payload) != expected_bytes:
        raise ValueError("TD-B qualification preparation byte count differs")
    expected_sha = (
        TD_B_QUALIFICATION_PREPARATION_R1_SHA256
        if expected_payload_sha256 is None
        else expected_payload_sha256
    )
    if hashlib.sha256(payload).hexdigest() != expected_sha:
        raise ValueError("TD-B qualification preparation hash differs")

    canonical_payload = canonical_path.read_bytes()
    if (
        len(canonical_payload) != TD_B_QUALIFICATION_PREPARATION_R1_BYTES
        or hashlib.sha256(canonical_payload).hexdigest()
        != TD_B_QUALIFICATION_PREPARATION_R1_SHA256
    ):
        raise ValueError("TD-B canonical qualification preparation drifted")
    preparation = json.loads(payload)
    canonical = json.loads(canonical_payload)
    required = {
        "schema", "status", "audit_current_head", "audit_current_parent",
        "source_c3_preparation", "successor_entry", "input_closure", "inputs",
        "budgets", "negative_matrix", "canonical_before_after",
    }
    if (
        set(preparation) != required
        or preparation.get("schema") != TD_B_QUALIFICATION_PREPARATION_R1_SCHEMA
        or preparation.get("status") != "prepared_waiting_for_planner"
        or code_checkpoint != TD_B_QUALIFICATION_AUDIT_CHECKPOINT
        or preparation.get("audit_current_head") != code_checkpoint
        or preparation.get("audit_current_parent")
        != TD_B_PUBLIC_DEFAULT_SUCCESSOR_COMMIT
    ):
        raise ValueError("TD-B qualification preparation schema/status/checkpoint differs")
    for name in (
        "source_c3_preparation", "successor_entry", "input_closure", "inputs",
        "budgets", "negative_matrix", "canonical_before_after",
    ):
        if preparation.get(name) != canonical.get(name):
            raise ValueError(f"TD-B qualification preparation {name} differs")

    successor = preparation["successor_entry"]
    successor_fields = {
        "canonical_path", "canonical_sha256", "canonical_bytes",
        "canonical_schema", "artifact_owner_commit", "artifact_owner_parent",
        "audit_current_head", "audit_current_parent", "provenance",
        "rollback_entries",
    }
    if (
        not isinstance(successor, Mapping)
        or set(successor) != successor_fields
        or "commit" in successor
        or "parent_commit" in successor
        or successor.get("artifact_owner_commit")
        != TD_B_PUBLIC_DEFAULT_SUCCESSOR_COMMIT
        or successor.get("artifact_owner_parent")
        != TD_B_PUBLIC_DEFAULT_SUCCESSOR_PARENT
        or successor.get("audit_current_head") != code_checkpoint
        or successor.get("audit_current_parent")
        != TD_B_PUBLIC_DEFAULT_SUCCESSOR_COMMIT
        or successor.get("canonical_path")
        != str(TD_B_PUBLIC_DEFAULT_SUCCESSOR_MANIFEST_PATH)
        or successor.get("canonical_sha256")
        != TD_B_PUBLIC_DEFAULT_SUCCESSOR_MANIFEST_SHA256
        or successor.get("canonical_schema")
        != "p7_td_b_ray_public_default_successor_lineage_c1"
        or successor.get("provenance")
        != TD_B_PUBLIC_DEFAULT_SUCCESSOR_PROVENANCE
        or successor.get("rollback_entries") != 7
    ):
        raise ValueError("TD-B qualification preparation successor provenance differs")
    _validate_td_b_public_default_successor_lineage(
        new_checkpoint=code_checkpoint,
    )
    if not _td_b_checkpoint_contains(
        code_checkpoint,
        TD_B_PUBLIC_DEFAULT_SUCCESSOR_COMMIT,
    ):
        raise ValueError("TD-B qualification preparation ancestry differs")

    closure = preparation["input_closure"]
    if closure != {
        "unique_inputs": 17,
        "predecessor_retained_artifacts": 13,
        "changed_paths": 57,
        "changed_paths_sorted_deduplicated": True,
        "successor_paths": "7/7",
        "workflow_overlap": "5/5",
        "mismatches": [],
        "prohibited_paths": [],
    }:
        raise ValueError("TD-B qualification preparation input closure differs")
    inputs = preparation["inputs"]
    if not isinstance(inputs, list) or len(inputs) != 17:
        raise ValueError("TD-B qualification preparation input count differs")
    seen: set[str] = set()
    for reference in inputs:
        if not isinstance(reference, Mapping) or set(reference) != {
            "path", "owner", "regular", "symlink", "bytes", "sha256",
        }:
            raise ValueError("TD-B qualification preparation input schema differs")
        input_path_value = str(reference.get("path"))
        if input_path_value in seen:
            raise ValueError("TD-B qualification preparation input is duplicated")
        seen.add(input_path_value)
        input_path = Path(input_path_value)
        if (
            input_path.is_symlink()
            or not input_path.is_file()
            or reference.get("regular") is not True
            or reference.get("symlink") is not False
            or input_path.stat().st_size != reference.get("bytes")
            or hashlib.sha256(input_path.read_bytes()).hexdigest()
            != reference.get("sha256")
        ):
            raise ValueError("TD-B qualification preparation input owner/hash differs")
    budgets = preparation["budgets"]
    if not isinstance(budgets, Mapping) or not budgets or any(
        isinstance(value, bool) or value != 0 for value in budgets.values()
    ):
        raise ValueError("TD-B qualification preparation side-effect budget differs")
    return preparation


def _td_b_checkpoint_contains(
    checkpoint: str,
    ancestor: str,
    *,
    project_root: str | Path = PROJECT_ROOT,
) -> bool:
    """Return whether a full checkpoint contains an exact lineage commit."""
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, checkpoint],
        cwd=Path(project_root).resolve(), capture_output=True,
    ).returncode == 0


def _load_td_b_strict_json_object(payload: bytes, *, owner: str) -> Mapping[str, Any]:
    """Decode an exact JSON object while rejecting duplicate and non-finite values."""

    def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"{owner} JSON contains duplicate keys")
            result[key] = value
        return result

    def reject_non_finite(value: str) -> None:
        raise ValueError(f"{owner} JSON contains non-finite value: {value}")

    try:
        decoded = json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_non_finite,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"{owner} JSON differs") from exc
    if not isinstance(decoded, Mapping):
        raise ValueError(f"{owner} contract differs")
    return decoded


def _validate_td_b_governance_lineage_successor(
    *,
    new_checkpoint: str,
    project_root: str | Path = PROJECT_ROOT,
    manifest_path: str | Path = TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PATH,
    require_canonical_manifest_owner: bool = True,
    expected_manifest_sha256: str | None = None,
) -> Mapping[str, str]:
    """Validate the exact subordinate governance provenance layer fail-closed."""
    root = Path(project_root).resolve()
    requested = Path(manifest_path)
    if requested.is_symlink():
        raise ValueError("TD-B governance successor manifest cannot be a symlink")
    path = requested.resolve()
    if (
        require_canonical_manifest_owner
        and path != TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PATH.resolve()
    ):
        raise ValueError("TD-B governance successor manifest owner differs")
    if not path.exists():
        raise ValueError("TD-B governance successor manifest is missing")
    if not path.is_file() or not stat.S_ISREG(path.stat().st_mode):
        raise ValueError("TD-B governance successor manifest is non-regular")
    payload = path.read_bytes()
    expected_payload_sha256 = (
        TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_SHA256
        if expected_manifest_sha256 is None
        else expected_manifest_sha256
    )
    if hashlib.sha256(payload).hexdigest() != expected_payload_sha256:
        raise ValueError("TD-B governance successor manifest hash differs")
    manifest = _load_td_b_strict_json_object(
        payload,
        owner="TD-B governance successor manifest",
    )
    required = {
        "schema", "status", "owner", "scope", "eligibility_owner", "commit",
        "parent_commit", "changed_path_ledger", "selected_path_count",
        "selected_paths", "selected_binary_diff_sha256", "rollback",
        "extra_paths", "operation_counters",
    }
    counters = {
        "candidate_reads", "retained_r3_reads", "canonical_retained_validator_calls",
        "eligibility_emissions", "release_calls", "network_calls", "env_reads",
        "device_calls", "camera_calls", "ray_calls", "strip_calls", "cleanup_calls",
        "formal_calls", "public_analyzer_calls", "td_c_calls", "sentinel_calls",
        "p8_calls",
    }
    ledger = manifest.get("changed_path_ledger")
    selected = manifest.get("selected_paths")
    operation_counters = manifest.get("operation_counters")
    if (
        set(manifest) != required
        or manifest.get("schema") != "p7_td_b_governance_lineage_successor_v1"
        or manifest.get("status") != "pass"
        or manifest.get("owner") != "subordinate_exact_governance_provenance_only"
        or manifest.get("scope") != "validation_only_no_eligibility_emission"
        or manifest.get("eligibility_owner")
        != "build_td_b_setup_release_lineage_candidate"
        or manifest.get("commit") != TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_COMMIT
        or manifest.get("parent_commit") != TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PARENT
        or manifest.get("selected_path_count") != 2
        or manifest.get("selected_binary_diff_sha256")
        != "5a6cd050cd1d096e0894508aec338f7249679810bea63626acdcff63df9d17c8"
        or manifest.get("rollback")
        != (
            "restore only the two selected parent blobs; do not alter the other "
            "179 paths or any historical manifest"
        )
        or manifest.get("extra_paths") != []
        or not isinstance(operation_counters, Mapping)
        or set(operation_counters) != counters
        or any(type(operation_counters[name]) is not int or operation_counters[name] != 0
               for name in counters)
    ):
        raise ValueError("TD-B governance successor manifest contract differs")
    expected_ledger_command = [
        "git", "diff", "--name-only", TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PARENT,
        TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_COMMIT,
    ]
    if (
        not isinstance(ledger, Mapping)
        or set(ledger) != {"argv", "count", "lf_sha256"}
        or ledger.get("argv") != expected_ledger_command
        or type(ledger.get("count")) is not int
        or ledger.get("count") != 181
        or ledger.get("lf_sha256")
        != "9596c3fa8aee58259aff13b44badcc7d448e0555c80f166b20706dcd1e321118"
    ):
        raise ValueError("TD-B governance successor changed-path ledger differs")

    entry_fields = {
        "path", "classification", "scope", "before_blob_oid", "after_blob_oid",
        "before_sha256", "after_sha256", "binary_diff_sha256", "rollback",
        "extra_paths",
    }
    expected_entries = {
        ".agents/skills/camera-based-rgbww-optimizer/SKILL.md": {
            "before_blob_oid": "1f8bf2a7f568de77f0fa4290d18e300f0e48047e",
            "after_blob_oid": "4d7dfe66c73036cb87e199c322f9344863f8c64e",
            "before_sha256": "c8dd57a23ad684b4f7001f342ed3413a1abf4349bc6aeb90dbee7f5158139607",
            "after_sha256": "3a77c8a0f7b02b0c8b15d31b625273e88a0ee38fca5bb739dbdaaacb40dfe81e",
            "binary_diff_sha256": "7127dfdfb608b7de284a181afcca704c36b107aa3859e2fecea059ae47af3049",
        },
        "AGENTS.md": {
            "before_blob_oid": "440956792bf843c15b2f315e66e16826305d2154",
            "after_blob_oid": "58bfacb5fc46fcb42bf643d12974063533a684eb",
            "before_sha256": "a035e6955ea113100031bf411f30abad3b84a9dd260fde848f1b1cfbd194c8a5",
            "after_sha256": "604b10bedeac6c9285f6448f94323521bf021a58275cce84d64163e16a2f07a0",
            "binary_diff_sha256": "5736f6992d6882b1012a26ae5123892674d1f88cde0fee6ad98a5d33f78f5066",
        },
    }
    ordered_paths = list(TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_CLASSIFICATIONS)
    if not isinstance(selected, list) or len(selected) != 2:
        raise ValueError("TD-B governance successor selected path count differs")
    if any(not isinstance(entry, Mapping) or set(entry) != entry_fields for entry in selected):
        raise ValueError("TD-B governance successor selected entry schema differs")
    actual_paths = [entry.get("path") for entry in selected]
    if actual_paths != ordered_paths or len(actual_paths) != len(set(actual_paths)):
        raise ValueError("TD-B governance successor selected path set differs")
    for entry in selected:
        entry_path = str(entry["path"])
        expected = expected_entries[entry_path]
        if (
            entry.get("classification") != "bounded_validation_or_documentation"
            or entry.get("scope") != "exact_authorized_governance_successor_only"
            or entry.get("rollback")
            != (
                f"restore {entry_path} from parent "
                f"{TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PARENT} without changing any other path"
            )
            or entry.get("extra_paths") != []
            or any(entry.get(name) != value for name, value in expected.items())
        ):
            raise ValueError(
                f"TD-B governance successor selected entry differs: {entry_path}"
            )

    if (
        not isinstance(new_checkpoint, str)
        or len(new_checkpoint) != 40
        or any(character not in "0123456789abcdef" for character in new_checkpoint)
    ):
        raise ValueError("TD-B governance successor checkpoint is invalid")
    try:
        resolved = subprocess.run(
            ["git", "rev-parse", new_checkpoint], cwd=root, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
        parent = subprocess.run(
            ["git", "rev-parse", f"{TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_COMMIT}^"],
            cwd=root, check=True, capture_output=True, text=True,
        ).stdout.strip()
        ledger_bytes = subprocess.run(
            expected_ledger_command, cwd=root, check=True, capture_output=True,
        ).stdout
    except subprocess.CalledProcessError as exc:
        raise ValueError("TD-B governance successor Git owner differs") from exc
    if (
        resolved != new_checkpoint
        or not _td_b_checkpoint_contains(
            resolved, TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_COMMIT, project_root=root,
        )
    ):
        raise ValueError("TD-B governance successor checkpoint ancestry differs")
    ledger_paths = ledger_bytes.decode("utf-8").splitlines()
    if (
        parent != TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PARENT
        or len(ledger_paths) != 181
        or len(ledger_paths) != len(set(ledger_paths))
        or any(not item for item in ledger_paths)
        or hashlib.sha256(ledger_bytes).hexdigest() != ledger["lf_sha256"]
    ):
        raise ValueError("TD-B governance successor historical owner differs")

    try:
        for entry in selected:
            entry_path = str(entry["path"])
            before_oid = subprocess.run(
                ["git", "rev-parse", f"{TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PARENT}:{entry_path}"],
                cwd=root, check=True, capture_output=True, text=True,
            ).stdout.strip()
            after_oid = subprocess.run(
                ["git", "rev-parse", f"{TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_COMMIT}:{entry_path}"],
                cwd=root, check=True, capture_output=True, text=True,
            ).stdout.strip()
            before = subprocess.run(
                ["git", "show", f"{TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PARENT}:{entry_path}"],
                cwd=root, check=True, capture_output=True,
            ).stdout
            after = subprocess.run(
                ["git", "show", f"{TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_COMMIT}:{entry_path}"],
                cwd=root, check=True, capture_output=True,
            ).stdout
            checkpoint = subprocess.run(
                ["git", "show", f"{new_checkpoint}:{entry_path}"],
                cwd=root, check=True, capture_output=True,
            ).stdout
            single_diff = subprocess.run(
                ["git", "diff", "--binary", TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PARENT,
                 TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_COMMIT, "--", entry_path],
                cwd=root, check=True, capture_output=True,
            ).stdout
            working = root / entry_path
            if working.is_symlink() or not working.is_file():
                raise ValueError(
                    f"TD-B governance successor working owner differs: {entry_path}"
                )
            if (
                before_oid != entry["before_blob_oid"]
                or after_oid != entry["after_blob_oid"]
                or hashlib.sha256(before).hexdigest() != entry["before_sha256"]
                or hashlib.sha256(after).hexdigest() != entry["after_sha256"]
                or hashlib.sha256(checkpoint).hexdigest() != entry["after_sha256"]
                or hashlib.sha256(working.read_bytes()).hexdigest() != entry["after_sha256"]
                or hashlib.sha256(single_diff).hexdigest() != entry["binary_diff_sha256"]
            ):
                raise ValueError(
                    f"TD-B governance successor path identity differs: {entry_path}"
                )
        combined_diff = subprocess.run(
            ["git", "diff", "--binary", TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PARENT,
             TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_COMMIT, "--", *ordered_paths],
            cwd=root, check=True, capture_output=True,
        ).stdout
    except subprocess.CalledProcessError as exc:
        raise ValueError("TD-B governance successor Git path owner differs") from exc
    if hashlib.sha256(combined_diff).hexdigest() != manifest["selected_binary_diff_sha256"]:
        raise ValueError("TD-B governance successor combined diff differs")
    return TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_CLASSIFICATIONS


def _validate_td_b_public_default_successor_lineage(
    *,
    new_checkpoint: str,
    project_root: str | Path = PROJECT_ROOT,
    manifest_path: str | Path = TD_B_PUBLIC_DEFAULT_SUCCESSOR_MANIFEST_PATH,
    require_canonical_manifest_owner: bool = True,
) -> Mapping[str, str]:
    """Validate the exact public-default successor commit and current path owners."""
    root = Path(project_root).resolve()
    if (
        not isinstance(new_checkpoint, str)
        or len(new_checkpoint) != 40
        or any(character not in "0123456789abcdef" for character in new_checkpoint)
    ):
        raise ValueError("TD-B public-default successor checkpoint is invalid")
    try:
        resolved_checkpoint = subprocess.run(
            ["git", "rev-parse", new_checkpoint], cwd=root, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
        resolved_head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
    except subprocess.CalledProcessError as exc:
        raise ValueError("TD-B public-default successor checkpoint is invalid") from exc
    if (
        resolved_checkpoint != new_checkpoint
        or len(resolved_head) != 40
        or any(character not in "0123456789abcdef" for character in resolved_head)
    ):
        raise ValueError("TD-B public-default successor checkpoint is invalid")
    current_head = resolved_checkpoint == resolved_head
    governance_successor = _td_b_checkpoint_contains(
        resolved_checkpoint,
        TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_COMMIT,
        project_root=root,
    )
    historical_checkpoint = (
        TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PARENT
        if current_head and governance_successor
        else resolved_checkpoint
    )
    requested = Path(manifest_path)
    if requested.is_symlink():
        raise ValueError("TD-B public-default successor manifest cannot be a symlink")
    path = requested.resolve()
    if (
        require_canonical_manifest_owner
        and path != TD_B_PUBLIC_DEFAULT_SUCCESSOR_MANIFEST_PATH.resolve()
    ):
        raise ValueError("TD-B public-default successor manifest owner differs")
    if not path.is_file():
        raise ValueError("TD-B public-default successor manifest is missing")
    payload = path.read_bytes()
    if hashlib.sha256(payload).hexdigest() != TD_B_PUBLIC_DEFAULT_SUCCESSOR_MANIFEST_SHA256:
        raise ValueError("TD-B public-default successor manifest hash differs")
    manifest = json.loads(payload)
    required = {
        "schema", "status", "commit", "parent_commit", "human_provenance",
        "entries", "extra_paths", "qualification_runs", "replay_runs",
        "candidate_builds", "release_generation", "release_consumption",
        "device_calls", "network_calls", "env_content_reads", "formal_calls",
        "git_mutations",
    }
    if (
        set(manifest) != required
        or manifest.get("schema")
        != "p7_td_b_ray_public_default_successor_lineage_c1"
        or manifest.get("status") != "pass"
        or manifest.get("commit") != TD_B_PUBLIC_DEFAULT_SUCCESSOR_COMMIT
        or manifest.get("parent_commit") != TD_B_PUBLIC_DEFAULT_SUCCESSOR_PARENT
        or manifest.get("human_provenance")
        != TD_B_PUBLIC_DEFAULT_SUCCESSOR_PROVENANCE
        or manifest.get("extra_paths") != []
        or any(manifest.get(name) != 0 for name in (
            "qualification_runs", "replay_runs", "candidate_builds",
            "release_generation", "release_consumption", "device_calls",
            "network_calls", "env_content_reads", "formal_calls", "git_mutations",
        ))
    ):
        raise ValueError("TD-B public-default successor manifest contract differs")

    entries = manifest.get("entries")
    entry_fields = {
        "path", "classification", "old_blob_state", "old_blob_sha256",
        "current_blob_sha256", "diff_sha256", "scope", "human_decision",
        "provenance", "rollback", "extra_paths",
    }
    if (
        not isinstance(entries, list)
        or len(entries) != len(TD_B_PUBLIC_DEFAULT_SUCCESSOR_CLASSIFICATIONS)
    ):
        raise ValueError("TD-B public-default successor manifest entry count differs")
    by_path: dict[str, Mapping[str, Any]] = {}
    ordered_paths: list[str] = []
    for raw_entry in entries:
        if not isinstance(raw_entry, Mapping) or set(raw_entry) != entry_fields:
            raise ValueError("TD-B public-default successor manifest entry schema differs")
        entry_path = str(raw_entry.get("path"))
        if entry_path in by_path:
            raise ValueError("TD-B public-default successor manifest contains duplicate paths")
        ordered_paths.append(entry_path)
        by_path[entry_path] = raw_entry
    if (
        set(by_path) != set(TD_B_PUBLIC_DEFAULT_SUCCESSOR_CLASSIFICATIONS)
        or ordered_paths != sorted(ordered_paths)
    ):
        raise ValueError("TD-B public-default successor manifest exact path set differs")

    if (
        not _td_b_checkpoint_contains(
            resolved_checkpoint,
            TD_B_PUBLIC_DEFAULT_SUCCESSOR_COMMIT,
            project_root=root,
        )
    ):
        raise ValueError("TD-B public-default successor checkpoint ancestry differs")

    for entry_path, classification in TD_B_PUBLIC_DEFAULT_SUCCESSOR_CLASSIFICATIONS.items():
        entry = by_path[entry_path]
        rollback = (
            f"restore {entry_path} from parent {TD_B_PUBLIC_DEFAULT_SUCCESSOR_PARENT} "
            "and remove only this exact successor manifest entry"
        )
        if (
            entry.get("classification") != classification
            or entry.get("old_blob_state") != "present"
            or entry.get("scope") != TD_B_PUBLIC_DEFAULT_SUCCESSOR_SCOPES[classification]
            or entry.get("human_decision")
            != TD_B_PUBLIC_DEFAULT_SUCCESSOR_HUMAN_DECISION
            or entry.get("provenance") != TD_B_PUBLIC_DEFAULT_SUCCESSOR_PROVENANCE
            or entry.get("rollback") != rollback
            or entry.get("extra_paths") != []
            or not all(
                isinstance(entry.get(name), str)
                and len(str(entry[name])) == 64
                and all(character in "0123456789abcdef" for character in str(entry[name]))
                for name in ("old_blob_sha256", "current_blob_sha256", "diff_sha256")
            )
        ):
            raise ValueError(
                f"TD-B public-default successor contract differs: {entry_path}"
            )
        working = root / entry_path
        require_legacy_working_owner = (
            current_head
            and not (
                governance_successor
                and entry_path in TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_CLASSIFICATIONS
            )
        )
        if require_legacy_working_owner and (
            working.is_symlink() or not working.is_file()
        ):
            raise ValueError(
                f"TD-B public-default successor path owner differs: {entry_path}"
            )
        try:
            old = subprocess.run(
                ["git", "show", f"{TD_B_PUBLIC_DEFAULT_SUCCESSOR_PARENT}:{entry_path}"],
                cwd=root, check=True, capture_output=True,
            ).stdout
            current = subprocess.run(
                ["git", "show", f"{TD_B_PUBLIC_DEFAULT_SUCCESSOR_COMMIT}:{entry_path}"],
                cwd=root, check=True, capture_output=True,
            ).stdout
            checkpoint = subprocess.run(
                ["git", "show", f"{historical_checkpoint}:{entry_path}"],
                cwd=root, check=True, capture_output=True,
            ).stdout
            diff = subprocess.run(
                ["git", "diff", "--binary", TD_B_PUBLIC_DEFAULT_SUCCESSOR_PARENT,
                 TD_B_PUBLIC_DEFAULT_SUCCESSOR_COMMIT, "--", entry_path],
                cwd=root, check=True, capture_output=True,
            ).stdout
        except subprocess.CalledProcessError as exc:
            raise ValueError(
                f"TD-B public-default successor Git owner differs: {entry_path}"
            ) from exc
        if (
            (
                require_legacy_working_owner
                and hashlib.sha256(working.read_bytes()).hexdigest()
                != entry.get("current_blob_sha256")
            )
            or hashlib.sha256(old).hexdigest() != entry.get("old_blob_sha256")
            or hashlib.sha256(current).hexdigest()
            != entry.get("current_blob_sha256")
            or hashlib.sha256(checkpoint).hexdigest()
            != entry.get("current_blob_sha256")
            or hashlib.sha256(diff).hexdigest() != entry.get("diff_sha256")
        ):
            raise ValueError(
                f"TD-B public-default successor hash or diff differs: {entry_path}"
            )
    if current_head and governance_successor:
        governance_classifications = _validate_td_b_governance_lineage_successor(
            new_checkpoint=new_checkpoint,
            project_root=root,
        )
        overlap = set(governance_classifications).intersection(
            TD_B_PUBLIC_DEFAULT_SUCCESSOR_CLASSIFICATIONS
        )
        if overlap != {".agents/skills/camera-based-rgbww-optimizer/SKILL.md"}:
            raise ValueError("TD-B governance successor overlap differs")
    return TD_B_PUBLIC_DEFAULT_SUCCESSOR_CLASSIFICATIONS


def _validate_td_b_workflow_path_lineage(
    *,
    new_checkpoint: str,
    project_root: str | Path = PROJECT_ROOT,
    manifest_path: str | Path = TD_B_WORKFLOW_PATH_MANIFEST_PATH,
    require_canonical_manifest_owner: bool = True,
    successor_manifest_path: str | Path = TD_B_PUBLIC_DEFAULT_SUCCESSOR_MANIFEST_PATH,
    require_canonical_successor_owner: bool = True,
) -> Mapping[str, str]:
    """Validate old workflow history while delegating superseded current owners."""
    root = Path(project_root).resolve()
    successor_classifications = (
        _validate_td_b_public_default_successor_lineage(
            new_checkpoint=new_checkpoint,
            project_root=root,
            manifest_path=successor_manifest_path,
            require_canonical_manifest_owner=require_canonical_successor_owner,
        )
        if _td_b_checkpoint_contains(
            new_checkpoint,
            TD_B_PUBLIC_DEFAULT_SUCCESSOR_COMMIT,
            project_root=root,
        )
        else {}
    )
    successor_paths = set(successor_classifications)
    requested = Path(manifest_path)
    if requested.is_symlink():
        raise ValueError("TD-B workflow path manifest cannot be a symlink")
    path = requested.resolve()
    if (
        require_canonical_manifest_owner
        and path != TD_B_WORKFLOW_PATH_MANIFEST_PATH.resolve()
    ):
        raise ValueError("TD-B workflow path manifest owner differs")
    if not path.is_file():
        raise ValueError("TD-B workflow path manifest is missing")
    payload = path.read_bytes()
    if hashlib.sha256(payload).hexdigest() != TD_B_WORKFLOW_PATH_MANIFEST_SHA256:
        raise ValueError("TD-B workflow path manifest hash differs")
    manifest = json.loads(payload)
    required = {
        "schema", "status", "commit", "parent_commit", "human_provenance",
        "entries", "extra_paths", "qualification_runs", "replay_runs",
        "candidate_builds", "release_generation", "device_calls", "network_calls",
        "env_content_reads", "formal_calls", "git_mutations",
    }
    if (
        set(manifest) != required
        or manifest.get("schema") != "p7_td_b_lineage_workflow_path_manifest_c1"
        or manifest.get("status") != "pass"
        or manifest.get("commit") != TD_B_WORKFLOW_PATH_COMMIT
        or manifest.get("parent_commit") != TD_B_WORKFLOW_PATH_PARENT
        or manifest.get("human_provenance")
        != (
            "Human instruction recorded in task history; exact commit subject: "
            "fix(workflow): clarify local calibration context"
        )
        or manifest.get("extra_paths") != []
        or any(manifest.get(name) != 0 for name in (
            "qualification_runs", "replay_runs", "candidate_builds",
            "release_generation", "device_calls", "network_calls",
            "env_content_reads", "formal_calls", "git_mutations",
        ))
    ):
        raise ValueError("TD-B workflow path manifest contract differs")
    entries = manifest.get("entries")
    if not isinstance(entries, list) or len(entries) != len(TD_B_WORKFLOW_PATH_CLASSIFICATIONS):
        raise ValueError("TD-B workflow path manifest entry count differs")
    by_path: dict[str, Mapping[str, Any]] = {}
    entry_fields = {
        "path", "classification", "old_blob_state", "old_blob_sha256",
        "current_blob_sha256", "diff_sha256", "scope", "human_instruction",
        "provenance", "rollback", "extra_paths",
    }
    for raw_entry in entries:
        if not isinstance(raw_entry, Mapping) or set(raw_entry) != entry_fields:
            raise ValueError("TD-B workflow path manifest entry schema differs")
        entry_path = str(raw_entry.get("path"))
        if entry_path in by_path:
            raise ValueError("TD-B workflow path manifest contains duplicate paths")
        by_path[entry_path] = raw_entry
    if set(by_path) != set(TD_B_WORKFLOW_PATH_CLASSIFICATIONS):
        raise ValueError("TD-B workflow path manifest exact path set differs")

    empty_sha = hashlib.sha256(b"").hexdigest()
    for entry_path, classification in TD_B_WORKFLOW_PATH_CLASSIFICATIONS.items():
        entry = by_path[entry_path]
        old_state = entry.get("old_blob_state")
        rollback = (
            f"restore {entry_path} from parent {TD_B_WORKFLOW_PATH_PARENT} and remove "
            "only this exact manifest entry"
            if old_state == "present"
            else f"remove commit-created {entry_path} and remove only this exact manifest entry"
        )
        if (
            entry.get("classification") != classification
            or old_state not in {"present", "absent"}
            or entry.get("scope") != TD_B_WORKFLOW_PATH_SCOPES[classification]
            or entry.get("human_instruction") != TD_B_WORKFLOW_PATH_HUMAN_INSTRUCTION
            or entry.get("provenance")
            != (
                "Human instruction recorded in task history and implemented by exact commit "
                f"{TD_B_WORKFLOW_PATH_COMMIT}"
            )
            or entry.get("rollback") != rollback
            or entry.get("extra_paths") != []
            or not all(
                isinstance(entry.get(name), str) and len(str(entry[name])) == 64
                for name in ("old_blob_sha256", "current_blob_sha256", "diff_sha256")
            )
        ):
            raise ValueError(f"TD-B workflow path manifest contract differs: {entry_path}")
        working = root / entry_path
        if entry_path not in successor_paths and (
            working.is_symlink() or not working.is_file()
        ):
            raise ValueError(f"TD-B workflow path owner differs: {entry_path}")
        current = subprocess.run(
            ["git", "show", f"{TD_B_WORKFLOW_PATH_COMMIT}:{entry_path}"],
            cwd=root, check=True, capture_output=True,
        ).stdout
        checkpoint = (
            b""
            if entry_path in successor_paths
            else subprocess.run(
                ["git", "show", f"{new_checkpoint}:{entry_path}"],
                cwd=root, check=True, capture_output=True,
            ).stdout
        )
        old_probe = subprocess.run(
            ["git", "cat-file", "-e", f"{TD_B_WORKFLOW_PATH_PARENT}:{entry_path}"],
            cwd=root, capture_output=True,
        )
        if old_state == "present":
            if old_probe.returncode != 0:
                raise ValueError(f"TD-B workflow path old owner differs: {entry_path}")
            old = subprocess.run(
                ["git", "show", f"{TD_B_WORKFLOW_PATH_PARENT}:{entry_path}"],
                cwd=root, check=True, capture_output=True,
            ).stdout
        else:
            if old_probe.returncode == 0 or entry.get("old_blob_sha256") != empty_sha:
                raise ValueError(f"TD-B workflow path old absence differs: {entry_path}")
            old = b""
        diff = subprocess.run(
            ["git", "diff", TD_B_WORKFLOW_PATH_PARENT, TD_B_WORKFLOW_PATH_COMMIT,
             "--", entry_path],
            cwd=root, check=True, capture_output=True,
        ).stdout
        expected_current = entry.get("current_blob_sha256")
        if (
            (entry_path not in successor_paths and (
                hashlib.sha256(working.read_bytes()).hexdigest() != expected_current
                or hashlib.sha256(checkpoint).hexdigest() != expected_current
            ))
            or hashlib.sha256(current).hexdigest() != expected_current
            or hashlib.sha256(old).hexdigest() != entry.get("old_blob_sha256")
            or hashlib.sha256(diff).hexdigest() != entry.get("diff_sha256")
        ):
            raise ValueError(f"TD-B workflow path hash or diff differs: {entry_path}")
    return TD_B_WORKFLOW_PATH_CLASSIFICATIONS


def _validate_td_b_cleanup_test_provenance(
    *,
    new_checkpoint: str,
    project_root: str | Path = PROJECT_ROOT,
    manifest_path: str | Path = TD_B_CLEANUP_TEST_PROVENANCE_MANIFEST_PATH,
    require_canonical_manifest_owner: bool = True,
) -> Mapping[str, str]:
    """Validate the exact cleanup-test correction without a tests allowlist."""
    root = Path(project_root).resolve()
    requested = Path(manifest_path)
    if requested.is_symlink():
        raise ValueError("TD-B cleanup-test provenance manifest cannot be a symlink")
    path = requested.resolve()
    if (
        require_canonical_manifest_owner
        and path != TD_B_CLEANUP_TEST_PROVENANCE_MANIFEST_PATH.resolve()
    ):
        raise ValueError("TD-B cleanup-test provenance manifest owner differs")
    if not path.is_file():
        raise ValueError("TD-B cleanup-test provenance manifest is missing")
    payload = path.read_bytes()
    if hashlib.sha256(payload).hexdigest() != TD_B_CLEANUP_TEST_PROVENANCE_MANIFEST_SHA256:
        raise ValueError("TD-B cleanup-test provenance manifest hash differs")
    manifest = json.loads(payload)
    required = {
        "schema", "status", "old_checkpoint", "new_checkpoint",
        "human_provenance", "entries", "extra_paths", "qualification_runs",
        "replay_runs", "candidate_builds", "release_generation", "device_calls",
        "network_calls", "env_content_reads", "formal_calls", "git_mutations",
    }
    if (
        set(manifest) != required
        or manifest.get("schema") != "p7_td_b_lineage_cleanup_test_provenance_c1"
        or manifest.get("status") != "pass"
        or manifest.get("old_checkpoint") != TD_B_CLEANUP_TEST_PROVENANCE_OLD
        or manifest.get("new_checkpoint") != TD_B_CLEANUP_TEST_PROVENANCE_NEW
        or manifest.get("human_provenance")
        != (
            "Human instruction recorded in task history; exact commit subject: "
            "fix(p7): bind workflow lineage paths exactly"
        )
        or manifest.get("extra_paths") != []
        or any(manifest.get(name) != 0 for name in (
            "qualification_runs", "replay_runs", "candidate_builds",
            "release_generation", "device_calls", "network_calls",
            "env_content_reads", "formal_calls", "git_mutations",
        ))
    ):
        raise ValueError("TD-B cleanup-test provenance manifest contract differs")
    entries = manifest.get("entries")
    entry_fields = {
        "path", "classification", "old_checkpoint", "new_checkpoint",
        "old_blob_sha256", "current_blob_sha256", "diff_sha256", "scope",
        "human_instruction", "provenance", "rollback", "extra_paths",
    }
    if not isinstance(entries, list) or len(entries) != 2:
        raise ValueError("TD-B cleanup-test provenance manifest entry count differs")
    by_path: dict[str, Mapping[str, Any]] = {}
    for raw_entry in entries:
        if not isinstance(raw_entry, Mapping) or set(raw_entry) != entry_fields:
            raise ValueError("TD-B cleanup-test provenance manifest entry schema differs")
        entry_path = str(raw_entry.get("path"))
        if entry_path in by_path:
            raise ValueError("TD-B cleanup-test provenance manifest contains duplicate paths")
        by_path[entry_path] = raw_entry
    if set(by_path) != set(TD_B_CLEANUP_TEST_PROVENANCE_CLASSIFICATIONS):
        raise ValueError("TD-B cleanup-test provenance exact path set differs")

    for entry_path, classification in TD_B_CLEANUP_TEST_PROVENANCE_CLASSIFICATIONS.items():
        entry = by_path[entry_path]
        if (
            entry.get("classification") != classification
            or entry.get("old_checkpoint") != TD_B_CLEANUP_TEST_PROVENANCE_OLD
            or entry.get("new_checkpoint") != TD_B_CLEANUP_TEST_PROVENANCE_NEW
            or entry.get("scope") != TD_B_CLEANUP_TEST_PROVENANCE_SCOPES[entry_path]
            or entry.get("human_instruction")
            != TD_B_CLEANUP_TEST_PROVENANCE_HUMAN_INSTRUCTION
            or entry.get("provenance")
            != (
                "Human-directed cleanup-test correction implemented by exact commit "
                f"{TD_B_CLEANUP_TEST_PROVENANCE_NEW}"
            )
            or entry.get("rollback")
            != (
                f"restore {entry_path} from checkpoint "
                f"{TD_B_CLEANUP_TEST_PROVENANCE_OLD} and remove only this exact manifest entry"
            )
            or entry.get("extra_paths") != []
            or not all(
                isinstance(entry.get(name), str) and len(str(entry[name])) == 64
                for name in ("old_blob_sha256", "current_blob_sha256", "diff_sha256")
            )
        ):
            raise ValueError(f"TD-B cleanup-test provenance contract differs: {entry_path}")
        working = root / entry_path
        if working.is_symlink() or not working.is_file():
            raise ValueError(f"TD-B cleanup-test provenance owner differs: {entry_path}")
        old = subprocess.run(
            ["git", "show", f"{TD_B_CLEANUP_TEST_PROVENANCE_OLD}:{entry_path}"],
            cwd=root, check=True, capture_output=True,
        ).stdout
        current = subprocess.run(
            ["git", "show", f"{TD_B_CLEANUP_TEST_PROVENANCE_NEW}:{entry_path}"],
            cwd=root, check=True, capture_output=True,
        ).stdout
        checkpoint = subprocess.run(
            ["git", "show", f"{new_checkpoint}:{entry_path}"],
            cwd=root, check=True, capture_output=True,
        ).stdout
        diff = subprocess.run(
            ["git", "diff", TD_B_CLEANUP_TEST_PROVENANCE_OLD,
             TD_B_CLEANUP_TEST_PROVENANCE_NEW, "--", entry_path],
            cwd=root, check=True, capture_output=True,
        ).stdout
        if (
            hashlib.sha256(working.read_bytes()).hexdigest()
            != entry.get("current_blob_sha256")
            or hashlib.sha256(old).hexdigest() != entry.get("old_blob_sha256")
            or hashlib.sha256(current).hexdigest() != entry.get("current_blob_sha256")
            or hashlib.sha256(checkpoint).hexdigest() != entry.get("current_blob_sha256")
            or hashlib.sha256(diff).hexdigest() != entry.get("diff_sha256")
        ):
            raise ValueError(f"TD-B cleanup-test provenance hash or diff differs: {entry_path}")
    return TD_B_CLEANUP_TEST_PROVENANCE_CLASSIFICATIONS


def _validate_td_b_post_eq_policy_lineage(
    *,
    new_checkpoint: str,
    project_root: str | Path = PROJECT_ROOT,
) -> Mapping[str, str]:
    """Validate the exact accepted post-EQ policy commit and mapped path owners."""
    root = Path(project_root).resolve()
    if (
        len(new_checkpoint) != 40
        or any(character not in "0123456789abcdef" for character in new_checkpoint)
    ):
        raise ValueError("TD-B post-EQ policy checkpoint is invalid")
    try:
        resolved = subprocess.run(
            ["git", "rev-parse", new_checkpoint],
            cwd=root, check=True, capture_output=True, text=True,
        ).stdout.strip()
    except subprocess.CalledProcessError as exc:
        raise ValueError("TD-B post-EQ policy checkpoint is invalid") from exc
    if (
        resolved != new_checkpoint
        or not _td_b_checkpoint_contains(
            resolved,
            TD_B_POST_EQ_POLICY_COMMIT,
            project_root=root,
        )
    ):
        raise ValueError("TD-B post-EQ policy checkpoint ancestry differs")

    try:
        parent = subprocess.run(
            ["git", "rev-parse", f"{TD_B_POST_EQ_POLICY_COMMIT}^"],
            cwd=root, check=True, capture_output=True, text=True,
        ).stdout.strip()
        subject = subprocess.run(
            ["git", "show", "-s", "--format=%s", TD_B_POST_EQ_POLICY_COMMIT],
            cwd=root, check=True, capture_output=True, text=True,
        ).stdout.strip()
        path_output = subprocess.run(
            [
                "git", "diff-tree", "--no-commit-id", "--name-only", "-r",
                TD_B_POST_EQ_POLICY_COMMIT,
            ],
            cwd=root, check=True, capture_output=True, text=True,
        ).stdout
    except subprocess.CalledProcessError as exc:
        raise ValueError("TD-B post-EQ policy accepted commit owner differs") from exc
    if parent != TD_B_POST_EQ_POLICY_PARENT:
        raise ValueError("TD-B post-EQ policy accepted parent differs")
    if subject != TD_B_POST_EQ_POLICY_SUBJECT:
        raise ValueError("TD-B post-EQ policy accepted subject differs")
    paths = tuple(sorted(path for path in path_output.splitlines() if path))
    path_payload = "".join(f"{path}\n" for path in paths).encode("utf-8")
    if (
        paths != TD_B_POST_EQ_POLICY_PATHS
        or hashlib.sha256(path_payload).hexdigest()
        != TD_B_POST_EQ_POLICY_PATHS_SHA256
        or set(TD_B_POST_EQ_POLICY_BLOB_SHA256) != set(TD_B_POST_EQ_POLICY_PATHS)
        or not set(TD_B_POST_EQ_POLICY_CLASSIFICATIONS).issubset(paths)
    ):
        raise ValueError("TD-B post-EQ policy accepted path set differs")

    for entry_path in TD_B_POST_EQ_POLICY_PATHS:
        try:
            accepted = subprocess.run(
                ["git", "show", f"{TD_B_POST_EQ_POLICY_COMMIT}:{entry_path}"],
                cwd=root, check=True, capture_output=True,
            ).stdout
        except subprocess.CalledProcessError as exc:
            raise ValueError(
                f"TD-B post-EQ policy accepted Git owner differs: {entry_path}"
            ) from exc
        expected_sha256 = TD_B_POST_EQ_POLICY_BLOB_SHA256[entry_path]
        if hashlib.sha256(accepted).hexdigest() != expected_sha256:
            raise ValueError(
                f"TD-B post-EQ policy accepted blob differs: {entry_path}"
            )
        if entry_path not in TD_B_POST_EQ_POLICY_CLASSIFICATIONS:
            continue
        working = root / entry_path
        if working.is_symlink() or not working.is_file():
            raise ValueError(
                f"TD-B post-EQ policy working owner differs: {entry_path}"
            )
        try:
            checkpoint = subprocess.run(
                ["git", "show", f"{new_checkpoint}:{entry_path}"],
                cwd=root, check=True, capture_output=True,
            ).stdout
        except subprocess.CalledProcessError as exc:
            raise ValueError(
                f"TD-B post-EQ policy checkpoint Git owner differs: {entry_path}"
            ) from exc
        if hashlib.sha256(checkpoint).hexdigest() != expected_sha256:
            raise ValueError(
                f"TD-B post-EQ policy checkpoint blob differs: {entry_path}"
            )
        if hashlib.sha256(working.read_bytes()).hexdigest() != expected_sha256:
            raise ValueError(
                f"TD-B post-EQ policy working owner differs: {entry_path}"
            )
    return TD_B_POST_EQ_POLICY_CLASSIFICATIONS


def build_td_b_setup_release_lineage_candidate(
    release_path: str | Path,
    *,
    old_checkpoint: str,
    new_checkpoint: str,
    changed_paths: Sequence[str],
) -> dict[str, Any]:
    """Build a Planner-only candidate; this never upgrades a production release."""
    if old_checkpoint != TD_B_SETUP_CHECKPOINT:
        raise ValueError("TD-B lineage old checkpoint differs from frozen setup owner")
    if (
        len(new_checkpoint) != 40
        or any(character not in "0123456789abcdef" for character in new_checkpoint)
        or new_checkpoint == old_checkpoint
    ):
        raise ValueError("TD-B lineage new checkpoint is invalid")
    path = Path(release_path).resolve()
    release = json.loads(path.read_text(encoding="utf-8"))
    validated = validate_td_b_setup_release(release, release_path=path)
    if (
        release.get("code_checkpoint") != old_checkpoint
        or validated.get("code_checkpoint") != old_checkpoint
    ):
        raise ValueError("TD-B lineage release is not bound to the frozen setup checkpoint")

    classifications: list[dict[str, str]] = []
    prohibited: list[str] = []
    if not changed_paths:
        raise ValueError("TD-B lineage changed-path ledger must not be empty")
    successor_paths = (
        set(TD_B_PUBLIC_DEFAULT_SUCCESSOR_CLASSIFICATIONS).intersection(changed_paths)
        if _td_b_checkpoint_contains(
            new_checkpoint,
            TD_B_PUBLIC_DEFAULT_SUCCESSOR_COMMIT,
        )
        else set()
    )
    successor_classifications = (
        _validate_td_b_public_default_successor_lineage(new_checkpoint=new_checkpoint)
        if successor_paths
        else {}
    )
    workflow_paths = set(TD_B_WORKFLOW_PATH_CLASSIFICATIONS).intersection(changed_paths)
    workflow_classifications = (
        _validate_td_b_workflow_path_lineage(new_checkpoint=new_checkpoint)
        if workflow_paths
        else {}
    )
    cleanup_test_paths = set(TD_B_CLEANUP_TEST_PROVENANCE_CLASSIFICATIONS).intersection(
        changed_paths
    )
    cleanup_test_classifications = (
        _validate_td_b_cleanup_test_provenance(new_checkpoint=new_checkpoint)
        if cleanup_test_paths
        else {}
    )
    post_eq_paths = set(TD_B_POST_EQ_POLICY_CLASSIFICATIONS).intersection(
        changed_paths
    )
    post_eq_classifications = (
        _validate_td_b_post_eq_policy_lineage(new_checkpoint=new_checkpoint)
        if post_eq_paths
        else {}
    )
    for raw_path in changed_paths:
        changed_path = str(raw_path).strip()
        if not changed_path or changed_path.startswith("/") or ".." in Path(changed_path).parts:
            raise ValueError("TD-B lineage changed path is not repository-relative")
        if changed_path == "AGENTS.md":
            _validate_td_b_agents_policy_lineage(
                old_checkpoint=old_checkpoint,
                new_checkpoint=new_checkpoint,
            )
            classification = "bounded_validation_or_documentation"
        elif changed_path in successor_classifications:
            classification = successor_classifications[changed_path]
        elif changed_path in workflow_classifications:
            classification = workflow_classifications[changed_path]
        elif changed_path in cleanup_test_classifications:
            classification = cleanup_test_classifications[changed_path]
        elif changed_path in post_eq_classifications:
            classification = post_eq_classifications[changed_path]
        elif changed_path in TD_B_LINEAGE_ALLOWED_PRODUCTION_PATHS:
            classification = "ambient_and_physical_ledger_contract"
        elif changed_path in TD_B_LINEAGE_ALLOWED_VALIDATION_PATHS:
            classification = "bounded_validation_or_documentation"
        elif changed_path.startswith(".agent-work/"):
            classification = "planner_or_execution_audit_only"
        else:
            classification = "prohibited_or_unreviewed"
            prohibited.append(changed_path)
        classifications.append({"path": changed_path, "classification": classification})
    if len(classifications) != len({item["path"] for item in classifications}):
        raise ValueError("TD-B lineage changed-path ledger contains duplicates")

    eligible = not prohibited
    return {
        "schema": TD_B_SETUP_RELEASE_LINEAGE_CANDIDATE_SCHEMA,
        "status": (
            "eligible_waiting_for_planner"
            if eligible
            else "ineligible_requires_new_setup"
        ),
        "old_checkpoint": old_checkpoint,
        "new_checkpoint": new_checkpoint,
        "release_reference": file_reference(path),
        "canonical_setup_reference": dict(release["canonical_setup"]),
        "resolved_formal_plan_reference": dict(release["resolved_formal_plan"]),
        "changed_paths": classifications,
        "prohibited_paths": prohibited,
        "canonical_setup_replay": "pass",
        "production_release_usable": False,
        "planner_acceptance_required": True,
    }


def _validate_td_b_planner_lineage_candidate(
    candidate: Mapping[str, Any],
    *,
    candidate_path: str | Path,
    legacy_release_path: str | Path,
) -> None:
    path = Path(candidate_path).resolve()
    legacy_path = Path(legacy_release_path).resolve()
    if (
        path != TD_B_F0A_LINEAGE_CANDIDATE_PATH.resolve()
        or not path.is_file()
        or hashlib.sha256(path.read_bytes()).hexdigest()
        != TD_B_F0A_LINEAGE_CANDIDATE_SHA256
    ):
        raise ValueError("TD-B Planner lineage candidate owner or hash differs")
    required = {
        "schema", "status", "old_checkpoint", "new_checkpoint",
        "release_reference", "canonical_setup_reference",
        "resolved_formal_plan_reference", "changed_paths", "prohibited_paths",
        "canonical_setup_replay", "production_release_usable",
        "planner_acceptance_required",
    }
    if (
        set(candidate) != required
        or candidate.get("schema") != TD_B_SETUP_RELEASE_LINEAGE_CANDIDATE_SCHEMA
        or candidate.get("status") != "eligible_waiting_for_planner"
        or candidate.get("old_checkpoint") != TD_B_SETUP_CHECKPOINT
        or candidate.get("new_checkpoint") != TD_B_F0A_CHECKPOINT
        or candidate.get("release_reference") != file_reference(legacy_path)
        or candidate.get("canonical_setup_replay") != "pass"
        or candidate.get("production_release_usable") is not False
        or candidate.get("planner_acceptance_required") is not True
        or candidate.get("prohibited_paths") != []
    ):
        raise ValueError("TD-B Planner lineage candidate contract differs")
    changed = candidate.get("changed_paths")
    if (
        not isinstance(changed, list)
        or not changed
        or any(
            not isinstance(item, Mapping)
            or set(item) != {"path", "classification"}
            for item in changed
        )
    ):
        raise ValueError("TD-B Planner lineage changed-path evidence differs")


def _normalize_td_b_resolved_plan(plan: Mapping[str, Any]) -> dict[str, Any]:
    normalized = deepcopy(dict(plan))
    normalized.pop("created_at", None)
    return normalized


def validate_td_b_lineage_resolved_plan(
    plan: Mapping[str, Any],
    *,
    canonical_setup_path: str | Path,
) -> None:
    setup_path = Path(canonical_setup_path).resolve()
    expected = build_diagnostic_plan(
        TD_B,
        source="ray",
        prerequisite_artifact=OPERATING_ENVELOPE_V2_PATH,
        for_execution=True,
        human_authorization=TD_B,
        v2_capture_capability=True,
    )
    expected = resolve_td_b_plan_with_setup(
        expected,
        setup_artifact_path=setup_path,
    )
    expected["setup_lineage_release_required"] = True
    if _normalize_td_b_resolved_plan(plan) != _normalize_td_b_resolved_plan(expected):
        raise ValueError("TD-B lineage resolved plan differs from current frozen plan")
    captures = plan.get("captures")
    budgets = plan.get("budgets")
    if (
        not isinstance(captures, list)
        or len(captures) != 16
        or any(step.get("capture_role") != "formal" for step in captures)
        or any(step.get("source_id") != "ray" for step in captures)
        or plan.get("native_raw_ambient_policy")
        != AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT
        or not isinstance(budgets, Mapping)
        or budgets.get("formal_cap") != 16
        or budgets.get("ambient_cap") != 0
        or budgets.get("physical_cr3_cap") != 24
        or plan.get("setup_physical_cr3_count") != 2
        or plan.get("formal_capture_eligible") is not True
        or plan.get("setup_lineage_release_required") is not True
    ):
        raise ValueError("TD-B lineage resolved plan protocol differs")


def validate_td_b_setup_lineage_release(
    release: Mapping[str, Any],
    *,
    release_path: str | Path,
    changed_paths_fn: Callable[[str, str], Sequence[str]] | None = None,
) -> dict[str, Any]:
    requested_path = Path(release_path)
    if requested_path.is_symlink():
        raise ValueError("TD-B setup lineage release cannot be a symlink")
    path = requested_path.resolve()
    required = {
        "schema", "status", "production_release_usable",
        "old_checkpoint", "code_checkpoint", "legacy_release",
        "planner_lineage_candidate", "current_lineage_candidate",
        "canonical_setup", "resolved_formal_plan",
    }
    if (
        set(release) != required
        or release.get("schema") != TD_B_SETUP_LINEAGE_RELEASE_SCHEMA
        or release.get("status") != "formal_plan_lineage_qualified"
        or release.get("production_release_usable") is not True
        or release.get("old_checkpoint") != TD_B_SETUP_CHECKPOINT
    ):
        raise ValueError("TD-B setup lineage release schema or status differs")
    checkpoint = release.get("code_checkpoint")
    if (
        not isinstance(checkpoint, str)
        or len(checkpoint) != 40
        or any(character not in "0123456789abcdef" for character in checkpoint)
        or checkpoint in {TD_B_SETUP_CHECKPOINT, TD_B_F0A_CHECKPOINT}
    ):
        raise ValueError("TD-B setup lineage release checkpoint differs")

    references: dict[str, Path] = {}
    for name in (
        "legacy_release", "planner_lineage_candidate",
        "current_lineage_candidate", "canonical_setup", "resolved_formal_plan",
    ):
        reference = release.get(name)
        if not isinstance(reference, Mapping) or set(reference) != {"path", "sha256"}:
            raise ValueError(f"TD-B setup lineage release {name} reference differs")
        target = Path(str(reference.get("path"))).resolve()
        if (
            not target.is_file()
            or target.is_symlink()
            or hashlib.sha256(target.read_bytes()).hexdigest()
            != reference.get("sha256")
        ):
            raise ValueError(f"TD-B setup lineage release {name} owner or hash differs")
        references[name] = target
    if (
        references["legacy_release"] != TD_B_SETUP_RELEASE_PATH.resolve()
        or references["planner_lineage_candidate"]
        != TD_B_F0A_LINEAGE_CANDIDATE_PATH.resolve()
        or references["current_lineage_candidate"].parent != path.parent
        or references["resolved_formal_plan"].parent != path.parent
    ):
        raise ValueError("TD-B setup lineage release path ownership differs")

    legacy = json.loads(references["legacy_release"].read_text(encoding="utf-8"))
    legacy_validated = validate_td_b_setup_release(
        legacy,
        release_path=references["legacy_release"],
    )
    if legacy_validated.get("code_checkpoint") != TD_B_SETUP_CHECKPOINT:
        raise ValueError("TD-B setup lineage legacy checkpoint differs")
    if references["canonical_setup"] != Path(
        legacy_validated["canonical_path"]
    ).resolve():
        raise ValueError("TD-B setup lineage canonical setup differs")

    planner_candidate = json.loads(
        references["planner_lineage_candidate"].read_text(encoding="utf-8")
    )
    _validate_td_b_planner_lineage_candidate(
        planner_candidate,
        candidate_path=references["planner_lineage_candidate"],
        legacy_release_path=references["legacy_release"],
    )
    current_candidate = json.loads(
        references["current_lineage_candidate"].read_text(encoding="utf-8")
    )
    if changed_paths_fn is None:
        changed_paths = changed_paths_between_checkpoints(
            TD_B_SETUP_CHECKPOINT,
            checkpoint,
        )
    else:
        changed_paths = list(
            changed_paths_fn(TD_B_SETUP_CHECKPOINT, checkpoint)
        )
    expected_candidate = build_td_b_setup_release_lineage_candidate(
        references["legacy_release"],
        old_checkpoint=TD_B_SETUP_CHECKPOINT,
        new_checkpoint=checkpoint,
        changed_paths=changed_paths,
    )
    if (
        current_candidate != expected_candidate
        or current_candidate.get("status") != "eligible_waiting_for_planner"
        or current_candidate.get("production_release_usable") is not False
        or current_candidate.get("prohibited_paths") != []
    ):
        raise ValueError("TD-B setup current lineage candidate differs")

    resolved = json.loads(
        references["resolved_formal_plan"].read_text(encoding="utf-8")
    )
    validate_td_b_lineage_resolved_plan(
        resolved,
        canonical_setup_path=references["canonical_setup"],
    )
    return {
        **legacy_validated,
        "schema": TD_B_SETUP_LINEAGE_RELEASE_SCHEMA,
        "code_checkpoint": checkpoint,
        "resolved_plan": resolved,
        "lineage_release_path": str(path),
    }


def validate_td_b_setup_cleanup(value: Any) -> None:
    if not isinstance(value, Mapping) or set(value) != {"python", "shell", "wrapper", "final_both_off"}:
        raise ValueError("TD-B setup cleanup evidence is incomplete")
    for owner in ("python", "shell"):
        row = value.get(owner)
        if not isinstance(row, Mapping) or set(row) != {"status", "steps", "exit_code"}:
            raise ValueError(f"TD-B setup {owner} cleanup schema differs")
        if row.get("status") != "pass" or row.get("exit_code") != 0:
            raise ValueError(f"TD-B setup {owner} cleanup failed")
        steps = row.get("steps")
        if not isinstance(steps, list) or len(steps) != 2:
            raise ValueError(f"TD-B setup {owner} cleanup lacks two shutdown owners")
        by_name = {step.get("name"): step for step in steps if isinstance(step, Mapping)}
        if set(by_name) != {"esphome", "ray120c"} or any(
            set(step) != {"name", "ok", "detail", "error"} or step.get("ok") is not True or step.get("error") is not None
            for step in by_name.values()
        ):
            raise ValueError(f"TD-B setup {owner} cleanup step evidence is invalid")
    wrapper = value.get("wrapper")
    if not isinstance(wrapper, Mapping) or set(wrapper) != {
        "status", "child_exit_code", "shell_cleanup_exit_code", "wrapper_exit_code", "signal",
    }:
        raise ValueError("TD-B setup wrapper cleanup schema differs")
    if (
        wrapper.get("status") != "complete"
        or wrapper.get("child_exit_code") != 0
        or wrapper.get("shell_cleanup_exit_code") != 0
        or wrapper.get("wrapper_exit_code") != 0
        or wrapper.get("signal") is not None
    ):
        raise ValueError("TD-B setup wrapper child/signal/cleanup evidence failed")
    final = value.get("final_both_off")
    if not isinstance(final, Mapping) or set(final) != {"strip_device_evidence", "ray_readback"}:
        raise ValueError("TD-B setup final both-off evidence is incomplete")
    from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import validate_both_off
    curve = json.loads(CURVE_PATH.read_text(encoding="utf-8"))
    validate_both_off(final["strip_device_evidence"], final["ray_readback"], curve)


def build_td_b_exposure_setup_artifact(
    *, attempts: Sequence[Mapping[str, Any]], camera: Mapping[str, Any],
    historical_seed: Mapping[str, Any], isolation: Mapping[str, Any],
    cold_proxy: Mapping[str, Any], cleanup: Mapping[str, Any],
    code_checkpoint: str, fake_only: bool,
) -> dict[str, Any]:
    """Produce the canonical setup artifact from adapter-owned attempt evidence."""
    rows = [deepcopy(dict(row)) for row in attempts]
    final = [row for row in rows if row.get("disposition") == "final"]
    artifact = {
        "schema": TD_B_SETUP_SCHEMA,
        "experiment_id": TD_B,
        "source": "ray",
        "state_id": TD_B_SETUP_STATE,
        "command": dict(TD_B_SETUP_COMMAND),
        "command_sha256": canonical_sha256(dict(TD_B_SETUP_COMMAND)),
        "capture_role": "exposure_setup",
        "formal_measurement": False,
        "counts_as_physical": True,
        "enters_58_feature_fit": False,
        "enters_repeatability_covariance": False,
        "enters_td_b_history_aggregate": False,
        "setup_method": "bounded_remote_v2_auto_exposure",
        "historical_seed": deepcopy(dict(historical_seed)),
        "camera": deepcopy(dict(camera)),
        "attempts": rows,
        "final_capture_id": final[0].get("capture_id") if len(final) == 1 else None,
        "resolved_shutter_speed": final[0].get("shutter_speed") if len(final) == 1 else None,
        "setup_physical_cr3_count": len(rows),
        "setup_physical_cr3_cap": TD_B_SETUP_PHYSICAL_CAP,
        "input_hashes": {
            "location": file_reference(LOCATION_PATH)["sha256"],
            "policy": file_reference(POLICY_PATH)["sha256"],
            "operating_envelope": file_reference(OPERATING_ENVELOPE_V2_PATH)["sha256"],
        },
        "code_checkpoint": code_checkpoint,
        "isolation": deepcopy(dict(isolation)),
        "cold_proxy": deepcopy(dict(cold_proxy)),
        "cleanup": deepcopy(dict(cleanup)),
        "failure": None,
        "fake_only": bool(fake_only),
    }
    validate_td_b_exposure_setup(artifact)
    return artifact


def resolve_td_b_plan_with_setup(
    plan: Mapping[str, Any], *, setup_artifact_path: str | Path,
) -> dict[str, Any]:
    if plan.get("experiment_id") != TD_B or plan.get("source") != "ray":
        raise ValueError("TD-B exposure setup can only resolve the Ray TD-B plan")
    path = Path(setup_artifact_path).resolve()
    artifact = json.loads(path.read_text(encoding="utf-8"))
    validated = validate_td_b_exposure_setup(artifact, artifact_path=path)
    fake_only = artifact.get("fake_only") is True
    if artifact.get("schema") == TD_B_SETUP_SCHEMA_V2:
        fake_only = False
    if not fake_only:
        checkpoint = validated.get("code_checkpoint", artifact.get("code_checkpoint"))
        if not isinstance(checkpoint, str) or len(checkpoint) != 40 or any(ch not in "0123456789abcdef" for ch in checkpoint):
            raise ValueError("TD-B retained setup lacks a full lowercase Git checkpoint")
    resolved = deepcopy(dict(plan))
    if resolved.get("frozen_shutters", {}).get(TD_B_SETUP_CACHE_KEY) is not None or TD_B_SETUP_CACHE_KEY not in resolved.get("exposure_setup_required", []):
        raise ValueError("TD-B Ray plan does not own the unresolved setup shutter")
    resolved["frozen_shutters"][TD_B_SETUP_CACHE_KEY] = validated["resolved_shutter_speed"]
    resolved["exposure_setup_required"] = []
    resolved["shutter_ledger_provenance"]["frozen_shutters_sha256"] = canonical_sha256(resolved["frozen_shutters"])
    resolved["exposure_setup_artifact"] = file_reference(path)
    resolved["setup_physical_cr3_count"] = validated["physical_count"]
    resolved["formal_capture_eligible"] = not fake_only
    resolved["status"] = "fake_resolved_device_locked" if fake_only else resolved["status"]
    return resolved


def replay_td_b_setup_resolution(
    plan: Mapping[str, Any], *, setup_artifact_path: str | Path,
) -> dict[str, Any]:
    """Public offline replay for both fake fixtures and future retained setup evidence."""
    inputs = plan.get("inputs")
    if not isinstance(inputs, Mapping):
        raise ValueError("TD-B setup replay lacks frozen inputs")
    validate_trusted_operating_envelope_reference(
        inputs.get("operating_envelope", {}), require_v2=True,
    )
    resolved = resolve_td_b_plan_with_setup(plan, setup_artifact_path=setup_artifact_path)
    path = Path(setup_artifact_path).resolve()
    artifact = json.loads(path.read_text(encoding="utf-8"))
    validated = validate_td_b_exposure_setup(artifact, artifact_path=path)
    if resolved.get("exposure_setup_required") or not resolved["frozen_shutters"].get(TD_B_SETUP_CACHE_KEY):
        raise ValueError("TD-B setup replay did not resolve the formal shutter ledger")
    return {
        "schema": "p7_td_b_exposure_setup_replay_v1",
        "status": "offline_fake_replay_pass" if artifact.get("fake_only") else "retained_setup_replay_pass",
        "formal_capture_eligible": bool(resolved.get("formal_capture_eligible")),
        "fake_only": bool(artifact.get("fake_only")),
        "setup_artifact": file_reference(path),
        "resolved_plan_sha256": canonical_sha256(resolved),
        "setup_physical_cr3_count": validated["physical_count"],
        "formal_capture_count": int(resolved["budgets"]["formal_cap"]),
        "physical_cr3_cap": int(resolved["budgets"]["physical_cr3_cap"]),
        "setup_excluded_from_formal_statistics": True,
        "setup_excluded_from_58_feature_fit": True,
        "setup_excluded_from_repeatability_covariance": True,
        "setup_excluded_from_td_b_history_aggregate": True,
    }


def build_diagnostic_plan(
    experiment_id: str,
    *,
    source: str | None = None,
    variant: str = "core",
    r1_run: str | Path = R1_RUN,
    prerequisite_artifact: str | Path = OPERATING_ENVELOPE_PATH,
    for_execution: bool = False,
    human_authorization: str | None = None,
    exposure_start_capability: bool = False,
    v2_capture_capability: bool = False,
) -> dict[str, Any]:
    if experiment_id not in EXPERIMENT_IDS:
        raise ValueError(f"unsupported exact experiment id: {experiment_id}")
    if source not in {None, "ray", "strip"}:
        raise ValueError("source must be ray or strip")
    if experiment_id in {TD_A, TD_B} and source is None:
        raise ValueError("TD-A/TD-B plans are source-specific")
    if experiment_id == TD_C and source is not None:
        raise ValueError("TD-C plans own both sources")
    if experiment_id == TD_C and variant not in {"core", "expansion"}:
        raise ValueError("TD-C variant must be core or expansion")

    prerequisite = resolve_trusted_operating_envelope(prerequisite_artifact)
    envelope = prerequisite["envelope"]
    _enforce_prerequisites(experiment_id, variant, envelope, for_execution=for_execution)
    if for_execution and human_authorization != experiment_id:
        raise PermissionError(f"execution requires exact Human authorization for {experiment_id}")
    timing_capability = bool(v2_capture_capability)
    if for_execution and not timing_capability:
        raise PermissionError("execution requires remote v2 capture timing capability")

    commands = load_r1_commands(r1_run)
    retained_shutters = load_r1_shutters(r1_run)
    if experiment_id == TD_A:
        stage_plan = _td_a_plan(str(source), commands)
    elif experiment_id == TD_B:
        stage_plan = _td_b_plan(str(source), commands, envelope)
    else:
        stage_plan = _td_c_plan(variant, commands, envelope)
    required_shutters = required_shutter_cache_keys(stage_plan["captures"])
    frozen_shutters = {key: retained_shutters.get(key) for key in required_shutters}
    inputs = {
        "r1_commands": file_reference(Path(r1_run) / "commands.jsonl"),
        "r1_plan": file_reference(Path(r1_run) / "plan.json"),
        "policy": file_reference(POLICY_PATH),
        "observer": file_reference(OBSERVER_PATH),
        "uncertainty": file_reference(UNCERTAINTY_PATH),
        "manifold": file_reference(MANIFOLD_PATH),
        "location": file_reference(LOCATION_PATH),
        "code_duty_curve": file_reference(CURVE_PATH),
        "operating_envelope": prerequisite["reference"],
    }
    plan = {
        "schema": PLAN_SCHEMA_V2,
        "status": "execute_authorized" if for_execution else "dry_run_complete_device_locked",
        "experiment_id": experiment_id,
        "variant": variant,
        "source": source,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": inputs,
        "camera": {
            "backend": "remote", "location": inputs["location"],
            "auto_exposure_in_timed_cycle": False,
            "actual_exposure_start_provenance_required": False,
            "adapter_capability_available": timing_capability,
            "v2_capture_timing_capability_available": timing_capability,
            "legacy_exposure_start_capability_deprecated_dry_run_only": bool(exposure_start_capability),
        },
        "execution_authorization": {
            "human_authorization_experiment_id": experiment_id if for_execution else None,
            "human_authorization_verified": bool(for_execution and human_authorization == experiment_id),
            "remote_v2_capability": timing_capability,
        },
        "timing_contract": timing_contract(2),
        "cold_proxy": envelope["cold_proxy"],
        "cleanup": {"python_finally": "required", "shell_trap": "EXIT_INT_TERM_HUP_required"},
        "offline_contract": {"env_calls": 0, "network_calls": 0, "device_calls": 0, "all_off_calls": 0},
        "hard_locks": {
            "sentinel_v2": True, "remaining_9": True, "boundary": True,
            "holdout": True, "P8": True, "Gate_6": True,
            "cold_steady_covariance_merge": True,
        },
        "formal_capture_eligible": False,
        "frozen_shutters": frozen_shutters,
        "exposure_setup_required": sorted(key for key, value in frozen_shutters.items() if value is None),
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": list(required_shutters),
            "frozen_shutters_sha256": canonical_sha256(frozen_shutters),
        },
        "capture_ledger_contract": {
            "formal_measurement": "boolean", "capture_role": ["formal", "ambient"],
            "ambient_counts_as_physical_cr3": True,
            "physical_return_ledger_schema": PHYSICAL_RETURN_LEDGER_SCHEMA,
            "physical_return_precedes_measurement_acceptance": True,
        },
        "native_raw_ambient_policy": expected_native_raw_ambient_policy(
            experiment_id,
            plan_schema=PLAN_SCHEMA_V2,
        ),
        "source_isolation_contract": "independent_both_off_readback_at_run_ambient_and_transition_gates",
    }
    plan.update(stage_plan)
    return plan


def _enforce_prerequisites(
    experiment_id: str, variant: str, envelope: Mapping[str, Any], *, for_execution: bool
) -> None:
    if not for_execution:
        return
    if experiment_id == TD_B:
        mode = validate_operating_envelope(envelope, require_v2=False)
        if mode["mode"] == "developer_human_override":
            return
        if envelope.get("status") != "td_a_pass":
            raise PermissionError("TD-B execute plan is locked until TD-A passes")
        if envelope.get("t_formal_provisional_s") not in SELECTABLE_SETTLE_POINTS:
            raise PermissionError("TD-B execute plan requires frozen t_formal_provisional_s in 60/120/300")
    if experiment_id == TD_C and envelope.get("status") not in {"td_b_pass", "td_c_core_pass_waiting_for_planner"}:
        raise PermissionError("TD-C execute plan is locked until TD-B passes")
    if experiment_id == TD_C and envelope.get("t_formal_s") not in SELECTABLE_SETTLE_POINTS:
        raise PermissionError("TD-C execute plan requires frozen t_formal_s in 60/120/300")
    if experiment_id == TD_C and variant == "expansion" and envelope.get("status") != "td_c_core_pass_waiting_for_planner":
        raise PermissionError("TD-C expansion is locked until core Planner acceptance")


def _step(
    source: str, state: str, elapsed: int | None, index: int,
    commands: Mapping[str, Mapping[str, int]], **extra: Any,
) -> dict[str, Any]:
    command = _command(source, state, commands)
    suffix = "deferred" if elapsed is None else str(elapsed)
    return {
        "capture_id": f"{index:03d}-{source}-{state.lower()}-t{suffix}",
        "source_id": source,
        "state_id": state,
        "command": command,
        "exact_command_hash": canonical_sha256(command),
        "requested_elapsed_s": elapsed,
        "timing_acceptance": "observed_elapsed_record_only" if elapsed is not None else None,
        "timing_status": "resolved" if elapsed is not None else "deferred",
        "formal_measurement": True,
        "capture_role": "formal",
        **extra,
    }


def _ambient_step(index: int, *, position: str, **extra: Any) -> dict[str, Any]:
    return {
        "capture_id": f"{index:03d}-ambient-{position}",
        "source_id": "ambient", "state_id": "ambient",
        "command": None, "exact_command_hash": canonical_sha256({"strip": "off", "ray": "off"}),
        "requested_elapsed_s": None, "timing_acceptance": None,
        "timing_status": "diagnostic_not_timed", "formal_measurement": False,
        "capture_role": "ambient", "ambient_position": position,
        **extra,
    }


def _td_a_plan(source: str, commands: Mapping[str, Mapping[str, int]]) -> dict[str, Any]:
    steps = [_ambient_step(0, position="start", isolation_gate_before="run_start_ambient_start")]
    for cycle in range(1, 4):
        for elapsed in TIMED_POINTS:
            steps.append(_step(
                source, "A", elapsed, len(steps), commands, cycle_index=cycle,
                isolation_gate_after=(f"after_cycle_{cycle}" if elapsed == 600 else None),
            ))
        if cycle == 2:
            steps.append(_ambient_step(
                len(steps), position="mid", cycle_index=cycle,
                isolation_gate_before="after_cycle_2_ambient_mid",
            ))
    steps.append(_ambient_step(
        len(steps), position="end", isolation_gate_before="after_cycle_3_ambient_end",
    ))
    return {
        "stage": "TD-A", "timing_schedule_s": list(TIMED_POINTS), "cycles": 3,
        "cold_proxy_wait_s": 1800,
        "captures": steps, "budgets": {"formal_cap": 12, "ambient_cap": 3, "physical_cr3_cap": 22},
        "continuous_command_between_timed_points": True,
        "exposure": {"source_specific_shutter_frozen_before_cycle": True, "setup_is_nonformal": True},
        "analysis_contract": {"settle_candidates_s": list(SELECTABLE_SETTLE_POINTS), "six_hundred_is_validation_only": True},
    }


def _td_b_plan(source: str, commands: Mapping[str, Mapping[str, int]], envelope: Mapping[str, Any]) -> dict[str, Any]:
    envelope_mode = validate_operating_envelope(envelope)
    override = envelope_mode["mode"] == "developer_human_override"
    provisional = envelope_mode["operational_dwell_s"] if override else envelope.get("t_formal_provisional_s")
    schedule: list[tuple[str, int | None, str]] = [("A", 600, "initial_anchor")]
    for state in ("D", "B", "C"):
        schedule.extend((state, elapsed, "switch_curve") for elapsed in TIMED_POINTS)
        schedule.append(("A", None if provisional is None else int(provisional), f"return_after_{state}"))
    steps = []
    for index, (state, elapsed, role) in enumerate(schedule):
        next_group = None if index + 1 == len(schedule) else (schedule[index + 1][0], schedule[index + 1][2])
        current_group = (state, role)
        steps.append(_step(
            source, state, elapsed, index, commands, role=role,
            timing_status=("deferred_until_td_a" if elapsed is None else "resolved"),
            isolation_gate_after=(f"after_{role}" if next_group != current_group else None),
        ))
    return {
        "stage": "TD-B", "captures": steps,
        "budgets": {"formal_cap": 16, "ambient_cap": 0, "setup_physical_cr3_cap": 8, "physical_cr3_cap": 24},
        "timing_resolution": "developer_override_resolved" if override else ("deferred_until_td_a" if provisional is None else "resolved"),
        "continuous_command_between_timed_points": True,
        "analysis_contract": {"return_anchor_states": ["A0", "A_after_D", "A_after_B", "A_after_C"]},
        "execute_lock": "developer_override_requires_new_bounded_plan" if override else "td_a_pass_required",
        "operational_dwell": td_b_operational_dwell_metadata(envelope),
    }


def _td_c_plan(variant: str, commands: Mapping[str, Mapping[str, int]], envelope: Mapping[str, Any]) -> dict[str, Any]:
    if variant == "core":
        states = ("A",)
        orders = (("ray", "strip"), ("strip", "ray"), ("ray", "strip"), ("strip", "ray"))
        physical = 16
    else:
        states = ("B", "C")
        orders = (("ray", "strip"), ("strip", "ray"))
        physical = 20
    formal_value = envelope.get("t_formal_s")
    elapsed = None if formal_value is None else int(formal_value)
    steps = []
    for state in states:
        for session_index, order in enumerate(orders, start=1):
            steps.append(_ambient_step(
                len(steps), position=f"session_{session_index}_{state}_start",
                state_group=state, session_index=session_index,
                isolation_gate_before=f"session_{session_index}_{state}_start_ambient",
            ))
            for source_order, source in enumerate(order, start=1):
                steps.append(_step(
                    source, state, elapsed, len(steps), commands,
                    session_index=session_index, source_order=source_order,
                    timing_status=("deferred_until_td_b" if elapsed is None else "resolved"),
                    isolation_gate_after=f"session_{session_index}_{state}_after_{source}",
                ))
            steps.append(_ambient_step(
                len(steps), position=f"session_{session_index}_{state}_end",
                state_group=state, session_index=session_index,
                isolation_gate_before=f"session_{session_index}_{state}_end_ambient",
            ))
    return {
        "stage": "TD-C", "comparison_design": "order_balanced_paired_comparison_not_classic_abba",
        "cold_proxy_wait_s": 1800,
        "session_orders": [list(order) for order in orders], "captures": steps,
        "budgets": {"formal_cap": 8, "ambient_cap": 8, "physical_cr3_cap": physical},
        "timing_resolution": "deferred_until_td_b" if elapsed is None else "resolved",
        "execute_lock": "td_b_pass_required" if variant == "core" else "td_c_core_planner_acceptance_required",
    }


@dataclass(frozen=True)
class TimedCaptureResult:
    nominal_slot_s: float
    best_effort_exposure_start_elapsed_s: float
    timing_offset_s: float
    timing_evidence_status: str
    capture: Mapping[str, Any]


def run_timed_schedule(
    requested_points_s: Sequence[int],
    *,
    command_apply_fn: Callable[[], Any],
    readback_fn: Callable[[], Any],
    capture_fn: Callable[[int], Mapping[str, Any]],
    monotonic_fn: Callable[[], float],
    sleep_fn: Callable[[float], None],
) -> list[TimedCaptureResult]:
    command_apply_fn()
    readback_fn()
    owner_start = monotonic_fn()
    output = []
    for requested in requested_points_s:
        remaining = owner_start + float(requested) - monotonic_fn()
        if remaining > 0:
            sleep_fn(remaining)
        capture = dict(capture_fn(int(requested)))
        timing = capture.get("timing_evidence")
        if not isinstance(timing, Mapping):
            raise ValueError("timed capture lacks best-effort timing evidence")
        observed = timing.get("best_effort_elapsed_s")
        if (
            timing.get("tier") not in ACCEPTED_TIMING_TIERS
            or timing.get("status") != "accepted_best_effort_anchor"
            or timing.get("provenance") != TIMING_CONTRACT_V2["provenance"]
            or isinstance(observed, bool)
            or not isinstance(observed, (int, float))
            or not math.isfinite(float(observed))
            or float(observed) < 0
        ):
            raise ValueError("timed capture lacks accepted best-effort observed elapsed evidence")
        offset = float(observed) - float(requested)
        output.append(TimedCaptureResult(
            float(requested), float(observed), offset, "accepted", capture,
        ))
    return output


def timing_sequence_identity(experiment_id: str, step: Mapping[str, Any]) -> tuple[Any, ...]:
    if not step.get("formal_measurement"):
        raise ValueError("timing sequence identity requires a formal capture step")
    source = step.get("source_id")
    state = step.get("state_id")
    if not isinstance(source, str) or not source or not isinstance(state, str) or not state:
        raise ValueError("thermal timing sequence lacks source/state identity")
    if experiment_id == TD_A:
        cycle = step.get("cycle_index")
        if type(cycle) is not int or cycle <= 0:
            raise ValueError("TD-A timing sequence lacks cycle identity")
        return (experiment_id, source, state, cycle)
    if experiment_id == TD_B:
        role = step.get("role")
        if not isinstance(role, str) or not role:
            raise ValueError("TD-B timing sequence lacks switch/return role identity")
        return (experiment_id, source, state, role)
    if experiment_id == TD_C:
        session = step.get("session_index")
        if type(session) is not int or session <= 0:
            raise ValueError("TD-C timing sequence lacks session identity")
        return (experiment_id, source, state, session)
    raise ValueError(f"unsupported thermal experiment identity: {experiment_id}")


def strip_duty(command: Mapping[str, int], curve: Mapping[str, Any]) -> dict[str, float]:
    points = curve.get("channels", curve)
    result: dict[str, float] = {}
    for channel in CHANNELS:
        channel_data = points[channel]
        entries = channel_data.get("measured_points", channel_data) if isinstance(channel_data, Mapping) else channel_data
        xs = np.asarray([float(item["code"] if isinstance(item, Mapping) else item[0]) for item in entries])
        ys = np.asarray([float(item.get("duty", item.get("linear", 0.0)) if isinstance(item, Mapping) else item[1]) for item in entries])
        result[channel] = float(np.interp(float(command[channel]), xs, ys))
    return result


def build_covariate_record(
    *, source_id: str, state_id: str, command: Mapping[str, Any], sequence_index: int,
    capture_order: int, source_order: int, monotonic_timestamp_ns: int,
    wall_clock_timestamp: str, session_elapsed_s: float, source_on_elapsed_s: float,
    state_on_elapsed_s: float, off_duration_before_s: float,
    previous_state_id: str | None, previous_state_dwell_s: float | None,
    shutter_seconds: float, raw_black_levels: Sequence[float], raw_white_level: float,
    load_history: Mapping[int, float], readback: Mapping[str, Any] | None = None,
    curve: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    record = {
        "monotonic_timestamp_ns": int(monotonic_timestamp_ns),
        "wall_clock_timestamp": str(wall_clock_timestamp),
        "session_elapsed_s": float(session_elapsed_s), "source_id": source_id,
        "state_id": state_id, "exact_command_hash": canonical_sha256(command),
        "source_on_elapsed_s": float(source_on_elapsed_s), "state_on_elapsed_s": float(state_on_elapsed_s),
        "off_duration_before_s": float(off_duration_before_s), "previous_state_id": previous_state_id,
        "previous_state_dwell_s": previous_state_dwell_s, "sequence_index": int(sequence_index),
        "capture_order": int(capture_order), "source_order": int(source_order),
        "ambient_temperature_c": None, "source_surface_temperature_c": None,
        "fan_mode": None, "power_mode": None, "shutter_seconds": float(shutter_seconds),
        "raw_black_levels": [float(value) for value in raw_black_levels],
        "raw_white_level": float(raw_white_level),
        "load_history_proxy_60s": float(load_history[60]),
        "load_history_proxy_300s": float(load_history[300]),
        "load_history_proxy_900s": float(load_history[900]),
    }
    if source_id == "strip":
        if curve is None:
            raise ValueError("strip covariates require the frozen code-duty curve")
        duty = strip_duty({key: int(command[key]) for key in CHANNELS}, curve)
        record.update({key: int(command[key]) for key in CHANNELS})
        record["linearized_duty"] = duty
        record["sum_duty"] = float(sum(duty.values()))
        record["rolling_integrated_sum_duty_history"] = {str(key): float(load_history[key]) for key in (60, 300, 900)}
    elif source_id == "ray":
        record["hsi_command"] = dict(command)
        record["hsi_readback"] = None if readback is None else dict(readback)
        record["rolling_int_on_history"] = {str(key): float(load_history[key]) for key in (60, 300, 900)}
        record["load_proxy_quality"] = "command_only_not_electrical_power"
    elif source_id == "ambient":
        record["ambient_diagnostic_only"] = True
        record["both_sources_verified_off"] = True
    else:
        raise ValueError("covariate source must be ray, strip, or ambient")
    validate_covariate_record(record, expected_command=command)
    return record


def validate_covariate_record(record: Mapping[str, Any], *, expected_command: Mapping[str, Any]) -> None:
    missing = [key for key in REQUIRED_COVARIATES if key not in record]
    if missing:
        raise ValueError(f"thermal covariate fields missing: {missing}")
    if record["exact_command_hash"] != canonical_sha256(expected_command):
        raise ValueError("thermal covariate command hash mismatch")
    for key in ("ambient_temperature_c", "source_surface_temperature_c"):
        value = record[key]
        if value is not None and (not isinstance(value, (int, float)) or not np.isfinite(value)):
            raise ValueError(f"invalid temperature covariate: {key}")
    if int(record["sequence_index"]) < 0 or int(record["capture_order"]) < 0:
        raise ValueError("chronology indices must be nonnegative")


def settle_from_cycles(
    cycles: Mapping[str, Mapping[int, Sequence[Mapping[str, float]]]],
    feature_ids: Sequence[str],
    *,
    compatibility_fn: Callable[[Sequence[float], Sequence[float]], bool] | None = None,
) -> dict[str, Any]:
    compatibility = compatibility_fn or (lambda left, right: bool(np.linalg.norm(np.asarray(left) - np.asarray(right)) <= 1e-9))
    normalized: dict[str, dict[int, np.ndarray]] = {}
    for cycle, rows in cycles.items():
        normalized[cycle] = {
            int(point): np.mean(np.vstack([ordered_unit_shape(row, feature_ids) for row in values]), axis=0)
            for point, values in rows.items()
        }
    for candidate in SELECTABLE_SETTLE_POINTS:
        candidate_centers = [rows[candidate] for rows in normalized.values() if candidate in rows]
        if len(candidate_centers) != len(normalized) or not _all_pairs(candidate_centers, compatibility):
            continue
        valid = True
        for rows in normalized.values():
            if any(not compatibility(rows[candidate], rows[later]) for later in TIMED_POINTS if later > candidate):
                valid = False
                break
        if valid:
            return {"status": "pass", "t_settle_s": candidate, "six_hundred_is_validation_only": True}
    return {"status": "settling_not_demonstrated_by_600", "t_settle_s": None, "six_hundred_is_validation_only": True}


def _all_pairs(values: Sequence[Sequence[float]], fn: Callable[[Sequence[float], Sequence[float]], bool]) -> bool:
    return all(fn(values[left], values[right]) for left in range(len(values)) for right in range(left + 1, len(values)))


def audit_chronology(rows: Sequence[Mapping[str, Any]]) -> None:
    if [int(row["sequence_index"]) for row in rows] != list(range(len(rows))):
        raise ValueError("thermal covariate sequence is missing, duplicated, or reordered")
    timestamps = [int(row["monotonic_timestamp_ns"]) for row in rows]
    if timestamps != sorted(timestamps) or len(timestamps) != len(set(timestamps)):
        raise ValueError("thermal covariate monotonic timestamps are not strictly increasing")


def summarize_group_audit(groups: Mapping[str, Sequence[Mapping[str, float]]], feature_ids: Sequence[str]) -> dict[str, Any]:
    summary = summarize_within_groups(groups, feature_ids)
    failures = summary["audit"]["failure_branches"]
    trend_failed = any(item.get("branch") == "trend" and float(item.get("score", 0)) > AUDIT_THRESHOLDS["trend_whitened_limit"] for item in failures)
    dominance_failed = any(item.get("branch") == "single_frame_dominance" for item in failures)
    return {"summary": summary, "trend_failed": trend_failed, "dominance_failed": dominance_failed}
