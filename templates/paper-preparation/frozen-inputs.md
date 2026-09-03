# 论文准备冻结输入：{{FREEZE_ID}}

> 本文只冻结允许来源和边界。以下是最低责任，不是语义 JSON schema，也不预先决定章节结论。

## 冻结身份

- run、时间、Leader、source snapshot：{{IDENTITY}}
- validation handoff / claim map：{{VALIDATION_INPUTS}}
- V6 证据优先答案重建 / 意图与题链对照：{{ANSWER_RECONSTRUCTION_INPUTS}}
- data/model handoff：{{ENGINEERING_HANDOFFS}}
- 逐问权威方法说明及其 build contract、代码/config、授权结果和接口对应版本：{{AUTHORITATIVE_METHOD_NOTES}}
- 候选模型汇报 / 真实人工模型决定 / route handoff：{{HUMAN_AUTHORIZED_ROUTE_TRACE}}

## 逐问授权

逐问链接可使用的结果、公式、claim、题间接口、版本、单位、精度、条件和限制；把 M6 指定且与当前验证处置一致的一个方法说明版本冻结为 CP3A 权威输入，并列出旧说明和已知语义缺口。说明哪些答案已经存在、哪些只能条件化使用、哪些仍因证据或决策缺口不能成文。CP 不得补造未形成的答案，也不得从代码反推方法。

同时区分建模前“相比 baseline 预期增加什么”与验证后实际成立的内容。逐问链接同口径 baseline/直观路线、主模型、有效挑战或结构反例，以及能够说明有效性、可行性、答案变化或无实质增量的证据；若没有完成必要比较，明确记录，不能把预期价值冻结为论文贡献。

## 官方要求与篇幅

记录论文模板、页数、答卷、语言、匿名、文件和其他官方要求；缺失项明确标记未知，不自行补造。

## 图表与引用状态

记录 figure-prep 的路径/版本、已有 Figure ID、仍待补的图表；链接 route-evidence-handoff、REF4–REF6 状态、source notes、references-handoff/references.bib 和 citation-needed。

## 两遍竞赛审读隔离

登记 `state/mcm-skill-snapshot.json`、`Workflow/mcm-skill-integration.json` 和国奖论文蒸馏材料的精确路径。CP5 盲审完成前使用 `blind-review`，禁止加载 `$mcm` 或蒸馏材料；第二遍由 Leader 显式切换到 `judge-review`，只把它作为答案层级、证据组织和表达镜头，不当成本题证据。

## 所有权、版本与开放发现

列出问题 owner、独立 reviewer、写入根、旧版保留方式、change request 路径，以及最低责任之外会改变论文准备的新发现。
