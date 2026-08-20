# 全文图表计划：{{TITLE}}

> 本计划整合各问题的图表数据包与建议，决定“是否值得画、支持什么、放在哪里”，不生成正式论文图，也不规定审美样式。以下是最低责任，不是字段白名单或固定 JSON schema；整合时必须保留各原始 memo 的限制和争议。

## 计划身份与输入

- 题目、run、冻结版本：{{TITLE_RUN_FREEZE}}
- Integrator / Leader：{{INTEGRATOR_AND_LEADER}}
- 章节地图版本：{{CHAPTER_MAP_VERSION}}
- 输入 question package、review、response、change request：{{INPUT_INDEX}}

## Figure ID 与优先级

逐项列出核心、辅助、可选、暂缓和不建议作图的候选；每项链接数据 provenance、recommendation、claim、来源版本和 review。优先级必须说明基于什么阅读收益、证据稳定性或重复风险，而不是按图数量凑齐。

建议索引：

| Figure ID | 问题/claim | 数据包 | 推荐图型 | 逻辑论文位置 | 与表/图关系 | 状态 |
|---|---|---|---|---|---|---|
| {{FIGURE_ID}} | {{CLAIM}} | {{DATA_PACKAGE}} | {{RECOMMENDATION}} | {{LOCATION}} | {{RELATION}} | {{STATUS}} |

## 跨问组合、重复与冲突

说明哪些图可组合为同一叙事、哪些必须拆分、是否重复表达同一 claim、颜色/编码语义是否会冲突（仅记录语义一致性，不规定视觉样式），以及共享结果、单位、粒度和版本如何统一。

## 章节与正文关系

对每个保留候选写逻辑位置、正文引入句要回答什么、图后解释重点、相邻公式/表/诊断证据和下一段/下一问接口。不得用假设页码替代叙事位置。

## Caption、限制与禁止表述

汇总每个 Figure 的 caption 骨架、总体/时间、指标/单位、分组、误差/缺失/可行性和验证条件；明确不可从图中推出的因果、最优性、泛化、显著性或范围外结论。

## 未决事项与裁决

保留重复争议、缺失章节、未裁决 change request、需要用户决定的核心/辅助取舍和会阻止交接的问题。说明哪些已由 Leader 裁决、依据是什么。

## 交接准备与停止

确认每个保留 Figure 都有可复现数据包、来源版本、推荐、位置、caption 和 evidence review；缺失项列明负责人和路径。本计划完成后移交外部绘图模块，不在 harness 内绘图或做审美评分。
