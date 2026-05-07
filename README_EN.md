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
  <b>Lightweight Terminal Data Processing Swiss Army Knife</b>
</p>

<p align="center">
  Zero-dependency CLI tool for JSON / YAML / TOML / CSV data processing
</p>

---

## 🎉 Introduction

**DataMorph** is a lightweight terminal data processing tool designed for developers. It solves the pain points of frequently switching between different data formats and manually parsing and converting data in daily development.

### 💡 Inspiration

In daily development, we often need to handle configuration files and data in various formats: JSON configs, YAML manifests, TOML settings, CSV data tables. Each time we need to install different tools or write temporary scripts to process these formats. DataMorph aims to provide a unified command-line tool to make data processing simple and efficient.

### ✨ Key Highlights

- 🚀 **Zero External Dependencies** - Implemented entirely with Python standard library, no third-party packages required
- 🔄 **Multi-format Conversion** - Support mutual conversion between JSON, YAML, TOML, CSV formats
- 🔍 **Powerful Query Engine** - JMESPath-like syntax with complex filtering and nested queries
- 🎨 **Beautiful Output** - Table, tree, and colorized highlight output formats
- 📊 **Stream Processing** - Pipeline support for handling large files
- ⚡ **Single File Execution** - Can be packaged as a standalone executable without Python environment

---

## ✨ Core Features

### 📦 Format Conversion

```bash
# JSON to YAML
datamorph convert config.json config.yaml

# YAML to TOML
datamorph convert settings.yaml settings.toml

# CSV to JSON
datamorph convert data.csv data.json

# Read from stdin
cat data.json | datamorph convert - output.yaml -t yaml
```

### 🔍 Data Query

```bash
# Query nested fields
datamorph query 'users[0].name' < users.json

# Filter arrays
datamorph query 'users[?age > 25]' < users.json

# Wildcard query
datamorph query 'items[*].price' < products.json
```

### 📊 Formatted Output

```bash
# Table format
datamorph table users.csv

# Tree structure
datamorph tree config.json

# Colorized JSON
datamorph pretty data.json
```

### ✅ Data Validation

```bash
# Validate JSON
datamorph validate config.json

# Validate YAML
datamorph validate settings.yaml -f yaml
```

### 📈 Data Information

```bash
# View data structure info
datamorph info data.json
```

---

## 🚀 Quick Start

### 📋 Requirements

- Python 3.8 or higher
- No external dependencies required

### 📥 Installation

#### Method 1: Install from Source

```bash
# Clone repository
git clone https://github.com/gitstq/DataMorph.git

# Enter directory
cd DataMorph

# Install
pip install -e .
```

#### Method 2: Run Directly

```bash
# No installation needed, run directly
python -m datamorph.cli --help
```

### 🎮 Basic Usage

```bash
# Show help
datamorph --help

# Convert format
datamorph convert input.json output.yaml

# Query data
echo '{"users": [{"name": "Alice", "age": 30}]}' | datamorph query 'users[0].name'

# Format output
datamorph table data.csv
```

---

## 📖 Detailed Usage Guide

### 🔄 convert Command

Convert between multiple data formats:

```bash
datamorph convert <input> <output> [options]

# Arguments
# input   - Input file path (use - for stdin)
# output  - Output file path (use - for stdout)

# Options
# -f, --from  - Input format (json/yaml/toml/csv), auto-detected
# -t, --to    - Output format (json/yaml/toml/csv), required

# Examples
datamorph convert config.json config.yaml -t yaml
datamorph convert data.csv data.json -t json
cat input.yaml | datamorph convert - - -f yaml -t json
```

### 🔍 query Command

Query data using expressions:

```bash
datamorph query <expression> [options]

# Query Syntax
# .field       - Access field
# [0]          - Array index
# [start:end]  - Array slice
# [?condition] - Filter condition
# [*]          - Wildcard

# Supported Comparison Operators
# ==, !=, <, >, <=, >=
# contains, starts_with, ends_with

# Examples
datamorph query 'users[0].name' < data.json
datamorph query 'items[?price > 100]' < products.json
datamorph query 'users[?age >= 25 && status == "active"]' < users.json
```

### 📊 table Command

Format data as table:

```bash
datamorph table [input] [options]

# Options
# -f, --format  - Input format
# -c, --columns - Columns to display (comma-separated)
# -w, --width   - Max table width

# Examples
datamorph table users.csv
datamorph table data.json -c name,age,email
datamorph table products.json -w 150
```

### 🌳 tree Command

Format data as tree structure:

```bash
datamorph tree [input] [options]

# Options
# -f, --format - Input format
# -d, --depth  - Max depth

# Examples
datamorph tree config.json
datamorph tree data.yaml -d 3
```

### 💅 pretty Command

Beautify JSON output:

```bash
datamorph pretty [input] [options]

# Options
# -i, --indent   - Indentation spaces (default 2)
# -o, --output   - Output file
# --no-color     - Disable colorized output

# Examples
datamorph pretty data.json
datamorph pretty input.json -o output.json -i 4
```

### 🗜️ minify Command

Minify JSON:

```bash
datamorph minify [input] [options]

# Examples
datamorph minify data.json
datamorph minify input.json -o minified.json
```

### ✅ validate Command

Validate data format:

```bash
datamorph validate <input> [options]

# Options
# -f, --format - Specify format

# Examples
datamorph validate config.json
datamorph validate settings.yaml -f yaml
```

---

## 💡 Design Philosophy & Roadmap

### 🏗️ Technology Choices

| Component | Choice | Reason |
|-----------|--------|--------|
| Language | Python 3.8+ | Rich standard library, cross-platform |
| CLI Framework | argparse | Built-in support, zero dependencies |
| YAML Parser | Custom implementation | No PyYAML dependency |
| TOML Parser | Custom implementation | No tomli dependency |
| Output Styling | ANSI escape codes | No third-party libraries |

### 📅 Future Roadmap

- [ ] Support XML format
- [ ] Add JSON Schema validation
- [ ] Support more query syntax
- [ ] Add data merge functionality
- [ ] Support remote URL reading
- [ ] Provide Web API interface
- [ ] Package as standalone executable

---

## 📦 Packaging & Deployment

### 🐍 PyPI Publishing

```bash
# Build
python setup.py sdist bdist_wheel

# Upload
twine upload dist/*
```

### 📦 Standalone Executable

Package with PyInstaller:

```bash
# Install PyInstaller
pip install pyinstaller

# Package
pyinstaller --onefile --name datamorph datamorph/cli.py

# Output in dist/ directory
```

---

## 🤝 Contributing

All forms of contribution are welcome!

### 📝 Commit Convention

We use Angular commit convention:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation update
- `refactor:` Code refactoring
- `test:` Test related
- `chore:` Build/tool related

### 🔀 Pull Request Process

1. Fork this repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Create Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

This means you can:
- ✅ Commercial use
- ✅ Modify code
- ✅ Distribute code
- ✅ Private use

The only requirement is to preserve the copyright notice and license copy.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>
