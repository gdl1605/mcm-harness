"""
阈值达标时间 / 首次 crossing 条件触发 snippet。

适用题型：阈值达标时间、首次超过/低于阈值、触发时点、分组达标率分析。
证据等级：[中频经验]
主要证据来源：references/distill/modeling-playbook.md Route B2；references/distill/source-notes/2025-c-commentary.md 的首次达标与区间删失讨论；2025 C 题已暴露诊断语料。
触发条件：题目明确问“何时首次达标/最早达标时间/首次 crossing/触发时点”，且有对象 ID、时间列、指标列和阈值定义。
何时不建议使用：普通未来数值预测、只有单时点数据、阈值没有题意依据、需要完整 survival/deep survival 模型时。
非目标：不是所有预测题默认骨架；不是 survival 套件；不是 2025 论文方案复刻；不替代 naive_forecast.py 的普通短期预测角色。
最小输入：多时点行表、对象 ID 列、时间列、指标列、阈值、可选分组列。
最小输出：对象级 first-hit 表、分组达标率表、阈值敏感性表。
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence

Row = Mapping[str, Any]


def _parse_time(value: Any) -> Any:
    """尽量把日期字符串转成 date；否则保留原值，适合孕周/批次这类数值时间。"""
    if isinstance(value, (date, int, float)):
        return value
    text = str(value)
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    try:
        return float(text)
    except ValueError:
        return text


def _is_crossed(value: float, threshold: float, direction: str) -> bool:
    if direction in {">=", "ge", "up"}:
        return value >= threshold
    if direction in {">", "gt"}:
        return value > threshold
    if direction in {"<=", "le", "down"}:
        return value <= threshold
    if direction in {"<", "lt"}:
        return value < threshold
    raise ValueError("direction 仅支持 >=、>、<=、< 或 ge/gt/le/lt/up/down")


def first_crossing_table(
    rows: Sequence[Row],
    id_col: str,
    time_col: str,
    value_col: str,
    threshold: float,
    group_col: Optional[str] = None,
    direction: str = ">=",
) -> List[Dict[str, Any]]:
    """输出每个对象首次达标时间；未达标对象保留 reached=False。"""
    grouped: Dict[Any, List[Row]] = defaultdict(list)
    for row in rows:
        grouped[row[id_col]].append(row)

    result: List[Dict[str, Any]] = []
    for obj, history in grouped.items():
        ordered = sorted(history, key=lambda r: _parse_time(r[time_col]))
        hit = None
        for row in ordered:
            value = float(row[value_col])
            if _is_crossed(value, threshold, direction):
                hit = row
                break
        base = ordered[0]
        result.append(
            {
                id_col: obj,
                "group": base.get(group_col) if group_col else "all",
                "threshold": threshold,
                "direction": direction,
                "reached": hit is not None,
                "first_cross_time": hit[time_col] if hit else None,
                "first_cross_value": float(hit[value_col]) if hit else None,
                "last_observed_time": ordered[-1][time_col],
                "last_observed_value": float(ordered[-1][value_col]),
                "n_observations": len(ordered),
            }
        )
    return result


def reach_rate_by_group(crossing_rows: Sequence[Row], group_col: str = "group") -> List[Dict[str, Any]]:
    """把对象级 first-hit 表压成分组达标率表。"""
    grouped: Dict[Any, List[Row]] = defaultdict(list)
    for row in crossing_rows:
        grouped[row.get(group_col, "all")].append(row)

    summary: List[Dict[str, Any]] = []
    for group, rows in grouped.items():
        reached = [row for row in rows if row.get("reached")]
        summary.append(
            {
                group_col: group,
                "n_objects": len(rows),
                "reached_count": len(reached),
                "reach_rate": len(reached) / len(rows) if rows else 0.0,
                "example_first_cross_time": reached[0].get("first_cross_time") if reached else None,
            }
        )
    return sorted(summary, key=lambda row: str(row[group_col]))


def threshold_sensitivity(
    rows: Sequence[Row],
    thresholds: Iterable[float],
    id_col: str,
    time_col: str,
    value_col: str,
    group_col: Optional[str] = None,
    direction: str = ">=",
) -> List[Dict[str, Any]]:
    """扰动阈值，观察达标数量和达标率是否稳定。"""
    out: List[Dict[str, Any]] = []
    for threshold in thresholds:
        table = first_crossing_table(rows, id_col, time_col, value_col, threshold, group_col, direction)
        reached_count = sum(1 for row in table if row["reached"])
        out.append(
            {
                "threshold": threshold,
                "n_objects": len(table),
                "reached_count": reached_count,
                "reach_rate": reached_count / len(table) if table else 0.0,
            }
        )
    return out


def conclusion_hint(summary_rows: Sequence[Row], group_col: str = "group") -> str:
    """给论文结果段一个可改写的中文结论句。"""
    if not summary_rows:
        return "尚无达标摘要，需先生成 first-hit 表。"
    best = max(summary_rows, key=lambda row: float(row.get("reach_rate", 0)))
    return f"由达标率表可见，{group_col}={best[group_col]} 的达标率最高，达到 {float(best['reach_rate']):.2%}，可作为时点或分组决策的重要依据。"


def _demo() -> None:
    rows = [
        {"person": "A", "group": "G1", "week": 11, "value": 0.030},
        {"person": "A", "group": "G1", "week": 12, "value": 0.041},
        {"person": "B", "group": "G1", "week": 11, "value": 0.025},
        {"person": "B", "group": "G1", "week": 13, "value": 0.038},
        {"person": "C", "group": "G2", "week": 12, "value": 0.044},
        {"person": "C", "group": "G2", "week": 13, "value": 0.052},
    ]
    first_hit = first_crossing_table(rows, "person", "week", "value", threshold=0.04, group_col="group")
    group_summary = reach_rate_by_group(first_hit)
    sensitivity = threshold_sensitivity(rows, [0.035, 0.04, 0.045], "person", "week", "value", group_col="group")
    print("first_hit:", first_hit)
    print("group_summary:", group_summary)
    print("sensitivity:", sensitivity)
    print(conclusion_hint(group_summary))


if __name__ == "__main__":
    _demo()
