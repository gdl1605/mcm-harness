# 论文准备 Task Brief：{{TASK_TITLE}}

> 下列问题是最低责任，不是字段白名单或输出上限。发现会改变答题、证据、章节、篇幅、题间接口或回滚范围的新内容时必须继续报告。

## 身份与目标

- 阶段/角色/Agent 句柄：{{PHASE_ROLE_AGENT}}
- 问题或全篇单元：{{UNIT}}
- 唯一目标与停止条件：{{GOAL_AND_STOP}}
- 父 run、冻结版本和当前材料版本：{{PARENT_AND_VERSION}}

## 上下文隔离

- 允许读取：{{ALLOWED_INPUTS}}
- 禁止上下文：{{FORBIDDEN_CONTEXT}}
- 本轮新暴露信息：{{NEWLY_EXPOSED_CONTEXT}}
- 国奖蒸馏是否允许：{{AWARD_DISTILLATION_ACCESS}}

## 写入权与版本

- 唯一主输出：{{PRIMARY_OUTPUT}}
- 额外允许写入：{{ALLOWED_WRITES}}
- 永久只读目录：`data/`、`modeling/`、`validation/`、`figure-prep/` 和其他 owner 目录：{{EXCEPTIONS}}
- 旧版保留与回滚：{{VERSION_POLICY}}

## 最低责任 A/B/C/D

- A：本轮必须确认的答题或结构对象是什么？
- B：证据、公式、结果、章节或竞赛表达需要完成什么？
- C：有哪些竞争解释、限制、禁止表达和读者风险？
- D：怎样复核、谁能修订、什么情况应上游重开？

## 任务之外的新发现

{{OPEN_DISCOVERIES}}

本任务不生成完整论文、正式图片、排版、审美评分、参考文献检索结果或提交包。
