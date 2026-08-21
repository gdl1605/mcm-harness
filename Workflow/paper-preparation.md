# 章节材料包与竞赛论文框架工作流

> 状态：已实现。本文定义 CP0–CP6 的运行边界。模块只把验证后的工程证据整理成可直接成文的材料与段落级框架，不生成完整论文、正式图片、排版或审美结论。

## 1. 入口、目标与停止点

入口包括 validation handoff/claim map、`literature/route-alignment/route-evidence-handoff.md` 和既有来源。图表与 REF4–REF6 可以并行；CP1 的 chapter-map-v0 同时提供给图表 F3 和 Citation Gap Analyst，最终图表与 references handoff 再由 CP4/CP5 纳入论文框架。

材料只能来自 Leader 在 CP0 明列的题意、路线、数据、建模、验证和图表交接。论文角色不得遍历 `modeling/runs/` 挑更好看的结果，也不得从代码猜公式、修改数字或把诊断观察升级为结论。

终点是 `paper-prep/paper-framework-handoff.md`。后续正式论文 Agent 应当不打开代码目录就能准确成文；本模块仍不负责完整论文、参考文献检索、正式绘图、排版和提交文件。

## 2. Team 与所有权

- **Leader**：冻结输入、派工、保存句柄、处理 change request、控制上下文暴露和宣布交接；不写章节材料或框架。
- **Paper Structure Architect**：新 Agent，只写 CP1 的最小章节地图、全文主线和篇幅预算。
- **Question Chapter Curator**：每个纳入问题一个新 Agent，只写自己的 `paper-prep/questions/qN/`；允许结论为“不建议单列某段/某图”，但不能遗漏题目回答。
- **Chapter Evidence Auditor**：每个 v1 材料包完成后创建的新 Agent，只写本问题的 `evidence-review.md`。
- **原 Chapter Curator 回应**：复用原 Curator，写 evidence response 与 v2；不得成为自己的独立 reviewer。
- **Paper Framework Integrator**：新的全篇 owner，统一章节、符号、表图、claim 与篇幅；只写 `structure/`、`shared/` 和 `integration/` 的获批路径。
- **Competition Manuscript Reviewer**：新的 fresh-context reviewer，先盲审竞赛成文性，再加载国奖论文蒸馏做第二遍模式扫描；只写 review。
- **Framework Response**：复用原 Integrator，按 Leader 分派的修订单形成 v2；涉及逐问事实时必须返回原 Curator。

CP2/CP3 按问题独立写根流式运行，不按段落拆 Agent，也不为填并发槽制造重复角色。CP4、CP5、CP5R 和 CP6 是全篇串行阶段。

## 3. CP0：论文输入冻结

Leader 写 `paper-prep/scope/frozen-inputs.md`，至少记录：

- 题意基线、候选模型汇报、真实人工模型决定、按决定形成的路线，以及 data/model/validation handoff 的精确路径、版本与哈希；
- 每问允许引用的结果、公式、claim、条件、限制和题间接口；
- 官方论文格式、页数、答卷要求和已有引用来源；
- 禁止使用的旧 run、未验证候选、诊断猜想和失效版本；
- 图表支线的当前状态，以及尚未形成的 Figure ID/数据包；
- route-evidence-handoff、已有 source notes、引用缺口和 REF4–REF6 状态；
- 国奖论文蒸馏材料的精确路径，但标记为 CP5 第二遍之前禁止暴露；
- 每问写入根、Agent 句柄和版本保留规则。

没有官方格式或蒸馏材料时记录缺口，不自行编造。缺蒸馏材料不阻塞第一遍竞赛盲审；缺验证授权会阻塞对应问题成文。

## 4. CP1：最小论文骨架

Leader 创建新的 Paper Structure Architect。它只看题目、官方要求、题意基线、验证交接和必要题间接口，不看国奖论文蒸馏、逐问工程日志或 Leader 的写作倾向。

输出：

- `structure/chapter-map-v0.md`：章节顺序、每问位置、各节读者任务、共用内容位置；
- `structure/narrative-spine.md`：全文核心回答、各问贡献和题间过渡；
- `structure/page-budget.md`：核心、辅助、附录和可删除内容的篇幅优先级。

v0 不是最终框架，也不预先规定每问必须套同一种章节结构。落盘后 Leader 将其路径、版本和哈希提供给图表 F3；图表支线不必等待 CP2。

## 5. CP2：逐问章节材料包

每问创建一个新的 Question Chapter Curator。它只读 CP0 白名单、chapter-map-v0 和本问题的授权证据，写 `questions/qN/chapter-material-v1.md`。

材料包至少让后续写作者看清：

- 该问要求、回答对象和一句话核心回答；
- 为什么使用当前问题结构、baseline 和主模型，哪些备选被拒绝及原因；
- 假设、变量、参数、索引、单位、公式、目标、约束和边界；
- 求解/实验步骤中哪些必须进正文，哪些只应进附录或来源说明；
- 验证后的结果、解释、对照、限制和题间消费关系；
- 表格、Figure ID、公式的逻辑位置和前后叙事任务；
- 可直接写、需条件写、禁止写的 claim；
- 每个数字、公式和结论的精确来源。

材料可以提供句子骨架和段落顺序，但不写完整正式论文。文件结构可自由扩展；上述问题不是字段白名单。

## 6. CP3/CP3R：证据审查与原 Curator 回应

某问题 v1 落盘后，Leader 立即创建新的 Chapter Evidence Auditor，不等待其他问题。Auditor 只读该问题材料、冻结证据和必要接口，写 `questions/qN/evidence-review.md`，检查：

- 数字、公式、单位、精度和结果是否能回到授权来源；
- 是否混入旧 run、未验证候选、错误总体或过度 claim；
- 公式—代码—结果表是否对应，题间输入输出能否直接消费；
- 正式写作者是否无需读代码即可复述方法和结果；
- 事实缺口应局部修订、限制表达还是返回上游。

Review 不使用笼统“通过/不通过”，而写来源、失败机制、影响和最小修正。

随后复用原 Curator，写 `evidence-response.md`，保留 v1 并形成 `chapter-material-v2.md`。默认一次集中修订；实质数据、模型或验证错误只写 `paper-prep/change-requests/REQUEST-ID.md`，由 Leader 返回最早责任阶段。

## 7. CP4：全文框架整合

所有纳入问题完成 evidence review/response 且 `literature/citation-preparation/references-handoff.md` 已落盘后，Leader 创建新的 Paper Framework Integrator。若某问题被明确暂缓，必须在范围中保留其影响，不能由 Integrator 补造内容。

Integrator 产出：

- `structure/chapter-map-v1.md`；
- `shared/notation-registry.md`；
- `shared/claim-to-section-map.md`；
- `shared/table-and-figure-plan.md`；
- `integration/paper-framework-v1.md`。

它负责统一术语、符号、单位、精度、模型名、题间衔接、引用、摘要/结论候选信息和篇幅；删除重复工程过程，标记正文/附录/可删除内容；纳入 references handoff 与 figure handoff。它不能润色成完整论文、编造引用或改逐问事实。

## 8. CP5：竞赛论文双遍独立审读

Leader 创建新的 Competition Manuscript Reviewer，与 Curator、Evidence Auditor 和 Integrator 均独立。

### 第一遍：盲审

只允许读取原题、官方要求、chapter-map-v1、paper-framework-v1、逐问最终材料和 Figure/Table 占位。禁止读取代码、工程日志、Leader 辩护、Evidence review 和国奖论文蒸馏。先写并冻结 `integration/competition-review-blind.md`。

盲审重点是：每问答案是否醒目；是否按“问题—方法—结果—意义”组织；模型选择是否有理由；结果是否被解释；摘要、结论和题间主线是否闭合；篇幅是否失衡；正文是否仍充满 run、debug、路径、调参流水账等工程语言。

### 第二遍：模式扫描

盲审落盘后，Leader 才向同一 Reviewer 开放 CP0 登记的国奖论文蒸馏材料，写 `integration/competition-review-pattern-sweep.md`。蒸馏材料只能作为结构、信息密度和表达镜头；不得照搬章节、引入其他题目的模型/结论、猜评分权重或覆盖本题证据。

两遍 review 都必须指出具体位置、读者障碍、对答题效果的影响和修改方向，不给虚假的获奖概率或总体“通过”标签。

## 9. CP5R/CP6：定向修订、关闭检查与交接

Leader 按问题归属派发一次修订：

- 公式、数字、结果和局部解释：复用原 Question Chapter Curator，保留 v2 并形成必要的 v3；
- 章节顺序、重复、篇幅和全篇叙事：复用原 Framework Integrator，使用 framework-response prompt；
- 上游证据缺陷：提交 change request，返回验证、建模或数据模块。

Integrator 写 `integration/framework-response.md` 和 `paper-framework-v2.md`。原 Competition Manuscript Reviewer 只做一次关闭检查，写 `integration/competition-review-closure.md`，仅核对原问题如何处理，不引入全新审稿轮次。仍有高影响分歧时限制表达、保留分支或升级用户。

最后在 figure handoff、references handoff 和 `literature/references.bib` 已落盘后，复用原 Integrator 把最终 Figure ID、引用位置和限制纳入 v2，并写 `paper-prep/paper-framework-handoff.md`。Integrator 是该文件唯一内容 owner；Leader 只核对后宣布交接。

## 10. 目录与开放交接

```text
paper-prep/
├── scope/frozen-inputs.md
├── structure/{chapter-map-v0.md,chapter-map-v1.md,narrative-spine.md,page-budget.md}
├── questions/qN/
│   ├── chapter-material-v1.md
│   ├── evidence-review.md
│   ├── evidence-response.md
│   ├── chapter-material-v2.md
│   └── chapter-material-v3.md（仅受 CP5R 影响时）
├── shared/{notation-registry.md,claim-to-section-map.md,table-and-figure-plan.md}
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

- 数字、公式或授权错误：返回原问题 Curator；需要改证据时返回上游。
- 章节、篇幅或工程文风问题：返回 Framework Integrator，不反向改数字迎合叙事。
- 图表尚未完成：允许占位，但必须记录状态；正式论文定稿前再由后续模块汇合。
- 缺少现成参考文献：记录引用需求，不在本模块发起外部检索。
- CP5 默认一轮双遍审读、一次定向修订、一次关闭检查，不无限迭代。
- 完成 handoff 后停止，不创建完整论文、正式图片、排版文件或提交包。
