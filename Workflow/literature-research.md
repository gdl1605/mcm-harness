# 文献、人的意见与引用证据工作流

> 状态：已实现。本文定义 REF0–REF6。模块在宽候选路线和论文准备两次进入：前期用论文与人的意见验证、反驳并扩展候选模型，后期把最终主张映射为可核验引用。语义使用开放 Markdown；BibTeX 只承载引用元数据。

## 1. 目标与边界

文献不能只在论文末尾补，也不能在读题前先搜“C题常用模型”。路线 A/B 必须先从题意和数据独立产生宽候选，再由文献和人的意见挑战、校准和补充。前期检索不能只给 Agent 已想到的模型找背书，必须主动发现替代模型和失败证据。

模块使用四类来源：用户提供的论文/PDF、可访问的学术网络来源、官方标准/数据说明、可选的本地 Zotero 库。Zotero 不是依赖；没有 Zotero 时仍可运行。向 Zotero 导入或修改记录必须另获用户授权，本 workflow 只允许只读搜索或导出已存在条目。

人的意见是决策输入，不自动成为论文事实；文献数量、期刊名气、引用量和“有人这样做”都不能证明路线正确。竞赛获奖论文只能作为路线先例或表达参考，不能替代原始方法和领域证据。

## 2. 前期插入位置

```text
W5A Route A/B 隔离宽候选提案
⇉ W5B 结构 Critic（不读文献）
⇉ REF0–REF2 文献检索与人的意见
→ REF3 独立证据审查与路线证据交接
→ W5C 原 Route A/B 作者回应
→ L2C Leader 候选模型汇报
→ H1 真实人工模型决策
→ L2 Leader 按人工决定路线交接
```

W5B 与 REF0–REF2 相互隔离，避免结构审查被“论文很多/模型流行”锚定。W5C 才同时看到结构 review、文献证据和人的意见。REF2 领域咨询即使缺失也可记录缺口；H1 模型决策则是必须等待真实用户回复的强制停点，两者不能混为一谈。

## 3. REF0：路线检索合同

W5A 落盘后，Leader 为每条路线写 `literature/route-alignment/search-briefs/route-X.md`，同时按路线结构与逐问候选模型族拆成可检索问题：

- 领域内如何命名该对象、决策和约束；
- 核心结构假设是否有原始研究或官方依据；
- 方法需要的数据、识别条件、边界和计算代价；
- 有哪些替代路线、失败案例和负面证据；
- 是否存在当前 A/B 都未提出、但更适合该数据结构或答题目标的模型族；
- 哪些真实应用与本题相似，哪些差异使其不可直接迁移；
- 应向人类咨询什么，而不是泛问“哪个模型好”。

检索 brief 不预设必须找到支持路线的文献，也不使用另一路线的报告污染 Scout。

## 4. REF1：逐路线 Literature Scout

每条真实候选路线创建一个新的 Route Literature Scout。它只读本路线提案、题意基线和 search brief，写 `route-X/scout-memo.md`，并只在 Leader 预分配的非重叠 REF-ID 范围内建立 `sources/REF-ID/source-note.md`。Scout 必须逐候选核对适用前提，并主动把文献中新发现的候选加入报告，不受原提案清单限制。

来源优先级：

1. 原始方法论文、原始领域研究和官方标准/数据文档；
2. 同类问题的同行评议应用研究；
3. 高质量综述，只用于领域地图和继续追原始来源；
4. 二手教程/博客只可补实现线索，不能支撑关键 claim；
5. 竞赛论文只可说明曾有人采用某表达或路线，不证明方法正确。

每份 source note 至少记录：标题、作者、年份、DOI/URL、来源渠道、访问状态；论文真正研究的问题；数据、总体、假设、方法和评价；对本路线支持/削弱/替代的具体部分；与本题差异；不能推出什么；目前只核对元数据、摘要还是全文。

不得仅凭标题、搜索摘要或生成式摘要宣布支持。无法读取全文时标记限制，不虚构细节。避免长段引用，保留定位和自己的摘要。

## 5. REF2：人的意见

创建或复用一个 Human Consultation Recorder。它先写 `human-consultation/consultation-brief.md`，针对高影响差异提出 3–8 个具体问题，例如对象定义、现实约束、最容易遗漏的边界、结果解释、路线风险和建议检索词。

Leader 将 brief 交给用户、指导老师、队友或领域人员。Recorder 只能根据真实回复写 `human-consultation/response-record.md`，记录：提供者角色、看到的材料、回复时间、原意、理由、可能偏见、会改变的路线、是否有论文/数据支持。无需收集不必要个人信息。

不得由 Agent 模拟人类意见。未获得回复时记录“已请求但未获得”，比赛时间盒到期后可以继续，但 L2 必须保留这一缺口。

## 6. REF3：独立路线证据审查

创建新的 Literature Evidence Auditor。它不参与 Scout 搜索，只读题意、A/B 原提案、结构 critic、source notes、可访问来源和真实 human response，写 `route-alignment/evidence-review.md`。

Auditor 检查文献真实性、元数据、是否过度依赖摘要、假设/数据/总体可比性、选择性搜证、负面证据、替代方法和人的意见是否被包装成事实。每项说明来源、失败机制、路线影响和仍需 pilot 的问题，不按文献数量或声望投票。

Leader 据此写 `route-alignment/route-evidence-handoff.md`，交给原 Route A/B 作者在 W5C 回应。Handoff 区分：逐候选文献支持/削弱、人的经验判断、仍不可判、应调整假设、应加入的新候选或替代路线，以及需要数据判别的内容。它不选模型；L2C 之后由 H1 真实人工决定。

## 7. REF4：最终引用缺口地图

V6 完成且 CP1 已形成 `chapter-map-v0.md` 后，创建新的 Citation Gap Analyst。它只读验证授权主张、route evidence、章节地图、图表/论文准备输入和已有来源，写 `citation-preparation/citation-gap-map.md`。

逐项判断哪些内容需要外部引用：领域背景、数据来源、经典方法、数学算法来源、参数/假设的领域依据、与既有研究关系和方法适用范围。本队计算结果由自己的验证证据支持，不用外部论文冒充结果证明。

每个缺口形成 `CIT-###`，记录拟写主张、章节位置、需要何种来源、当前候选、检索词、不能接受的二手来源和若找不到应怎样降级表述。

## 8. REF5：定向 Citation Scout

按独立主题簇创建新的 Citation Literature Scout，不按每条引用制造 Agent。它只处理 gap map，写主题 scout memo、Leader 预分配 REF-ID 的 source notes 和 `scouts/TOPIC/references-candidate.bib`。不同 Scout 不得同时写共享候选库；全部返回后由 Leader 机械合并、去重为 `citation-preparation/references-candidate.bib`，再交 Citation Auditor。

每个建议引用必须映射到具体正文主张，说明文献实际支持的范围、建议引用位置、BibTeX key、Zotero item key（若来源于 Zotero）和禁止过度表达。Zotero item key 与 BibTeX key 必须分开记录。

如果使用本地 Zotero，先只读检查 status/search/inventory；同步或导出已存在条目可以执行到 run 目录。导入 BibTeX/RIS、保存新网页或修改 Zotero 库必须先取得用户授权。没有 Zotero 时由 Scout 生成候选 BibTeX，并保留来源链接和核验状态。

## 9. REF6：引用独立审查与交接

创建新的 Citation Auditor。它只读 gap map、source notes、候选 BibTeX、验证 claim 和章节地图，写 `citation-preparation/citation-audit.md`，检查：

- 文献、作者、标题、年份、DOI/URL 和引用键是否真实一致；
- 正文主张是否被该文献直接支持，是否把相关写成因果；
- 是否用综述/二手文献替代可获得的原始来源；
- 是否引用未实际查看的内容或重复生成多个 key；
- 引用位置、claim、限制和参考文献表能否互相链接；
- 人的意见是否仍被清楚标为意见。

Auditor 只写 review，不直接修改 source notes 或 BibTeX。Leader 根据 review 机械整理 `literature/references.bib`、`citation-preparation/claim-to-citation-map.md` 和 `citation-preparation/references-handoff.md`；不确定条目保留 `[CITATION-NEEDED-ID]`，不得编造。

REF6 handoff 必须在 CP6 和 PW0 前可用。新的文献如果推翻核心路线或验证主张，不能只改引用，应返回 L2、建模或验证的最早受影响阶段。

## 10. 目录与停止边界

```text
literature/
├── scope/
├── route-alignment/
│   ├── search-briefs/
│   ├── route-a/
│   ├── route-b/
│   ├── sources/REF-ID/source-note.md
│   ├── human-consultation/{consultation-brief.md,response-record.md}
│   ├── evidence-review.md
│   └── route-evidence-handoff.md
├── citation-preparation/
│   ├── citation-gap-map.md
│   ├── search-briefs/
│   ├── scouts/
│   ├── sources/REF-ID/source-note.md
│   ├── references-candidate.bib
│   ├── claim-to-citation-map.md
│   ├── citation-audit.md
│   └── references-handoff.md
└── references.bib
```

路线部分在 `route-evidence-handoff.md` 暂停并交给 W5C/L2C/H1；完整模块在 `references-handoff.md` 停止。正式论文 Writer 只能使用 handoff 授权的引用或显式 `[CITATION-NEEDED-ID]`。
