# 正式论文写作与全文组装工作流

> 状态：已实现。本文定义 PW0–PW7。唯一正文源是 Markdown；主 Leader 是唯一全文作者。模块不生成 Word/LaTeX、正式图片、排版、引用检索结果或提交包。

## 1. 入口、目标与停止点

入口为 paper framework、figure handoff、`literature/citation-preparation/references-handoff.md`、`literature/references.bib`、验证授权证据和官方论文要求。正式图尚未交付时允许 Figure ID 占位；引用缺口只能保留 CITATION-NEEDED，不得虚构。

目标是形成连续、可提交前继续加工的竞赛论文 Markdown 正文，并通过四种彼此独立的审查：事实一致性、竞赛表达、全文连贯、AI/口水文风。Reviewer 永久只写修改单；原问题作者修局部，Leader 组装并统一全文。

停止于 `paper-writing/formal-paper-handoff.md`，正文为 `paper-writing/manuscript/final-paper.md`。后续排版与最终交付不得改变已冻结的数字、公式、单位和 claim。

## 2. Team 与文件所有权

- **Leader/全文作者**：写 PW0/PW1、公共章节、摘要结论、全部 `manuscript/` 版本、全局 response 与最终 handoff；只有 Leader 可修改全文主稿。
- **Question Manuscript Writer**：每问一个新 Agent，只写自己的 `sections/qN/section-v1.md`；事实修订时复用原 Agent写 response/v2。
- **Full-Paper Fact Auditor**：新 Agent，独立核对全文数字、公式、单位、claim、表图和题间接口；只写 fact review，PW6 复用做事实回归。
- **Competition Expression Reviewer**：新 Agent，只检查竞赛答题感、信息密度、方法动机、结果解释和重点分配；PW6 复用关闭原问题。
- **Full-Paper Coherence Reviewer**：新 Agent，只检查定义顺序、章节关系、题间过渡、摘要正文结论闭合与表图引用；PW6 复用关闭原问题。
- **AI Prose Auditor**：新 Agent，只检查可定位的机械、空洞、工程化和口水表达；不判断作者身份，不给 AI 分数，不直接改文；PW6 复用关闭原问题。

四个 Reviewer 互不读取 peer review 或 Leader 辩护。PW5 三个语言/结构 Reviewer 必须读取同一个冻结的 `full-paper-v2.md`，不能边审边看改稿。

## 3. PW0：正式写作输入冻结

Leader 写 `paper-writing/scope/frozen-inputs.md`，至少冻结：

- paper framework、章节地图、逐问当前材料和符号注册表；
- validation handoff/claim map、授权公式、数字、条件和禁止表达；
- figure handoff、Figure/Table ID、正式图片状态和占位方式；
- 官方页数、格式、匿名、语言和答卷要求；
- 已有参考文献、待补引用和禁止虚构来源；
- references handoff、claim-to-citation map、references.bib、引用键和人的意见边界；
- 旧材料、旧数字、未验证候选和上游只读边界；
- 每问 writer/reviewer 句柄、写入根与版本保留规则。

缺正式图片或引用不阻塞内容写作，但必须保持可追踪占位；缺验证授权阻塞对应 claim。

## 4. PW1：Leader 写作计划

Leader 写：

- `plan/writing-plan.md`：章节顺序、写作波次、输入版本和总篇幅；
- `plan/section-contracts.md`：逐问输入、必须回答、篇幅、Figure/Table、禁止扩张和唯一写入根；
- `plan/prose-boundary.md`：必要技术术语、正文/附录边界、工程词禁区和不可随意替换的数学名词；
- `plan/figure-table-slots.md`：稳定 ID、来源、引入位置、caption 状态和回填规则。

这些计划是开放 Markdown，不是固定论文目录。Leader 不在每问 writer 开始前预写其正文措辞。

## 5. PW2：逐问正式正文

每问创建一个新的 Question Manuscript Writer。它只读对应 section contract、最终章节材料、全局符号/术语和获批表图，写 `sections/qN/section-v1.md`。

正文必须是连续竞赛论文内容，而不是提纲或工程索引，至少涵盖：问题分析、模型选择理由、假设/变量/公式、模型建立与求解、验证结果与解释、已审引用、表图引入与图后说明、评价/限制和题间过渡。

不得把 run、config、debug、pipeline、文件路径、调参日志和版本处理写入正文，除非它们对可复现性不可替代且 section contract 明确要求。不得自行写摘要、总结合并段或修改其他问题。

## 6. PW3/PW4/PW4R：全文 v1、事实审查与事实修订

所有 section-v1 落盘后，Leader 写公共章节、摘要、关键词、全局假设与符号、结论、优缺点和推广，统一术语、公式编号、表图占位和篇幅，形成 `manuscript/full-paper-v1.md`。

Leader 随后创建新的 Full-Paper Fact Auditor。它只读 v1、验证授权证据、结果表、公式来源和 figure handoff，写 `reviews/fact-consistency-review.md`，逐项检查：

- 数字、公式、单位、精度、总体、条件和 claim；
- 摘要、正文、结论之间的结果一致性；
- Figure/Table/caption 与正文；
- 题间 producer–consumer 接口；
- 限制是否在正文保留。

每项必须含正文位置、来源、失败影响和责任 owner，不用笼统“有误”。同时检查引用键是否来自 references handoff、引用句是否越过文献支持范围、人的意见是否被写成事实。

PW4R 中，局部事实问题退给原 Question Manuscript Writer，写 `section-fact-response.md` 和 `section-v2.md`；全局复述由 Leader 修；上游证据错误写 change request。Leader 保留 v1，写 `responses/fact-response.md` 和 `manuscript/full-paper-v2.md`。

## 7. PW5：三路语言与全文独立审查

在 `full-paper-v2.md` 冻结后，并行创建三个新 Reviewer。三者只读各自白名单，不读 peer review。

### 7.1 Competition Expression Reviewer

只写 `reviews/competition-expression-review.md`，检查每问答案是否醒目、模型选择是否有理由、结果是否解释、摘要是否交代方法/结果/结论、内容是否像说明书/教程/开发报告、篇幅与重点是否符合竞赛阅读需要。不得猜评分权重或以国奖范文替代本题判断。

### 7.2 Full-Paper Coherence Reviewer

只写 `reviews/full-paper-coherence-review.md`，检查定义—公式—结果顺序、章节和题间逻辑、符号/术语/模型名、摘要—正文—结论闭合、表图引入与解释，以及未定义、未使用、重复或相互矛盾的内容。

### 7.3 AI Prose Auditor

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

三份 review 全部落盘后，Leader 写 `responses/language-review-response.md`。逐问专业事实退给原 writer；章节逻辑、摘要结论、过渡和统一语气由 Leader 修。冲突按“事实准确 > 答题直接 > 表达简洁”裁决，形成 `manuscript/full-paper-v3.md`，默认一次集中语言修订。

PW6 复用原四个 Reviewer，各自只检查原 review 的处置：Fact Auditor 做数字/公式/条件/claim 回归；其余三者检查原定位问题是否关闭。分别写 `reviews/closure/` 下的四份 closure，不开启新一轮全面审稿。

事实错误必须修；影响答题或全文矛盾的内容局部重开；纯风格偏好在一轮后保留 Leader 版本或升级用户，不无限润色。

## 9. PW7：正式论文交接

Leader 根据 v3 和 closure 形成 `manuscript/final-paper.md` 与 `formal-paper-handoff.md`。Handoff 至少链接正文版本、授权结果/公式、Figure/Table、references handoff/references.bib、四类 review、关闭状态、未完成图片/引用/排版/提交事项，以及后续不得改变的数字、公式、单位和 claim。

完成后停止，不生成 Word/LaTeX、正式图片、参考文献检索、版式文件、答卷或提交包。

## 10. 目录与开放交接

```text
paper-writing/
├── scope/frozen-inputs.md
├── plan/{writing-plan.md,section-contracts.md,prose-boundary.md,figure-table-slots.md}
├── sections/qN/{section-v1.md,section-fact-response.md,section-v2.md}
├── manuscript/{full-paper-v1.md,full-paper-v2.md,full-paper-v3.md,final-paper.md}
├── reviews/
│   ├── fact-consistency-review.md
│   ├── competition-expression-review.md
│   ├── full-paper-coherence-review.md
│   ├── ai-prose-review.md
│   └── closure/
├── responses/{fact-response.md,language-review-response.md}
├── change-requests/
└── formal-paper-handoff.md
```

所有语义内容使用开放 Markdown；模板问题只是最低责任。JSON 只保存配置、路径、版本、哈希、运行参数和状态，不裁决事实或文风。
