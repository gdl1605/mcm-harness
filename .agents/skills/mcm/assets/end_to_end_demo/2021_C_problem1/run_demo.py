"""
2021 C 题问题一最小贯通 demo。
读什么：sample_suppliers.csv 中的候选供应商特征。
输出什么：outputs/top50_suppliers_demo.csv，即 Top-k 供应商排序表示例。
判定规则：熵权 TOPSIS 得分越高，候选优先级越高。
这不是：完整 2021 C 题复现，也不是 24 周订购/转运矩阵生成器。
证据等级：[中频经验]；证据来源：2021 C066/C169/C283 与跨年份回归中的 Top50 表要求。
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Mapping, Sequence

ROOT = Path(__file__).resolve().parent
SNIPPETS = ROOT.parents[1] / "snippets"
sys.path.insert(0, str(SNIPPETS))

from entropy_topsis import fit_rank  # noqa: E402


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(row) for row in csv.DictReader(f)]


def write_rows(rows: Sequence[Mapping[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    input_path = ROOT / "sample_suppliers.csv"
    output_path = ROOT / "outputs" / "top50_suppliers_demo.csv"
    rows = read_rows(input_path)
    ranking = fit_rank(
        rows,
        indicators=["total_supply", "stability_rate", "material_importance", "loss_rate"],
        id_col="supplier",
        directions={
            "total_supply": "positive",
            "stability_rate": "positive",
            "material_importance": "positive",
            "loss_rate": "negative",
        },
        top_k=50,
    )
    write_rows(ranking, output_path)
    print(f"已导出：{output_path}")


if __name__ == "__main__":
    main()
