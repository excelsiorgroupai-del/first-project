#!/usr/bin/env python3
"""記帳小工具（Tkinter GUI）。"""

from __future__ import annotations

import json
import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Any

DATA_FILE = Path("records.json")


def load_records() -> list[dict[str, Any]]:
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_records(records: list[dict[str, Any]]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)


def add_record(amount: float, category: str, note: str, record_date: str) -> dict[str, Any]:
    if amount <= 0:
        raise ValueError("金額必須大於 0")

    record = {
        "date": record_date,
        "amount": round(amount, 2),
        "category": category.strip(),
        "note": note.strip(),
    }

    records = load_records()
    records.append(record)
    save_records(records)
    return record


def summary_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    total = sum(item["amount"] for item in records)

    by_category: dict[str, float] = {}
    for item in records:
        by_category[item["category"]] = by_category.get(item["category"], 0) + item["amount"]

    return {
        "count": len(records),
        "total": round(total, 2),
        "by_category": {k: round(v, 2) for k, v in sorted(by_category.items())},
    }


class LedgerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("記帳小工具")
        self.root.geometry("760x520")

        self.amount_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.note_var = tk.StringVar()
        self.date_var = tk.StringVar(value=date.today().isoformat())

        self._build_form()
        self._build_table()
        self._build_summary()
        self.refresh_view()

    def _build_form(self) -> None:
        form = ttk.LabelFrame(self.root, text="新增記帳")
        form.pack(fill="x", padx=12, pady=12)

        ttk.Label(form, text="日期 (YYYY-MM-DD)").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        ttk.Entry(form, textvariable=self.date_var, width=18).grid(row=0, column=1, padx=8, pady=6)

        ttk.Label(form, text="分類").grid(row=0, column=2, sticky="w", padx=8, pady=6)
        ttk.Entry(form, textvariable=self.category_var, width=18).grid(row=0, column=3, padx=8, pady=6)

        ttk.Label(form, text="金額").grid(row=1, column=0, sticky="w", padx=8, pady=6)
        ttk.Entry(form, textvariable=self.amount_var, width=18).grid(row=1, column=1, padx=8, pady=6)

        ttk.Label(form, text="備註").grid(row=1, column=2, sticky="w", padx=8, pady=6)
        ttk.Entry(form, textvariable=self.note_var, width=18).grid(row=1, column=3, padx=8, pady=6)

        ttk.Button(form, text="➕ 新增記錄", command=self.on_add).grid(
            row=0, column=4, rowspan=2, padx=10, pady=6, sticky="ns"
        )

    def _build_table(self) -> None:
        frame = ttk.LabelFrame(self.root, text="記錄列表")
        frame.pack(fill="both", expand=True, padx=12, pady=4)

        columns = ("date", "category", "amount", "note")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)

        self.tree.heading("date", text="日期")
        self.tree.heading("category", text="分類")
        self.tree.heading("amount", text="金額")
        self.tree.heading("note", text="備註")

        self.tree.column("date", width=140, anchor="center")
        self.tree.column("category", width=130, anchor="center")
        self.tree.column("amount", width=100, anchor="e")
        self.tree.column("note", width=320, anchor="w")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _build_summary(self) -> None:
        footer = ttk.Frame(self.root)
        footer.pack(fill="x", padx=12, pady=10)

        self.summary_label = ttk.Label(footer, text="總筆數：0   總金額：$0.00", font=("Arial", 11, "bold"))
        self.summary_label.pack(side="left")

        ttk.Button(footer, text="🔄 重新整理", command=self.refresh_view).pack(side="right")

    def refresh_view(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = load_records()
        for record in records:
            self.tree.insert(
                "",
                "end",
                values=(record["date"], record["category"], f"${record['amount']:.2f}", record["note"]),
            )

        summary = summary_records(records)
        self.summary_label.config(text=f"總筆數：{summary['count']}   總金額：${summary['total']:.2f}")

    def on_add(self) -> None:
        record_date = self.date_var.get().strip()
        category = self.category_var.get().strip()
        note = self.note_var.get().strip()
        amount_text = self.amount_var.get().strip()

        if not category:
            messagebox.showerror("輸入錯誤", "請輸入分類")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror("輸入錯誤", "金額請輸入數字")
            return

        try:
            add_record(amount=amount, category=category, note=note, record_date=record_date)
        except ValueError as error:
            messagebox.showerror("輸入錯誤", str(error))
            return

        self.amount_var.set("")
        self.note_var.set("")
        self.refresh_view()
        messagebox.showinfo("完成", "已成功新增記錄")


def main() -> None:
    root = tk.Tk()
    LedgerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
