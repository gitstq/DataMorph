#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Table formatter for DataMorph."""

from typing import Any, Dict, List, Optional, Union


class TableFormatter:
    """Format data as ASCII tables."""
    
    def __init__(self, data: Any, max_width: int = 80):
        """Initialize table formatter.
        
        Args:
            data: Data to format
            max_width: Maximum table width
        """
        self.data = data
        self.max_width = max_width
    
    def format(self, columns: Optional[List[str]] = None) -> str:
        """Format data as table.
        
        Args:
            columns: Columns to include (default: all)
            
        Returns:
            Formatted table string
        """
        if not self.data:
            return "(empty)"
        
        if isinstance(self.data, dict):
            return self._format_dict_table(self.data)
        elif isinstance(self.data, list):
            if all(isinstance(item, dict) for item in self.data):
                return self._format_list_of_dicts(self.data, columns)
            else:
                return self._format_list(self.data)
        else:
            return str(self.data)
    
    def _format_dict_table(self, data: Dict) -> str:
        """Format a dictionary as a key-value table.
        
        Args:
            data: Dictionary to format
            
        Returns:
            Formatted table
        """
        if not data:
            return "(empty)"
        
        # Calculate column widths
        key_width = max(len(str(k)) for k in data.keys())
        value_width = min(
            max(len(self._truncate(str(v))) for v in data.values()),
            self.max_width - key_width - 7
        )
        
        # Build table
        lines = []
        border = f"+{'-' * (key_width + 2)}+{'-' * (value_width + 2)}+"
        
        lines.append(border)
        
        for key, value in data.items():
            truncated = self._truncate(str(value), value_width)
            lines.append(f"| {str(key).ljust(key_width)} | {truncated.ljust(value_width)} |")
        
        lines.append(border)
        
        return '\n'.join(lines)
    
    def _format_list_of_dicts(self, data: List[Dict], columns: Optional[List[str]] = None) -> str:
        """Format a list of dictionaries as a table.
        
        Args:
            data: List of dictionaries
            columns: Columns to include
            
        Returns:
            Formatted table
        """
        if not data:
            return "(empty)"
        
        # Determine columns
        if columns is None:
            columns = list(data[0].keys())
        
        # Calculate column widths
        widths = {}
        for col in columns:
            widths[col] = len(col)
            for row in data:
                value = self._truncate(str(row.get(col, '')))
                widths[col] = min(max(widths[col], len(value)), 30)
        
        # Build header
        header_parts = [col.ljust(widths[col]) for col in columns]
        header = "| " + " | ".join(header_parts) + " |"
        
        # Build separator
        sep_parts = ["-" * widths[col] for col in columns]
        separator = "+-" + "-+-".join(sep_parts) + "-+"
        
        # Build rows
        lines = [separator, header, separator]
        
        for row in data:
            row_parts = []
            for col in columns:
                value = self._truncate(str(row.get(col, '')), widths[col])
                row_parts.append(value.ljust(widths[col]))
            lines.append("| " + " | ".join(row_parts) + " |")
        
        lines.append(separator)
        
        return '\n'.join(lines)
    
    def _format_list(self, data: List) -> str:
        """Format a simple list.
        
        Args:
            data: List to format
            
        Returns:
            Formatted list
        """
        if not data:
            return "(empty)"
        
        lines = []
        for i, item in enumerate(data):
            lines.append(f"[{i}] {self._truncate(str(item))}")
        
        return '\n'.join(lines)
    
    def _truncate(self, text: str, max_len: int = 30) -> str:
        """Truncate text if too long.
        
        Args:
            text: Text to truncate
            max_len: Maximum length
            
        Returns:
            Truncated text
        """
        if len(text) <= max_len:
            return text
        return text[:max_len - 3] + "..."
