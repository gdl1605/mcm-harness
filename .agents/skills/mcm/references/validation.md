# Validation

Serves `SKILL.md` Step 7: validate, stress-test, and explain why the result should be trusted.

Call this file when:

- A model has produced outputs.
- The user asks for sensitivity analysis, robustness, or reliability.
- The result looks plausible but not yet contest-ready.

## Validation Input Gate

Validation can start only after at least one of these exists:

- a first result table
- a first final answer artifact draft
- a baseline error/metric table
- a first scheme/decision table

If none of these exists, go back to execution. You are still planning, not validating.

## Minimum Validation Plan Template

Validation output must be structured. Use at least:

| 待验证结果 | baseline | 关键扰动参数/替代对照 | 可行性检查 | 合理性解释 | 缺口 |
| --- | --- | --- | --- | --- | --- |

If you only say “可以做灵敏度分析/对比实验”, validation is not started.

## When Validation Is Mandatory

Validation is mandatory if any of these is true:

- The task outputs a plan or strategy.
- The task claims improvement over a baseline.
- The task uses manually set parameters or thresholds.
- The task handles uncertainty, risk, or grouped rules.
- The task uses a classifier or anomaly detector.
- The task uses an interpretable statistical model and claims significance.

If none of these has been checked, the answer is not finished.

## Match Validation To Task Type

| Task type | Minimum validation | Stronger validation |
| --- | --- | --- |
| Evaluation/ranking | Weight or feature sensitivity | Stability of top-k under alternative settings |
| Prediction | Naive baseline or recent-history check | Rolling-window or scenario comparison |
| Optimization/decision | Baseline plan comparison | Parameter perturbation, scenario analysis, feasibility stress |
| Classification/clustering | Error inspection and feature interpretation | Alternative classifier, imbalance handling, boundary-case checks |
| Statistical analysis | Significance or robustness across groups | Alternative aggregation or subgroup comparison |
| Mechanism/process | Diagnostic checks | Alternative specifications, likelihood/comparison tests |

## High-Risk Contest Cases

### Repeated measurements / hierarchical data

If the same person/object appears multiple times, do at least one of these:

- compare within-group and between-group conclusions
- use grouped resampling or cluster bootstrap
- use mixed-effects or grouped diagnostics if the route supports it

Never claim strong significance from repeated rows treated as i.i.d. samples without checking this structure.

### Grouped timing / threshold decisions

If the answer is a recommended detection time, intervention time, or group boundary, validate all three:

- threshold perturbation
- group-boundary perturbation
- risk-weight or success-rate perturbation

The result is not contest-ready if the final recommendation changes dramatically under tiny perturbations and this is not discussed.

### Proxy-label / surrogate-target tasks

If the target is a screening result, intermediate判定, observed sell-through, or recent indicator rather than final truth:

- state that clearly
- report minority/abnormal-class recall or F1
- do not rely on overall accuracy alone
- explain what part of the real target is still unobserved or approximated

## Stable Contest Workflow

Use this order unless the task clearly needs something else:

1. Check whether the output is feasible.
2. Compare against a baseline.
3. Perturb the most important parameters.
4. Explain whether the conclusion changes.
5. Write one short reasonableness paragraph.

## Sensitivity Analysis Recipe

Use sensitivity analysis when:

- The answer depends on manually chosen weights
- The result changes with price, cost, yield, capacity, threshold, or grouping boundary
- The task explicitly asks for robustness or “灵敏度”

Recipe:

1. Pick 2-5 parameters that actually drive the answer.
2. Perturb them with a small, interpretable range such as `±5%`, `±10%`, or nearby thresholds.
3. Recompute the result.
4. Record what stays stable and what changes materially.
5. Report the direction and scale of change, not just “still good”.

Good writing:

- “Under a `±10%` yield change, the recommended crop mix remains unchanged for…”
- “The ranking of the top suppliers is stable except for…”
- “The optimal detection time shifts later when the accuracy threshold is raised.”

## How To Arrange Baseline, Alternative Models, And Perturbations

### Baseline

Choose the simplest defensible reference:

- Existing strategy
- Problem 1 result
- Naive forecast
- Simpler version of the current model

### Alternative model

Use when:

- The primary route is not the only reasonable route
- The user or judges may question whether the chosen model is overkill

Goal:

- Show why the chosen route is better suited
- Not prove every other method wrong

### Parameter perturbation

Use when:

- A threshold or weight was set manually
- Market, yield, supply, or biological variation matters

Goal:

- Show whether the decision is stable enough to trust

## How To Write Reasonableness Analysis

Every validation section should answer:

1. Is the result feasible?
2. Is the result directionally sensible?
3. Does it outperform or at least improve on a baseline?
4. Does it remain acceptable under small changes?
5. If repeated measurements or proxy labels exist, was that structure checked explicitly?

Template:

- “The proposed strategy satisfies all stated constraints and improves … relative to the baseline.”
- “The result remains stable under moderate perturbations of …”
- “This is consistent with domain expectations because …”

## Common Validation Gaps

- No baseline comparison
- Only one final number with no robustness check
- Sensitivity on irrelevant parameters instead of key drivers
- Statistical claims with no significance or diagnostics
- Classifier results with no error analysis or feature explanation
- Decision plan with no feasibility discussion
- Uncertainty mentioned in the prompt but ignored in the solution
- Writing a validation wishlist without any concrete result object to validate

## Quick Validation Checklist

Before closing the task, confirm:

1. Is there a baseline?
2. Is there at least one robustness check?
3. Is there at least one reasonableness explanation?
4. If the task is decision-heavy, has feasibility been checked?
5. If the task is diagnosis-heavy, have errors or diagnostics been inspected?

If any answer is “no”, validation is incomplete.
