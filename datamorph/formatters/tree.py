#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tree formatter for DataMorph."""

from typing import Any, Dict, List, Optional, Union


class TreeFormatter:
    """Format data as a tree structure."""
    
    def __init__(self, data: Any, max_depth: int = 5):
        """Initialize tree formatter.
        
        Args:
            data: Data to format
            max_depth: Maximum depth to traverse
        """
        self.data = data
        self.max_depth = max_depth
    
    def format(self) -> str:
        """Format data as tree.
        
        Returns:
            Formatted tree string
        """
        return self._format_node(self.data, "", True)
    
    def _format_node(self, node: Any, prefix: str, is_last: bool, depth: int = 0) -> str:
        """Format a single node.
        
        Args:
            node: Node to format
            prefix: Line prefix
            is_last: Whether this is the last sibling
            depth: Current depth
            
        Returns:
            Formatted node string
        """
        if depth > self.max_depth:
            return f"{prefix}{'└── ' if is_last else '├── '}..."
        
        if node is None:
            return f"{prefix}{'└── ' if is_last else '├── '}null"
        
        if isinstance(node, bool):
            return f"{prefix}{'└── ' if is_last else '├── '}{str(node).lower()}"
        
        if isinstance(node, (int, float, str)):
            return f"{prefix}{'└── ' if is_last else '├── '}{self._truncate(str(node))}"
        
        if isinstance(node, dict):
            return self._format_dict(node, prefix, is_last, depth)
        
        if isinstance(node, list):
            return self._format_list(node, prefix, is_last, depth)
        
        return f"{prefix}{'└── ' if is_last else '├── '}{str(node)}"
    
    def _format_dict(self, data: Dict, prefix: str, is_last: bool, depth: int) -> str:
        """Format a dictionary node.
        
        Args:
            data: Dictionary to format
            prefix: Line prefix
            is_last: Whether this is the last sibling
            depth: Current depth
            
        Returns:
            Formatted dictionary string
        """
        if not data:
            return f"{prefix}{'└── ' if is_last else '├── '}{{}}"
        
        lines = []
        keys = list(data.keys())
        
        # Add header
        connector = "└── " if is_last else "├── "
        lines.append(f"{prefix}{connector}{{}} ({len(keys)} keys)")
        
        # Add children
        new_prefix = prefix + ("    " if is_last else "│   ")
        
        for i, key in enumerate(keys):
            is_last_child = (i == len(keys) - 1)
            child_prefix = new_prefix + "├── " if not is_last_child else new_prefix + "└── "
            
            value = data[key]
            
            if isinstance(value, (dict, list)) and value:
                # Complex value
                lines.append(f"{new_prefix}{'└── ' if is_last_child else '├── '}{key}:")
                lines.append(self._format_node(value, new_prefix, is_last_child, depth + 1))
            else:
                # Simple value
                lines.append(f"{new_prefix}{'└── ' if is_last_child else '├── '}{key}: {self._format_simple(value)}")
        
        return '\n'.join(lines)
    
    def _format_list(self, data: List, prefix: str, is_last: bool, depth: int) -> str:
        """Format a list node.
        
        Args:
            data: List to format
            prefix: Line prefix
            is_last: Whether this is the last sibling
            depth: Current depth
            
        Returns:
            Formatted list string
        """
        if not data:
            return f"{prefix}{'└── ' if is_last else '├── '}[]"
        
        lines = []
        
        # Add header
        connector = "└── " if is_last else "├── "
        lines.append(f"{prefix}{connector}[] ({len(data)} items)")
        
        # Add children
        new_prefix = prefix + ("    " if is_last else "│   ")
        
        for i, item in enumerate(data):
            is_last_child = (i == len(data) - 1)
            
            if isinstance(item, (dict, list)) and item:
                # Complex item
                lines.append(f"{new_prefix}{'└── ' if is_last_child else '├── '}[{i}]:")
                lines.append(self._format_node(item, new_prefix, is_last_child, depth + 1))
            else:
                # Simple item
                lines.append(f"{new_prefix}{'└── ' if is_last_child else '├── '}[{i}]: {self._format_simple(item)}")
        
        return '\n'.join(lines)
    
    def _format_simple(self, value: Any) -> str:
        """Format a simple value.
        
        Args:
            value: Value to format
            
        Returns:
            Formatted string
        """
        if value is None:
            return "null"
        if isinstance(value, bool):
            return str(value).lower()
        if isinstance(value, str):
            return f'"{self._truncate(value)}"'
        return str(value)
    
    def _truncate(self, text: str, max_len: int = 50) -> str:
        """Truncate text if too long.
        
        Args:
            text: Text to truncate
            max_len: Maximum length
            
        Returns:
            Truncated text
        """
        text = text.replace('\n', '\\n')
        if len(text) <= max_len:
            return text
        return text[:max_len - 3] + "..."
