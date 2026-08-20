# 数据工程 Task Brief：{{TASK_TITLE}}

> 下列问题是本角色的最低责任，不是字段白名单或输出上限。若发现更高影响的数据语义、风险、接口或回滚问题，请改变章节顺序并完整展开。

## 运行与隔离信息

- Run：{{RUN_ID}}
- Source snapshot：{{SOURCE_SNAPSHOT_ID}}
- 数据版本：{{DATA_VERSION_OR_PENDING}}
- Wave：{{WAVE}}
- Role：{{ROLE}}
- 唯一输出路径：{{OUTPUT_PATH}}
- 允许读取的原始材料：{{ALLOWED_SOURCES}}
- 允许读取的既有报告：{{ALLOWED_REPORTS}}
- 为保持独立性不得读取：{{HIDDEN_CONTEXT}}
- 允许修改的范围：{{WRITE_SCOPE}}

## 本轮目标

{{TASK_GOAL}}

## 最低责任问题

### A. 对象与口径

{{QUESTION_A}}

### B. 数据事实或实现责任

{{QUESTION_B}}

### C. 风险、反例与影响

{{QUESTION_C}}

### D. 复现、接口或回滚

{{QUESTION_D}}

## 必须保留的依据

尽量定位到题面、附件说明、文件、sheet、字段、代码、日志、数据版本或最小样例。明确区分已观察事实、推断、暂用处理和未知项。

## 开放发现

报告 brief 未预见、但会改变题意、路线、数据总体、处理方法、题间接口或下游可用性的内容。不要为了匹配 A–D 而删减发现，也不要只返回 JSON、勾选表或 ID 列表。

## 停止条件与禁止事项

{{STOP_CONDITION}}

本角色不得越权执行：{{FORBIDDEN_ACTIONS}}

