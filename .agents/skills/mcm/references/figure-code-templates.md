# Figure Code Templates

服务 `SKILL.md` Step 6、Step 8：把已有结果表转成能支撑论文结论的稳妥图表。

最应该调用的场景：已经有结果表、排序表、预测表或分组摘要表，需要快速生成正文可引用图。

证据等级：[高频共性]
证据来源：`references/distill/modeling-playbook.md` 第 5 节；`references/distill/writing-playbook.md` 的“结果要先成为答案”与“信息密度”原则；`references/distill/evidence-map.md` 的图表职责证据。

## 硬规则

一张图只服务一句核心结论。若题目要求精确数值、推荐名单、判定结果，先给表，再用图解释规律。

## 0. 通用保存骨架

```python
from pathlib import Path
import matplotlib.pyplot as plt

FIGURES = Path("outputs/figures")
FIGURES.mkdir(parents=True, exist_ok=True)

plt.rcParams["font.sans-serif"] = ["SimHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def save_fig(fig, filename):
    fig.tight_layout()
    fig.savefig(FIGURES / filename, dpi=300, bbox_inches="tight")
    plt.close(fig)
```

## 1. 排序/评分结果图

适用场景：TOPSIS 得分、供应商/对象 Top-k、优先级评分。

支撑结论：谁排在前列、头部差距是否明显、推荐对象是否稳定。

最少输入：`label_col`、`score_col`，可选 `top_n`。

不建议使用：对象很多且需要完整名单时；此时最终答卷应先给排序表。

更适合用表：题目要求提交 Top-k 名单、推荐清单或每个对象精确得分。

```python
import pandas as pd
import matplotlib.pyplot as plt


def plot_topk_bar(df, label_col, score_col, title, filename, top_n=10):
    data = df.sort_values(score_col, ascending=False).head(top_n).copy()
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.barh(data[label_col].astype(str)[::-1], data[score_col][::-1], color="#3b6ea8")
    ax.set_title(title)
    ax.set_xlabel(score_col)
    ax.set_ylabel(label_col)
    ax.grid(axis="x", alpha=0.25)
    save_fig(fig, filename)
```

正文承接句：`图 x 显示，前 n 个对象得分明显高于其余对象，因此可作为优先候选集。`

## 2. 趋势/对比折线图

适用场景：销量、价格、达标率、误差、收益随时间或阶段变化。

支撑结论：趋势方向、周期差异、方案对比随时间变化。

最少输入：`x_col`、`y_col`、可选 `group_col`。

不建议使用：只有一个时间点、横轴没有顺序、需要提交精确方案表。

更适合用表：最终预测值、每日补货量、每日定价方案。

```python
import matplotlib.pyplot as plt


def plot_trend_lines(df, x_col, y_col, title, filename, group_col=None):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if group_col:
        for name, part in df.sort_values(x_col).groupby(group_col):
            ax.plot(part[x_col], part[y_col], marker="o", linewidth=1.8, label=str(name))
        ax.legend(title=group_col, fontsize=9)
    else:
        data = df.sort_values(x_col)
        ax.plot(data[x_col], data[y_col], marker="o", linewidth=1.8)
    ax.set_title(title)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.grid(alpha=0.25)
    save_fig(fig, filename)
```

正文承接句：`图 x 表明，{指标} 在 {时间范围} 内呈现 {上升/下降/波动}，这为后续 {预测/补货/时点选择} 提供依据。`

## 3. 分组柱状图

适用场景：不同类别、分组、方案或场景下的均值/总量/指标对比。

支撑结论：组间差异、方案优势、某类对象需要单独处理。

最少输入：`group_col`、`value_col`，可选 `category_col`。

不建议使用：组别过多、柱子超过 15 个、需要精确最终值。

更适合用表：分组边界、推荐方案、判定结果。

```python
import matplotlib.pyplot as plt


def plot_grouped_bar(df, group_col, value_col, title, filename, category_col=None):
    fig, ax = plt.subplots(figsize=(8, 4.8))
    if category_col:
        pivot = df.pivot(index=group_col, columns=category_col, values=value_col).fillna(0)
        pivot.plot(kind="bar", ax=ax)
        ax.legend(title=category_col, fontsize=9)
    else:
        data = df.sort_values(value_col, ascending=False)
        ax.bar(data[group_col].astype(str), data[value_col], color="#6b9b5b")
    ax.set_title(title)
    ax.set_xlabel(group_col)
    ax.set_ylabel(value_col)
    ax.grid(axis="y", alpha=0.25)
    save_fig(fig, filename)
```

正文承接句：`由图 x 可见，不同 {分组} 在 {指标} 上差异明显，说明模型需要按组制定方案。`

## 4. 简洁热力图

适用场景：相关矩阵、方案-场景得分矩阵、品类间关系强度。

支撑结论：关系强弱、矩阵结构、哪些对象联系更紧密。

最少输入：二维数值矩阵或可 pivot 的三列表。

不建议使用：矩阵太大、标签密集到无法阅读、最终答案需要逐项精确值。

更适合用表：最终推荐、精确方案、完整相关系数清单。

```python
import matplotlib.pyplot as plt


def plot_heatmap(matrix_df, title, filename, cmap="YlGnBu"):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    im = ax.imshow(matrix_df.values, cmap=cmap, aspect="auto")
    ax.set_title(title)
    ax.set_xticks(range(len(matrix_df.columns)))
    ax.set_xticklabels(matrix_df.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(matrix_df.index)))
    ax.set_yticklabels(matrix_df.index)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    save_fig(fig, filename)
```

正文承接句：`图 x 的颜色深浅反映了 {关系/得分} 强弱，其中 {对象 A} 与 {对象 B} 的关系更突出。`

## 图表与 final answer artifact 的关系

- 图表解释“为什么”，final answer artifact 回答“是什么”。
- 图表文件名要能被正文稳定引用，例如 `problem2_replenishment_trend.png`。
- 每张图后至少跟一句中文解释：它支持哪一个判断。
- 不要让图成为装饰；如果正文没有引用这张图，就删掉或移到附录。
