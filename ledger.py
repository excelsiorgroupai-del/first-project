#!/usr/bin/env python3
"""簡單記帳小工具（CLI）。"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

DATA_FILE = Path("records.json")


def load_records() -> list[dict[str, Any]]:
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_records(records: list[dict[str, Any]]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def add_record(amount: float, category: str, note: str, record_date: str) -> dict[str, Any]:
    if amount <= 0:
        raise ValueError("金額必須大於 0")

    record = {
        "date": record_date,
        "amount": round(amount, 2),
        "category": category,
        "note": note,
    }

    records = load_records()
    records.append(record)
    save_records(records)
    return record


def list_records() -> list[dict[str, Any]]:
    return load_records()


def summary_records() -> dict[str, Any]:
    records = load_records()
    total = sum(item["amount"] for item in records)

    by_category: dict[str, float] = {}
    for item in records:
        by_category[item["category"]] = by_category.get(item["category"], 0) + item["amount"]

    return {
        "count": len(records),
        "total": round(total, 2),
        "by_category": {k: round(v, 2) for k, v in sorted(by_category.items())},
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="記帳小工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="新增一筆支出")
    add_parser.add_argument("amount", type=float, help="金額（正數）")
    add_parser.add_argument("category", help="分類，例如：餐飲、交通、娛樂")
    add_parser.add_argument("note", nargs="?", default="", help="備註（可選）")
    add_parser.add_argument("--date", default=date.today().isoformat(), help="日期，格式 YYYY-MM-DD")

    subparsers.add_parser("list", help="列出所有記錄")
    subparsers.add_parser("summary", help="顯示支出摘要")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        record = add_record(args.amount, args.category, args.note, args.date)
        print(f"✅ 已新增：{record['date']} {record['category']} ${record['amount']:.2f} {record['note']}")
    elif args.command == "list":
        records = list_records()
        if not records:
            print("目前還沒有記錄。")
            return

        print("日期         分類      金額      備註")
        print("-" * 50)
        for item in records:
            print(f"{item['date']:<12} {item['category']:<8} ${item['amount']:<8.2f} {item['note']}")
    elif args.command == "summary":
        result = summary_records()
        print(f"總筆數：{result['count']}")
        print(f"總金額：${result['total']:.2f}")
        print("分類統計：")
        for category, amount in result["by_category"].items():
            print(f"  - {category}: ${amount:.2f}")


if __name__ == "__main__":
    main()
