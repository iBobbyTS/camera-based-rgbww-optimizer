"""D4 (GUIDE13 evidence completion 20261020): source version binding.

Offline provenance binding for the code actually used by the 88 GUIDE13
capture runs:
- read each run's input-checkpoint.json git binding (commit, dirty),
- resolve the transitive local import closure of the GUIDE13 owners/runners
  recorded in the original package source/ members,
- for every (run commit, module) pair compute the exact file bytes at that
  commit (git show), and bind them to: current worktree, original GUIDE13
  package member, or a base-package member (exact zip + member path + sha),
- emit DEPENDENCY_STATUS.json with per-module verdicts and copy any version
  that exists in none of the packages into the increment's source/ tree.

Dirty-at-launch runs keep their recorded dirty flag; unrecoverable versions
are recorded as such, never guessed.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
D = Path("D:/rgbww-optimizer")
WORK = D / "guide13" / "completion-20261020"
IDENTITY = "reanalysis/export (GUIDE13 evidence completion 20261020)"
SRC = "src/camera_based_rgbww_optimizer"
PKG13 = D / "guide13/package/GUIDE13-COMPLETE-PROCESSED-EVIDENCE-20261019.zip"
BASE_COMPLETE = REPO / ".agent-work/guide12/GUIDE12-COMPLETE-PROCESSED-EVIDENCE-20261012.zip"
BASE_COMPLETION = REPO / ".agent-work/guide12/GUIDE12-EVIDENCE-COMPLETION-20261012.zip"
ROOT_FILES = [
    "src/camera_based_rgbww_optimizer/optimization/guide12.py",
    "src/camera_based_rgbww_optimizer/optimization/guide12_c122.py",
    "src/camera_based_rgbww_optimizer/optimization/guide12_w123.py",
    "src/camera_based_rgbww_optimizer/optimization/guide12_w124.py",
    "src/camera_based_rgbww_optimizer/optimization/guide12_n2.py",
    "src/camera_based_rgbww_optimizer/optimization/white_calibration_common.py",
    "src/camera_based_rgbww_optimizer/optimization/bounded_least_squares.py",
    "src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py",
    "src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py",
    "src/camera_based_rgbww_optimizer/optimization/guide12_c124.py",
    "src/camera_based_rgbww_optimizer/optimization/measure_guide12_w12.py",
    "src/camera_based_rgbww_optimizer/optimization/measure_guide12_w123.py",
    "src/camera_based_rgbww_optimizer/optimization/measure_guide12_c122.py",
    "src/camera_based_rgbww_optimizer/paths.py",
    "src/camera_based_rgbww_optimizer/control/camera_remote.py",
    "src/camera_based_rgbww_optimizer/control/esphome_rgbww_strip.py",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_show_bytes(commit: str, rel: str) -> bytes | None:
    proc = subprocess.run(
        ["git", "-C", str(REPO), "show", f"{commit}:{rel}"],
        capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def zip_index(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            if not info.is_dir():
                out[info.filename] = sha256_bytes(zf.read(info.filename))
    return out


def import_closure(entry_files: list[Path]) -> list[str]:
    """Transitive local import closure relative to repo root (posix rel paths)."""
    seen: set[str] = set()
    queue: list[Path] = list(entry_files)
    pkg_re = re.compile(r"(?:from|import)\s+(camera_based_rgbww_optimizer[\w.]*)")
    while queue:
        f = queue.pop()
        rel = f.relative_to(REPO).as_posix()
        if rel in seen or not f.exists():
            continue
        seen.add(rel)
        try:
            text = f.read_text(encoding="utf-8")
        except OSError:
            continue
        for mod in pkg_re.findall(text):
            base = mod.replace(".", "/")
            for cand in (Path(SRC).parent / (base + ".py"),
                         Path(SRC).parent / base / "__init__.py"):
                if (REPO / cand).exists():
                    queue.append(REPO / cand)
    return sorted(seen)


def main() -> int:
    run_index = json.loads(
        (WORK / "RUN_INDEX_COMPLETE.json").read_text(encoding="utf-8"))
    # 1. git bindings per run
    commit_runs: dict[str, list[str]] = defaultdict(list)
    dirty_runs: list[str] = []
    for r in run_index:
        if r["class"] == "plan_dry" or not r["git_commit_at_launch"]:
            continue
        key = f"{r['campaign']}/{r['run']}"
        commit_runs[r["git_commit_at_launch"]].append(key)
    print("distinct run commits:", len(commit_runs))
    for c, runs in sorted(commit_runs.items()):
        print("  ", c[:12], len(runs), "runs")

    # 2. module universe: advisor-named dependencies + import closure of the
    #    GUIDE13 owner/runner modules shipped in the original package
    pkg13 = zip_index(PKG13)
    entry_files = [REPO / n[len("source/"):] for n in pkg13
                   if n.startswith("source/src/") and n.endswith(".py")]
    closure = import_closure(entry_files)
    print("import closure size:", len(closure))
    modules = sorted({*ROOT_FILES, *closure})

    base_c = zip_index(BASE_COMPLETE)
    base_k = zip_index(BASE_COMPLETION)

    def bind(sha: str) -> dict:
        hits = []
        for member, msha in pkg13.items():
            if msha == sha:
                hits.append({"package": "GUIDE13-COMPLETE-PROCESSED-EVIDENCE-20261019.zip",
                             "member": member,
                             "zip_sha256": "919ef2ad47dd1b919190526fefc4fb570a7e743c13b9672684ba885e49fe3ab3"})
        for member, msha in base_c.items():
            if msha == sha:
                hits.append({"package": "GUIDE12-COMPLETE-PROCESSED-EVIDENCE-20261012.zip",
                             "member": member,
                             "zip_sha256": "3ed20b169cb2cc60470702a05c0e0bfb96f38aa24010b7948e664d271f53d500"})
        for member, msha in base_k.items():
            if msha == sha:
                hits.append({"package": "GUIDE12-EVIDENCE-COMPLETION-20261012.zip",
                             "member": member,
                             "zip_sha256": "85a61c4ee3a46c28f5922804dcd3f69590c82069477f1f9ad8924627cb52b4bc"})
        return hits

    # 3. per-module version binding
    status: dict[str, dict] = {}
    copy_out: list[tuple[str, bytes]] = []
    for rel in modules:
        cur = REPO / rel
        cur_sha = sha256_bytes(cur.read_bytes()) if cur.exists() else None
        per_commit: dict[str, dict] = {}
        version_shas: set[str] = set()
        for commit in commit_runs:
            data = git_show_bytes(commit, rel)
            if data is None:
                per_commit[commit[:12]] = {"status": "not_in_commit"}
                continue
            sha = sha256_bytes(data)
            version_shas.add(sha)
            per_commit[commit[:12]] = {
                "sha256": sha,
                "identical_to_current_worktree": sha == cur_sha,
                "byte_identical_members": bind(sha)[:4],
            }
        entry = {
            "current_worktree_sha256": cur_sha,
            "used_by_run_commits": per_commit,
            "single_version_across_all_runs": len(version_shas) <= 1,
        }
        # copy versions absent from every package into the increment
        for sha in sorted(version_shas):
            if not bind(sha):
                data = None
                for commit in commit_runs:
                    data = git_show_bytes(commit, rel)
                    if data is not None and sha256_bytes(data) == sha:
                        break
                if data is not None:
                    arc = f"source/{rel}"
                    copy_out.append((arc, data))
                    entry.setdefault("versions_added_to_increment", []).append(sha)
        status[rel] = entry

    # 4. dirty-launch truth
    for r in run_index:
        if r["class"] == "plan_dry":
            continue
        ckpt = D / r["campaign"] / r["run"] / "input-checkpoint.json"
        g = json.loads(ckpt.read_text(encoding="utf-8")).get("git", {})
        if g.get("dirty"):
            dirty_runs.append(f"{r['campaign']}/{r['run']}: {g.get('commit','')[:12]} "
                              f"dirty_entries={g.get('dirty_entries')}")

    out = {
        "schema": "guide13_completion_dependency_status_v1",
        "identity": IDENTITY,
        "run_commit_bindings": {
            c: {"runs": runs} for c, runs in sorted(commit_runs.items())},
        "dirty_at_launch": dirty_runs,
        "module_binding_basis": (
            "module set = advisor-named direct dependencies plus the transitive "
            "local import closure of the GUIDE13 owner/runner files shipped in "
            "the original package source/; per-commit bytes resolved with "
            "'git show <commit>:<path>'; binding compares exact sha256 against "
            "current worktree, the original GUIDE13 package and both GUIDE12 "
            "base packages"),
        "modules": status,
    }
    (WORK / "DEPENDENCY_STATUS.json").write_text(
        json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    for arc, data in copy_out:
        dst = WORK / arc
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
    single = sum(1 for v in status.values() if v["single_version_across_all_runs"])
    print(f"modules bound: {len(status)}, single-version across runs: {single}, "
          f"versions copied to increment: {len(copy_out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
