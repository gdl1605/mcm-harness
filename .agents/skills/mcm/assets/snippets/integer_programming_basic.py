"""
整数/0-1 规划最小骨架 snippet。

适用题型：离散选择、入选/不入选、分配、周计划、矩阵填表等优化决策题。
证据等级：[高频共性]
主要证据来源：references/distill/modeling-playbook.md Route C；references/distill/evidence-map.md 中 2021/2024 离散决策与 0-1/整数规划经验。
触发条件：决策变量天然是整数、二元选择或有限集合取值。
非目标：不是 GA/SA 启发式；不是复杂整数规划库教程；不是完整业务约束全集。
最小输入：候选对象、目标收益、容量/资源约束、变量范围。
最小输出：对象-决策值表、目标值、可行性状态。
"""

from __future__ import annotations

import itertools
from typing import Dict, List, Mapping, Optional, Sequence, Tuple


def solve_binary_selection(
    items: Sequence[Mapping[str, object]],
    id_key: str,
    value_key: str,
    weight_key: str,
    capacity: float,
    min_items: int = 0,
    max_items: Optional[int] = None,
) -> Dict[str, object]:
    """二元选择骨架：从候选集中选若干对象，使收益最大且不超容量。"""
    n = len(items)
    max_items = n if max_items is None else max_items
    best_choice = None
    best_value = None

    for bits in itertools.product([0, 1], repeat=n):
        chosen_count = sum(bits)
        if chosen_count < min_items or chosen_count > max_items:
            continue
        total_weight = sum(float(item[weight_key]) * bit for item, bit in zip(items, bits))
        if total_weight > capacity:
            continue
        total_value = sum(float(item[value_key]) * bit for item, bit in zip(items, bits))
        if best_value is None or total_value > best_value:
            best_value = total_value
            best_choice = bits

    if best_choice is None:
        return {"status": "infeasible", "objective_value": None, "decision_table": []}

    decision_table = []
    for item, bit in zip(items, best_choice):
        decision_table.append({
            "object": item[id_key],
            "decision_value": bit,
            "selected": bool(bit),
            "value": float(item[value_key]),
            "weight": float(item[weight_key]),
        })
    return {"status": "optimal_by_enumeration", "objective_value": best_value, "decision_table": decision_table}


def solve_integer_grid(
    variables: Sequence[str],
    objective: Mapping[str, float],
    constraints: Sequence[Mapping[str, object]],
    bounds: Mapping[str, Tuple[int, int]],
    maximize: bool = True,
) -> Dict[str, object]:
    """整数变量网格骨架：适合小规模示范，真实比赛可替换为 scipy/pulp/ortools。"""
    ranges = [range(bounds[var][0], bounds[var][1] + 1) for var in variables]
    best_values = None
    best_obj = None
    for candidate in itertools.product(*ranges):
        values = dict(zip(variables, candidate))
        feasible = True
        for constraint in constraints:
            lhs = sum(float(constraint["coeffs"].get(var, 0.0)) * values[var] for var in variables)
            sense = str(constraint["sense"])
            rhs = float(constraint["rhs"])
            if (sense == "<=" and lhs > rhs) or (sense == ">=" and lhs < rhs) or (sense in {"=", "=="} and lhs != rhs):
                feasible = False
                break
        if not feasible:
            continue
        obj = sum(float(objective.get(var, 0.0)) * values[var] for var in variables)
        if best_obj is None or (maximize and obj > best_obj) or ((not maximize) and obj < best_obj):
            best_obj = obj
            best_values = values
    return {
        "status": "optimal_by_integer_grid" if best_values else "infeasible",
        "objective_value": best_obj,
        "decision_table": [{"variable": var, "decision_value": best_values[var] if best_values else None} for var in variables],
    }


if __name__ == "__main__":
    demo_items = [
        {"id": "A", "score": 10, "cost": 5},
        {"id": "B", "score": 8, "cost": 4},
        {"id": "C", "score": 7, "cost": 3},
    ]
    print(solve_binary_selection(demo_items, id_key="id", value_key="score", weight_key="cost", capacity=8))
