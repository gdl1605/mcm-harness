"""
线性规划最小骨架 snippet。

适用题型：确定性优化/决策、资源配置、订购/运输/排班等可线性表达的问题。
证据等级：[高频共性]
主要证据来源：references/distill/modeling-playbook.md Route C；references/distill/evidence-map.md 中 2021 与 2024 优化题经验。
触发条件：题目能写成变量、目标函数、线性约束，并需要最终方案表。
非目标：不是通用求解器封装；不是多场景鲁棒优化系统；不是自动建模器。
最小输入：变量列表、目标系数、约束列表、变量上下界。
最小输出：决策变量表、目标值、可行性状态。
"""

from __future__ import annotations

import itertools
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

Constraint = Mapping[str, object]


def _frange(low: float, high: float, step: float) -> Iterable[float]:
    current = low
    # 为比赛骨架保留可读性，避免浮点边界漏掉上界。
    while current <= high + step * 1e-9:
        yield round(current, 10)
        current += step


def _satisfy(value: float, sense: str, rhs: float, tol: float = 1e-8) -> bool:
    if sense == "<=":
        return value <= rhs + tol
    if sense == ">=":
        return value >= rhs - tol
    if sense in {"=", "=="}:
        return abs(value - rhs) <= tol
    raise ValueError(f"未知约束方向：{sense}")


def solve_grid_lp(
    variables: Sequence[str],
    objective: Mapping[str, float],
    constraints: Sequence[Constraint],
    bounds: Mapping[str, Tuple[float, float]],
    maximize: bool = True,
    step: float = 1.0,
) -> Dict[str, object]:
    """小规模可运行 LP 骨架：用网格枚举打通变量-目标-约束-结果表。"""
    grids = [_frange(bounds[var][0], bounds[var][1], step) for var in variables]
    best_values = None
    best_obj = None
    feasible_count = 0

    for candidate in itertools.product(*grids):
        values = dict(zip(variables, candidate))
        feasible = True
        for constraint in constraints:
            coeffs = constraint["coeffs"]
            lhs = sum(float(coeffs.get(var, 0.0)) * values[var] for var in variables)
            if not _satisfy(lhs, str(constraint["sense"]), float(constraint["rhs"])):
                feasible = False
                break
        if not feasible:
            continue
        feasible_count += 1
        obj = sum(float(objective.get(var, 0.0)) * values[var] for var in variables)
        if best_obj is None or (maximize and obj > best_obj) or ((not maximize) and obj < best_obj):
            best_obj = obj
            best_values = values

    status = "optimal_on_grid" if best_values is not None else "infeasible_on_grid"
    decision_table = [
        {"variable": var, "value": best_values[var] if best_values else None}
        for var in variables
    ]
    return {
        "status": status,
        "objective_value": best_obj,
        "feasible_count": feasible_count,
        "decision_table": decision_table,
    }


if __name__ == "__main__":
    result = solve_grid_lp(
        variables=["x1", "x2"],
        objective={"x1": 5, "x2": 4},
        constraints=[
            {"name": "resource_a", "coeffs": {"x1": 6, "x2": 4}, "sense": "<=", "rhs": 24},
            {"name": "resource_b", "coeffs": {"x1": 1, "x2": 2}, "sense": "<=", "rhs": 6},
        ],
        bounds={"x1": (0, 10), "x2": (0, 10)},
        maximize=True,
        step=1,
    )
    print(result)
