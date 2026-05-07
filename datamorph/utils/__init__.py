#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utilities module for DataMorph."""

from .stream import (
    read_stream, 
    read_lines, 
    write_stream, 
    is_pipe_input, 
    is_pipe_output
)

__all__ = [
    "read_stream", 
    "read_lines", 
    "write_stream", 
    "is_pipe_input", 
    "is_pipe_output"
]
