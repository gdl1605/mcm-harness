# 问题图表准备包：{{QUESTION_ID}}

> 本包是单个问题或共享结果单元的开放交接，不是固定 JSON schema，也不是“每问必须有图”的门禁。以下是最低责任；任何会改变结果、claim、位置、题间接口或上游回滚的新信息必须保留。

## 范围、owner 与冻结版本

- 问题/共享单元：{{QUESTION_ID_AND_OWNER}}
- Curator、Agent 句柄与复用关系：{{CURATOR_IDENTITY}}
- 冻结输入和版本：{{FROZEN_INPUTS}}
- 包生成时间、当前版本、旧版本：{{PACKAGE_VERSION}}

## 诊断支线

链接 `diagnostic-index.md` 和各 `diagnostic-note.md`，概括检查目的、关键观察、未解释异常、是否触发验证/模型/数据 change request，以及哪些只是诊断线索。

## 论文图候选

逐项链接 candidate ID、`figure-data-provenance.md`、数据文件、`figure-recommendation.md` 和授权 claim。说明每项是核心、辅助、可选、暂缓或不建议作图，并给出不作图的理由。

## 数据与语义摘要

汇总各候选的数据来源、主键、粒度、单位、时间范围、样本量、误差/区间、缺失、可行性、精确值和禁止表达；不要用摘要覆盖 provenance 中的限制。

## 问题内部叙事

说明候选图之间的先后关系、主结果表、公式、文字分析、诊断证据和下一问题接口；图在论文中的逻辑位置应能被外部 integrator 直接使用。

## 独立复核状态

链接 `evidence-review.md`、`curator-response.md` 和相关版本；保留接受、反驳、条件性支持、未决分歧和未完成检查，不以角色一致替代证据。

## Change request 与回滚

列出已提交/已裁决/待裁决的 `change-request.md`，说明受影响的上游阶段、候选、数据包和需要重做的复核。Curator 不直接修改上游目录。

## 汇交备注与停止

说明本包是否足以交给跨问 integrator、缺什么输入、哪些候选不得进入最终 handoff。此包不生成正式论文图、样式或审美评价。
