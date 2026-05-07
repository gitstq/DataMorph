#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""YAML parser for DataMorph - Zero dependency implementation."""

import re
from typing import Any, Dict, List, Optional, Union


class YAMLParser:
    """YAML parser with zero external dependencies.
    
    Supports a subset of YAML 1.2 specification including:
    - Basic scalars (strings, numbers, booleans, null)
    - Lists and dictionaries
    - Multi-line strings
    - Comments
    """
    
    # YAML type patterns
    NULL_PATTERN = re.compile(r'^(null|Null|NULL|~)$')
    BOOL_PATTERN = re.compile(r'^(true|True|TRUE|false|False|FALSE)$')
    INT_PATTERN = re.compile(r'^[-+]?[0-9]+$')
    FLOAT_PATTERN = re.compile(r'^[-+]?(\.[0-9]+|[0-9]+(\.[0-9]*)?)([eE][-+]?[0-9]+)?$')
    
    @staticmethod
    def parse(data: str) -> Any:
        """Parse YAML string to Python object.
        
        Args:
            data: YAML string to parse
            
        Returns:
            Parsed Python object
            
        Raises:
            ValueError: If YAML is invalid
        """
        lines = data.split('\n')
        parser = _YAMLParser(lines)
        return parser.parse()
    
    @staticmethod
    def parse_file(filepath: str, encoding: str = "utf-8") -> Any:
        """Parse YAML file to Python object.
        
        Args:
            filepath: Path to YAML file
            encoding: File encoding
            
        Returns:
            Parsed Python object
        """
        with open(filepath, "r", encoding=encoding) as f:
            return YAMLParser.parse(f.read())
    
    @staticmethod
    def stringify(data: Any, indent: int = 2, default_flow_style: bool = False) -> str:
        """Convert Python object to YAML string.
        
        Args:
            data: Python object to convert
            indent: Indentation level
            default_flow_style: Use flow style for collections
            
        Returns:
            YAML string
        """
        return _YAMLDumper(data, indent).dump()
    
    @staticmethod
    def validate(data: str) -> bool:
        """Validate YAML string.
        
        Args:
            data: YAML string to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            YAMLParser.parse(data)
            return True
        except (ValueError, TypeError):
            return False


class _YAMLParser:
    """Internal YAML parser implementation."""
    
    def __init__(self, lines: List[str]):
        self.lines = lines
        self.pos = 0
    
    def parse(self) -> Any:
        """Parse the YAML content."""
        # Skip empty lines and comments at the beginning
        self._skip_empty_and_comments()
        
        if self.pos >= len(self.lines):
            return None
        
        return self._parse_value(0)
    
    def _skip_empty_and_comments(self):
        """Skip empty lines and comments."""
        while self.pos < len(self.lines):
            line = self.lines[self.pos]
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                break
            self.pos += 1
    
    def _get_indent(self, line: str) -> int:
        """Get the indentation level of a line."""
        return len(line) - len(line.lstrip())
    
    def _parse_value(self, expected_indent: int) -> Any:
        """Parse a YAML value at the given indentation level."""
        if self.pos >= len(self.lines):
            return None
        
        line = self.lines[self.pos]
        stripped = line.strip()
        
        if not stripped or stripped.startswith('#'):
            return None
        
        # Check for list item
        if stripped.startswith('- ') or stripped == '-':
            return self._parse_list(expected_indent)
        
        # Check for dictionary
        if ':' in stripped:
            return self._parse_dict(expected_indent)
        
        # Parse scalar
        self.pos += 1
        return self._parse_scalar(stripped)
    
    def _parse_list(self, base_indent: int) -> List[Any]:
        """Parse a YAML list."""
        result = []
        
        while self.pos < len(self.lines):
            self._skip_empty_and_comments()
            if self.pos >= len(self.lines):
                break
            
            line = self.lines[self.pos]
            indent = self._get_indent(line)
            stripped = line.strip()
            
            if indent < base_indent:
                break
            
            if not stripped.startswith('-'):
                break
            
            self.pos += 1
            
            # Get the value after '-'
            value_part = stripped[1:].strip()
            
            if value_part:
                if ':' in value_part and not value_part.startswith('"') and not value_part.startswith("'"):
                    # Inline dict
                    result.append(self._parse_inline_dict(value_part))
                else:
                    result.append(self._parse_scalar(value_part))
            else:
                # Multi-line value
                next_indent = indent + 2
                result.append(self._parse_value(next_indent))
        
        return result
    
    def _parse_dict(self, base_indent: int) -> Dict[str, Any]:
        """Parse a YAML dictionary."""
        result = {}
        
        while self.pos < len(self.lines):
            self._skip_empty_and_comments()
            if self.pos >= len(self.lines):
                break
            
            line = self.lines[self.pos]
            indent = self._get_indent(line)
            stripped = line.strip()
            
            if indent < base_indent:
                break
            
            if stripped.startswith('-'):
                break
            
            if ':' not in stripped:
                break
            
            self.pos += 1
            
            # Split key and value
            colon_pos = stripped.index(':')
            key = stripped[:colon_pos].strip()
            value_part = stripped[colon_pos + 1:].strip()
            
            # Remove quotes from key if present
            if (key.startswith('"') and key.endswith('"')) or \
               (key.startswith("'") and key.endswith("'")):
                key = key[1:-1]
            
            if value_part:
                if value_part.startswith('|'):
                    # Multi-line string
                    result[key] = self._parse_multiline_string(indent + 2)
                elif value_part.startswith('[') or value_part.startswith('{'):
                    result[key] = self._parse_inline_value(value_part)
                else:
                    result[key] = self._parse_scalar(value_part)
            else:
                # Value on next line(s)
                next_indent = indent + 2
                result[key] = self._parse_value(next_indent)
        
        return result
    
    def _parse_inline_dict(self, text: str) -> Dict[str, Any]:
        """Parse an inline dictionary."""
        result = {}
        parts = text.split(',')
        for part in parts:
            if ':' in part:
                key, value = part.split(':', 1)
                result[key.strip()] = self._parse_scalar(value.strip())
        return result
    
    def _parse_inline_value(self, text: str) -> Any:
        """Parse an inline JSON-like value."""
        # Simple inline array
        if text.startswith('[') and text.endswith(']'):
            inner = text[1:-1].strip()
            if not inner:
                return []
            items = [self._parse_scalar(item.strip()) for item in inner.split(',')]
            return items
        
        # Simple inline object
        if text.startswith('{') and text.endswith('}'):
            inner = text[1:-1].strip()
            if not inner:
                return {}
            return self._parse_inline_dict(inner)
        
        return self._parse_scalar(text)
    
    def _parse_multiline_string(self, base_indent: int) -> str:
        """Parse a multi-line string."""
        lines = []
        
        while self.pos < len(self.lines):
            line = self.lines[self.pos]
            
            if not line.strip():
                lines.append('')
                self.pos += 1
                continue
            
            indent = self._get_indent(line)
            
            if indent < base_indent:
                break
            
            lines.append(line[base_indent:])
            self.pos += 1
        
        return '\n'.join(lines).rstrip()
    
    def _parse_scalar(self, value: str) -> Any:
        """Parse a scalar value."""
        # Remove quotes
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            return value[1:-1]
        
        # Null
        if YAMLParser.NULL_PATTERN.match(value):
            return None
        
        # Boolean
        if YAMLParser.BOOL_PATTERN.match(value):
            return value.lower() == 'true'
        
        # Integer
        if YAMLParser.INT_PATTERN.match(value):
            return int(value)
        
        # Float
        if YAMLParser.FLOAT_PATTERN.match(value):
            return float(value)
        
        return value


class _YAMLDumper:
    """Internal YAML dumper implementation."""
    
    def __init__(self, data: Any, indent: int = 2):
        self.data = data
        self.indent = indent
        self.result = []
    
    def dump(self) -> str:
        """Convert data to YAML string."""
        self._dump_value(self.data, 0)
        return '\n'.join(self.result)
    
    def _dump_value(self, value: Any, level: int):
        """Dump a value at the given indentation level."""
        if value is None:
            self.result.append(' ' * (level * self.indent) + 'null')
        elif isinstance(value, bool):
            self.result.append(' ' * (level * self.indent) + ('true' if value else 'false'))
        elif isinstance(value, (int, float)):
            self.result.append(' ' * (level * self.indent) + str(value))
        elif isinstance(value, str):
            self._dump_string(value, level)
        elif isinstance(value, list):
            self._dump_list(value, level)
        elif isinstance(value, dict):
            self._dump_dict(value, level)
        else:
            self.result.append(' ' * (level * self.indent) + str(value))
    
    def _dump_string(self, value: str, level: int):
        """Dump a string value."""
        indent_str = ' ' * (level * self.indent)
        
        # Check if multi-line
        if '\n' in value:
            self.result.append(f'{indent_str}|')
            for line in value.split('\n'):
                self.result.append(' ' * ((level + 1) * self.indent) + line)
        elif any(c in value for c in ':[]{}#&*?|<>%@`') or value.startswith(' ') or value.startswith('\t'):
            # Quote special strings
            self.result.append(f'{indent_str}"{value}"')
        else:
            self.result.append(f'{indent_str}{value}')
    
    def _dump_list(self, value: List[Any], level: int):
        """Dump a list."""
        indent_str = ' ' * (level * self.indent)
        
        for item in value:
            if isinstance(item, (dict, list)):
                self.result.append(f'{indent_str}-')
                self._dump_value(item, level + 1)
            else:
                self.result.append(f'{indent_str}- {self._scalar_to_string(item)}')
    
    def _dump_dict(self, value: Dict[str, Any], level: int):
        """Dump a dictionary."""
        indent_str = ' ' * (level * self.indent)
        
        for key, val in value.items():
            if isinstance(val, (dict, list)):
                self.result.append(f'{indent_str}{key}:')
                self._dump_value(val, level + 1)
            else:
                self.result.append(f'{indent_str}{key}: {self._scalar_to_string(val)}')
    
    def _scalar_to_string(self, value: Any) -> str:
        """Convert a scalar to string representation."""
        if value is None:
            return 'null'
        elif isinstance(value, bool):
            return 'true' if value else 'false'
        elif isinstance(value, str):
            if '\n' in value or any(c in value for c in ':[]{}#&*?|<>%@`'):
                return f'"{value}"'
            return value
        else:
            return str(value)
