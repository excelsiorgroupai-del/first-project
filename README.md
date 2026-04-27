# first-project

codex/create-a-budgeting-tool-program-3tbiit
這是一個用 Python tkinter 製作的「記帳小工具」GUI 程式。

## 功能

- 使用視窗介面輸入日期、分類、金額、備註
- 點按按鈕即可新增記錄（不需要終端機參數）
- 表格顯示所有歷史記錄
- 顯示總筆數與總金額
- 資料會自動儲存到 `records.json`

## 啟動方式

```bash
python3 ledger.py
```

## 使用步驟

1. 啟動程式後，在上方輸入欄位填入：日期、分類、金額、備註。
2. 點擊「➕ 新增記錄」按鈕。
3. 新增成功後，清單會立即更新，底部也會更新總筆數與總金額。
4. 如需重新載入資料，可按「🔄 重新整理」。

## 注意事項

- 金額必須是數字且大於 0。
- 分類不可空白。
- 日期預設為今天（格式 `YYYY-MM-DD`）。
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
main
