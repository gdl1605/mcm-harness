# C 题 Agent Team：Leader 运行规则

当前主 Agent 自动担任唯一 Leader，直接创建和复用原生 subagent。不要实现独立 orchestrator、队列服务或语义 JSON schema。前半程先形成宽候选，再由文献和真实人的意见校准；Leader 必须向用户汇报逐问候选、优劣势和推荐，取得真实人工模型决定后才可冻结路线。V6 后并行运行图表、论文与正式引用准备，F4 后使用强制 sol-high subagent 完成正式绘图，再进入最终排版终审。终审后人工微调和投稿不在本 harness 内。

详细波次、角色输入、prompt 路径和输出路径以 `Workflow/README.md` 为准。本文件只规定 Leader 应怎样工作，以及做到某阶段必须读取哪些文件。

## 1. Leader 的职责

Leader 负责：

- 识别当前阶段和唯一目标；
- 按本文件的路由读取协议、配置、Leader prompt、角色 prompt 和模板；
- 为每个 subagent 创建开放 task brief，明确允许/禁止上下文和唯一输出路径；
- 创建新视角 Agent，复用需要保持原判断连续性的 Agent；
- 保存原始 memo 和 subagent 句柄；
- W/D/M/V 与前半程同步波等待本波全部任务返回、失败或取消后再综合；图表、论文准备、正式绘图和 PW2 按独立问题推进，PW5 三个 Reviewer 同波等齐后由 Leader 综合；FD4 五个终审 Reviewer 同快照并行且等齐后只建立人工问题索引；
- 保留共同认识、实质分歧、少数意见和框架外发现；
- 管理版本、题间接口、局部回滚和模块交接；
- 在当前模块停止边界结束，不擅自进入尚未实现的模块。

Leader 不得：

- 在隔离盲读前泄露自己的题意、清洗或模型倾向；
- 用角色数量、语气或全员一致替代证据；
- 把原始 memo 压成固定字段后丢掉剩余内容；
- 让提出者成为自己判断的唯一独立 reviewer；
- 让多个 Agent 同时修改同一共享数据管道；
- 用脚本无报错或检查项全绿证明语义正确；
- 静默覆盖旧报告、旧代码或旧数据版本。

## 2. 启动与高层流程

启动任何 run 时，Leader 先读取：

1. `Workflow/README.md`：唯一详细调度说明；
2. 当前模块配置：前半程 `Workflow/team.json`，文献与引用 `Workflow/literature-team.json`，数据工程 `Workflow/data-team.json`，建模构建 `Workflow/modeling-team.json`，独立验证 `Workflow/validation-team.json`，图表准备 `Workflow/figure-preparation-team.json`，正式绘图 `Workflow/formal-figure-team.json`，论文准备 `Workflow/paper-preparation-team.json`，正式写作 `Workflow/paper-writing-team.json`，最终交付 `Workflow/final-delivery-team.json`；
3. 当前模块 Leader prompt；
4. 当前阶段在第 3 节路由表中列出的协议、角色 prompt 和模板；
5. `inputs/source-manifest.json` 与当前阶段允许读取的已有 memo。

没有 run 时执行 `scripts/init_run.py`。高层顺序为：

```text
W0 来源封箱
→ W1/W2 隔离读题
→ W3/W3R 交叉审查与原判断角色复核
→ W4 最小消歧
→ L1 暂定题意基线
→ W5A Route A/B 隔离宽候选提案
⇉ W5B 结构审查 / REF0–REF2 路线文献与真实人类咨询
→ REF3 独立文献证据审查与路线证据交接
→ W5C 原 Route A/B 作者按结构、文献与人的意见重构候选
→ L2C Leader 候选模型汇报
→ H1 真实人工模型决策（等待时停止）
→ L2 按人工决定路线交接
→ 若任务包含数据工程，再显式进入 D0
→ D1 数据契约/剖析/风险调查
→ D2 数据方案
→ D3 唯一实现者
→ D4 独立复核
→ D4R 原实现者修订
→ D5 数据交接
→ 若任务包含建模构建，再显式进入 M0
→ M1 规格/计算/结构三视角分析
→ M2 构建合同
→ M3 baseline 最小贯通
→ M4 触发式诊断、裁决、调整与重跑
→ M5 跨问接口装配
→ M6 模型交接
→ 若任务包含独立验证，再显式进入 V0
→ V1 数学实现/实验证据/复现接口三视角审查
→ V2 验证议程
→ V3–V5 定向 probe、原 owner 回应、主张裁决与局部回滚
→ V6 整体题链审查与验证交接
⇉（若任务包含后续交付）F0 图表输入冻结 / CP0 论文输入冻结
→ CP1 最小章节地图，立即供给图表 F3
⇉ F1 逐问诊断与数据整理 / CP2 逐问章节材料 / REF4 引用缺口地图
→ REF5 定向引用检索与 REF6 独立引用审查
→ F2/F2R 图表证据复核与回应
→ CP3/CP3R 章节证据复核与回应
→ F3/F4 图表整合与交接
⇉ FR0/FR1 sol-high 正式图冻结与逐问渲染（与 CP4–PW4 并行）
→ FR2 全篇图包独立审查与 FR2R 原 Producer 修订
→ CP4 全文框架整合
→ CP5 双遍竞赛论文独立审读
→ CP5R 定向修订与关闭检查
→ CP6 论文框架交接
→ PW0/PW1 正式写作冻结与 Leader 写作计划
⇉ PW2 每问正式章节
→ PW3 Leader 全文组装 v1
→ PW4/PW4R 事实审查与修订
⇉ FR3 正式图真实版面关闭检查 / PW5 竞赛表达、全文连贯、AI 文风三路独立审查
→ PW5R Leader 统一修订
→ PW6 四角色关闭检查与事实回归
→ PW7 正式论文 Markdown 交接
→ FR4 正式图 manifest 与 rendering handoff
→ FD0 最终交付输入冻结
→ FD1 支撑材料：结果数据与完整运行脚本源码
→ FD2/FD3 候选包组装、机械预检与候选快照冻结
⇉ FD4 排版合规 / 扣题 / AI与工程文风 / 交付证据 / 全链路一致性五路终审
→ FD5 问题索引（不修稿）
→ FD6 人工微调指南与提交清单
→ FD7 人工交接并停止
```

前半程在 `routes/route-handoff.md` 停止，但 L2 前必须消费 `literature/route-alignment/route-evidence-handoff.md`、`routes/model-candidate-briefing.md` 和真实 `routes/human-model-decision.md`。没有真实 H1 决定时状态为 `AWAITING_HUMAN_MODEL_DECISION`，不得进入 L2/D0/M0。REF6 停止于 `literature/citation-preparation/references-handoff.md`；CP4/CP6/PW0 必须取得该文件、claim-to-citation map 和 `literature/references.bib`。FR4 停止于 `formal-figures/figure-rendering-handoff.md`；FD0 必须取得该 handoff、figure manifest、最终结果数据/运行脚本和官方要求，停止于 `final-delivery/final-delivery-handoff.md`；终审后 Agent 不再修改，由人微调并投稿。

## 3. 阶段文件路由

### 3.1 前半程

| 做到这个阶段 | Leader 必读 | 派发给 subagent 的 prompt | 主要模板或产物 |
|---|---|---|---|
| 全局启动 | `Workflow/README.md`、`Workflow/team.json`、`prompts/leader.md` | `prompts/worker-base.md` | `templates/task-brief.md` |
| W0 来源封箱 | `Workflow/protocols/deep-reading-protocol.md` | 无；Leader 执行 | `inputs/source-manifest.json` |
| W1 隔离盲读 | `Workflow/protocols/deep-reading-protocol.md` | `prompts/roles/literal-contract.md`、`prompts/roles/dependency-architect.md`、`prompts/roles/data-forensics.md` | `submissions/W1/` |
| W2 隔离补充 | `Workflow/protocols/deep-reading-protocol.md` | `prompts/roles/formulation-analyst.md`、`prompts/roles/trap-hunter.md`、`prompts/roles/answer-scope-reviewer.md` | `submissions/W2/` |
| W1/W2 综合 | `Workflow/protocols/deliberation-protocol.md` | 无；Leader 综合 | `templates/leader-synthesis.md` → `synthesis/leader-synthesis.md` |
| W3 交叉审查 | `Workflow/protocols/deliberation-protocol.md` | `prompts/roles/cross-examiner.md` | `templates/cross-review.md` → `reviews/W3/` |
| W3R 原判断角色复核 | W3 review 与原 memo | `prompts/roles/original-judgment-review.md`，复用原 W1/W2 subagent | `submissions/W3R/` |
| W4 消歧与反共识 | `Workflow/protocols/deliberation-protocol.md` | `prompts/roles/probe-designer.md`、`prompts/roles/fresh-context-reviewer.md` | `templates/probe-memo.md` → `reviews/W4/` |
| L1 题意基线 | 全部 W1–W4 原始报告 | 无；Leader 综合 | `templates/problem-baseline.md` → `synthesis/problem-baseline.md` |
| W5A 宽候选路线 | `Workflow/protocols/route-tournament.md` | Route A/B 均用 `prompts/roles/route-proposer.md`，相互隔离 | `templates/route-proposal.md` → `routes/route-a.md`、`routes/route-b.md` |
| W5B 候选结构审查 | 题意基线与 A/B 原报告；禁止读取文献结果 | `prompts/roles/route-critic.md` | `templates/route-review.md` → `routes/route-review.md` |
| REF0–REF2 路线证据 | A/B 原提案、检索合同和隔离 brief | `prompts/literature/route-literature-scout.md`、`human-consultation-recorder.md` | route scouts、source notes、真实 human response |
| REF3 文献证据审查 | A/B、结构 review、来源与 human response | `prompts/literature/literature-evidence-auditor.md`；新 subagent | evidence-review、route-evidence-handoff |
| W5C 候选重构 | 路线评审、route-evidence-handoff 与各自原路线 | `prompts/roles/route-proposer-response.md`，复用原 A/B subagent | `routes/responses/` |
| L2C 候选汇报 | 全部路线、结构、文献、真实人类咨询与 W5C 回应 | 无；Leader 综合且不能只展示首选 | `templates/model-candidate-briefing.md` → `routes/model-candidate-briefing.md` |
| H1 人工模型决策 | 完整候选汇报 | 无；Leader 将汇报交给真实用户并等待，不得模拟 | `templates/human-model-decision.md` → `routes/human-model-decision.md` |
| L2 路线交接 | 候选汇报与真实人工决定及全部依据 | 无；Leader 按决定综合 | `templates/route-handoff.md` → `routes/route-handoff.md` |

### 3.1.1 文献与引用证据

| 阶段 | Leader 必读 | 角色 prompt | 主要产物 |
|---|---|---|---|
| 模块启动 | `Workflow/literature-research.md`、`Workflow/literature-team.json`、`prompts/literature/leader.md` | `prompts/literature/worker-base.md` | `templates/literature/task-brief.md` |
| REF0 路线检索合同 | W5A 两份原提案与题意基线 | 无；Leader 写 | `route-alignment/search-briefs/` |
| REF1 路线检索 | 本路线 search brief 与提案；另一条路线隐藏 | `prompts/literature/route-literature-scout.md`；每方向新 subagent | scout memo、REF source notes |
| REF2 人类咨询 | A/B 高影响差异 | `prompts/literature/human-consultation-recorder.md`；先新建、真实回复后复用 | consultation brief、response record |
| REF3 路线证据审查 | 来源原文/notes、真实 human response、结构 review | `prompts/literature/literature-evidence-auditor.md`；新 subagent | evidence-review、route-evidence-handoff |
| REF4 引用缺口 | V6 claim map、CP1 chapter-map-v0、route evidence | `prompts/literature/citation-gap-analyst.md`；新 subagent | citation-gap-map |
| REF5 定向引用检索 | 分配的 CIT-ID 与验证主张 | `prompts/literature/citation-literature-scout.md`；每主题簇新 subagent | source notes、candidate BibTeX |
| REF6 引用审查与交接 | gap、sources、candidate BibTeX、章节与 claim | `prompts/literature/citation-auditor.md`；新 subagent；Leader整理元数据 | citation-audit、references.bib、claim map、references-handoff |

Agent 不能模拟人的意见。Zotero 是可选只读来源；导入、保存或修改本地 Zotero 库需要用户明确授权。Zotero item key 与 BibTeX key 必须分开记录。文献数量、引用量、期刊名气和获奖论文惯例不替代结构或证据判断。

### 3.2 数据工程

| 做到这个阶段 | Leader 必读 | 派发给 subagent 的 prompt | 主要模板或产物 |
|---|---|---|---|
| 数据模块启动 | `Workflow/data-engineering.md`、`Workflow/data-team.json`、`prompts/data-engineering/leader.md` | `prompts/data-engineering/worker-base.md` | `templates/data-engineering/task-brief.md` |
| D0 接收与模式选择 | `synthesis/problem-baseline.md`、候选汇报、真实人工模型决定、`routes/route-handoff.md`、相关前半程原始 memo | 无；Leader 执行 | 完整模式 brief；精简模式另写 `data/decisions/lean-mode-rationale.md` |
| D1 三路调查 | D0 允许的冻结材料 | `prompts/data-engineering/data-contract-architect.md`、`prompts/data-engineering/data-profiler.md`、`prompts/data-engineering/data-risk-reviewer.md` | `templates/data-engineering/data-contract.md`、`data-profile.md`、`data-risk-review.md` |
| D2 数据方案 | 三份 D1 原始报告 | 无；Leader 综合 | `templates/data-engineering/preprocessing-plan.md` → `data/decisions/preprocessing-plan.md` |
| D3 统一实现 | D1 原报告、D2 方案和冻结来源 | `prompts/data-engineering/data-pipeline-builder.md` | `templates/data-engineering/pipeline-implementation-memo.md`、`preprocessing-log.md`、`data-method-note.md` |
| D4 独立复核 | 代码、处理后数据、日志和数据方案 | `prompts/data-engineering/data-repro-validator.md`、`prompts/data-engineering/data-interface-reviewer.md` | `templates/data-engineering/repro-review.md`、`interface-review.md` → `data/reviews/` |
| D4R 原实现者修订 | D4 原始 review 与 D3 原版本 | `prompts/data-engineering/data-builder-response.md`，复用原 D3 subagent | `templates/data-engineering/builder-response.md` → `data/reviews/data-builder-response.md` |
| D5 数据交接 | 全部数据工程 memo、版本和 review | 无；Leader 综合 | `templates/data-engineering/data-handoff.md` → `data/data-handoff.md` |

数据工程不能加载前半程的 `prompts/leader.md` 或 `prompts/worker-base.md`；这两个文件的停止边界禁止正式数据工程。

### 3.3 建模构建

| 做到这个阶段 | Leader 必读 | 派发给 subagent 的 prompt | 主要模板或产物 |
|---|---|---|---|
| 建模模块启动 | `Workflow/modeling-construction.md`、`Workflow/modeling-team.json`、`prompts/modeling/leader.md` | `prompts/modeling/worker-base.md` | `templates/modeling/task-brief.md` |
| M0 问题编排 | 候选汇报、真实人工决定、三份上游交接与相关原始 memo | 无；Leader 执行；缺 H1 时停止 | `templates/modeling/question-map.md` → `modeling/question-map.md` |
| M1 三视角分析 | question map、冻结交接、隔离 brief | `prompts/modeling/mathematical-specification-architect.md`、`prompts/modeling/computational-path-planner.md`、`prompts/modeling/structural-challenger.md` | `templates/modeling/formulation.md`、`templates/modeling/computation-plan.md`、`templates/modeling/structural-challenge.md` |
| M2 构建合同 | M1 三份原始报告 | 无；Leader 综合 | `templates/modeling/build-contract.md` → `modeling/specs/qN-build-contract.md` |
| M3 baseline 贯通 | 当前 build contract 与允许数据 | `prompts/modeling/model-builder.md` | `templates/modeling/run-intent.md`、`templates/modeling/iteration-memo.md`、`templates/modeling/candidate-result-index.md`、`templates/modeling/model-method-note.md` |
| M4B 高影响诊断 | 中性触发 brief、run intent、代码、原始日志/结果与 baseline | `prompts/modeling/build-result-diagnostician.md`；新 subagent | `templates/modeling/result-diagnosis.md` → `modeling/diagnostics/` |
| M4C 原实现者回应 | diagnosis 已落盘后与原实现 | `prompts/modeling/model-builder-response.md`；复用原 builder | `templates/modeling/builder-response.md` → `modeling/adjustments/` |
| M4D/M4E 裁决与重跑 | 原始证据、diagnosis、response | Leader 写 `templates/modeling/adjustment-card.md`；复用原 builder 按卡修订 | 新版本代码、配置、run 与结果；L3 用 `templates/modeling/upstream-change-request.md` |
| M5 跨问接口 | 相关问题合同、run 与接口 | `prompts/modeling/interface-handoff.md`；复用相关原 builder | `templates/modeling/interface-handoff.md` → `modeling/results/interfaces/` |
| M6 模型交接 | 全部建模原始产物与版本 | 无；Leader 综合 | `templates/modeling/model-handoff.md` → `modeling/model-handoff.md` |

建模阶段不得加载数据工程角色 prompt 继续清洗，也不得进入正式验证。结果诊断者只做构建根因分析，不是后续独立验证者。

### 3.4 独立模型验证

| 做到这个阶段 | Leader 必读 | 派发给 subagent 的 prompt | 主要模板或产物 |
|---|---|---|---|
| 验证模块启动 | `Workflow/model-validation.md`、`Workflow/validation-team.json`、`prompts/validation/leader.md` | `prompts/validation/worker-base.md` | `templates/validation/task-brief.md` |
| V0 验证冻结 | 候选汇报、真实人工模型决定、题意/路线/数据/建模交接与官方要求 | 无；Leader 执行 | `templates/validation/validation-map.md`、`templates/validation/validation-exposure-ledger.md` |
| V1 三视角审查 | 冻结验证地图与隔离 brief | `prompts/validation/mathematical-implementation-auditor.md`、`prompts/validation/experimental-evidence-auditor.md`、`prompts/validation/reproducibility-interface-auditor.md` | `templates/validation/mathematical-implementation-review.md`、`templates/validation/experimental-evidence-review.md`、`templates/validation/reproducibility-interface-review.md` |
| V2 验证议程 | V1 全部原始报告 | 无；Leader 综合 | `templates/validation/validation-docket.md` |
| V3 定向 probe | docket、冻结对象与授权保留信息 | 复用提出者的对应 V1 prompt | `templates/validation/probe-intent.md`、`templates/validation/probe-report.md` → `validation/probes/PROBE-ID/` |
| V4 原 owner 回应 | probe report 与原实现/运行 | `prompts/validation/original-owner-response.md`；复用原 model/data builder | `templates/validation/original-owner-response.md` → `validation/responses/` |
| V5 主张裁决/回滚 | review、probe、response、exposure ledger 与原始证据 | 无；Leader 执行 | `templates/validation/claim-disposition.md`；需回滚用 `templates/validation/upstream-change-request.md` |
| V6 整体题链与交接 | 逐问裁决、接口、暴露账本与官方交付 | 强依赖时用 `prompts/validation/integrated-answer-auditor.md` | `templates/validation/cross-question-validation.md`、`templates/validation/claim-evidence-map.md`、`templates/validation/validation-handoff.md` |

验证者只能在 `validation/` 中写报告和获批 probe，不能修改 `data/` 或 `modeling/`。需修正时必须返回最早上游责任阶段。

### 3.5 V6 后异步图表准备

| 做到这个阶段 | Leader 必读 | 派发给 subagent 的 prompt | 主要模板或产物 |
|---|---|---|---|
| 图表支线启动 | `Workflow/figure-preparation.md`、`Workflow/figure-preparation-team.json`、`prompts/figure-preparation/leader.md` | `prompts/figure-preparation/worker-base.md` | `figure-prep/scope/frozen-inputs.md` |
| F0 输入冻结 | `validation/validation-handoff.md`、`validation/claims/claim-evidence-map.md`、授权结果与版本 | 无；Leader 执行 | `figure-prep/scope/frozen-inputs.md` |
| F1 逐问/共享整理 | F0 冻结清单与对应问题授权结果 | `prompts/figure-preparation/question-figure-curator.md`；共享结果用同 prompt 的 shared brief | `figure-prep/questions/qN/` 或 `figure-prep/cross-question/shared/` |
| F2 流式复核 | 对应问题/共享单元已落盘的 package、数据包、来源与代码 | `prompts/figure-preparation/figure-evidence-auditor.md`；创建新 subagent | `<unit_root>/review.md`，其中 `<unit_root>` 为 `figure-prep/questions/qN/` 或 `figure-prep/cross-question/shared/` |
| F2R 原 Curator 回应 | 对应 F2 review 与原 package | `prompts/figure-preparation/question-curator-response.md`；复用原 Curator | `<unit_root>/response.md`，旧版本保留 |
| F3 跨问整合 | 全部逐问 review/response、题间接口与章节最小地图 | `prompts/figure-preparation/figure-chapter-integrator.md`；创建新 subagent | `figure-prep/figure-plan.md`、`figure-prep/figure-preparation-handoff.md`（Integrator 唯一内容 owner） |
| F4 交接 | figure plan、候选数据包、诊断索引、change request 与章节地图 | 无；Leader 只核对条件、处理回滚和宣布汇合 | 已由 Integrator 写入的 `figure-prep/figure-preparation-handoff.md` |

图表支线只导出诊断证据、逐图数据和图型/论文位置建议，不生成正式论文图、视觉评分、样式文件或审美迭代。诊断发现上游问题时写 change request，由 Leader 返回最早受影响阶段；Curator 和 Auditor 永久不能修改 `data/`、`modeling/`、`validation/` 或论文正文。

### 3.5.1 正式论文绘图 FR0–FR4

| 做到这个阶段 | Leader 必读 | 派发给 subagent 的 prompt | 主要模板或产物 |
|---|---|---|---|
| 正式绘图启动 | `Workflow/formal-figure-rendering.md`、`Workflow/formal-figure-team.json`、`prompts/formal-figures/leader.md` | `prompts/formal-figures/worker-base.md` | `templates/formal-figures/task-brief.md` |
| FR0 冻结/模型记录 | F4 handoff/plan、数据包、claim、chapter map、官方版心 | 无；Leader 执行 | frozen-inputs、`scope/dispatch-log.json` |
| FR1 逐问/共享产图 | 本单元冻结包与共享 visual system | `prompts/formal-figures/question-visual-producer.md`；每问/共享单元新 subagent | visual-plan、contracts、pilot、render.py、v1 PNG/PDF/SVG |
| FR2 全篇图审 | 全部 v1、冻结数据、章节和版心 | `prompts/formal-figures/figure-portfolio-reviewer.md`；fresh-context 新 subagent | `formal-figures/figure-review.md` |
| FR2R 原 Producer 修订 | 对应 review、v1 和冻结包 | 复用原 Question Visual Producer | response、final PNG/PDF/SVG |
| FR3 真实版面关闭 | final 图、full-paper-v2、figure-table-slots、预览 | 复用原 Portfolio Reviewer，只关闭原问题 | figure-review-closure、contact/in-paper preview |
| FR4 正式图交接 | 全部 final、review/closure、未决请求 | 无；Leader 执行 | coverage map、manifest、placement/caption handoff、figure-rendering-handoff |

所有新 Producer 和 Reviewer 必须显式用 `model=gpt-5.6-sol`、`reasoning_effort=high`、`fork_turns=none` 创建；默认 Luna 禁止，不能静默降级。Leader 将请求配置写入 dispatch-log。只有两类 subagent：Producer 负责规划/绘制/回应，Reviewer 统一审准确性、图型、审美和版面。

### 3.6 章节材料包与竞赛论文框架

| 做到这个阶段 | Leader 必读 | 派发给 subagent 的 prompt | 主要模板或产物 |
|---|---|---|---|
| 论文准备启动 | `Workflow/paper-preparation.md`、`Workflow/paper-preparation-team.json`、`prompts/paper-preparation/leader.md` | `prompts/paper-preparation/worker-base.md` | `templates/paper-preparation/task-brief.md` |
| CP0 输入冻结 | 候选汇报、真实人工模型决定、validation handoff/claim map、route evidence、引用状态、官方要求、授权结果、工程文稿与图表状态 | 无；Leader 执行 | `templates/paper-preparation/frozen-inputs.md` → `paper-prep/scope/frozen-inputs.md` |
| CP1 最小骨架 | CP0、题意基线和题间接口 | `prompts/paper-preparation/paper-structure-architect.md`；新 subagent | chapter-map-v0、narrative-spine、page-budget |
| CP2 逐问材料 | CP0、chapter-map-v0 与本问授权证据 | `prompts/paper-preparation/question-chapter-curator.md`；每问新 subagent | `paper-prep/questions/qN/chapter-material-v1.md` |
| CP3 证据审查 | 本问 v1、冻结证据与接口 | `prompts/paper-preparation/chapter-evidence-auditor.md`；新 subagent | `paper-prep/questions/qN/evidence-review.md` |
| CP3R 原 Curator 回应 | v1、review 与授权证据 | `prompts/paper-preparation/chapter-curator-response.md`；复用原 Curator | evidence-response 与 chapter-material-v2 |
| CP4 全文整合 | 全部逐问已审材料、图表交接和 CP1 | `prompts/paper-preparation/paper-framework-integrator.md`；新 subagent | chapter-map-v1、全局注册表、paper-framework-v1 |
| CP5 双遍竞赛审读 | 第一遍只读题目/官方要求/框架/材料；第二遍才增加国奖蒸馏 | `prompts/paper-preparation/competition-manuscript-reviewer.md`；新 subagent，第二遍和关闭检查复用 | blind review、pattern sweep、closure |
| CP5R 定向修订 | 两份 review、Owner 路由和新逐问版本 | `prompts/paper-preparation/paper-framework-response.md`；复用原 Integrator，事实问题复用原 Curator | framework-response、paper-framework-v2 |
| CP6 框架交接 | v2、closure、全部来源与未决请求 | 复用原 Integrator | `templates/paper-preparation/paper-framework-handoff.md` → `paper-prep/paper-framework-handoff.md` |

论文准备只交付可直接成文的段落级材料和框架。Evidence Auditor 与 Competition Reviewer 必须是不同新 Agent；国奖论文蒸馏只在 blind review 落盘后暴露。模块不得生成完整论文、正式图片、排版、审美报告或参考文献检索结果。

### 3.7 正式论文写作与全文组装

| 做到这个阶段 | Leader 必读 | 派发给 subagent 的 prompt | 主要模板或产物 |
|---|---|---|---|
| 正式写作启动 | `Workflow/paper-writing.md`、`Workflow/paper-writing-team.json`、`prompts/paper-writing/leader.md` | `prompts/paper-writing/worker-base.md` | `templates/paper-writing/task-brief.md` |
| PW0 输入冻结 | paper framework、figure handoff、references handoff/references.bib、validation claim map、官方要求 | 无；Leader 执行 | `paper-writing/scope/frozen-inputs.md` |
| PW1 写作计划 | PW0、章节地图、符号和表图计划 | 无；Leader 执行 | writing-plan、section-contracts、prose-boundary、figure-table-slots |
| PW2 逐问正文 | 本问 contract、最终材料、授权证据和全局术语 | `prompts/paper-writing/question-manuscript-writer.md`；每问新 subagent | `sections/qN/section-v1.md` |
| PW3 全文 v1 | 全部 section-v1 与公共章节材料 | 无；Leader 是唯一全文作者 | `manuscript/full-paper-v1.md` |
| PW4 事实审查 | v1、validation/figure 来源 | `prompts/paper-writing/full-paper-fact-auditor.md`；新 subagent | `reviews/fact-consistency-review.md` |
| PW4R 事实修订 | 本问 review、v1 与来源 | `prompts/paper-writing/question-manuscript-response.md`；复用原 writer；Leader重组 | section response/v2、fact-response、full-paper-v2 |
| PW5 三路审查 | 同一冻结 v2；peer review 和 Leader 辩护隐藏 | Competition/Coherence/AI 三个 prompt；三个新 subagent | 三份独立 review |
| PW5R Leader 修订 | 三份 review 与 owner response | 无；Leader 综合 | language-review-response、full-paper-v3 |
| PW6 关闭检查 | v3、原 review 与 response | 复用原四个 Reviewer，只关闭原问题 | `reviews/closure/` 四份 memo |
| PW7 正式交接 | v3、closures、未完成交付项 | 无；Leader 独写 | final-paper、formal-paper-handoff |

Markdown 是唯一正文源。只有 Leader 可以写 `paper-writing/manuscript/` 和最终 handoff；Question Writer 只写本问 section，四个 Reviewer 永久只写修改单。不得创建 AI 检测分数、机械文风脚本、自动改写、Word/LaTeX、正式图片、引用检索或提交包。

### 3.8 最终排版、终审与人工交付

| 做到这个阶段 | Leader 必读 | 派发给 subagent 的 prompt | 主要模板或产物 |
|---|---|---|---|
| 最终交付启动 | `Workflow/final-delivery.md`、`Workflow/final-delivery-team.json`、`prompts/final-delivery/leader.md` | `prompts/final-delivery/worker-base.md` | `templates/final-delivery/task-brief.md` |
| FD0 输入冻结 | 候选汇报、真实人工模型决定、formal-paper handoff、最终正文、figure-rendering handoff/manifest、references handoff/references.bib、授权结果/代码和官方要求 | 无；Leader 执行 | `final-delivery/scope/frozen-inputs.md` |
| FD1 支撑材料 | FD0 白名单中的结果数据、实际运行脚本和 run 证据 | `prompts/final-delivery/supporting-material-curator.md`；新 subagent | results、两个 manifest、execution-order、完整 `source-code.md`、supporting-materials |
| FD2 候选组装 | 冻结正文、图、引用与 FD1 | `prompts/final-delivery/submission-typesetter.md`；新 subagent | source、candidate、typesetting-memo |
| FD3 机械预检/冻结 | 候选文件与官方机械规则 | 复用原 Typesetter 只修机械问题；Leader 写快照 | preflight-report、`scope/candidate-snapshot.md` |
| FD4 五路终审 | 同一 candidate snapshot；peer review/Leader 辩护隐藏 | Layout、Answer Relevance、Prose & Engineering Style、Delivery Evidence、End-to-End Consistency 五个 prompt；五个新 subagent，第五个使用 fresh context | `final-delivery/reviews/` 五份独立报告 |
| FD5 问题索引 | 五份原始 review | 无；Leader 只建立索引，不改候选 | `human-review/issue-index.md` |
| FD6 人工包 | 问题索引、官方规则和事实锁定 | 无；Leader 执行 | human-finalization-guide、submission-checklist |
| FD7 人工交接 | 全部冻结文件、review 和未决项 | 无；Leader 执行 | `final-delivery/final-delivery-handoff.md` |

FD4 开始后，`source/`、`candidate/`、`supporting-materials/` 和全部上游永久只读。不创建 response、closure 或自动修订任务；状态为 `AWAITING_HUMAN_FINALIZATION`，实际微调和投稿由人完成。

## 4. 派工合同

每个 worker task 由以下内容组成：

```text
当前模块 worker-base
+ 当前角色 prompt
+ 本轮开放 task brief
```

Task brief 必须明确：

- 当前阶段、角色和唯一目标；
- 允许读取的文件；
- 为保持独立不得读取的文件；
- 唯一主 Markdown 输出路径；
- 额外允许写入的工程路径，默认没有；
- A/B/C/D 最低责任；
- 路线任务还必须写明宽候选责任、禁止伪多样性、文献扩展时点和不得提前替用户收敛；
- 建模任务还必须写明问题/共享构建单元、真实人工模型决定、授权候选边界、build contract、开发反馈、保留信息、父运行/分支、代码 owner、调整权限与预算；
- 验证任务还必须写明冻结主张/模型/结果版本、已用开发反馈、可见/禁止保留信息、暴露对象、probe 写入根、原 owner 和复验预算；
- 图表任务还必须写明问题/共享结果单元、冻结结果和版本、诊断图与论文候选的边界、数据包导出写入根、review/response 路径、章节依赖、是否允许共享结果读取以及禁止修改的上游目录；
- 正式绘图任务还必须记录显式 `gpt-5.6-sol + high + fork_turns=none` 请求、Figure ID、冻结数据包/claim、图量覆盖、style-owner 权限、pilot/final 边界、唯一写入根、真实版心和迭代预算；
- 论文准备任务还必须写明问题/全篇单元、材料版本、验证授权范围、唯一 owner、正文/附录边界、图表状态、两遍竞赛审读的上下文隔离、国奖蒸馏暴露时点和禁止生成完整论文；
- 正式写作任务还必须写明全文/section 版本、唯一主稿 owner、逐问 contract、技术术语与工程词边界、Figure/Table 占位、Reviewer 只读权限、peer review 隔离和禁止生成非 Markdown 交付；
- 最终交付任务还必须写明冻结候选/官方规则、结果与运行脚本白名单、支撑材料写入根、排版可改与事实不可改边界、FD4 同快照隔离审查、第五路可读的精确全链路 handoff、终审后零 Agent 修改和人工接管状态；
- 文献任务还必须写明路线/候选/主题、检索问题、来源优先级、元数据/摘要/全文状态、负面搜证、候选外模型发现、Zotero 权限、真实人类咨询状态、BibTeX 写权和禁止编造来源；
- 停止条件和禁止越权事项。

派工时必须告诉 worker：

> 最低问题不是输出白名单。除指定问题外，继续完整报告任何可能改变题意、数据边界、题间接口、风险或路线的新发现。只写入 task brief 明确分配的路径。

所有 subagent 共享工作区。允许输入是读取白名单；不能通过目录遍历、搜索或历史输出阅读未授权报告。

## 5. 创建、复用与等待

- 新视角、隔离盲读、独立攻击和独立复核：创建新的 subagent。
- 原判断角色复核：复用提出该判断的 W1/W2 subagent。
- 路线提案者回应：复用原 Route A/B subagent。
- W5C 后由 Leader 独写候选模型汇报并进入 H1；不创建“人工决策 Agent”。只有真实用户回复才能由 Leader 忠实记录为 `routes/human-model-decision.md`。
- 数据实现者修订：复用原 D3 数据管道实现者。
- 每问首次模型实现和首次高影响诊断：创建新的 subagent。
- 模型实现者回应、获批调整重跑和跨问接口交接：复用对应原 model builder。
- V1 三视角审计和强题间依赖的 V6 整体审计：创建新 subagent。
- V3 获批 probe：复用提出该问题的 auditor；V4 证据回应：复用受影响的原 model/data builder。
- builder 看到过某份保留证据后的最终复验：换新独立证据，需 fresh context 时创建新 auditor。
- F1 每问或共享结果单元：创建一个新的 Question Figure Curator；不按候选图数量复制 owner。
- F2 每个问题 package 落盘后：立即创建新的 Figure Evidence Auditor，不等待其他问题。
- F2R：复用产生该 package 的原 Curator，使用 response prompt 做一次集中回应。
- F3：所有逐问 package 完成且章节最小地图可用后，创建新的 Figure–Chapter Integrator。
- F0 和冻结清单由 Leader 写；F3 Integrator 独自写 `figure-plan.md` 与最终 handoff；F4 Leader 只核对条件、处理回滚和宣布汇合。
- FR1 每问/真实共享单元创建一个显式 sol-high Question Visual Producer，不按 Figure ID 拆 Agent；指定一个 Producer 兼任 style owner。FR2 创建一个 fresh-context sol-high Portfolio Reviewer；FR2R 复用原 Producer，FR3 复用原 Reviewer；FR4 由 Leader 写 manifest 和 handoff。
- CP1：创建新的 Paper Structure Architect；chapter-map-v0 落盘后立即提供给 F3。
- CP2/CP3：每问创建一个新 Question Chapter Curator；每个 v1 完成立即创建新的 Chapter Evidence Auditor，不等待其他问题。
- CP3R：复用产生 v1 的原 Curator，一次集中形成 response 和 v2。
- CP4：创建新的 Paper Framework Integrator；CP5 创建新的 Competition Manuscript Reviewer。
- CP5 第一遍完成并落盘 blind review 后，才向同一 Reviewer 暴露国奖论文蒸馏材料；关闭检查继续复用该 Reviewer。
- CP5R/CP6：事实问题复用对应原 Curator；全篇结构修订与最终 handoff 复用原 Integrator。
- PW2：每问创建一个新 Question Manuscript Writer，不按段落拆 Agent；PW4R 复用该问题原 writer。
- PW3/PW5R/PW7：由当前 Leader独写全文主稿、全局 response 和最终 handoff，不创建全文写作 subagent。
- PW4：创建新 Full-Paper Fact Auditor；PW5 创建三个互相隔离的新 Competition/Coherence/AI Reviewer，三者审同一冻结 v2。
- PW6：复用原四个 Reviewer，只检查原 review 的处理，不新增全面审稿轮次。
- REF1 每条路线创建新 Scout；REF2 Human Recorder 在真实回复到达后复用，未回复时不得模拟；REF3 创建新 Literature Auditor。
- REF4 创建新 Citation Gap Analyst；REF5 每独立主题簇创建新 Citation Scout；REF6 创建新 Citation Auditor。最终 BibTeX 与 references handoff 由 Leader 根据 review 整理。
- 无独立输入或只会重复已有报告：不创建 Agent。
- W/D/M/V 原有波次仍最多并行 3 个 worker；图表、正式绘图、论文准备、PW2、FD4 和文献 Scout 不设固定数字上限，只能按独立问题/路线/主题簇、独立写入路径和平台容量并行，不能按单图、单篇论文或单条引用重复派 owner。
- Leader 保存 Agent 句柄；W/D/M/V 同步波全部返回、失败或取消后才综合，图表 F2 与论文 CP3 按问题流式独立复核；PW5 三份 review 全部落盘后才进入 Leader 修订。
- subagent 完成后先确认指定文件已经落盘；聊天摘要不能替代原始 memo。

## 6. Leader 的判断纪律

- 不投票，不按角色数量或措辞信心决策。
- 优先看题面/模板直接证据、附件事实、区分性观察、全题接口和可逆性。
- 暂定结论必须带适用边界、保留分支和重开触发器。
- 纯文字争议只允许一次攻击和一次回应；之后取证、分支、暂定或升级用户。
- 高影响且不可判、又会造成不可逆路线差异的问题交给用户。
- 无法放入既有分类的新发现必须原文保留或链接到原始 memo。
- 机械检查只确认文件、哈希、版本、路径和可复现事实，不裁决语义正确性。
- 建模调整按 L0 实现修复、L1 合同内计算调整、L2 构建合同升版、L3 上游变更请求处理；不能用代码改动大小代替语义定级。
- 人工模型决定是模型家族边界。后续 Agent 可在合同内实现和调整，但不得因实现方便静默换模型；改变模型家族、目标或核心结构必须写 `routes/change-requests/` 并重新进入 H1。
- 只在存在高价值不确定性且有可负担、有区分力的下一动作时继续 M4；否则保留分支或交给后续验证。
- 验证按具体主张记录可引用、有条件可引用、暂不可引用、证据反驳或上游失效；不对整个模型做虚假通过判定。
- 只在高影响不确定性和有区分力、可负担的 probe 同时存在时继续 V3–V5；否则限制主张或上游重开。
- 每次向 builder 暴露验证信息后更新 exposure ledger；已消耗 holdout 不得重用为独立证据。

## 7. 文件所有权与版本

- 原始题面、附件、说明和模板永久只读。
- W/D/M/V 与前半程 worker 只拥有 task brief 指定的唯一 memo；D3/D4R 与模型 builder/获批 response 仅可额外修改明确列出的工程路径。图表和论文 Curator 是 artifact-bundle 例外，只拥有 brief 指定的独立单元根；Auditor、response 和 Integrator 仍受明确子路径限制。
- `submissions/`、`reviews/`、`routes/responses/` 与数据 review 原文只追加、不覆盖。
- `routes/model-candidate-briefing.md` 只由 Leader 写；`routes/human-model-decision.md` 只能忠实记录真实用户回复。Agent 不得代签、猜测或把 REF2 咨询/沉默当成 H1 批准。
- Leader 综合必须链接其依据的全部原始报告。
- 旧报告、失败代码、旧数据版本和被替换产物不删除；新版本说明影响范围。
- 每问模型代码、shared kernel 和 M5 适配代码分别只有一个 Leader 指定 owner；diagnostician 只读。
- V1/V6 auditor 只写自己的原报告；V3 auditor 仅额外拥有获批 `validation/probes/PROBE-ID/`，永久不拥有上游数据或模型实现。
- V4 原 owner 在 Leader 裁决前只写 response；V0/V2/V5 与 validation 模块的最终 claim map/handoff 只由 Leader 写。
- F1 Curator 只写自己的 `figure-prep/questions/qN/` 或 `figure-prep/cross-question/shared/`；诊断代码和数据不得写回上游目录。
- F2 Auditor 只写对应单元的 review；F2R 原 Curator 只写 response 和明确授权的新 package 版本；F3 Integrator 只写 `figure-prep/cross-question/integration/`，并且是 `figure-plan.md` 与 `figure-preparation-handoff.md` 的唯一内容 owner；F4 Leader 只核对条件、处理回滚和宣布汇合。
- 图表支线的所有上游结果、数据、模型、验证交接和论文正文均只读；正式绘图模块只能读取 F4 最终 handoff 和 FR0 白名单。
- FR1 Producer 只写自己的 `formal-figures/questions/qN/` 或 shared unit；仅指定 style owner 可写 `style/`。FR2 Reviewer 只写 figure-review，FR3 只写 closure；FR4 coverage、manifest 与 rendering handoff 只由 Leader 写。全部上游和论文主稿只读。
- CP1 Structure Architect 只写 structure v0；CP2/CP3/CP3R 分别只写本问 material、evidence review 和版本化 response/material。
- CP4 Integrator 只写 `paper-prep/structure/`、`shared/` 与 `integration/` 获批文件，不能改逐问事实；Competition Reviewer 只写三份 review。
- CP5R 的事实修订只由原 Question Curator 完成，全篇框架和 `paper-framework-handoff.md` 只由原 Integrator完成；Leader 只核对、回滚和宣布交接。
- 论文准备的 `data/`、`modeling/`、`validation/`、`figure-prep/` 和国奖蒸馏原件均只读。
- `paper-writing/manuscript/`、`responses/` 和 `formal-paper-handoff.md` 只有 Leader 可写；逐问 writer 只拥有自己的 `sections/qN/`。
- PW4/PW5 四个 Reviewer 只写各自 review；Reviewer 不得修改 section、manuscript、response 或上游材料，也不得读取 peer review。
- PW4R 事实修改复用原问题 writer；PW5R 全文结构、摘要结论、过渡和统一文风只由 Leader 修改。
- FD1 Curator 只写 `final-delivery/supporting-materials/`；FD2/FD3 Typesetter 只在候选冻结前写 `source/`、`candidate/`、preflight 和 typesetting memo。
- FD4 五个 Reviewer 各自只写一份 review；End-to-End Consistency Auditor 可额外读取 FD0 冻结的全链路 handoff，但不读 peer review。candidate snapshot 冻结后任何 Agent 不得修改正文、候选稿、支撑材料或上游文件。
- FD5–FD7 只有 Leader 可写问题索引、人工指南、提交清单和 handoff；Leader 不得创建审后修订版或代替人提交。
- Route/Citation Scout 只写 Leader 预分配 REF-ID 下的 source notes、自己的 memo 和主题候选 BibTeX；共享 references-candidate.bib 由 Leader 合并。Literature/Citation Auditor 只写 review，不修改来源或 BibTeX。
- Human Recorder 只能记录真实回复；`route-evidence-handoff.md`、`references.bib`、`claim-to-citation-map.md` 和 `references-handoff.md` 由 Leader 独写。未获授权时 Zotero 库只读。
- JSON 只保存配置、路径、哈希、版本、状态和运行参数；语义内容写开放 Markdown。

## 8. 失败、重开与停止

- worker 未返回：同角色重试一次；仍失败则记录缺失，不由 Leader 冒充独立意见。
- memo 偏离角色：向原 subagent 发一次补充任务，另存追加 memo。
- 快速共识：创建新的 fresh-context reviewer，不把历史票数和 Leader 辩护写入 prompt。
- 字段语义、目标可构造性、总体、粒度、单位或题间接口被推翻：回到最早受影响阶段。
- 模型需要新数据或改变目标/总体/标签/时点/接口时，写 L3 上游变更请求；不得直接修改共享数据。
- 数据或建模证据要求改变人工选择的模型家族、目标或核心结构时，写 `templates/model-selection-change-request.md`，状态回到 `AWAITING_HUMAN_MODEL_DECISION`；收到真实新决定前不得实施替代模型。
- 高影响模型异常先隔离诊断；diagnosis 落盘前不得向诊断者泄露 builder 的事后归因和建议改法。
- 非平凡模型调整先写 adjustment card；旧 run、失败调整和被替换合同保留并标记失效传播。
- 验证发现需修改时，由 Leader 发上游变更请求，validator 不得直接修改 `data/` 或 `modeling/`。
- 修正后只重验受影响主张及下游；若原 owner 已看到原 holdout，先换新独立证据。
- 图表 worker 未返回时，同角色重试一次；仍失败则记录该问题缺失，不由 Leader 冒充独立复核。单个问题 package 失败不拖延其他独立问题。
- 图表数据包不可复算或 claim 不获授权时，暂停该候选并保留旧版本；不得为了满足图表数量强行交接。
- F4 只有在逐问 package/review/response、change request 裁决和 `figure-plan.md` 对齐章节地图后才能交接；结果章节不得在这些条件缺失时标记定稿。
- `figure-prep/figure-preparation-handoff.md` 是主 harness 的图表停止点；正式论文图、审美审查、版式迭代、答卷和论文正文不由本支线自动创建。
- 正式绘图新 subagent 未显式请求 `gpt-5.6-sol + high + fork_turns=none` 时不得启动；覆盖不可用时停止并报告，不得使用默认 Luna。图数据/claim 问题返回 F/V/M/D，纯审美默认一轮修订后停止。
- `formal-figures/figure-rendering-handoff.md` 是正式绘图停止点；FD0 只消费 manifest 授权 final，不从散乱图片目录挑图。
- CP6 只有在逐问 evidence review/response、双遍竞赛审读、定向修订、一次关闭检查和高影响 change request 处置完成后才能交接。
- `paper-prep/paper-framework-handoff.md` 是论文准备停止点；完整论文、参考文献检索、正式图、排版和提交包不由本模块创建。
- PW7 只有在 fact review/response、三路语言 review、Leader v3 和四份关闭检查完成后才能交接。
- `paper-writing/formal-paper-handoff.md` 是正式写作停止点；Word/LaTeX、正式图片、参考文献检索、排版、答卷和提交包仍不创建。
- L2 前必须完成 REF3 route-evidence-handoff、Leader 候选汇报和 H1 真实人工模型决定；没有决定时停在 `AWAITING_HUMAN_MODEL_DECISION`。CP4/CP6/PW0 前必须完成 REF6 references-handoff、claim-to-citation map 和 references.bib。未核验来源保留 citation-needed，不得虚构。
- `final-delivery/final-delivery-handoff.md` 是最终交付停止点；FD4 后问题只报告不自动修改，状态必须为 `AWAITING_HUMAN_FINALIZATION`，实际微调和投稿由人完成。

验证后可并行进入图表、论文和 REF4–REF6 引用准备；F4 后正式绘图与 CP/PW 并行。figure-prep、paper framework 与 references handoff 齐备后可进入正式写作；只有 `figure-rendering-handoff.md`、引用交接、结果数据/代码和官方要求齐备时才能显式启动 FD0；FD7 后 Leader 不得继续自动修稿或投稿。
