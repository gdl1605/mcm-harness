# C 题 Agent Team：详细调度工作流

本文是 Leader 的逐波调度手册。根目录 `AGENTS.md` 规定 Leader 的行为、判断纪律和文件路由；本文说明每一波创建谁、复用谁、给什么 prompt、允许看什么、写到哪里。各模块 `*-team.json` 只是同一安排的机器可读清单，不能替代本文。

当前实现范围包括独立验证、两条准备支线、sol-high 正式绘图、正式论文 Markdown 写作，以及最终排版终审与人工交接：

```text
题意诊断、宽候选与人工模型决策 W0–H1–L2
⇉ W5A 后文献/人的意见 REF0–REF3
→ 数据工程 D0–D5
→ 建模构建 M0–M6
→ 独立模型验证 V0–V6
→ validation/validation-handoff.md
⇉ 图表准备 F0–F4 / 论文准备 CP0–CP6
⇉ CP1 后正式引用 REF4–REF6
→ 分别停止于 figure-preparation-handoff / paper-framework-handoff
⇉ 正式绘图 FR0–FR4 / 正式论文写作 PW0–PW7
→ 停止于 figure-rendering-handoff / formal-paper-handoff
→ 最终交付 FD0–FD7
→ 停止于 final-delivery/final-delivery-handoff.md
```

文献模块在 W5A 后验证、反驳并扩展候选，H1 由真实用户选择模型，在 V6/CP1 后补齐正式引用；图表支线准备数据和图型建议；正式绘图使用强制 sol-high Producer/Reviewer 生成与审查正式图片；论文准备和正式写作可与绘图并行。最终交付消费 rendering handoff 与已审引用，生成候选包和支撑材料，冻结后只审不改并交给人微调。实际投稿仍不在本模块内。

## 1. Leader 怎样使用本文

开始前，Leader 必须先读根目录 `AGENTS.md`，再按当前模块读取：

- 前半程配置：`Workflow/team.json`
- 前半程 Leader prompt：`prompts/leader.md`
- 文献与引用配置：`Workflow/literature-team.json`
- 文献与引用设计：`Workflow/literature-research.md`
- 文献与引用 Leader prompt：`prompts/literature/leader.md`
- 数据工程配置：`Workflow/data-team.json`
- 数据工程设计：`Workflow/data-engineering.md`
- 数据工程 Leader prompt：`prompts/data-engineering/leader.md`
- 建模构建配置：`Workflow/modeling-team.json`
- 建模构建设计：`Workflow/modeling-construction.md`
- 建模构建 Leader prompt：`prompts/modeling/leader.md`
- 独立验证配置：`Workflow/validation-team.json`
- 独立验证设计：`Workflow/model-validation.md`
- 独立验证 Leader prompt：`prompts/validation/leader.md`
- 图表准备配置：`Workflow/figure-preparation-team.json`
- 图表准备设计：`Workflow/figure-preparation.md`
- 正式绘图配置：`Workflow/formal-figure-team.json`
- 正式绘图设计：`Workflow/formal-figure-rendering.md`
- 正式绘图 Leader prompt：`prompts/formal-figures/leader.md`
- 论文准备配置：`Workflow/paper-preparation-team.json`
- 论文准备设计：`Workflow/paper-preparation.md`
- 论文准备 Leader prompt：`prompts/paper-preparation/leader.md`
- 正式写作配置：`Workflow/paper-writing-team.json`
- 正式写作设计：`Workflow/paper-writing.md`
- 正式写作 Leader prompt：`prompts/paper-writing/leader.md`
- 最终交付配置：`Workflow/final-delivery-team.json`
- 最终交付设计：`Workflow/final-delivery.md`
- 最终交付 Leader prompt：`prompts/final-delivery/leader.md`
- 图表准备 Leader prompt：`prompts/figure-preparation/leader.md`

每个 subagent 的完整派工上下文由三部分拼成：

```text
当前模块 worker-base prompt
+ 当前角色 prompt
+ 本轮开放 task brief
```

前半程使用：

```text
prompts/worker-base.md
+ 下表指定的 prompts/roles/*.md
+ 基于 templates/task-brief.md 写出的本轮 brief
```

文献与引用使用：

```text
prompts/literature/worker-base.md
+ 当前角色 prompt
+ 基于 templates/literature/task-brief.md 的开放 brief
```

文献 Scout 必须区分元数据、摘要和全文状态并搜索负面/替代证据；Human Recorder 不能模拟人的意见；Auditor 只写 review。Zotero 可选且默认只读。

数据工程使用：

```text
prompts/data-engineering/worker-base.md
+ 下表指定的 prompts/data-engineering/*.md
+ 基于 templates/data-engineering/task-brief.md 写出的本轮 brief
```

数据工程不得加载 `prompts/leader.md` 或 `prompts/worker-base.md`。前半程 prompt 的停止边界禁止正式数据工程。

建模构建使用：

```text
prompts/modeling/worker-base.md
+ 下表指定的 prompts/modeling/*.md
+ 基于 templates/modeling/task-brief.md 写出的本轮 brief
```

建模阶段不得加载数据工程角色 prompt 继续清洗；数据变化通过上游变更请求返回数据模块。

独立验证使用：

```text
prompts/validation/worker-base.md
+ 下表指定的 prompts/validation/*.md
+ 基于 templates/validation/task-brief.md 写出的本轮 brief
```

验证者只在 `validation/` 中写审计、probe 和裁决产物。发现数据或模型问题时返回原模块，不直接修改上游实现。

图表准备使用：

```text
prompts/figure-preparation/worker-base.md
+ 当前角色 prompt
+ 基于 templates/figure-preparation/task-brief.md 的开放 brief
```

图表 worker 只在自己的 `figure-prep/` 问题或共享目录中写诊断、数据包和 review。它们不得修改 `data/`、`modeling/`、`validation/` 或论文草稿；正式绘图交给 FR0–FR4。

正式绘图使用：

```text
prompts/formal-figures/worker-base.md
+ prompts/formal-figures/question-visual-producer.md 或 figure-portfolio-reviewer.md
+ 基于 templates/formal-figures/task-brief.md 的开放 brief
```

Leader 创建每个新 Producer/Reviewer 时必须显式指定 `model=gpt-5.6-sol`、`reasoning_effort=high`、`fork_turns=none`，并写 `formal-figures/scope/dispatch-log.json`。默认 Luna 禁止；覆盖不可用时停止并报告。Producer 每问/共享单元一个，负责规划、绘制和回应；默认一个 Portfolio Reviewer 统一审准确性、图型、审美和真实版面。

论文准备使用：

```text
prompts/paper-preparation/worker-base.md
+ 当前角色 prompt
+ 基于 templates/paper-preparation/task-brief.md 的开放 brief
```

论文准备 worker 只写自己的问题目录或获批的 structure/shared/integration 路径；不得修改上游证据，也不得生成完整论文。Competition Reviewer 第一遍禁止看到国奖论文蒸馏，blind memo 落盘后才允许第二遍加载。

正式写作使用：

```text
prompts/paper-writing/worker-base.md
+ 当前角色 prompt
+ 基于 templates/paper-writing/task-brief.md 的开放 brief
```

Question Writer 只写本问 section；四个 Reviewer 只写修改单；Leader 是全文主稿、全局 response 和最终 handoff 的唯一 owner。不得调用 AI 检测器或自动改写。

最终交付使用：

```text
prompts/final-delivery/worker-base.md
+ 当前角色 prompt
+ 基于 templates/final-delivery/task-brief.md 的开放 brief
```

Supporting Material Curator 只写结果数据和完整运行脚本源码包；Typesetter 只在 candidate freeze 前处理版式；FD4 五个 Reviewer 只写报告，其中 End-to-End Consistency Auditor 使用 fresh context 反查全链路 handoff。终审开始后所有候选和支撑材料只读，Leader 只建立人工问题索引与 handoff。

Task brief 中的 A/B/C/D 是最低必答问题，不是报告字段白名单。subagent 可以改变报告结构，并必须继续报告任何会改变题意、数据边界、题间接口、风险或路线的新发现。

## 2. 通用派工动作

每次派工都按以下顺序执行：

1. Leader 确认当前波次、唯一目标和并发范围。W/D/M/V 每波最多 3 个 worker；图表、正式绘图、论文准备、PW2、FD4 独立终审和文献 Scout 按隔离写入根派工，不受该数字上限约束。正式绘图额外强制 sol-high。
2. 根据下表决定创建新 subagent，还是复用原 subagent。
3. 从对应模板新建开放 task brief，写明允许读取、禁止读取、唯一主输出路径、额外工程写入权限和停止条件。
4. 向 subagent 发送完整三段 prompt，并直接给出绝对或 run 内可解析路径。
5. W/D/M/V 等同步波等待本波全部 subagent 返回、失败或取消；图表 F2 与论文 CP3 按问题流式等待；PW5 三个 Reviewer 同波等齐后综合；FD4 五个 Reviewer 同快照等齐后只建立人工问题索引。
6. 核对指定 Markdown 已落盘。聊天摘要不能代替原始 memo。
7. 保留原报告后再综合；不得把报告压成固定 JSON 字段后删除框架外发现。

创建与复用规则：

- 隔离盲读、新鲜视角、独立攻击和独立验证：创建新 subagent。
- 复核某个原判断：复用提出该判断的 W1/W2 subagent。
- 回应路线评审：复用原 Route A 或 Route B 提案者。
- 回应数据评审并修订：复用原 D3 数据管道实现者。
- 独立验证 V1 三视角和强题间依赖 V6 整体审计：创建新 subagent。
- V3 定向 probe：复用提出该问题的 auditor；V4 回应：复用原 model/data owner。
- 原 owner 因验证证据修正后，若旧 holdout 已消耗，使用新独立证据并在必要时创建 fresh-context auditor。
- 图表 F1 每问或共享结果单元创建一个新 Question Figure Curator；F2 每个 package 落盘后立即流式创建一个新 Figure Evidence Auditor；F2R 复用原 Curator；F3 创建一个新 Figure–Chapter Integrator。
- 正式绘图 FR1 每问/共享单元创建一个显式 sol-high Visual Producer，不按图拆 Agent；FR2 创建一个 fresh-context sol-high Portfolio Reviewer；FR2R/FR3 分别复用原 Producer/Reviewer；FR4 Leader 独写 manifest/handoff。
- F3 Integrator 是 `figure-plan.md` 与 `figure-preparation-handoff.md` 的唯一内容 owner；F4 Leader 只核对条件、处理回滚和宣布汇合。
- 论文 CP1 创建新 Structure Architect；CP2 每问新 Curator；CP3 每个 v1 完成即创建新 Evidence Auditor；CP3R 复用原 Curator；CP4 创建新 Integrator；CP5 创建新 Competition Reviewer。
- CP5 blind review 落盘前禁止加载国奖论文蒸馏；第二遍和关闭检查复用同一 Reviewer。CP5R/CP6 复用原 Integrator，事实修订复用原 Question Curator。
- PW2 每问新建 Question Manuscript Writer；PW4R 复用原 writer。PW4 新建 Fact Auditor；PW5 新建三个独立 Reviewer；PW6 复用原四个 Reviewer。
- PW3/PW5R/PW7 全文主稿和 handoff 只由 Leader写，不创建全文作者 subagent。
- FD1 创建新 Supporting Material Curator；FD2 创建新 Submission Typesetter，FD3 只复用原 Typesetter 修纯机械问题；FD4 创建五个互相隔离的新 Reviewer，其中全链路审查者必须 fresh-context；FD5–FD7 只由 Leader 写人工索引和 handoff，不创建修稿角色。
- REF1 每路线新建 Scout，REF2 真实人类回复后复用 Recorder，REF3 新建 Literature Auditor；REF4 新建 Gap Analyst，REF5 每主题簇新建 Scout，REF6 新建 Citation Auditor。
- L2C 候选汇报由 Leader 独写；H1 不创建 Agent，只等待真实用户决定并忠实记录，决定缺失时禁止 L2/D0/M0。
- route-evidence-handoff、references.bib、claim-to-citation map 和 references-handoff 由 Leader 整理；Auditor 不修改来源或 BibTeX。
- 没有独立输入或只会重复已有报告：不创建角色。

## 3. 前半程总览

```text
W0 来源封箱
→ W1/W2 六角色隔离盲读
→ Leader 首次综合
→ W3 新 reviewer 交叉审查
→ W3R 原判断角色复核
→ W4 定向消歧/反共识
→ L1 暂定题意基线
→ W5A A/B 隔离生成宽候选
⇉ W5B 独立结构审查 / REF0–REF2 文献与真实人类咨询
→ REF3 文献证据独立审查
→ W5C 原路线提案者按证据重构候选
→ L2C Leader 候选模型汇报
→ H1 真实人工模型决策
→ L2 Leader 按人工决定路线交接
```

### W0：来源封箱

| 项目 | 安排 |
|---|---|
| 执行者 | Leader，不创建 subagent |
| Leader prompt | `prompts/leader.md` |
| 必读协议 | `Workflow/protocols/deep-reading-protocol.md` |
| 输入 | 用户提供的原题、附件、答卷要求、官方说明 |
| 动作 | 计算来源哈希，记录版本、路径、可读性和缺失项；原始材料转为只读 |
| 输出 | `inputs/source-manifest.json` |
| 停止条件 | 来源清单能区分原题、附件、模板与补充说明；缺失或损坏已显式记录 |

W0 的 JSON 只记录路径、哈希、版本和机械状态，不承载题意判断。

### W1：三角色隔离盲读

W1 创建 3 个新 subagent 并行运行。三者只看原始材料、`inputs/source-manifest.json` 和自己的 brief，互相不可见，Leader 不先表达观点。

| 角色 | 创建方式 | 角色 prompt | 最低关注 | 主输出 |
|---|---|---|---|---|
| 字面契约审读者 | 新 subagent | `prompts/roles/literal-contract.md` | 逐句拆解对象、动词、量词、单位、粒度、约束、交付口径和歧义 | `submissions/W1/literal-contract.md` |
| 题链架构师 | 新 subagent | `prompts/roles/dependency-architect.md` | 每问输入/输出、共享量、正向依赖、末问反演和可消费接口 | `submissions/W1/dependency-architect.md` |
| 数据法证员 | 新 subagent | `prompts/roles/data-forensics.md` | 附件字段、主键、时间、粒度、单位、proxy、泄漏、缺失和不可构造目标 | `submissions/W1/data-forensics.md` |

### W2：三角色隔离补充盲读

W2 再创建 3 个新 subagent。即使 W1 已完成，W2 仍不得读取 W1 报告或 Leader 综合，避免锚定。

| 角色 | 创建方式 | 角色 prompt | 最低关注 | 主输出 |
|---|---|---|---|---|
| 数学结构分析者 | 新 subagent | `prompts/roles/formulation-analyst.md` | 变量、状态、决策、目标、约束、识别条件与结构性备选；首轮不按模型名套题 | `submissions/W2/formulation-analyst.md` |
| 未知陷阱猎手 | 新 subagent | `prompts/roles/trap-hunter.md` | 指代、边界、总体、时间、信息可用时点、附件闲置字段和反例 | `submissions/W2/trap-hunter.md` |
| 作答范围审查者 | 新 subagent | `prompts/roles/answer-scope-reviewer.md` | 每问最低回答、证据负担、有效增强、停止线、答卷模板和交付物 | `submissions/W2/answer-scope-reviewer.md` |

### W1/W2 后：Leader 首次综合

| 项目 | 安排 |
|---|---|
| 执行者 | Leader，不创建 subagent |
| 必读协议 | `Workflow/protocols/deliberation-protocol.md` |
| 输入 | 六份 W1/W2 原始 memo 与原始来源 |
| 模板 | `templates/leader-synthesis.md` |
| 输出 | `synthesis/leader-synthesis.md` |

Leader 只归并共同认识、实质冲突、少数意见、待区分问题和框架外发现，不宣布题意已经正确。相互冲突的原文判断必须保留来源链接。

### W3：新 reviewer 定向交叉审查

W3 创建 3 个新的 cross-examiner。每人只读取被分配的一组原始 memo、必要原始来源和自己的 brief。推荐配对如下：

| 审查组 | 创建方式 | 角色 prompt | 审查对象 | 主输出 |
|---|---|---|---|---|
| 字面契约 × 作答范围 | 新 subagent | `prompts/roles/cross-examiner.md` | W1 字面契约与 W2 作答范围 | `reviews/W3/literal-vs-answer-scope.md` |
| 题链 × 数据法证 | 新 subagent | `prompts/roles/cross-examiner.md` | W1 题链与 W1 数据法证 | `reviews/W3/dependency-vs-data.md` |
| 数学结构 × 未知陷阱 | 新 subagent | `prompts/roles/cross-examiner.md` | W2 数学结构与 W2 陷阱报告 | `reviews/W3/formulation-vs-traps.md` |

模板使用 `templates/cross-review.md`。Reviewer 先准确复述和钢人化原判断，再给出来源证据、具体失败机制、会改变的答卷内容和可区分办法。泛泛的“可能有问题”不算有效质询。

### W3R：原判断角色复核

这里不是“论文原作者回应”。“原判断角色”指在 W1/W2 中写出被质询判断的那个 subagent。

| 项目 | 安排 |
|---|---|
| 调度 | 复用对应 W1/W2 subagent，不创建替代作者 |
| 角色 prompt | `prompts/roles/original-judgment-review.md` |
| 可读 | 自己的原 memo、指向自己的 W3 review、必要原始来源 |
| 不可读 | 其他未分配 review、Leader 倾向、其他角色答辩 |
| 输出 | `submissions/W3R/<original-role>-review.md` |

每个被质询的判断只有一次正式复核：承认并修订、用证据维持原判断、或保留竞争解释并提出区分条件。W3R 结束后不继续纯文字拉扯。

### W4：定向消歧与反共识

W4 只为仍会改变答卷对象、变量/约束、粒度/单位、题间接口或路线结构的争议创建 1–3 个新 subagent。

| 场景 | 创建方式 | 角色 prompt | 任务 | 主输出 |
|---|---|---|---|---|
| 存在低成本区分办法 | 新 subagent | `prompts/roles/probe-designer.md` | 设计来源复核、字段/单位/时间检查、玩具样例或边界反例；不做正式训练求解 | `reviews/W4/probe-<issue>.md` |
| 全员过快一致或疑似共同锚定 | 新 fresh-context subagent | `prompts/roles/fresh-context-reviewer.md` | 在尽量少的历史结论下攻击共识，寻找最小失效措辞或字段 | `reviews/W4/fresh-context-review.md` |

探针 memo 使用 `templates/probe-memo.md`。能安全做的低成本机械取证可以执行；正式 EDA、训练、求解和模型评分留给后续模块。高影响且不可判的问题保留分支或交给用户。

### L1：Leader 暂定题意基线

| 项目 | 安排 |
|---|---|
| 执行者 | Leader，不创建 subagent |
| 输入 | W1–W4 全部原始 memo、来源与 `synthesis/leader-synthesis.md` |
| 模板 | `templates/problem-baseline.md` |
| 输出 | `synthesis/problem-baseline.md` |

基线应说明每问要回答什么、最低做到多少、题间接口、数据边界、当前工作解释、仍存少数意见、禁止默认事项和重开触发器。它是可回滚的执行版本，不是语义正确性证明。

### W5A：A/B 隔离生成宽候选

L1 完成后才允许路线角色读取模型资料。创建 2 个新 subagent 并行运行，首轮互不可见。

| 角色 | 创建方式 | 角色 prompt | 路线责任 | 主输出 |
|---|---|---|---|---|
| Route A 提案者 | 新 subagent | `prompts/roles/route-proposer.md` | 给出最低完整的题链，并按问题展开多个结构不同的候选模型族 | `routes/route-a.md` |
| Route B 挑战提案者 | 新 subagent | `prompts/roles/route-proposer.md` | 挑战实质结构假设，形成另一组宽候选并指出可能遗漏的方向 | `routes/route-b.md` |

两者均用 `templates/route-proposal.md`，但 brief 中必须写清 A/B 的不同责任。每问先展开结构方向，再具体化多个候选；数量不是硬配额，不用同一家族算法/超参数凑数，也不因当前依赖或实现难度隐藏适配候选。B 若找不到实质结构差异，应如实说明并请求回到题意争议。

### W5B：独立路线审查

| 项目 | 安排 |
|---|---|
| 调度 | 创建 1 个新 subagent |
| 角色 prompt | `prompts/roles/route-critic.md` |
| 可读 | `synthesis/problem-baseline.md`、`routes/route-a.md`、`routes/route-b.md` 与必要原始来源 |
| 模板 | `templates/route-review.md` |
| 输出 | `routes/route-review.md` |

Critic 先分别钢人化两案，再比较对象、状态量、决策量、约束、题间接口、证据负担、识别风险、候选结构宽度、伪多样性和遗漏方向。不得按模型新颖度或投票决定胜者，也不替用户选模型。W5B 与 REF0–REF2 并行，Critic 禁止读取文献检索和人的意见。

### REF0–REF3：路线文献与人的意见校准

完整设计见 [`Workflow/literature-research.md`](literature-research.md)。W5A 后由 Leader 为 A/B 分别写 route-and-candidate search brief；每方向创建新的 Route Literature Scout，使用 `prompts/literature/route-literature-scout.md`。Scout 逐候选检索原始来源、官方依据、应用、限制和负面证据，并用不带既有模型名的结构检索发现新候选；不能只给现有方案找背书或只列标题。

并行创建 Human Consultation Recorder，使用 `prompts/literature/human-consultation-recorder.md`。它先写具体咨询问题；Leader 把问题交给真实用户、老师、队友或领域人员，收到回复后复用原 Recorder 忠实记录。没有回复时只记缺口，Agent 永久不能模拟人的意见。

REF1/REF2 完成后创建新的 Literature Evidence Auditor，使用 `prompts/literature/literature-evidence-auditor.md`。它审来源真实性、摘要过度推断、可比性、选择性搜证、替代模型遗漏和人的意见边界，只写 evidence review。Leader 形成逐候选的 `literature/route-alignment/route-evidence-handoff.md`。REF2 咨询可以记录缺口继续，但不能代替 H1 强制人工决策。

Zotero 可作为只读来源；Zotero item key 与 BibTeX key 分开。导入、保存或修改本地库必须另获用户授权。

### W5C：原路线提案者回应

这里的回应者是 W5A 的 Route A/B 提案 subagent，不是新 reviewer。

| 角色 | 调度 | 角色 prompt | 可读 | 主输出 |
|---|---|---|---|---|
| Route A 回应者 | 复用原 Route A subagent | `prompts/roles/route-proposer-response.md` | 自己的路线、题意基线、结构审查和 route evidence 中与 A 有关部分 | `routes/responses/route-a-response.md` |
| Route B 回应者 | 复用原 Route B subagent | `prompts/roles/route-proposer-response.md` | 自己的路线、题意基线、结构审查和 route evidence 中与 B 有关部分 | `routes/responses/route-b-response.md` |

每条路线只做一次正式回应：按结构 review 与逐候选文献证据增加、合并、缩小、降级或撤回候选，保留不可判分歧。回应不得提前选唯一主模型，也不得执行数据清洗、训练或求解。

### L2C：Leader 候选模型汇报

| 项目 | 安排 |
|---|---|
| 执行者 | Leader，不创建新的选择角色 |
| 必读协议 | `Workflow/protocols/route-tournament.md` |
| 输入 | 题意基线、A/B 原提案、结构审查、逐候选 route-evidence-handoff、真实咨询记录和两份 W5C 回应 |
| 模板 | `templates/model-candidate-briefing.md` |
| 输出 | `routes/model-candidate-briefing.md` |

Leader 逐问展示值得人选择的完整候选范围，说明结构、适配理由、文献支持/削弱、优劣势、假设、失败风险、题间作用、实现/验证成本和竞赛价值；另给主选、备选/敏感性、baseline 和不推荐意见。不得只展示首选，也不得因为库未安装、代码较难或简单模型没报错而隐藏候选。

### H1：真实人工模型决策

Leader 将完整 briefing 交给用户，并把状态置为 `AWAITING_HUMAN_MODEL_DECISION`。此时不创建 subagent，也不得进入 L2、D0 或 M0。

用户可以选择主模型；选择主模型加备选/敏感性模型；要求补文献或扩展候选；全部否决；或规定时间、依赖和实现限制。只有收到真实回复后，Leader 才能使用 `templates/human-model-decision.md` 忠实记录为 `routes/human-model-decision.md`。REF2 咨询、Agent 判断、超时或沉默均不构成批准。

### L2：Leader 按人工决定路线交接

| 项目 | 安排 |
|---|---|
| 执行者 | Leader，不创建 subagent |
| 必读协议 | `Workflow/protocols/route-tournament.md` |
| 输入 | L2C briefing、真实 H1 决定及其全部题意、路线、结构和文献依据 |
| 模板 | `templates/route-handoff.md` |
| 输出 | `routes/route-handoff.md` |

Leader 按人工决定交接主模型、保留备选/挑战/敏感性模型、仅作 baseline、明确放弃项、共同安全核心、数据要求、题间接口和重新 H1 条件。后续若必须改变模型家族、目标或核心结构，使用 `templates/model-selection-change-request.md` 写 `routes/change-requests/REQUEST-ID.md` 并重新等待真实决定，不得静默降级。完成后前半程立即停止。

## 4. 数据工程总览

进入数据工程前，Leader 必须确认真实 H1 决定和按其形成的 L2 均已落盘，再显式切换到 D0 并改用数据工程 prompt：

```text
D0 接收与模式选择
→ D1 数据契约/剖析/风险三路调查
→ D2 Leader 数据方案
→ D3 单一实现者统一实现
→ D4 新 reviewer 独立复核
→ D4R 原实现者集中回应与修订
→ D5 Leader 数据交接
```

完整原则和角色合同见 `Workflow/data-engineering.md`；以下是 Leader 的实际派工表。

### D0：接收前半程与选择模式

| 项目 | 安排 |
|---|---|
| 执行者 | Leader，不创建 subagent |
| Leader prompt | `prompts/data-engineering/leader.md` |
| 必读 | `Workflow/data-engineering.md`、`Workflow/data-team.json`、`synthesis/problem-baseline.md`、`routes/model-candidate-briefing.md`、真实 `routes/human-model-decision.md`、`routes/route-handoff.md` 与相关前半程原始 memo |
| task brief 模板 | `templates/data-engineering/task-brief.md` |
| 输出 | 完整模式的 `data/briefs/D1/*.md`；精简模式另写 `data/decisions/lean-mode-rationale.md` |

默认采用完整模式。只有单表、字段清楚、连接和时间风险低、没有实质跨问接口风险时才可选精简模式，并逐条记录理由。

### D1：三角色隔离调查

完整模式创建 3 个新 subagent 并行运行。三者只读原始来源、冻结的题意/路线交接和自己的 brief，不读同伴报告或 Leader 清洗偏好。

| 角色 | 创建方式 | 角色 prompt | 最低关注 | 主输出 |
|---|---|---|---|---|
| 数据契约架构师 | 新 subagent | `prompts/data-engineering/data-contract-architect.md` | 表/对象/主键/粒度/时间/单位/字段语义、题间共享规范层与分析视图接口 | `data/contracts/data-contract.md` |
| 数据剖析员 | 新 subagent | `prompts/data-engineering/data-profiler.md` | 可复现剖析、规模、分布、连接覆盖、重复、缺失、零值、时间范围与异常现象 | `data/profiling/data-profile.md` |
| 数据风险审查员 | 新 subagent | `prompts/data-engineering/data-risk-reviewer.md` | proxy、泄漏、信息时点、总体偏移、错误聚合、结构性空值和不可逆清洗风险 | `data/reviews/data-risk-review.md` |

精简模式跳过 D1 subagent 波次，但不能由 Leader 假装三种独立意见，也不能取消 D3 单一实现者和 D4 独立复核。

### D2：Leader 数据方案

| 项目 | 安排 |
|---|---|
| 执行者 | Leader，不创建 subagent |
| 输入 | 三份 D1 原始报告、题意基线、路线交接和来源 |
| 模板 | `templates/data-engineering/preprocessing-plan.md` |
| 输出 | `data/decisions/preprocessing-plan.md` |

数据方案冻结原始层、规范层和每问分析视图的接口，说明每项处理的理由、影响、保留信息、回滚方式和后续模型不得擅改的边界。它不能替代 D1 原报告。

### D3：单一数据管道实现

| 项目 | 安排 |
|---|---|
| 调度 | 创建 1 个新 subagent，作为共享管道唯一实现所有者 |
| worker-base | `prompts/data-engineering/worker-base.md` |
| 角色 prompt | `prompts/data-engineering/data-pipeline-builder.md` |
| 可读 | 原始来源、题意/路线交接、D1 原报告和 D2 数据方案 |
| 可写 | `data/pipeline/`、`data/staging/`、`data/processed/canonical/`、`data/processed/analytical/` 及下列工程 memo |
| 禁止 | 训练模型、按分数反向清洗、静默改题意、覆盖原始数据、并行争抢同一管道 |

D3 必须同时落盘：

- `data/decisions/preprocessing-log.md`，模板 `templates/data-engineering/preprocessing-log.md`；
- `data/pipeline/implementation-memo.md`，模板 `templates/data-engineering/pipeline-implementation-memo.md`；
- `data/paper-notes/data-method-note.md`，模板 `templates/data-engineering/data-method-note.md`；
- 可复现管道代码、测试、运行参数、规范层数据和各问分析视图。

`data-method-note.md` 是工程留档，不是正式论文段落。它记录可追溯的处理事实、公式、影响和待披露限制，后续论文模块再据此扩写。

### D4：新 reviewer 独立复核

完整模式可并行创建 2 个新 subagent。Reviewer 只写 review，不能修改 D3 代码或处理后数据。

| 角色 | 创建方式 | 角色 prompt | 最低关注 | 主输出 |
|---|---|---|---|---|
| 复现与质量验证者 | 新 subagent | `prompts/data-engineering/data-repro-validator.md` | 从入口复跑、版本/参数、行数与主键守恒、转换一致性、测试覆盖和可追溯性 | `data/reviews/reproducibility-quality-review.md` |
| 题间接口审查者 | 新 subagent | `prompts/data-engineering/data-interface-reviewer.md` | 各问对象、粒度、单位、时间、共享量与可用信息是否和题意/路线交接一致 | `data/reviews/interquestion-interface-review.md` |

分别使用 `templates/data-engineering/repro-review.md` 和 `templates/data-engineering/interface-review.md`。精简模式由 1 个新的 subagent 同时持有两份 review 合同，输出 `data/reviews/combined-data-review.md`；独立性不能取消。

### D4R：原 D3 实现者集中回应与修订

| 项目 | 安排 |
|---|---|
| 调度 | 复用原 D3 数据管道实现者，不换人 |
| 角色 prompt | `prompts/data-engineering/data-builder-response.md` |
| 可读 | 自己的 D3 实现与全部 D4 review |
| 模板 | `templates/data-engineering/builder-response.md` |
| 主输出 | `data/reviews/data-builder-response.md`，以及明确标记版本的 D3 修订产物 |

实现者逐项接受、反驳或保留限制，并说明代码、数据、日志、方法留档和题间接口受到的影响。第一版和失败证据必须保留；修订后由 Leader决定是否需要定向复查，不开启无限答辩。

### D5：Leader 数据交接

| 项目 | 安排 |
|---|---|
| 执行者 | Leader，不创建 subagent |
| 输入 | 数据契约、剖析、风险报告、方案、管道版本、日志、方法留档、D4 review 与 D4R 回应 |
| 模板 | `templates/data-engineering/data-handoff.md` |
| 输出 | `data/data-handoff.md` |

交接必须说明当前数据版本和生成入口、字段字典、主键/粒度/时间/单位、共享规范层、每问分析视图、处理记录、允许/禁止使用的信息、复核结论、已知限制和局部回滚触发器。完成后数据工程停止。

## 5. 建模构建总览

D5 完成后，Leader 必须显式从数据工程切换到 M0，并改用：

```text
prompts/modeling/worker-base.md
+ 当前角色 prompt
+ templates/modeling/task-brief.md 生成的开放 brief
```

完整设计见 `Workflow/modeling-construction.md`，机械配置见 `Workflow/modeling-team.json`。固定外框与动态内核为：

```text
M0 问题编排
→ M1 规格/计算/结构三视角分析
→ M2 构建合同
→ M3 baseline 最小贯通
→ M4 观察—诊断—回应—裁决—调整—重跑
→ M5 跨问接口装配
→ M6 模型交接
```

### M0：Leader 接收与问题编排

| 项目 | 安排 |
|---|---|
| 执行者 | Leader，不创建 subagent |
| Leader prompt | `prompts/modeling/leader.md` |
| 必读 | `Workflow/modeling-construction.md`、`Workflow/modeling-team.json`、`synthesis/problem-baseline.md`、`routes/model-candidate-briefing.md`、真实 `routes/human-model-decision.md`、`routes/route-handoff.md`、`data/data-handoff.md` |
| 模板 | `templates/modeling/question-map.md` |
| 输出 | `modeling/question-map.md`、`modeling/briefs/M1/` |

Leader 逐问记录人工授权的主模型、baseline、保留备选/敏感性模型，以及答案对象、数据入口、父/消费问题、共享参数/状态/代码、开发反馈、验证保留信息、失效传播和并行顺序。缺 H1 决定时停止；M1 新候选只能触发 change request，不能自行进入合同。

### M1：三视角隔离分析

每个问题或共享构建单元默认创建 3 个新的 subagent 并行运行。三者只读冻结交接、question map、必要来源和自己的 brief，首轮互不可见。

| 角色 | 创建方式 | 角色 prompt | 模板 | 主输出 |
|---|---|---|---|---|
| 数学规格架构师 | 新 subagent | `prompts/modeling/mathematical-specification-architect.md` | `templates/modeling/formulation.md` | `modeling/specs/qN-formulation.md` |
| 计算路径规划师 | 新 subagent | `prompts/modeling/computational-path-planner.md` | `templates/modeling/computation-plan.md` | `modeling/plans/qN-computation-plan.md` |
| 结构挑战者 | 新 subagent | `prompts/modeling/structural-challenger.md` | `templates/modeling/structural-challenge.md` | `modeling/challenges/qN-structural-challenge.md` |

Leader 保存三者句柄并等待全部结束。只有分歧会改变变量、目标、约束、评价口径或题间接口时，才复用对应原角色做一次定向澄清；不建立固定答辩波次，也不按二比一投票。

### M2：Leader 构建合同

| 项目 | 安排 |
|---|---|
| 执行者 | Leader，不创建 subagent |
| 输入 | 三份 M1 原报告、冻结上游交接和 question map |
| 模板 | `templates/modeling/build-contract.md` |
| 输出 | `modeling/specs/qN-build-contract.md` |

合同必须冻结数学对象、数据/信息边界、题间接口、真实人工授权来源、baseline、人工选择的主/挑战/敏感性候选、统一结果口径、预期画像、L0/L1 预授权、L2/L3 触发器、分支/计算预算和停止线。改变模型家族、目标或核心结构必须重新进入 H1；合同只约束修改权限，不证明模型正确。

### M3：baseline 最小贯通

每问首次进入 M3 时创建 1 个新的 model builder；后续本问 M4 都复用它。

| 项目 | 安排 |
|---|---|
| worker-base | `prompts/modeling/worker-base.md` |
| 角色 prompt | `prompts/modeling/model-builder.md` |
| 可读 | 当前 build contract、允许的数据视图、M1 原报告和 brief 明列的依赖 |
| 可写 | brief 明列的 `modeling/src/`、`configs/`、`runs/`、candidate tables、interfaces 和 paper-notes |
| 禁止 | 修改上游交接/Canonical 数据、打开保留验证信息、并行争抢共享内核、执行正式验证 |

执行顺序：

1. 用 `templates/modeling/run-intent.md` 在运行前写 `modeling/runs/<run-id>/run-intent.md`；
2. 实现统一输入、baseline、标准候选结果表和题间接口；
3. 保存代码、配置、日志、求解状态、失败与机器结果；
4. 用 `templates/modeling/iteration-memo.md` 写事后观察；
5. 更新 `templates/modeling/candidate-result-index.md` 和 `templates/modeling/model-method-note.md` 对应产物。

首次结果无论普通、失败、异常糟糕或异常优秀都保留。异常优秀同样可能来自泄漏、重复、未来信息或指标实现错误。

### M4：触发式诊断与受约束调整

M4 不是固定轮数。Leader 每次根据运行事实选择以下路径。

#### M4-A：明确的低影响 L0

明显索引、维度、公式翻译、读写或日志错误，且根因没有实质竞争解释时：原 builder 记录 → Leader 确认合同不变 → 复用原 builder 修复重跑。无需为形式完整创建诊断者，旧 run 保留。

#### M4-B：高影响、多解释或异常优秀/糟糕

| 子阶段 | 调度 | 允许读取 | 隐藏/禁止 | 输出 |
|---|---|---|---|---|
| M4B.1 中性触发 brief | Leader | build contract 与原始产物路径 | 不写 Leader 根因倾向 | `modeling/briefs/M4/` |
| M4B.2 独立诊断 | 创建新 subagent，使用 `prompts/modeling/build-result-diagnostician.md` | build contract、run intent、代码、原始日志/结果、baseline、中性触发说明 | builder 事后归因/建议、Leader 倾向、其他诊断 | `templates/modeling/result-diagnosis.md` → `modeling/diagnostics/` |
| M4B.3 原实现者回应 | diagnosis 落盘后复用原 builder，使用 `prompts/modeling/model-builder-response.md` | 自己原实现、iteration memo 与 diagnosis | Leader 裁决前不得修改 | `templates/modeling/builder-response.md` → `modeling/adjustments/` |
| M4B.4 Leader 定级 | Leader | 原始证据、diagnosis、response | 不投票 | L0/L1、L2、L3、双分支或停止 |
| M4B.5 获批调整 | Leader 写卡，复用原 builder | 当前版本与获批范围 | 未授权路径、保留信息 | `templates/modeling/adjustment-card.md`、新 run/版本 |

第一次高影响诊断必须使用新 diagnostician。同一失败机制的连续复查可以复用；连续两轮仍沿用同一解释且没有区分力时，换 fresh-context diagnostician 或停止搜索。

#### M4-C：L2 模型结构变化

暂停 builder 写入，定向复用数学规格架构师和/或结构挑战者，Leader 升版 build contract，标记旧合同下失效 runs，再复用原 builder 实施。改一行目标函数也可能是 L2，判断按数学含义而非代码量。

#### M4-D：L3 上游变化

需要改变目标构造、标签/proxy、总体、Canonical 数据、可用时点、题间接口、路线或题意时，立即停止本问，用 `templates/modeling/upstream-change-request.md` 写入 `modeling/change-requests/`，回到最早受影响阶段。不得把 L3 伪装成特征工程。

#### 继续与停止

只有存在影响答卷的高价值不确定性，且有可负担、有区分力的下一动作时继续。只剩边际指标、需要打开保留信息、预算耗尽，或需要正式稳健性/敏感性/复现时，冻结候选并交给后续验证。

### M5：跨问接口装配

| 变体 | 调度 | 角色 prompt | 主责任 |
|---|---|---|---|
| Producer | 复用上游原 builder | `prompts/modeling/interface-handoff.md` | 写实际输出对象、版本、限制和失效传播 |
| Consumer | 复用下游原 builder | `prompts/modeling/interface-handoff.md` | 写实际需求和不能消费点 |
| Integrator | 需要代码时从相关原 builder 中指定唯一 owner | `prompts/modeling/interface-handoff.md` | 只实现获批的机械适配 |

使用 `templates/modeling/interface-handoff.md`，产物写 `modeling/results/interfaces/`。适配若改变对象、目标、粒度、单位、时间、标签或数学含义，返回 M2/L3，不用 glue code 掩盖。

### M6：Leader 模型交接

| 项目 | 安排 |
|---|---|
| 执行者 | Leader，不创建总结型 worker |
| 输入 | 全部 formulation、plan、challenge、contracts、run intents、iteration memos、diagnoses、responses、adjustments、代码、结果、接口和 paper-notes |
| 模板 | `templates/modeling/model-handoff.md` |
| 输出 | `modeling/model-handoff.md` |

交接必须保留逐问候选、关键调整与回滚、失败/异常结果、实际使用的开发反馈、未打开的保留信息、题间接口、失效传播、上游请求和后续验证优先攻击项。完成后建模构建停止，所有结果仍是待验证候选。

### 完整与精简模式

- 完整模式用于强题间依赖、优化/仿真/动态/时空/组合问题、实质结构分支或显著数值风险，执行 M1 三角色与触发式诊断。
- 精简模式仅限对象清楚、算法直接、规模小且无实质结构分支；可以只创建 1 个规格角色和 1 个 builder，但 baseline、run intent、调整留档、模型交接和后续验证入口不能省略。
- 精简模式一旦出现高影响触发信号，仍创建新的 diagnostician。

## 6. 独立模型验证总览

M6 完成后，Leader 必须显式切换到 V0，改用：

```text
prompts/validation/worker-base.md
+ 当前角色 prompt
+ templates/validation/task-brief.md 生成的开放 brief
```

完整设计见 `Workflow/model-validation.md`，机械配置见 `Workflow/validation-team.json`。主链为：

```text
V0 验证对象与保留信息冻结
→ V1 三视角隔离审查
→ V2 Leader 验证议程
→ V3 定向 probe
→ V4 原 owner 证据回应
→ V5 Leader 主张裁决/局部回滚/必要复验
→ V6 整体题链审查与验证交接
```

V3–V5 是触发式循环，不是固定轮数。验证按具体主张裁决，不对整个模型设虚假通过门禁。

### V0：Leader 验证冻结

| 项目 | 安排 |
|---|---|
| 执行者 | Leader，不创建 subagent |
| 必读 | `modeling/model-handoff.md`、相关 build contracts/code/config/runs/results/interfaces、`data/data-handoff.md`、D4 review、候选汇报、真实人工模型决定、题意/路线交接、官方要求 |
| 模板 | `templates/validation/validation-map.md`、`templates/validation/validation-exposure-ledger.md` |
| 输出 | `validation/scope/validation-map.md`、`validation/scope/exposure-ledger.md` |

Leader 逐问冻结答案对象、候选主张、主张—结果—模型—数据—代码—run 链、高风险假设、题间失效传播、已用开发反馈和未打开保留信息。V0 不执行新试验，不宣布候选应当通过。

### V1：三视角隔离审查

完整模式并行创建三个新 subagent。三者读相同冻结交接和自己 brief，不读 peer 报告、Leader 根因倾向或 builder 新辩护。

| 角色 | 角色 prompt | 最低责任 | 主输出模板 |
|---|---|---|---|
| 数学—实现审计者 | `prompts/validation/mathematical-implementation-auditor.md` | 题意/公式/变量/目标/约束/量纲/边界与代码、配置、求解状态对应 | `templates/validation/mathematical-implementation-review.md` |
| 实验证据审计者 | `prompts/validation/experimental-evidence-auditor.md` | 泄漏、切分、可用时点、baseline 公平性、不确定性、稳健性和主张证据负担 | `templates/validation/experimental-evidence-review.md` |
| 复现—接口审计者 | `prompts/validation/reproducibility-interface-auditor.md` | 冻结入口复跑、环境/随机性/求解器、结果表、题间消费与官方交付 | `templates/validation/reproducibility-interface-review.md` |

等全部返回后才综合。V1 可做低成本静态核对和未消耗 holdout 的复跑，但默认无 probe 工程写权。

### V2：Leader 验证议程

| 项目 | 安排 |
|---|---|
| 执行者 | Leader |
| 输入 | V1 全部原始报告、validation map、exposure ledger 和原始证据 |
| 模板 | `templates/validation/validation-docket.md` |
| 输出 | `validation/dockets/qN-validation-docket.md` |

Leader 不投票。按对答案/主张影响、虚假优秀风险、题间传播、probe 区分力、成本和 holdout 消耗排序，保留未授权项及理由。

### V3–V5：定向取证、回应与裁决

| 子阶段 | 调度 | 输入/隔离 | 输出 |
|---|---|---|---|
| V3.1 Probe intent | 复用提出问题的 auditor | docket 授权、冻结版本、可见 holdout；禁止临时改目标/指标 | `templates/validation/probe-intent.md` → `validation/probes/PROBE-ID/probe-intent.md` |
| V3.2 Probe 执行 | 同一 auditor | 只写自己 `validation/probes/PROBE-ID/`；`data/` 与 `modeling/` 只读 | raw outputs 与 `templates/validation/probe-report.md` |
| V4 原 owner 回应 | probe report 落盘后复用原 model/data builder | 可读原实现与获批验证证据；Leader 裁决前不得修改 | `prompts/validation/original-owner-response.md` + `templates/validation/original-owner-response.md` → `validation/responses/` |
| V5 主张裁决 | Leader | review、intent/report、response、exposure ledger、原始证据 | `templates/validation/claim-disposition.md`；回滚用 `templates/validation/upstream-change-request.md` |

Leader 对具体主张记录“可引用 / 有条件可引用 / 暂不可引用 / 证据反驳 / 上游失效”。需修正时回到最早责任阶段：合同内实现回 M3/M4，结构问题回 M2，数据问题回 D0–D4，路线回 L2，题意回 L1 或更早。validator 不直接修上游。

每次向 builder 暴露新验证信息后，Leader 立即更新 exposure ledger。该证据不再是未见 holdout；修正后必须使用新切片、嵌套设计、滚动回测或其他独立证据。

### V6：整体题链审查与验证交接

| 任务 | 调度 | Prompt/模板 | 输出 |
|---|---|---|---|
| 整体题链审查 | 强题间依赖时创建新 subagent；弱依赖由 Leader 依原始证据整合 | `prompts/validation/integrated-answer-auditor.md` + `templates/validation/cross-question-validation.md` | `validation/interfaces/cross-question-validation.md` |
| Claim–Evidence Map | Leader | `templates/validation/claim-evidence-map.md` | `validation/claims/claim-evidence-map.md` |
| 验证交接 | Leader | `templates/validation/validation-handoff.md` | `validation/validation-handoff.md` |

整体审查核对 producer–artifact–consumer 版本、对象、粒度、单位、时间、总体、不确定性传播和官方交付覆盖。交接授权后续可用结果和准确主张，同时保留条件、否定证据、未决争议和禁止过度表述。

### 完整与精简模式

- 完整模式用于学习、时序、优化、仿真、时空/网络、综合评价、强题间依赖、proxy/泄漏风险、异常优秀结果或高影响 holdout，执行 V1 三路和必要 V6 独立审查。
- 精简模式仅限数学对象清晰、确定性强、单问/弱依赖且无实质分支；可只创建数学—实现和复现—接口两个 auditor。
- 两种模式都不能取消 validation map、exposure ledger、独立 probe、主张裁决、回滚入口和 validation handoff。发现高影响泄漏、结构或题间风险时立即升级完整模式。

## 7. V6 后异步图表准备

完整设计见 [`Workflow/figure-preparation.md`](figure-preparation.md)，本节是 Leader 的实际调度入口。该支线只整理诊断证据、逐图数据包和论文图表建议，不绘制正式论文图，也不做视觉/审美审查。它与本仓库的 CP0–CP6 论文准备支线并行，最迟在论文框架交接前汇合。

### 7.1 入口与冻结

V6 的 `validation/validation-handoff.md` 和 `validation/claims/claim-evidence-map.md` 落盘后，若当前 run 包含后续交付，Leader 明确切换到 F0：

1. 读取验证交接、逐问授权结果、结果表、run/模型/数据/代码版本、题间接口和禁止使用的旧候选；
2. 写 `figure-prep/scope/frozen-inputs.md`，只记录路径、哈希、版本、授权范围、冻结时间和禁止事项；章节地图没有固定路径时也在此记录实际路径和哈希，缺失则标为 F3 阻塞项；
3. 每问建立一个独立 `Question Figure Curator`；跨问共享结果另建一个 shared curator，写入 `figure-prep/cross-question/shared/`；
4. 同时启动论文准备 CP0；CP1 的 chapter-map-v0 落盘前，F3 只登记依赖，不自行生成章节结构。两条支线不能互相覆盖文件。

Leader 不在 F0 预先决定每问必须画什么，也不修改上游数据/模型/验证结果。

### 7.2 F1 逐问 Curator

| 项目 | 安排 |
|---|---|
| 创建方式 | 每问/共享结果单元一个新的 subagent；不按候选图数量复制 owner |
| Prompt | `prompts/figure-preparation/question-figure-curator.md`；共享 curator 复用该 prompt |
| 读取 | F0 冻结清单、对应授权结果、必要诊断产物、题间接口和自己的 brief；不得读 peer 草稿或 Leader 倾向 |
| 写入 | 自己 `figure-prep/questions/qN/`，或 `figure-prep/cross-question/shared/`；不得写 `data/`、`modeling/`、`validation/` 或论文草稿 |
| 诊断输出 | `diagnostics/diagnostic-index.md`、源代码、诊断数据、图和观察；图只用于排查，不是论文最终图 |
| 论文候选输出 | 每个候选独立目录 `candidates/FIG-QN-XX/`，含 `data.csv`、导出脚本、`provenance.md` 和 `recommendation.md`；另写 `question-package.md` |

Curator 必须说明 claim、推荐/备选图型、视觉编码、误差/区间/样本量/阈值、论文逻辑位置、caption 骨架、限制和禁止过度解释。不强制每问有图；明确“不建议作图”也是有效结果。

导出数据必须从 V6 授权结果重建，保留精确值、主键、粒度、时间、单位、筛选、聚合、排序、缺失和可行性状态。不能为了作图静默删异常、改分母、制造标签/proxy 或提前四舍五入。需要改变数据口径时写 change request，不能在 F1 偷换。

### 7.3 F2 流式独立复核

F2 是逐问题流式例外，不等待所有 Curator 完成：某问题的 `question-package.md` 与其保留候选的数据包/导出入口一旦落盘，Leader 立即创建一个新的 `Figure Evidence Auditor`；明确“不建议作图”的 package 无需伪造候选数据包。其他问题可以继续 F1，论文 CP1–CP3 也不必等待。

本节将当前问题或共享结果单元的写入根称为 `<unit_root>`：它只能是 `figure-prep/questions/qN/` 或 `figure-prep/cross-question/shared/`。

| 项目 | 安排 |
|---|---|
| Prompt | `prompts/figure-preparation/figure-evidence-auditor.md` |
| 读取 | F0 冻结材料、该问题已落盘 package、数据包、来源结果和导出代码；不得读未授权 peer 报告或 Leader 解释 |
| 检查 | 数据能否复算；行数/主键/粒度/单位/时间一致性；派生、区间、样本量和缺失保留；图型与 claim 匹配；章节位置可用；FR Producer 能否只凭交接包作图 |
| 写入 | 只写 `<unit_root>/review.md`；不改 package 或上游 |

当前机械检查只确认文件、路径和非空可读性；哈希、版本、重建和列级一致性由 Auditor 独立复核。Auditor 必须写观察、证据、未知、影响和建议，不用脚本全绿代替语义判断。

### 7.4 F2R 原 Curator 回应

review 落盘后立即复用产生该 package 的原 Curator，使用 `prompts/figure-preparation/question-curator-response.md`：

- 默认一次集中回应；接受、反驳、缩小 claim、标记暂缓或修订数据导出；
- 旧 package、旧脚本和旧 review 永久保留，新版本说明影响和哈希；
- response 写 `<unit_root>/response.md`；
- 实质数据、模型、验证或题意问题只写 change request，交 Leader 裁决返回上游；Curator 不直接修上游。

Leader 不以票数解决 review 分歧；仍不能判断时保留分支、限制 claim、暂停候选或升级用户。

### 7.5 F3 跨问与章节位置整合

所有已启动问题的 package/review/response 完成，且 CP1 已提供 `paper-prep/structure/chapter-map-v0.md` 后，创建新的 `Figure–Chapter Integrator`，使用 `prompts/figure-preparation/figure-chapter-integrator.md`。章节地图实际路径、版本与哈希必须已登记；缺失时停在 F2R，不得自行生成章节结构。Integrator 读取全部逐问/共享 package、题间接口、已裁决 change request 和章节地图，但不绘图、不修改论文材料；整合过程只写 `figure-prep/cross-question/integration/`。

Integrator 是以下两个文件的唯一内容 owner：

- `figure-prep/figure-plan.md`：全篇 Figure ID、核心/辅助/可选/放弃项、跨问组合、结果表关系、章节位置和正文叙事顺序；
- `figure-prep/figure-preparation-handoff.md`：逐图数据包、来源/版本、claim、推荐/备选图型、必要编码/标注、caption、限制、禁止表达、诊断异常、回滚和 FR0–FR4 边界。

Integrator 不得补造尚未完成的数据，不得为了完整而保留不能支持 claim 的图。F3 产生的文件可由 Leader 要求一次补充，但内容修改仍由同一 Integrator 完成。

### 7.6 F4 Leader 汇合检查

F4 不是新的写作角色。Integrator 已写出 `figure-plan.md` 和 `figure-preparation-handoff.md` 后，Leader 只检查：

- 每个已启动问题有 package 和 review；保留图候选的单元有对应数据包，不建议作图的单元已在 package 说明理由；
- review 已由原 Curator 回应，或明确记录缺失/暂缓/保留分支；
- 高影响 change request 已裁决或标明禁止表达；
- figure plan 已与章节最小地图对齐；
- 每个 Figure ID、来源、claim、数据版本和逻辑位置能互相链接；
- handoff 已声明 FR0–FR4 不得改变的数据口径。

缺条件时，Leader 退回对应 F1/F2/F2R/F3 或上游；不代替 Integrator 修改 handoff。条件满足后，Leader 宣布图表支线汇合并停止。结果章节可以提前使用 Figure ID 占位，但上述条件未满足前不得标记定稿。

### 7.7 并发、失败与所有权

- 图表支线不设固定 subagent 数量上限；并行只允许在输入冻结、输出路径独立且有独立判断价值时发生。不得按每个候选图再复制 owner。
- F2 可在问题级流式启动；不必等同批其他 Curator。
- worker 未返回时同角色重试一次；仍失败则记录该问题缺失，其他独立问题继续。
- 数据包不可复算、claim 未获授权或诊断发现上游问题时，暂停候选并保留版本；Leader 通过 change request 返回最早受影响阶段。
- Curator 只写自己的问题/共享目录，Auditor 只写 review，F2R 只写 response/新版本；F3 Integrator 独占 figure plan/handoff；F4 Leader 只检查、回滚和宣布。
- F0–F4 不生成正式论文图、样式文件、审美评分或视觉迭代记录；FR0–FR4 只能消费最终 handoff 和显式冻结数据包。

## 7A. 正式论文绘图 FR0–FR4

完整设计见 [`Workflow/formal-figure-rendering.md`](formal-figure-rendering.md)。模块只有两类 subagent：Question Visual Producer 和 Figure Portfolio Reviewer。所有新 Agent 都必须由 Leader 显式创建为 `gpt-5.6-sol`、`reasoning_effort=high`、`fork_turns=none`；默认 Luna 不得使用，覆盖失败时停止并报告用户。

### 7A.1 FR0 冻结与 sol-high 调度

F4 handoff 和 `chapter-map-v0.md` 落盘后，Leader 写 `formal-figures/scope/frozen-inputs.md`，解析每个 Figure ID 的数据包、provenance、recommendation、claim、章节、官方版心、路径、版本和哈希。

每次新建 Producer/Reviewer 都必须把请求模型、reasoning、fork、角色、单元和 Agent 句柄追加到 `formal-figures/scope/dispatch-log.json`。因为覆盖模型不能配合 full-history fork，使用 `fork_turns=none`，完整上下文通过 prompt、brief 和文件路径提供。未显式覆盖不算完成派工。

Leader指定一个 Producer 兼任 style owner，先写 `style/visual-system.md`、`paper.mplstyle` 和 `theme.py`；这是同一角色，不新增样式 Agent。

### 7A.2 FR1 每问/共享 Visual Producer

每问创建一个新的 sol-high Producer；真实共享结果可创建一个同角色 shared Producer。不得按 Figure ID 拆 Agent。Producer 写：

- `visual-plan.md`：数据/统计、关系、模型结构、核心结果、baseline、误差/稳健性、情景/决策和题间接口覆盖；
- 每图 `chart-contract.md` 与 `data-ref.md`：claim、粒度、单位、时间、样本量、误差、比较任务、图型、轴、尺度、颜色、标注和版心；
- pilot：用极值、零/负值、长标签、缺失、稀有类别和密集区域调试，不进入 handoff；
- `render.py`、render config/memo 和使用完整冻结数据的 v1 PNG/PDF/SVG。

典型每问先考虑数据/结构、核心结果、比较/不确定性三类，必要时加情景图；典型三至四问题目的 12–20 候选、正文 8–14 张只是规划参考。没有 claim、重复表格或证据不足时放弃/转附录，不按数量凑图。缺关键数据包时写 coverage request 返回 F1/F2。

### 7A.3 FR2/FR2R 统一审图与原 Producer 修订

所有 v1 落盘后，创建一个 fresh-context sol-high Portfolio Reviewer，使用 `prompts/formal-figures/figure-portfolio-reviewer.md`，只写 `formal-figures/figure-review.md`。默认一次审全部图；确实超出上下文才按问题包拆多个同角色 Reviewer。

Reviewer 在同一报告中审：数据/单位/样本量/误差/轴域与 claim，图型与图量覆盖，字体/颜色/层级/碰撞/灰度与全篇风格，以及目标版心中的可读性。它不改图、不打综合美观分。

FR2R 复用各原 Producer，保留 v1，写 response 并生成 final PNG/PDF/SVG。默认一轮；只有数值/尺度错误、关键不可读或导出损坏允许第二次定向修复。数据或 claim 问题返回上游。

### 7A.4 FR3/FR4 真实版面关闭与交接

`full-paper-v2.md` 和 `figure-table-slots.md` 可用后，生成只读 contact sheet/in-paper preview，复用原 Reviewer 只关闭原问题，写 `figure-review-closure.md`，不再全面审稿。

Leader 随后写 `figure-coverage-map.md`、`figure-manifest.md`、`placement-and-caption-handoff.md` 和 `figure-rendering-handoff.md`。FD0 只消费 manifest 授权的 final 图，不从散乱目录挑图。

## 8. 章节材料包与竞赛论文框架 CP0–CP6

完整设计见 [`Workflow/paper-preparation.md`](paper-preparation.md)。该模块只整理可直接成文的逐问材料和段落级论文框架，不生成完整论文、正式图片、排版、参考文献检索结果或提交包。

### 8.1 CP0 输入冻结与两条支线启动

V6 完成后，若当前 run 包含后续交付，Leader 可并行启动 F0、CP0 和 REF4–REF6。CP0 读取 validation handoff/claim map、题意与路线、route evidence、data/model handoff、已有来源、工程方法文稿、官方要求和图表状态，写 `paper-prep/scope/frozen-inputs.md`。

冻结文件必须列出逐问授权结果、公式、claim、版本、禁止旧候选、国奖论文蒸馏路径和 owner。蒸馏材料只登记路径，在 CP5 blind review 落盘前禁止发送给任何论文准备角色。

### 8.2 CP1 最小章节接口

Leader 创建新的 Paper Structure Architect：

| 项目 | 安排 |
|---|---|
| Prompt | `prompts/paper-preparation/paper-structure-architect.md` |
| 读取 | 原题、官方要求、题意基线、验证交接、题间接口；禁止蒸馏、代码和工程日志 |
| 写入 | `paper-prep/structure/chapter-map-v0.md`、`narrative-spine.md`、`page-budget.md` |

chapter-map-v0 落盘后，Leader 立即把精确路径、版本和哈希补充给图表 F3 与 Citation Gap Analyst。它只定义章节目标和关系，不等待 CP2，也不预先套固定获奖论文目录。

### 8.2A REF4–REF6：正式引用补齐

V6 claim map 与 chapter-map-v0 齐备后，创建新的 Citation Gap Analyst，使用 `prompts/literature/citation-gap-analyst.md`，逐章区分外部引用需求和本队内部结果证据，形成 CIT-ID gap map。

按独立主题簇创建新的 Citation Literature Scouts，使用 `prompts/literature/citation-literature-scout.md`。Leader 预分配不重叠的 CIT-ID/REF-ID；每个 Scout 只写自己的 source notes 和 `scouts/TOPIC/references-candidate.bib`，不按单条引用创建 Agent。全部返回后 Leader 才合并共享候选 BibTeX。每条引用必须绑定具体主张和支持范围，无法核验时保留 citation-needed，不能编造。

最后创建新的 Citation Auditor，使用 `prompts/literature/citation-auditor.md`，审文献真实性、元数据、原始/二手来源、正文支持范围、重复 key 和人的意见边界。Auditor 不修改 BibTeX。Leader 根据 review 写 `literature/references.bib`、claim-to-citation map 与 `references-handoff.md`。

REF6 与 CP2/图表准备可并行，但 `references-handoff.md` 必须在 CP4/CP6 和 PW0 前落盘；推翻路线或验证主张的新文献必须返回上游，不能只改引用。

### 8.3 CP2/CP3/CP3R 逐问流式材料链

每个纳入问题创建一个新的 Question Chapter Curator，使用 `prompts/paper-preparation/question-chapter-curator.md`，只写 `paper-prep/questions/qN/chapter-material-v1.md`。材料应包含一句话回答、模型选择理由、公式与变量、求解顺序、授权结果解释、题间接口、表图位置、正文/附录划分、来源和禁止表达。

某问 v1 落盘后立即创建新的 Chapter Evidence Auditor，使用 `prompts/paper-preparation/chapter-evidence-auditor.md`，只写本问 `evidence-review.md`。它审数字、公式、单位、claim、来源和题间消费，不审竞赛文风，也不修改材料。

Review 完成后复用原 Curator，使用 `prompts/paper-preparation/chapter-curator-response.md`，保留 v1，写 `evidence-response.md` 和 `chapter-material-v2.md`。事实问题只能由原 Curator修订；上游证据问题写 change request。

### 8.4 CP4 全文框架整合

全部纳入问题完成 CP3R 且 REF6 references-handoff 已落盘后，创建新的 Paper Framework Integrator，使用 `prompts/paper-preparation/paper-framework-integrator.md`。它统一章节、符号、单位、精度、题间衔接、引用、表图和篇幅，产出：

- `paper-prep/structure/chapter-map-v1.md`；
- `paper-prep/shared/notation-registry.md`；
- `paper-prep/shared/claim-to-section-map.md`；
- `paper-prep/shared/table-and-figure-plan.md`；
- `paper-prep/integration/paper-framework-v1.md`。

Integrator 不能修改逐问数字、公式或 claim；冲突必须返回 owner。图表 handoff 已完成时直接纳入，未完成时保留带来源的 Figure ID 占位。

### 8.5 CP5 双遍竞赛论文独立审读

创建新的 Competition Manuscript Reviewer，使用 `prompts/paper-preparation/competition-manuscript-reviewer.md`。

第一遍 brief 只给原题、官方要求、chapter-map-v1、paper-framework-v1、逐问最终材料和表图占位；明确禁止代码、工程日志、Leader 辩护、Evidence review 和国奖蒸馏。Reviewer 先写并冻结 `competition-review-blind.md`，专查答案是否醒目、论证是否闭合、结果是否解释、篇幅是否合理，以及 run/debug/路径/调参流水账等工程文风。

只有 blind memo 确认落盘后，Leader 才向同一 Reviewer 发送第二轮 task，增加 CP0 登记的国奖论文蒸馏路径，写 `competition-review-pattern-sweep.md`。第二遍只比较结构和表达模式，不照搬目录、不引入其他题模型/结论、不猜评分权重。

### 8.6 CP5R/CP6 修订与交接

Leader 按 owner 分派一次修订：事实问题复用原 Question Curator，结构/篇幅/重复问题复用原 Framework Integrator，上游证据问题返回相应模块。Integrator 使用 `prompts/paper-preparation/paper-framework-response.md` 写 `framework-response.md` 和 `paper-framework-v2.md`。

原 Competition Reviewer 只做一次关闭检查，写 `competition-review-closure.md`，不得扩展为新一轮全面审稿。figure handoff、references handoff 和 `literature/references.bib` 落盘后，原 Integrator 把最终 Figure ID、引用位置和限制纳入 v2，再独自写 `paper-prep/paper-framework-handoff.md`；Leader 只核对并宣布停止。

### 8.7 并发、所有权和停止边界

- CP2/CP3 按问题流式并行，不按段落拆 Agent；CP4 以后全篇串行。
- Evidence Auditor 与 Competition Reviewer 必须是两个独立新 Agent。
- CP5R 默认一轮定向修订和一次关闭检查，不无限迭代。
- 旧 material、review、response 和 framework 不覆盖。
- `paper-framework-handoff.md` 完成后停止；不得自动生成完整论文、正式图片、排版或提交包。

## 9. 正式论文写作与全文组装 PW0–PW7

完整设计见 [`Workflow/paper-writing.md`](paper-writing.md)。本模块以 Markdown 为唯一正文源；Leader 是唯一全文作者，逐问 subagent 只写 section，Reviewer 永久只写修改单。

### 9.1 PW0/PW1 冻结与写作计划

`paper-framework-handoff.md`、`figure-preparation-handoff.md`、references handoff、claim-to-citation map 和 `literature/references.bib` 落盘后，Leader 写 `paper-writing/scope/frozen-inputs.md`，冻结论文框架、逐问材料、validation claim、Figure/Table、引用键、官方要求和禁用旧版本。

Leader 随后写 `writing-plan.md`、`section-contracts.md`、`prose-boundary.md` 和 `figure-table-slots.md`。其中 prose boundary 区分必要技术术语与应移出正文的 run/config/debug/pipeline/路径/调参信息，不作为机械禁词表。

### 9.2 PW2 逐问正式章节

每问创建一个新的 Question Manuscript Writer，使用 `prompts/paper-writing/question-manuscript-writer.md`，只写 `sections/qN/section-v1.md`。正文必须是连续竞赛论文，不是材料索引或工程日志；不得写摘要、总结、公共章节或全文主稿。

### 9.3 PW3/PW4/PW4R 事实稳定

所有 section-v1 完成后，Leader 写公共章节、摘要、关键词、结论、优缺点和推广，组装 `manuscript/full-paper-v1.md`。

创建新的 Full-Paper Fact Auditor，使用 `prompts/paper-writing/full-paper-fact-auditor.md`，只写 `reviews/fact-consistency-review.md`。它审数字、公式、单位、claim、摘要/正文/结论、表图和题间接口，不审文风。

局部事实问题复用原 Question Writer，使用 `prompts/paper-writing/question-manuscript-response.md` 写 section response/v2；Leader 写 `fact-response.md` 并组装 `full-paper-v2.md`。v1 永久保留。

### 9.4 PW5 三路独立语言审查

冻结同一份 `full-paper-v2.md`，并行创建三个互相隔离的新 Reviewer：

- `prompts/paper-writing/competition-expression-reviewer.md`：答案可见性、方法动机、结果解释、摘要信息和竞赛重点；
- `prompts/paper-writing/full-paper-coherence-reviewer.md`：定义/公式/结果顺序、章节题间逻辑、术语、摘要正文结论和表图关系；
- `prompts/paper-writing/ai-prose-auditor.md`：关联词堆积、模板句、空洞拔高、无必要比喻、口水话、长句、工程词和错误术语替换。

三者不能读取 peer review 或 Leader 辩护，只写各自 review。AI Prose Auditor 不判断作者身份、不给 AI 分数、不调用检测器、不自动改文，也不能通过口语化、错别字或降低专业性制造“人味”。

### 9.5 PW5R/PW6/PW7 修订、关闭与交接

三份 review 全部落盘后，Leader 写 language-review-response；逐问专业事实退原作者，全篇结构、过渡、摘要结论和统一语气由 Leader 修改，形成 `full-paper-v3.md`。冲突按事实准确、答题直接、表达简洁裁决。

PW6 复用原四个 Reviewer，各自只检查原问题，写 `reviews/closure/` 四份 memo；不新增全面审稿轮次。事实错误必须修，答题或全文矛盾局部重开，纯风格偏好一轮后停止。

PW7 由 Leader 独写 `manuscript/final-paper.md` 与 `formal-paper-handoff.md`。Handoff 完成后停止，不生成 Word/LaTeX、正式图片、引用检索、排版或提交包。

## 10. 最终排版、终审与人工交付 FD0–FD7

完整设计见 [`Workflow/final-delivery.md`](final-delivery.md)。本模块不重写论文内容；它把冻结 Markdown、FR4 manifest 授权正式图、引用、结果数据和实际运行脚本装配为供人最终处理的候选包。

### 10.1 FD0 输入冻结

Leader 读取 `Workflow/final-delivery-team.json` 和 `prompts/final-delivery/leader.md`，写 `final-delivery/scope/frozen-inputs.md`。必须列出题意基线、路线、route evidence、数据/模型/验证/图表/论文各阶段 handoff，以及正文、figure-rendering handoff/manifest、references handoff/references.bib、结果/公式/claim、实际执行脚本、官方要求、精确版本/哈希和禁止旧候选。缺项可以记录，但不得伪装候选包完整；不得从 manifest 外挑图。

### 10.2 FD1 支撑材料

创建新的 Supporting Material Curator，使用 `prompts/final-delivery/supporting-material-curator.md`。它只写 `final-delivery/supporting-materials/`：

- `results/` 与 `result-data-manifest.md` 保存论文实际使用的精确结果；
- `source-code-manifest.md` 和 `execution-order.md` 记录脚本—run—结果关系；
- `source-code.md` 必须完整粘贴实际生成最终结果的运行脚本，不能只给路径或链接；
- `supporting-materials.md` 供后续排版为正文后附或独立附件。

废弃候选、debug 临时脚本、缓存、第三方库源码和密钥不得混入；发现敏感内容只报告，不静默改写。

### 10.3 FD2/FD3 候选组装、机械预检与冻结

创建新的 Submission Typesetter，使用 `prompts/final-delivery/submission-typesetter.md`，只写 `source/`、`candidate/`、`typesetting-memo.md` 和 `preflight-report.md`。它可以修字体、分页、公式渲染、图表/引用编号、交叉引用、乱码和截断，但不得润色正文、删减内容或改变数学事实。

FD3 只复用原 Typesetter 修纯机械问题。Leader 随后写 `scope/candidate-snapshot.md`，记录候选和支撑材料的精确哈希。从快照落盘起，正文、候选文件、支撑材料和全部上游永久只读。

### 10.4 FD4 五路独立终审

并行创建五个互相隔离的新 Reviewer，读取同一 candidate snapshot，不读 peer review 或 Leader 辩护：

- `prompts/final-delivery/layout-compliance-auditor.md`：页数、模板、匿名、公式图表、引用、答卷、附件、命名和可见版面问题；
- `prompts/final-delivery/answer-relevance-reviewer.md`：逐问是否扣题、答案是否醒目、方法—结果—解释和摘要正文结论是否闭合；
- `prompts/final-delivery/prose-engineering-style-auditor.md`：AI 套话、机械关联词、工程报告风、口水话、无必要比喻、模糊结论和开发流水账；
- `prompts/final-delivery/delivery-evidence-auditor.md`：正文—图表—精确结果—完整脚本—run—引用是否使用同一授权版本。
- `prompts/final-delivery/end-to-end-consistency-auditor.md`：从候选稿反查题意、路线、数据、模型、验证、图表和论文各阶段 handoff，定位跨阶段漂移、接口断裂、旧候选混入和问题未传播；必须使用 fresh context。

五者各写 `final-delivery/reviews/` 下唯一报告，不给 AI 分数，不修改候选，不写 response/closure。前四者按本角色白名单读取；第五个额外读取 FD0 精确冻结的全链路 handoff，但同样不能读取 peer review。

### 10.5 FD5–FD7 人工问题包与停止

五份 review 全部落盘后，Leader 只写：

- `human-review/issue-index.md`：保留原 review，按必须处理、强烈建议、可选润色建立人工索引；
- `human-review/human-finalization-guide.md`：可改范围、事实锁定和修改后复查项；
- `submission-checklist.md`：官方文件、匿名、页数、附件、命名和人工投稿动作；
- `final-delivery-handoff.md`：候选、支撑材料、审查、未决项和文件哈希。

FD4 后不创建 Agent 修订版。FD7 状态必须为 `AWAITING_HUMAN_FINALIZATION`；人完成微调和实际投稿。

## 11. 等待、失败与局部重开

- W/D/M/V 同步波在本波所有任务返回、失败或取消前，Leader 不进入综合阶段；图表 F2、正式绘图 FR1、论文 CP3、PW2 和 REF1/REF5 Scout 是独立单元并行例外；FR2 默认一个 Reviewer 审全篇图包；PW5 三个 Reviewer 必须全部结束后再综合；FD4 五个 Reviewer 必须全部结束后才能建立人工问题索引。
- subagent 未返回时，同角色重试一次；仍失败则记录缺失，不由 Leader 冒充独立意见。
- memo 偏离角色时，向原 subagent 发一次补充任务，写追加 memo，不覆盖原文。
- 出现字段语义、目标可构造性、总体、粒度、单位、时间或题间接口被推翻时，回到最早受影响阶段。
- 新证据只触发局部重开；旧 memo、旧代码和旧数据版本保留。
- 高影响、不可判且会造成不可逆路线差异的争议交给用户。

机械脚本只做辅助：

```bash
python3 scripts/init_run.py RUN_DIR --title "题目名称" --source /path/to/problem.pdf
python3 scripts/build_prompt.py --role literal-contract --task-brief RUN_DIR/briefs/W1-literal.md
python3 scripts/build_prompt.py --literature-role route_literature_scout --task-brief RUN_DIR/literature/route-alignment/search-briefs/route-a.md
python3 scripts/build_prompt.py --data-role data_profiler --task-brief RUN_DIR/data/briefs/D1-profiler.md
python3 scripts/build_prompt.py --model-role model_builder --task-brief RUN_DIR/modeling/briefs/M3/q1-builder.md
python3 scripts/build_prompt.py --validation-role experimental_evidence_auditor --task-brief RUN_DIR/validation/briefs/V1/q1-evidence.md
python3 scripts/build_prompt.py --paper-prep-role question_chapter_curator --task-brief RUN_DIR/paper-prep/briefs/CP2-q1.md
python3 scripts/build_prompt.py --paper-writing-role question_manuscript_writer --task-brief RUN_DIR/paper-writing/briefs/PW2-q1.md
python3 scripts/build_prompt.py --formal-figure-role question_visual_producer --task-brief RUN_DIR/formal-figures/briefs/FR1-q1.md
python3 scripts/build_prompt.py --final-delivery-role supporting_material_curator --task-brief RUN_DIR/final-delivery/briefs/FD1-support.md
python3 scripts/check_workspace.py RUN_DIR --stage data --json
python3 scripts/check_workspace.py RUN_DIR --stage paper-prep --json
python3 scripts/check_workspace.py RUN_DIR --stage paper-writing --json
python3 scripts/check_workspace.py RUN_DIR --stage formal-figures --json
python3 scripts/check_workspace.py RUN_DIR --stage final-delivery --json
python3 scripts/check_workspace.py RUN_DIR --stage literature --json
```

这些脚本不创建或调度 subagent，不解析 Markdown 语义，也不证明题意、模型、图形准确/美观、竞赛表达或 AI 文风正确。formal-figures checker 只验证 dispatch log 请求了 sol-high，不能证明运行平台实际提供了该模型；Leader 仍需保存真实创建结果。当前没有 `check_workspace.py --stage validation`。

## 12. 运行目录与最终停止边界

```text
run/
├── inputs/
├── briefs/
├── submissions/{W1,W2,W3R}/
├── reviews/{W3,W4}/
├── synthesis/
├── routes/
│   ├── responses/
│   ├── change-requests/
│   ├── route-a.md
│   ├── route-b.md
│   ├── route-review.md
│   ├── model-candidate-briefing.md
│   ├── human-model-decision.md
│   └── route-handoff.md
├── literature/
│   ├── scope/
│   ├── route-alignment/{search-briefs,route-a,route-b,sources,human-consultation}/
│   ├── citation-preparation/{search-briefs,scouts,sources}/
│   └── references.bib
├── data/
│   ├── briefs/
│   ├── contracts/
│   ├── profiling/
│   ├── decisions/
│   ├── staging/
│   ├── pipeline/{src,tests}/
│   ├── processed/{canonical,analytical}/
│   ├── reviews/
│   ├── paper-notes/
│   └── data-handoff.md
├── modeling/
│   ├── briefs/{M1,M3,M4,M5}/
│   ├── specs/
│   ├── plans/
│   ├── challenges/
│   ├── src/
│   ├── configs/
│   ├── runs/
│   ├── diagnostics/
│   ├── adjustments/
│   ├── results/{candidate-tables,interfaces}/
│   ├── paper-notes/
│   ├── change-requests/
│   └── model-handoff.md
├── validation/
│   ├── briefs/{V1,V3,V4,V6}/
│   ├── scope/
│   ├── reviews/
│   ├── dockets/
│   ├── probes/
│   ├── responses/
│   ├── decisions/
│   ├── interfaces/
│   ├── claims/
│   ├── change-requests/
│   └── validation-handoff.md
├── figure-prep/
│   ├── scope/frozen-inputs.md
│   ├── questions/qN/
│   ├── cross-question/{shared,integration}/
│   ├── change-requests/
│   ├── figure-plan.md
│   └── figure-preparation-handoff.md
├── formal-figures/
│   ├── scope/{frozen-inputs.md,dispatch-log.json}
│   ├── style/{visual-system.md,paper.mplstyle,theme.py}
│   ├── questions/qN/{visual-plan.md,FIG-ID/}
│   ├── shared/UNIT-ID/
│   ├── previews/
│   ├── change-requests/
│   ├── figure-review.md
│   ├── figure-review-closure.md
│   ├── figure-coverage-map.md
│   ├── figure-manifest.md
│   ├── placement-and-caption-handoff.md
│   └── figure-rendering-handoff.md
├── paper-prep/
│   ├── scope/frozen-inputs.md
│   ├── structure/{chapter-map-v0.md,chapter-map-v1.md,narrative-spine.md,page-budget.md}
│   ├── questions/qN/
│   ├── shared/
│   ├── integration/
│   └── paper-framework-handoff.md
├── paper-writing/
│   ├── scope/frozen-inputs.md
│   ├── plan/{writing-plan.md,section-contracts.md,prose-boundary.md,figure-table-slots.md}
│   ├── sections/qN/{section-v1.md,section-fact-response.md,section-v2.md}
│   ├── manuscript/{full-paper-v1.md,full-paper-v2.md,full-paper-v3.md,final-paper.md}
│   ├── reviews/{fact-consistency-review.md,competition-expression-review.md,full-paper-coherence-review.md,ai-prose-review.md,closure/}
│   ├── responses/{fact-response.md,language-review-response.md}
│   ├── change-requests/
│   └── formal-paper-handoff.md
└── final-delivery/
    ├── scope/{frozen-inputs.md,candidate-snapshot.md}
    ├── source/{submission-source.md,supporting-materials.md}
    ├── supporting-materials/{results/,result-data-manifest.md,source-code-manifest.md,execution-order.md,source-code.md,supporting-materials.md}
    ├── candidate/{paper.pdf,paper.docx-or-tex,supporting-materials.pdf}
    ├── preflight-report.md
    ├── typesetting-memo.md
    ├── reviews/{layout-and-compliance-review.md,answer-relevance-review.md,prose-and-engineering-style-review.md,delivery-evidence-review.md,end-to-end-consistency-review.md}
    ├── human-review/{issue-index.md,human-finalization-guide.md}
    ├── submission-checklist.md
    └── final-delivery-handoff.md
```

目录表示所有权与追溯边界，不是固定语义 schema。报告使用开放 Markdown；JSON 只保存配置、状态、路径、哈希、版本和运行参数。

验证后可并行完成图表、论文和 REF4–REF6 引用准备；F4 后 FR0–FR2 与 CP/PW 并行，FR3 等待事实稳定正文。figure-prep、paper framework、references handoff 和 references.bib 齐备后启动 PW0–PW7；FR4 rendering handoff、已审引用、最终结果/代码和官方要求齐备后显式启动 FD0–FD7，停止于 `final-delivery/final-delivery-handoff.md`。终审后 Leader 不得自动修改或投稿。
