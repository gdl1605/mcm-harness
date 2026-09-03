# 章节材料包与竞赛论文框架工作流

> 状态：已实现。本文定义 CP0–CP6 的运行边界。模块只把验证后的工程证据整理成可直接成文的材料与段落级框架，不生成完整论文、正式图片、排版或审美结论。

## 1. 入口、目标与停止点

入口包括 V6 的 `answer-reconstruction.md`、cross-question validation、validation handoff/claim map、M6 指定且与验证处置一致的逐问权威方法说明、`literature/route-alignment/route-evidence-handoff.md` 和既有来源。图表与 REF4–REF6 可以并行；CP1 的 chapter-map-v0 同时提供给图表 F3 和 Citation Gap Analyst，最终图表与 references handoff 再由 CP4/CP5 纳入论文框架。

材料只能来自 Leader 在 CP0 明列的题意、路线、数据、建模、验证和图表交接。论文角色不得遍历 `modeling/runs/` 挑更好看的结果，也不得从代码猜公式、修改数字或把诊断观察升级为结论。

终点是 `paper-prep/paper-framework-handoff.md`。后续正式论文 Agent 应当不打开代码目录就能准确成文；本模块仍不负责完整论文、参考文献检索、正式绘图、排版和提交文件。

本模块通过 `scripts/build_prompt.py` 使用内置 `$mcm`：Leader、Structure Architect、Question Curator、Framework Integrator 和 Response 默认采用 `paper-material`；Evidence Auditor 采用 `validation`。这些 profile 只提供答案形状和证据组织语义，不改变白名单与 owner。Competition Manuscript Reviewer 第一遍采用 `blind-review`，第二遍必须显式覆盖为 `judge-review`；精确路由以 `Workflow/mcm-skill-integration.json` 为准。

## 2. Team 与所有权

- **Leader**：冻结输入、派工、保存句柄、处理 change request、控制上下文暴露和宣布交接；不写章节材料或框架。
- **Paper Structure Architect**：新 Agent，只写 CP1 的最小章节地图、全文主线和篇幅预算。
- **Question Chapter Curator**：每个纳入问题一个新 Agent，只写自己的 `paper-prep/questions/qN/`；允许结论为“不建议单列某段/某图”，但不能遗漏题目回答。
- **Chapter Evidence Auditor**：每问在未见 v1、未见代码时创建；CP3A 写独立 `method-reconstruction.md`，CP3B 复用同一 Agent 对照 v1 写 `evidence-review.md`，纯文档修复时最多再写一次 closure。
- **原 Chapter Curator 回应**：复用原 Curator，写 evidence response 与 v2；不得成为自己的独立 reviewer。
- **Paper Framework Integrator**：新的全篇 owner，统一章节、符号、表图、claim 与篇幅；只写 `structure/`、`shared/` 和 `integration/` 的获批路径。
- **Competition Manuscript Reviewer**：新的 fresh-context reviewer，先盲审竞赛成文性，再加载国奖论文蒸馏做第二遍模式扫描；只写 review。
- **Framework Response**：复用原 Integrator，按 Leader 分派的修订单形成 v2；涉及逐问事实时必须返回原 Curator。

CP2 与 CP3A 可在同一问题上并行，因为两者输入隔离、写入不同；CP3B 必须等待 v1 与冻结的 reconstruction/closure，并复用原 Auditor。各问可以流式推进，不按段落拆 Agent，也不为填并发槽制造重复角色。CP4、CP5、CP5R 和 CP6 是全篇串行阶段。

## 3. CP0：论文输入冻结

Leader 写 `paper-prep/scope/frozen-inputs.md`，至少记录：

- 题意基线、候选模型汇报、真实人工模型决定、按决定形成的路线，以及 data/model/validation handoff 的精确路径、版本与哈希；
- 每问允许引用的结果、公式、claim、条件、限制和题间接口；
- V6 证据优先答案重建和意图对照的精确路径；哪些答案已经存在、哪些只能条件化使用、哪些仍因证据或决策缺口不能成文；
- 每问一个权威方法说明的精确路径与版本，以及它对应的 build contract、代码/config、授权结果和接口；同时列出旧说明和已知语义缺口；
- 建模前候选相对 baseline 的预期价值与验证后实际证据必须分开；逐问冻结同口径 baseline/直观路线、主模型、有效挑战或结构反例，以及它们是否改变有效性、可行性或题目答案；
- 官方论文格式、页数、答卷要求和已有引用来源；
- 禁止使用的旧 run、未验证候选、诊断猜想和失效版本；
- 图表支线的当前状态，以及尚未形成的 Figure ID/数据包；
- route-evidence-handoff、已有 source notes、引用缺口和 REF4–REF6 状态；
- `state/mcm-skill-snapshot.json`、`Workflow/mcm-skill-integration.json` 及其记录的 Skill 版本；
- 国奖论文蒸馏材料的精确路径，但标记为 CP5 第二遍之前禁止暴露；
- 每问写入根、Agent 句柄和版本保留规则。

没有官方格式或蒸馏材料时记录缺口，不自行编造。缺蒸馏材料不阻塞第一遍竞赛盲审；缺验证授权或 V6 明确指出答案尚不存在时，CP0 不得把该问标成可成文。已完成问题可以先整理，但 CP4 全篇框架不得掩盖仍未完成的必答问题，也不得由论文角色补答案。

## 4. CP1：最小论文骨架

Leader 创建新的 Paper Structure Architect。它只看题目、官方要求、题意基线、验证交接和必要题间接口，不看国奖论文蒸馏、逐问工程日志或 Leader 的写作倾向。

输出：

- `structure/chapter-map-v0.md`：章节顺序、每问位置、各节读者任务、共用内容位置；
- `structure/narrative-spine.md`：全文核心回答、各问候选论证作用和题间过渡；此时不宣布贡献；
- `structure/page-budget.md`：核心、辅助、附录和可删除内容的篇幅优先级。

v0 不是最终框架，也不预先规定每问必须套同一种章节结构。落盘后 Leader 将其路径、版本和哈希提供给图表 F3；图表支线不必等待 CP2。

## 5. CP2：逐问章节材料包

每问创建一个新的 Question Chapter Curator。它只读 CP0 白名单、chapter-map-v0、本问题的权威方法说明和授权证据，写 `questions/qN/chapter-material-v1.md`。它不打开代码补解释，也不知道并行 CP3A 的独立重建内容。

材料包应按本问真实推理组织，不要求与其他问题采用相同小标题、篇幅或顺序。它至少要让后续写作者理解：

- 该问最终应让读者获得什么认识、选择或行动，现有证据允许回答到哪里，以及它在题链中的作用；不预写必须原样进入论文的“核心答案句”；
- 为什么使用当前问题结构、baseline 和主模型，哪些备选被拒绝及原因；
- 假设、变量、参数、索引、单位、公式、目标、约束和边界；
- 求解/实验步骤中哪些必须进正文，哪些只应进附录或来源说明；
- 验证后的结果、解释、对照、限制和题间消费关系；
- 本问真实困难、直观/baseline 缺口、当前处理、具有区分力的证据及答案是否因此发生有效变化；未证增量时保留为建模选择，不强造贡献；
- 表格、Figure ID、公式的逻辑位置和前后叙事任务；
- 可直接写、需条件写、禁止写的 claim；
- 每个数字、公式和结论的精确来源。

材料传递答案含义和证据关系，不提供要求下游复制的句子骨架，也不写完整正式论文。文件结构可自由扩展；上述问题不是字段白名单。

## 6. CP3A/CP3B/CP3R：无代码重建、材料对照与原 Curator 回应

### CP3A：独立方法重建

每问创建一个新的 Chapter Evidence Auditor，可与该问 CP2 同时启动。Auditor 第一遍只能读取原题与官方交付、V6 答案重建、CP0 冻结的权威方法说明、授权结果及条件/限制、必要接口和符号；禁止代码、config、run、日志、v1、Curator 私有推理、Leader 辩护和国奖材料。

它用自己的话写 `questions/qN/method-reconstruction.md`，说明本题的观测/决策对象、数据与变量如何进入核心关系/目标/约束、参数或方案如何估计/求解、输出怎样成为题目答案。V6 负责“证据允许回答什么”，CP3A 只负责“模型怎样产生该答案”，不能重新挑主答案。结构随问题自然展开，不填固定表，不以公式、伪代码或篇幅作为完整性代理。

CP3A 发现断点后按含义路由：

- 已实现语义只是在权威方法说明中漏写，且可回到冻结合同或验证处置：复用原 model builder 只修订说明并升版，不改代码、模型或结果；随后复用同一 Auditor 一次写 `method-reconstruction-closure.md`。无法定位的新解释不按纯文档修复关闭。
- 修订会改变模型结构、目标/约束、数据—变量映射、估计/求解、输出转换或结果含义：返回 M2/M3 及验证；新结果冻结后创建新的 Auditor，旧 reconstruction 保留。
- 缺的是主选择、规则、阈值、时点、名单或其他答案对象：返回 V6/对应答案 owner，不让方法说明或 CP 补造。

Auditor 不得通过打开代码自行修补第一类与第二类的边界；有疑义时保留竞争解释并交 Leader 路由。

### CP3B 与 CP3R：对照材料并回应

只有该问 v1 与可接受的 reconstruction/closure 都已冻结，Leader 才复用原 Auditor。第二遍新增 v1、validation claim map 和 Auditor 自己的 memo，代码与工程日志仍禁止。Auditor 写 `questions/qN/evidence-review.md`，比较材料的模型—答案链与独立重建，并核对数字、公式、单位、精度、总体、版本、claim、题间消费和来源；寻找旧候选、诊断升级、相关性冒充因果、局部结果冒充全局，以及为了显得完整而补造的边界、时点、规则、名单、因果或主选择。

Review 不给笼统“通过/不通过”，而写位置、来源、失败机制、影响和最小责任 owner。随后复用原 Curator，读取 reconstruction、必要 closure 和 review，写 `evidence-response.md`，保留 v1 并形成 `chapter-material-v2.md`。默认一次集中修订；Curator 不能修权威方法说明或上游答案。

## 7. CP4：全文框架整合

所有纳入问题完成 method reconstruction/必要 closure、evidence review/response 且 `literature/citation-preparation/references-handoff.md` 已落盘后，Leader 创建新的 Paper Framework Integrator。若某问题被明确暂缓，必须在范围中保留其影响，不能由 Integrator 补造内容。

Integrator 产出：

- `structure/chapter-map-v1.md`；
- `structure/narrative-spine-v1.md`：在保留 CP1 初稿的前提下，用验证后证据重建全文贡献与降级事项；
- `shared/notation-registry.md`；
- `shared/claim-to-section-map.md`；
- `shared/table-and-figure-plan.md`；
- `integration/paper-framework-v1.md`。

它负责统一术语、符号、单位、精度、模型名、题间衔接、引用、摘要/结论候选信息和篇幅；删除重复工程过程，标记正文/附录/可删除内容；纳入 references handoff 与 figure handoff。

CP4 同时负责验证后贡献重建：从本题真实困难、参考路线缺口、当前处理、决定性证据、答案变化和边界中判断哪些可作为竞赛贡献，哪些只是必要建模选择，哪些没有进入答案而应降为辅助/附录/删除。不要求每问贡献，指标提升也不能脱离答案含义。贡献 claim 写入 narrative spine 与 claim-to-section map；缺必要比较时降级或返回 M/V，不能由 Integrator 补数。

整合时必须保留不同题型各自的推理节奏，不能为全篇整齐把所有问题改成同一段落骨架。它不能润色成完整论文、编造引用、改逐问事实或把竞赛处理特点升级为未经文献支持的学术原创。

## 8. CP5：竞赛论文双遍独立审读

Leader 创建新的 Competition Manuscript Reviewer，与 Curator、Evidence Auditor 和 Integrator 均独立。

### 第一遍：盲审

只允许读取原题、官方要求、chapter-map-v1、`narrative-spine-v1.md`、`claim-to-section-map.md`、paper-framework-v1、逐问最终材料和 Figure/Table 占位。`build_prompt.py` 保持默认 `blind-review`；禁止调用 `$mcm`，也禁止读取代码、工程日志、Leader 辩护、原始 Evidence review 和国奖论文蒸馏。先写并冻结 `integration/competition-review-blind.md`。

盲审重点是：每问的答案能否从其真实论证中自然看见；模型选择是否有理由；结果是否被解释；所谓贡献能否从本题困难、参考路线、区分证据、答案变化和边界中恢复；摘要、结论和题间主线是否闭合；不同问题是否被强行压成同一种结构；篇幅是否失衡；正文是否仍充满 run、debug、路径、调参流水账等工程语言。方法适配但增量未证实不等于失败，应诚实降级；没有进入答案的内容不能作为主要贡献。

### 第二遍：模式扫描

盲审落盘后，Leader 才以 `--mcm-profile judge-review` 重建后续 prompt，向同一 Reviewer 开放内置评委语义 reference 与 CP0 登记的国奖论文蒸馏材料，写 `integration/competition-review-pattern-sweep.md`。蒸馏材料只能作为答案层级、证据闭环、结构、信息密度、贡献表达位置和表达镜头；不得从范文发明本题贡献、照搬章节、引入其他题目的模型/结论、猜评分权重或覆盖本题证据。

两遍 review 都必须指出具体位置、读者障碍、对答题效果的影响和修改方向，不给虚假的获奖概率或总体“通过”标签。

## 9. CP5R/CP6：定向修订、关闭检查与交接

Leader 按问题归属派发一次修订：

- 公式、数字、结果和局部解释：复用原 Question Chapter Curator，保留 v2 并形成必要的 v3；
- 章节顺序、重复、篇幅和全篇叙事：复用原 Framework Integrator，使用 framework-response prompt；
- 贡献仅缺少已有证据之间的表达联结：由原 Integrator 重组；贡献缺决定性证据：降级措辞或返回 M/V，不得由论文角色补造；
- 上游证据缺陷：提交 change request，返回验证、建模或数据模块。

Integrator 写 `integration/framework-response.md` 和 `paper-framework-v2.md`。若 review 改变贡献、必要方法或辅助/删除边界，保留 CP4 版本并另写 `structure/narrative-spine-v2.md` 与 `shared/claim-to-section-map-v2.md`；没有变化时不制造空版本。原 Competition Manuscript Reviewer 只做一次关闭检查，写 `integration/competition-review-closure.md`，仅核对原问题如何处理，不引入全新审稿轮次。仍有高影响分歧时限制表达、保留分支或升级用户。

最后在 figure handoff、references handoff 和 `literature/references.bib` 已落盘后，复用原 Integrator 把最终 Figure ID、引用位置和限制纳入 v2，并写 `paper-prep/paper-framework-handoff.md`。Integrator 是该文件唯一内容 owner；Leader 只核对后宣布交接。

## 10. 目录与开放交接

```text
paper-prep/
├── scope/frozen-inputs.md
├── structure/{chapter-map-v0.md,chapter-map-v1.md,narrative-spine.md,narrative-spine-v1.md[,narrative-spine-v2.md],page-budget.md}
├── questions/qN/
│   ├── method-reconstruction.md
│   ├── method-reconstruction-closure.md（仅纯方法说明修复时）
│   ├── chapter-material-v1.md
│   ├── evidence-review.md
│   ├── evidence-response.md
│   ├── chapter-material-v2.md
│   └── chapter-material-v3.md（仅受 CP5R 影响时）
├── shared/{notation-registry.md,claim-to-section-map.md[,claim-to-section-map-v2.md],table-and-figure-plan.md}
├── integration/
│   ├── paper-framework-v1.md
│   ├── competition-review-blind.md
│   ├── competition-review-pattern-sweep.md
│   ├── framework-response.md
│   ├── paper-framework-v2.md
│   └── competition-review-closure.md
├── change-requests/
└── paper-framework-handoff.md
```

所有语义材料使用开放 Markdown，模板问题只是最低责任。JSON 只保存团队配置、路径、哈希、版本、运行参数和状态，不裁决论文质量。

## 11. 停止与回滚

- 材料转写的数字、公式或授权错误：返回原问题 Curator；证据或模型错误返回上游。
- 权威方法说明仅漏写真实实现语义：复用原 model builder 修说明，再由同一 Auditor 做一次 closure；若任何模型或结果含义改变，返回建模与验证并换新 Auditor。
- 缺主答案、主选择或最终对象：返回 V6/答案 owner，不在 CP3 或方法说明中补造。
- 章节、篇幅或工程文风问题：返回 Framework Integrator，不反向改数字迎合叙事。
- 图表尚未完成：允许占位，但必须记录状态；正式论文定稿前再由后续模块汇合。
- 缺少现成参考文献：记录引用需求，不在本模块发起外部检索。
- CP5 默认一轮双遍审读、一次定向修订、一次关闭检查，不无限迭代。
- 完成 handoff 后停止，不创建完整论文、正式图片、排版文件或提交包。
