# Model Selection

Serves `SKILL.md` Step 3: choose a primary path and decide whether a backup path is needed for each subproblem.

Call this file when:

- You have already typed the question.
- You need contest-safe model choices instead of a model name dump.
- You need to explain why a route fits and how to validate it.

## Output Contract For Route Selection

Route selection must be a decision card, not a prose blob.

For each question, output at least:

| 问题 | 风险等级 | 主方案 | 是否需要备选 | 备选方案或“不需要备选”的理由 | 验证方式 | 最终输出对象 |
| --- | --- | --- | --- | --- | --- | --- |

If this table is missing, route selection is not finished.

## Contest-Safe Choice Principles

Use these principles before naming any model:

1. Prefer fit-to-deliverable over fit-to-fashion.
2. Prefer an explainable baseline before an advanced variant.
3. Prefer routes that naturally connect to validation and paper writing.
4. Treat low-frequency methods as backup options unless data structure clearly requires them.

## When A Backup Path Is Mandatory

You should provide a backup path when at least one of these is true:

- the question is high-risk because of repeated measurements, proxy targets, threshold-time, or unstable constraints
- the primary route depends on a strong modeling assumption
- the prompt is decision-heavy and the judges may challenge feasibility or robustness
- the data quality, aggregation grain, or target definition is uncertain

## When A Primary Path Alone Is Enough

You may keep only the primary path when all of these are true:

- the question is low-risk and the output object is straightforward
- the route is descriptive or clearly single-path
- the baseline can already answer the prompt directly
- you explicitly state why a backup path is unnecessary

Do not force a decorative backup path onto a simple question.

## By-Type Selection Rules

## 1. Evaluation / Ranking

### Primary path `[高频共性]`

- Build stable features first.
- Standardize and align direction.
- Use a composite evaluation method such as TOPSIS, entropy-weighted TOPSIS, or a clear indicator system.

Use this when:

- The output is a ranked list or priority score.
- Multiple indicators matter at the same time.
- The ranking will feed a later decision step.

Data needed:

- A feature table per object
- Clear indicator meaning
- Direction and scale information

Main risks:

- Ranking by raw totals
- Ignoring volatility, stability, or risk indicators

Validation:

- Compare ranking under different weights or feature subsets.
- Check whether top objects remain stable.

### Backup path `[中频经验]`

- Reduce or screen features first with PCA, VIP-style screening, or other dimension reduction.
- Then rank or classify.

Use this when:

- Indicators are highly correlated.
- Feature dimension is high relative to sample size.

Do not default to:

- Black-box classification replacing ranking logic
- Clustering when the task clearly asks for ordered importance

## 2. Prediction

### Primary path A: short-horizon operational prediction `[高频共性]`

- Aggregate data to the decision grain.
- Use regression or short-horizon time-series methods.
- Feed forecasts into the downstream decision model.

Use this when:

- The task asks for future daily/weekly demand, price, or supply.
- The prediction horizon is short.

Main risks:

- Predicting at the wrong grain
- Using a heavy model on a short window without payoff
- Treating observed sales, recent loss, or other surrogate indicators as the full true target without stating the approximation

Validation:

- Compare with a naive baseline.
- Check forecast direction and scale against recent history.
- State whether the predicted quantity is true demand, observed sell-through, or another proxy target

### Primary path B: threshold-time / process prediction `[中频经验]`

- Start with a threshold-time baseline that the paper can explain:
  - first-hit table, reach-rate table, percentile timing table, or grouped threshold summary
- Then use interpretable process-aware models such as mixed-effects, Gaussian process regression, or survival-style probability models if the baseline is not enough

Use this when:

- The task asks when a threshold is first reached.
- Repeated measurements or grouped individuals exist.

Main risks:

- Treating repeated measurements as independent rows
- Using static classification to answer a timing question
- Jumping to deep sequence models before a percentile/reach-rate baseline exists

Validation:

- Diagnostics for fit quality
- Sensitivity to threshold and grouping choices
- Comparison between baseline timing rule and advanced timing model

### Backup path `[中频经验]`

- Use scenario-based prediction or parameter intervals when historical sequence depth is limited.

## 3. Optimization / Decision

### Primary path `[高频共性]`

- Translate business rules into variables, objective, and constraints first.
- Start from linear, integer, 0-1, or multi-objective programming if the structure permits it.
- For grouped timing or screening decisions, define:
  - the risk/loss term
  - the success-rate or feasibility constraint
  - the final recommendation table the contest needs

Use this when:

- The output is a plan, schedule, allocation, pricing rule, or resource strategy.
- Constraints are explicit or recoverable from the prompt.

Data needed:

- Decision grain
- Feasible set
- Objective components
- Constraint table

Validation:

- Compare with baseline or prior plan.
- Perturb the key parameters.
- Check feasibility under edge conditions.

### Backup path `[高频共性]`

- Keep the mathematical model.
- Use a solver-oriented or heuristic route such as GA, DEGA, SA, greedy, dynamic programming, or random planning only after the model structure is clear.
- If the task is threshold timing, keep a percentile or quantile-based decision baseline in reserve even when using GA or other heuristics.

Use this when:

- Search space is large
- Nonlinearity or discreteness blocks direct solving
- Multiple scenarios or risk layers must be handled

Do not default to:

- “Use genetic algorithm” without variables and constraints
- Algorithm-first explanations
- A heuristic search with no recommendation table or no baseline decision rule

## 4. Classification / Clustering

### Primary path `[中频经验]`

- Standardize or transform features if needed.
- Screen features.
- Use a supervised classifier when labels exist.
- Use clustering only as exploration when labels do not exist.

Strong contest routes:

- PLS-DA for structured component data
- LightGBM or similar tree ensembles with feature importance for tabular classification

Use this when:

- The output is class assignment or abnormality determination.

Main risks:

- Ignoring class imbalance
- Reporting only accuracy without feature interpretation
- Treating a proxy label as if it were the final ground-truth outcome

Validation:

- Holdout or cross-check if feasible
- Confusion-style error inspection
- Feature importance or variable contribution summary
- Recall/F1 for minority or abnormal classes when those classes matter more than overall accuracy

### Backup path `[中频经验]`

- Cluster first, then classify or interpret groups if labels are weak or incomplete.

Use this only when the prompt supports exploratory grouping.

## 5. Statistical Analysis / Correlation

### Primary path `[高频共性]`

- Start with descriptive statistics and visualization.
- Add correlation or significance testing.
- Push the findings into a later forecast, ranking, or decision model when needed.

Use this when:

- The question asks for distributional patterns or associations.

Main risks:

- Stopping at a correlation matrix when the contest still needs a decision output

Validation:

- Check robustness across groups, windows, or aggregation levels.

## 6. Process / Mechanism Explanation

### Primary path `[中频经验]`

- Use interpretable relation models.
- Respect hierarchy or repeated measurements.
- Add diagnostics such as AIC/BIC, likelihood-based comparisons, residual checks, or random-effect diagnostics where relevant.

Use this when:

- The question asks how a process evolves, not just what the final label is.

Do not default to:

- A purely black-box model that cannot explain the mechanism

## Common Combined Routes

Use these routes often. They are more reliable than inventing a brand-new chain each time.

| Combined route | Best use |
| --- | --- |
| Evaluation -> optimization | Too many candidates; need screening before planning |
| Statistical analysis -> prediction -> optimization | Operational data with future decision output |
| Statistical analysis -> feature screening -> classification | High-dimensional tabular or composition-style data |
| Mechanism explanation -> grouping -> timing/strategy optimization | Threshold timing or grouped decision problems |

## How To Choose Between “Advanced” And “Stable”

Prefer the stable route when:

- The simpler model answers the question directly.
- The advanced route adds little writing value.
- Validation and interpretation would become weaker.
- Data size or structure does not justify the added complexity.
- The contest still lacks a clear answer table, risk function, or baseline recommendation rule

Escalate to the advanced route when:

- The task is impossible to answer well with the baseline.
- The data structure truly demands it.
- You can still explain, validate, and defend the route under contest time pressure.

## Quick Decision Frame

For each subproblem, fill this frame:

- Primary type:
- Required deliverable:
- Primary path:
- Why it fits:
- Is backup needed:
- Backup path (if needed):
- Why keep it in reserve / why it is safe to omit:
- Required preprocessing:
- First executable baseline:
- Required validation:
- Biggest failure mode:

If this frame is incomplete, the model choice is not ready.
