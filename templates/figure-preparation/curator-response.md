# 图表 Curator 回应：{{RESPONSE_ID}}

> 本回应记录原 Curator 对独立 evidence review 的处理，不是新的独立证据，也不是正式论文图验收。以下是最低责任，不是字段白名单；允许报告 review 未覆盖但会改变上游或交接的新发现。

## 原始身份、版本与复核范围

- Response ID / Curator / 原 question package：{{RESPONSE_ID_AND_CURATOR}}
- 收到的 review、数据包、推荐和版本：{{REVIEW_AND_PACKAGE_VERSIONS}}
- 本回应已读取的新暴露信息：{{NEW_EXPOSURE}}

## 逐项回应

对每条实质 review：

- 复述可核对的事实；
- 接受、部分接受、证据化反驳或保留分歧；
- 链接数据、脚本、结果、单位、粒度、claim 或论文位置证据；
- 说明对候选、交接和下游的影响。

不要只写“已修改”，也不要用角色信心代替复算。

## 修改与版本关系

说明修改了哪些 Markdown、导出脚本、数据包或推荐，前后路径/哈希/版本、重建命令和保留的旧产物。不得直接修改 `data/`、`modeling/`、`validation/` 或论文正文。

## 未解决问题与 Change request

列出仍未能回答的复核事项、竞争解释、需要 Leader 裁决的语义差异，以及应使用 `change-request.md` 返回的最早上游阶段。明确哪些候选应暂停或降级。

## 独立性与停止

记录本回应暴露的验证信息不得再次作为独立 holdout 的部分。默认一次集中修订后停止；若仍有高影响问题，升级而不是无限美化或改写图表口径。

## 开放发现

记录超出 review 但会改变题意、claim、数据版本、章节位置或外部绘图边界的新信息。本回应不包含审美评分。
