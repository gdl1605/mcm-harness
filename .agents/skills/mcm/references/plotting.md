# Plotting And Result Presentation

Serves `SKILL.md` Step 7: map outputs to tables/figures and make the visuals support the written conclusion.

Call this file when:

- You need to choose between a figure and a table.
- You need to turn results into paper-ready visuals.
- You need to fix weak result presentation.

## Decide Figure vs Table First

Use a table when the reader needs exact values:

- Rankings
- Final plan matrices
- Parameter settings
- Group boundaries
- Recommended detection/intervention times
- Model comparison metrics
- Sensitivity summary values

Use a figure when the reader needs pattern recognition:

- Trends over time
- Seasonal changes
- Correlation structures
- Cluster separation
- Sensitivity curves
- Profit/risk trajectories
- Spatial or allocation heatmaps

If the result must both be submitted and explained, use both:

- Table for the final answer
- Figure for the pattern behind it

If the prompt includes an official workbook or appendix table, the template-shaped table takes priority over any optional figure.

## Stable Contest Plot Types

| Plot type | Best use |
| --- | --- |
| Line chart | Time trend, seasonal movement, profit or demand curves |
| Bar chart | Top-k comparison, contribution comparison, sensitivity ranking |
| Heatmap | Correlation matrix, allocation plan, multi-year strategy comparison |
| Scatter plot | Relation analysis, cluster separation, diagnostic inspection |
| Box plot | Distribution comparison across groups |
| Confusion-style matrix or error plot | Classification performance summary |

For decision-heavy questions, the stable pair is:

- one figure for the trend or risk pattern
- one table for the final recommended boundary / timing / scheme

For classification-heavy questions, the stable pair is:

- one confusion-style matrix or class-metric table
- one feature-importance or rule-summary visual/table

## Figure And Table Standards

For every figure or table, ensure:

- Numbering is consistent
- Title states object, scope, and time range where needed
- Units are shown
- Axes are labeled
- Legend is readable
- Color choices are functional, not decorative

For tables:

- Keep column names short and explicit
- Highlight only key values if needed
- Avoid oversized raw dumps in the main text

## How Visuals Must Connect To The Text

Write in this order:

1. Cite the figure or table by number.
2. State the pattern.
3. State the interpretation.
4. State why it matters for the question.

Example pattern:

- “As shown in Figure 4, demand peaks in …”
- “This indicates that …”
- “Therefore the replenishment plan should …”

Never leave a figure or table unexplained.

## Caption And Figure Language

Prefer captions that identify:

- What is shown
- Which objects are compared
- Which time or scenario is used

Prefer text such as:

- “Figure x shows…”
- “Table x reports…”
- “The heatmap indicates…”
- “The comparison suggests…”

Avoid:

- “See Figure x”
- “The figure is obvious”
- “The result is very good”

## Common Presentation Failures

- Using a figure when the contest needs exact final values
- Dumping a full spreadsheet into the main text
- Too many curves in one plot
- Missing units or labels
- Decorative colors with no analytical meaning
- Figure says one thing, text claims another
- Showing plots without saying what decision they support
- Only showing trend plots for a decision problem and forgetting the final recommendation table

## Quick Plotting Checklist

Before keeping a visual in the main text, ask:

1. Does it support a specific claim?
2. Would a table be clearer?
3. Is the caption informative enough to stand alone?
4. Are labels and units complete?
5. Is the explanation directly below or near the visual?

If any answer is “no”, fix the visual or move it to the appendix.
