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
  <b>轻量级终端数据处理瑞士军刀</b>
</p>

<p align="center">
  零依赖 CLI 工具，支持 JSON / YAML / TOML / CSV 数据处理
</p>

---

## 🎉 项目介绍

**DataMorph** 是一款专为开发者设计的轻量级终端数据处理工具。它解决了日常开发中频繁切换不同数据格式、手动解析和转换数据的痛点。

### 💡 设计灵感

在日常开发中，我们经常需要处理各种格式的配置文件和数据：JSON 配置、YAML 清单、TOML 设置、CSV 数据表。每次都需要安装不同的工具或编写临时脚本来处理这些格式。DataMorph 旨在提供一个统一的命令行工具，让数据处理变得简单高效。

### ✨ 自研差异化亮点

- 🚀 **零外部依赖** - 完全使用 Python 标准库实现，无需安装任何第三方包
- 🔄 **多格式互转** - 支持 JSON、YAML、TOML、CSV 四种格式的相互转换
- 🔍 **强大查询引擎** - 类 JMESPath 语法，支持复杂过滤和嵌套查询
- 🎨 **美化输出** - 表格、树形、彩色高亮多种输出格式
- 📊 **流式处理** - 支持管道操作，可处理大文件
- ⚡ **单文件执行** - 可打包为单个可执行文件，无需 Python 环境

---

## ✨ 核心特性

### 📦 格式转换

```bash
# JSON 转 YAML
datamorph convert config.json config.yaml

# YAML 转 TOML
datamorph convert settings.yaml settings.toml

# CSV 转 JSON
datamorph convert data.csv data.json

# 从标准输入读取
cat data.json | datamorph convert - output.yaml -t yaml
```

### 🔍 数据查询

```bash
# 查询嵌套字段
datamorph query 'users[0].name' < users.json

# 过滤数组
datamorph query 'users[?age > 25]' < users.json

# 通配符查询
datamorph query 'items[*].price' < products.json
```

### 📊 格式化输出

```bash
# 表格格式
datamorph table users.csv

# 树形结构
datamorph tree config.json

# 彩色 JSON
datamorph pretty data.json
```

### ✅ 数据验证

```bash
# 验证 JSON
datamorph validate config.json

# 验证 YAML
datamorph validate settings.yaml -f yaml
```

### 📈 数据信息

```bash
# 查看数据结构信息
datamorph info data.json
```

---

## 🚀 快速开始

### 📋 环境要求

- Python 3.8 或更高版本
- 无需任何外部依赖

### 📥 安装方式

#### 方式一：从源码安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/DataMorph.git

# 进入目录
cd DataMorph

# 安装
pip install -e .
```

#### 方式二：直接运行

```bash
# 无需安装，直接运行
python -m datamorph.cli --help
```

### 🎮 基本使用

```bash
# 查看帮助
datamorph --help

# 转换格式
datamorph convert input.json output.yaml

# 查询数据
echo '{"users": [{"name": "Alice", "age": 30}]}' | datamorph query 'users[0].name'

# 格式化输出
datamorph table data.csv
```

---

## 📖 详细使用指南

### 🔄 convert 命令

在多种数据格式之间进行转换：

```bash
datamorph convert <input> <output> [options]

# 参数说明
# input   - 输入文件路径（使用 - 从标准输入读取）
# output  - 输出文件路径（使用 - 输出到标准输出）

# 选项
# -f, --from  - 输入格式（json/yaml/toml/csv），自动检测
# -t, --to    - 输出格式（json/yaml/toml/csv），必需

# 示例
datamorph convert config.json config.yaml -t yaml
datamorph convert data.csv data.json -t json
cat input.yaml | datamorph convert - - -f yaml -t json
```

### 🔍 query 命令

使用表达式查询数据：

```bash
datamorph query <expression> [options]

# 查询语法
# .field       - 访问字段
# [0]          - 数组索引
# [start:end]  - 数组切片
# [?condition] - 过滤条件
# [*]          - 通配符

# 支持的比较运算符
# ==, !=, <, >, <=, >=
# contains, starts_with, ends_with

# 示例
datamorph query 'users[0].name' < data.json
datamorph query 'items[?price > 100]' < products.json
datamorph query 'users[?age >= 25 && status == "active"]' < users.json
```

### 📊 table 命令

将数据格式化为表格：

```bash
datamorph table [input] [options]

# 选项
# -f, --format  - 输入格式
# -c, --columns - 显示的列（逗号分隔）
# -w, --width   - 最大表格宽度

# 示例
datamorph table users.csv
datamorph table data.json -c name,age,email
datamorph table products.json -w 150
```

### 🌳 tree 命令

将数据格式化为树形结构：

```bash
datamorph tree [input] [options]

# 选项
# -f, --format - 输入格式
# -d, --depth  - 最大深度

# 示例
datamorph tree config.json
datamorph tree data.yaml -d 3
```

### 💅 pretty 命令

美化 JSON 输出：

```bash
datamorph pretty [input] [options]

# 选项
# -i, --indent   - 缩进空格数（默认 2）
# -o, --output   - 输出文件
# --no-color     - 禁用彩色输出

# 示例
datamorph pretty data.json
datamorph pretty input.json -o output.json -i 4
```

### 🗜️ minify 命令

压缩 JSON：

```bash
datamorph minify [input] [options]

# 示例
datamorph minify data.json
datamorph minify input.json -o minified.json
```

### ✅ validate 命令

验证数据格式：

```bash
datamorph validate <input> [options]

# 选项
# -f, --format - 指定格式

# 示例
datamorph validate config.json
datamorph validate settings.yaml -f yaml
```

---

## 💡 设计思路与迭代规划

### 🏗️ 技术选型

| 组件 | 选择 | 理由 |
|------|------|------|
| 语言 | Python 3.8+ | 标准库丰富，跨平台兼容 |
| CLI 框架 | argparse | 内置支持，零依赖 |
| YAML 解析 | 自研实现 | 无需 PyYAML 依赖 |
| TOML 解析 | 自研实现 | 无需 tomli 依赖 |
| 输出美化 | ANSI 转义码 | 无需第三方库 |

### 📅 后续迭代计划

- [ ] 支持 XML 格式
- [ ] 添加 JSON Schema 验证
- [ ] 支持更多查询语法
- [ ] 添加数据合并功能
- [ ] 支持远程 URL 读取
- [ ] 提供 Web API 接口
- [ ] 打包为独立可执行文件

---

## 📦 打包与部署指南

### 🐍 PyPI 发布

```bash
# 构建
python setup.py sdist bdist_wheel

# 上传
twine upload dist/*
```

### 📦 独立可执行文件

使用 PyInstaller 打包：

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包
pyinstaller --onefile --name datamorph datamorph/cli.py

# 输出在 dist/ 目录
```

---

## 🤝 贡献指南

欢迎所有形式的贡献！

### 📝 提交规范

我们使用 Angular 提交规范：

- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具相关

### 🔀 提交流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 📄 开源协议说明

本项目采用 [MIT License](LICENSE) 开源协议。

这意味着您可以：
- ✅ 商业使用
- ✅ 修改代码
- ✅ 分发代码
- ✅ 私人使用

唯一要求是保留版权声明和许可证副本。

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>
