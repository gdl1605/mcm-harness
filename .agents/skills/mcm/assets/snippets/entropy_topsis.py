"""
熵权 TOPSIS 评价/排序基线 snippet。

适用题型：评价/排序、Top-k 筛选、上游候选集筛选。
证据等级：[高频共性]
主要证据来源：references/distill/modeling-playbook.md Route A；references/distill/evidence-map.md 中 2021 C066/C169/C283。
触发条件：题目要求对象排序、优先级评分或 Top-k 名单，且已有清洗后的指标表。
非目标：不是完整比赛解法；不是自动构建指标体系；不是替用户判断权重合理性的工具。
最小输入：对象主键列、指标列、指标方向配置，可选权重模式。
最小输出：对象-得分-排名表，可选 Top-k 表。
"""

from __future__ import annotations

import math
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence

Row = MutableMapping[str, Any]


def _as_rows(table: Any) -> List[Row]:
    """接受 pandas.DataFrame 或 list[dict]，统一转为行字典。"""
    if hasattr(table, "to_dict"):
        return [dict(row) for row in table.to_dict("records")]
    return [dict(row) for row in table]


def _safe_float(value: Any) -> float:
    if value is None or value == "":
        return 0.0
    return float(value)


def _normalize_matrix(rows: List[Row], indicators: Sequence[str], directions: Mapping[str, str]) -> List[List[float]]:
    columns: Dict[str, List[float]] = {
        indicator: [_safe_float(row.get(indicator)) for row in rows]
        for indicator in indicators
    }
    normalized: List[List[float]] = []
    for row_index in range(len(rows)):
        current: List[float] = []
        for indicator in indicators:
            values = columns[indicator]
            low, high = min(values), max(values)
            if math.isclose(high, low):
                current.append(1.0)
                continue
            raw = values[row_index]
            direction = directions.get(indicator, "positive")
            if direction in {"negative", "cost", "min"}:
                current.append((high - raw) / (high - low))
            else:
                current.append((raw - low) / (high - low))
        normalized.append(current)
    return normalized


def _entropy_weights(matrix: List[List[float]], indicators: Sequence[str]) -> Dict[str, float]:
    n = len(matrix)
    m = len(indicators)
    if n == 0 or m == 0:
        raise ValueError("指标矩阵不能为空")
    if n == 1:
        return {indicator: 1.0 / m for indicator in indicators}

    diversities: List[float] = []
    for j in range(m):
        col = [max(matrix[i][j], 0.0) for i in range(n)]
        total = sum(col)
        if math.isclose(total, 0.0):
            diversities.append(0.0)
            continue
        entropy = 0.0
        for value in col:
            if value <= 0:
                continue
            p = value / total
            entropy -= p * math.log(p)
        entropy /= math.log(n)
        diversities.append(1 - entropy)

    total_diversity = sum(diversities)
    if math.isclose(total_diversity, 0.0):
        return {indicator: 1.0 / m for indicator in indicators}
    return {indicator: diversities[idx] / total_diversity for idx, indicator in enumerate(indicators)}


def _resolve_weights(
    matrix: List[List[float]],
    indicators: Sequence[str],
    weight_mode: str,
    weights: Optional[Mapping[str, float]],
) -> Dict[str, float]:
    if weights:
        total = sum(float(weights[indicator]) for indicator in indicators)
        if math.isclose(total, 0.0):
            raise ValueError("自定义权重之和不能为 0")
        return {indicator: float(weights[indicator]) / total for indicator in indicators}
    if weight_mode == "equal":
        return {indicator: 1.0 / len(indicators) for indicator in indicators}
    if weight_mode == "entropy":
        return _entropy_weights(matrix, indicators)
    raise ValueError("weight_mode 仅支持 entropy、equal 或传入 custom weights")


def fit_rank(
    table: Any,
    indicators: Sequence[str],
    id_col: str,
    weight_mode: str = "entropy",
    directions: Optional[Mapping[str, str]] = None,
    weights: Optional[Mapping[str, float]] = None,
    top_k: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """输出对象、得分、排名和权重信息。"""
    rows = _as_rows(table)
    if not rows:
        raise ValueError("输入表不能为空")
    directions = directions or {indicator: "positive" for indicator in indicators}
    matrix = _normalize_matrix(rows, indicators, directions)
    resolved_weights = _resolve_weights(matrix, indicators, weight_mode, weights)

    results: List[Dict[str, Any]] = []
    for row, values in zip(rows, matrix):
        weighted = [values[idx] * resolved_weights[indicator] for idx, indicator in enumerate(indicators)]
        positive_distance = math.sqrt(sum((weighted[idx] - resolved_weights[indicators[idx]]) ** 2 for idx in range(len(indicators))))
        negative_distance = math.sqrt(sum(weighted[idx] ** 2 for idx in range(len(indicators))))
        score = negative_distance / (positive_distance + negative_distance) if not math.isclose(positive_distance + negative_distance, 0.0) else 0.0
        results.append({id_col: row[id_col], "score": score})

    results.sort(key=lambda item: item["score"], reverse=True)
    for rank, item in enumerate(results, start=1):
        item["rank"] = rank
        for indicator in indicators:
            item[f"weight_{indicator}"] = resolved_weights[indicator]
    return results[:top_k] if top_k else results


if __name__ == "__main__":
    demo_rows = [
        {"supplier": "S1", "supply": 92, "stability": 0.88, "loss_rate": 0.03},
        {"supplier": "S2", "supply": 76, "stability": 0.95, "loss_rate": 0.04},
        {"supplier": "S3", "supply": 84, "stability": 0.81, "loss_rate": 0.02},
    ]
    ranking = fit_rank(
        demo_rows,
        indicators=["supply", "stability", "loss_rate"],
        id_col="supplier",
        directions={"supply": "positive", "stability": "positive", "loss_rate": "negative"},
        top_k=2,
    )
    for row in ranking:
        print(row)
