# 建模构建模块详细实施计划

> 状态：建模构建部分已执行，终点仍是 `modeling/model-handoff.md`。后续独立验证、图表准备和论文准备已在各自模块实现；完整论文、正式绘图与最终交付仍不属于本计划。

## 1. 实施目标

把现有设计转成主 Agent 可以直接调度原生 subagent 的模块，使 Leader 无需外部 orchestrator 就能完成：

```text
数据交接
→ 逐问规格与计算计划
→ baseline 最小贯通
→ 触发式诊断与受约束调整
→ 主/挑战候选构建
→ 跨问接口装配
→ 模型交接
```

完成后的模块应具备：

- 根 `AGENTS.md` 中的 Leader 规则和建模文件路由；
- `Workflow/README.md` 中逐阶段、逐角色、带准确 prompt 路径的调度说明；
- 只记录路径、角色和创建/复用关系的 machine-readable team 配置；
- Leader、worker-base 和全部角色 prompt；
- 开放 Markdown task brief 与各阶段模板；
- run 目录初始化和可选 prompt 拼装支持；
- 明确的 M4 动态触发、调整权限、分支预算和局部回滚。

不以“某模型效果达到阈值”作为实施完成条件，也不预置任何通用模型路线。

## 2. 实际运行时的详细调度

### 2.1 谁在真正调度

真正的调度者只有当前主 Agent，也就是 Leader。运行时不启动调度脚本、队列服务或常驻进程。

Leader 的实际动作只有五类：

1. 读取 `AGENTS.md` 和 `Workflow/README.md` 确认当前阶段；
2. 从模板写本轮开放 task brief；
3. 创建新 subagent，或按要求向原 subagent 发 follow-up；
4. 等待本轮相关角色完成并确认原始 memo 落盘；
5. 综合、定级、授权下一步或退回上游。

角色 prompt、task brief 和输入文件都通过路径交给 subagent。辅助脚本不决定创建谁、不判断结果好坏，也不自动推进阶段。

### 2.2 M0：模块接收与问题编排

M0 完全由 Leader 执行，不创建 worker。

| 子步骤 | Leader 动作 | 读取 | 写入 | 完成后的去向 |
|---|---|---|---|---|
| M0.1 接收上游 | 核对当前采用的题意、候选汇报、真实人工模型决定、路线和数据版本 | `synthesis/problem-baseline.md`、`routes/model-candidate-briefing.md`、`routes/human-model-decision.md`、`routes/route-handoff.md`、`data/data-handoff.md` | 暂不写综合 | H1 或其他上游缺失则停止 |
| M0.2 问题依赖图 | 逐问列输入、输出、父问题、消费问题和失效传播 | 三份交接及必要原始 memo | `modeling/question-map.md` | 明确串行/并行关系 |
| M0.3 数据与反馈边界 | 标出允许使用的分析视图、开发反馈和保留信息 | data handoff | 写入 question map | 不得自行打开保留信息 |
| M0.4 所有权 | 指定 shared-kernel owner；为各问预留独立代码/运行目录 | question map | 写入 question map | 避免并行写冲突 |
| M0.5 M1 brief | 每问或共享问题写三个隔离 brief | 建模设计、question map | `modeling/briefs/M1/` | 进入 M1 |

如果问题之间共享同一个状态空间、参数估计或优化内核，先将其定义为共享构建单元，再决定各问如何消费；不能让三个问题分别实现三个口径不同的公共量。

### 2.3 M1：三视角隔离分析

每个待构建单元默认并行创建 3 个新 subagent：

| 角色 | 完整 prompt | 允许读取 | 首轮隐藏 | 输出 |
|---|---|---|---|---|
| 数学规格架构师 | `prompts/modeling/worker-base.md` + `prompts/modeling/mathematical-specification-architect.md` + 自己的 brief | 三份冻结交接、question map、必要原始来源 | 其他 M1 报告、Leader 模型倾向 | `modeling/specs/qN-formulation.md` |
| 计算路径规划师 | `prompts/modeling/worker-base.md` + `prompts/modeling/computational-path-planner.md` + 自己的 brief | 同上 | 同上 | `modeling/plans/qN-computation-plan.md` |
| 结构挑战者 | `prompts/modeling/worker-base.md` + `prompts/modeling/structural-challenger.md` + 自己的 brief | 同上 | 同上 | `modeling/challenges/qN-structural-challenge.md` |

Leader 的顺序是：同时派出 → 保存三个 subagent 句柄 → 等待全部返回/失败 → 确认三个路径实际存在 → 才开始综合。

如果某个角色失败，同角色重试一次；仍失败则记录缺失。Leader 不冒充缺失的独立角色。三份报告只是竞争视角，不以二比一投票。

只有当分歧会改变变量、目标、约束、评价口径或题间接口时，Leader 才向对应原角色发一次定向 follow-up。普通措辞差异不创建答辩阶段。

### 2.4 M2：形成可执行构建合同

M2 由 Leader 执行。Leader 读取三份 M1 原报告，不删除少数意见，写 `modeling/specs/qN-build-contract.md`。

Leader 需要逐项决定：

1. 数学对象：集合、变量、参数、目标、约束和输出；
2. 数据对象：数据版本、视图、字段、粒度、单位、时间和可用时点；
3. 构建对象：人工授权的 baseline、主候选、备选/挑战/敏感性候选；
4. 结果口径：候选结果表和题间接口的对象/单位/粒度；
5. 反馈边界：开发阶段允许看的信息与后续验证保留信息；
6. 预期画像：合理结果可能表现出的范围、符号、形状和约束状态；
7. 调整包络：L0/L1 哪些变化预授权，哪些属于 L2/L3；
8. 预算：本问的分支数、时间、计算资源和停止条件；
9. 回滚：哪些观察回到 M2、数据、路线或题意。

仍有两个结构都合理时，合同允许主/挑战双分支；不是为了“完整”强行选一个，也不允许无限增加第三条路线。

### 2.5 M3：baseline 最小贯通

每问第一次进入 M3 时创建一个新的 model builder。该 builder 在本问后续所有 M4 修订中持续复用。

| 子步骤 | 执行者 | 动作 | 产物 |
|---|---|---|---|
| M3.1 接收 | 新 builder | 读取 build contract、允许数据和自己的 brief | 不写其他角色文件 |
| M3.2 运行前声明 | 原 builder | 在运行前写目的、单一假设、预期观察、冻结项和预算 | `modeling/runs/<run-id>/run-intent.md` |
| M3.3 实现 baseline | 原 builder | 建统一输入、最简模型、标准结果表和题间输出 | `modeling/src/`、`configs/`、candidate tables/interfaces |
| M3.4 执行与留档 | 原 builder | 运行并保留日志、状态、失败和结果 | `modeling/runs/<run-id>/` |
| M3.5 事后解释 | 原 builder | 写实际观察、偏差、竞争解释和建议 | `modeling/runs/<run-id>/iteration-memo.md` |
| M3.6 初次裁决 | Leader | 根据预设触发信号选择直接 L0、进入诊断、L2 重开或 L3 上游请求 | 进入 M4 或暂停 |

baseline 不能省略。它不负责获胜，而是固定一个可解释参照、验证结果接口能否工作并尽早暴露不可构造目标。

### 2.6 M4：结果不好时具体怎样调

M4 不是固定波次，而是 Leader 每次看完运行后选择以下路径之一。

#### 路径 A：低影响且已定位的 L0 实现错误

适用：明显索引错误、维度错误、公式翻译错误、读写错误或日志遗漏，根因没有实质竞争解释。

```text
原 builder 记录错误和影响
→ Leader 确认未改变合同
→ 复用原 builder 修复并产生新 run
→ 旧 run 保留
```

这里不创建诊断者；否则会为了流程形式浪费上下文。

#### 路径 B：高影响、多解释或异常优秀/异常糟糕

| 子步骤 | 调度 | 可见上下文 | 输出/决定 |
|---|---|---|---|
| M4B.1 中性触发 brief | Leader | build contract、预设触发信号、原始产物路径 | `modeling/briefs/M4/qN-runK-diagnosis.md` |
| M4B.2 独立诊断 | 创建新 diagnostician | build contract、run intent、代码、原始日志/结果、baseline；隐藏 builder 事后归因和建议 | `modeling/diagnostics/qN-runK-diagnosis.md` |
| M4B.3 交换观点 | Leader | diagnosis 已落盘后，才将 diagnosis 发给原 builder | 不修改代码 |
| M4B.4 原实现者回应 | 复用原 builder，加载 response prompt | 自己原实现、iteration memo、diagnosis | `modeling/adjustments/qN-runK-builder-response.md` |
| M4B.5 Leader 定级 | Leader | 原始证据、独立 diagnosis、builder response | L0/L1、L2、L3、双分支或停止 |
| M4B.6 adjustment card | Leader 写裁决，builder补执行细节 | 当前版本和获批范围 | `modeling/adjustments/qN-runK-adjustment.md` |
| M4B.7 修订重跑 | 复用原 builder | 只读获批 adjustment card | 新代码/配置版本和新 run |

新的 diagnostician 不是正式验证者：它只做根因竞争解释和下一步判别。第一次诊断使用新 agent；同一失败机制的连续复查可以复用，若连续两轮都沿用同一解释却没有区分力，则换 fresh-context diagnostician 或停止搜索。

#### 路径 C：L2 模型结构变化

适用：需要改变函数形式、状态关系、目标/约束表达、模型特定表示或候选族。

```text
Leader 暂停 builder 写入
→ 复用数学规格架构师和/或结构挑战者做定向复核
→ Leader 生成 qN-build-contract-vK+1
→ 标记旧合同下哪些 run 失效
→ 复用原 builder 按新合同构建
```

代码改动很小也可能是 L2；判断依据是数学含义是否改变。

#### 路径 D：L3 上游变化

适用：需要改变目标构造、标签/proxy、样本总体、Canonical 数据、可用时点、题间接口、题意或路线。

```text
立即停止本问修改
→ 写 modeling/change-requests/<target>-request.md
→ Leader 回到数据/路线/题意相应阶段
→ 上游形成新版本与影响说明
→ 只让受影响问题重新进入 M0/M2/M3
```

模型 builder 不能直接改共享数据后继续跑，也不能把 L3 伪装成“特征工程”。

#### 每轮之后怎样决定继续

Leader 只在存在“影响答卷的高价值不确定性 + 可负担且有区分力的下一动作”时再开一轮。以下情况停止搜索并交给验证：

- 只剩同口径的小幅指标波动；
- 下一步只能增加复杂度，不能区分根因；
- 必须提前打开验证保留信息；
- 已达到构建合同预算；
- 当前分歧本质上需要独立稳健性、敏感性或复现判断。

### 2.7 多问题怎样并行

- 问题依赖图中互不依赖、写入路径分离的问题可以并行，各有自己的 builder；
- 同一个问题的 builder、diagnostician 和 responder 不并行改文件；diagnostician 只读；
- 有共同内核时先指定 shared-kernel owner，其他问题 builder 只调用公共接口；
- 上游问题版本变化时，Leader 只取消或失效标记其后代运行，不影响独立分支；
- 并发槽位优先给当前关键路径，不为填满 3 个槽创建无独立输入的任务。

### 2.8 M5：跨问接口装配

1. 复用上游原 builder，用 interface prompt 写 producer memo；
2. 复用下游原 builder，用同一 prompt 的 consumer 变体写 consumer memo；
3. Leader 比较双方主键、粒度、单位、时间、版本和不确定性；
4. 不需改代码则记录接口版本；
5. 需要适配代码时，从相关原 builder 中指定唯一 integrator，只有它可以修改接口目录；
6. 若适配会改变语义，回到 M2/L3，不允许用 glue code 掩盖。

产物写入 `modeling/results/interfaces/`，并记录哪些下游 run 依赖哪个上游版本。

### 2.9 M6：模型交接

M6 由 Leader 执行，不创建总结型 worker。Leader读取全部原始规格、计划、挑战、合同、run intent、iteration memo、diagnosis、response、adjustment、代码/结果和接口 memo，写 `modeling/model-handoff.md`。

交接完成只表示候选构建物、调整历史和待验证问题已经完整交出，不表示模型通过验证。Leader 此时停止，不创建验证、绘图或论文角色。

## 3. 文件改动总表

### 3.1 修改现有文件

| 文件 | 改动责任 |
|---|---|
| `AGENTS.md` | 增加建模模块 Leader 路由、创建/复用规则、M4 调整权限和新的最远停止点 |
| `Workflow/README.md` | 增加 M0–M6 的详细派工，直接列出每个角色 prompt、允许上下文和输出路径 |
| `README.md` | 把建模构建状态从“已设计”更新为“已实现”，保留项目介绍和文档入口 |
| `Workflow/back-half-top-level-design.md` | 更新当时的后半程状态；后续模块的当前状态以该文件最新内容为准 |
| `Workflow/modeling-construction.md` | 只在实施中发现设计冲突时修订，不把运行细节再次复制成第二份调度手册 |
| `scripts/init_run.py` | 初始化建模目录，不预生成任何语义 Markdown 报告 |
| `scripts/build_prompt.py` | 增加建模 Leader/角色 prompt 拼装入口 |

### 3.2 新增配置

- `Workflow/modeling-team.json`

它只保存执行模式、角色到 prompt 的映射、固定阶段、动态触发角色、创建/复用策略、所有权、停止点和机械 artifact 路径。模型解释、诊断、调整理由和裁决不进入 JSON。

### 3.3 新增 prompt

```text
prompts/modeling/
├── leader.md
├── worker-base.md
├── mathematical-specification-architect.md
├── computational-path-planner.md
├── structural-challenger.md
├── model-builder.md
├── build-result-diagnostician.md
├── model-builder-response.md
└── interface-handoff.md
```

### 3.4 新增开放模板

```text
templates/modeling/
├── task-brief.md
├── question-map.md
├── formulation.md
├── computation-plan.md
├── structural-challenge.md
├── build-contract.md
├── run-intent.md
├── iteration-memo.md
├── result-diagnosis.md
├── builder-response.md
├── adjustment-card.md
├── candidate-result-index.md
├── interface-handoff.md
├── model-method-note.md
├── upstream-change-request.md
└── model-handoff.md
```

所有模板声明：所列问题是最低责任，不是字段白名单；角色可以改变章节结构，并继续报告未预见但会改变模型、数据、接口或回滚范围的发现。

## 4. 运行目录

`scripts/init_run.py` 追加以下空目录：

```text
run/
└── modeling/
    ├── briefs/
    │   ├── M1/
    │   ├── M3/
    │   ├── M4/
    │   └── M5/
    ├── specs/
    ├── plans/
    ├── challenges/
    ├── src/
    ├── configs/
    ├── runs/
    ├── diagnostics/
    ├── adjustments/
    ├── results/
    │   ├── candidate-tables/
    │   └── interfaces/
    ├── paper-notes/
    └── change-requests/
```

初始化时不创建 `question-map.md`、规格、诊断或 handoff 占位文件，避免空模板看起来像已经完成的报告。具体问题编号在每次 run 中由 Leader 决定，不在仓库配置中假设固定有三问。

## 5. team 配置设计

`Workflow/modeling-team.json` 建议包含以下机械信息。

### 5.1 execution

- `mode`: `leader_with_native_subagents`
- `leader`: `current_primary_agent`
- `external_orchestrator_required`: `false`
- `worker_slots`: `3`
- `worker_base_prompt`: `prompts/modeling/worker-base.md`
- `leader_speaks_last_in_each_wave`: `true`
- `new_agent_for`: M1 隔离分析、首次模型实现、首次高影响结果诊断
- `reuse_original_agent_for`: 实现者回应、调整重跑、跨问接口说明/集成

### 5.2 roles

| role key | prompt | 创建/复用 |
|---|---|---|
| `leader` | `prompts/modeling/leader.md` | 当前主 Agent |
| `mathematical_specification_architect` | `prompts/modeling/mathematical-specification-architect.md` | M1 新建 |
| `computational_path_planner` | `prompts/modeling/computational-path-planner.md` | M1 新建 |
| `structural_challenger` | `prompts/modeling/structural-challenger.md` | M1 新建 |
| `model_builder` | `prompts/modeling/model-builder.md` | 每问首次 M3 新建；M4 复用 |
| `build_result_diagnostician` | `prompts/modeling/build-result-diagnostician.md` | 高影响 M4 触发时新建 |
| `model_builder_responder` | `prompts/modeling/model-builder-response.md` | 复用对应原 builder |
| `interface_handoff_owner` | `prompts/modeling/interface-handoff.md` | 复用相关原 builder；代码修改时指定唯一集成所有者 |

### 5.3 phases

配置列出固定阶段 `M0/M1/M2/M3/M5/M6`，并把 M4 表达为动态循环：

```text
M4A observation
M4B diagnosis_if_triggered
M4C original_builder_response
M4D leader_decision
M4E authorized_revision
```

JSON 只声明哪个角色在什么事件下可被创建或复用，不写“低于多少分必须重做”等语义阈值。具体触发解释以设计文档和 Leader prompt 为准。

### 5.4 ownership

- 题意、路线和数据交接：只读；
- M1 报告：一角色一报告，只追加；
- M2 构建合同：Leader 所有；
- 每问模型代码/配置/运行：对应原 model builder 单一所有；
- M4 诊断：新 diagnostician 只写自己的 diagnosis；
- M4 回应/修订：原 builder 所有；
- 共享建模内核：Leader 指定唯一 owner；
- M5 接口适配代码：一个被指定的原 builder 单一所有；
- M6 模型交接：Leader 所有。

## 6. Leader 调度实现

### 6.1 `AGENTS.md`

新增“建模构建阶段文件路由”表，至少包含：

| 阶段 | Leader 必读 | 派发 prompt | 主要产物 |
|---|---|---|---|
| 建模启动 | 设计、team 配置、建模 Leader prompt | worker-base | 建模 task brief |
| M0 | 三份上游交接 | 无，Leader 执行 | `modeling/question-map.md` |
| M1 | 建模设计与当前问题 brief | 三个隔离角色 prompt | formulation / plan / challenge |
| M2 | M1 原始报告 | 无，Leader 综合 | build contract |
| M3 | 当前 build contract | model builder | run intent、baseline、iteration memo |
| M4B | 中性触发 brief 与原始运行产物 | diagnostician | diagnosis |
| M4C/E | diagnosis 与原实现 | builder response，复用 builder | response、adjustment、修订版本 |
| M5 | 各问题接口产物 | interface handoff，复用 builder | producer/consumer memo、必要适配代码 |
| M6 | 全部建模原始产物 | 无，Leader 综合 | `modeling/model-handoff.md` |

同时更新：

- 高层流程从 D5 延伸到 M6；
- 新建/复用规则；
- 诊断者第一轮不得看到实现者事后归因；
- L0–L3 调整权限；
- 当前最远停止点改为 `modeling/model-handoff.md`；
- 正式验证、论文级绘图和论文写作仍禁止。

### 6.2 `Workflow/README.md`

这里写完整调度，不只链接 team JSON。每次派工必须直接列出：

- 创建新 subagent 还是复用原 subagent；
- 准确的 worker-base 和角色 prompt 路径；
- 允许读取和必须隐藏的上下文；
- 唯一主 Markdown 输出和额外工程写入范围；
- 本阶段停止条件和回退方向。

M4 需要单独写成条件分支，不伪装成每次都固定创建诊断者：

```text
低影响且已定位 L0
→ 原 builder 留档修复

高影响/多解释/异常优秀或接口失败
→ 新 diagnostician 隔离分析
→ 复用原 builder 回应
→ Leader 定级
→ 原 builder 按授权修订

涉及目标、数据、标签、总体或题意
→ 暂停本问并发上游变更请求
```

## 7. prompt 实现要求

### 7.1 Leader prompt

`prompts/modeling/leader.md` 必须覆盖：

- M0–M6 的创建、等待、复用和停止顺序；
- 问题依赖图、共享代码和失效传播；
- 开发反馈与保留信息隔离；
- baseline 冻结和主/挑战分支预算；
- M4 触发信号、L0–L3 权限和 adjustment card；
- 诊断者的上下文隔离；
- M5 接口集成单一所有权；
- 何时继续、分支、停止或退回上游；
- 不以运行成功、单一指标或模型复杂度宣布正确。

### 7.2 Worker base

`prompts/modeling/worker-base.md` 延续现有开放交付口径：

- 只读 task brief 白名单；
- 默认只写唯一 Markdown；
- 只有 builder/response/interface brief 可授权代码、配置和候选结果写入；
- A/B/C/D 是最低责任，不是 schema；
- 单列任务之外的新发现；
- 不修改题意、路线、Canonical 数据或其他角色原报告；
- 不进入正式验证、论文图和论文正文。

### 7.3 M1 三角色

- 数学规格角色只定义数学对象和题间接口，不实现代码；
- 计算路径角色只规划复杂度、求解器、数值风险和执行顺序，不抢共享所有权；
- 结构挑战者先寻找简单 baseline 和最小失效反例，不用复杂算法制造挑战路线；
- 三者首轮互不可见，Leader 最后综合。

### 7.4 Model builder

`model-builder.md` 必须要求：

- 先写 run intent 再运行；
- 人工授权的 baseline、主候选和挑战/敏感性候选共用冻结数据/结果接口；
- 每次运行记录输入、代码、配置、随机性、求解状态和结果路径；
- 不只保留最佳版本；
- 遇到 L2/L3 问题停止修改并请求 Leader；
- 同步写模型方法工程文稿。

### 7.5 Result diagnostician

第一轮 prompt 明确禁止读取：

- builder 的事后归因；
- builder 建议采用的修复；
- Leader 对根因的倾向；
- 其他诊断者结论。

它只读 build contract、run intent、代码、原始日志/结果、baseline 和中性触发说明。报告必须区分七类失败来源，提出可反驳解释和最小判别动作，不修改工程文件。

### 7.6 Builder response

`model-builder-response.md` 只在 diagnosis 落盘后加载，并复用原 builder。它负责钢人化诊断、说明接受/反驳/分支/上游重开，草拟 adjustment card；Leader 裁决前不得直接改冻结对象。

### 7.7 Interface handoff

同一 prompt 通过 task brief 指定三种变体：

- producer：说明上游真正生产的对象与版本；
- consumer：说明下游真正需要的对象与不能消费点；
- integrator：被 Leader 指定的唯一代码 owner，只实现获批接口适配。

## 8. 模板实现要求

### 8.1 Task brief

除通用角色、目标、输入、隐藏上下文、唯一输出和写入范围外，建模 brief 还需支持：

- 问题编号和父问题版本；
- 当前 build contract；
- 开发反馈与保留信息边界；
- 实现所有者和共享代码所有者；
- 当前分支、父运行和失效传播；
- 本轮允许的 L0/L1/L2/L3 权限；
- 时间/计算预算与停止条件。

### 8.2 Build contract

模板包含最低责任：数学对象、数据接口、题间接口、baseline、主/挑战候选、结果预期画像、开发反馈、保留信息、调整包络、分支预算、计算预算和重开信号。

### 8.3 Run intent 与 iteration memo

必须分成两个文件或两个不可混淆的版本：

- run intent 在执行前形成，记录目的、单一主要假设、预期观察、冻结项和预算；
- iteration memo 在执行后形成，记录实际结果、偏差、作者解释和建议动作。

这样诊断者可以只读运行前意图和原始产物，不被作者事后解释锚定。

### 8.4 Diagnosis、response 与 adjustment

- diagnosis：新诊断者的独立根因竞争解释和最小判别动作；
- builder response：原实现者在看到 diagnosis 后的一次集中回应；
- adjustment card：Leader 裁决后的获批变化、冻结项、预期反证、影响和回滚。

三者不能合并为一份“已修复报告”，否则无法保留观点顺序和责任。

### 8.5 Model handoff

交接模板必须保留：

- 逐问规格、候选和版本；
- 全部关键调整与回滚关系；
- 已使用开发反馈和未打开保留信息；
- 候选结果、代码、配置、数据和题间接口；
- 失败运行、异常优秀结果、未决分支和实现妥协；
- 验证模块优先攻击项；
- 论文工程文稿路径及禁止过度表述内容。

## 9. 辅助脚本：是什么、何时需要

这里的“机械”是指：输入和输出完全确定，只处理目录、路径、文本拼接和存在性，不解释题意、不诊断模型、不创建 Agent、不做调度裁决。它们不是 M0–M6 的一个建模阶段。

| 工具 | 在真实流程中的位置 | 是否是核心依赖 | 解决的问题 | 明确不做什么 |
|---|---|---|---|---|
| `scripts/init_run.py` | 一道新题刚建立 run 时，位于 W0 之前；不是进入 M0 时重复运行 | 新 run 推荐使用；已有 run 不需要重跑 | 一次性创建共享目录、来源 manifest 和机械状态，避免不同 Agent 随意建目录 | 不派工、不写语义报告、不决定问题数量 |
| `scripts/build_prompt.py` | Leader 准备派某个角色时，可把 worker-base、role prompt、task brief 拼成一段文本 | 可选；原生 subagent 可以直接按路径读取 | 兼容只能接收单段 prompt 的环境，减少漏掉某段 prompt | 不创建 subagent、不选择角色、不决定上下文白名单 |
| `scripts/check_workspace.py` | M6 交接以后由人或后续自动化检查调用 | 当前模块不需要，延期 | 只发现目录或 handoff 文件缺失 | 不判断模型、公式、诊断或调整正确性 |

因此，本轮建模模块实现只把 `init_run.py` 的目录扩展视为必要支持；`build_prompt.py` 扩展为兼容功能，不能成为 Leader 调度的前置条件；`check_workspace.py --stage modeling` 与自动化测试一起延期。

### 9.1 `init_run.py`

- 只创建第 4 节目录；
- 将 metadata 中的最远 scope 更新为 `modeling/model-handoff.md`；
- 不预建任何 `.md` 报告；
- 不假设问题数量或模型类型。

调用位置只有一次：

```text
收到新题
→ python3 scripts/init_run.py RUN_DIR ...
→ W0 来源封箱
→ 后续 W/D/M 阶段复用同一个 run
```

如果 run 已经由旧版本脚本创建，Leader 只补建缺失的 `modeling/` 空目录；不得重新运行初始化覆盖已有状态。

### 9.2 `build_prompt.py`

增加：

```text
--model-leader
--model-role ROLE --task-brief PATH
```

支持 role key 与文件 stem 两种名称，例如 `model_builder` 与 `model-builder`。渲染顺序固定为：

```text
prompts/modeling/worker-base.md
+ 角色 prompt
+ 开放 task brief
```

脚本只拼装文本，不创建 subagent、不决定触发条件、不读取语义报告。原生 subagent 的首选调度仍是 Leader 在派工消息里明确要求读取三个路径；即使此脚本不可用，M0–M6 也应能完整执行。

### 9.3 `check_workspace.py`

未来新增 `--stage modeling` 时，只检查：

- 数据阶段所需机械目录仍存在；
- 建模目录已创建；
- `modeling/model-handoff.md` 存在且非空；
- 输出中继续声明 `markdown_content_parsed=false` 和 `semantic_correctness_checked=false`。

它不检查模型分数、公式正确性、是否收敛、调整是否合理或候选是否可发表。该改动不纳入本轮建模模块实现，与后续测试/历史题回放一起设计。

## 10. 分阶段实施顺序

### P0：命名与责任冻结

动作：

- 确认 M0–M6、M4A–M4E、L0–L3 命名；
- 确认每个角色的创建/复用关系；
- 确认 prompt、模板和输出路径；
- 确认 run intent 与作者事后解释分离；
- 确认 M5 唯一接口集成所有者。

产物：本计划与设计文档一致，不再存在同一阶段多套命名。

### P1：调度骨架

动作：

1. 创建 `Workflow/modeling-team.json`；
2. 更新 `AGENTS.md` 的建模路由和 Leader 边界；
3. 更新 `Workflow/README.md` 的完整调度及准确 prompt 路径；
4. 更新 README 与后半程实现状态。

完成标志：人只读 `AGENTS.md` 和 `Workflow/README.md` 就能派工；JSON 不再承担语义说明。

### P2：角色 prompt

动作：

1. 编写建模 Leader 和 worker-base；
2. 编写 M1 三个隔离角色；
3. 编写 model builder；
4. 编写结果诊断者；
5. 编写原 builder response；
6. 编写 interface handoff。

完成标志：每个 prompt 都明确允许输入、隐藏上下文、写入范围、最低责任、开放发现和停止边界。

### P3：开放模板

按第 3.4 节创建 16 个模板。先完成 task brief、build contract、run intent、iteration memo、diagnosis、response 和 adjustment card，因为它们决定动态循环能否真正执行；再完成 M1、接口、方法文稿和最终交接模板。

完成标志：任何一次运行、诊断和调整都能保持先后顺序、证据来源、版本与回滚关系，不需要语义 JSON。

### P4：运行目录与可选 prompt 拼装

动作：

1. 扩展 run 目录初始化；
2. 扩展建模 prompt 拼装作为可选兼容入口；
3. 保持旧前半程和数据工程 CLI 兼容；
4. 不在本阶段扩展 modeling workspace checker。

完成标志：新 run 具备建模目录；Leader 即使不调用 prompt 拼装脚本也能按文档直接派工；没有形成隐藏 orchestrator。

### P5：文档一致性收口

只做静态一致性核对：

- `modeling-team.json` 中每个 prompt 路径在 `Workflow/README.md` 直接出现；
- `AGENTS.md` 的阶段路由与实际文件一致；
- 完整/精简模式、动态触发和停止点在设计、调度、prompt 中不冲突；
- 所有角色仍使用开放 Markdown，JSON 不承载语义结论；
- 最远停止点统一为 `modeling/model-handoff.md`。

自动化测试、历史 C 题回放和实战效果评估按用户要求留到后续，不属于本轮实施计划。

## 11. 关键实现约束

1. 不新增外部 orchestrator；Leader 直接使用原生 subagent。
2. 不把 M4 写成固定轮数，也不为每次普通运行都创建诊断者。
3. 不让诊断者先看到 builder 的事后归因和建议修复。
4. 不让诊断者修改代码，也不让 builder 自己成为唯一独立诊断意见。
5. 每问和共享内核都有唯一代码 owner；M5 适配同样只有一个 owner。
6. 任何非平凡调整先形成 adjustment card，再修改和重跑。
7. L2 必须升版 build contract；L3 必须发上游变更请求。
8. baseline、开发反馈、保留信息和评价口径不能跟随结果静默漂移。
9. 默认最多一个主分支和一个实质挑战分支；新增分支需 Leader 给出区分价值。
10. 建模产物始终标为候选，未经独立验证不能升级为最终论文结论。

## 12. 实施风险与处理

| 风险 | 处理 |
|---|---|
| M4 文档过多，Agent 忽略记录 | 只在有意义运行创建 run/adjustment memo；L0 小修可合并记录，不机械制造文件 |
| 诊断者与实现者使用同一模型，意见仍同质 | 强制第一轮上下文隔离、原始证据优先；反复同一解释时再引入 fresh-context 诊断 |
| 每问一个 builder 导致共享代码冲突 | 先指定 shared-kernel owner；其他 builder 只调用，不直接修改 |
| 无限调参耗尽时间 | M2 预先写预算；每轮单一假设；无区分价值则停止并交给验证 |
| 为提高效果偷改数据或指标 | L3 上游请求、baseline 冻结、开发/保留信息隔离 |
| 下游建立在失效上游结果上 | question map 记录父版本；上游变更显式使相关下游运行失效 |
| 模板变成新的固定 schema | 每份模板声明最低责任和开放发现，允许重排、扩展和附录 |

## 13. 本计划的停止点

实施完成时，仓库具备可执行的建模构建调度、角色 prompt、模板、运行目录初始化和可选 prompt 拼装，但不会包含：

- 具体竞赛题模型答案；
- 正式模型验证角色或验证结论；
- 论文级图表；
- 答卷或正式论文；
- 自动化测试与历史题回放。

`check_workspace.py --stage modeling` 也随测试阶段延期，不作为建模构建模块当前完成条件。

P1 → P2 → P3 → P4 → P5 已按本计划完成。独立验证已在 `Workflow/model-validation.md` 中作为单独模块实现，没有反向并入建模构建。
