"""GUIDE12 evidence-completion offline validation (no devices, no D: paths).

Runs against two extracted package roots:
    python validate_completion_package.py <base_root> <completion_root>

Sections (Advisor request §7):
  1. manifest/member integrity of both packages
  2. stat correspondence + real-hash dedupe across base+completion
  3. adopted-colour identity traceability (confirmations vs selection)
  4. Ray-100% / strip-fullscale / pre-capture isolation trace checks
  5. W12-2 node recomputation (white points via packaged matrix + source)
  6. N2 white-state paired CI/PI recomputation
  7. W12-4 FAST/LONG difference-in-differences recomputation
  8. adopted-colour direct dz recomputation (base replay set)
  9. W12-3 / C12-4 runtime-model vs actually-executed commands
 10. batch-1 exposure qualification + all-off sensitivity recomputation

Writes validation-report.json next to this script and prints a summary.
Numeric disagreements with original results are reported as
replay_discrepancy entries; original results are never modified.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
import zipfile
from pathlib import Path

BASE = Path(sys.argv[1]).resolve()
COMP = Path(sys.argv[2]).resolve()
REPORT: dict = {"schema": "guide12_completion_validation_v1",
                "checks": {}, "replay_discrepancy": []}
FAILS: list[str] = []


def check(name: str, ok: bool, detail) -> bool:
    REPORT["checks"][name] = {"pass": bool(ok), "detail": detail}
    if not ok:
        FAILS.append(name)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return bool(ok)


def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines()
            if l.strip()]


# ---------------------------------------------------------------- 1. zips
def verify_package(root: Path, label: str) -> dict:
    man_p = root / "MANIFEST.json"
    man = json.loads(man_p.read_text(encoding="utf-8"))
    bad = []
    n = 0
    for f in man["files"]:
        p = root / f["path"]
        if not p.exists():
            bad.append(f["path"] + " missing")
            continue
        n += 1
        if p.stat().st_size != f["byte_count"]:
            bad.append(f["path"] + " size")
        elif sha_file(p) != f["sha256"]:
            bad.append(f["path"] + " sha")
    return {"manifest_members": len(man["files"]), "verified": n,
            "bad": bad[:10], "label": label}


pkg_base = verify_package(BASE, "base")
pkg_comp = verify_package(COMP, "completion")
check("manifest_integrity",
      not pkg_base["bad"] and not pkg_comp["bad"]
      and pkg_base["verified"] == pkg_base["manifest_members"]
      and pkg_comp["verified"] == pkg_comp["manifest_members"],
      {"base": pkg_base, "completion": pkg_comp})

# ------------------------------------------------- shared data + source import
sys.path.insert(0, str(COMP / "source" / "src"))
from camera_based_rgbww_optimizer.optimization import (  # noqa: E402
    white_calibration_common as wcc,
)

obs = jsonl(COMP / "OBSERVATIONS_COMPLETE.jsonl")
raw_index = jsonl(COMP / "RAW_INDEX_COMPLETE.jsonl")
matrix_of_frame: dict[tuple[str, str], str] = {}
for r in raw_index:
    mid = (r.get("offline_recheck") or {}).get("matrix_id")
    if mid:
        matrix_of_frame[(r["run_alias"], r["capture_id"])] = mid
matrices = {m.stem: json.loads(m.read_text(encoding="utf-8"))["matrix_3x3"]
            for m in (COMP / "matrices").glob("*.json")}

_by_key: dict[tuple[str, str], dict] = {}


def stats_of(run_alias: str, capture_id: str) -> Path:
    p = BASE / "measurements" / run_alias / f"{capture_id}.patch-statistics.json"
    if p.exists():
        return p
    return COMP / "measurements" / run_alias / f"{capture_id}.patch-statistics.json"


def planes_of(run_alias: str, capture_id: str) -> dict[str, float]:
    st = json.loads(stats_of(run_alias, capture_id).read_text(encoding="utf-8"))
    block = next(p for p in st["patches"] if p.get("index") == 6)
    return {pl: float(block["planes"][pl]["statistics"]
                      ["normalized_per_second"]["trimmed_mean"])
            for pl in ("R", "G1", "G2", "B")}


def white_point(run_alias: str, capture_id: str) -> dict[str, float]:
    pl = planes_of(run_alias, capture_id)
    g = 0.5 * (pl["G1"] + pl["G2"])
    est = wcc.estimate_white_point_from_camera_neutral(
        [pl["R"] / g, 1.0, pl["B"] / g],
        matrices[matrix_of_frame[(run_alias, capture_id)]])
    return {"cct_K": float(est["cct_K"]), "duv": float(est["duv"]),
            "mired": 1e6 / float(est["cct_K"])}


def z_of(run_alias: str, capture_id: str) -> tuple[float, float]:
    pl = planes_of(run_alias, capture_id)
    g = 0.5 * (pl["G1"] + pl["G2"])
    return (math.log(pl["R"] / g), math.log(pl["B"] / g))


# --------------------------------------------- 2. stats correspondence + dedupe
comp_man = json.loads((COMP / "MANIFEST.json").read_text(encoding="utf-8"))
comp_members = {f["path"]: f["sha256"] for f in comp_man["files"]}
base_man = json.loads((BASE / "MANIFEST.json").read_text(encoding="utf-8"))
base_members = {f["path"]: f["sha256"] for f in base_man["files"]}
n_base_stats = sum(1 for p in base_members if p.startswith("measurements/"))
n_comp_stats = sum(1 for p in comp_members if p.startswith("measurements/"))
raw_rows_with_stats = sum(1 for r in raw_index
                          if (r.get("stats_source") or {}).get("sha256"))
uniq_stats_sha = {(r.get("stats_source") or {}).get("sha256")
                  for r in raw_index if (r.get("stats_source") or {}).get("sha256")}
phys_rows = sum(1 for r in raw_index if not r.get("diagnostic_payload"))
diag_rows = sum(1 for r in raw_index if r.get("diagnostic_payload"))
unreadable = [r["capture_id"] for r in raw_index
              if (r.get("offline_recheck") or {}).get("readable") is not True]
hash_chain_ok = all(
    (r["acquisition"]["cr3_sha256"]
     == r["offline_recheck"]["recomputed_sha256"]
     == r["stats_source"]["sha256"])
    for r in raw_index
    if not r.get("diagnostic_payload") and r.get("stats_source", {}).get("sha256")
)
check("stats_correspondence_and_dedupe",
      n_base_stats == 1051 and n_comp_stats == 17 and unreadable == []
      and hash_chain_ok,
      {"base_stats_members": n_base_stats,
       "completion_stats_members": n_comp_stats,
       "raw_rows": len(raw_index), "physical_rows": phys_rows,
       "diagnostic_rows": diag_rows, "raw_with_stats": raw_rows_with_stats,
       "unique_recorded_stats_sha": len(uniq_stats_sha),
       "unreadable_raw": unreadable,
       "acquisition==recompute==stats_source for all physical rows":
           hash_chain_ok})

# ------------------------------------- 3. adopted colour identity traceability
adopted_table = json.loads(
    (BASE / "models/strip-hsi-command-model.json").read_text(
        encoding="utf-8"))["adopted"]
identity = {}
for label, cmd in adopted_table.items():
    key = json.dumps(cmd, sort_keys=True)
    frames = [o for o in obs
              if json.dumps((o.get("plan_step") or {}).get("command"),
                            sort_keys=True) == key]
    runs = sorted({o["run_alias"] for o in frames})
    identity[label] = {
        "command": cmd,
        "frames": len(frames),
        "distinct_runs": len(runs),
        "runs": runs,
        "tags": sorted({(o.get("plan_step") or {}).get("c122_tag")
                        for o in frames} - {None}),
        "roles": sorted({(o.get("plan_step") or {}).get("candidate_role")
                         for o in frames} - {None}),
        "max_channel_at_fullscale": max(cmd.values()) == 4095,
    }
check("adopted_colour_traceability",
      len(identity) >= 6 and all(v["frames"] >= 1 for v in identity.values()),
      {"adopted_entries": len(identity), "identity": identity})

# ---------------------------- 4. Ray-100% / fullscale / isolation trace checks
ray_viol = []
for o in obs:
    ps = o.get("plan_step") or {}
    if not ps or o.get("ledger") != "captures.jsonl":
        continue
    if str(ps.get("source_id")) == "ray" and ps.get("capture_role") == "formal":
        inten = (ps.get("command") or {}).get("intensity_percent")
        if inten is not None and float(inten) != 100.0:
            ray_viol.append((o["run_alias"], o["capture_id"], inten))
strip_rows = [o for o in obs
              if (o.get("plan_step") or {}).get("source_id") == "strip"
              and o.get("ledger") == "captures.jsonl"]
fullscale_ok = sum(
    1 for o in strip_rows
    if max((o["plan_step"].get("command") or {}).values()) >= 4095)
iso_missing = sum(
    1 for o in strip_rows
    if (o.get("capture") or {}).get("ray_zero_before_capture") is None)
iso_ray_missing = sum(
    1 for o in obs
    if (o.get("plan_step") or {}).get("source_id") == "ray"
    and o.get("ledger") == "captures.jsonl"
    and (o.get("capture") or {}).get("strip_zero_before_capture") is None)
check("reference_and_isolation_trace",
      not ray_viol and iso_missing == 0 and iso_ray_missing == 0,
      {"formal_ray_frames_not_100pct": ray_viol[:5],
       "ray_frames_total": sum(
           1 for o in obs
           if (o.get("plan_step") or {}).get("source_id") == "ray"
           and o.get("ledger") == "captures.jsonl"),
       "strip_frames": len(strip_rows),
       "strip_frames_with_fullscale_channel": fullscale_ok,
       "strip_frames_missing_ray_zero_flag": iso_missing,
       "ray_frames_missing_strip_zero_flag": iso_ray_missing})

# ------------------------------------------------ 5. W12-2 node recomputation
w122 = json.loads((BASE / "results/w12-2-verification-analysis.json")
                  .read_text(encoding="utf-8"))
TOL = w122["tolerances"]
target_node = "3200/100"
recomputed = []
max_dev = 0.0
for pair in w122["node_pairs"]:
    if pair["node"] != target_node:
        continue
    strip = pair["steps"].get("strip")
    if not strip or not strip.get("white_point"):
        continue
    ray_refs = [pair["steps"][k] for k in ("ray", "raybefore", "rayafter")
                if pair["steps"].get(k, {}).get("white_point")]
    if not ray_refs:
        continue
    wp = white_point(f"guide12-w122/{strip['run']}", strip["capture_id"])
    ref = {c: sum(white_point(f"guide12-w122/{r['run']}", r["capture_id"])[c]
                 for r in ray_refs) / len(ray_refs)
           for c in ("cct_K", "duv", "mired")}
    signed = {c: wp[c] - ref[c] for c in ref}
    e = max(abs(signed["cct_K"]) / TOL["cct_K"],
            abs(signed["mired"]) / TOL["mired"],
            abs(signed["duv"]) / TOL["duv"])
    dev = max(abs(wp[c] - strip["white_point"][c]) for c in ref)
    dev = max(dev, max(abs(ref[c] - pair["reference_white_point"][c])
                       for c in ref))
    max_dev = max(max_dev, dev)
    recomputed.append({"repeat": pair["repeat"],
                       "E_original": pair.get("E_normalized"),
                       "E_recomputed": e,
                       "signed_original": pair.get("signed_errors"),
                       "signed_recomputed": signed})
ok_w122 = all(abs(r["E_original"] - r["E_recomputed"]) < 1e-3
              for r in recomputed if r["E_original"] is not None)
check("w12_2_node_recompute", bool(recomputed) and ok_w122,
      {"node": target_node, "pairs": recomputed,
       "max_white_point_deviation_vs_original": max_dev})

# ------------------------------------------------- 6. N2 CI/PI recomputation
n2 = json.loads((BASE / "results/n2-repeatability-analysis-20261005.json")
                .read_text(encoding="utf-8"))
BONF_T = {0.9833: {2: 9.925}, 0.95: {2: 4.303, 5: 2.571}}
state = "white_1800_100"
n2_obs = [o for o in obs
          if o["run_alias"].startswith("guide12-n2/")
          and (o.get("plan_step") or {}).get("n2_state_key") == state
          and o.get("ledger") == "captures.jsonl"]
N2_SESSION_RUNS = {1: "guide12-n2/formal-n2-session1-r5",
                   2: "guide12-n2/formal-n2-session2-r2",
                   3: "guide12-n2/formal-n2-session3"}
d_rows = []
for s in (1, 2, 3):
    run_alias = N2_SESSION_RUNS[s]
    for c in (1, 2):
        ray = next((o for o in n2_obs
                    if o["run_alias"] == run_alias
                    and o["plan_step"].get("n2_cycle_index") == c
                    and o["plan_step"].get("source_id") == "ray"), None)
        strip = next((o for o in n2_obs
                      if o["run_alias"] == run_alias
                      and o["plan_step"].get("n2_cycle_index") == c
                      and o["plan_step"].get("source_id") == "strip"), None)
        if ray and strip:
            wr = white_point(ray["run_alias"], str(ray["capture_id"]))
            ws = white_point(strip["run_alias"], str(strip["capture_id"]))
            d_rows.append({c2: ws[c2] - wr[c2]
                           for c2 in ("cct_K", "duv", "mired")})
orig_d = [r["d"] for r in n2["white_states"][state]["paired_differences"]]
dev_d = max(abs(d_rows[i][c] - orig_d[i][c])
            for i in range(len(d_rows)) for c in d_rows[i])
comp_stats = n2["white_states"][state]["component_statistics"]
n2_ok = len(d_rows) == len(orig_d) and dev_d < 1e-6
for c in ("cct_K", "duv", "mired"):
    ci = comp_stats[c]["ci_mean_session_unit"]
    sess_means = [(d_rows[2 * s][c] + d_rows[2 * s + 1][c]) / 2
                  for s in (0, 1, 2)]
    mean = sum(sess_means) / 3
    half = BONF_T[0.95][2] * (sum((m - mean) ** 2 for m in sess_means) / 2) ** 0.5 / math.sqrt(3)
    n2_ok = n2_ok and abs(mean - ci["mean"]) < 1e-6 and abs(half - ci["half_width"]) < 1e-6
check("n2_pairing_ci_recompute", n2_ok,
      {"state": state, "paired_rows": len(d_rows),
       "max_paired_difference_deviation": dev_d,
       "original_ci_cct": comp_stats["cct_K"]["ci_mean_session_unit"]})

# ---------------------------------------------- 7. W12-4 DiD recomputation
w124 = json.loads((BASE / "results/w12-4-order-reverification-analysis-20261009.json")
                  .read_text(encoding="utf-8"))
runs_w124 = [("3200/100", "long", "formal-w124-01-p3200100-long"),
             ("3200/100", "fast", "formal-w124-05-p3200100-fast")]
wps = {}
for point, proto, run in runs_w124:
    rows = [o for o in obs if o["run_alias"] == f"guide12-w124/{run}"]
    wps[proto] = {src: white_point(f"guide12-w124/{run}",
                                   str(next(o["capture_id"] for o in rows
                                            if (o["plan_step"] or {}).get("source_id") == src)))
                  for src in ("ray", "strip")}
did = {c: (wps["long"]["strip"][c] - wps["long"]["ray"][c])
       - (wps["fast"]["strip"][c] - wps["fast"]["ray"][c])
       for c in ("cct_K", "duv", "mired")}
orig = next(r for r in w124["points"] if r["point"] == "3200/100")
dev_did = max(abs(did[c] - orig["Delta_protocol"][c]) for c in did)
check("w12_4_did_recompute", dev_did < 1e-6,
      {"point": "3200/100", "recomputed_Delta_protocol": did,
       "original": orig["Delta_protocol"], "max_deviation": dev_did})

# --------------------------------------- 8. adopted colour dz recomputation
expected = json.loads((BASE / "replay/expected-results.json")
                      .read_text(encoding="utf-8"))["adopted_samples"]
by_cmd: dict[str, list[dict]] = {}
for o in obs:
    ps = o.get("plan_step") or {}
    if (ps.get("source_id") == "strip" and o.get("ledger") == "captures.jsonl"
            and ((o.get("capture") or {}).get("direct_quality") or {})
            .get("status") == "pass"):
        by_cmd.setdefault(json.dumps(ps.get("command"), sort_keys=True),
                          []).append(o)
dz_fail = []
colour_detail = {}
for name, spec in expected.items():
    key = json.dumps(spec["command"], sort_keys=True)
    rows = by_cmd.get(key, [])
    dzs = []
    for o in rows:
        rays = [z for zz in obs
                if zz["run_alias"] == o["run_alias"]
                and (zz.get("plan_step") or {}).get("source_id") == "ray"
                and zz.get("ledger") == "captures.jsonl"
                and ((zz.get("capture") or {}).get("direct_quality") or {})
                .get("status") == "pass"
                for z in [z_of(zz["run_alias"], str(zz["capture_id"]))]]
        if not rays:
            continue
        ref = [sum(z[i] for z in rays) / len(rays) for i in (0, 1)]
        z = z_of(o["run_alias"], str(o["capture_id"]))
        dzs.append((z[0] - ref[0], z[1] - ref[1]))
    mean = [sum(d[i] for d in dzs) / len(dzs) for i in (0, 1)] if dzs else None
    ok = mean is not None and all(
        abs(mean[i] - spec["mean_dz"][i]) <= spec["tol"][i] for i in (0, 1))
    colour_detail[name] = {"n": len(dzs), "mean_dz": mean,
                           "expected": spec["mean_dz"]}
    if not ok or len(dzs) < 3:
        dz_fail.append(name)
check("adopted_colour_dz_recompute", not dz_fail, colour_detail)

# ------------------------- 9. runtime-model outputs vs executed commands
from camera_based_rgbww_optimizer.optimization import guide12_w123  # noqa: E402
from camera_based_rgbww_optimizer.optimization import guide12_c124  # noqa: E402

lut = json.loads((BASE / "models/white-final-lut.json")
                 .read_text(encoding="utf-8"))
rt = json.loads((BASE / "models/white-runtime-model.json")
                .read_text(encoding="utf-8"))
vec_fail = []
for cct_gm, vec in rt["test_vectors"].items():
    cct, gm = (int(x) for x in cct_gm.split("/"))
    want = guide12_w123.interpolate_fullscale_command(lut["nodes"], cct, gm)
    want_cmd = want["command"] if isinstance(want, dict) and "command" in want else want
    got_cmd = vec["command"] if isinstance(vec, dict) and "command" in vec else vec
    if json.dumps(want_cmd, sort_keys=True) != json.dumps(got_cmd, sort_keys=True):
        vec_fail.append(cct_gm)
w123_runs = {o["run_alias"] for o in obs
             if o["run_alias"].startswith("guide12-w123/")}
w123_cmds = {json.dumps((o.get("plan_step") or {}).get("command"), sort_keys=True)
             for o in obs
             if o["run_alias"].startswith("guide12-w123/")
             and (o.get("plan_step") or {}).get("source_id") == "strip"}
c124_holdout_cmds = set()
for hue, sat in guide12_c124.C124_HOLDOUTS:
    out = guide12_c124.c124_model_command(hue, sat)
    c124_holdout_cmds.add(json.dumps(out["command"], sort_keys=True))
c124_exec = {json.dumps((o.get("plan_step") or {}).get("command"), sort_keys=True)
             for o in obs
             if o["run_alias"].startswith("guide12-c124/")
             and (o.get("plan_step") or {}).get("source_id") == "strip"}
adopted_exec = {json.dumps(cmd, sort_keys=True) for cmd in adopted_table.values()}
adopted_observed = adopted_exec & {
    json.dumps((o.get("plan_step") or {}).get("command"), sort_keys=True)
    for o in obs
    if (o.get("plan_step") or {}).get("source_id") == "strip"}
check("runtime_model_vs_executed_commands",
      not vec_fail and c124_holdout_cmds <= c124_exec,
      {"w123_vector_mismatches": vec_fail,
       "w123_runs": len(w123_runs),
       "w123_distinct_strip_cmds": len(w123_cmds),
       "c124_holdout_cmds_all_executed": c124_holdout_cmds <= c124_exec,
       "c124_exec_cmds": len(c124_exec),
       "adopted_commands_observed_in_runs": f"{len(adopted_observed)}/{len(adopted_exec)}"})

# --------------------------------------- 10. batch-1 recomputation
b1_root = COMP / "runs/guide12-batch1/formal-b1-20260929-r1"
b1_spec = json.loads((b1_root / "experiment-spec.json").read_text(encoding="utf-8"))
b1_cap = jsonl(b1_root / "captures.jsonl")
b1_qual_orig = json.loads(
    next((COMP / "results/original/guide12-batch1-derived")
         .glob("b1-exposure-qualification-*.json")).read_text(encoding="utf-8"))


def b1_frame(run_alias: str, cid: str) -> dict:
    st = json.loads(stats_of(run_alias, cid).read_text(encoding="utf-8"))
    block = next(p for p in st["patches"] if p.get("index") == 6)
    planes = {}
    for pl, blk in block["planes"].items():
        planes[pl] = {
            "q": blk["quality"]["status"],
            "nps": blk["statistics"]["normalized_per_second"]["trimmed_mean"],
            "p99": blk["statistics"]["raw_code"].get("percentile_99"),
            "white": float(blk["cfa"]["effective_white_level"]),
            "rail": blk["metrics"].get("white_rail_plateau"),
            "nrf": blk["metrics"].get("near_white_rail_fraction"),
        }
    return planes


def b1_z(pl: dict) -> tuple[float, float]:
    g = 0.5 * (pl["G1"]["nps"] + pl["G2"]["nps"])
    return (math.log(pl["R"]["nps"] / g), math.log(pl["B"]["nps"] / g))


followups = [("guide12-batch1/formal-b1-white-reverse-20260930-r1",
              jsonl(COMP / "runs/guide12-batch1/formal-b1-white-reverse-20260930-r1/captures.jsonl")),
             ("guide12-batch1/formal-b1-white-corrected-20260930-r1",
              jsonl(COMP / "runs/guide12-batch1/formal-b1-white-corrected-20260930-r1/captures.jsonl"))]
klass_frames: dict[str, list[tuple[str, str]]] = {}
for o in b1_cap:
    lc = (o.get("plan_step") or {}).get("ladder_class")
    if lc:
        klass_frames.setdefault(lc, []).append(
            ("guide12-batch1/formal-b1-20260929-r1", str(o["capture_id"])))
for alias, rows in followups:
    for o in rows:
        lc = (o.get("plan_step") or {}).get("ladder_class")
        if lc:
            klass_frames.setdefault(lc, []).append((alias, str(o["capture_id"])))
b1_result = {}
for klass in b1_spec["analysis_contract"]["classes"]:
    frames = klass_frames.get(klass["label"], [])
    stops = []
    for alias, cid in frames:
        pl = b1_frame(alias, cid)
        valid = all(v["q"] == "accepted" for v in pl.values()) and not any(
            v["rail"] or (v["nrf"] or 0) > 0.05 for v in pl.values())
        stops.append({"cid": cid, "valid": valid, "z": b1_z(pl)})
    # faithful copy of the frozen analyzer: adjacent-stop dz consistency,
    # then the fastest valid stop with a consistent neighbour wins
    pair_ok: dict[int, bool] = {}
    for i in range(len(stops) - 1):
        dz = max(abs(stops[i + 1]["z"][j] - stops[i]["z"][j]) for j in (0, 1))
        pair_ok[i] = dz <= 0.01
    selected = None
    for i, s in enumerate(stops):
        if not s["valid"]:
            continue
        if pair_ok.get(i - 1, False) or pair_ok.get(i, False):
            selected = s["cid"]
            break
    orig_sel = next((k["selected_capture_id"] for k in b1_qual_orig["classes"]
                     if k["label"] == klass["label"]), None)
    b1_result[klass["label"]] = {"selected": selected,
                                 "original_selected": orig_sel}
# all-off sensitivity: 1/8 start frame vs corrected white on-frame
alloff = next((o for o in b1_cap
               if (o.get("plan_step") or {}).get("ambient_position") == "start"
               and (o.get("plan_step") or {}).get("ambient_shutter_speed") == "1/8"),
              None)
on_cid = next((k["selected_capture_id"] for k in b1_qual_orig["classes"]
               if k["label"] == "high_white_load"), None)
on_alias = "guide12-batch1/formal-b1-white-corrected-20260930-r1"
env_ok = None
if alloff and on_cid:
    a = b1_frame("guide12-batch1/formal-b1-20260929-r1", str(alloff["capture_id"]))
    on = b1_frame(on_alias, on_cid)
    A_on = {pl: a[pl]["nps"] / on[pl]["nps"] for pl in a}
    env_ok = {"A_over_on": A_on}
    orig_env = next((e for e in b1_qual_orig["all_off"] if e["shutter"] == "1/8"), {})
    orig_ratios = (orig_env or {}).get("A_over_on_ratio")
    ratio_dev = max(abs(A_on[pl] - orig_ratios[pl]) for pl in A_on) if orig_ratios else None
    env_ok["max_ratio_dev_vs_original"] = ratio_dev
b1_ok = all(v["selected"] == v["original_selected"] for v in b1_result.values())
check("batch1_exposure_and_ambient_recompute", b1_ok,
      {"classes": b1_result, "ambient_1over8": env_ok})

# ------------------------------------------------------------------ report
REPORT["overall"] = "PASS" if not FAILS else f"FAIL: {FAILS}"
out = Path(__file__).resolve().parent / "validation-report.json"
out.write_text(json.dumps(REPORT, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"\nOVERALL: {REPORT['overall']}")
print(f"written: {out}")
sys.exit(0 if not FAILS else 1)
