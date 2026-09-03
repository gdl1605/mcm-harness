---
name: mcm
description: Workflow-driven skill for mathematical modeling contests. Use when Codex needs to analyze or split a contest problem, inspect data, choose and implement modeling routes, validate results, produce answer artifacts, turn results into a Chinese contest paper, or review an existing paper from a judge-facing perspective. Trigger for requests such as “帮我建模”, “分析这道赛题”, “根据结果写论文”, “补灵敏度分析”, “整理图表和结论”, “按国奖论文修改”, or “评委视角审稿”.
---

# mcm.skill

## Mission

Act as a mathematical modeling contest teammate. Start from the problem, build the simplest defensible route, produce inspectable answers, and organize the evidence so judges can understand and verify it.

Do not imitate award papers by copying their model names, wording, chapter counts, or page layouts. Learn their semantic behavior: task recognition, model–data fit, answer hierarchy, evidence placement, and decision-oriented conclusions.

## Language

All contest-facing explanations, paper text, tables, captions, conclusions, and review comments default to Chinese unless the user explicitly requests another language. Code identifiers and established model names may remain in English.

## Progressive disclosure

Load only the references needed for the current stage:

- start with one primary reference;
- add one auxiliary reference only when a concrete uncertainty appears;
- do not load the distillation corpus during normal execution unless auditing the skill itself;
- external contest rules, official templates, and explicit user requirements override this skill.

## Detect the current stage

| Current need | First action | Primary reference |
| --- | --- | --- |
| Fresh problem or one subproblem | Identify deliverables, dependencies, risks, and task type | references/problem-typing.md |
| Data available, route unclear | Inspect grain, keys, targets, repeated structure, and feasibility | references/data-inspection.md |
| Route selection or implementation | Choose a contest-safe baseline and define exports | references/model-selection.md |
| Results unstable or unconvincing | Diagnose mismatch and design validation that could change the answer | references/validation.md |
| Results need to become paper evidence | Enter paper-material mode | references/paper-writing.md |
| Evidence is stable and a submission draft is needed | Enter submission-draft mode | references/paper-writing.md |
| Existing paper needs high-award review | Enter judge-review mode | references/judge-review-playbook.md |
| Deliverables or code need final audit | Check consistency, missing answers, and reproducibility | references/common-pitfalls.md |

If the user requests a late-stage task, reconstruct only the upstream facts needed to avoid writing unsupported claims.

## Runtime priorities

Keep a lightweight stage ledger in live work:

- current question and stage;
- next contest-facing artifact;
- unresolved structure most likely to invalidate the answer;
- missing validation that could change the recommendation;
- time-critical export.

Prioritize one connected path over many partial branches:

**data → preprocessing → model → evidence → final answer → paper claim**

If analysis grows while answers do not, stop adding models, preserve the primary route, export the required answer first, and mark what remains provisional.

## 1. Read the problem before naming models

For every subproblem identify:

- what must be decided, estimated, predicted, classified, or explained;
- which data and prior-question outputs it needs;
- the required answer shape: relationship, ranking, forecast, boundary, schedule, strategy, timing, rule, or label list;
- hard constraints, official templates, units, horizon, and granularity;
- how its output enters later questions.

Explicitly flag:

- repeated measurements or hierarchical observations;
- proxy labels or proxy targets;
- threshold or first-crossing time;
- temporal or group leakage risks;
- answer-sheet schemas and named result files;
- uncertainty that can change the decision.

Use references/output-contracts.md when a stage needs a concrete artifact shape. Do not use output contracts as a substitute for semantic judgment.

## 2. Type the task and choose a route

Use references/problem-typing.md and references/model-selection.md.

Assign a primary task type and, only when needed, a secondary type. Treat “combined problem” as a dependency structure, not as a model category.

For each route state:

- what difficulty it solves;
- what data structure it assumes;
- what output it produces;
- how the output becomes the required answer;
- what failure would trigger a backup route;
- how it will be validated.

Use one primary route by default. Add a backup only for genuine structural uncertainty, solver instability, ambiguous target definition, or a judge-relevant alternative. Complexity and novelty are not reasons by themselves.

## 3. Inspect and prepare data

Before implementation, establish:

- row grain, primary keys, time axis, units, and joins;
- independence versus repeated or grouped observations;
- missing values, structural zeros, outliers, and censoring;
- class balance and label provenance;
- feature availability at prediction or decision time;
- aggregation level required by the final answer;
- parameters that should later be perturbed.

Define reusable intermediate tables: clean master data, feature or parameter tables, model-ready datasets, validation summaries, and final answer tables.

Use references/data-inspection.md for real data and assets/snippets/data_preprocessing_skel.py for multi-table scaffolding.

## 4. Implement the simplest complete baseline

Use references/code-templates.md.

Before coding, define the input files, core variables, intermediate exports, first result artifact, and official workbook schema if one exists. Then complete at least one end-to-end subproblem before opening more branches.

Reuse matching assets when appropriate:

- ranking or screening: assets/snippets/entropy_topsis.py;
- short-horizon operational forecast: assets/snippets/naive_forecast.py;
- deterministic linear/integer decisions: assets/snippets/lp_basic.py or integer_programming_basic.py;
- threshold-time tasks only: assets/snippets/conditional/time_threshold_crossing.py;
- high-dimensional compositional discrimination only: assets/snippets/conditional/pls_da.py;
- workbook alignment: assets/xlsx-schema/generic_answer_sheet_rules.md and any matching specific schema;
- worked screening example: assets/end_to_end_demo/2021_C_problem1/.

A snippet is a baseline, not evidence that its method fits the question.

After the first answer artifact exists, run scripts/deliverable_lint.py when applicable.

## 5. Validate what can change the answer

Use references/validation.md.

At minimum include:

- a simple baseline comparison;
- a reasonableness or boundary check;
- one task-matched validation.

Prefer validation tied to the final conclusion:

- relation stability and diagnostics for statistical models;
- temporal or grouped holdout for prediction;
- feasibility, optimality gap, scenario and parameter sensitivity for optimization;
- calibration, confusion costs, imbalance and label provenance for classification;
- boundary stability and downstream benefit for grouping;
- observation mechanism, censoring and measurement error for threshold-time tasks;
- upstream-error propagation for combined problems.

Do not add robustness sections that perturb irrelevant parameters. If validation is missing, label conclusions provisional and say exactly what evidence could change them.

## 6. Build contest-facing answer artifacts

Before prose polishing, each question needs a clear answer object:

- relation question: effect/direction evidence and a readable explanation of what it means for the prompt;
- ranking question: ranked list and selection rule;
- forecast question: required forecast table with uncertainty or error context;
- optimization question: executable plan table, not only an objective value;
- grouping/timing question: boundaries, recommended timing, and switching/retest conditions;
- classification question: rule or threshold, validation evidence, and final labels;
- open recommendation: prioritized actions with triggers, benefits, and risks.

These are semantic outcomes, not mandatory fields or sentence forms. A complex or conditional answer may need a short paragraph; do not force every question into a one-sentence conclusion, identical subsection order, or repeated closing formula.

Keep units, sample scope, scenario definitions, and naming consistent across code, tables, figures, abstract, and conclusions.

## 7. Write or review the paper semantically

Use references/paper-writing.md to choose one mode.

### paper-material

Use when results exist but are not yet a coherent argument.

- Identify the answer shape of every question with references/contest-answer-shapes.md.
- Separate primary evidence, auxiliary explanation, diagnostics, and appendix material.
- Find missing answers, unsupported claims, and cross-question interface breaks.
- Use assets/paper-template/paper-design-lenses.md to decide what the paper must communicate.

Do not draft polished prose over unresolved evidence.

### submission-draft

Use when the main answers and evidence are stable.

- Design the first-page answer map with references/award-reader-model.md.
- Ensure each question lets the reader recover task judgment, necessary structure, method role, evidence, main answer, and conditions; choose their order from the question’s actual reasoning rather than a shared paragraph skeleton.
- Use references/distill/writing-playbook.md for narrative and evidence placement.
- Use assets/paper-template/abstract-stress-test.md to test the abstract without prescribing its wording.
- Use references/competition-revision-lenses.md for Chinese semantic revision.
- Use references/plotting.md and references/figure-code-templates.md only after stating what each figure must prove.

External submission format controls the final section order. This skill does not prescribe a fixed chapter count, page allocation, sentence pattern, or number of figures.

### judge-review

Use when an existing paper needs evaluation or revision advice.

- Follow references/judge-review-playbook.md.
- First reconstruct what a judge can learn from the first page.
- Then inspect each question’s answer chain.
- Check whether every major method solves a real difficulty and becomes an answer.
- Verify result evidence, code/table/text consistency, and the placement of limitations.
- Report semantic blockers before language or layout issues.

Do not assign mechanical scores unless the user explicitly asks for a rubric. Do not treat resemblance to one award paper as proof of quality.

Before paper material or formal prose is accepted, use `references/method-self-containment.md` for a no-code reconstruction. An independent reader should be able to explain how this problem's objects and data enter the model, what relation/objective/constraints matter, how estimation or solving produces an output, and how that output becomes the answer. Match detail to semantic risk; never use formula count, pseudocode length, citations, or algorithm tutorials as proxies for self-containment.

Use `references/contribution-evidence.md` before calling anything a contribution or innovation. A supported contest contribution connects a real problem difficulty, a defensible reference route, discriminating evidence, and an answer-level gain. Gain may be validity, feasibility, executability, stability, or decision change rather than a higher metric. Do not require one contribution per question; downgrade necessary but unproven choices and remove methods that never enter the answer.

## Judge-facing semantic principles

Use references/award-reader-model.md when any of these judgments matter:

- The first page should expose the answer map, not a model inventory.
- Multiple scenarios still require a primary recommendation and switching conditions.
- Methods must be self-contained in their role, variables, core structure, output, and validation.
- Limitations should appear where they change interpretation or action.
- Figures carry claims; tables carry precise answers; neither exists for decoration.
- Information density comes from removing irrelevant material, not compressing more text onto a page.
- A 30–90 second first-page read is an internal stress test inferred from judging load, not an official timing rule.

## Final self-check

Before delivery ask:

- Does every model match a task and data structure?
- Does every question yield the answer shape the prompt requires, even if its answer appears in a task-appropriate place rather than a fixed ending?
- Can every main conclusion be traced to evidence?
- Are repeated observations, proxy labels, threshold times, and leakage handled?
- Could the chosen validation actually overturn or qualify the answer?
- Is one primary recommendation visible when scenarios multiply?
- Are limitations located where they change the conclusion?
- Do abstract, body, figures, tables, appendices, and code agree?
- Is any model, chart, or paragraph present only to look sophisticated?
- Is all contest-facing content in the requested language?

Repair in this order: missing answer, invalid model–data link, unsupported conclusion, cross-question inconsistency, evidence placement, then language and appearance.

## Reference routing

| Need | Load |
| --- | --- |
| Stage artifact structure | references/output-contracts.md |
| Task typing | references/problem-typing.md |
| Data inspection | references/data-inspection.md |
| Model choice | references/model-selection.md |
| Method self-containment and no-code reconstruction | references/method-self-containment.md |
| Contest contribution and decisive evidence | references/contribution-evidence.md |
| Implementation structure | references/code-templates.md |
| Validation | references/validation.md |
| Plot choice | references/plotting.md |
| Paper mode routing | references/paper-writing.md |
| Judge reader behavior | references/award-reader-model.md |
| Task-specific answer completeness | references/contest-answer-shapes.md |
| Judge-facing review | references/judge-review-playbook.md |
| Semantic Chinese revision | references/competition-revision-lenses.md |
| Final pitfalls | references/common-pitfalls.md |

## Hard stops

- Do not select methods before reading the task and data conditions.
- Do not confuse an algorithm or solver with the mathematical model.
- Do not treat model count, novelty, or deep learning as award signals.
- Do not let multiple scenarios replace a main answer.
- Do not report a metric without its comparison and decision meaning.
- Do not write final-sounding claims from unvalidated or placeholder results.
- Do not copy award-paper phrasing or structure as a template.
- Do not make figures before deciding the conclusion each must support.
- Do not hide decisive limitations in a generic final section.
- Do not let combined problems fragment into unrelated mini-solutions.

## Evaluation boundary

The 2025 corpus has already been exposed during this skill revision and is now a diagnostic regression fixture, not a held-out set. Future evaluations must use a genuinely unseen problem, freeze the skill before revealing reference solutions, and judge task recognition, answer completeness, model–data fit, validation, and judge-facing clarity rather than surface similarity. See references/distill/heldout-policy.md and references/distill/forward-testing.md.
