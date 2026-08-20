# 图表准备冻结输入：{{FREEZE_ID}}

> 本文记录 F0 之后图表准备支线看到的输入边界。以下问题是最低责任，不是字段白名单；语义解释、例外和未决争议必须保留在 Markdown，不得压缩成限定死的 JSON。

## 冻结身份

- 题目/运行：{{TITLE_AND_RUN}}
- 冻结时间与 Leader：{{FREEZE_TIME_AND_LEADER}}
- source snapshot / manifest：{{SOURCE_SNAPSHOT}}
- 图表准备支线版本：{{FIGURE_PREP_VERSION}}
- 上游停止点：`validation/validation-handoff.md`（或明确的替代交接）：{{UPSTREAM_HANDOFF}}

## 允许使用的验证与结果

链接并解释当前授权的 `validation-handoff`、`claim-evidence-map`、逐问结果表、接口和限制；说明它们各自的版本、run、代码/config、数据版本和适用范围。

## 逐问冻结清单

按问题或共享结果单元说明：

- 允许使用的结果对象、来源路径和版本；
- 主键、粒度、字段、单位、时间窗、样本量、误差/区间、缺失和可行性状态；
- 可直接支持的 claim 与禁止/有条件支持的表述；
- 允许生成诊断证据的位置和允许导出的数据根目录。

可使用表格帮助索引，但表格不是语义输出上限。

## 禁止读取、禁止使用与保留版本

列出未授权的旧 run、被替换结果、未验证候选、已暴露 holdout、其他 Agent 的私密报告和任何不能支持当前 claim 的数据。说明它们为何不能作为论文图来源；旧版本只保留，不删除。

## 题间接口与共享单元

说明跨问共享结果的 producer、consumer、版本、粒度、单位、时间和失效传播。标出哪些共享对象只允许由 shared curator 处理，避免多个 question curator 争写。

## 章节地图接口

记录 CP1 产生的 `paper-prep/structure/chapter-map-v0.md` 的精确路径、哈希、版本和提供时点。若尚未提供，明确标记为 F3 阻塞项；Curator 可以继续完成 F1/F2R，但 Integrator 不得自行生成章节结构或进入最终交接。

## 冻结变更规则

冻结后发现结果、数据、模型或验证口径需要改变时，只能通过 `change-request.md` 请求 Leader 裁决；不得在图表准备目录中静默换源。记录允许的局部补充及其新版本。

## 开放发现与停止

保留冻结时尚未归类但会影响图表、claim 或论文叙事的新发现，并说明本冻结只授权诊断、数据整理和图表建议，不授权正式论文图绘制、视觉审美评价或论文正文改写。
