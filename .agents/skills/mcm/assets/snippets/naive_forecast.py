"""
短期预测 baseline snippet。

适用题型：短期需求、销量、供给、价格等运营预测，并常作为下游决策模型输入。
证据等级：[高频共性]
主要证据来源：references/distill/modeling-playbook.md Route B1；references/distill/evidence-map.md 中 2023 C050；跨年份回归中“先给 7 天方案表”的结论。
触发条件：题目需要未来几天/几周预测，且先要一个可解释、可验证的 baseline。
非目标：不是完整时序库；不是 ARIMA/深度模型大全；不是需求校正系统。
最小输入：日期、对象、目标值三列构成的历史序列表。
最小输出：日期-对象-预测值表、可选误差摘要表。
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime
from typing import Dict, Iterable, List, Mapping, Sequence


def _parse_date(value: object) -> date:
    if isinstance(value, date):
        return value
    return datetime.strptime(str(value), "%Y-%m-%d").date()


def _group_history(rows: Sequence[Mapping[str, object]], date_key: str, id_key: str, value_key: str) -> Dict[object, List[Dict[str, object]]]:
    grouped: Dict[object, List[Dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[row[id_key]].append({"date": _parse_date(row[date_key]), "value": float(row[value_key])})
    for values in grouped.values():
        values.sort(key=lambda item: item["date"])
    return grouped


def recent_value_forecast(
    rows: Sequence[Mapping[str, object]],
    future_dates: Sequence[object],
    date_key: str = "date",
    id_key: str = "object",
    value_key: str = "value",
) -> List[Dict[str, object]]:
    """最近值 baseline：适合先形成可交付预测表。"""
    grouped = _group_history(rows, date_key, id_key, value_key)
    forecasts: List[Dict[str, object]] = []
    for obj, history in grouped.items():
        last_value = history[-1]["value"]
        for future_date in future_dates:
            forecasts.append({"date": str(_parse_date(future_date)), "object": obj, "forecast": last_value, "method": "recent_value"})
    return forecasts


def moving_average_forecast(
    rows: Sequence[Mapping[str, object]],
    future_dates: Sequence[object],
    window: int = 3,
    date_key: str = "date",
    id_key: str = "object",
    value_key: str = "value",
) -> List[Dict[str, object]]:
    """移动平均 baseline：适合短窗口运营预测。"""
    grouped = _group_history(rows, date_key, id_key, value_key)
    forecasts: List[Dict[str, object]] = []
    for obj, history in grouped.items():
        values = [item["value"] for item in history[-window:]]
        avg_value = sum(values) / len(values)
        for future_date in future_dates:
            forecasts.append({"date": str(_parse_date(future_date)), "object": obj, "forecast": avg_value, "method": f"ma_{window}"})
    return forecasts


def weekday_average_forecast(
    rows: Sequence[Mapping[str, object]],
    future_dates: Sequence[object],
    fallback_window: int = 3,
    date_key: str = "date",
    id_key: str = "object",
    value_key: str = "value",
) -> List[Dict[str, object]]:
    """星期效应 baseline：当销售/需求有明显周内节律时使用。"""
    grouped = _group_history(rows, date_key, id_key, value_key)
    forecasts: List[Dict[str, object]] = []
    for obj, history in grouped.items():
        by_weekday: Dict[int, List[float]] = defaultdict(list)
        for item in history:
            by_weekday[item["date"].weekday()].append(float(item["value"]))
        fallback_values = [float(item["value"]) for item in history[-fallback_window:]]
        fallback = sum(fallback_values) / len(fallback_values)
        for future_date in future_dates:
            dt = _parse_date(future_date)
            values = by_weekday.get(dt.weekday(), [])
            forecast = sum(values) / len(values) if values else fallback
            forecasts.append({"date": str(dt), "object": obj, "forecast": forecast, "method": "weekday_average"})
    return forecasts


if __name__ == "__main__":
    demo_rows = [
        {"date": "2026-01-01", "object": "品类A", "value": 100},
        {"date": "2026-01-02", "object": "品类A", "value": 110},
        {"date": "2026-01-03", "object": "品类A", "value": 105},
        {"date": "2026-01-01", "object": "品类B", "value": 80},
        {"date": "2026-01-02", "object": "品类B", "value": 86},
        {"date": "2026-01-03", "object": "品类B", "value": 82},
    ]
    for row in moving_average_forecast(demo_rows, ["2026-01-04", "2026-01-05"], window=2):
        print(row)
