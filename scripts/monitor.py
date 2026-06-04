#!/usr/bin/env python3
"""
PHOENIX Monitor — 7-Sense Metacognitive Tracking Engine
Lightweight post-tool-call monitoring. Reads session data, updates sense state files.
"""

import json
import os
import sys
import time
import hashlib
import re
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from typing import Optional

PHOENIX_HOME = Path.home() / ".claude" / "phoenix"
SENSES_DIR = PHOENIX_HOME / "senses"
PROJECTS_DIR = Path.home() / ".claude" / "projects" / "-Users-holyty"

O2_WARN_PCT, O2_CRIT_PCT = 70, 85
NOCI_WARN_ERRORS, NOCI_WINDOW = 3, 5
ECHO_REPEAT_THRESHOLD = 3
SPATIAL_FILES_PER_CALL_WARN = 5
VESTIBULAR_IMBALANCE_PCT = 80
DRIFT_WARN_PCT = 30
CHRONOS_IDLE_SEC = 300


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict:
    try:
        if path.exists():
            return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        pass
    return {}


def save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def hash_text(text: str) -> str:
    return hashlib.md5(text.encode()[:200]).hexdigest()[:12]


def get_latest_transcript() -> Optional[Path]:
    if not PROJECTS_DIR.exists():
        return None
    jsonl_files = sorted(PROJECTS_DIR.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    return jsonl_files[0] if jsonl_files else None


def sample_recent_activity(transcript_path: Path, n: int = 30) -> list[dict]:
    try:
        lines = transcript_path.read_text().strip().split("\n")
        recent = lines[-n:] if len(lines) > n else lines
        events = []
        for line in recent:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return events
    except (OSError, IOError):
        return []


def check_o2(events: list[dict], state: dict) -> dict:
    total_chars = sum(len(json.dumps(e)) for e in events)
    est_tokens = total_chars // 3
    context_limit = state.get("context_limit", 128000)
    usage_pct = (est_tokens / context_limit * 100) if context_limit > 0 else 0

    status = "normal"
    warnings = []
    if usage_pct > O2_CRIT_PCT:
        status = "critical"
        warnings.append(f"Context at {usage_pct:.0f}% — CRITICAL. Force compaction now.")
    elif usage_pct > O2_WARN_PCT:
        status = "warning"
        warnings.append(f"Context at {usage_pct:.0f}% — consider /compact")

    return {
        "status": status, "last_updated": now_iso(),
        "metrics": {"estimated_tokens": est_tokens, "context_limit": context_limit,
                     "usage_percent": round(usage_pct, 1), "message_count": len(events)},
        "warnings": warnings,
        "recommendation": "/compact" if usage_pct > O2_WARN_PCT else "continue"
    }


def check_nociception(events: list[dict], state: dict) -> dict:
    recent_errors, error_hashes = [], []
    for e in events[-NOCI_WINDOW:]:
        content = json.dumps(e)
        if any(kw in content.lower() for kw in ["error", "错误", "failed", "traceback", "exit code: 1"]):
            recent_errors.append(e)
            error_hashes.append(hash_text(content))

    status, warnings = "normal", []
    if len(recent_errors) >= NOCI_WARN_ERRORS:
        status = "warning"
        warnings.append(f"{len(recent_errors)} errors in last {NOCI_WINDOW} calls")
    hash_counts = Counter(error_hashes)
    for h, count in hash_counts.items():
        if count >= ECHO_REPEAT_THRESHOLD:
            status = "critical"
            warnings.append(f"Same error repeated {count}x — agent is STUCK.")

    return {
        "status": status, "last_updated": now_iso(),
        "metrics": {"errors_in_window": len(recent_errors), "window_size": NOCI_WINDOW,
                     "unique_error_hashes": len(set(error_hashes)),
                     "repeated_errors": sum(1 for c in hash_counts.values() if c >= ECHO_REPEAT_THRESHOLD)},
        "warnings": warnings,
        "recommendation": "Pause and analyze root cause" if status != "normal" else "continue"
    }


def check_echo(events: list[dict], state: dict) -> dict:
    error_signatures = Counter()
    for e in events:
        content = json.dumps(e)
        if "error" in content.lower() or "错误" in content.lower():
            error_signatures[hash_text(content)] += 1

    status, warnings = "normal", []
    for sig, count in error_signatures.items():
        if count >= ECHO_REPEAT_THRESHOLD:
            status = "critical"
            warnings.append(f"Pattern {sig} repeated {count}x — stuck in loop")

    return {
        "status": status, "last_updated": now_iso(),
        "metrics": {"unique_error_signatures": len(error_signatures),
                     "repeated_signatures": sum(1 for c in error_signatures.values() if c >= ECHO_REPEAT_THRESHOLD),
                     "tool_distribution": dict(Counter(e.get("type", e.get("tool", "?")) for e in events).most_common(5))},
        "warnings": warnings,
        "recommendation": "Try a fundamentally different approach" if status != "normal" else "continue"
    }


def check_vestibular(events: list[dict], state: dict) -> dict:
    tool_types = Counter(e.get("type", e.get("tool", "unknown")) for e in events)
    total = sum(tool_types.values())
    dominant_pct = (tool_types.most_common(1)[0][1] / total * 100) if total > 0 else 0

    status, warnings = "normal", []
    if dominant_pct > VESTIBULAR_IMBALANCE_PCT and total > 5:
        status = "warning"
        warnings.append(f"{dominant_pct:.0f}% of calls are '{tool_types.most_common(1)[0][0]}' — diversify")

    return {
        "status": status, "last_updated": now_iso(),
        "metrics": {"total_calls": total, "tool_distribution": dict(tool_types.most_common()),
                     "dominant_percentage": round(dominant_pct, 1)},
        "warnings": warnings,
        "recommendation": "Consider different tool types" if status != "normal" else "continue"
    }


def check_spatial(events: list[dict], state: dict) -> dict:
    files_touched, tool_calls = set(), 0
    for e in events:
        paths = re.findall(r'(?:/[\w./-]+)', json.dumps(e))
        files_touched.update(paths)
        tool_calls += 1

    files_per_call = len(files_touched) / max(tool_calls, 1)
    status, warnings = "normal", []
    if files_per_call > SPATIAL_FILES_PER_CALL_WARN:
        status = "warning"
        warnings.append(f"High file churn: {files_per_call:.1f} files/call")

    return {
        "status": status, "last_updated": now_iso(),
        "metrics": {"unique_files_touched": len(files_touched), "tool_calls": tool_calls,
                     "files_per_call": round(files_per_call, 1)},
        "warnings": warnings,
        "recommendation": "Narrow scope" if status != "normal" else "continue"
    }


def check_drift(events: list[dict], state: dict) -> dict:
    if not events:
        return {"status": "normal", "last_updated": now_iso(), "metrics": {},
                "warnings": [], "recommendation": "continue"}

    first_user_msg = ""
    for e in events:
        if "role" in e and e["role"] == "user":
            first_user_msg = str(e.get("content", ""))[:200]
            break

    if not first_user_msg:
        return {"status": "normal", "last_updated": now_iso(), "metrics": {},
                "warnings": [], "recommendation": "continue"}

    keywords = set(re.findall(r'[\w一-鿿]{3,}', first_user_msg.lower()))
    recent_keywords = set()
    for e in events[-5:]:
        recent_keywords.update(re.findall(r'[\w一-鿿]{3,}', str(e.get("content", ""))[:500].lower()))

    overlap = len(keywords & recent_keywords) / len(keywords) * 100 if keywords else 100
    status, warnings = "normal", []
    if overlap < (100 - DRIFT_WARN_PCT):
        status = "warning"
        warnings.append(f"Topic drift: only {overlap:.0f}% overlap with session goal")

    return {
        "status": status, "last_updated": now_iso(),
        "metrics": {"keyword_overlap_percent": round(overlap, 1),
                     "original_keywords": list(keywords)[:10], "recent_keywords": list(recent_keywords)[:10]},
        "warnings": warnings,
        "recommendation": "Re-anchor to original task" if status != "normal" else "continue"
    }


def check_chronos(events: list[dict], state: dict) -> dict:
    last_active = state.get("last_active_at")
    idle_sec = 0
    if last_active:
        try:
            last_dt = datetime.fromisoformat(last_active)
            idle_sec = (datetime.now(timezone.utc) - last_dt).total_seconds()
        except (ValueError, TypeError):
            pass

    status, warnings = "normal", []
    if idle_sec > CHRONOS_IDLE_SEC:
        status = "warning"
        warnings.append(f"Idle for {idle_sec:.0f}s")

    return {
        "status": status, "last_updated": now_iso(),
        "metrics": {"idle_seconds": round(idle_sec, 0), "last_active_at": last_active or "unknown"},
        "warnings": warnings,
        "recommendation": "Check if stuck waiting" if status != "normal" else "continue"
    }


SENSE_CHECKS = {
    "o2": check_o2, "nociception": check_nociception, "echo": check_echo,
    "vestibular": check_vestibular, "spatial": check_spatial, "drift": check_drift,
    "chronos": check_chronos,
}


def run_all_checks(session_id: str = None) -> dict[str, dict]:
    transcript = get_latest_transcript()
    events = sample_recent_activity(transcript) if transcript else []
    results = {}
    for sense_name, check_fn in SENSE_CHECKS.items():
        state_path = SENSES_DIR / f"{sense_name}.json"
        state = load_json(state_path)
        state["session_id"] = session_id or state.get("session_id", "unknown")
        result = check_fn(events, state)
        save_json(state_path, result)
        results[sense_name] = result
    return results


def emit_alerts(results: dict[str, dict]) -> str:
    alerts = []
    for sense_name, result in results.items():
        if result["status"] in ("warning", "critical"):
            level = result["status"].upper()
            for w in result["warnings"]:
                alerts.append(f"[PHOENIX:{sense_name.upper()}:{level}] {w} → {result['recommendation']}")
    return "\n".join(alerts)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="PHOENIX 7-Sense Monitor")
    parser.add_argument("--session-id", help="Current session ID")
    parser.add_argument("--sense", choices=list(SENSE_CHECKS.keys()) + ["all"], default="all")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--alerts-only", action="store_true")
    args = parser.parse_args()

    session_id = args.session_id or os.environ.get("CLAUDE_SESSION_ID", f"session-{int(time.time())}")

    if args.sense == "all":
        results = run_all_checks(session_id)
    else:
        state_path = SENSES_DIR / f"{args.sense}.json"
        state = load_json(state_path)
        state["session_id"] = session_id
        transcript = get_latest_transcript()
        events = sample_recent_activity(transcript) if transcript else []
        results = {args.sense: SENSE_CHECKS[args.sense](events, state)}
        save_json(SENSES_DIR / f"{args.sense}.json", results[args.sense])

    if args.alerts_only:
        alerts = emit_alerts(results)
        if alerts:
            print(alerts)
    elif args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        alerts = emit_alerts(results)
        summary = {s: r["status"] for s, r in results.items()}
        print(f"PHOENIX Monitor — {now_iso()}")
        print(f"Session: {session_id}")
        print(f"Sense status: {json.dumps(summary, indent=2)}")
        if alerts:
            print(f"\nAlerts:\n{alerts}")
        else:
            print("\nAll senses normal")


if __name__ == "__main__":
    main()
