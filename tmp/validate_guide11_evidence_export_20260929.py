"""External validation of GUIDE11-COMPLETE-PROCESSED-EVIDENCE-20260929.zip.

Re-opens the built ZIP, verifies CRC, cross-checks every member against the
in-archive MANIFEST.json (path, byte count, SHA-256), asserts the key
accounting facts, and spot-decompresses one patch-statistics member. Writes
tmp/GUIDE11-EVIDENCE-EXPORT-VALIDATION-20260929.json as the versioned
validation record. Read-only with respect to the package.
"""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

REPO = Path("C:/Users/iBobb/Projects/WLED-RGBWW")
ZIP_PATH = REPO / ".agent-work/guide11/GUIDE11-COMPLETE-PROCESSED-EVIDENCE-20260929.zip"
OUT = REPO / "tmp/GUIDE11-EVIDENCE-EXPORT-VALIDATION-20260929.json"


def main() -> None:
    z = zipfile.ZipFile(ZIP_PATH)
    bad = z.testzip()
    prefix = "GUIDE11-COMPLETE-PROCESSED-EVIDENCE-20260929/"
    manifest = json.loads(z.read(prefix + "MANIFEST.json"))
    by_path = {m["path"]: m for m in manifest["files"]}

    members = [n for n in z.namelist() if not n.endswith("/")]
    expected_self_entry = {"MANIFEST.json"}  # present in zip, excluded from manifest by design
    missing_in_zip = sorted(set(by_path) - {n[len(prefix):] for n in members})
    extra_in_zip = sorted({n[len(prefix):] for n in members} - set(by_path) - expected_self_entry)
    hash_mismatch = []
    size_mismatch = []
    for m in manifest["files"]:
        rel = prefix + m["path"]
        info = z.getinfo(rel)
        if info.file_size != m["byte_count"]:
            size_mismatch.append(m["path"])
        h = hashlib.sha256(z.read(rel)).hexdigest()
        if h != m["sha256"]:
            hash_mismatch.append(m["path"])

    checks = json.loads(z.read(prefix + "replay/OFFLINE-CHECKS-20260929.json"))
    obs = [json.loads(l) for l in z.read(prefix + "OBSERVATIONS.jsonl").decode("utf-8").splitlines() if l.strip()]
    aliases = json.loads(z.read(prefix + "observation_aliases.json"))
    conf = json.loads(z.read(prefix + "replay/w2-adopted-commands-confirmation-status.json"))

    spot_rel = prefix + next(
        m["path"] for m in manifest["files"]
        if m["path"].startswith("runs/guide11-w2/formal-w2-20260922/measurements/")
    )
    spot = json.loads(z.read(spot_rel))
    spot_block06 = next(p for p in spot["patches"] if p.get("index") == 6)["planes"]["R"]["statistics"]["normalized_per_second"]["trimmed_mean"]

    record = {
        "schema": "guide11_evidence_export_validation_v1",
        "zip_path": str(ZIP_PATH),
        "zip_byte_count": ZIP_PATH.stat().st_size,
        "zip_sha256": hashlib.sha256(ZIP_PATH.read_bytes()).hexdigest(),
        "zip_crc_testzip": "ok" if bad is None else f"FAIL:{bad}",
        "manifest_file_count": manifest["file_count"],
        "zip_member_count": len(members),
        "manifest_members_missing_from_zip": missing_in_zip,
        "zip_members_missing_from_manifest": extra_in_zip,
        "size_mismatch_members": size_mismatch,
        "hash_mismatch_members": hash_mismatch,
        "assertions": {
            "manifest_matches_zip": not missing_in_zip and not extra_in_zip and not size_mismatch and not hash_mismatch,
            "observation_rows_equal_unique_raw": len(obs) == aliases["unique_raw_sha256_count"] == 472,
            "lut_matched_w2_commands_9": conf["adopted_count_matched_into_frozen_lut_by_command"] == 9,
            "all_w2_confirmations_not_acquired": all(
                c["independent_fast_confirmation"] == "not_acquired" for c in conf["commands"]),
            "c4_derived_present": any(m["path"] == "derived/guide11-c4/c4-holdout-analysis-20260928.json" for m in manifest["files"]),
            "frozen_lut_present": any(m["path"] == "frozen-inputs/frozen-lut-20260923.json" for m in manifest["files"]),
            "prior_machine_manifest_present": any(m["path"] == "frozen-inputs/prior-final-package/GUIDE11-FINAL-PACKAGE-MANIFEST-20260929.json" for m in manifest["files"]),
            "replay_zero_diff": all(v == 0.0 for v in checks["5_replay_one_white_one_color"]["white_abs_diffs"].values())
            and all(v == 0.0 for v in checks["5_replay_one_white_one_color"]["color_abs_diffs"].values()),
        },
        "spot_decompress": {
            "member": spot_rel[len(prefix):],
            "block06_R_trimmed_mean_per_second": spot_block06,
            "parsed_ok": isinstance(spot_block06, float),
        },
        "offline_checks_reference": "replay/OFFLINE-CHECKS-20260929.json inside the archive",
    }
    all_ok = all(record["assertions"].values()) and record["zip_crc_testzip"] == "ok"
    record["overall"] = "pass" if all_ok else "FAIL"
    OUT.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"overall": record["overall"], "assertions": record["assertions"],
                      "zip_sha256": record["zip_sha256"], "members": record["zip_member_count"]}, indent=1))


if __name__ == "__main__":
    main()
