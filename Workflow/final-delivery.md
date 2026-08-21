# 最终排版、终审与人工交付工作流

> 状态：已实现。本文定义 FD0–FD7。模块把 PW7 的 Markdown、外部正式图、引用和最终结果装配为提交候选包；终审冻结后只报告问题，不再由 Agent 修改，最终状态为 `AWAITING_HUMAN_FINALIZATION`。

## 1. 入口、目标与停止点

入口至少包括：

- `paper-writing/formal-paper-handoff.md` 与 `paper-writing/manuscript/final-paper.md`；
- `figure-prep/figure-preparation-handoff.md` 以及外部模块交付的正式图片；
- 验证授权的结果、公式、单位、精度、限制和 claim；
- 最终引用库与引用交接（若当前 run 已实现）；
- 生成最终结果的实际数据文件、运行脚本和版本证据；
- 官方模板、页数、匿名、答卷、附件和文件命名要求。

目标是形成可供人最终微调的论文候选稿、支撑材料、五份独立终审报告和人工问题索引。本模块不自动投稿，不宣称语义“通过”，也不在终审后自动修正文稿。

停止于 `final-delivery/final-delivery-handoff.md`，状态必须写为 `AWAITING_HUMAN_FINALIZATION`。人修改数字、公式、单位、条件或核心 claim 时，应返回最早受影响的验证/建模/数据阶段；仅修改措辞、版面和合规信息时由人自行确认。

## 2. Team 与所有权

- **Final Delivery Leader**：执行 FD0，派工，冻结候选快照，保存原始 review，写问题索引、人工指南和最终 handoff；不排版、不整理支撑材料、不冒充独立 Reviewer。
- **Supporting Material Curator**：新 Agent；只写 `supporting-materials/`。整理授权结果数据，并把实际运行脚本完整粘贴到 `source-code.md`。不能从目录里自行挑“看起来最好”的结果或脚本。
- **Submission Typesetter**：新 Agent；只写 `source/`、`candidate/` 和冻结前的排版 memo。只可修改版式、资源绑定和格式转换，不得改数学事实或润色正文。
- **Layout & Compliance Auditor**：新 Agent；只写排版与官方规则 review。
- **Answer Relevance Reviewer**：新 Agent；只检查是否扣题、各问回答是否醒目、摘要正文结论是否闭合。
- **Prose & Engineering Style Auditor**：新 Agent；只定位 AI 套话、工程报告风、口水话、无必要比喻和机械句式；不给 AI 分数。
- **Delivery Evidence Auditor**：新 Agent；检查正文—图表—结果数据—代码—引用的最终对应关系。
- **End-to-End Consistency Auditor**：fresh-context 新 Agent；从最终候选反查题意、路线、数据、模型、验证、图表和论文交接，寻找跨阶段漂移与未传播问题。

五个终审角色互不读取 peer review、Leader 辩护或尚未冻结的草稿，并共享同一候选快照。前四个按各自白名单读取终稿相关材料；全链路 Auditor 额外读取 FD0 冻结的各阶段 handoff。所有 Reviewer 永久只写报告。

## 3. FD0：最终输入冻结

Leader 写 `scope/frozen-inputs.md`，列出精确路径、版本、哈希、用途和禁止旧候选。至少冻结：

- 正文 Markdown 与 formal-paper handoff；
- 正式图片文件、Figure/Table ID、caption 和来源版本；
- 结果数据、公式、单位、精度、限制和 claim；
- 引用库、已有引用核实状态与缺失引用；
- 官方模板、页数、匿名、答卷和附件规则；
- 最终运行脚本、运行记录、输入和结果版本；
- `problem-baseline`、`route-handoff`、数据/模型/验证 handoff、claim map、图表/论文框架/正式写作 handoff 的精确版本，供第五路全链路反查；
- 输出格式和支撑材料是正文后附还是独立附件。

缺少正式图片、关键引用、官方规则或最终脚本时可以建立清单，但不得把候选包标为完整。FD0 只冻结，不搜索新模型、不重开论文润色。

## 4. FD1：支撑材料整理

创建新的 Supporting Material Curator。它只使用 FD0 白名单，写：

- `supporting-materials/results/`：论文实际使用的最终结果数据及必要机器可读文件；
- `result-data-manifest.md`：结果 ID、正文/图表/claim、单位、精度、来源 run 和文件；
- `source-code-manifest.md`：脚本用途、对应问题/结果、原路径、版本、哈希和是否实际执行；
- `execution-order.md`：输入、运行顺序、入口命令、依赖和输出关系；
- `source-code.md`：按真实执行顺序完整粘贴运行脚本源代码，不能只给路径或仓库链接；
- `supporting-materials.md`：供排版的统一支撑材料源。

只收入实际生成最终授权结果的预处理、模型、汇总和必要验证脚本。不收入废弃候选、debug 临时脚本、缓存、第三方库源码或密钥。发现秘密、私人路径、许可证问题、脚本与最终 run 不一致时原样报告，不静默改写；是否脱敏交给人决定。

结果数据必须保留精确值、单位、粒度、时间范围、样本量、缺失/可行性状态和来源。篇幅过大时，Markdown 展示必要表格，同时保留完整机器可读文件；不得只展示四舍五入后的论文数字。

## 5. FD2/FD3：候选包组装、机械预检与冻结

Submission Typesetter 读取冻结正文、正式图、引用和支撑材料，写：

- `source/submission-source.md` 与 `source/supporting-materials.md`；
- `candidate/paper.pdf`；
- 官方要求的可编辑格式，如 `paper.docx` 或 LaTeX 源；
- `candidate/supporting-materials.pdf`，或官方要求的等价独立附件；
- `preflight-report.md` 与 `typesetting-memo.md`。

冻结前允许修复纯机械问题：字体、字号、页边距、标题层级、分页、公式渲染、图表尺寸、编号、交叉引用、参考文献样式、乱码、截断和资源缺失。不得为了页数删除内容、改写句子、改变数字/公式/claim，或把未完成图片伪装为正式图。超页、缺图、缺引用等需要语义取舍的问题留给终审和人。

机械预检完成后，Leader 写 `scope/candidate-snapshot.md`，列出所有候选文件、来源、哈希和冻结时间。从该时点起，`source/`、`candidate/`、`supporting-materials/` 和上游目录全部只读。

## 6. FD4：五路独立终审

四个新 Reviewer 并行读取同一 candidate snapshot，不读取 peer review。每条问题都要给精确页码/章节/短句或 artifact 定位、依据、影响、建议人工动作和不得改变的数学含义。不得只写“通过/不通过”。

### 6.1 排版与规则审查

`Layout & Compliance Auditor` 写 `reviews/layout-and-compliance-review.md`，检查页数、模板、匿名、字体/页边距、公式/图表/引用编号、清晰度、分页、答卷、附件、文件名和提交清单。

### 6.2 扣题与内容审查

`Answer Relevance Reviewer` 写 `reviews/answer-relevance-review.md`，检查每问是否直接回答题目动词和交付对象，是否有方法无结论、结果无解释、题间依赖缺失、摘要正文结论不闭合，以及次要技术细节是否挤压核心答案。

### 6.3 AI/工程风/口水话审查

`Prose & Engineering Style Auditor` 写 `reviews/prose-and-engineering-style-review.md`，定位机械关联词、重复段式、“为了……本文……”、空洞拔高、无证据形容词、无必要比喻、重复解释、长句和主语不清、模糊结论、run/debug/pipeline/config/路径/调参流水账、错误术语替换和模板化排比。它不判断作者身份，不给 AI 分数，不自动改文。

### 6.4 交付证据审查

`Delivery Evidence Auditor` 写 `reviews/delivery-evidence-review.md`，检查正文、摘要、结论、图表、结果数据、源代码、运行顺序和引用是否使用同一授权版本；关键脚本是否遗漏；是否混入旧 run、旧参数或废弃候选；支撑材料能否说明结果从哪里来。

### 6.5 全链路一致性审查

`End-to-End Consistency Auditor` 写 `reviews/end-to-end-consistency-review.md`。它使用 fresh context，从 candidate snapshot 反向读取 `problem-baseline`、`route-handoff`、数据/模型/验证 handoff、claim map、图表/论文框架/正式写作 handoff，检查题意、路线、数据口径、模型合同、题间接口、验证限制和版本选择是否跨阶段保持一致。

该角色重点报告题意或数据口径漂移、接口断裂、验证限制未传播、旧候选混入、版本错配和未裁决 change request。每项必须定位最早受影响 checkpoint 和下游传播范围；不重新选模型、不执行新实验、不修改任何阶段产物。

## 7. FD5：问题索引，只汇总不修稿

五份原始 review 全部落盘后，Leader 写 `human-review/issue-index.md`。Leader 只去重和建立交叉引用，不能覆盖、弱化或删除少数意见，也不能修改候选稿。

问题按人工处理优先级组织：

- **必须人工处理**：错误数字、缺问、匿名泄露、关键脚本/数据不对应、文件损坏等；
- **强烈建议处理**：明显不扣题、工程报告风、关键结果解释缺失、图文关系混乱等；
- **可选润色**：不改变数学含义的纯风格或版面偏好。

这只是人工优先级，不是语义通过门禁，也不生成综合 AI 分数。

## 8. FD6/FD7：人工包与停止

Leader 写：

- `human-review/human-finalization-guide.md`：哪些可改、哪些事实锁定、每项修改需复查什么；
- `submission-checklist.md`：官方文件、匿名、页数、附件、命名和人工提交动作；
- `final-delivery-handoff.md`：候选文件、支撑材料、五份 review、问题索引、未决项、哈希和状态。

FD4 之后不得创建 response、closure 或自动修订版。FD7 不提交比赛、不替人勾选已完成事项，状态固定为 `AWAITING_HUMAN_FINALIZATION`。

## 9. 运行目录

```text
final-delivery/
├── briefs/
├── scope/{frozen-inputs.md,candidate-snapshot.md}
├── source/{submission-source.md,supporting-materials.md}
├── supporting-materials/
│   ├── results/
│   ├── result-data-manifest.md
│   ├── source-code-manifest.md
│   ├── execution-order.md
│   ├── source-code.md
│   └── supporting-materials.md
├── candidate/{paper.pdf,paper.docx-or-tex,supporting-materials.pdf}
├── preflight-report.md
├── typesetting-memo.md
├── reviews/
│   ├── layout-and-compliance-review.md
│   ├── answer-relevance-review.md
│   ├── prose-and-engineering-style-review.md
│   ├── delivery-evidence-review.md
│   └── end-to-end-consistency-review.md
├── human-review/{issue-index.md,human-finalization-guide.md}
├── submission-checklist.md
└── final-delivery-handoff.md
```

所有语义交接使用开放 Markdown，模板问题只是最低责任。JSON 只记录角色、路径、版本、哈希和运行状态。机械 checker 不评价扣题、文风、证据语义或排版美观。
