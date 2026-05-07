#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""JSON parser for DataMorph."""

import json
import sys
from typing import Any, Dict, List, Optional, Union
from io import StringIO


class JSONParser:
    """JSON parser with streaming support and error handling."""
    
    @staticmethod
    def parse(data: str, **kwargs) -> Any:
        """Parse JSON string to Python object.
        
        Args:
            data: JSON string to parse
            **kwargs: Additional arguments for json.loads
            
        Returns:
            Parsed Python object
            
        Raises:
            ValueError: If JSON is invalid
        """
        try:
            return json.loads(data, **kwargs)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
    
    @staticmethod
    def parse_file(filepath: str, encoding: str = "utf-8") -> Any:
        """Parse JSON file to Python object.
        
        Args:
            filepath: Path to JSON file
            encoding: File encoding (default: utf-8)
            
        Returns:
            Parsed Python object
        """
        try:
            with open(filepath, "r", encoding=encoding) as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filepath}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file {filepath}: {e}")
    
    @staticmethod
    def parse_stream(stream=None) -> Any:
        """Parse JSON from stdin stream.
        
        Args:
            stream: Input stream (default: stdin)
            
        Returns:
            Parsed Python object
        """
        if stream is None:
            stream = sys.stdin
        data = stream.read()
        return JSONParser.parse(data)
    
    @staticmethod
    def stringify(data: Any, indent: int = 2, sort_keys: bool = False, 
                  ensure_ascii: bool = False) -> str:
        """Convert Python object to JSON string.
        
        Args:
            data: Python object to convert
            indent: Indentation level (default: 2)
            sort_keys: Whether to sort keys (default: False)
            ensure_ascii: Whether to escape non-ASCII (default: False)
            
        Returns:
            JSON string
        """
        return json.dumps(
            data, 
            indent=indent, 
            sort_keys=sort_keys,
            ensure_ascii=ensure_ascii
        )
    
    @staticmethod
    def validate(data: str) -> bool:
        """Validate JSON string.
        
        Args:
            data: JSON string to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            json.loads(data)
            return True
        except (json.JSONDecodeError, TypeError):
            return False
    
    @staticmethod
    def minify(data: str) -> str:
        """Minify JSON string (remove whitespace).
        
        Args:
            data: JSON string to minify
            
        Returns:
            Minified JSON string
        """
        parsed = JSONParser.parse(data)
        return json.dumps(parsed, separators=(",", ":"))
    
    @staticmethod
    def pretty(data: str, indent: int = 2) -> str:
        """Pretty print JSON string.
        
        Args:
            data: JSON string to format
            indent: Indentation level
            
        Returns:
            Formatted JSON string
        """
        parsed = JSONParser.parse(data)
        return JSONParser.stringify(parsed, indent=indent)
