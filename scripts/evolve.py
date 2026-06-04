#!/usr/bin/env python3
"""
PHOENIX Evolve — Framework Lifecycle Manager
Manages the full framework lifecycle: active → observed → validated → hardened
Auto-generates rule files from validated frameworks.
"""
import json, sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

PHOENIX_HOME = Path.home() / ".claude" / "phoenix"
FW_DIR = PHOENIX_HOME / "frameworks"
RULES_DIR = Path.home() / ".claude" / "rules" / "phoenix"
STORY_LOG = PHOENIX_HOME / "story.jsonl"

THRESHOLDS = {
    "active_to_observed": {"min_observations": 3, "min_confidence": 0.3},
    "observed_to_validated": {"min_observations": 10, "min_confidence": 0.6, "min_success_rate": 0.7},
    "validated_to_hardened": {"min_observations": 50, "min_confidence": 0.9, "min_success_rate": 0.9, "zero_contradictions": True},
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_frameworks(stage: str) -> list[dict]:
    stage_dir = FW_DIR / stage
    if not stage_dir.exists():
        return []
    return [json.loads(p.read_text()) for p in stage_dir.glob("*.json") if p.name != "framework-schema.json"]


def save_framework(fw: dict, stage: str):
    (FW_DIR / stage).mkdir(parents=True, exist_ok=True)
    (FW_DIR / stage / f"{fw['id']}.json").write_text(json.dumps(fw, indent=2, ensure_ascii=False))


def delete_framework(fw: dict, stage: str):
    p = FW_DIR / stage / f"{fw['id']}.json"
    if p.exists():
        p.unlink()


def log_event(event_type: str, description: str, details: dict = None):
    entry = {"event": event_type, "timestamp": now_iso(), "description": description, "details": details or {}}
    with open(STORY_LOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def calc_conf(fw: dict) -> float:
    total = fw.get("successes", 0) + fw.get("failures", 0)
    return fw.get("successes", 0) / total if total > 0 else fw.get("confidence", 0.1)


def check_promotion(fw: dict, stage: str) -> Optional[str]:
    if stage == "active":
        t = THRESHOLDS["active_to_observed"]
        if fw["observations"] >= t["min_observations"] and calc_conf(fw) >= t["min_confidence"]:
            return "observed"
    elif stage == "observed":
        t = THRESHOLDS["observed_to_validated"]
        sr = fw.get("successes", 0) / max(fw["observations"], 1)
        if fw["observations"] >= t["min_observations"] and calc_conf(fw) >= t["min_confidence"] and sr >= t["min_success_rate"]:
            return "validated"
    elif stage == "validated":
        t = THRESHOLDS["validated_to_hardened"]
        sr = fw.get("successes", 0) / max(fw["observations"], 1)
        if fw["observations"] >= t["min_observations"] and calc_conf(fw) >= t["min_confidence"] and sr >= t["min_success_rate"] and fw.get("failures", 0) == 0:
            return "hardened"
    return None


def check_demotion(fw: dict, stage: str) -> Optional[str]:
    if stage in ("observed", "validated", "hardened") and calc_conf(fw) < 0.3 and fw["observations"] > 5:
        return {"hardened": "validated", "validated": "observed", "observed": "active"}.get(stage)
    return None


def generate_rule_file(fw: dict) -> Path:
    RULES_DIR.mkdir(parents=True, exist_ok=True)
    rp = RULES_DIR / f"{fw['id']}.md"
    el = ["CLAUDE.md advice", "memory injection", "skill guidance",
          "rule file", "hook warning", "hook block", "session abort"]
    rp.write_text(f"""# {fw['id'].replace('-', ' ').title()} (PHOENIX Auto-Generated)

> Auto-evolved rule from PHOENIX Evolution Engine
> Stage: {fw.get('stage', 'validated')} | Confidence: {calc_conf(fw):.0%}
> Observations: {fw.get('observations', 0)} | Successes: {fw.get('successes', 0)} | Failures: {fw.get('failures', 0)}
> Enforcement: {el[fw.get('enforcement_level', 4) - 1]} (Level {fw.get('enforcement_level', 4)})

## Trigger

{fw.get('trigger', 'Auto-detected pattern')}

## Action

{fw.get('action', 'Apply this pattern when the trigger condition is met')}

## Domains

{', '.join(fw.get('domains', ['general']))}

## Evolution History

- Created: {fw.get('created_at', 'unknown')}
- Evolved from: {', '.join(fw.get('evolved_from', [])) or 'original detection'}
- Amendments: {', '.join(fw.get('amendments', [])) or 'none'}
""")
    return rp


def promote(fw: dict, fm: str, to: str):
    fw["stage"] = to
    fw["confidence"] = calc_conf(fw)
    fw["promoted_at"] = fw.get("promoted_at", {})
    fw["promoted_at"][to] = now_iso()
    fw["enforcement_level"] = {"active": 1, "observed": 2, "validated": 4, "hardened": 6}.get(to, 1)
    delete_framework(fw, fm)
    save_framework(fw, to)
    if to == "validated":
        generate_rule_file(fw)
        log_event("rule-generated", f"Auto-generated rule: {fw['id']}")
    elif to == "hardened":
        log_event("framework-hardened", f"Framework {fw['id']} reached HARDENED stage")
    log_event("framework-promoted", f"Promoted {fw['id']}: {fm} → {to}",
              {"from": fm, "to": to, "confidence": fw['confidence']})


def demote(fw: dict, fm: str, to: str):
    fw["stage"] = to
    fw["confidence"] = max(0.1, calc_conf(fw) - 0.2)
    fw["enforcement_level"] = {"active": 1, "observed": 2, "validated": 4, "hardened": 6}.get(to, 1)
    delete_framework(fw, fm)
    save_framework(fw, to)
    if fm == "validated":
        rp = RULES_DIR / f"{fw['id']}.md"
        if rp.exists():
            rp.unlink()
    log_event("framework-demoted", f"Demoted {fw['id']}: {fm} → {to}")


def sync_to_soul(frameworks: list[dict]):
    sp = PHOENIX_HOME / "soul.json"
    try:
        soul = json.loads(sp.read_text())
    except (json.JSONDecodeError, OSError):
        return
    eids = {t["id"] for t in soul.get("validated_truths", [])}
    for fw in frameworks:
        if fw["stage"] in ("validated", "hardened"):
            t = {
                "id": fw["id"],
                "statement": f"{fw['trigger']} → {fw['action']}",
                "confidence": calc_conf(fw),
                "source": "PHOENIX Evolution Engine",
                "stage": fw["stage"],
                "observations": fw["observations"]
            }
            if fw["id"] in eids:
                for i, vt in enumerate(soul.get("validated_truths", [])):
                    if vt["id"] == fw["id"]:
                        soul["validated_truths"][i] = t
                        break
            else:
                soul["validated_truths"].append(t)
                eids.add(fw["id"])
    sp.write_text(json.dumps(soul, indent=2, ensure_ascii=False))


def run_cycle() -> dict:
    stages = ["active", "observed", "validated", "hardened"]
    all_fws = {s: load_frameworks(s) for s in stages}
    stats = {"checked": 0, "promoted": 0, "demoted": 0, "rules_generated": 0}

    for stage in stages:
        for fw in all_fws[stage]:
            stats["checked"] += 1
            ns = check_promotion(fw, stage)
            if ns:
                promote(fw, stage, ns)
                stats["promoted"] += 1
            ds = check_demotion(fw, stage)
            if ds:
                demote(fw, stage, ds)
                stats["demoted"] += 1

    for s in stages:
        stats[s] = len(list((FW_DIR / s).glob("*.json")))

    sync_to_soul(load_frameworks("validated") + load_frameworks("hardened"))
    log_event("evolution-cycle", f"Cycle complete: {stats['promoted']}↑ {stats['demoted']}↓", stats)
    return stats


def main():
    import argparse
    p = argparse.ArgumentParser(description="PHOENIX Evolution Engine")
    p.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    p.add_argument("--framework", help="Inspect a specific framework")
    args = p.parse_args()

    print(f"PHOENIX Evolution Engine — {now_iso()}\n")

    if args.framework:
        for s in ["active", "observed", "validated", "hardened"]:
            fp = FW_DIR / s / f"{args.framework}.json"
            if fp.exists():
                fw = json.loads(fp.read_text())
                print(f"Framework: {fw['id']} | Stage: {fw['stage']}")
                print(f"  Confidence: {calc_conf(fw):.0%} | Observations: {fw['observations']}")
                print(f"  S/F: {fw.get('successes', 0)}/{fw.get('failures', 0)}")
                return
        print(f"Framework '{args.framework}' not found")
        return

    if args.dry_run:
        stats = {"checked": 0, "promoted": 0}
        for s in ["active", "observed", "validated", "hardened"]:
            for fw in load_frameworks(s):
                stats["checked"] += 1
                ns = check_promotion(fw, s)
                if ns:
                    print(f"  Would promote: {fw['id']} ({s} → {ns})")
                    stats["promoted"] += 1
        print(f"\nWould promote {stats['promoted']} of {stats['checked']} frameworks")
    else:
        stats = run_cycle()
        print(f"Checked: {stats['checked']} | Promoted: {stats['promoted']} | Demoted: {stats['demoted']}")
        print(f"Rules generated: {stats['rules_generated']}")
        print(f"Distribution: active={stats.get('active',0)} observed={stats.get('observed',0)} "
              f"validated={stats.get('validated',0)} hardened={stats.get('hardened',0)}")

    print("\nEvolution cycle complete.")


if __name__ == "__main__":
    main()
