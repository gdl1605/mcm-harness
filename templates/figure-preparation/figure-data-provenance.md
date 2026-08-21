# 论文图数据来源与复现说明：{{FIGURE_ID}}

> 本文说明一个候选论文图数据包从授权结果到可作图数据的完整血缘。以下是最低责任，不是字段白名单或 JSON schema；所有会影响解释的语义、限制和例外都必须用开放 Markdown 说明。

## 候选身份与授权 claim

- Figure ID / 问题：{{FIGURE_ID_AND_QUESTION}}
- 支持的精确 claim：{{AUTHORIZED_CLAIM}}
- claim disposition / 验证证据：{{CLAIM_DISPOSITION_AND_EVIDENCE}}
- 数据包状态与版本：{{PACKAGE_STATUS_AND_VERSION}}

## 来源链

逐层链接原始结果表、模型/run、代码/config、数据版本、接口和导出脚本，说明每一层实际贡献。记录旧版本、被替换版本、哈希和失效传播，不只写“来自模型结果”。

## 导出对象与语义

说明 CSV/Parquet/其他文件的路径、主键、行粒度、字段含义、单位、时间范围、分组、排序和精确值。区分 observed、derived、proxy、label、decision quantity；说明每个派生量的公式、分母和适用边界。

## 选择、变换与聚合

完整记录筛选条件、缺失处理、异常保留、聚合、归一化、重采样、排序和展示前精度；不得静默删除不利结果或为了作图改变目标总体。若新增分析口径，必须回到上游确认并标记版本。

## 不确定性、缺失与可行性

明确误差、置信/预测区间、样本量、重复次数、缺失含义、不可行状态、约束违背和截断范围如何在数据包中保留。没有可用信息时也要写明“未知”，不能让 FR Visual Producer 猜测。

## 复现入口与检查

- 从冻结输入重建命令：{{REBUILD_COMMAND}}
- 导出脚本与依赖环境：{{EXPORT_SCRIPT_AND_ENV}}
- 输出文件哈希/行数/范围检查：{{CHECKS}}
- 失败、例外和未完成检查：{{FAILURES_AND_GAPS}}

## 允许与禁止表达

说明本数据包允许支持的图表叙事、必须随图传递的条件，以及不允许 FR Visual Producer 暗示的因果、最优性、泛化、显著性或超出验证范围的结论。

## 交接备注与开放发现

记录 FR Visual Producer 可能需要的语义解释、诊断线索、争议、change request 和尚未解决的问题。本文不要求生成正式论文图、样式文件或审美评分。
