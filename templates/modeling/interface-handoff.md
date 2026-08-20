# 跨问模型接口：{{INTERFACE_NAME}}

> 本文可作为 producer、consumer 或 integrator memo。以下问题是最低责任；接口存在不等于语义兼容。

## 身份、变体与版本

- 角色变体：{{PRODUCER_CONSUMER_INTEGRATOR}}
- 上游/下游问题与 build contracts：{{UPSTREAM_DOWNSTREAM}}
- 数据、代码、run 和接口版本：{{VERSIONS}}
- 当前唯一 integrator：{{INTEGRATOR_OR_NONE}}

## Producer 实际输出

说明对象、字段、主键、粒度、单位、时间、版本、不确定性、来源 run 和仍待验证限制。

## Consumer 实际需求

说明下游所需对象、字段、主键、粒度、单位、时间、可用时点和无法消费点。

## 差异与语义风险

区分机械命名/格式适配与会改变目标、总体、粒度、时间、标签或数学含义的差异。

## 获批适配与实现

仅 integrator 说明修改路径、映射、前后版本、重新生成入口、影响对象和旧接口保留。

## 失效传播

说明上游合同、数据、代码或候选版本变化时哪些接口和下游 run 失效。

## 回退与停止

指出应回到当前 M2、上游问题、数据、路线或题意的位置。需要语义变化时停止 glue code。

## 任务之外的新发现

记录未预见的跨问关系、反馈或共同隐变量。
