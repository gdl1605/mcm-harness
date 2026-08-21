# 图表准备 Task Brief：{{TASK_TITLE}}

> 下列问题是本角色的最低责任，不是字段白名单、固定 schema 或输出上限。语义内容必须继续写在开放 Markdown 中；不得为了满足模板而省略会改变数据、主张、论文位置、题间接口或回滚路径的新发现。

## 阶段、问题与角色

- 阶段：{{FIGURE_PREPARATION_STAGE}}
- 题目/问题/共享结果单元：{{QUESTION_OR_SHARED_UNIT}}
- 角色与 Agent 句柄：{{ROLE_AND_AGENT_HANDLE}}
- 当前目标：{{TASK_GOAL}}
- 父运行、分支和输入冻结版本：{{PARENT_RUN_BRANCH_FREEZE}}

## 允许读取与隔离

- 允许读取的题意、验证交接、claim、结果、run、数据和章节材料：{{ALLOWED_INPUTS}}
- 为保持独立必须隐藏的报告、判断、保留信息和未授权版本：{{HIDDEN_CONTEXT}}
- 已允许使用的开发反馈或变更决定：{{AUTHORIZED_FEEDBACK}}
- 不得把诊断图、旧 run 或未授权候选当作论文图来源：{{FORBIDDEN_CANDIDATES}}

## 唯一主输出与写入权

- 唯一主 Markdown 输出：{{UNIQUE_MARKDOWN_OUTPUT}}
- 允许额外写入的路径：{{ALLOWED_WRITES}}
- 禁止修改：`data/`、`modeling/`、`validation/`、论文正文和其他 Agent 的产物，除非 Leader 明确授权：{{EXCEPTIONS}}
- 版本、哈希、旧文件和失败产物的保留方式：{{VERSION_POLICY}}

## 最低责任问题

### A. 结果、数据与主张

说明本轮使用的结果对象、字段、主键、粒度、单位、时间范围、误差/区间、缺失和可行性状态，以及它们支持的精确 claim。

### B. 诊断或图表准备任务

说明需要检查、导出或推荐什么，为什么有助于读者理解；若认为没有必要作图，说明理由而不是强行制造候选。

### C. 竞争解释、过度表达与限制

说明哪些观察只是诊断线索、哪些结论有授权，列出可能误导的图型、缺失信息、外推边界和不可支持的表达。

### D. 区分动作、审查与回滚

说明如何复算数据、如何请求独立复核、什么发现应写 change request，以及什么情形必须返回数据/建模/验证上游。

## 停止与升级

- 本角色可以完成的范围：{{ROLE_BOUNDARY}}
- 需要 Leader 裁决的高影响问题：{{LEADER_ESCALATION}}
- 停止条件：{{STOP_CONDITIONS}}
- 未预见但会改变题意、数据、模型、验证、图表授权或论文叙事的新发现：{{OPEN_DISCOVERIES}}

## 明确不在本任务内

本任务不要求生成正式论文图、选择最终美术风格、制作样式文件、进行审美/视觉评分或修改论文正文。正式绘图由 FR0–FR4 消费后续交接包完成。
