# C 题 Agent Team：Leader 运行规则

当前主 Agent 自动担任唯一 Leader，直接创建和复用原生 subagent。不要实现独立 orchestrator、队列服务或语义 JSON schema。前半程、数据工程、建模构建和独立验证由同一个 Leader 连续管理；V6 后并行运行图表准备与论文准备，再进入正式论文写作。正式绘图、排版、引用检索和提交包仍不在本 harness 内。

详细波次、角色输入、prompt 路径和输出路径以 `Workflow/README.md` 为准。本文件只规定 Leader 应怎样工作，以及做到某阶段必须读取哪些文件。

## 1. Leader 的职责

Leader 负责：

- 识别当前阶段和唯一目标；
- 按本文件的路由读取协议、配置、Leader prompt、角色 prompt 和模板；
- 为每个 subagent 创建开放 task brief，明确允许/禁止上下文和唯一输出路径；
- 创建新视角 Agent，复用需要保持原判断连续性的 Agent；
- 保存原始 memo 和 subagent 句柄；
- W/D/M/V 与前半程同步波等待本波全部任务返回、失败或取消后再综合；图表、论文准备和 PW2 按独立问题推进，PW5 三个 Reviewer 同波等齐后由 Leader 综合；
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
2. 当前模块配置：前半程 `Workflow/team.json`，数据工程 `Workflow/data-team.json`，建模构建 `Workflow/modeling-team.json`，独立验证 `Workflow/validation-team.json`，图表准备 `Workflow/figure-preparation-team.json`，论文准备 `Workflow/paper-preparation-team.json`，正式写作 `Workflow/paper-writing-team.json`；
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
→ W5A/W5B/W5C 路线竞标、审查与回应
→ L2 路线交接
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
⇉ F1 逐问诊断与数据整理 / CP2 逐问章节材料
→ F2/F2R 图表证据复核与回应
→ CP3/CP3R 章节证据复核与回应
→ F3/F4 图表整合与交接
→ CP4 全文框架整合
→ CP5 双遍竞赛论文独立审读
→ CP5R 定向修订与关闭检查
→ CP6 论文框架交接
→ PW0/PW1 正式写作冻结与 Leader 写作计划
⇉ PW2 每问正式章节
→ PW3 Leader 全文组装 v1
→ PW4/PW4R 事实审查与修订
⇉ PW5 竞赛表达 / 全文连贯 / AI 文风三路独立审查
→ PW5R Leader 统一修订
→ PW6 四角色关闭检查与事实回归
→ PW7 正式论文 Markdown 交接
```

前半程在 `routes/route-handoff.md` 停止；数据工程、建模、验证、图表和论文准备分别止于自己的 handoff。PW0 只能在 `paper-framework-handoff.md` 与 `figure-preparation-handoff.md` 落盘后显式启动，停止于 `paper-writing/formal-paper-handoff.md`。随后由外部/后续模块负责正式绘图、引用检索、排版和提交包。

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
| W5A 路线竞标 | `Workflow/protocols/route-tournament.md` | Route A/B 均用 `prompts/roles/route-proposer.md`，相互隔离 | `templates/route-proposal.md` → `routes/route-a.md`、`routes/route-b.md` |
| W5B 路线审查 | 题意基线与 A/B 原报告 | `prompts/roles/route-critic.md` | `templates/route-review.md` → `routes/route-review.md` |
| W5C 路线提案者回应 | 路线评审与各自原路线 | `prompts/roles/route-proposer-response.md`，复用原 A/B subagent | `routes/responses/` |
| L2 路线交接 | `Workflow/protocols/route-tournament.md` 与全部路线 memo | 无；Leader 综合 | `templates/route-handoff.md` → `routes/route-handoff.md` |

### 3.2 数据工程

| 做到这个阶段 | Leader 必读 | 派发给 subagent 的 prompt | 主要模板或产物 |
|---|---|---|---|
| 数据模块启动 | `Workflow/data-engineering.md`、`Workflow/data-team.json`、`prompts/data-engineering/leader.md` | `prompts/data-engineering/worker-base.md` | `templates/data-engineering/task-brief.md` |
| D0 接收与模式选择 | `synthesis/problem-baseline.md`、`routes/route-handoff.md`、相关前半程原始 memo | 无；Leader 执行 | 完整模式 brief；精简模式另写 `data/decisions/lean-mode-rationale.md` |
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
| M0 问题编排 | 三份上游交接与相关原始 memo | 无；Leader 执行 | `templates/modeling/question-map.md` → `modeling/question-map.md` |
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
| V0 验证冻结 | 题意/路线/数据/建模交接与官方要求 | 无；Leader 执行 | `templates/validation/validation-map.md`、`templates/validation/validation-exposure-ledger.md` |
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

### 3.6 章节材料包与竞赛论文框架

| 做到这个阶段 | Leader 必读 | 派发给 subagent 的 prompt | 主要模板或产物 |
|---|---|---|---|
| 论文准备启动 | `Workflow/paper-preparation.md`、`Workflow/paper-preparation-team.json`、`prompts/paper-preparation/leader.md` | `prompts/paper-preparation/worker-base.md` | `templates/paper-preparation/task-brief.md` |
| CP0 输入冻结 | validation handoff/claim map、官方要求、授权结果、工程文稿与图表状态 | 无；Leader 执行 | `templates/paper-preparation/frozen-inputs.md` → `paper-prep/scope/frozen-inputs.md` |
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
| PW0 输入冻结 | paper framework、figure handoff、validation claim map、官方要求 | 无；Leader 执行 | `paper-writing/scope/frozen-inputs.md` |
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
- 建模任务还必须写明问题/共享构建单元、build contract、开发反馈、保留信息、父运行/分支、代码 owner、调整权限与预算；
- 验证任务还必须写明冻结主张/模型/结果版本、已用开发反馈、可见/禁止保留信息、暴露对象、probe 写入根、原 owner 和复验预算；
- 图表任务还必须写明问题/共享结果单元、冻结结果和版本、诊断图与论文候选的边界、数据包导出写入根、review/response 路径、章节依赖、是否允许共享结果读取以及禁止修改的上游目录；
- 论文准备任务还必须写明问题/全篇单元、材料版本、验证授权范围、唯一 owner、正文/附录边界、图表状态、两遍竞赛审读的上下文隔离、国奖蒸馏暴露时点和禁止生成完整论文；
- 正式写作任务还必须写明全文/section 版本、唯一主稿 owner、逐问 contract、技术术语与工程词边界、Figure/Table 占位、Reviewer 只读权限、peer review 隔离和禁止生成非 Markdown 交付；
- 停止条件和禁止越权事项。

派工时必须告诉 worker：

> 最低问题不是输出白名单。除指定问题外，继续完整报告任何可能改变题意、数据边界、题间接口、风险或路线的新发现。只写入 task brief 明确分配的路径。

所有 subagent 共享工作区。允许输入是读取白名单；不能通过目录遍历、搜索或历史输出阅读未授权报告。

## 5. 创建、复用与等待

- 新视角、隔离盲读、独立攻击和独立复核：创建新的 subagent。
- 原判断角色复核：复用提出该判断的 W1/W2 subagent。
- 路线提案者回应：复用原 Route A/B subagent。
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
- 无独立输入或只会重复已有报告：不创建 Agent。
- W/D/M/V 原有波次仍最多并行 3 个 worker；图表、论文准备和 PW2 不设固定数字上限，只能按独立问题/共享单元、独立写入路径和平台容量并行，不能重复派 owner。
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
- 只在存在高价值不确定性且有可负担、有区分力的下一动作时继续 M4；否则保留分支或交给后续验证。
- 验证按具体主张记录可引用、有条件可引用、暂不可引用、证据反驳或上游失效；不对整个模型做虚假通过判定。
- 只在高影响不确定性和有区分力、可负担的 probe 同时存在时继续 V3–V5；否则限制主张或上游重开。
- 每次向 builder 暴露验证信息后更新 exposure ledger；已消耗 holdout 不得重用为独立证据。

## 7. 文件所有权与版本

- 原始题面、附件、说明和模板永久只读。
- W/D/M/V 与前半程 worker 只拥有 task brief 指定的唯一 memo；D3/D4R 与模型 builder/获批 response 仅可额外修改明确列出的工程路径。图表和论文 Curator 是 artifact-bundle 例外，只拥有 brief 指定的独立单元根；Auditor、response 和 Integrator 仍受明确子路径限制。
- `submissions/`、`reviews/`、`routes/responses/` 与数据 review 原文只追加、不覆盖。
- Leader 综合必须链接其依据的全部原始报告。
- 旧报告、失败代码、旧数据版本和被替换产物不删除；新版本说明影响范围。
- 每问模型代码、shared kernel 和 M5 适配代码分别只有一个 Leader 指定 owner；diagnostician 只读。
- V1/V6 auditor 只写自己的原报告；V3 auditor 仅额外拥有获批 `validation/probes/PROBE-ID/`，永久不拥有上游数据或模型实现。
- V4 原 owner 在 Leader 裁决前只写 response；V0/V2/V5 与 validation 模块的最终 claim map/handoff 只由 Leader 写。
- F1 Curator 只写自己的 `figure-prep/questions/qN/` 或 `figure-prep/cross-question/shared/`；诊断代码和数据不得写回上游目录。
- F2 Auditor 只写对应单元的 review；F2R 原 Curator 只写 response 和明确授权的新 package 版本；F3 Integrator 只写 `figure-prep/cross-question/integration/`，并且是 `figure-plan.md` 与 `figure-preparation-handoff.md` 的唯一内容 owner；F4 Leader 只核对条件、处理回滚和宣布汇合。
- 图表支线的所有上游结果、数据、模型、验证交接和论文正文均只读；外部绘图模块也只能读取最终 handoff。
- CP1 Structure Architect 只写 structure v0；CP2/CP3/CP3R 分别只写本问 material、evidence review 和版本化 response/material。
- CP4 Integrator 只写 `paper-prep/structure/`、`shared/` 与 `integration/` 获批文件，不能改逐问事实；Competition Reviewer 只写三份 review。
- CP5R 的事实修订只由原 Question Curator 完成，全篇框架和 `paper-framework-handoff.md` 只由原 Integrator完成；Leader 只核对、回滚和宣布交接。
- 论文准备的 `data/`、`modeling/`、`validation/`、`figure-prep/` 和国奖蒸馏原件均只读。
- `paper-writing/manuscript/`、`responses/` 和 `formal-paper-handoff.md` 只有 Leader 可写；逐问 writer 只拥有自己的 `sections/qN/`。
- PW4/PW5 四个 Reviewer 只写各自 review；Reviewer 不得修改 section、manuscript、response 或上游材料，也不得读取 peer review。
- PW4R 事实修改复用原问题 writer；PW5R 全文结构、摘要结论、过渡和统一文风只由 Leader 修改。
- JSON 只保存配置、路径、哈希、版本、状态和运行参数；语义内容写开放 Markdown。

## 8. 失败、重开与停止

- worker 未返回：同角色重试一次；仍失败则记录缺失，不由 Leader 冒充独立意见。
- memo 偏离角色：向原 subagent 发一次补充任务，另存追加 memo。
- 快速共识：创建新的 fresh-context reviewer，不把历史票数和 Leader 辩护写入 prompt。
- 字段语义、目标可构造性、总体、粒度、单位或题间接口被推翻：回到最早受影响阶段。
- 模型需要新数据或改变目标/总体/标签/时点/接口时，写 L3 上游变更请求；不得直接修改共享数据。
- 高影响模型异常先隔离诊断；diagnosis 落盘前不得向诊断者泄露 builder 的事后归因和建议改法。
- 非平凡模型调整先写 adjustment card；旧 run、失败调整和被替换合同保留并标记失效传播。
- 验证发现需修改时，由 Leader 发上游变更请求，validator 不得直接修改 `data/` 或 `modeling/`。
- 修正后只重验受影响主张及下游；若原 owner 已看到原 holdout，先换新独立证据。
- 图表 worker 未返回时，同角色重试一次；仍失败则记录该问题缺失，不由 Leader 冒充独立复核。单个问题 package 失败不拖延其他独立问题。
- 图表数据包不可复算或 claim 不获授权时，暂停该候选并保留旧版本；不得为了满足图表数量强行交接。
- F4 只有在逐问 package/review/response、change request 裁决和 `figure-plan.md` 对齐章节地图后才能交接；结果章节不得在这些条件缺失时标记定稿。
- `figure-prep/figure-preparation-handoff.md` 是主 harness 的图表停止点；正式论文图、审美审查、版式迭代、答卷和论文正文不由本支线自动创建。
- CP6 只有在逐问 evidence review/response、双遍竞赛审读、定向修订、一次关闭检查和高影响 change request 处置完成后才能交接。
- `paper-prep/paper-framework-handoff.md` 是论文准备停止点；完整论文、参考文献检索、正式图、排版和提交包不由本模块创建。
- PW7 只有在 fact review/response、三路语言 review、Leader v3 和四份关闭检查完成后才能交接。
- `paper-writing/formal-paper-handoff.md` 是正式写作停止点；Word/LaTeX、正式图片、参考文献检索、排版、答卷和提交包仍不创建。

验证后可并行进入图表与论文准备；两个 handoff 完成后才能进入正式写作，并停止于 `paper-writing/formal-paper-handoff.md`。Leader 不得越过该交接自动生成正式图、非 Markdown 文档、排版或提交包。
