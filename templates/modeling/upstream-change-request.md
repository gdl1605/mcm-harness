# 建模上游变更请求：{{TARGET_STAGE_AND_ISSUE}}

> 本文用于 L3 或必要的上游重开，不授权模型 builder 直接修改数据、路线或题意。以下问题是最低责任。

## 触发运行与当前版本

索引问题、build contract、run intent、iteration memo、diagnosis、response、adjustment、数据/路线/题意版本。

## 无法在建模合同内解决的问题

说明目标构造、标签/proxy、总体、Canonical 数据、可用时点、题间接口、路线或题意哪里冲突。

## 证据与竞争解释

给出题面、数据、代码、日志、结果和反例；说明为何不是普通 L0/L1/L2。

## 请求的上游动作

明确请求哪个阶段核查什么，不预先替上游决定答案。列出最低成本区分证据。

## 是否改变人工模型决定

若改变模型家族、目标或核心结构，另行使用 `templates/model-selection-change-request.md` 写入 `routes/change-requests/`，并将状态置为 `AWAITING_HUMAN_MODEL_DECISION`；本请求本身不构成人工批准。

## 影响与暂停范围

说明哪些问题、run、接口、结果和文稿暂停/失效，哪些可继续。

## 期望回传

说明上游需返回的新版本、适用边界、数据/接口变化和回滚说明。

## 临时安全核心与新发现

若有不依赖争议的工作可继续，明确边界；保留任务之外的新事项。
