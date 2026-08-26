# C 题建模 Harness

这是一个独立的 Leader + Subagents 协作工程，不需要额外 orchestrator；它现在内置项目级 `$mcm` Skill 作为各阶段 Agent 的语义判断层，但 Skill 不替代 Leader、角色所有权或工作流。当前主 Agent 自动担任 Leader，直接使用原生 subagent 完成审题、宽候选路线、候选级文献校准、人工模型决策、数据工程、建模构建、独立验证、图表准备、sol-high 正式绘图、论文准备、正式引用、正式论文 Markdown 写作，以及最终排版终审与人工交接。

当前已实现九段工作流：

1. **深度审题、宽候选与人工路线交接**：确认每问真正要什么、做到多少、题间怎样串联；A/B 分段产生宽候选，文献验证并扩展后由 Leader 汇报优劣势，真实用户选择模型才放行。
2. **数据工程**：把原始附件转为可复现、可追溯、可供各问消费的规范数据与分析视图，并通过独立复现和题间接口审查。
3. **建模构建**：按题间依赖形成数学规格、baseline、候选模型、动态诊断与受约束调整，并交付待独立验证的模型包。
4. **独立模型验证**：通过数学实现、实验证据和复现接口审计，动态取证并按主张交付可引用范围、失效条件和回滚路径。
5. **V6 后异步图表准备**：由每问 Curator 整理诊断证据、逐图数据包、推荐图型和论文逻辑位置，流式复核后交给正式绘图模块。
6. **正式论文绘图**：每问一个 sol-high Visual Producer 显式调用 `$visualize-data → $ssci-plots → $nature-figure`，使用用户选定的 `cassatt2_quiet_journal_v1` 完成 v1→v2 首轮视觉自审；fresh-context Reviewer 审 v2 后由原 Producer 完成 v2→final 第二轮，统一检查审美、Cassatt2 漂移、重复图例/caption、重叠、裁切、压缩和真实版面；默认 Luna 和静默 fallback 禁止。
7. **章节材料包与竞赛论文框架**：逐问整理可直接成文的材料，经证据审计和双遍竞赛成文审读后，交付段落级论文框架。
8. **正式论文写作与全文组装**：每问 subagent 写正式章节，Leader 独占全文主稿，并通过事实、竞赛表达、连贯性和 AI/口水文风四类独立审查。
9. **最终排版、终审与人工交付**：在论文参考文献后追加“支撑材料”结果/代码展示，并装配含处理后数据、结果和完整原始脚本的独立 ZIP；冻结后由五个独立 Reviewer 并行审排版、扣题、文风、交付证据和全链路一致性，只报问题并交给人最终微调和投稿。

另有一个贯穿模块：**文献、人的意见与引用证据**。它在 W5A 后逐候选检索支持、削弱、替代和新模型方向，在 V6/CP1 后生成 claim-to-citation map、`references.bib` 和引用交接。H1 是单独的强制真人模型决策；Agent 不得模拟人的意见，Zotero 可选且默认只读。

主 harness 现在可以完成文献/引用检索与审查、正式论文图、正式论文 Markdown、提交候选包和人工终审交接。正式绘图新 subagent 强制使用 `gpt-5.6-sol + high + fork_turns=none`；FD4 终审后不自动改稿、不自动投稿，最终状态为 `AWAITING_HUMAN_FINALIZATION`。

项目坚持开放 Markdown 交接：角色必须回答最低问题，也可以补充任务单未预见的新发现；JSON 只保存团队配置、路径、哈希、版本、运行参数和状态，不承载或裁决语义结论。

文档入口：

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
