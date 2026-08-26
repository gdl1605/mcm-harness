# Common Pitfalls

Serves `SKILL.md` Step 9: self-check and repair weak contest solutions.

Call this file when:

- You think the answer is “almost done”.
- You need a final audit of model, validation, plots, and writing.
- The result looks busy but not convincing.

## Read-The-Problem Failures

| Symptom | Why it hurts | Fix now |
| --- | --- | --- |
| You cannot state the required deliverable clearly | Model choice will drift | Rewrite each question as objective + deliverable + constraints |
| You ignored required output templates or spreadsheets | Final answer may be unusable | Identify mandatory output files before solving |
| You treated linked questions as independent | Later questions lose upstream inputs | Rebuild the dependency chain |

## Typing Failures

| Symptom | Why it hurts | Fix now |
| --- | --- | --- |
| You picked a model before naming the task type | The route may not match the prompt | Re-type the question first |
| You marked a decision problem as pure prediction | No executable plan will be produced | Split forecast and decision layers |
| You used clustering where the task needs ranking or labels | Output target is wrong | Rebuild the route around the actual deliverable |
| You missed repeated measurements, proxy labels, or threshold-time structure during typing | The whole route may drift early | Re-type the question with those high-risk signals flagged |
| You saw a template workbook or appendix table but did not lock its schema early | The final answer may not fit the required format | Define the answer-sheet shape before modeling |
| You treated an open recommendation problem as free discussion | The answer becomes hard to grade quickly | Convert it into a prioritized final table or checklist |

## Model-Selection Failures

| Symptom | Why it hurts | Fix now |
| --- | --- | --- |
| A high-risk question has no backup path | No fallback if assumptions fail | Add a backup path with risks and validation |
| A simple low-risk question is forced to carry a decorative backup path | It wastes contest time and increases explanation burden | Keep the primary path and state why backup is unnecessary |
| The algorithm is named but variables/constraints are missing | The method is not defendable | Write the mathematical structure first |
| The chosen route looks advanced but is hard to explain | Judges will not reward opacity | Downgrade to a clearer baseline unless complexity is necessary |
| A timing/decision problem has no final recommendation table | The answer feels unfinished | Export the final scheme, boundary, or timing table explicitly |
| Every question has ideas but none has a full end-to-end path | The whole solution remains fragile | Finish one complete subproblem path before opening new branches |

## Execution And Output-Contract Failures

| Symptom | Why it hurts | Fix now |
| --- | --- | --- |
| The solution stays at planning level and no result table has been exported | There is nothing concrete to validate or write from | Run the baseline and export the first result table immediately |
| Each step is “explained” but not structured | Teammates cannot tell whether the work is actually complete | Rewrite the output as tables, cards, or numbered checklists |
| There is no final answer artifact | The work looks thoughtful but not submit-ready | Build the recommendation / ranking / judgment table first |
| Contest-facing output drifts into English or mixed language | The answer loses Chinese contest style and readability | Rewrite headings, explanations, captions, and conclusions in Chinese |

## Preprocessing Failures

| Symptom | Why it hurts | Fix now |
| --- | --- | --- |
| Data grain is unclear | Aggregations and constraints will misalign | Define key, unit, and time grain explicitly |
| Structural zeros are treated as missing values | Rankings and classifiers become distorted | Recode zero vs missing correctly |
| Feature construction is absent in ranking/classification tasks | The model has little to work with | Build stable, interpretable features first |
| Repeated observations are treated as independent samples | Significance and model fit become misleading | Add grouped handling, grouped summaries, or repeated-measure diagnostics |
| Proxy labels are used as if they were final truth | Classifier claims become overstated | State the target provenance and validate against that boundary |
| Surrogate targets or indirect criteria are treated as the full true objective | Forecast and decision claims become overstated | State what is proxied and keep the interpretation conservative |

## Validation Failures

| Symptom | Why it hurts | Fix now |
| --- | --- | --- |
| No baseline comparison | Improvement claims are weak | Add the simplest defensible baseline now |
| No sensitivity or perturbation check | The answer may be brittle | Perturb the key parameters and record change |
| Statistical claims lack diagnostics | Interpretive claims lose credibility | Add significance or fit diagnostics |
| Decision output has no feasibility check | “Optimal” may be unusable | Recheck constraints and edge cases |

## Plotting And Result-Presentation Failures

| Symptom | Why it hurts | Fix now |
| --- | --- | --- |
| A figure is present but not interpreted | It adds no score | Write the specific claim below it |
| Exact outputs are hidden in a figure | Judges cannot recover the answer | Add a table for the final values |
| Titles, labels, or units are missing | Visuals look unfinished | Standardize captions and axes |
| Too many plots show the same thing | The paper becomes noisy | Keep only visuals that support distinct claims |

## Writing Failures

| Symptom | Why it hurts | Fix now |
| --- | --- | --- |
| Abstract is only a task list | It does not show solving quality | Add methods, key results, and one strength sentence |
| Problem analysis is generic | The modeling route feels arbitrary | State why each question is typed the way it is |
| Results report numbers only | The paper does not answer the prompt clearly | Add interpretation and back-to-question sentences |
| Conclusion repeats the abstract | The ending feels empty | Summarize by question and decision implication |
| A decision/classification question ends with trends only | The paper reads like analysis notes, not a contest answer | Add one final recommendation or判定表 per question |
| An open recommendation question ends with prose only | The answer is hard to grade quickly | Convert it into a prioritized checklist or data-use table |
| The abstract is written at the very end with no material pool | It becomes vague and repetitive | Build a background-method-result-strength pool before drafting |
| The paper structure is treated as fixed even when the contest gives another format | The submission may violate the real requirement | Obey the external format first, then borrow the default paper structure |

## “Looks Busy But Scores Little” Failures

Use this list aggressively. These are common contest traps.

- Too many model names, too little task logic
- A complex algorithm used where a clean baseline would score better
- Polished code with weak explanation
- Many figures with no direct decision value
- Large appendices compensating for a weak main text
- Impressive metrics without a clear link to the contest deliverable
- A heavy model appears before a baseline decision rule or answer table exists

## Final Self-Check

Before you stop, answer these with “yes”:

1. Can I state the deliverable for every question in one line?
2. Is each question typed correctly?
3. Does each high-risk question have a backup path, or is the absence of backup justified?
4. Is preprocessing explicit and sufficient?
5. Is there at least one meaningful validation route?
6. Does each key figure or table support a specific claim?
7. Does the paper explain results instead of dumping them?
8. Have I removed anything that is only there to look advanced?
9. If repeated measurements or proxy labels exist, did I handle them explicitly?
10. Does each decision/classification question end with a clear answer table?
11. Has at least one question been fully completed end-to-end?
12. Is there an abstract material pool instead of a last-minute summary guess?
13. Are key stage outputs structured instead of being loose prose?
14. Are contest-facing outputs in Chinese unless the user explicitly asked for English?

If any answer is “no”, the solution still needs repair.
