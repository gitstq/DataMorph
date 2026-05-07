#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Query engine for DataMorph."""

import re
from typing import Any, Dict, List, Optional, Union


class QueryEngine:
    """Query engine for filtering and transforming data.
    
    Supports a simple query syntax similar to JMESPath:
    - Field access: data.field
    - Array access: data[0]
    - Filter: data[?field == 'value']
    - Wildcard: data[*].field
    - Pipe: data | [@].field
    """
    
    def __init__(self, data: Any):
        """Initialize query engine with data.
        
        Args:
            data: Data to query
        """
        self.data = data
    
    def query(self, expression: str) -> Any:
        """Execute a query expression.
        
        Args:
            expression: Query expression
            
        Returns:
            Query result
        """
        # Parse and execute the expression
        tokens = self._tokenize(expression)
        return self._execute(tokens, self.data)
    
    def _tokenize(self, expression: str) -> List[str]:
        """Tokenize the query expression.
        
        Args:
            expression: Query expression
            
        Returns:
            List of tokens
        """
        tokens = []
        current = ''
        in_bracket = False
        in_quote = False
        quote_char = None
        
        for char in expression:
            if char in ('"', "'") and not in_quote:
                in_quote = True
                quote_char = char
                current += char
            elif char == quote_char and in_quote:
                in_quote = False
                quote_char = None
                current += char
            elif in_quote:
                current += char
            elif char == '[':
                if current:
                    tokens.append(current)
                    current = ''
                tokens.append('[')
                in_bracket = True
            elif char == ']':
                if current:
                    tokens.append(current)
                    current = ''
                tokens.append(']')
                in_bracket = False
            elif char == '.' and not in_bracket:
                if current:
                    tokens.append(current)
                    current = ''
            elif char == '|' and not in_bracket:
                if current:
                    tokens.append(current)
                    current = ''
                tokens.append('|')
            else:
                current += char
        
        if current:
            tokens.append(current)
        
        return tokens
    
    def _execute(self, tokens: List[str], data: Any) -> Any:
        """Execute tokens on data.
        
        Args:
            tokens: List of tokens
            data: Data to operate on
            
        Returns:
            Result
        """
        result = data
        i = 0
        
        while i < len(tokens):
            token = tokens[i]
            
            if token == '|':
                # Pipe - continue with next tokens
                i += 1
                continue
            elif token == '[':
                # Array access or filter
                i += 1
                if i < len(tokens):
                    bracket_content = tokens[i]
                    i += 1  # Skip to ']'
                    if i < len(tokens) and tokens[i] == ']':
                        i += 1
                    
                    result = self._handle_bracket(result, bracket_content)
            elif token == ']':
                i += 1
            elif token.startswith('?'):
                # Filter expression
                result = self._filter(result, token[1:])
                i += 1
            else:
                # Field access
                result = self._get_field(result, token)
                i += 1
        
        return result
    
    def _get_field(self, data: Any, field: str) -> Any:
        """Get a field from data.
        
        Args:
            data: Data to get field from
            field: Field name
            
        Returns:
            Field value
        """
        if data is None:
            return None
        
        if isinstance(data, dict):
            return data.get(field)
        elif isinstance(data, list):
            return [self._get_field(item, field) for item in data]
        else:
            return getattr(data, field, None)
    
    def _handle_bracket(self, data: Any, content: str) -> Any:
        """Handle bracket access.
        
        Args:
            data: Data to access
            content: Content inside brackets
            
        Returns:
            Result
        """
        if content == '*':
            # Wildcard - return all
            return data
        
        if content == '?':
            # Filter marker - will be handled by next token
            return data
        
        if content.startswith('?'):
            # Filter expression
            return self._filter(data, content[1:])
        
        # Try to parse as index
        try:
            index = int(content)
            if isinstance(data, list):
                return data[index] if -len(data) <= index < len(data) else None
            elif isinstance(data, dict):
                keys = list(data.keys())
                return data.get(keys[index]) if 0 <= index < len(keys) else None
        except ValueError:
            pass
        
        # Try to parse as slice
        if ':' in content:
            return self._handle_slice(data, content)
        
        return None
    
    def _handle_slice(self, data: Any, content: str) -> Any:
        """Handle slice notation.
        
        Args:
            data: Data to slice
            content: Slice expression (e.g., "0:5" or "1:")
            
        Returns:
            Sliced data
        """
        if not isinstance(data, (list, tuple)):
            return data
        
        parts = content.split(':')
        
        try:
            if len(parts) == 2:
                start = int(parts[0]) if parts[0] else None
                end = int(parts[1]) if parts[1] else None
                return data[start:end]
            elif len(parts) == 3:
                start = int(parts[0]) if parts[0] else None
                end = int(parts[1]) if parts[1] else None
                step = int(parts[2]) if parts[2] else None
                return data[start:end:step]
        except (ValueError, TypeError):
            pass
        
        return data
    
    def _filter(self, data: Any, condition: str) -> Any:
        """Filter data based on condition.
        
        Args:
            data: Data to filter
            condition: Filter condition
            
        Returns:
            Filtered data
        """
        if not isinstance(data, list):
            return data
        
        result = []
        
        for item in data:
            if self._evaluate_condition(item, condition):
                result.append(item)
        
        return result
    
    def _evaluate_condition(self, item: Any, condition: str) -> bool:
        """Evaluate a filter condition.
        
        Args:
            item: Item to evaluate
            condition: Condition string
            
        Returns:
            True if condition is met
        """
        # Parse condition
        # Supported operators: ==, !=, <, >, <=, >=, contains, starts_with, ends_with
        
        operators = [
            ('!=', lambda a, b: a != b),
            ('==', lambda a, b: a == b),
            ('<=', lambda a, b: a <= b if a is not None and b is not None else False),
            ('>=', lambda a, b: a >= b if a is not None and b is not None else False),
            ('<', lambda a, b: a < b if a is not None and b is not None else False),
            ('>', lambda a, b: a > b if a is not None and b is not None else False),
        ]
        
        # Parse logical operators
        if ' && ' in condition:
            parts = condition.split(' && ')
            return all(self._evaluate_condition(item, p.strip()) for p in parts)
        
        if ' || ' in condition:
            parts = condition.split(' || ')
            return any(self._evaluate_condition(item, p.strip()) for p in parts)
        
        # Check for contains
        if 'contains' in condition:
            match = re.match(r'(\w+)\s+contains\s+["\']?(.+?)["\']?$', condition)
            if match:
                field, value = match.groups()
                field_value = self._get_field(item, field)
                return value in str(field_value) if field_value is not None else False
        
        # Check for starts_with
        if 'starts_with' in condition:
            match = re.match(r'(\w+)\s+starts_with\s+["\']?(.+?)["\']?$', condition)
            if match:
                field, value = match.groups()
                field_value = self._get_field(item, field)
                return str(field_value).startswith(value) if field_value is not None else False
        
        # Check for ends_with
        if 'ends_with' in condition:
            match = re.match(r'(\w+)\s+ends_with\s+["\']?(.+?)["\']?$', condition)
            if match:
                field, value = match.groups()
                field_value = self._get_field(item, field)
                return str(field_value).endswith(value) if field_value is not None else False
        
        # Check for comparison operators
        for op, func in operators:
            if op in condition:
                parts = condition.split(op, 1)
                if len(parts) == 2:
                    field = parts[0].strip()
                    value = parts[1].strip()
                    
                    # Get field value
                    field_value = self._get_field(item, field)
                    
                    # Parse comparison value
                    parsed_value = self._parse_value(value)
                    
                    return func(field_value, parsed_value)
        
        # Check for existence
        field = condition.strip()
        if field.startswith('!'):
            return self._get_field(item, field[1:]) is None
        return self._get_field(item, field) is not None
    
    def _parse_value(self, value: str) -> Any:
        """Parse a string value to appropriate type.
        
        Args:
            value: String value
            
        Returns:
            Parsed value
        """
        value = value.strip()
        
        # Remove quotes
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            return value[1:-1]
        
        # Boolean
        if value.lower() == 'true':
            return True
        if value.lower() == 'false':
            return False
        
        # Null
        if value.lower() in ('null', 'none'):
            return None
        
        # Number
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            pass
        
        return value


def query_data(data: Any, expression: str) -> Any:
    """Query data with expression.
    
    Args:
        data: Data to query
        expression: Query expression
        
    Returns:
        Query result
    """
    engine = QueryEngine(data)
    return engine.query(expression)
