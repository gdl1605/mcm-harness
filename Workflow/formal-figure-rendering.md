# 正式论文绘图工作流

> 状态：已实现。本文定义 FR0–FR4。模块消费 F4 已授权的逐图数据包，显式调用 `$visualize-data → $ssci-plots → $nature-figure`，按用户选定的 `cassatt2_quiet_journal_v1` 视觉语言生成可复现且经过两轮成图检查的正式论文图，并在 `formal-figures/figure-rendering-handoff.md` 停止。

## 1. 入口、目标与模型要求

入口至少包括：

- `figure-prep/figure-preparation-handoff.md`、`figure-plan.md` 和逐图数据包；
- `validation/validation-handoff.md` 与 claim-evidence map；
- `paper-prep/structure/chapter-map-v0.md`，后续补充 v1 和 `paper-writing/plan/figure-table-slots.md`；
- 官方版心、页面、图片格式、语言和清晰度要求。
- `Workflow/nature-figure-skill.lock.json`、`Workflow/ssci-plots-skill.lock.json`、`Workflow/formal-figure-style-profile.cassatt2.json`，以及当前项目可发现的对应 skills。

正式绘图可以与 CP4–CP6、PW0–PW4 并行；PW 使用稳定 Figure ID 占位。FR3 最晚读取事实稳定的 `paper-writing/manuscript/full-paper-v2.md` 做真实版面检查，FR4 handoff 必须在 FD0 前完成。

本模块所有新 subagent 都必须由 Leader 显式指定：

```text
model = gpt-5.6-sol
reasoning_effort = high
fork_turns = none
```

用户口径 `gpt5.6sol-high` 对应上述 canonical 配置。默认 Luna 不得用于正式图 Producer 或 Reviewer。因为模型覆盖与 full-history fork 不能同时使用，Leader 必须用 `fork_turns="none"` 创建 Agent，并在 task brief 中提供完整文件路径和边界。若指定模型或 high reasoning 不可用，停止该任务并报告用户；不得静默降级。

正式图 Producer 和 Reviewer 还必须显式调用 `$visualize-data`、`$ssci-plots`、`$nature-figure`，并在 brief 中预先选择 `backend=python` 与 `visual_profile=cassatt2_quiet_journal_v1`。三者分别负责信息层级/图型合同、Cassatt2 样式实现、Python 导出与最终版面 QA。当前 harness 的重建合同是 `render.py + frozen data`，因此不让 skill 在派工后再次询问 Python/R，也不允许转用 R 或普通 Matplotlib 静默替代。Leader 在 FR0 校验两个项目级 `SKILL.md` 哈希与各自 lock 一致，并确认 `$visualize-data` 可发现；任一缺失或不一致时停止并报告。

## 2. 精简 Team

只有两类 subagent：

- **Question Visual Producer**：每问一个，负责本问图量规划、科学约束、`$visualize-data` 图型/阅读路径、`$ssci-plots` Cassatt2 成图、`$nature-figure` 导出/QA、实际看图、自审迭代和独立 review 后修订。同一 prompt 也用于真实跨问共享图。不得按一图一个 Agent 拆分。
- **Figure Portfolio Reviewer**：默认只创建一个 fresh-context Agent，按同一 skill chain 检查全部 v2 的数据准确性、视觉效果、Cassatt2 一致性、图型选择、可读性和论文真实版面；复用一次做关闭检查。只有总图量确实超过单个上下文承载时，才按问题包拆成多个同角色 Reviewer，不新增角色种类。

主 Leader 负责冻结、指定 style owner、汇总图量覆盖、派发 review、处理 change request、写 manifest 和最终 handoff。Leader 不画图、不冒充 Reviewer。

## 3. 图量覆盖，不按数量凑图

每个 Producer 在 `visual-plan.md` 中检查以下适用责任：

- 数据概况与统计分布；
- 时间、空间、类别和变量关系；
- 模型结构或题间接口；
- baseline 与主模型比较；
- 核心结果；
- 误差、残差、敏感性、稳健性和不确定性；
- 情景、优化、决策与跨问总结。

典型问题先考虑“1 张数据/结构图 + 1 张核心结果图 + 1 张比较/不确定性图 + 必要时 1 张情景图”。典型三至四问题目的规划参考为 12–20 个候选、正文 8–14 张、其余附录或放弃；这不是语义门禁。每张图必须服务一个明确问题或 claim，精确查值更合适时明确以表代图。

若 F4 包不足以覆盖关键统计分析、主结果或稳健性证据，Producer 只写 `formal-figures/change-requests/coverage-request.md`。Leader 局部重开 F1/F2 获取新数据包和 Figure ID；Producer 不自行制造数据或 claim。

## 4. FR0：Leader 冻结、skill preflight 与派工

Leader 写 `formal-figures/scope/frozen-inputs.md`，逐项记录允许读取的 Figure ID、数据包、provenance、recommendation、claim、章节位置、官方版心和文件哈希。不得让 Producer 搜索 modeling/validation 目录挑结果。

Leader 读取两个 skill lock 和 `Workflow/formal-figure-style-profile.cassatt2.json`，确认 `.agents/skills/ssci-plots/SKILL.md`、`.agents/skills/nature-figure/SKILL.md` 哈希一致，并确认 `$visualize-data` 可发现。然后在每次创建正式图 subagent 时显式传入 `gpt-5.6-sol`、`high` 和 `fork_turns="none"`，并在 `formal-figures/scope/dispatch-log.json` 保存 Agent 句柄、角色、单元、模型请求、`required_skills=[visualize-data,ssci-plots,nature-figure]`、对应三个 invocation、`backend=python`、`visual_profile=cassatt2_quiet_journal_v1`、`palette=metbrewer_cassatt2` 和两个 lock 哈希。该 JSON 仅是机械调度元数据，不承载视觉判断。未显式覆盖、skill/profile preflight 失败均视为未派工。

Leader 指定一个 Question Visual Producer 兼任 style owner。Cassatt2 palette、白底、低装饰、图外总标题/长注释和非颜色冗余编码从 profile 起即固定；图型、面板数量和画布布局仍由证据决定，不在首稿前写死。各 Producer 先生成完整数据 v1；全部 v1 可见后，style owner 才从真实成图提炼 `formal-figures/style/visual-system.md`、`paper.mplstyle` 和必要 `theme.py`，记录 Cassatt2 palette API/角色映射与例外，不复制或手改 HEX。

## 5. FR1：逐问 Visual Producer 与第一轮视觉迭代

每问创建一个新的 sol-high Producer，写自己的 `formal-figures/questions/qN/`；真实共享单元使用同一 prompt 写 `formal-figures/shared/UNIT-ID/`。

Producer 先写 `visual-plan.md`，说明覆盖责任、正文/附录优先级、缺图和以表代图理由。每个 Figure ID 写 `chart-contract.md`，首稿前只冻结分析问题、claim、数据粒度/单位/时间/样本量、误差、读者比较任务、必须保留的限制和禁止误导项。图型、画布比例、面板大小、图例位置和正文位置在 v1 前均为开放视觉变量；可以记录候选方向，但不得写成不可调整的合同。

Producer 在 task 开头显式写 `Using $visualize-data → $ssci-plots → $nature-figure; backend=python; visual_profile=cassatt2_quiet_journal_v1`。先由 `$visualize-data` 冻结分析问题、阅读路径、图型和色彩语义，再由 `$ssci-plots` 调用 `get_palette(..., 'metbrewer_cassatt2')` 与匹配的 chart-family/multi-panel helper，最后由 `$nature-figure` 生成/导出完整数据 v1 并做目标宽度 QA。不得把 profile 误解为固定模板：只有恰好四个同类面板构成一个连贯比较且在目标宽度可读时才优先安静 2×2；否则允许纵向、横向或非对称布局。stress pilot 只验证代码边界，不替代完整数据视觉选型，也不得进入 handoff。

正式 v1 必须使用完整冻结数据，写：

```text
FIG-ID/
├── data-ref.md
├── chart-contract.md
├── render.py
├── render-config.md
├── render-memo.md
├── pilots/
├── v1/{figure.png,figure.pdf,figure.svg}
├── iteration-log.md
└── v2/{figure.png,figure.pdf,figure.svg}
```

生成 v1 后，Producer 必须实际打开 PNG、PDF 预览和目标正文宽度预览，完成第一轮视觉诊断。`iteration-log.md` 的 Round 1 至少检查：是否仍像默认库输出、核心信息是否不突出、画面是否难看或松散、标签/图例/注释是否重叠、元素是否裁切、长宽比是否被压缩、缩到正文宽度后是否不可读、Cassatt2 是否漂移或被硬编码替代、颜色与留白是否失衡、面板是否过密/同权、图例是否重复已有直接标签、图内是否混入总标题/长 caption、是否出现未授权派生 claim。Producer 记录证据和修改理由，再结合共享 visual system 生成 v2。第一轮不得改变数据、统计语义或 claim。

绘图代码只做已声明的视觉映射和必要格式化。语义筛选、聚合、归一化、平滑或插值必须已经在授权包中存在，或明确写入 change request。诊断图只能作为线索，正式图必须从授权数据重新绘制。

## 6. FR2/FR2R：第二轮统一审查与原 Producer 修订

全部 v2 完成后，Leader 创建一个新的 sol-high、fresh-context Figure Portfolio Reviewer。Reviewer 读取同一冻结 portfolio、v1→v2 的可定位变化和目标宽度预览，不读 Producer 辩护，只写 `formal-figures/figure-review.md`。

一份 review 同时覆盖：

1. **准确性**：数据包、筛选、聚合、单位、时间、样本量、误差、图中数字、零点、对数/截断、平滑和 claim；
2. **信息设计**：图型是否匹配比较任务，统计图、主结果和稳健性图是否缺失或重复；
3. **视觉质量**：成图是否精致而非默认库风格，核心视觉层级、留白、比例、Cassatt2 palette/角色映射、直接标签、图外 caption、图例经济和面板组合是否成立；2×2 是否由数据结构支持而非模板强套；
4. **渲染缺陷**：重叠、裁切、挤压、失真、压缩、字号过小、颜色难辨和导出漂移；
5. **正文环境**：目标宽度下是否清楚，Figure ID、caption 方向和章节位置是否合理。

Reviewer 不给综合美观分，不直接改图。每项写 Figure ID、证据、影响、建议动作和不得改变的数据含义。

FR2R 复用各原 Producer，把 reviewer 发现的问题写入 `iteration-log.md` Round 2 和 `response.md`，保留 v1/v2 并生成 `final/` 的 PNG/PDF/SVG。这是第二轮视觉迭代，必须处理已证实的不好看、层级弱、重叠、裁切、压缩或正文不可读问题。只有数值/尺度错误、关键不可读或导出损坏允许在 Round 2 内做一次定向复渲染；新审美方向不得开启第三轮全面改造。

## 7. FR3：真实正文检查与关闭

事实稳定的 `full-paper-v2.md` 和 `figure-table-slots.md` 可用后，Leader 生成只读 `contact-sheet.pdf` 和 `in-paper-preview.pdf`。后者必须把 final 图按预计实际嵌入宽度、原始长宽比和相邻 caption 放进 A4/官方页面，而不是只查看原生单图。复用原 Figure Portfolio Reviewer，只检查原问题是否处理、最终图是否在真实版心中可读、是否出现新重叠、裁切、压缩、错位或全篇风格漂移，写 `figure-review-closure.md`；不开展新一轮全面审稿。

准确性问题必须修复或撤图；高影响数据/claim 问题返回 F/V/M/D；纯审美分歧保留给 Leader/人，不无限迭代。

## 8. FR4：正式图交接

Leader 写：

- `figure-coverage-map.md`：逐问覆盖、正文/附录/放弃项；
- `figure-manifest.md`：Figure ID、最终 PNG/PDF/SVG、render.py、数据包、哈希、claim 和版本；
- `placement-and-caption-handoff.md`：论文位置、尺寸、caption 骨架和禁止表达；
- `figure-rendering-handoff.md`：输入、review/closure、未决请求和 FD0 不得改变的图形口径。

完成后停止。FD0 只能消费 manifest 授权的最终图片，不能从散乱目录挑图。

manifest 还必须记录每张图的最终物理宽高、长宽比、FR3 通过的实际嵌入宽度和允许的最小可读宽度。FD2/FD3 若改变宽度、长宽比或采用会压缩图内文字的转换，原 FR3 视觉关闭失效，必须在候选冻结前退回 FR3 重新渲染检查。

## 9. 图形准确性与视觉纪律

- 绝对量柱状图默认从零开始；非零截断、对数轴、标准化、平滑和插值必须显式标注；
- 同类面板保持相同单位、尺度、时间和排序；保留误差、样本量、分母、缺失和可行性状态；
- 不混合总体、均值和明细粒度，不删除异常值来美化，不用 3D 柱状图，双 Y 轴默认不用；
- 全文使用一套中文字体和数值字体，白/近白背景、深灰文字；固定 `metbrewer_cassatt2` palette 并通过 `$ssci-plots` API 取色，不硬编码 HEX；主模型/基线等稳定语义跨图保持同一角色映射，并辅以标记/线型/开闭填充；
- 总标题、Figure number 和长 Note/caption 留在论文或 caption handoff，不嵌入图体；面板内只保留短中性标题、必要单位/样本量/统计注释；不重复同时使用行标签和等价图例；
- Cassatt2 是视觉语言而非固定布局。四个同类面板可优先安静 2×2；证据层级、标签长度、尺度或目标宽度不适合时必须改用更合适的纵向、横向或非对称组合；
- 不使用彩虹色图或同亮度红绿组合，不只靠颜色区分；同时使用线型、标记、填充、直接标签或分面；
- 标题说明画了什么，副标题补单位、时间、样本量和条件；优先直接标签，避免冗余图例；
- 最终图必须由 `render.py + frozen data` 重建，并同时交付矢量 PDF/SVG 与 PNG 预览。

## 10. 运行目录

```text
formal-figures/
├── briefs/
├── scope/{frozen-inputs.md,dispatch-log.json}
├── style/{visual-system.md,paper.mplstyle,theme.py}  # 记录 profile 适配与 palette API，不复制 HEX
├── questions/qN/{visual-plan.md,FIG-ID/}
├── shared/UNIT-ID/
├── previews/{contact-sheet.pdf,in-paper-preview.pdf}
├── change-requests/
├── figure-review.md
├── figure-review-closure.md
├── figure-coverage-map.md
├── figure-manifest.md
├── placement-and-caption-handoff.md
└── figure-rendering-handoff.md
```

语义交接使用开放 Markdown。JSON 只记录团队、模型请求、路径、哈希、版本和状态。机械 checker 不判断数据语义或审美，也不能证明实际 subagent 模型身份；Leader 必须在调度记录中保存显式 sol-high 请求。
