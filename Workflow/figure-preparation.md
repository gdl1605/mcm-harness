# V6 后异步图表准备工作流

> 本文件定义主 harness 中的图表准备支线。它只负责诊断证据、论文作图数据包和图表/位置建议，不负责正式论文图的绘制、审美评价、样式迭代或论文正文写作。

## 1. 边界、入口与停止

图表准备在 `validation/validation-handoff.md` 形成后才可以启动。Leader 先冻结验证交接、`validation/claims/claim-evidence-map.md`、逐问可引用结果、run/模型/数据版本、题间接口和禁止使用的旧候选，然后把图表支线与论文准备 CP0–CP6 并行启动。

本支线的输入只包括：

- `validation/validation-handoff.md`；
- `validation/claims/claim-evidence-map.md`；
- 被交接授权的结果表、结果文件、run、模型、数据与代码版本；
- 相关题间接口和官方答卷/论文要求；
- 需要解释的已存诊断产物。

本支线的输出是 `figure-prep/` 下的诊断记录、逐图数据包、图表建议、跨问图表计划和 `figure-preparation-handoff.md`。完成交接后停止，不自动进入论文图绘制、视觉审查、答卷或论文写作。

正式论文图由外部高审美绘图模块消费本支线交接包生成。外部模块不得据此自行改变数据口径、筛选、聚合、单位或验证授权范围；如果需要改变这些内容，必须产生变更请求返回上游。

## 2. Leader 与异步调度原则

主 Agent 仍是唯一 Leader。Leader 不代替 worker 做诊断、导出数据或撰写图表建议，只负责：

- 冻结输入版本并记录范围；
- 按问题或共享结果单元派发 subagent；
- 给每个 task brief 指定读取白名单、禁止上下文、唯一主输出路径和额外工程写权；
- 发现上游问题时裁决 change request 是否返回验证/建模/数据；
- 等待最终汇合条件成立，核对 Integrator 写出的全局交接并宣布汇合；Leader 不代写或改写该交接。

图表支线是后台支线，不阻塞论文准备 CP0–CP3。它不采用固定“每图一个 agent”，而是按问题 owner 或跨问共享结果单元派工。只有输入已冻结、写入路径互不冲突、任务确实有独立判断价值时才并行创建 worker。

W0–V6 的既有波次限制继续有效；本支线不设置固定 subagent 数量上限，但受独立输入、独立输出路径和平台容量约束。一个问题只创建一个 `Question Figure Curator`，一个跨问共享结果只创建一个 shared curator；不因图表候选数量增加而复制重复 owner。

每个 worker 任务都由以下三部分拼成：

```text
prompts/figure-preparation/worker-base.md
+ 当前角色 prompt
+ 本轮开放 task brief
```

角色和路径以 `Workflow/figure-preparation-team.json` 与对应 prompt 为准；该配置只记录机械调度信息，不能把开放 Markdown 交接压缩成语义 JSON schema。

## 3. F0：V6 冻结与异步分支

### Leader 动作

1. 确认 `validation/validation-handoff.md` 已落盘，核对当前版本与 claim map。
2. 创建 `figure-prep/scope/frozen-inputs.md`，列出每问授权结果、来源表、数据/run/模型/代码版本、题间接口、禁止使用的旧结果和冻结时间；CP1 尚未完成时把 `paper-prep/structure/chapter-map-v0.md` 标为 F3 阻塞项，落盘后登记实际路径、版本和哈希。
3. 建立问题清单：每问一个 curator；有跨问共享结果时另建 shared curator，写入 `figure-prep/cross-question/shared/`。
4. 同时启动论文准备 CP0；CP1 完成后只通过 chapter-map-v0 路径交接，双方不互相覆盖文件。
5. 为每个 curator 建立独立 brief，说明它只能写自己问题目录或 `cross-question/shared/` 目录。

### F0 不做的事

- 不在冻结前替换结果表、重跑模型或重新解释题意；
- 不要求每一道题都必须有论文图；
- 不把诊断图直接命名为最终论文图；
- 不由 Leader 预先给出“应该画什么”的倾向，避免污染 curator 的独立判断。

## 4. F1：逐问题诊断与数据整理

每个 `Question Figure Curator` 只读冻结输入、相关问题的授权结果和自己的 task brief。它可以在自己目录内运行只读分析和补做诊断图，但不得修改 `data/`、`modeling/`、`validation/` 或论文草稿。

### 4.1 诊断图

诊断图用于检查结果、残差、稳定性、敏感性、约束冲突、异常和题间接口。Curator 应保留：

- 诊断目的和触发原因；
- 输入数据、筛选、run、模型、代码和参数版本；
- 生成代码、原始输出和可读预览；
- 图中观察、未知、反例和对结论的影响；
- 是否需要向验证/建模/数据提交 change request。

诊断图允许信息密度较高，不需要论文级审美迭代。若观察可能推翻已授权主张，Curator 只能写 `figure-prep/change-requests/` 请求，由 Leader 决定返回最早受影响阶段；不得直接修上游。

### 4.2 论文图候选

Curator 逐问判断哪些 claim 值得图示，允许明确写“不建议作图”。候选建议至少说明：

- 图要回答的 claim 和读者任务；
- 推荐图型、备选图型及选择理由；
- 横轴、纵轴、分组、颜色/线型/标记/面板分别表示什么；
- 必须保留的误差、区间、样本量、阈值、缺失或可行性状态；
- 数据允许支持和不允许支持的表述；
- 逻辑位置，例如“问题二结果分析的主结果表之后、敏感性分析之前”；
- caption 骨架、正文引入句和图后解释重点；
- 与相邻表格或其他图的重复、冲突和组合关系。

### 4.3 逐图数据包

每个候选图建立独立目录 `figure-prep/questions/qN/candidates/FIG-QN-XX/`，至少包含：

- 未静默四舍五入的 `data.csv`；必要时附 `data.parquet`；
- 可复现的 `export.py` 或等价导出入口；
- `provenance.md`：来源结果表、数据/run/代码版本、筛选、聚合、排序、派生、主键、粒度、时间范围和单位；
- `recommendation.md`：图型、编码、位置、caption、限制、备选和禁止过度解释。

导出必须从冻结授权结果重建。不能为了方便绘图删除异常、缺失或不利结果，不能把展示精度写回源值，不能静默制造题面没有支持的标签、proxy、目标量或总体。若图型需要新聚合、归一化或指标，先写 change request，不在 F1 偷换口径。

F1 的最低问题只是起点，不是输出白名单。Curator 必须保留任何可能改变 claim、数据边界、题间接口、风险或论文位置的新发现。

## 5. F2：逐问流式独立复核

一个问题的 `question-package.md` 和候选数据包落盘后，Leader 立即创建该问题的全新 `Figure Evidence Auditor`，不等待其他问题完成。Auditor 不读取 Curator 的未授权草稿、其他问题 review 或 Leader 的裁决倾向；它只读取冻结输入、该问题已落盘 package、代码和允许的来源结果。

当前问题或共享结果单元的写入根统一记为 `<unit_root>`：只能是 `figure-prep/questions/qN/` 或 `figure-prep/cross-question/shared/`。Auditor 的主报告固定写入 `<unit_root>/review.md`，不另造问题级路径。

Auditor 检查：

- 数据包能否由授权结果表和 `export.py` 复算；
- 行数、主键、粒度、筛选、聚合、排序、单位和时间范围是否一致；
- 派生量、区间、样本量、缺失和可行性状态是否保留且解释正确；
- 推荐图型是否能回答 claim，是否存在误导性坐标或编码；
- 逻辑位置是否和问题内部叙事、相邻表格及章节地图相容；
- 外部绘图模块是否只凭交接包即可作图，不必重新猜测代码意图。

Auditor 只写 `<unit_root>/review.md`，不得改数据包或上游实现。当前机械检查只确认文件、路径和非空可读性；哈希、版本、CSV 重建和列级一致性由 Auditor 复核。不能用脚本无报错替代语义复核。

## 6. F2R：原 Curator 回应与定向修订

Leader 将 `<unit_root>/review.md` 原文交给产生该 package 的原 `Question Figure Curator`，使用同一 subagent 进行一次集中回应。回应固定写入 `<unit_root>/response.md`，它可以：

- 修正文档、导出脚本、数据包或图表建议，并保留旧版本；
- 接受问题、以证据维持原判断、缩小适用范围或标记暂不可交接；
- 说明修订对 claim、位置、caption、下游图表和版本哈希的影响。

Curator 永久不能直接修改 `data/`、`modeling/`、`validation/` 或论文正文。发现实质数据、模型或验证问题时，只写带来源的 `change-request`。Leader 依据变更影响返回最早上游阶段，并标记受影响的图表候选；未受影响的问题不全盘重做。

默认只进行一次 F2R。若仍有分歧，Leader 可保留分支、限制 claim、暂缓候选或请求用户决策，不开启无限答辩。

## 7. F3：跨问与章节位置整合

当所有逐问 package 已完成，且 CP1 已提供 `paper-prep/structure/chapter-map-v0.md` 后，Leader 创建新的 `Figure–Chapter Integrator`。章节地图的实际路径、版本与哈希必须已经登记；没有地图时停在 F2R，不允许 Integrator 自造章节结构。Integrator 只读各问题 package、reviews/responses、冻结输入、题间接口和章节地图，不绘图、不修改论文材料。Integrator 只在 `figure-prep/cross-question/integration/` 写整合过程，并且是 `figure-plan.md` 和 `figure-preparation-handoff.md` 的唯一内容 owner；Leader 不替它撰写或改写这两份内容。

Integrator 负责：

- 删除重复或不能显著降低理解成本的候选；
- 统一 Figure ID，区分核心、辅助、可选和放弃项；
- 识别应组合成跨问图或必须拆开的候选；
- 将逐问建议映射到章节、结果表和论证顺序；
- 写正文引入句、图后解释重点、相邻表格关系和 caption 方向；
- 汇总诊断异常、已裁决 change request、仍保留的分歧和外部绘图注意事项；
- 生成全篇 `figure-plan.md`；
- 根据同一整合判断生成 `figure-preparation-handoff.md`，确保每个 Figure ID、来源、claim、位置和限制可追溯。

如果跨问共享结果尚未完成，Integrator 只能标记缺口，不能自行补造数据。共享 curator 的输出先过同样的 Auditor，再进入 F3。

## 8. F4：汇合与交接

F3 Integrator 写出 `figure-plan.md` 和 `figure-preparation-handoff.md` 后，Leader 只核对以下汇合条件，不代替 Integrator 修改内容：

1. 每个已启动问题都有 `question-package.md` 和 review；保留了论文图候选的单元还必须有对应数据包，不建议作图的单元须在 package 中说明理由；
2. 复核意见已由原 Curator 回应，或明确记录缺失、暂缓和保留分支；
3. 所有高影响 change request 已裁决，未裁决项有影响范围和禁止表达；
4. `figure-plan.md` 已与章节地图对齐；
5. 每个 Figure ID 都能链接到数据包、来源、claim、推荐图型和逻辑位置；
6. 交接明确不建议作图和外部模块不得改变的口径。

结果章节可以在支线运行期间使用 Figure ID 占位，但不得在上述条件未满足时标记定稿。F4 完成后主 harness 停止图表准备；外部绘图模块另行负责：

- 选择具体审美方案和图形版式；
- 绘制和渲染正式论文图；
- 多模态视觉检查、审美 A/B 和有限轮次迭代；
- 返回最终图、caption 和图表文件。

外部绘图若发现数据语义问题，必须回到本交接包或更早上游，不得以视觉修改掩盖问题。

## 9. 运行目录与交接对象

```text
figure-prep/
├── scope/frozen-inputs.md
├── questions/qN/
│   ├── diagnostics/
│   │   ├── diagnostic-index.md
│   │   ├── src/
│   │   ├── data/
│   │   └── figures/
│   ├── candidates/FIG-QN-XX/
│   │   ├── data.csv
│   │   ├── export.py
│   │   ├── provenance.md
│   │   └── recommendation.md
│   ├── question-package.md
│   ├── review.md
│   └── response.md
├── cross-question/
│   ├── shared/
│   │   ├── diagnostics/
│   │   ├── candidates/FIG-SHARED-XX/
│   │   ├── question-package.md
│   │   ├── review.md
│   │   └── response.md
│   └── integration/
├── change-requests/
├── figure-plan.md
└── figure-preparation-handoff.md
```

文件夹表示所有权和追溯边界，不是固定语义 schema。开放 Markdown memo 可以增补任何未预见内容；如需机器记录，只允许在配置、状态、路径、哈希、版本和运行参数中使用 JSON。

`figure-preparation-handoff.md` 至少包含：

- 必做、可选、放弃和不建议制作的 Figure ID；
- 每张图的数据包、来源结果表、版本和精确值；
- 支持的 claim、限制和禁止表述；
- 推荐/备选图型、视觉编码、误差/阈值/样本量和必要标注；
- 论文逻辑位置、正文引入句、caption 骨架和相邻表格关系；
- 诊断异常、已裁决回滚、未决 change request 和外部绘图注意事项。

## 10. 失败、重开与停止纪律

- worker 未返回：同角色重试一次；仍失败则标记该问题缺失，不能由 Leader 冒充独立复核。
- package 不可复算：暂停该问题交接，保留失败版本，要求原 Curator 修订；不影响已独立完成的其他问题。
- claim 与授权结果不符：降低或撤销该候选，不为凑图保留。
- 诊断发现模型、数据、题意或验证边界问题：写 change request 返回最早受影响阶段；图表支线不直接修上游。
- 只是审美分歧：记录为外部绘图模块的开放选择，不在主 harness 内评分或无限迭代。
- 需要改变图型表达但不改变数据：更新 recommendation 和 Figure ID 版本即可；需要改变数据口径则重新走上游交接。
- 旧诊断、失败导出、旧 package、旧 review 和被替换版本均保留，通过版本和来源索引标记当前使用项。

当前机械检查只确认文件存在、路径和非空可读性；哈希、版本、数据重建和列级一致性由独立 Auditor 负责。它不评价图是否美观，也不替代数据/claim 的独立判断。
