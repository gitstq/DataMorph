#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TOML parser for DataMorph - Zero dependency implementation."""

import re
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, date, time


class TOMLParser:
    """TOML parser with zero external dependencies.
    
    Supports TOML 1.0 specification including:
    - Basic key/value pairs
    - Tables (sections)
    - Arrays
    - Inline tables
    - Strings (basic, literal, multi-line)
    - Numbers (integers, floats, hex, octal, binary)
    - Booleans and null
    - Dates and times
    """
    
    @staticmethod
    def parse(data: str) -> Any:
        """Parse TOML string to Python object.
        
        Args:
            data: TOML string to parse
            
        Returns:
            Parsed Python object (dict)
            
        Raises:
            ValueError: If TOML is invalid
        """
        parser = _TOMLParser(data)
        return parser.parse()
    
    @staticmethod
    def parse_file(filepath: str, encoding: str = "utf-8") -> Any:
        """Parse TOML file to Python object.
        
        Args:
            filepath: Path to TOML file
            encoding: File encoding
            
        Returns:
            Parsed Python object
        """
        with open(filepath, "r", encoding=encoding) as f:
            return TOMLParser.parse(f.read())
    
    @staticmethod
    def stringify(data: Any, indent: int = 2) -> str:
        """Convert Python object to TOML string.
        
        Args:
            data: Python object to convert
            indent: Indentation level for nested tables
            
        Returns:
            TOML string
        """
        return _TOMLDumper(data, indent).dump()
    
    @staticmethod
    def validate(data: str) -> bool:
        """Validate TOML string.
        
        Args:
            data: TOML string to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            TOMLParser.parse(data)
            return True
        except (ValueError, TypeError):
            return False


class _TOMLParser:
    """Internal TOML parser implementation."""
    
    def __init__(self, data: str):
        self.data = data
        self.pos = 0
        self.line = 1
        self.col = 1
    
    def parse(self) -> Dict[str, Any]:
        """Parse the TOML content."""
        result = {}
        current_table = result
        current_path = []
        
        while self.pos < len(self.data):
            self._skip_whitespace_and_comments()
            
            if self.pos >= len(self.data):
                break
            
            char = self.data[self.pos]
            
            if char == '[':
                # Table or array of tables
                current_table, current_path = self._parse_table_header(result, current_path)
            elif char == '\n':
                self.pos += 1
                self.line += 1
                self.col = 1
            elif char and not char.isspace():
                # Key-value pair
                key, value = self._parse_key_value()
                self._set_nested_value(current_table, key, value)
            else:
                self.pos += 1
                self.col += 1
        
        return result
    
    def _skip_whitespace_and_comments(self):
        """Skip whitespace and comments."""
        while self.pos < len(self.data):
            char = self.data[self.pos]
            
            if char == '#':
                # Skip comment until end of line
                while self.pos < len(self.data) and self.data[self.pos] != '\n':
                    self.pos += 1
            elif char in ' \t\r':
                self.pos += 1
                self.col += 1
            else:
                break
    
    def _parse_table_header(self, result: Dict, current_path: List[str]) -> tuple:
        """Parse table header [table] or [[array.of.tables]]."""
        self.pos += 1  # Skip '['
        self.col += 1
        
        is_array = False
        if self.pos < len(self.data) and self.data[self.pos] == '[':
            is_array = True
            self.pos += 1
            self.col += 1
        
        # Parse the table path
        path = self._parse_key()
        
        # Skip to closing bracket
        self._skip_whitespace_and_comments()
        if self.pos >= len(self.data) or self.data[self.pos] != ']':
            raise ValueError(f"Expected ']' at line {self.line}")
        self.pos += 1
        self.col += 1
        
        if is_array:
            if self.pos >= len(self.data) or self.data[self.pos] != ']':
                raise ValueError(f"Expected ']]' at line {self.line}")
            self.pos += 1
            self.col += 1
        
        # Navigate to the table
        path_parts = path.split('.')
        current = result
        
        for i, part in enumerate(path_parts):
            if part not in current:
                if is_array and i == len(path_parts) - 1:
                    current[part] = []
                else:
                    current[part] = {}
            
            if is_array and i == len(path_parts) - 1:
                # Add new table to array
                new_table = {}
                current[part].append(new_table)
                current = new_table
            else:
                current = current[part]
        
        return current, path_parts
    
    def _parse_key_value(self) -> tuple:
        """Parse a key-value pair."""
        key = self._parse_key()
        
        self._skip_whitespace_and_comments()
        
        if self.pos >= len(self.data) or self.data[self.pos] != '=':
            raise ValueError(f"Expected '=' at line {self.line}")
        self.pos += 1
        self.col += 1
        
        self._skip_whitespace_and_comments()
        
        value = self._parse_value()
        
        return key, value
    
    def _parse_key(self) -> str:
        """Parse a key."""
        key_parts = []
        
        while self.pos < len(self.data):
            self._skip_whitespace_and_comments()
            
            if self.pos >= len(self.data):
                break
            
            char = self.data[self.pos]
            
            if char == '"' or char == "'":
                # Quoted key
                key_parts.append(self._parse_string())
            elif char.isalnum() or char == '_' or char == '-':
                # Bare key
                start = self.pos
                while self.pos < len(self.data) and (self.data[self.pos].isalnum() or self.data[self.pos] in '_-'):
                    self.pos += 1
                    self.col += 1
                key_parts.append(self.data[start:self.pos])
            elif char == '.':
                self.pos += 1
                self.col += 1
                continue
            elif char == '=' or char == ']' or char == '\n':
                break
            else:
                break
        
        return '.'.join(key_parts)
    
    def _parse_value(self) -> Any:
        """Parse a value."""
        if self.pos >= len(self.data):
            return None
        
        char = self.data[self.pos]
        
        if char == '"':
            if self.pos + 2 < len(self.data) and self.data[self.pos:self.pos+3] == '"""':
                return self._parse_multiline_string()
            return self._parse_basic_string()
        elif char == "'":
            if self.pos + 2 < len(self.data) and self.data[self.pos:self.pos+3] == "'''":
                return self._parse_multiline_literal_string()
            return self._parse_literal_string()
        elif char == '[':
            return self._parse_array()
        elif char == '{':
            return self._parse_inline_table()
        elif char == 't' and self.data[self.pos:self.pos+4] == 'true':
            self.pos += 4
            self.col += 4
            return True
        elif char == 'f' and self.data[self.pos:self.pos+5] == 'false':
            self.pos += 5
            self.col += 5
            return False
        elif char == 'i' and self.data[self.pos:self.pos+3] == 'inf':
            self.pos += 3
            self.col += 3
            return float('inf')
        elif char == 'n' and self.data[self.pos:self.pos+3] == 'nan':
            self.pos += 3
            self.col += 3
            return float('nan')
        elif char == '-' or char == '+' or char.isdigit():
            return self._parse_number()
        else:
            # Try to parse datetime
            return self._parse_datetime()
    
    def _parse_basic_string(self) -> str:
        """Parse a basic string."""
        self.pos += 1  # Skip opening quote
        self.col += 1
        
        result = []
        
        while self.pos < len(self.data):
            char = self.data[self.pos]
            
            if char == '"':
                self.pos += 1
                self.col += 1
                return ''.join(result)
            elif char == '\\':
                self.pos += 1
                self.col += 1
                if self.pos < len(self.data):
                    escape_char = self.data[self.pos]
                    escape_map = {
                        'n': '\n', 't': '\t', 'r': '\r',
                        '\\': '\\', '"': '"', 'b': '\b', 'f': '\f'
                    }
                    result.append(escape_map.get(escape_char, escape_char))
                    self.pos += 1
                    self.col += 1
            else:
                result.append(char)
                self.pos += 1
                self.col += 1
        
        raise ValueError(f"Unterminated string at line {self.line}")
    
    def _parse_literal_string(self) -> str:
        """Parse a literal string."""
        self.pos += 1  # Skip opening quote
        self.col += 1
        
        result = []
        
        while self.pos < len(self.data):
            char = self.data[self.pos]
            
            if char == "'":
                self.pos += 1
                self.col += 1
                return ''.join(result)
            else:
                result.append(char)
                self.pos += 1
                self.col += 1
        
        raise ValueError(f"Unterminated string at line {self.line}")
    
    def _parse_multiline_string(self) -> str:
        """Parse a multi-line basic string."""
        self.pos += 3  # Skip opening quotes
        self.col += 3
        
        # Skip immediate newline
        if self.pos < len(self.data) and self.data[self.pos] == '\n':
            self.pos += 1
            self.line += 1
            self.col = 1
        
        result = []
        
        while self.pos < len(self.data):
            if self.data[self.pos:self.pos+3] == '"""':
                self.pos += 3
                self.col += 3
                return ''.join(result)
            
            char = self.data[self.pos]
            
            if char == '\n':
                result.append(char)
                self.pos += 1
                self.line += 1
                self.col = 1
            elif char == '\\':
                self.pos += 1
                self.col += 1
                if self.pos < len(self.data):
                    if self.data[self.pos] in ' \t\n':
                        # Line ending backslash
                        while self.pos < len(self.data) and self.data[self.pos] in ' \t\n':
                            if self.data[self.pos] == '\n':
                                self.line += 1
                                self.col = 1
                            self.pos += 1
                    else:
                        escape_map = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"'}
                        result.append(escape_map.get(self.data[self.pos], self.data[self.pos]))
                        self.pos += 1
                        self.col += 1
            else:
                result.append(char)
                self.pos += 1
                self.col += 1
        
        raise ValueError(f"Unterminated multi-line string")
    
    def _parse_multiline_literal_string(self) -> str:
        """Parse a multi-line literal string."""
        self.pos += 3  # Skip opening quotes
        self.col += 3
        
        # Skip immediate newline
        if self.pos < len(self.data) and self.data[self.pos] == '\n':
            self.pos += 1
            self.line += 1
            self.col = 1
        
        result = []
        
        while self.pos < len(self.data):
            if self.data[self.pos:self.pos+3] == "'''":
                self.pos += 3
                self.col += 3
                return ''.join(result)
            
            char = self.data[self.pos]
            result.append(char)
            
            if char == '\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1
            self.pos += 1
        
        raise ValueError(f"Unterminated multi-line literal string")
    
    def _parse_array(self) -> List[Any]:
        """Parse an array."""
        self.pos += 1  # Skip '['
        self.col += 1
        
        result = []
        
        while self.pos < len(self.data):
            self._skip_whitespace_and_comments()
            
            if self.pos >= len(self.data):
                break
            
            char = self.data[self.pos]
            
            if char == ']':
                self.pos += 1
                self.col += 1
                return result
            elif char == ',':
                self.pos += 1
                self.col += 1
            elif char == '\n':
                self.pos += 1
                self.line += 1
                self.col = 1
            else:
                result.append(self._parse_value())
        
        raise ValueError(f"Unterminated array at line {self.line}")
    
    def _parse_inline_table(self) -> Dict[str, Any]:
        """Parse an inline table."""
        self.pos += 1  # Skip '{'
        self.col += 1
        
        result = {}
        
        while self.pos < len(self.data):
            self._skip_whitespace_and_comments()
            
            if self.pos >= len(self.data):
                break
            
            char = self.data[self.pos]
            
            if char == '}':
                self.pos += 1
                self.col += 1
                return result
            elif char == ',':
                self.pos += 1
                self.col += 1
            else:
                key, value = self._parse_key_value()
                result[key] = value
        
        raise ValueError(f"Unterminated inline table at line {self.line}")
    
    def _parse_number(self) -> Union[int, float]:
        """Parse a number."""
        start = self.pos
        is_float = False
        
        # Handle sign
        if self.data[self.pos] in '+-':
            self.pos += 1
            self.col += 1
        
        # Handle special bases
        if self.pos + 1 < len(self.data) and self.data[self.pos] == '0':
            next_char = self.data[self.pos + 1].lower()
            if next_char == 'x':
                # Hex
                self.pos += 2
                self.col += 2
                while self.pos < len(self.data) and (self.data[self.pos].isdigit() or self.data[self.pos].lower() in 'abcdef'):
                    self.pos += 1
                    self.col += 1
                return int(self.data[start:self.pos].replace('_', ''), 16)
            elif next_char == 'o':
                # Octal
                self.pos += 2
                self.col += 2
                while self.pos < len(self.data) and self.data[self.pos] in '01234567_':
                    self.pos += 1
                    self.col += 1
                return int(self.data[start:self.pos].replace('_', '').replace('0o', '0o'), 8)
            elif next_char == 'b':
                # Binary
                self.pos += 2
                self.col += 2
                while self.pos < len(self.data) and self.data[self.pos] in '01_':
                    self.pos += 1
                    self.col += 1
                return int(self.data[start:self.pos].replace('_', '').replace('0b', ''), 2)
        
        # Regular number
        while self.pos < len(self.data):
            char = self.data[self.pos]
            
            if char.isdigit() or char == '_':
                self.pos += 1
                self.col += 1
            elif char == '.':
                is_float = True
                self.pos += 1
                self.col += 1
            elif char.lower() == 'e':
                is_float = True
                self.pos += 1
                self.col += 1
                if self.pos < len(self.data) and self.data[self.pos] in '+-':
                    self.pos += 1
                    self.col += 1
            else:
                break
        
        num_str = self.data[start:self.pos].replace('_', '')
        
        if is_float:
            return float(num_str)
        return int(num_str)
    
    def _parse_datetime(self) -> Any:
        """Parse a datetime value."""
        # Simple datetime parsing
        start = self.pos
        
        # Look for datetime pattern
        while self.pos < len(self.data):
            char = self.data[self.pos]
            if char.isalnum() or char in '-:T.Z' or char.isdigit():
                self.pos += 1
                self.col += 1
            else:
                break
        
        dt_str = self.data[start:self.pos]
        
        # Try to parse as datetime
        try:
            if 'T' in dt_str or ' ' in dt_str:
                return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
            elif '-' in dt_str and dt_str.count('-') == 2:
                return date.fromisoformat(dt_str)
            elif ':' in dt_str:
                return time.fromisoformat(dt_str)
        except ValueError:
            pass
        
        return dt_str
    
    def _set_nested_value(self, table: Dict, key: str, value: Any):
        """Set a value in a nested table."""
        parts = key.split('.')
        current = table
        
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        current[parts[-1]] = value


class _TOMLDumper:
    """Internal TOML dumper implementation."""
    
    def __init__(self, data: Any, indent: int = 2):
        self.data = data
        self.indent = indent
        self.result = []
    
    def dump(self) -> str:
        """Convert data to TOML string."""
        self._dump_table(self.data, [])
        return '\n'.join(self.result)
    
    def _dump_table(self, data: Dict, path: List[str]):
        """Dump a table."""
        # First, dump simple key-value pairs
        tables = []
        arrays = []
        
        for key, value in data.items():
            if isinstance(value, dict):
                tables.append((key, value))
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                arrays.append((key, value))
            else:
                self._dump_key_value(key, value)
        
        # Then, dump nested tables
        for key, value in tables:
            new_path = path + [key]
            self.result.append('')
            self.result.append(f"[{'.'.join(new_path)}]")
            self._dump_table(value, new_path)
        
        # Finally, dump arrays of tables
        for key, value in arrays:
            new_path = path + [key]
            for item in value:
                self.result.append('')
                self.result.append(f"[[{'.'.join(new_path)}]]")
                self._dump_table(item, new_path)
    
    def _dump_key_value(self, key: str, value: Any):
        """Dump a key-value pair."""
        self.result.append(f"{key} = {self._value_to_string(value)}")
    
    def _value_to_string(self, value: Any) -> str:
        """Convert a value to TOML string representation."""
        if value is None:
            return '""'
        elif isinstance(value, bool):
            return 'true' if value else 'false'
        elif isinstance(value, int):
            return str(value)
        elif isinstance(value, float):
            return str(value)
        elif isinstance(value, str):
            if '\n' in value:
                return f'"""\n{value}"""'
            elif any(c in value for c in '"\\\n\t\r'):
                escaped = value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r')
                return f'"{escaped}"'
            return f'"{value}"'
        elif isinstance(value, list):
            items = [self._value_to_string(item) for item in value]
            return f"[{', '.join(items)}]"
        elif isinstance(value, dict):
            items = [f"{k} = {self._value_to_string(v)}" for k, v in value.items()]
            return f"{{ {', '.join(items)} }}"
        elif isinstance(value, datetime):
            return value.isoformat()
        elif isinstance(value, date):
            return value.isoformat()
        elif isinstance(value, time):
            return value.isoformat()
        else:
            return f'"{str(value)}"'
