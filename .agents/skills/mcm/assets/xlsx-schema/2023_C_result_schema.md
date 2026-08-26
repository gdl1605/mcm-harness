# 2023 C 题结果 schema 锚点

适用场景：2023 C 类“蔬菜补货与定价”运营题，尤其是“未来一周按品类方案表”“单日按单品方案表”“开放式数据建议表”。
来源锚点：2023 mini blind run、答案表检查、年度回归摘要、回归 scorecard/delta summary；`references/distill/evidence-map.md` 中 2023-C050 的链路总结。
证据等级：[中频经验]

## 非目标

- 不是正式 Excel 成品。
- 不是 1085 天流水与全部单品字段的全量导出模板。
- 不是价格-销量-利润联合优化器本身。
- 不要求把所有中间分析字段都塞进最终答卷表。

## 结果结构总览

| 结果对象 | 适用问题 | 最小粒度 | 最关键的最终答卷支撑列 | 备注 |
| --- | --- | --- | --- | --- |
| `Q1_品类规律摘要表` | 问题 1 | `category_name` | `category_name`、`avg_daily_sales_kg`、`sales_volatility_index`、`seasonality_note`、`correlation_note` | Q1 以摘要表 + 图/相关说明为主，不必硬造推荐表 |
| `Q2A_7天品类补货表` | 问题 2 | `date × category_name` | `date`、`category_name`、`replenishment_kg` | 补货表必须独立存在，不能藏在模型变量里 |
| `Q2B_7天品类定价表` | 问题 2 | `date × category_name` | `date`、`category_name`、`selling_price_yuan_per_kg` | 与补货表配套，正文共同引用 |
| `Q2C_品类方案收益摘要表` | 问题 2 | `date × category_name` 或 `category_name` | `expected_sales_kg`、`expected_profit_yuan`、`decision_note` | 用于说明为什么这套 7 天方案可取 |
| `Q3_7月1日单品方案表` | 问题 3 | `item_code × 2023-07-01` | `item_code`、`item_name`、`category_name`、`replenishment_kg`、`selling_price_yuan_per_kg` | 这是 Q3 最核心的最终表 |
| `Q4_数据建议优先级表` | 问题 4 | `priority × data_item` | `priority`、`data_item`、`solve_question`、`expected_use`、`expected_benefit` | 开放问答必须表格化收口 |

## Q1：品类规律摘要表

适用场景：回答“品类及单品销售分布规律与相互关系”。

| 列名 | 含义 | 列角色 | 与正文如何呼应 |
| --- | --- | --- | --- |
| `category_name` | 品类名称 | 最终答卷支撑列 | “由表 x 可见，各品类销售规模存在明显差异……” |
| `avg_daily_sales_kg` | 日均销量 | 最终答卷支撑列 | 用于说明规模和补货压力 |
| `sales_volatility_index` | 波动性指标 | 正文支撑列 | 用于解释为什么某品类需要更保守补货 |
| `weekday_pattern` | 周内规律摘要 | 正文支撑列 | 用于说明周期性 |
| `discount_share` | 折扣销售占比 | 中间分析列 | 可在正文按需提一句，不必强制出现在最终表 |
| `correlation_note` | 与其他品类的相关性摘要 | 最终答卷支撑列 | 用于把 Q1 结果衔接到 Q2/Q3 |
| `representative_items` | 代表性单品 | 可后补列 | 时间紧时可先不填 |

使用提醒：

- Q1 的重点是“服务 Q2/Q3 的分析前置模块”，不是把图表堆满。
- 最终表可以瘦，但必须能支撑一句“这对后续补货/定价意味着什么”。

## Q2A：7 天品类补货表

适用场景：回答“未来一周每天各品类补货量”。

| 列名 | 含义 | 列角色 | 与正文如何呼应 |
| --- | --- | --- | --- |
| `date` | 日期 | 最终答卷支撑列 | 正文引用日期范围 |
| `category_name` | 品类名称 | 最终答卷支撑列 | 正文说明品类差异 |
| `replenishment_kg` | 建议补货量（kg） | 最终答卷支撑列 | “7 月 1-7 日各品类建议补货量见表 x” |
| `expected_sales_kg` | 预期销量 | 正文支撑列 | 用于解释补货量不是拍脑袋给出 |
| `loss_rate_proxy` | 使用的损耗率代理 | 中间分析列 | 一般放模型说明或附录 |
| `inventory_or_display_floor` | 最低陈列/库存约束 | 可后补列 | 若时间紧可先在正文解释，不强制进表 |
| `decision_note` | 特殊说明 | 可后补列 | 例如节假日、异常波动说明 |

## Q2B：7 天品类定价表

适用场景：回答“未来一周每天各品类定价策略”。

| 列名 | 含义 | 列角色 | 与正文如何呼应 |
| --- | --- | --- | --- |
| `date` | 日期 | 最终答卷支撑列 | 与补货表同频引用 |
| `category_name` | 品类名称 | 最终答卷支撑列 | 与补货表配对 |
| `selling_price_yuan_per_kg` | 建议售价（元/kg） | 最终答卷支撑列 | “建议售价见表 x” |
| `wholesale_price_yuan_per_kg` | 对应批发价 | 正文支撑列 | 支撑毛利解释 |
| `expected_sales_kg` | 该价位下预期销量 | 正文支撑列 | 解释定价并非只看加成 |
| `expected_profit_yuan` | 预期利润 | 最终答卷支撑列 | 支撑“为何这样定价” |
| `pricing_note` | 调价说明 | 可后补列 | 时间紧时可简化为正文说明 |

## Q2C：品类方案收益摘要表

适用场景：把补货与定价方案压成可解释的收益摘要。

| 列名 | 含义 | 列角色 | 与正文如何呼应 |
| --- | --- | --- | --- |
| `date` | 日期 | 正文支撑列 | 可做逐日收益比较 |
| `category_name` | 品类名称 | 正文支撑列 | 说明不同品类策略差异 |
| `expected_revenue_yuan` | 预期销售额 | 正文支撑列 | 配合利润解释 |
| `expected_profit_yuan` | 预期利润 | 最终答卷支撑列 | 核心比较列 |
| `gross_margin_rate` | 毛利率 | 正文支撑列 | 衔接定价逻辑 |
| `decision_note` | 方案说明 | 可后补列 | 解释保守/激进策略 |

使用提醒：

- Q2 最终至少要有“补货表 + 定价表”；收益摘要表可以和正文、验证一起使用。
- 不要只给“价格-销量关系图”而不落成 `日期 × 品类` 表。

## Q3：7 月 1 日单品方案表

适用场景：回答“在可售单品与最小陈列量约束下，给出 7 月 1 日单品补货与定价方案”。

| 列名 | 含义 | 列角色 | 与正文如何呼应 |
| --- | --- | --- | --- |
| `item_code` | 单品编码 | 最终答卷支撑列 | 明确回答“选了哪些单品” |
| `item_name` | 单品名称 | 最终答卷支撑列 | 方便正文引用与人工核查 |
| `category_name` | 所属品类 | 最终答卷支撑列 | 支撑品类覆盖说明 |
| `replenishment_kg` | 建议补货量（kg） | 最终答卷支撑列 | Q3 最关键输出列之一 |
| `selling_price_yuan_per_kg` | 建议售价（元/kg） | 最终答卷支撑列 | Q3 最关键输出列之一 |
| `expected_sales_kg` | 预期销量 | 正文支撑列 | 用于解释为什么选它 |
| `expected_profit_yuan` | 预期利润 | 正文支撑列 | 用于说明单品组合的收益性 |
| `display_floor_kg` | 最小陈列量 | 中间分析列 | 可在约束说明或附录中出现 |
| `selection_reason` | 入选原因 | 可后补列 | 时间不够时可以只在正文概括 |

使用提醒：

- 这张表必须是“最终单日单品方案表”，不能只停留在“候选单品清单”或“筛选原则”。
- 若时间紧，可先给 27-33 个单品的 `item_code/item_name/category_name/replenishment_kg/selling_price_yuan_per_kg` 五列，再补收益解释列。

## Q4：数据建议优先级表

适用场景：回答“还应采集哪些数据，以及这些数据如何帮助补货与定价”。

| 列名 | 含义 | 列角色 | 与正文如何呼应 |
| --- | --- | --- | --- |
| `priority` | 优先级 | 最终答卷支撑列 | 开放问答必须有明确先后顺序 |
| `data_item` | 建议采集的数据项 | 最终答卷支撑列 | 直接回答“采什么” |
| `solve_question` | 主要服务哪一问 | 最终答卷支撑列 | 把建议和赛题绑定 |
| `expected_use` | 具体用途 | 最终答卷支撑列 | 说明不是泛泛建议 |
| `expected_benefit` | 预期收益 | 最终答卷支撑列 | 支撑优先级 |
| `collection_frequency` | 采集频率 | 可后补列 | 时间紧可先不写 |
| `implementation_note` | 采集说明 | 可后补列 | 作为落地说明 |

使用提醒：

- Q4 不能只写成一段建议文字，至少要导出一张优先级表。
- 正文应围绕 `priority + data_item + expected_benefit` 三列给出最短结论。

## 与正文呼应的最短写法

可直接参考以下句式：

- “由表 x 中的 `date`、`category_name` 与 `replenishment_kg` 可见，未来一周各品类补货量存在明显日间差异，因此补货策略应按天滚动调整。”
- “根据表 x 的 `selling_price_yuan_per_kg` 与 `expected_profit_yuan`，花叶类与食用菌类应采用差异化定价，以兼顾销量与毛利。”
- “表 x 给出的 `item_code`、`item_name`、`replenishment_kg` 与 `selling_price_yuan_per_kg` 构成了 7 月 1 日最终单品方案，可直接作为题目要求的可售单品安排。”
- “综合表 x 的 `priority`、`data_item` 与 `expected_benefit`，优先建议补采……，其直接价值在于提升……问题的补货与定价精度。”

## 最小可交付版本

时间不够时，先保以下列：

### Q2 最小可交付列

- `date`
- `category_name`
- `replenishment_kg`
- `selling_price_yuan_per_kg`

可后补：`expected_sales_kg`、`expected_profit_yuan`、`decision_note`

绝不能缺：日期、品类、补货量、售价。缺任一项都会让“未来一周方案表”无法交卷。

### Q3 最小可交付列

- `item_code`
- `item_name`
- `category_name`
- `replenishment_kg`
- `selling_price_yuan_per_kg`

可后补：`expected_sales_kg`、`expected_profit_yuan`、`selection_reason`

绝不能缺：单品标识、所属品类、补货量、售价。否则只能算“筛选思路”，不能算“单品方案表”。

### Q4 最小可交付列

- `priority`
- `data_item`
- `solve_question`
- `expected_use`

可后补：`expected_benefit`、`collection_frequency`、`implementation_note`

绝不能缺：优先级、数据项、服务问题、用途。否则开放问答无法形成可评分交付表。

## 不要做什么

- 不要把所有中间分析字段都塞进最终表，导致表太胖、正文反而无法引用。
- 不要只有 Q2 的价格/销量关系说明，没有 `日期 × 品类` 的正式方案表。
- 不要只有 Q3 的筛选原则或候选单品说明，没有最终 `单品 × 补货量 × 定价` 表。
- 不要让 schema 只停留在说明层，最后的 final answer artifact 和正文却各写各的。
- 不要把 Q1 做成大量图表堆积，反而挤压 Q2/Q3 的最终交付。
