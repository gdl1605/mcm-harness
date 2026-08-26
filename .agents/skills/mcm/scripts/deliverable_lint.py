#!/usr/bin/env python3
"""
读什么：一个比赛工作目录或若干输出文件。
输出什么：计算与答卷资产的存在性提示，可选 JSON。
判定规则：只检查 baseline、最终答案类文件和验证痕迹是否出现。
这不是：论文质量判断、摘要完整性判断、语义判卷器或自动修复器。
证据来源：references/output-contracts.md。论文写作和评委审读必须使用语义 references，不能由本脚本判定。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

TEXT_SUFFIXES = {".md", ".txt", ".csv", ".tsv", ".py", ".json"}

CHECKS = {
    "baseline/结果表痕迹": ["baseline", "基线", "结果表", "result"],
    "final answer artifact": ["final answer artifact", "最终推荐表", "最终排序表", "最终判定表", "方案表", "Top50"],
    "验证或稳健性": ["验证", "稳健性", "灵敏度", "baseline", "对照"],
}


def iter_files(paths: Sequence[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            yield path
        elif path.is_dir():
            for child in path.rglob("*"):
                if child.is_file() and child.suffix in TEXT_SUFFIXES:
                    yield child


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def run_checks(paths: Sequence[Path]) -> Dict[str, object]:
    files = list(iter_files(paths))
    combined = "\n".join(read_text(path) for path in files)
    details = []
    for name, keywords in CHECKS.items():
        hit = any(keyword in combined for keyword in keywords)
        details.append({"检查项": name, "通过": hit, "提示": "已发现相关交付痕迹" if hit else f"缺少关键词：{', '.join(keywords)}"})
    return {
        "扫描文件数": len(files),
        "通过": all(item["通过"] for item in details),
        "检查结果": details,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="检查数学建模目录是否存在基本计算与答卷资产；不评价论文语义质量。")
    parser.add_argument("paths", nargs="+", help="要检查的目录或文件")
    parser.add_argument("--json", action="store_true", help="输出 JSON 而不是中文文本")
    args = parser.parse_args()

    report = run_checks([Path(p) for p in args.paths])
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"扫描文件数：{report['扫描文件数']}")
        for item in report["检查结果"]:
            mark = "通过" if item["通过"] else "缺口"
            print(f"[{mark}] {item['检查项']}：{item['提示']}")
        print("总体结论：" + ("基本资产痕迹已找到，仍需语义审查" if report["通过"] else "基本计算或答卷资产可能缺失"))
    return 0 if report["通过"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
