# Problem Typing

Serves `SKILL.md` Step 2: type each subproblem before choosing models.

Call this file when:

- You just received a contest problem.
- You need to classify one question quickly.
- You are unsure whether a question is single-type or combined.

## Fast Output Format

For each subproblem, write:

`objective -> deliverable -> primary type -> secondary type (if any) -> dependency -> key data shape`

Do not choose models until this line is clear.

## Type Definitions And Boundaries

| Type | What the question really wants | Typical deliverable | Strong signals | Common data shape | Easy confusion |
| --- | --- | --- | --- | --- | --- |
| Evaluation/ranking | Score, sort, screen, prioritize objects | Top-k list, score table, importance ranking | “最重要”, “综合评价”, “排序”, “筛选”, “优先选择” | Multi-object, multi-index, panel or feature table | Classification, clustering |
| Prediction | Estimate future values or future threshold time | Forecast table, predicted curve, future date/week | “未来”, “预测”, “预期”, “趋势”, “最早达标时间” | Time series, panel time series, repeated measurements | Optimization |
| Optimization/decision | Produce the best plan under constraints | Plan table, schedule, allocation, pricing, grouping strategy | “最优”, “方案”, “策略”, “在约束下”, “收益最大/成本最小” | Decision variables plus explicit constraints | Evaluation |
| Classification/clustering | Assign labels or divide into groups | Class label, abnormal/normal result, subgroup result | “分类”, “判定”, “聚类”, “分组”, “亚类”, “异常识别” | High-dimensional features, may or may not have labels | Evaluation |
| Statistical analysis/correlation | Describe distributions, patterns, relations | Distribution summary, correlation matrix, significance result | “分布规律”, “相关关系”, “显著性”, “影响因素” | Descriptive tables, pairwise relations, grouped data | Mechanism explanation |
| Process/mechanism explanation | Explain how a process evolves or why a threshold is reached | Relation model, mechanism statement, growth/threshold explanation | “关系模型”, “影响机制”, “达标过程”, “变化过程” | Repeated measurements, grouped observations, hierarchical data | Prediction |
| Combined problem | Chain several task types into one workflow | Multiple linked outputs | “参考问题一”, “在问题二基础上”, multi-question dependency | Mixed | “Several unrelated small questions” |

## Fast Signal Rules

Use these rules in order:

1. Look at the required output.
   - Ranking list -> evaluation
   - Future value -> prediction
   - Schedule/plan/strategy -> optimization
   - Label/group/abnormality -> classification
   - Relation/significance/distribution -> statistical or mechanism

2. Look at the verbs.
   - “确定/制定/优化” usually signals decision.
   - “预测/估计” usually signals prediction.
   - “分析规律/相关性” usually signals statistical analysis.
   - “判定/分类/识别” usually signals classification.

3. Look at dependency wording.
   - If Question 2 depends on Question 1 output, it is almost always combined.

## High-Risk Signals To Flag Before Choosing Models

These are not separate types, but they must be detected during typing because they change the safe modeling route.

- Repeated measurements / hierarchical structure:
  - signals: same object/person appears multiple times, multiple tests per case, panel-like repeated observations
  - implication: mechanism/statistical and threshold-time questions should not be solved as plain i.i.d. rows
- Proxy label / surrogate target / indirect criterion:
  - signals: the target column is a screening result, expert rule, operational status, observed sales used as demand proxy, or recent indicator used in place of the true future quantity
  - implication: the route must state what is being approximated, and validation must match that boundary instead of pretending the proxy is the full truth
- Threshold-time deliverable:
  - signals: “最早达标时间”, “何时达到阈值”, “最佳检测时点”
  - implication: this is usually a combined chain of process/threshold prediction upstream and decision downstream, not a plain regression task

## Easy-To-Mix Pairs

### Evaluation vs Classification

- Choose evaluation if the output is ordered importance, score, or priority.
- Choose classification if the output is a class label or abnormal/normal boundary.

### Prediction vs Optimization

- Choose prediction if the output is a future value.
- Choose optimization if the output is a plan based on future values.
- If both appear, type it as combined:
  - prediction upstream
  - optimization downstream

### Statistical Analysis vs Mechanism Explanation

- Choose statistical analysis if the task stops at “what patterns exist”.
- Choose mechanism/process if the task asks “how/why the variable changes” or needs interpretable structural relations.

### Clustering vs Classification

- Choose clustering if there are no labels and the task is exploratory grouping.
- Choose classification if there are labels, standards, or a clear判定目标.

## How To Detect A Combined Problem

Mark the question as combined when at least one of these is true:

- The question explicitly depends on an earlier question.
- The output requires both a descriptive module and a decision module.
- The decision needs predicted values, screened candidates, or grouped objects first.
- The writing naturally forms “analyze first, decide second”.

Common contest-safe combined chains:

- Evaluation -> optimization
- Statistical analysis -> prediction -> optimization
- Mechanism explanation -> grouping -> timing/strategy optimization
- Statistical analysis -> feature screening -> classification

## 60-Second Typing Checklist

Before selecting a model, answer these yes/no questions:

1. Do I know the final deliverable for this question?
2. Do I know whether the task ends at analysis or must produce a plan/label?
3. Do I know whether this question depends on earlier outputs?
4. Do I know the data grain needed to answer it?
5. Do I know the primary type?
6. If mixed, do I know which module is upstream and which is downstream?
7. Have I flagged repeated measurements, proxy labels, or threshold-time structure if they exist?

If any answer is “no”, keep typing the problem. Do not jump to models.
