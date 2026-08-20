# 图表准备上游变更请求：{{REQUEST_ID}}

> 图表 subagent 用本文提出证据驱动的上游变更请求，不直接修 `data/`、`modeling/` 或 `validation/`。以下是最低责任，不是字段白名单；若存在其他失效传播、竞争解释或新主张，必须继续记录。

## 触发与来源版本

- Request ID / 提出角色 / 时间：{{REQUEST_ID_AND_OWNER}}
- 触发的诊断、review、response 或原始证据：{{TRIGGER_EVIDENCE}}
- 受影响的 data、model、validation、claim、run、结果、接口和图表版本：{{AFFECTED_VERSIONS}}

## 事实、推断与失效机制

区分已核对事实、合理推断、反例、未知和为什么当前图表目录不能自行修复；说明问题是数据、粒度、单位、时间、误差、缺失、可行性、模型结果、验证授权还是论文叙事。

## 最早回滚位置与责任 owner

指定应返回的数据工程 D 阶段、建模 M 阶段、验证 V 阶段或更早阶段，列出原 owner、应读取的交接和需要复用/新建的 Agent。不要用图表 Curator 代替上游责任。

## 最小修正范围与冻结项

说明允许改变的对象、必须冻结的总体、目标、标签、时点、接口、单位和 claim，旧版本如何保留，哪些“为了画图好看”的改动禁止进行。

## 失效传播与重验

列出暂停使用的诊断、数据包、候选图、claim、章节位置和下游接口；说明修正后需要新 run、新数据导出或新的独立验证证据的范围。

## Leader 裁决与状态

- 当前状态：{{OPEN_ACCEPTED_REJECTED_DEFERRED}}
- Leader 决定与依据：{{LEADER_DECISION}}
- 生效版本与重开路径：{{EFFECTIVE_VERSION_AND_REOPEN}}

## 保留信息与开放发现

记录原 owner 或 Curator 已看到的验证信息、不能再作为独立证据的对象，以及本请求之外可能改变论文表述或图表授权的新发现。
