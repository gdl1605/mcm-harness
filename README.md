# C 题建模 Harness

这是一个独立的 Leader + Subagents 协作工程，不是 Skill，也不需要额外 orchestrator。当前主 Agent 自动担任 Leader，直接使用原生 subagent 完成审题、路线竞标、数据工程、建模构建、独立验证、图表与论文准备、正式论文 Markdown 写作，以及最终排版终审与人工交接。

当前已实现八段工作流：

1. **深度审题与路线交接**：确认每问真正要什么、做到多少、题间怎样串联、附件支持边界、未知陷阱和暂定建模路线。
2. **数据工程**：把原始附件转为可复现、可追溯、可供各问消费的规范数据与分析视图，并通过独立复现和题间接口审查。
3. **建模构建**：按题间依赖形成数学规格、baseline、候选模型、动态诊断与受约束调整，并交付待独立验证的模型包。
4. **独立模型验证**：通过数学实现、实验证据和复现接口审计，动态取证并按主张交付可引用范围、失效条件和回滚路径。
5. **V6 后异步图表准备**：由每问 Curator 整理诊断证据、逐图数据包、推荐图型和论文逻辑位置，流式复核后交给外部绘图模块。
6. **章节材料包与竞赛论文框架**：逐问整理可直接成文的材料，经证据审计和双遍竞赛成文审读后，交付段落级论文框架。
7. **正式论文写作与全文组装**：每问 subagent 写正式章节，Leader 独占全文主稿，并通过事实、竞赛表达、连贯性和 AI/口水文风四类独立审查。
8. **最终排版、终审与人工交付**：装配 PDF/可编辑候选稿和含结果数据、完整运行脚本源码的支撑材料；冻结后由五个独立 Reviewer 并行审排版、扣题、文风、交付证据和全链路一致性，只报问题并交给人最终微调和投稿。

主 harness 现在可以从正式论文 Markdown 继续生成提交候选包和人工终审交接。正式绘图与引用检索仍由外部/前置模块提供；FD4 终审后不自动改稿、不自动投稿，最终状态为 `AWAITING_HUMAN_FINALIZATION`。

项目坚持开放 Markdown 交接：角色必须回答最低问题，也可以补充任务单未预见的新发现；JSON 只保存团队配置、路径、哈希、版本、运行参数和状态，不承载或裁决语义结论。

文档入口：

- [AGENTS.md](AGENTS.md)：Leader 调度、上下文隔离、角色复用、所有权和跨模块交接规则。
- [Workflow/README.md](Workflow/README.md)：已实现波次、运行目录与模块交接顺序。
- [Workflow/team.json](Workflow/team.json)：前半程机械调度配置。
- [Workflow/data-engineering.md](Workflow/data-engineering.md)：数据工程职责、D0–D5、数据分层与回滚设计。
- [Workflow/data-team.json](Workflow/data-team.json)：数据工程完整/精简模式配置。
- [Workflow/modeling-construction.md](Workflow/modeling-construction.md)：建模构建模块的边界、Agent Team、逐问调度和工程留档设计。
- [Workflow/modeling-team.json](Workflow/modeling-team.json)：建模构建固定阶段、动态诊断、角色与所有权配置。
- [Workflow/modeling-implementation-plan.md](Workflow/modeling-implementation-plan.md)：建模构建模块的文件清单、角色 prompt、动态调度和分阶段实施计划。
- [Workflow/model-validation.md](Workflow/model-validation.md)：独立验证边界、V0–V6、保留信息暴露、动态 probe 和主张裁决。
- [Workflow/validation-team.json](Workflow/validation-team.json)：独立验证角色、固定阶段、动态循环与文件所有权配置。
- [Workflow/figure-preparation.md](Workflow/figure-preparation.md)：V6 后异步图表准备 F0–F4、逐问 Curator、流式复核和外部绘图交接。
- [Workflow/figure-preparation-team.json](Workflow/figure-preparation-team.json)：图表准备角色、阶段和机械所有权配置。
- [Workflow/paper-preparation.md](Workflow/paper-preparation.md)：章节材料、双层独立审查、竞赛论文框架和 CP0–CP6 交接。
- [Workflow/paper-preparation-team.json](Workflow/paper-preparation-team.json)：论文准备角色、上下文隔离、创建/复用和机械所有权配置。
- [Workflow/paper-writing.md](Workflow/paper-writing.md)：PW0–PW7 正式正文写作、Leader 全文组装和四类独立审查。
- [Workflow/paper-writing-team.json](Workflow/paper-writing-team.json)：正式写作角色、审查隔离、创建/复用和文件所有权配置。
- [Workflow/final-delivery.md](Workflow/final-delivery.md)：FD0–FD7 排版、支撑材料、候选冻结、五路终审和人工接管。
- [Workflow/final-delivery-team.json](Workflow/final-delivery-team.json)：最终交付角色、终审隔离、冻结后只读和文件所有权配置。
- [Workflow/back-half-top-level-design.md](Workflow/back-half-top-level-design.md)：后半程总体边界与其余待实现模块。
