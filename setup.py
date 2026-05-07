#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Setup script for DataMorph."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="datamorph",
    version="1.0.0",
    author="gitstq",
    author_email="",
    description="🔄 DataMorph - Lightweight Terminal Data Processing Swiss Army Knife",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/DataMorph",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
        "Topic :: Text Processing",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "datamorph=datamorph.cli:main",
        ],
    },
    keywords="cli json yaml toml csv data processing terminal",
    license="MIT",
)
