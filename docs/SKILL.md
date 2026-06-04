---
name: phoenix
description: PHOENIX Self-Evolving Agent Harness — master orchestrator for continuous autonomous evolution. Fuses ECC + MUNDO + Metacog + Claude Soul + Autoresearch patterns. Triggers metacognitive monitoring, framework lifecycle management, self-correction, and enforcement hierarchy. Activated automatically at session start and periodically during sessions.
origin: PHOENIX
version: 1.0.0
---

# PHOENIX — Self-Evolving Agent Harness

## When to Use

This skill is **ALWAYS ACTIVE**. It operates in the background, monitoring agent behavior and evolving the configuration. Specific triggers:

- **Session Start**: Injects soul.json truths and validated frameworks into context
- **Every 10 tool calls**: Triggers metacognitive 7-sense check via PostToolUse hook
- **Session End**: Triggers evolution analysis via Stop hook (framework promotion, pattern extraction)
- **On error spike**: Triggers nociception (pain) detection and self-correction
- **Manual trigger**: `/phoenix-status`, `/phoenix-evolve`, `/phoenix-correct`

## Core Architecture

```
┌──────────┐    ┌──────────┐    ┌───────────┐
│ Observer │ → │Evolution │ → │Self-Correct│
│ (7-sense)│   │  Engine  │   │  Engine   │
└────┬─────┘    └────┬─────┘   └─────┬─────┘
     │               │               │
senses/*.json   frameworks/     amendments/
     │               │               │
     └───────────────┼───────────────┘
                     ↓
           soul.json / shadow.json
```

## Metacognitive 7-Sense System (from Metacog)

| Sense | What It Detects | Threshold | Response |
|-------|----------------|-----------|----------|
| **O2** (Vitality) | Token burn rate, message velocity | >70% context | Suggest compaction |
| **Chronos** (Time) | Wall-clock time, session duration, task pacing | >5min idle | Check if stuck |
| **Nociception** (Pain) | Error cascade, repeated failures | >2 errors in 5 calls | Pause and analyze root cause |
| **Spatial** (Space) | File dependency count, working directory churn | >5 files touched/call | Check scope creep |
| **Vestibular** (Balance) | Context distribution, tool type imbalance | >80% one tool type | Diversify approach |
| **Echo** (Repetition) | Same error or fix recurrence | Same error 3x | Force different strategy |
| **Drift** (Focus) | Semantic distance from session goal | Topic shift >30% | Re-anchor to original task |

## Framework Lifecycle (from Claude Soul)

```
hypothesis ──(3+ observations, >30% confidence)──→ observed
observed   ──(10+ observations, >60% confidence)──→ validated
validated  ──(50+ observations, >90% confidence)──→ hardened
```

**At each promotion**:
- `active → observed`: Start injecting as "suggested behavior"
- `observed → validated`: Promote to a rule file in `rules/phoenix/`
- `validated → hardened`: Enforce via hook (exit code 2 on violation)

## Enforcement Hierarchy (from ContinuousClaude)

| Level | Mechanism | When Applied | Violation Consequence |
|-------|-----------|-------------|----------------------|
| **7** | Hook exit code 2 | Hardened frameworks | Tool call BLOCKED |
| **6** | Hook warning | Validated frameworks | Warning + override prompt |
| **5** | PostToolUse diagnostic | Observed frameworks | Correction suggested |
| **4** | Rule file | Validated frameworks | Violation noted |
| **3** | Skill auto-trigger | Observed frameworks | Best practice suggested |
| **2** | Memory injection | Active frameworks | Contextual reminder |
| **1** | CLAUDE.md advice | All frameworks | Behavioral preference |

## Self-Correction Pipeline (from Autoresearch)

Karpathy Cycle: `measure → change → verify → keep/discard`

1. **Detect decline**: Framework success rate drops >10% over 7-day window
2. **Analyze**: Compare recent failures to historical success patterns
3. **Propose**: Generate amendment in `amendments/pending/{id}.json`
4. **Shadow test**: Run amendment in observation mode for N sessions (default 5)
5. **Verify**: Compare outcomes (old vs new behavior)
6. **Apply or Reject**: Move to `applied/` or `rejected/`

## PHOENIX Commands

- `/phoenix-status` — Display full evolution dashboard (soul, shadow, frameworks, senses)
- `/phoenix-evolve` — Manually trigger evolution analysis cycle
- `/phoenix-correct <framework-id>` — Trigger self-correction for a specific framework
- `/phoenix-observe` — Run a 7-sense observation checkpoint
- `/phoenix-promote <framework-id>` — Manually promote a framework to next stage
- `/phoenix-amend <id>` — Review and vote on a pending amendment

## Integration Points

PHOENIX is not a standalone system — it orchestrates existing ECC infrastructure:

- **Monitoring** → Uses ECC's PostToolUse hooks + metacog-observer agent
- **Evolution** → Uses ECC's Stop hooks + evolution-engine agent
- **Correction** → Uses ECC's skill-evolution health tracking + self-correct agent
- **Memory** → Extends ECC's continuous-learning-v2 with framework lifecycle
- **Rules** → Auto-generates `rules/phoenix/` files from validated frameworks
- **Soul/Shadow** → Session-start hook injects into context alongside ECC rules

## Evolution Data Flow

```
Session runs → PostToolUse hook fires → monitor.py samples
  → senses/*.json updated → anomaly? → inject warning
  → Session ends → Stop hook fires → evolve.py runs
    → pattern extraction → framework creation/promotion
    → self-correct.py checks for declining frameworks
      → amendment proposed → shadow testing scheduled
    → story.jsonl appended
    → metrics/sessions.jsonl updated
  → Next SessionStart → soul.json + validated frameworks injected
```

## Key Design Principles

1. **失败教训权重 > 成功经验**: shadow.json always checked before soul.json (MUNDO principle)
2. **渐进式提升**: frameworks move through stages based on evidence, not time
3. **零人工干预**: once seeded, the evolution pipeline runs autonomously
4. **可审计**: all state is human-readable JSON/JSONL, git-diffable
5. **可回滚**: amendments can be rejected, frameworks can be demoted
