You are a BDD quality judge. Score the following Gherkin feature file
against this rubric. Return JSON only.

FEATURE FILE:
{generated_output}

RUBRIC:
1. Every AC has ≥1 scenario (2pts)
2. Data-driven ACs use Scenario Outline (2pts)
3. No scenario has >1 When step (1pt)
4. Every scenario is tagged (1pt)
5. Step text uses plain English (2pts)
6. Background used for shared preconditions (1pt)
7. Feature header has "So that" (1pt)

Return: { "score": N, "max": 10, "failures": ["..."] }
```

Run this judge after every skill change — if score drops below your threshold (e.g. 8/10), block the change.

📖 **Reference:** [LLM as a Judge — Maxim AI](https://www.getmaxim.ai/articles/llm-as-a-judge-a-practical-reliable-path-to-evaluating-ai-systems-at-scale/)

---

## Level 6 — Regression Testing When You Update Skills

Every time you edit a `SKILL.md`, re-run your full golden dataset and compare scores. You want fast, targeted signals that surface specific regressions early, rather than a single pass/fail verdict at the end. 

Maintain a `evals/scores.log`:
```
2026-01-10  v1.0  bdd-feature-generator  8.2/10
2026-01-18  v1.1  bdd-feature-generator  9.1/10  ← description keyword fix
2026-02-02  v1.2  bdd-feature-generator  7.8/10  ← REGRESSION — revert