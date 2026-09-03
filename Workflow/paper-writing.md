# 正式论文写作与全文组装工作流

> 状态：已实现。本文定义 PW0–PW7。唯一正文源是 Markdown；主 Leader 是唯一全文作者。模块不生成 Word/LaTeX、正式图片、排版、引用检索结果或提交包。

## 1. 入口、目标与停止点

入口为 paper framework、逐问权威方法说明与 CP3 method reconstruction/evidence review、CP4 narrative spine/claim-to-section map 中验证后建立的贡献边界、figure handoff、`literature/citation-preparation/references-handoff.md`、`literature/references.bib`、验证授权证据和官方论文要求。FR0–FR4 可与 PW0–PW4 并行；正式图尚未交付时允许 Figure ID 占位，`full-paper-v2.md` 和 figure-table slots 提供给 FR3 做真实版面关闭。引用缺口只能保留 CITATION-NEEDED，不得虚构。

目标是形成连续、可提交前继续加工的竞赛论文 Markdown 正文，并通过四种彼此独立的审查：事实一致性、竞赛表达、全文连贯、AI/口水文风。Reviewer 永久只写修改单；原问题作者修局部，Leader 组装并统一全文。

停止于 `paper-writing/formal-paper-handoff.md`，正文为 `paper-writing/manuscript/final-paper.md`。后续排版与最终交付不得改变已冻结的数字、公式、单位和 claim。

本模块的正式作者默认由 `build_prompt.py` 注入 `$mcm submission-draft`；Fact Auditor 使用 `validation`，Competition Expression Reviewer 第一遍使用 `front-page-review`、第二遍和原问题关闭显式切换 `judge-review`，Coherence Reviewer 使用 `judge-review`，AI Prose Auditor 使用 `prose-revision`。Skill 只影响语义取舍和阅读判断，不能增加事实、引用、写权或审查可见范围；精确 reference 由 `Workflow/mcm-skill-integration.json` 路由。

## 2. Team 与文件所有权

- **Leader/全文作者**：写 PW0/PW1、公共章节、摘要结论、全部 `manuscript/` 版本、全局 response 与最终 handoff；只有 Leader 可修改全文主稿。
- **Question Manuscript Writer**：每问一个新 Agent，只写自己的 `sections/qN/section-v1.md`；PW4R 事实修订时复用写 response/v2，PW5R 仅在正文漏掉冻结上游已有答案时复用写 expression response/v3。
- **Full-Paper Fact Auditor**：新 Agent，独立核对全文数字、公式、单位、claim、表图和题间接口；只写 fact review，PW6 复用做事实回归。
- **Competition Expression Reviewer**：PW5A 新 Agent，先在正文隐藏时重建首页实际传达内容；PW5B 复用同一 Agent 对照冻结全文并完成竞赛表达审查；PW6 复用关闭原全文问题，高影响首页修订才条件创建一个 fresh 同角色实例。
- **Full-Paper Coherence Reviewer**：新 Agent，只检查定义顺序、章节关系、题间过渡、摘要正文结论闭合与表图引用；PW6 复用关闭原问题。
- **AI Prose Auditor**：新 Agent，只检查可定位的机械、空洞、工程化和口水表达；不判断作者身份，不给 AI 分数，不直接改文；PW6 复用关闭原问题。

四个 Reviewer 互不读取 peer review 或 Leader 辩护。PW5 的全部全文审查最终使用同一个冻结 `full-paper-v2.md`；但 Competition Reviewer 第一遍只能看到该版本的原样 front matter，第一遍 memo 落盘后才增加完整正文。不能边审边看改稿。

## 3. PW0：正式写作输入冻结

Leader 写 `paper-writing/scope/frozen-inputs.md`，至少冻结：

- paper framework、章节地图、逐问当前材料和符号注册表；
- 每问权威方法说明、独立 method reconstruction、必要 closure 和 evidence review 的精确版本，以及它们与当前授权结果的一致关系；
- CP4/CP5 已支持的竞赛贡献、必要但不升级的建模选择、辅助/删除项，以及每项贡献的本题困难、参考路线、决定性证据、答案变化、边界和措辞上限；
- validation handoff/claim map、授权公式、数字、条件和禁止表达；
- figure handoff、Figure/Table ID、正式图片状态和占位方式；
- 官方页数、格式、匿名、语言和答卷要求；
- 已有参考文献、待补引用和禁止虚构来源；
- references handoff、claim-to-citation map、references.bib、引用键和人的意见边界；
- `state/mcm-skill-snapshot.json` 与本轮 `submission-draft` / reviewer profile 路由；
- 旧材料、旧数字、未验证候选和上游只读边界；
- 每问 writer/reviewer 句柄、写入根与版本保留规则。

缺正式图片不阻塞内容写作，但必须保持可追踪占位并登记 FR owner；缺已审引用或验证授权阻塞对应 claim。FR4 handoff 在 FD0 前必须完成。

## 4. PW1：Leader 写作计划

Leader 写：

- `plan/writing-plan.md`：章节顺序、写作波次、输入版本、首页两遍暴露和总篇幅；
- `plan/section-contracts.md`：逐问输入、权威方法说明与 reconstruction/review、读者最终应获得的认识/选择/行动、该问特有的展开逻辑、已授权贡献或必要/辅助定位、篇幅、Figure/Table、禁止扩张和唯一写入根；不预写答案句、统一段落顺序或每问贡献；
- `plan/prose-boundary.md`：必要技术术语、正文/附录边界、工程词禁区和不可随意替换的数学名词；
- `plan/figure-table-slots.md`：稳定 ID、来源、引入位置、caption 状态和回填规则。

这些计划是开放 Markdown，不是固定论文目录。Leader 不在每问 writer 开始前预写其正文措辞。

## 5. PW2：逐问正式正文

每问创建一个新的 Question Manuscript Writer。它只读对应 section contract、最终章节材料、冻结的权威方法说明、method reconstruction/必要 closure、evidence review、全局符号/术语和获批表图，写 `sections/qN/section-v1.md`。代码、config、run 和工程日志不在其白名单内。

正文必须是连续竞赛论文内容，而不是提纲或工程索引。Writer 根据本问题的任务和证据选择自然展开：读者应能理解模型为何需要、证据如何产生、最终获得什么认识/选择/行动以及条件如何改变使用方式，但这些内容不要求按统一顺序、统一小标题或统一结尾出现。复杂或条件性答案可以由连续段落构成，不强压成一句话。只有 section contract 授权时才表达贡献；方法适配但答案增量未证实，只说明选择理由，不写成创新。

方法说明与独立重建共同约束模型语义，evidence review 约束可写边界；三者冲突时返回 CP3/原 model builder/验证，不让 Writer 打开代码裁决。不得把 run、config、debug、pipeline、文件路径、调参日志和版本处理写入正文。不得自行写摘要、总结合并段或修改其他问题。

## 6. PW3/PW4/PW4R：全文 v1、事实审查与事实修订

所有 section-v1 落盘后，Leader 写公共章节、摘要、关键词、全局假设与符号、结论、优缺点和推广，统一术语、公式编号、表图占位和篇幅，形成 `manuscript/full-paper-v1.md`。Leader 只能表达 PW0 冻结的贡献，不从模型组合或写作习惯新增“创新、首次、显著提升、推广价值”；必要建模选择与辅助结果保持原层级。

Leader 随后创建新的 Full-Paper Fact Auditor。它只读 v1、逐问权威方法说明与 method reconstruction/closure/evidence review、验证授权证据、结果表、公式来源和 figure handoff，禁止代码与工程日志，写 `reviews/fact-consistency-review.md`，逐项检查：

- 数字、公式、单位、精度、总体、条件和 claim；
- 摘要、正文、结论之间的结果一致性；
- Figure/Table/caption 与正文；
- 题间 producer–consumer 接口；
- 正文的输入—模型—输出—答案关系是否偏离已审重建；
- 贡献/创新/提升/稳健/推广等 claim 是否能回到参考路线、区分证据、答案变化与边界，竞赛处理特点是否被误写成学术原创；
- 限制是否在正文保留。

每项必须含正文位置、来源、失败影响和责任 owner，不用笼统“有误”。同时检查引用键是否来自 references handoff、引用句是否越过文献支持范围、人的意见是否被写成事实。

PW4R 中，局部事实问题退给原 Question Manuscript Writer，写 `section-fact-response.md` 和 `section-v2.md`；全局复述由 Leader 修；上游证据错误写 change request。Leader 保留 v1，写 `responses/fact-response.md` 和 `manuscript/full-paper-v2.md`。

## 7. PW5：首页两遍重建与三路独立审查

在 `full-paper-v2.md` 冻结后，Leader 写 `scope/front-matter-v2.md`。它只能原样复制标题、摘要、关键词和首页已有文字，并记录源版本和截取边界；不能概括、润色或补答案。实际页码和视觉效果仍由后续排版/图表流程负责，本阶段只审首页语义。

随后并行启动：Competition Reviewer 的 PW5A、Full-Paper Coherence Reviewer 和 AI Prose Auditor。后两者直接读取同一冻结 v2；Competition Reviewer 必须完成第一遍后才能进入 PW5B。三者只读各自白名单，不读 peer review。

### 7.1 PW5A：首页独立重建

创建新的 Competition Expression Reviewer，默认使用 `front-page-review`。它只读原题、官方要求和 `front-matter-v2.md`；禁止完整正文、V6 答案重建、框架、claim map、逐问材料、方法说明、旧 review 和 Leader 辩护。

它写开放的 `reviews/first-page-reconstruction.md`，自然复述首页让读者实际获得的任务、主答案、证据口径、本题贡献和改变结论的条件，并区分明确表达、合理推断与无法知道。模型名不能替代变量、职责、阈值或最终对象；孤立指标不能替代答案证据。此时不验证首页是否真实，不提供替换句或评分。

### 7.2 PW5B：首页—正文比较与竞赛表达审查

确认 reconstruction 已落盘并冻结后，Leader 以 `--mcm-profile judge-review` 重建后续 prompt，复用同一 Reviewer，新增它自己的 memo 和同一冻结 `full-paper-v2.md`。Reviewer 写 `reviews/competition-expression-review.md`。

先比较首页承诺与正文：正文已成立但首页漏写，由 Leader 修 front matter；首页强于正文则缩小表达，事实冲突返回 Fact Auditor；答案存在于上游但正文漏写，返回原 Question Writer；证据尚未形成答案，返回 V6/上游。贡献必须能恢复本题困难、参考路线、区分证据、答案变化和边界；必要方法不得自动升级，未进入答案的内容不能占主要贡献。再检查每问答案是否自然可复述、模型理由、结果解释、信息密度、篇幅重点、说明书/教程/工程报告倾向，以及不同问题是否被强行同构。对主要方法、结果和诊断执行答案保持型删除判断：删去不损失答案、有效性依据或使用条件时，合并、转附录或删除；不按字数机械裁剪。

### 7.3 Full-Paper Coherence Reviewer

只写 `reviews/full-paper-coherence-review.md`，检查每个问题内部真实需要的定义、公式、证据和结论关系，章节和题间逻辑、符号/术语/模型名、摘要—正文—结论闭合、表图引入与解释，以及未定义、未使用、重复或相互矛盾的内容。不得把“统一顺序”本身当作连贯性，也不得要求用套话修补逻辑。

### 7.4 AI Prose Auditor

只读 v2、官方要求和必要技术术语注册表，写 `reviews/ai-prose-review.md`。它不判断“是不是 AI 写的”，只定位：

- “首先、其次、再次、此外、综上、由此可见”等机械关联词堆积；
- 相同段首、转折、结尾和模板化小结反复出现；
- “为了……本文……”及空洞意义拔高；
- 无证据的“显著、有效、充分、全面、科学”；
- 无必要比喻、拟人、文学化表达和宣传语气；
- 重复解释简单事实、长句逗号堆积、主语不明和模糊结论；
- run/debug/pipeline/config/路径/调参流水账；
- 为避重复而错误替换数学术语；
- 过度整齐的排比、三段式和套话。

每项必须给短句定位、类别、为何削弱表达、应删除/合并/具体化/直接陈述，以及不能改变的数学含义。可以给一句简短示例，但不能直接改稿，不能用口语、错别字或降低专业性伪装“人味”。

## 8. PW5R/PW6：Leader 统一修订与关闭检查

`first-page-reconstruction.md` 与三份完整 review 全部落盘后，Leader 写 `responses/language-review-response.md`。正文已成立而首页遗漏由 Leader 修；首页事实越权重开 Fact 处置；冻结上游已有答案而逐问正文漏写，或局部正文越权抬高贡献时，复用该问原 Writer 写 `section-expression-response.md` 与 `section-v3.md`；贡献缺决定性证据时降级/删除，若不可省的优越性主张需要新比较则返回 M/V；证据本身缺答案则返回 V6/上游。章节逻辑、摘要结论、过渡和统一语气由 Leader 修。冲突按“事实准确 > 答题直接 > 表达简洁”裁决，根据受影响问题的新 section 形成 `manuscript/full-paper-v3.md`，并从 v3 原样写 `scope/front-matter-v3.md`。默认一次集中语言修订。

PW6 复用原四个 Reviewer，各自只检查原 review 的处置：Fact Auditor 做数字/公式/条件/claim 回归；原 Competition Reviewer 显式使用 `judge-review` 关闭全文表达问题；其余两者关闭原定位问题。分别写 `reviews/closure/` 下的四份 closure，不开启新一轮全面审稿。

若且仅若 PW5A 曾发现主答案、证据口径、贡献边界或关键条件无法从首页恢复，并且 PW5R 实质修改了 front matter，Leader 再创建一个 fresh Competition Expression Reviewer 实例。它仍是原角色，默认 `front-page-review`，只读原题、官方要求和 `front-matter-v3.md`，不读正文、旧 memo、review 或 response，写一次 `closure/first-page-reconstruction-closure.md`。这一步只报告仍阻断首页理解的高影响缺口，不扩展为新一轮全篇审稿。

事实错误必须修；影响答题、首页独立理解或全文矛盾的内容局部重开；纯风格偏好和 fresh 复核提出的第二轮新方向在一轮后保留 Leader 版本或升级用户，不无限润色。

## 9. PW7：正式论文交接

Leader 根据 v3 和 closure 形成 `manuscript/final-paper.md` 与 `formal-paper-handoff.md`。Handoff 至少链接正文版本、首页 reconstruction/必要 fresh closure、经证据支持的贡献与已降级事项、授权结果/公式、Figure/Table、references handoff/references.bib、四类 review、关闭状态、未完成图片/引用/排版/提交事项，以及后续不得改变的数字、公式、单位和 claim。

完成后停止，不生成 Word/LaTeX、正式图片、参考文献检索、版式文件、答卷或提交包。

## 10. 目录与开放交接

```text
paper-writing/
├── scope/{frozen-inputs.md,front-matter-v2.md,front-matter-v3.md}
├── plan/{writing-plan.md,section-contracts.md,prose-boundary.md,figure-table-slots.md}
├── sections/qN/{section-v1.md,section-fact-response.md,section-v2.md[,section-expression-response.md,section-v3.md]}
├── manuscript/{full-paper-v1.md,full-paper-v2.md,full-paper-v3.md,final-paper.md}
├── reviews/
│   ├── fact-consistency-review.md
│   ├── first-page-reconstruction.md
│   ├── competition-expression-review.md
│   ├── full-paper-coherence-review.md
│   ├── ai-prose-review.md
│   └── closure/{fact-closure.md,competition-expression-closure.md,coherence-closure.md,ai-prose-closure.md[,first-page-reconstruction-closure.md]}
├── responses/{fact-response.md,language-review-response.md}
├── change-requests/
└── formal-paper-handoff.md
```

所有语义内容使用开放 Markdown；模板问题只是最低责任。JSON 只保存配置、路径、版本、哈希、运行参数和状态，不裁决事实或文风。
