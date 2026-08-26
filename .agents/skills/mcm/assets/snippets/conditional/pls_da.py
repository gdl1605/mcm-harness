"""
PLS-DA 高维成分判别条件触发 snippet。

适用题型：成分判别、组别区分、高维强共线特征下的分类解释。
证据等级：[中频经验]
主要证据来源：references/distill/evidence-map.md 中 2022 C229/C155；references/distill/modeling-playbook.md Route D；分类题“先特征筛选，再判别，并给变量重要度/可分性展示”的中频经验。
触发条件：样本有明确标签；特征维度较高或强共线；题目不仅要分类结果，还要解释哪些变量区分类别。
何时不建议使用：低维普通表格分类、无标签聚类题、强非线性且无需解释变量重要度、样本极少且类别不可分时。
非目标：不是默认 tabular 分类器；不是所有分类题第一选择；不是化学成分完整专用管线；不是替代 LightGBM/普通特征筛选的万能方案。
最小输入：样本特征矩阵、标签列、样本 ID，可选成分数。
最小输出：sample_id -> true_label -> predicted_label 表、feature -> VIP/importance 表、可分性摘要。
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np

Row = Mapping[str, Any]


def _as_matrix(rows: Sequence[Row], feature_cols: Sequence[str]) -> np.ndarray:
    return np.array([[float(row[col]) for col in feature_cols] for row in rows], dtype=float)


def _standardize(x: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = x.mean(axis=0)
    std = x.std(axis=0, ddof=0)
    std[std == 0] = 1.0
    return (x - mean) / std, mean, std


def _one_hot(labels: Sequence[Any]) -> Tuple[np.ndarray, List[Any]]:
    classes = sorted(set(labels), key=lambda item: str(item))
    encoded = np.zeros((len(labels), len(classes)))
    for i, label in enumerate(labels):
        encoded[i, classes.index(label)] = 1.0
    return encoded, classes


def fit_pls_da(
    rows: Sequence[Row],
    feature_cols: Sequence[str],
    label_col: str,
    sample_id_col: Optional[str] = None,
    n_components: int = 2,
) -> Dict[str, Any]:
    """最小 PLS-DA 风格基线：用 X-Y 协方差 SVD 得到潜变量，再做最小二乘分类。"""
    if not rows:
        raise ValueError("rows 不能为空")
    if n_components < 1:
        raise ValueError("n_components 必须 >= 1")

    labels = [row[label_col] for row in rows]
    x_raw = _as_matrix(rows, feature_cols)
    x_scaled, x_mean, x_std = _standardize(x_raw)
    y, classes = _one_hot(labels)
    y_centered = y - y.mean(axis=0)

    cross_cov = x_scaled.T @ y_centered
    weights, singular_values, _ = np.linalg.svd(cross_cov, full_matrices=False)
    n_components = min(n_components, weights.shape[1])
    weights = weights[:, :n_components]
    singular_values = singular_values[:n_components]

    scores = x_scaled @ weights
    coef, *_ = np.linalg.lstsq(scores, y, rcond=None)
    y_score = scores @ coef
    pred_idx = np.argmax(y_score, axis=1)
    predictions = [classes[i] for i in pred_idx]

    ids = [row.get(sample_id_col, idx) if sample_id_col else idx for idx, row in enumerate(rows)]
    classification_table = [
        {
            "sample_id": ids[i],
            "true_label": labels[i],
            "predicted_label": predictions[i],
            "is_correct": labels[i] == predictions[i],
        }
        for i in range(len(rows))
    ]

    vip_table = _vip_table(feature_cols, weights, singular_values)
    accuracy = sum(row["is_correct"] for row in classification_table) / len(classification_table)
    separability_summary = {
        "n_samples": len(rows),
        "n_features": len(feature_cols),
        "n_classes": len(classes),
        "n_components": n_components,
        "training_accuracy_baseline": accuracy,
        "note": "该准确率仅用于赛时基线检查，正式论文应补验证集或交叉验证。",
    }

    return {
        "classes": classes,
        "feature_cols": list(feature_cols),
        "x_mean": x_mean,
        "x_std": x_std,
        "weights": weights,
        "coef": coef,
        "classification_table": classification_table,
        "vip_table": vip_table,
        "separability_summary": separability_summary,
    }


def _vip_table(feature_cols: Sequence[str], weights: np.ndarray, singular_values: np.ndarray) -> List[Dict[str, Any]]:
    p = len(feature_cols)
    if singular_values.size == 0 or np.isclose(np.sum(singular_values ** 2), 0.0):
        importance = np.ones(p)
    else:
        importance = np.sqrt(p * ((weights ** 2) @ (singular_values ** 2)) / np.sum(singular_values ** 2))
    rows = [
        {"feature": feature_cols[i], "vip_like_importance": float(importance[i])}
        for i in range(p)
    ]
    return sorted(rows, key=lambda row: row["vip_like_importance"], reverse=True)


def predict_pls_da(model: Mapping[str, Any], rows: Sequence[Row]) -> List[Dict[str, Any]]:
    """用已拟合模型给新样本分类；rows 需包含训练时相同特征列。"""
    feature_cols = model["feature_cols"]
    x = _as_matrix(rows, feature_cols)
    x_scaled = (x - model["x_mean"]) / model["x_std"]
    scores = x_scaled @ model["weights"]
    y_score = scores @ model["coef"]
    pred_idx = np.argmax(y_score, axis=1)
    classes = model["classes"]
    return [{"row_index": i, "predicted_label": classes[idx]} for i, idx in enumerate(pred_idx)]


def conclusion_hint(result: Mapping[str, Any], top_n: int = 3) -> str:
    """给论文结果段一个可改写的中文结论句。"""
    summary = result["separability_summary"]
    top_features = ", ".join(row["feature"] for row in result["vip_table"][:top_n])
    return (
        f"PLS-DA 基线显示，前 {top_n} 个区分类别的重要变量为 {top_features}；"
        f"当前训练内判别一致率为 {summary['training_accuracy_baseline']:.2%}，正式结果仍需结合验证集或交叉验证解释。"
    )


def _demo() -> None:
    rows = [
        {"id": "S1", "label": "A", "f1": 1.0, "f2": 0.9, "f3": 0.2, "f4": 0.1},
        {"id": "S2", "label": "A", "f1": 1.1, "f2": 1.0, "f3": 0.3, "f4": 0.2},
        {"id": "S3", "label": "B", "f1": 0.2, "f2": 0.3, "f3": 1.0, "f4": 1.1},
        {"id": "S4", "label": "B", "f1": 0.3, "f2": 0.2, "f3": 1.1, "f4": 1.0},
    ]
    result = fit_pls_da(rows, ["f1", "f2", "f3", "f4"], "label", sample_id_col="id", n_components=2)
    print("classification_table:", result["classification_table"])
    print("vip_table:", result["vip_table"])
    print("summary:", result["separability_summary"])
    print(conclusion_hint(result))


if __name__ == "__main__":
    _demo()
