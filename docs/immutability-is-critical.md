# Immutability Is Critical (鲤鱼 Seed Rule)

> Auto-evolved rule | Stage: validated | Confidence: 95%
> Observations: 50 | Successes: 48 | Failures: 2
> Enforcement: rule file (Level 4)
> Source: ECC coding-style.md + MUNDO memory patterns

## Trigger

When modifying state in any programming language — TypeScript, Python, Go, Java, Rust, etc.

## Action

ALWAYS create new objects. NEVER mutate existing ones.

```typescript
// WRONG: mutation
obj.field = newValue;
array.push(item);

// CORRECT: immutability
const newObj = { ...obj, field: newValue };
const newArray = [...array, item];
```

Rationale: Immutable data prevents hidden side effects, makes debugging easier, and enables safe concurrency.

## Domains

code-style, all-languages, debugging

## Evolution History

- Created: 2026-06-05 from ECC coding-style.md rule
- Evolved from: ECC common rules
- Amendments: none
