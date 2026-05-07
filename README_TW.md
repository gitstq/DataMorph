<p align="center">
  <a href="README.md">简体中文</a> | 
  <a href="README_EN.md">English</a> | 
  <a href="README_TW.md">繁體中文</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/dependencies-0-brightgreen.svg" alt="Dependencies">
</p>

<h1 align="center">🔄 DataMorph</h1>

<p align="center">
  <b>輕量級終端數據處理瑞士刀</b>
</p>

<p align="center">
  零依賴 CLI 工具，支援 JSON / YAML / TOML / CSV 數據處理
</p>

---

## 🎉 專案介紹

**DataMorph** 是一款專為開發者設計的輕量級終端數據處理工具。它解決了日常開發中頻繁切換不同數據格式、手動解析和轉換數據的痛點。

### 💡 設計靈感

在日常開發中，我們經常需要處理各種格式的設定檔和數據：JSON 設定、YAML 清單、TOML 設置、CSV 數據表。每次都需要安裝不同的工具或編寫臨時腳本來處理這些格式。DataMorph 旨在提供一個統一的命令列工具，讓數據處理變得簡單高效。

### ✨ 自研差異化亮點

- 🚀 **零外部依賴** - 完全使用 Python 標準庫實現，無需安裝任何第三方套件
- 🔄 **多格式互轉** - 支援 JSON、YAML、TOML、CSV 四種格式的相互轉換
- 🔍 **強大查詢引擎** - 類 JMESPath 語法，支援複雜過濾和嵌套查詢
- 🎨 **美化輸出** - 表格、樹形、彩色高亮多種輸出格式
- 📊 **串流處理** - 支援管道操作，可處理大檔案
- ⚡ **單檔案執行** - 可打包為單個可執行檔，無需 Python 環境

---

## ✨ 核心特性

### 📦 格式轉換

```bash
# JSON 轉 YAML
datamorph convert config.json config.yaml

# YAML 轉 TOML
datamorph convert settings.yaml settings.toml

# CSV 轉 JSON
datamorph convert data.csv data.json

# 從標準輸入讀取
cat data.json | datamorph convert - output.yaml -t yaml
```

### 🔍 數據查詢

```bash
# 查詢嵌套欄位
datamorph query 'users[0].name' < users.json

# 過濾陣列
datamorph query 'users[?age > 25]' < users.json

# 萬用字元查詢
datamorph query 'items[*].price' < products.json
```

### 📊 格式化輸出

```bash
# 表格格式
datamorph table users.csv

# 樹形結構
datamorph tree config.json

# 彩色 JSON
datamorph pretty data.json
```

### ✅ 數據驗證

```bash
# 驗證 JSON
datamorph validate config.json

# 驗證 YAML
datamorph validate settings.yaml -f yaml
```

### 📈 數據資訊

```bash
# 查看數據結構資訊
datamorph info data.json
```

---

## 🚀 快速開始

### 📋 環境要求

- Python 3.8 或更高版本
- 無需任何外部依賴

### 📥 安裝方式

#### 方式一：從原始碼安裝

```bash
# 複製儲存庫
git clone https://github.com/gitstq/DataMorph.git

# 進入目錄
cd DataMorph

# 安裝
pip install -e .
```

#### 方式二：直接執行

```bash
# 無需安裝，直接執行
python -m datamorph.cli --help
```

### 🎮 基本使用

```bash
# 查看幫助
datamorph --help

# 轉換格式
datamorph convert input.json output.yaml

# 查詢數據
echo '{"users": [{"name": "Alice", "age": 30}]}' | datamorph query 'users[0].name'

# 格式化輸出
datamorph table data.csv
```

---

## 📖 詳細使用指南

### 🔄 convert 命令

在多種數據格式之間進行轉換：

```bash
datamorph convert <input> <output> [options]

# 參數說明
# input   - 輸入檔案路徑（使用 - 從標準輸入讀取）
# output  - 輸出檔案路徑（使用 - 輸出到標準輸出）

# 選項
# -f, --from  - 輸入格式（json/yaml/toml/csv），自動檢測
# -t, --to    - 輸出格式（json/yaml/toml/csv），必需

# 範例
datamorph convert config.json config.yaml -t yaml
datamorph convert data.csv data.json -t json
cat input.yaml | datamorph convert - - -f yaml -t json
```

### 🔍 query 命令

使用表達式查詢數據：

```bash
datamorph query <expression> [options]

# 查詢語法
# .field       - 訪問欄位
# [0]          - 陣列索引
# [start:end]  - 陣列切片
# [?condition] - 過濾條件
# [*]          - 萬用字元

# 支援的比較運算子
# ==, !=, <, >, <=, >=
# contains, starts_with, ends_with

# 範例
datamorph query 'users[0].name' < data.json
datamorph query 'items[?price > 100]' < products.json
datamorph query 'users[?age >= 25 && status == "active"]' < users.json
```

### 📊 table 命令

將數據格式化為表格：

```bash
datamorph table [input] [options]

# 選項
# -f, --format  - 輸入格式
# -c, --columns - 顯示的欄位（逗號分隔）
# -w, --width   - 最大表格寬度

# 範例
datamorph table users.csv
datamorph table data.json -c name,age,email
datamorph table products.json -w 150
```

### 🌳 tree 命令

將數據格式化為樹形結構：

```bash
datamorph tree [input] [options]

# 選項
# -f, --format - 輸入格式
# -d, --depth  - 最大深度

# 範例
datamorph tree config.json
datamorph tree data.yaml -d 3
```

### 💅 pretty 命令

美化 JSON 輸出：

```bash
datamorph pretty [input] [options]

# 選項
# -i, --indent   - 縮排空格數（預設 2）
# -o, --output   - 輸出檔案
# --no-color     - 停用彩色輸出

# 範例
datamorph pretty data.json
datamorph pretty input.json -o output.json -i 4
```

### 🗜️ minify 命令

壓縮 JSON：

```bash
datamorph minify [input] [options]

# 範例
datamorph minify data.json
datamorph minify input.json -o minified.json
```

### ✅ validate 命令

驗證數據格式：

```bash
datamorph validate <input> [options]

# 選項
# -f, --format - 指定格式

# 範例
datamorph validate config.json
datamorph validate settings.yaml -f yaml
```

---

## 💡 設計思路與迭代規劃

### 🏗️ 技術選型

| 元件 | 選擇 | 理由 |
|------|------|------|
| 語言 | Python 3.8+ | 標準庫豐富，跨平台相容 |
| CLI 框架 | argparse | 內建支援，零依賴 |
| YAML 解析 | 自研實現 | 無需 PyYAML 依賴 |
| TOML 解析 | 自研實現 | 無需 tomli 依賴 |
| 輸出美化 | ANSI 轉義碼 | 無需第三方函式庫 |

### 📅 後續迭代計劃

- [ ] 支援 XML 格式
- [ ] 加入 JSON Schema 驗證
- [ ] 支援更多查詢語法
- [ ] 加入數據合併功能
- [ ] 支援遠端 URL 讀取
- [ ] 提供 Web API 介面
- [ ] 打包為獨立可執行檔

---

## 📦 打包與部署指南

### 🐍 PyPI 發布

```bash
# 建構
python setup.py sdist bdist_wheel

# 上傳
twine upload dist/*
```

### 📦 獨立可執行檔

使用 PyInstaller 打包：

```bash
# 安裝 PyInstaller
pip install pyinstaller

# 打包
pyinstaller --onefile --name datamorph datamorph/cli.py

# 輸出在 dist/ 目錄
```

---

## 🤝 貢獻指南

歡迎所有形式的貢獻！

### 📝 提交規範

我們使用 Angular 提交規範：

- `feat:` 新功能
- `fix:` 修復問題
- `docs:` 文檔更新
- `refactor:` 程式碼重構
- `test:` 測試相關
- `chore:` 建構/工具相關

### 🔀 提交流程

1. Fork 本儲存庫
2. 建立特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 建立 Pull Request

---

## 📄 開源協議說明

本專案採用 [MIT License](LICENSE) 開源協議。

這意味著您可以：
- ✅ 商業使用
- ✅ 修改程式碼
- ✅ 分發程式碼
- ✅ 私人使用

唯一要求是保留版權聲明和授權條款副本。

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>
