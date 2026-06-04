#!/usr/bin/env python3
"""
PHOENIX Correct — Self-Correction Engine (Karpathy Cycle)
measure → change → verify → keep/discard
"""
import json, sys
from pathlib import Path
from datetime import datetime, timezone

PHOENIX_HOME = Path.home() / ".claude" / "phoenix"
AMEND_DIR = PHOENIX_HOME / "amendments"
FW_DIR = PHOENIX_HOME / "frameworks"
STORY_LOG = PHOENIX_HOME / "story.jsonl"
SHADOW_SESSIONS_DEFAULT = 5


def now_iso(): return datetime.now(timezone.utc).isoformat()


def load_all_frameworks() -> list[dict]:
    frameworks = []
    for stage in ["active", "observed", "validated", "hardened"]:
        sd = FW_DIR / stage
        if sd.exists():
            for p in sd.glob("*.json"):
                if p.name != "framework-schema.json":
                    try: frameworks.append(json.loads(p.read_text()))
                    except: continue
    return frameworks


def load_pending_amendments() -> list[dict]:
    d = AMEND_DIR / "pending"
    if not d.exists(): return []
    return [json.loads(p.read_text()) for p in d.glob("*.json")]


def save_amendment(am: dict, status: str):
    (AMEND_DIR / status).mkdir(parents=True, exist_ok=True)
    am["status"] = status
    (AMEND_DIR / status / f"{am['id']}.json").write_text(json.dumps(am, indent=2, ensure_ascii=False))


def delete_amendment(am: dict, status: str):
    p = AMEND_DIR / status / f"{am['id']}.json"
    if p.exists(): p.unlink()


def log_event(event_type: str, description: str, details: dict = None):
    with open(STORY_LOG, "a") as f:
        f.write(json.dumps({"event": event_type, "timestamp": now_iso(), "description": description, "details": details or {}}, ensure_ascii=False) + "\n")


def detect_decline(frameworks: list[dict]) -> list[dict]:
    """Detect frameworks with declining performance"""
    declining = []
    for fw in frameworks:
        total = fw.get("successes", 0) + fw.get("failures", 0)
        if total < 5: continue
        sr = fw.get("successes", 0) / total
        if sr < 0.5 and fw.get("stage") in ("observed", "validated"):
            declining.append({"framework": fw, "success_rate": sr, "reason": f"Success rate {sr:.0%} < 50%"})
        if fw.get("failures", 0) >= 3 and fw.get("successes", 0) < fw.get("failures", 0):
            declining.append({"framework": fw, "success_rate": sr, "reason": f"Failures ({fw['failures']}) > successes ({fw['successes']})"})
    return declining


def propose_amendment(fw: dict, reason: str) -> dict:
    """Generate an amendment proposal for a declining framework"""
    amendment_id = f"amend-{int(datetime.now(timezone.utc).timestamp())}"
    return {
        "id": amendment_id,
        "framework_id": fw["id"],
        "type": "correction",
        "description": f"Auto-proposed correction for {fw['id']}: {reason}",
        "proposed_trigger": fw.get("trigger", ""),
        "proposed_action": fw.get("action", ""),
        "evidence": [reason, f"Success rate: {fw.get('successes', 0)}/{fw.get('successes', 0) + fw.get('failures', 0)}"],
        "confidence": 0.5,
        "status": "pending",
        "created_at": now_iso(),
        "shadow_sessions_remaining": SHADOW_SESSIONS_DEFAULT
    }


def evaluate_shadows() -> list[dict]:
    """Evaluate pending amendments that have completed shadow testing"""
    results = []
    for am in load_pending_amendments():
        if am.get("shadow_sessions_remaining", 0) <= 0:
            if am.get("shadow_successes", 0) > am.get("shadow_failures", 0):
                results.append({"amendment": am, "decision": "keep", "reason": "Shadow testing showed improvement"})
            else:
                results.append({"amendment": am, "decision": "discard", "reason": "Shadow testing showed no improvement or decline"})
    return results


def apply_amendment(am: dict):
    """Apply a kept amendment to its framework"""
    for stage in ["active", "observed", "validated", "hardened"]:
        fpath = FW_DIR / stage / f"{am['framework_id']}.json"
        if fpath.exists():
            fw = json.loads(fpath.read_text())
            if am.get("proposed_trigger"): fw["trigger"] = am["proposed_trigger"]
            if am.get("proposed_action"): fw["action"] = am["proposed_action"]
            fw["amendments"] = fw.get("amendments", []) + [am["id"]]
            fpath.write_text(json.dumps(fw, indent=2, ensure_ascii=False))
            delete_amendment(am, "pending")
            save_amendment(am, "applied")
            log_event("amendment-applied", f"Applied {am['id']} to {am['framework_id']}", am)
            return
    # Framework not found — reject
    delete_amendment(am, "pending")
    save_amendment(am, "rejected")
    log_event("amendment-rejected", f"Framework {am['framework_id']} not found for amendment {am['id']}")


def main():
    import argparse
    p = argparse.ArgumentParser(description="PHOENIX Self-Correction Engine")
    p.add_argument("--check-all", action="store_true", help="Check all frameworks for decline")
    p.add_argument("--evaluate-shadows", action="store_true", help="Evaluate completed shadow tests")
    p.add_argument("--framework", help="Target specific framework ID")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    print(f"PHOENIX Self-Correct — {now_iso()}\n")

    if args.evaluate_shadows:
        results = evaluate_shadows()
        for r in results:
            print(f"  {r['decision'].upper()}: {r['amendment']['id']} ({r['reason']})")
            if r["decision"] == "keep" and not args.dry_run:
                apply_amendment(r["amendment"])
        if not results: print("  No amendments ready for evaluation")
        return

    frameworks = load_all_frameworks()
    if args.framework:
        frameworks = [fw for fw in frameworks if fw["id"] == args.framework]

    declining = detect_decline(frameworks)
    if not declining:
        print("No declining frameworks detected.")
        return

    for d in declining:
        fw = d["framework"]
        print(f"  Decline detected: {fw['id']} — {d['reason']}")
        if not args.dry_run:
            am = propose_amendment(fw, d["reason"])
            save_amendment(am, "pending")
            print(f"    → Amendment proposed: {am['id']} (shadow sessions: {SHADOW_SESSIONS_DEFAULT})")
            log_event("amendment-proposed", f"Proposed {am['id']} for {fw['id']}", am)

    if args.dry_run:
        print(f"\n[DRY RUN] Would propose {len(declining)} amendments")


if __name__ == "__main__":
    main()
