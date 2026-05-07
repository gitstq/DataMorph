#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stream utilities for DataMorph."""

import sys
from typing import Any, Dict, Iterator, Optional


def read_stream(stream=None, chunk_size: int = 8192) -> Iterator[str]:
    """Read from stream in chunks.
    
    Args:
        stream: Input stream (default: stdin)
        chunk_size: Size of chunks to read
        
    Yields:
        Chunks of data
    """
    if stream is None:
        stream = sys.stdin
    
    while True:
        chunk = stream.read(chunk_size)
        if not chunk:
            break
        yield chunk


def read_lines(stream=None) -> Iterator[str]:
    """Read lines from stream.
    
    Args:
        stream: Input stream (default: stdin)
        
    Yields:
        Lines from stream
    """
    if stream is None:
        stream = sys.stdin
    
    for line in stream:
        yield line.rstrip('\n\r')


def write_stream(data: str, stream=None):
    """Write data to stream.
    
    Args:
        data: Data to write
        stream: Output stream (default: stdout)
    """
    if stream is None:
        stream = sys.stdout
    
    stream.write(data)
    stream.flush()


def is_pipe_input() -> bool:
    """Check if input is coming from a pipe.
    
    Returns:
        True if input is piped
    """
    return not sys.stdin.isatty()


def is_pipe_output() -> bool:
    """Check if output is going to a pipe.
    
    Returns:
        True if output is piped
    """
    return not sys.stdout.isatty()
