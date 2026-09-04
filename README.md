# MCM Harness：C 题全流程自动化建模

[MIT License](LICENSE) · [版权与第三方说明](NOTICE.md) · [贡献指南](CONTRIBUTING.md) · [安全反馈](SECURITY.md) · [更新记录](CHANGELOG.md)

## 我们的用途

`mcm-harness` 面向全国大学生数学建模竞赛 C 题，目标是实现从赛题和附件到模型、验证、图表、论文及提交候选包的全流程自动化建模。它适合探索多 Agent 如何协作完成一整套建模任务，也可用于已有解题流程的分阶段复现、审查与改进。

主 Agent 担任唯一 Leader，使用原生 subagent 分工执行与独立审查，不需要额外调度服务。内置 `$mcm` Skill 提供建模与论文判断指导，Harness 负责阶段推进、上下文隔离、文件所有权、版本和回退。判断依据保留在开放 Markdown 中；JSON 和机械检查不代替语义审查。

自动化覆盖审题、候选模型与文献校准、数据工程、模型实现、独立验证、正式绘图、论文写作和排版终审。最终交付的是论文候选稿、图表与引用、处理后数据和完整代码组成的支撑材料包，以及供人处理的终审问题清单。

**全流程自动化不等于无人值守：模型选择必须由人确认，最终修改与投稿必须由人接管。** 两个人工 gate 的位置和重新触发条件见下文。

## 当前可能的问题与运行成本

项目仍处于探索和迭代中，流程已覆盖不代表各阶段效果已经稳定。

- **模型选择偏保守。** 当前仍可能偏向熟悉、容易实现或验证的模型，对更有潜力但实现成本较高的路线探索不足。宽候选、文献扩展和人工 H1 是约束措施，不代表这一问题已解决；用户应在 H1 主动审查候选是否充分。
- **绘图效果仍不理想。** 即使已有指定样式、两轮视觉迭代和独立审图，成图效果仍可能达不到预期，需要人工复核和调整。文件导出成功、检查通过，不等于图形表达和论文版面足够好。
- **token 与时间消耗较大。** 项目实践记录的全流程开销约为 **8 亿 token、20 小时**。这是维护者提供的经验记录，不是标准化性能基准或固定开销；实际消耗会随题目、模型、上下文、并行度和返工轮次变化。

建议先限定阶段和预算，再决定是否运行全流程；不要把它视作低成本的一键参赛工具，也不要把自动产物直接当作可投稿成品。

## 当前全流程

以下按当前 [AGENTS.md](AGENTS.md) 与 [详细调度手册](Workflow/README.md) 概括；阶段编号用于定位文档，不代表所有模块严格串行。

| 阶段 | 自动执行的工作与交付 |
| --- | --- |
| 审题与候选路线：W0–W5C、L2C | 封存来源，隔离读题、交叉审查与消歧；A/B 提出宽候选，经结构审查和逐候选文献校准后重构路线，Leader 汇报选项、优劣势、成本及推荐。 |
| 人工模型决策：H1 → L2 | 等待真实用户选择主模型及备选、挑战或敏感性路线；Leader 忠实记录决定，再形成路线交接。 |
| 数据工程：D0–D5 | 数据契约、剖析与风险调查，统一清洗和分析视图构建，经独立复现与题间接口审查后交接。 |
| 建模构建：M0–M6 | 数学规格与构建合同、baseline 贯通、主模型实现、触发式诊断和受约束调整、跨问接口装配；交付模型包及与实际实现一致的方法说明。 |
| 独立验证：V0–V6 | 数学实现、实验证据和复现接口审计，定向取证并按具体主张裁决；多问题任务在 V6 先从证据重建可得答案，再对照作者意图与题间接口。 |
| 图表准备：F0–F4 | 从验证授权结果整理诊断证据、逐图数据包、图型建议与章节位置；独立复核后交给正式绘图，不在此阶段生成正式图。 |
| 论文准备：CP0–CP6 | 逐问材料整理与 CP3A 无代码方法重建并行，随后对照复核；从验证后的比较证据重建贡献，经过先盲审、后参考蒸馏经验的两遍审读，交付论文框架。 |
| 正式绘图：FR0–FR4 | 使用指定模型、绘图技能链与 Cassatt2 样式；Producer 完成 v1→v2 自审，独立 Reviewer 审 v2 后由原 Producer 修订为 final，再检查真实正文版面并交接。 |
| 正式写作：PW0–PW7 | 逐问写作、Leader 组装全文、事实审查；PW5A 先只读首页重建读者理解，PW5B 再对照全文，同时进行连贯性和 AI 套话/工程文风审查；修订与关闭检查后交付 Markdown 正文。 |
| 最终交付：FD0–FD7 | 整理处理后数据、结果和完整原始脚本，在参考文献后追加“支撑材料”展示并生成独立 ZIP；候选冻结后进行五路只读终审，最后交付问题索引、人工指南与候选包。 |

文献与引用是贯穿模块：W5A 后的 **REF0–REF3** 搜索支持、反驳、替代与新模型方向，并记录真实咨询；V6/CP1 后的 **REF4–REF6** 补齐引用缺口、审查来源，交付主张—引用对应表及 `references.bib`。咨询不能替代 H1，Agent 不得模拟人的意见或虚构来源。

后半程按依赖并行：V6 后启动图表准备和论文准备，CP1 提供章节地图后推进正式引用；F4 后正式绘图可与论文准备后段和正式写作并行。正式引用交接是 CP4/CP6/PW0 的前置条件，PW0 还需论文框架与图表准备交接；FR3 需事实稳定的全文 v2 做版面检查。正式正文、正式图、引用和结果代码齐备后才进入 FD0。

最近的框架重点是三项独立复核：**V6 检查“证据实际回答了什么” → CP3A 检查“不看代码能否理解并重建方法” → PW5A/PW5B 检查“首页传递的答案与全文是否一致”**。贡献必须由验证后的增量证据支持，不因模型复杂、名字新或范文习惯而自动成立。

## 人工 gate 在哪里

### Gate 1：H1 模型选择，正式数据工程和建模之前

完成候选重构与 L2C 汇报后，流程停在 `AWAITING_HUMAN_MODEL_DECISION`。用户可以选择主模型及备选/敏感性路线、要求补文献或扩展候选、全部否决，或给出时间与实现限制。

只有真实回复才能写入运行目录的 `routes/human-model-decision.md`。没有确认就不能进入 L2、D0 或 M0；Agent 推荐、REF2 咨询、沉默和超时都不算批准。

**H1 可能重新触发：** 后续如果必须改变已授权的模型家族、目标或核心结构，先写变更请求，再等待用户重新决定，不能因实现困难而静默换成更简单的模型。合同内的实现修复和已授权调整不要求每一步都由人确认。

### Gate 2：FD7 人工接管，最终修改和投稿之前

FD3 冻结候选后，FD4 的五个 Reviewer 分别检查排版合规、扣题程度、文风、交付证据和全链路一致性；它们只报告问题，不修改候选。FD5–FD7 由 Leader 汇总问题索引、人工修改指南及交付清单，最终停在 `AWAITING_HUMAN_FINALIZATION`。

此时由人检查未决问题、调整图表与版面、核对竞赛规则并实际投稿。Harness 不自动进行终审后修稿或投稿；如果人工修改涉及数字、模型含义或关键结论，应返回最早受影响的建模/验证阶段复核。

另外，缺失数据、外部技能/模型不可用、权限不足或高影响争议也可能需要用户处理。这些是按条件触发的暂停，不是每个阶段都新增一次人工 gate；H1 与最终人工接管不能被“自动运行”指令跳过。

## 快速开始

clone 仓库，在 Agent 中打开它，然后说“初始化”即可。默认 [Bootstrap](BOOTSTRAP.md) 负责准备材料目录、建立 run、记录来源和执行基础检查，不再要求用户手工拼初始化命令。

1. 获取仓库并进入根目录：

   ```bash
   git clone https://github.com/gdl1605/mcm-harness.git
   cd mcm-harness
   ```

2. 在支持项目 `AGENTS.md` 的 Agent 中打开仓库，使用 Python 3.10+，直接发送：

   ```text
   初始化这个项目。
   ```

3. 将合法取得的赛题和附件放入自动准备的 `raw-sources/`，再说“进行 init”。已有材料也可直接告诉 Agent 文件路径，无需复制。Bootstrap 有材料时默认建立 `run/`；没有材料就提示补充，不冻结空来源 run。重复 init 只核对旧 run，不覆盖或重置进度。这两个默认目录已被 `.gitignore` 排除。

4. 初始化后，要开始解题时发送：

   ```text
   使用当前 run 开始 C 题全流程建模；到 H1 等我选模型，FD7 交给我最终修改和投稿。
   ```

“初始化 / 执行初始化 / 进行 init / bootstrap”都路由到同一入口。只要求初始化时不会自动开始解题；也可说“初始化并开始解题”，但人工 gate 不变。若客户端未自动加载项目规则，先让它读取 `AGENTS.md`；不要与客户端自身的 `/init` 或 `git init` 混淆。

手动入口及多题运行（可选）：

```bash
python3 scripts/bootstrap.py
python3 scripts/bootstrap.py --run-dir runs/case-02 --title "另一道 C 题" --source /path/to/problem.pdf --source /path/to/attachment.xlsx
```

辅助脚本只依赖 Python 标准库，不创建或调度 subagent。Bootstrap 不安装外部技能或所有建模依赖，缺项会按阶段报告；完整流程仍需相应平台能力。原始材料只记录路径和哈希，不修改；生成的 manifest 含本地绝对路径，不要直接公开。Leader 按 [任务模板](templates/task-brief.md) 和 [详细调度手册](Workflow/README.md) 继续派工。

## 依赖与使用边界

- 内置 `.agents/skills/mcm/` 随仓库提供；无需额外安装 mcm。
- 正式绘图依赖 `$visualize-data → $ssci-plots → $nature-figure`。后两者的技能目录不随仓库分发，visualize-data 由用户平台提供。来源与许可状态见 [NOTICE.md](NOTICE.md)；锁文件是依赖记录，不是安装器。
- 当前正式绘图协议要求 `gpt-5.6-sol + high + fork_turns=none` 及指定 Python/样式配置。这是本项目配置要求，不保证任意平台均提供该模型或技能；无法满足时停止并报告，不静默降级。
- 模型服务账号、调用费用、检索权限和阶段性依赖由使用者准备；无需为阅读工作流或运行基础测试安装所有科学计算库。
- 本项目不提供赛题原件、官方附件、完整参考论文或真实比赛运行包；不代表官方要求，也不保证获奖。实际比赛规则、AI 使用合规及最终投稿由使用者核对和负责。

## 文档入口

- [BOOTSTRAP.md](BOOTSTRAP.md)：自然语言初始化路由、默认目录、幂等检查和能力预检。
- [AGENTS.md](AGENTS.md)：Leader 调度、上下文隔离、角色复用、所有权和跨模块交接规则。
- [.agents/skills/mcm/SKILL.md](.agents/skills/mcm/SKILL.md)：内置数学建模与国奖向论文语义 Skill；无需外部安装。
- [Workflow/mcm-skill-integration.json](Workflow/mcm-skill-integration.json)：`build_prompt.py` 使用的阶段/角色 → Skill 模式与参考文件路由；只做上下文注入，不裁决论文质量。
- [Workflow/README.md](Workflow/README.md)：已实现波次、运行目录与模块交接顺序。
- [Workflow/team.json](Workflow/team.json)：前半程机械调度配置。
- [Workflow/literature-research.md](Workflow/literature-research.md)：路线文献校准、真实人类咨询、正式引用补齐和 Zotero 可选接口。
- [Workflow/literature-team.json](Workflow/literature-team.json)：文献 Scout、两类 Auditor、咨询记录和引用角色配置。
- [Workflow/data-engineering.md](Workflow/data-engineering.md)：数据工程职责、D0–D5、数据分层与回滚设计。
- [Workflow/data-team.json](Workflow/data-team.json)：数据工程完整/精简模式配置。
- [Workflow/modeling-construction.md](Workflow/modeling-construction.md)：建模构建模块的边界、Agent Team、逐问调度和工程留档设计。
- [Workflow/modeling-team.json](Workflow/modeling-team.json)：建模构建固定阶段、动态诊断、角色与所有权配置。
- [Workflow/modeling-implementation-plan.md](Workflow/modeling-implementation-plan.md)：建模构建模块的文件清单、角色 prompt、动态调度和分阶段实施计划。
- [Workflow/model-validation.md](Workflow/model-validation.md)：独立验证边界、V0–V6、保留信息暴露、动态 probe 和主张裁决。
- [Workflow/validation-team.json](Workflow/validation-team.json)：独立验证角色、固定阶段、动态循环与文件所有权配置。
- [Workflow/figure-preparation.md](Workflow/figure-preparation.md)：V6 后异步图表准备 F0–F4、逐问 Curator、流式复核和 FR0–FR4 数据交接。
- [Workflow/figure-preparation-team.json](Workflow/figure-preparation-team.json)：图表准备角色、阶段和机械所有权配置。
- [Workflow/formal-figure-rendering.md](Workflow/formal-figure-rendering.md)：FR0–FR4 图量覆盖、绘图、统一审查、真实版面 QA 和正式图交接。
- [Workflow/formal-figure-team.json](Workflow/formal-figure-team.json)：两类正式图角色、强制 sol-high 调度、所有权和迭代配置。
- [Workflow/nature-figure-skill.lock.json](Workflow/nature-figure-skill.lock.json)：正式绘图所需 `$nature-figure` 的项目级安装来源、hash、Python 后端和许可边界。
- [Workflow/ssci-plots-skill.lock.json](Workflow/ssci-plots-skill.lock.json)：`$ssci-plots` 项目级来源、commit、hash 与 MIT 许可证。
- [Workflow/formal-figure-style-profile.cassatt2.json](Workflow/formal-figure-style-profile.cassatt2.json)：用户选择的 C / Cassatt2 安静期刊视觉语言、palette 语义与布局边界。
- [Workflow/paper-preparation.md](Workflow/paper-preparation.md)：章节材料、双层独立审查、竞赛论文框架和 CP0–CP6 交接。
- [Workflow/paper-preparation-team.json](Workflow/paper-preparation-team.json)：论文准备角色、上下文隔离、创建/复用和机械所有权配置。
- [Workflow/paper-writing.md](Workflow/paper-writing.md)：PW0–PW7 正式正文写作、Leader 全文组装和四类独立审查。
- [Workflow/paper-writing-team.json](Workflow/paper-writing-team.json)：正式写作角色、审查隔离、创建/复用和文件所有权配置。
- [Workflow/final-delivery.md](Workflow/final-delivery.md)：FD0–FD7 排版、支撑材料、候选冻结、五路终审和人工接管。
- [Workflow/final-delivery-team.json](Workflow/final-delivery-team.json)：最终交付角色、终审隔离、冻结后只读和文件所有权配置。
- [Workflow/back-half-top-level-design.md](Workflow/back-half-top-level-design.md)：后半程总体边界与其余待实现模块。

## 检查与开源许可

```bash
python3 -m unittest discover -s tests -v
git diff --check
```

单元测试和 `check_workspace.py` 仅验证对应工程行为，不证明模型、论文、引用或图形正确。发布前按 [发布清单](docs/releasing.md) 核对文件、第三方许可、敏感信息和历史记录，不要直接压缩含运行数据及本地技能的开发目录。

本项目原创内容采用 [MIT License](LICENSE)，Copyright (c) 2026 gdl1605。内置及外部组件的来源、许可和分发边界见 [NOTICE.md](NOTICE.md)；贡献与安全报告分别遵循 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [SECURITY.md](SECURITY.md)。
