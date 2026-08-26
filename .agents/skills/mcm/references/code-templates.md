# Code Templates

Serves `SKILL.md` Steps 5-6: turn a plan into executable artifacts, intermediate tables, and first contest-facing outputs.

Call this file when:

- You need to start coding quickly from a modeling plan.
- You need a contest-safe project structure.
- You need to avoid chaotic scripts and missing intermediate outputs.

## Execution Gate: Planning Is Not Execution

Implementation is not considered started until you have exported something usable.

Before moving to validation, export at least:

- one clean or intermediate table
- one first result table or figure
- one first final-answer artifact draft

If these do not exist, keep coding. Do not pretend that a script outline is a finished execution step.

## Snippet And Demo Routing

If a matching repository asset already covers the baseline, use it before writing a fresh scaffold.

- 排序/Top-k/筛选表：`assets/snippets/entropy_topsis.py`
- 短期运营预测、`日期 × 对象/品类` 结果表：`assets/snippets/naive_forecast.py`
- 线性决策表：`assets/snippets/lp_basic.py`
- 0-1/整数选择与分配表：`assets/snippets/integer_programming_basic.py`
- 多表、面板、运营流水预处理：`assets/snippets/data_preprocessing_skel.py`

Use `assets/end_to_end_demo/2021_C_problem1/` when you need a worked example of：
`原始特征表 -> 排序表 -> 结论句`

Do not force a snippet onto a mismatched high-risk structure such as threshold-time, repeated-measure mixed-effects, or custom classification without checking fit first.

## Minimal Contest Project Layout

Use a case-specific working folder such as:

```text
scratch/<case_name>/
├── data_raw/
├── data_clean/
├── artifacts/
├── figures/
├── final_answer_artifacts/
├── paper/
├── tables/
├── logs/
├── run_problem1.py
├── run_problem2.py
└── utils.py
```

Keep:

- raw inputs untouched
- clean intermediate tables saved explicitly
- final tables and figures separated from temporary artifacts

## Generic Python Skeleton

```python
from pathlib import Path
import pandas as pd

ROOT = Path("scratch/case_name")
RAW = ROOT / "data_raw"
CLEAN = ROOT / "data_clean"
TABLES = ROOT / "tables"
FIGURES = ROOT / "figures"
ARTIFACTS = ROOT / "artifacts"
FINAL = ROOT / "final_answer_artifacts"

for p in [CLEAN, TABLES, FIGURES, ARTIFACTS, FINAL]:
    p.mkdir(parents=True, exist_ok=True)


def load_inputs():
    # Replace with the contest-specific files
    df = pd.read_excel(RAW / "input.xlsx")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Add grain alignment, missing-value handling, and feature construction here
    out = df.copy()
    return out


def save_table(df: pd.DataFrame, name: str) -> None:
    df.to_csv(TABLES / f"{name}.csv", index=False)
```

## Preprocessing Skeleton

Use an explicit preprocessing function or script. Do not hide cleaning logic inside the model code.

```python
def build_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    # 1. Align keys and time grain
    # 2. Separate structural zeros from missing values
    # 3. Normalize units
    # 4. Aggregate if needed
    # 5. Construct features used by the model
    return out
```

Save important intermediates:

- cleaned master table
- aggregated decision table
- feature table
- parameter table for optimization
- repeated-measure summary table if the same object/person appears multiple times
- final recommendation table if the question ends in a decision or grouped scheme
- abstract material pool or result note file once stable outputs appear

## Common Contest Script Organization

Split by task role, not by random utility growth:

- `run_problem1.py` for the first deliverable
- `run_problem2.py` for the second deliverable
- `utils.py` for shared helpers
- optional `validation.py` when robustness work is non-trivial

If the task is combined, let upstream outputs become saved inputs for downstream scripts.

## Result Export Skeleton

```python
def export_result(df: pd.DataFrame, filename: str) -> None:
    path = TABLES / filename
    if filename.endswith(".xlsx"):
        df.to_excel(path, index=False)
    else:
        df.to_csv(path, index=False)
```

## Minimum Path From Plan To First Deliverable

Use this order when time is tight:

1. load inputs
2. clean and align
3. save one clean table
4. run one baseline
5. export one result table
6. export one `final_answer_artifact` draft
7. only then decide whether to refine the model

If step 5 or 6 is still missing, do not keep polishing the model.

If a matching snippet exists, adapt it and export the first table before building a custom version. If a matching schema exists, define the target columns before step 5. After step 6, run `scripts/deliverable_lint.py`. Paper and abstract review is semantic and follows `references/paper-writing.md`; it is not a code-stage field-completeness check.

Always export:

- the final answer table
- the main intermediate table that justifies it
- a short validation summary table
- a final-answer artifact copy in a dedicated folder when the question is recommendation / ranking / judgment heavy

Prefer filenames that show their contest role clearly, for example:

- `problem2_recommendation_table.csv`
- `problem3_group_boundary_table.csv`
- `problem4_prediction_table.csv`
- `problem1_validation_summary.csv`
- `problem2_final_recommendation_table.xlsx`

If the prompt includes an official workbook or appendix:

- create the target schema first
- keep an export path for the template-ready file such as `.xlsx`
- do not wait until the end to decide the row/column layout

## Plot Output Skeleton

```python
import matplotlib.pyplot as plt


def save_line_plot(x, y, title, xlabel, ylabel, filename):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, y, linewidth=2)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGURES / filename, dpi=300)
    plt.close(fig)
```

Use deterministic filenames so figures can be cited consistently in the paper draft.

## Validation Skeleton

```python
def compare_with_baseline(current_metric, baseline_metric):
    return {
        "current": current_metric,
        "baseline": baseline_metric,
        "delta": current_metric - baseline_metric,
    }


def perturb_parameter(run_fn, base_value, ratios):
    rows = []
    for r in ratios:
        value = base_value * (1 + r)
        result = run_fn(value)
        rows.append({"ratio": r, "value": value, "result": result})
    return pd.DataFrame(rows)
```

Always save validation outputs separately from the final answer table.

If the question is decision-heavy, also save one compact answer table that could be inserted into the paper with minimal rewriting.

If the question is template-heavy, save both:

- the full template-ready workbook output
- a compact summary table for the main text

## Implementation Order

Follow this order unless the task has a compelling reason not to:

1. Read and inspect
2. Clean and align
3. Save the clean table
4. Run the baseline
5. Export the baseline result
6. Add validation
7. Add backup or advanced model if still needed

For simple or low-risk questions, do not delay step 5 waiting for a backup route.

## High-Frequency Coding Mistakes To Avoid

- Mixing raw data cleaning with model solving
- Overwriting raw inputs
- Failing to save the intermediate table used for the final decision
- No fixed output directory structure
- Hard-coding unexplained constants with no comments
- Writing a giant single script for all questions
- Producing figures without saving the underlying summary data

If the implementation cannot be rerun from raw input to final table cleanly, the contest workflow is too fragile.
