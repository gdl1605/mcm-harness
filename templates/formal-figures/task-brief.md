# 正式绘图 Task Brief：{{TASK_TITLE}}

> 以下是最低责任，不是字段白名单。继续报告任何影响图量、数据准确性、视觉表达、论文位置或回滚范围的新发现。

- 阶段、角色、Agent 句柄：{{PHASE_ROLE_AGENT}}
- mcm profile：`auto`；若覆盖则写 profile 与原因：{{MCM_PROFILE_OR_OVERRIDE_REASON}}
- 强制创建配置：`model=gpt-5.6-sol`、`reasoning_effort=high`、`fork_turns=none`
- 强制视觉链：`$visualize-data → $ssci-plots → $nature-figure`、`backend=python`、两个 skill lock/path/SHA-256：{{VISUAL_SKILL_LOCKS}}
- 用户选定视觉配置：`visual_profile=cassatt2_quiet_journal_v1`、`palette=metbrewer_cassatt2`、profile path/hash：{{VISUAL_PROFILE}}
- 问题/共享单元与唯一目标：{{UNIT_AND_GOAL}}
- 允许读取的精确路径/版本/哈希：{{ALLOWED_INPUTS}}
- 禁止上下文和上游写入：{{FORBIDDEN_CONTEXT}}
- 唯一写入根与 style-owner 权限：{{OUTPUT_AND_WRITES}}
- Figure ID、claim、章节和版心：{{FIGURE_CLAIM_CONTEXT}}
- 迭代预算、旧版保留与停止：{{ITERATION_AND_STOP}}

若 Leader 未显式请求 sol-high、未写完整 skill chain/Python/两个 lock/Cassatt2 profile，或输入不是 F4 冻结对象，停止并报告，不继承默认 Luna，不自行搜索替代结果或静默回退其他 palette/普通 Matplotlib。
