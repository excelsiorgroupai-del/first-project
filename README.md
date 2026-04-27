# first-project

這是一個用 Python 製作的「記帳小工具」CLI 程式。

## 功能

- 新增支出記錄
- 查看所有記錄
- 查看總結（總金額與分類統計）

## 使用方式

```bash
python3 ledger.py add 120 餐飲 午餐
python3 ledger.py add 45 交通 公車
python3 ledger.py list
python3 ledger.py summary
```

## 資料儲存

- 會自動儲存在專案根目錄的 `records.json`
- 使用 JSON 格式，方便閱讀與備份

## 指令說明

### 1) 新增記錄

```bash
python3 ledger.py add <金額> <分類> [備註] --date <YYYY-MM-DD>
```

- `--date` 可省略，預設為今天日期

### 2) 列出記錄

```bash
python3 ledger.py list
```

### 3) 顯示摘要

```bash
python3 ledger.py summary
```
