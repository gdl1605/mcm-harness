"""
数学建模比赛数据预处理骨架 snippet。

适用题型：几乎所有数据驱动题；尤其是面板数据、运营流水、模板型题和需要 proxy target 的问题。
证据等级：[高频共性]
主要证据来源：references/distill/modeling-playbook.md 3.1/3.2；references/distill/evidence-map.md 中 2021/2023/2025 的粒度、结构性 0 与多时点证据。
触发条件：拿到原始数据后，尚未锁定主键、时间轴、结构性 0、特征表和导出路径。
非目标：不是自动 EDA 平台；不是万能缺失值修复器；不是特定题目的清洗代码。
最小输入：原始行表、主键、时间列、目标列或字段字典。
最小输出：clean_master_table、feature_table、处理日志。
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence

Row = MutableMapping[str, object]


def read_csv_table(path: str | Path) -> List[Row]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(row) for row in csv.DictReader(f)]


def write_csv_table(rows: Sequence[Mapping[str, object]], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def standardize_columns(rows: Sequence[Mapping[str, object]], rename_map: Mapping[str, str]) -> List[Row]:
    """统一列名，避免后续模型脚本混用中文/英文/别名字段。"""
    out: List[Row] = []
    for row in rows:
        new_row: Row = {}
        for key, value in row.items():
            new_row[rename_map.get(key, key)] = value
        out.append(new_row)
    return out


def add_missing_and_zero_flags(
    rows: Sequence[Mapping[str, object]],
    value_cols: Sequence[str],
    structural_zero_cols: Optional[Sequence[str]] = None,
) -> List[Row]:
    """区分缺失值和结构性 0；这是 ranking/forecast/optimization 前的高频风险点。"""
    structural_zero_cols = set(structural_zero_cols or [])
    out: List[Row] = []
    for row in rows:
        new_row = dict(row)
        for col in value_cols:
            value = row.get(col)
            new_row[f"{col}_is_missing"] = value in {None, ""}
            new_row[f"{col}_is_structural_zero"] = col in structural_zero_cols and str(value) in {"0", "0.0"}
        out.append(new_row)
    return out


def aggregate_numeric(
    rows: Sequence[Mapping[str, object]],
    group_keys: Sequence[str],
    value_cols: Sequence[str],
) -> List[Row]:
    """按主键/时间粒度聚合，为特征表或优化参数表做准备。"""
    grouped: Dict[tuple, Dict[str, float]] = defaultdict(lambda: {col: 0.0 for col in value_cols})
    counts: Dict[tuple, int] = defaultdict(int)
    for row in rows:
        key = tuple(row[k] for k in group_keys)
        counts[key] += 1
        for col in value_cols:
            value = row.get(col)
            if value in {None, ""}:
                continue
            grouped[key][col] += float(value)
    out: List[Row] = []
    for key, sums in grouped.items():
        current: Row = {group_keys[idx]: key[idx] for idx in range(len(group_keys))}
        for col in value_cols:
            current[f"{col}_sum"] = sums[col]
            current[f"{col}_mean"] = sums[col] / counts[key]
        current["row_count"] = counts[key]
        out.append(current)
    return out


def run_preprocessing(
    raw_rows: Sequence[Mapping[str, object]],
    id_key: str,
    value_cols: Sequence[str],
    time_key: Optional[str] = None,
    rename_map: Optional[Mapping[str, str]] = None,
    structural_zero_cols: Optional[Sequence[str]] = None,
) -> Dict[str, object]:
    """最小预处理通路：列名统一 -> 缺失/结构性 0 标记 -> 特征表。"""
    clean = standardize_columns(raw_rows, rename_map or {})
    clean = add_missing_and_zero_flags(clean, value_cols, structural_zero_cols)
    group_keys = [id_key] + ([time_key] if time_key else [])
    feature_table = aggregate_numeric(clean, group_keys=group_keys, value_cols=value_cols)
    log = [
        f"主键：{id_key}",
        f"时间轴：{time_key or '无显式时间轴'}",
        f"数值字段：{', '.join(value_cols)}",
        f"结构性 0 字段：{', '.join(structural_zero_cols or []) or '未指定'}",
        "proxy target 说明：若目标列不是题目真实目标，必须在建模说明中标注为替代目标。",
    ]
    return {"clean_master_table": clean, "feature_table": feature_table, "process_log": log}


if __name__ == "__main__":
    demo = [
        {"supplier": "S1", "week": "1", "amount": "10"},
        {"supplier": "S1", "week": "2", "amount": ""},
        {"supplier": "S2", "week": "1", "amount": "0"},
    ]
    result = run_preprocessing(demo, id_key="supplier", time_key="week", value_cols=["amount"], structural_zero_cols=["amount"])
    print(result["process_log"])
    print(result["feature_table"])
