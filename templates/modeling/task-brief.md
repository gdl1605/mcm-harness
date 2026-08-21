# 建模 Task Brief：{{TASK_TITLE}}

> 下列问题是本角色最低责任，不是字段白名单或输出上限。发现更高影响的数学、数据、计算、接口或回滚问题时，请改变章节结构并完整展开。

## 运行、问题与角色

- Run / source snapshot：{{RUN_AND_SNAPSHOT}}
- 阶段 / 问题或共享构建单元：{{PHASE_AND_BUILD_UNIT}}
- Role / 原 Agent 句柄：{{ROLE_AND_AGENT_HANDLE}}
- 当前 build contract / 分支 / 父运行：{{CONTRACT_BRANCH_PARENT_RUN}}
- 当前数据、代码与接口版本：{{DATA_CODE_INTERFACE_VERSIONS}}
- 候选模型汇报与真实人工决定：{{MODEL_CANDIDATE_BRIEFING_AND_HUMAN_DECISION}}

## 输入与隔离

- 允许读取：{{ALLOWED_INPUTS}}
- 为保持独立必须隐藏：{{HIDDEN_CONTEXT}}
- 允许使用的开发反馈：{{DEVELOPMENT_FEEDBACK}}
- 不得打开的保留信息：{{RESERVED_INFORMATION}}

## 写入与所有权

- 唯一主 Markdown 输出：{{UNIQUE_MARKDOWN_OUTPUT}}
- 允许额外写入的工程路径：{{ALLOWED_ENGINEERING_WRITES}}
- 当前问题/共享内核/接口 owner：{{OWNERSHIP}}
- 禁止修改：{{FORBIDDEN_WRITES}}

## 本轮唯一目标

{{TASK_GOAL}}

## 最低责任问题

### A. 对象与当前主张

{{QUESTION_A}}

### B. 证据、实现或运行责任

{{QUESTION_B}}

### C. 竞争解释、失败机制与影响

{{QUESTION_C}}

### D. 区分动作、接口与回滚

{{QUESTION_D}}

## 调整权限、预算与停止

- 当前允许的 L0/L1/L2/L3 权限：{{ADJUSTMENT_AUTHORITY}}
- 人工授权的模型边界与重开 H1 条件：{{HUMAN_AUTHORIZED_MODEL_BOUNDARY}}
- 活跃主/挑战分支：{{ACTIVE_BRANCHES}}
- 时间与计算预算：{{BUDGET}}
- 停止条件与升级方向：{{STOP_AND_ESCALATION}}

## 开放发现

报告任务未预见、但会改变题意、路线、数据、模型结构、评价口径、题间接口、失效传播或后续验证的内容。不要只返回 JSON、勾选表或 ID 列表。
