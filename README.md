# 🐦‍🔥 PHOENIX — Self-Evolving Agent Harness v1.0.0

> *"每一段进化，都是从一次观察开始的"*
> — PHOENIX, born from the fusion of ECC + MUNDO + Metacog + Claude Soul

---

## What Is PHOENIX?

PHOENIX is a **self-evolving agent configuration layer** for Claude Code. It is not a new agent runtime — it is a metacognitive orchestration system that makes Claude Code's configuration a **living, evolving entity**.

It observes its own behavior, extracts patterns, promotes successful frameworks through a lifecycle, and self-corrects when performance declines.

## Architecture

```
┌─────────────────────────────────────────────┐
│              PHOENIX Evolution Layer         │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│  │ Observer │→│Evolution │→│Self-Correct│  │
│  │ (7-sense)│  │  Engine  │  │  Engine   │  │
│  └────┬─────┘  └────┬─────┘  └─────┬─────┘  │
│       │              │              │        │
│  senses/*.json  frameworks/   amendments/   │
│       │              │              │        │
│       └──────────────┼──────────────┘        │
│                      ↓                       │
│         soul.json / shadow.json              │
│         story.jsonl                          │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────┼──────────────────────┐
│           ECC Infrastructure                │
│  67 agents · 92 skills · 85 rules · 34 hooks │
└─────────────────────────────────────────────┘
```

## Core Features

### 🧠 7-Sense Metacognitive Monitoring
Real-time awareness of agent state: O2 (vitality), Chronos (time), Nociception (pain), Spatial (workspace), Vestibular (balance), Echo (repetition), Drift (focus)

### 🔄 4-Stage Framework Lifecycle
`active → observed → validated → hardened` — behavioral patterns evolve through evidence-based promotion

### 🩹 Karpathy Self-Correction Cycle
`measure → change → verify → keep/discard` — declining frameworks auto-correct with shadow testing

### 📊 7-Level Enforcement Hierarchy
`CLAUDE.md advice → Memory → Skill → Rule → Hook Warning → Hook Block → Session Abort`

### 💾 Persistent Soul & Shadow
`soul.json`: validated truths, core values, evolution metrics
`shadow.json`: anti-patterns, failure lessons (importance: 9 > success: 7)

## File Structure

```
phoenix-site/
├── index.html           # Main landing page
├── README.md            # This file
├── docs/
│   ├── CLAUDE.md        # PHOENIX Constitution (full)
│   ├── SKILL.md         # Master orchestrator skill
│   ├── soul.json        # Core identity state
│   ├── shadow.json      # Failure patterns state
│   ├── framework-schema.json  # Framework template
│   ├── story.jsonl      # Evolution event log
│   └── evolution.jsonl  # Evolution metrics
├── scripts/
│   ├── monitor.py       # 7-sense monitoring engine
│   ├── evolve.py        # Framework lifecycle manager
│   ├── correct.py       # Self-correction engine
│   └── analyze.py       # Pattern extraction engine
└── agents/
    ├── metacog-observer.md   # Observer agent definition
    ├── evolution-engine.md   # Evolution agent definition
    └── self-correct.md       # Self-correction agent definition
```

## Quick Start

```bash
# Clone the repository
git clone https://github.com/holyty/phoenix-site.git
cd phoenix-site

# Run the 7-sense monitor
python3 scripts/monitor.py

# Check evolution status
python3 scripts/evolve.py --dry-run

# Run pattern analysis
python3 scripts/analyze.py

# Check for self-correction needs
python3 scripts/correct.py --check-all
```

## The Evolution Promise

| Sessions | Expected State |
|----------|---------------|
| 1-5 | First active frameworks detected |
| 10-20 | 3-5 frameworks reach observed, begin behavior injection |
| 30-50 | First auto-generated rules in `rules/phoenix/` |
| 100+ | First hardened framework 💎 |

## Fusion Sources

PHOENIX draws inspiration from the best agent systems:

| Source | What We Learned |
|--------|----------------|
| **ECC** (Everything Claude Code, 207k⭐) | Agent orchestration, hook system, rule framework |
| **MUNDO Agent v1.2.0** (LiHongwei) | Context budget, affective intelligence, memory architecture |
| **Metacog** (houtini-ai) | 7-sense monitoring, nociception escalation, motor learning |
| **Claude Soul** (DomDemetz) | Framework lifecycle, soul/shadow identity, evolution tracking |
| **Continuous Claude** (parcadei) | Enforcement hierarchy, Ouros sandbox, force compaction |
| **Autoresearch** (uditgoenka) | Karpathy cycle, one-change-at-a-time, auto-rollback |

## License

MIT — Free and open source.

---

*Born from the fusion of 207,000 stars of collective intelligence. Evolving one observation at a time.* 🐦‍🔥
