#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DataMorph - Lightweight Terminal Data Processing Swiss Army Knife
轻量级终端数据处理瑞士军刀

A zero-dependency CLI tool for JSON/YAML/TOML/CSV data processing.
Supports format conversion, querying, validation, and beautiful output.
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__license__ = "MIT"

from .cli import main

__all__ = ["main", "__version__"]
