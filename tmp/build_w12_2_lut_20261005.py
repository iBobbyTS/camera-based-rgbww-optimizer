"""GUIDE12 W12-2 frozen 70-node LUT assembly (offline, read-only inputs).

Merges the authoritative command owners into the single 70-node actual-PWM
LUT that W12-2 verifies (commands are frozen BEFORE verification):
1. GUIDE10 canonical LUT (baseline, 70 nodes with status);
2. GUIDE11 W2 selections (25 re-adopted nodes, 2026-09-23);
3. GUIDE12 W12-1 adopted commands (18 re-optimized nodes, 2026-10-02,
   parsed from the authoritative result document).

Per node: provenance chain, changed-since-W2 flag, verification class:
- "needs_two_pairs": command changed by W12-1 (or never independently
  confirmed) -> at least 2 new independent source pairs in W12-2
  (GUIDE: extra budget 4 frames per such node);
- "one_pair_plus_history": unchanged W2 command with existing valid
  confirmation -> 1 new pair (N2 shares pre-registered for 3200/0);
- 20000/0 keeps its W12-1 retest-candidate note (Ray-drift blocked
  certification at E=0.0748).

GM convention note (GUIDE W12-2): raw GM100 is neutral, not user GM+1;
the LUT stores raw gm exactly as the Ray API uses it.

Output: D:/rgbww-optimizer/guide12-w122/derived/w12-2-frozen-lut-20261005.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

GUIDE10 = Path(
    "D:/rgbww-optimizer/guide10/guide10-white70-w8-final/guide10-white70-final-artifact.json"
)
W2 = Path(
    "D:/rgbww-optimizer/guide11/guide11-w2/derived/w2-selection-20260923.json"
)
W12_RESULT = Path(".agent-work/guide12/GUIDE12-W12-RESULT-20260930.md")
OUT = Path(
    "D:/rgbww-optimizer/guide12-w122/derived/w12-2-frozen-lut-20261005.json"
)

CMD_KEYS = ("cw", "ww", "r", "g", "b")
CMD_RE = re.compile(
    r"\{\s*(?:([a-z]+):(\d+)\s*,?\s*)+\}"
)
NODE_RE = re.compile(r"^##\s+节点\s+(\d+)/(\d+)\s*—", re.MULTILINE)


def parse_w12_adopted() -> dict[tuple[int, int], dict[str, int]]:
    text = W12_RESULT.read_text(encoding="utf-8")
    adopted: dict[tuple[int, int], dict[str, int]] = {}
    for match in NODE_RE.finditer(text):
        cct, gm = int(match.group(1)), int(match.group(2))
        section = text[match.end():]
        nxt = NODE_RE.search(section)
        section = section[: nxt.start()] if nxt else section
        # adopted lines are marked 采用命令 (qualified nodes) or
        # 最优实测命令 (20000/0, reference/operating_limited retest
        # candidate); command key order varies (b-first on cold nodes)
        command = None
        for marker in ("采用命令", "最优实测命令"):
            pos = section.find(marker)
            if pos < 0:
                continue
            rest = section[pos:]
            m = re.search(r"\{([^{}]*)\}", rest)
            if m is None:
                continue
            channel = dict(
                (k, int(v)) for k, v in re.findall(r"([a-z]+):(\d+)", m.group(1))
            )
            if sorted(channel) == sorted(CMD_KEYS):
                command = {k: channel[k] for k in CMD_KEYS}
                break
        if command is None:
            raise ValueError(f"W12-1 node {cct}/{gm} has no adopted command")
        adopted[(cct, gm)] = command
    return adopted


def main() -> int:
    guide10 = json.loads(GUIDE10.read_text(encoding="utf-8"))["canonical_lut"]
    w2 = json.loads(W2.read_text(encoding="utf-8"))["nodes"]
    w12 = parse_w12_adopted()

    w2_by_node = {
        (int(n["cct"]), int(n["gm"])): n["selected"]["command"] for n in w2
    }
    nodes = []
    for entry in guide10:
        cct, gm = int(entry["cct"]), int(entry["gm"])
        key = (cct, gm)
        command = entry["command"]
        provenance = ["guide10_canonical"]
        changed_since_w2 = False
        if key in w2_by_node:
            command = w2_by_node[key]
            provenance.append("guide11_w2_selected")
        if key in w12:
            command = w12[key]
            provenance.append("guide12_w12_1_adopted")
            changed_since_w2 = key not in w2_by_node or w12[key] != w2_by_node[key]
        verification_class = (
            "needs_two_pairs" if changed_since_w2 else "one_pair_plus_history"
        )
        nodes.append({
            "cct": cct, "gm": gm, "command": command,
            "provenance": provenance,
            "changed_since_w2": changed_since_w2,
            "verification_class": verification_class,
            "guide10_status": entry.get("status"),
            "fullscale": max(command.values()) == 4095,
        })
    needs_two = [n for n in nodes if n["verification_class"] == "needs_two_pairs"]
    not_fullscale = [n for n in nodes if not n["fullscale"]]
    result = {
        "schema": "guide12_w12_2_frozen_lut_v1",
        "frozen_at": "2026-10-05",
        "gm_convention": "raw GM100 is neutral (not user GM+1); Ray API gm units",
        "node_count": len(nodes),
        "nodes": nodes,
        "summary": {
            "needs_two_pairs": len(needs_two),
            "one_pair_plus_history": len(nodes) - len(needs_two),
            "extra_frames_for_changed": 4 * len(needs_two),
            "not_actual_fullscale": [
                f"{n['cct']}/{n['gm']}" for n in not_fullscale
            ],
            "verification_frames_total": 2 * len(nodes) + 4 * len(needs_two),
            "special_notes": {
                "20000/0": "W12-1 retest candidate (E=0.0748, Ray-drift blocked)",
                "20000/100": (
                    "N2 measured stable -304K bias + second-scale strip drift; "
                    "one bounded correction only if queue budget and predicted "
                    "improvement allow, otherwise failure-region closure"
                ),
                "3200/0": "N2 six pairs pre-registered as independent shares",
            },
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"written: {OUT}")
    print("节点:", len(nodes), "| changed(needs_two_pairs):", len(needs_two),
          "| 验证帧总额:", result["summary"]["verification_frames_total"])
    print("非满幅命令:", result["summary"]["not_actual_fullscale"])
    print("changed 节点:", [f"{n['cct']}/{n['gm']}" for n in needs_two])
    return 0


if __name__ == "__main__":
    sys.exit(main())
