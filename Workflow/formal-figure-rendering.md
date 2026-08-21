# 正式论文绘图工作流

> 状态：已实现。本文定义 FR0–FR4。模块消费 F4 已授权的逐图数据包，生成可复现、经过独立审查的正式论文图，并在 `formal-figures/figure-rendering-handoff.md` 停止。

## 1. 入口、目标与模型要求

入口至少包括：

- `figure-prep/figure-preparation-handoff.md`、`figure-plan.md` 和逐图数据包；
- `validation/validation-handoff.md` 与 claim-evidence map；
- `paper-prep/structure/chapter-map-v0.md`，后续补充 v1 和 `paper-writing/plan/figure-table-slots.md`；
- 官方版心、页面、图片格式、语言和清晰度要求。

正式绘图可以与 CP4–CP6、PW0–PW4 并行；PW 使用稳定 Figure ID 占位。FR3 最晚读取事实稳定的 `paper-writing/manuscript/full-paper-v2.md` 做真实版面检查，FR4 handoff 必须在 FD0 前完成。

本模块所有新 subagent 都必须由 Leader 显式指定：

```text
model = gpt-5.6-sol
reasoning_effort = high
fork_turns = none
```

用户口径 `gpt5.6sol-high` 对应上述 canonical 配置。默认 Luna 不得用于正式图 Producer 或 Reviewer。因为模型覆盖与 full-history fork 不能同时使用，Leader 必须用 `fork_turns="none"` 创建 Agent，并在 task brief 中提供完整文件路径和边界。若指定模型或 high reasoning 不可用，停止该任务并报告用户；不得静默降级。

## 2. 精简 Team

只有两类 subagent：

- **Question Visual Producer**：每问一个，负责本问图量规划、chart contract、pilot、绘图代码、完整数据渲染和 review 后修订。同一 prompt 也用于真实跨问共享图。不得按一图一个 Agent 拆分。
- **Figure Portfolio Reviewer**：默认只创建一个 fresh-context Agent，统一检查全部 v1 的数据准确性、图型选择、审美、可读性和论文真实版面；复用一次做关闭检查。只有总图量确实超过单个上下文承载时，才按问题包拆成多个同角色 Reviewer，不新增角色种类。

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

## 4. FR0：Leader 冻结与派工

Leader 写 `formal-figures/scope/frozen-inputs.md`，逐项记录允许读取的 Figure ID、数据包、provenance、recommendation、claim、章节位置、官方版心和文件哈希。不得让 Producer 搜索 modeling/validation 目录挑结果。

Leader 在每次创建正式图 subagent 时显式传入 `gpt-5.6-sol`、`high` 和 `fork_turns="none"`，并在 `formal-figures/scope/dispatch-log.json` 保存 Agent 句柄、角色、单元和实际请求配置。该 JSON 仅是机械调度元数据，不承载视觉判断。未显式覆盖视为未派工。

Leader指定一个 Question Visual Producer 兼任 style owner。它仍是同一角色，只额外先写 `formal-figures/style/visual-system.md`、`paper.mplstyle` 和必要 `theme.py`；其他 Producer 在共同样式落盘后开始正式渲染。

## 5. FR1：逐问 Visual Producer

每问创建一个新的 sol-high Producer，写自己的 `formal-figures/questions/qN/`；真实共享单元使用同一 prompt 写 `formal-figures/shared/UNIT-ID/`。

Producer 先写 `visual-plan.md`，说明覆盖责任、正文/附录优先级、缺图和以表代图理由。每个 Figure ID 写 `chart-contract.md`，至少说明分析问题、claim、数据粒度/单位/时间/样本量、读者比较任务、主/备图型、轴/颜色/分面/标注、尺度、误差和论文宽度。

随后用包含极值、负值/零值、最长标签、缺失、稀有类别、时间首尾和密集区域的代表性切片做 pilot。Pilot 只调代码和布局，不得进入正式 handoff。图型有真实歧义时最多生成两个 pilot 方案。

正式 v1 必须使用完整冻结数据，写：

```text
FIG-ID/
├── data-ref.md
├── chart-contract.md
├── render.py
├── render-config.md
├── render-memo.md
├── pilots/
└── v1/{figure.png,figure.pdf,figure.svg}
```

绘图代码只做已声明的视觉映射和必要格式化。语义筛选、聚合、归一化、平滑或插值必须已经在授权包中存在，或明确写入 change request。诊断图只能作为线索，正式图必须从授权数据重新绘制。

## 6. FR2/FR2R：统一审查与原 Producer 修订

全部 v1 完成后，Leader 创建一个新的 sol-high、fresh-context Figure Portfolio Reviewer。Reviewer 读取同一冻结 portfolio，不读 Producer 辩护，只写 `formal-figures/figure-review.md`。

一份 review 同时覆盖：

1. **准确性**：数据包、筛选、聚合、单位、时间、样本量、误差、图中数字、零点、对数/截断、平滑和 claim；
2. **信息设计**：图型是否匹配比较任务，统计图、主结果和稳健性图是否缺失或重复；
3. **视觉质量**：字体、颜色、层级、留白、标签、图例、碰撞、裁切、灰度/色觉可读性和默认库风格；
4. **正文环境**：目标宽度下是否清楚，Figure ID、caption 方向和章节位置是否合理。

Reviewer 不给综合美观分，不直接改图。每项写 Figure ID、证据、影响、建议动作和不得改变的数据含义。

FR2R 复用各原 Producer，分别写 `response.md`、保留 v1 并生成 `final/` 的 PNG/PDF/SVG。默认一次集中修订；只有数值/尺度错误、关键不可读或导出损坏允许第二次定向修复。纯审美偏好一轮后停止。

## 7. FR3：真实正文检查与关闭

事实稳定的 `full-paper-v2.md` 和 `figure-table-slots.md` 可用后，Leader 生成或安排只读 in-paper preview/contact sheet。复用原 Figure Portfolio Reviewer，只检查原问题是否处理、最终图是否在真实版心中可读、是否出现新裁切/错位和全篇风格是否一致，写 `figure-review-closure.md`；不开展新一轮全面审稿。

准确性问题必须修复或撤图；高影响数据/claim 问题返回 F/V/M/D；纯审美分歧保留给 Leader/人，不无限迭代。

## 8. FR4：正式图交接

Leader 写：

- `figure-coverage-map.md`：逐问覆盖、正文/附录/放弃项；
- `figure-manifest.md`：Figure ID、最终 PNG/PDF/SVG、render.py、数据包、哈希、claim 和版本；
- `placement-and-caption-handoff.md`：论文位置、尺寸、caption 骨架和禁止表达；
- `figure-rendering-handoff.md`：输入、review/closure、未决请求和 FD0 不得改变的图形口径。

完成后停止。FD0 只能消费 manifest 授权的最终图片，不能从散乱目录挑图。

## 9. 图形准确性与视觉纪律

- 绝对量柱状图默认从零开始；非零截断、对数轴、标准化、平滑和插值必须显式标注；
- 同类面板保持相同单位、尺度、时间和排序；保留误差、样本量、分母、缺失和可行性状态；
- 不混合总体、均值和明细粒度，不删除异常值来美化，不用 3D 柱状图，双 Y 轴默认不用；
- 全文使用一套中文字体和数值字体，白/近白背景、深灰文字、安静网格；单图优先一个主色根加灰，多类别颜色有上限；
- 不使用彩虹色图或同亮度红绿组合，不只靠颜色区分；同时使用线型、标记、填充、直接标签或分面；
- 标题说明画了什么，副标题补单位、时间、样本量和条件；优先直接标签，避免冗余图例；
- 最终图必须由 `render.py + frozen data` 重建，并同时交付矢量 PDF/SVG 与 PNG 预览。

## 10. 运行目录

```text
formal-figures/
├── briefs/
├── scope/{frozen-inputs.md,dispatch-log.json}
├── style/{visual-system.md,paper.mplstyle,theme.py}
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
