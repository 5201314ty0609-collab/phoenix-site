#!/usr/bin/env python3
"""
PHOENIX Analyze — Pattern Extraction Engine
Mines session transcripts for behavioral patterns:
- Successful patterns → framework candidates
- Failed patterns → shadow candidates
- Repeated patterns → echo signatures
"""

import json
import sys
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

PHOENIX_HOME = Path.home() / ".claude" / "phoenix"
PROJECTS_DIR = Path.home() / ".claude" / "projects" / "-Users-holyty"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    events = []
    for line in path.read_text().strip().split("\n"):
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def hash_text(text: str) -> str:
    return hashlib.md5(text.encode()[:200]).hexdigest()[:12]


def extract_tool_sequences(events: list[dict]) -> list[list[str]]:
    """Extract sequences of tool calls from events"""
    sequences = []
    current = []
    for e in events:
        tool = e.get("type", e.get("tool", ""))
        if tool:
            current.append(tool)
        elif current:
            if len(current) >= 2:
                sequences.append(current)
            current = []
    if len(current) >= 2:
        sequences.append(current)
    return sequences


def extract_error_patterns(events: list[dict]) -> list[dict]:
    """Extract error patterns with context"""
    patterns = []
    for i, e in enumerate(events):
        content = json.dumps(e)
        if any(kw in content.lower() for kw in ["error", "错误", "failed", "traceback"]):
            ctx_start = max(0, i - 2)
            ctx_end = min(len(events), i + 3)
            context = events[ctx_start:ctx_end]
            patterns.append({
                "error_hash": hash_text(content),
                "error_snippet": content[:300],
                "context_tools": [x.get("type", x.get("tool", "?")) for x in context if x.get("type")],
                "timestamp": e.get("timestamp", now_iso())
            })
    return patterns


def extract_success_patterns(events: list[dict]) -> list[dict]:
    """Extract successful patterns (tool sequences that ended with success)"""
    patterns = []
    for i, e in enumerate(events):
        content = json.dumps(e)
        if any(kw in content.lower() for kw in ["success", "✓", "completed", "done", "完成"]):
            ctx_start = max(0, i - 3)
            context = events[ctx_start:i+1]
            tools = [x.get("type", x.get("tool", "?")) for x in context if x.get("type")]
            if tools:
                patterns.append({
                    "pattern_hash": hash_text("→".join(tools)),
                    "tool_sequence": tools,
                    "success_indicator": e.get("type", "result"),
                    "timestamp": e.get("timestamp", now_iso())
                })
    return patterns


def extract_anti_patterns(events: list[dict]) -> list[dict]:
    """Identify anti-patterns from events"""
    anti_patterns = []
    tool_counter = Counter()

    for e in events:
        tool = e.get("type", e.get("tool", ""))
        tool_counter[tool] += 1

    total = sum(tool_counter.values())

    # Detect tool overuse
    for tool, count in tool_counter.most_common(3):
        if total > 10 and count / total > 0.7:
            anti_patterns.append({
                "type": "tool_overuse",
                "tool": tool,
                "ratio": count / total,
                "description": f"Over-reliance on '{tool}': {count}/{total} calls ({count/total*100:.0f}%)"
            })

    # Detect read-only loops (never writing)
    if "read_file" in tool_counter and tool_counter.get("write_file", 0) + tool_counter.get("edit_file", 0) == 0:
        if tool_counter.get("read_file", 0) > 10:
            anti_patterns.append({
                "type": "read_only_loop",
                "description": "Many reads but no writes — agent may be stuck reading without acting"
            })

    return anti_patterns


def propose_framework(pattern: dict, source: str) -> dict:
    """Create a framework proposal from an extracted pattern"""
    framework_id = pattern.get("pattern_hash", hash_text(json.dumps(pattern)))
    return {
        "id": f"fw-{framework_id}",
        "trigger": f"When executing: {' → '.join(pattern.get('tool_sequence', []))}",
        "action": pattern.get("success_indicator", pattern.get("description", "Detected pattern")),
        "confidence": 0.2,
        "stage": "active",
        "enforcement_level": 1,
        "observations": 1,
        "successes": 1 if source == "success" else 0,
        "failures": 0,
        "domains": ["auto-detected"],
        "evolved_from": [],
        "created_at": now_iso(),
        "promoted_at": {"active": now_iso(), "observed": None, "validated": None, "hardened": None},
        "amendments": []
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="PHOENIX Pattern Analyzer")
    parser.add_argument("--session-file", help="Path to a specific session transcript JSONL")
    parser.add_argument("--output-dir", help="Where to write framework proposals")
    parser.add_argument("--mode", choices=["full", "errors", "success", "antipatterns"], default="full")
    args = parser.parse_args()

    if args.session_file:
        events = load_jsonl(Path(args.session_file))
    else:
        jsonl_files = sorted(PROJECTS_DIR.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
        events = load_jsonl(jsonl_files[0]) if jsonl_files else []

    print(f"PHOENIX Analyze — {now_iso()}")
    print(f"Analyzing {len(events)} events\n")

    results = {}

    if args.mode in ("full", "errors"):
        error_patterns = extract_error_patterns(events)
        results["errors"] = error_patterns
        print(f"Error patterns found: {len(error_patterns)}")

    if args.mode in ("full", "success"):
        success_patterns = extract_success_patterns(events)
        results["success"] = success_patterns
        print(f"Success patterns found: {len(success_patterns)}")

    if args.mode in ("full", "antipatterns"):
        anti_patterns = extract_anti_patterns(events)
        results["antipatterns"] = anti_patterns
        print(f"Anti-patterns found: {len(anti_patterns)}")

    # Propose frameworks from success patterns
    proposals = []
    for sp in results.get("success", [])[:5]:
        proposals.append(propose_framework(sp, "success"))

    output_dir = Path(args.output_dir) if args.output_dir else PHOENIX_HOME / "frameworks" / "active"
    output_dir.mkdir(parents=True, exist_ok=True)

    for proposal in proposals:
        fname = f"{proposal['id']}.json"
        (output_dir / fname).write_text(json.dumps(proposal, indent=2, ensure_ascii=False))
        print(f"  → Proposed framework: {fname}")

    if not proposals:
        print("  No new framework proposals — insufficient data")

    print(f"\nAnalysis complete. {len(proposals)} frameworks proposed.")


if __name__ == "__main__":
    main()
