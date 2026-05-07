#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Color output formatter for DataMorph."""

import sys
from typing import Any, Optional


class ColorFormatter:
    """Format output with ANSI colors."""
    
    # ANSI color codes
    COLORS = {
        'reset': '\033[0m',
        'bold': '\033[1m',
        'dim': '\033[2m',
        'italic': '\033[3m',
        'underline': '\033[4m',
        
        # Foreground colors
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        
        # Bright foreground colors
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
    }
    
    # Semantic colors
    SEMANTIC = {
        'key': 'cyan',
        'string': 'green',
        'number': 'yellow',
        'boolean': 'magenta',
        'null': 'dim',
        'error': 'red',
        'success': 'green',
        'warning': 'yellow',
        'info': 'blue',
    }
    
    def __init__(self, enabled: bool = True):
        """Initialize color formatter.
        
        Args:
            enabled: Whether colors are enabled
        """
        self.enabled = enabled and self._supports_color()
    
    def _supports_color(self) -> bool:
        """Check if terminal supports colors.
        
        Returns:
            True if colors are supported
        """
        # Check if stdout is a terminal
        if not hasattr(sys.stdout, 'isatty'):
            return False
        
        if not sys.stdout.isatty():
            return False
        
        # Check for common environment indicators
        import os
        if os.environ.get('NO_COLOR'):
            return False
        
        if os.environ.get('TERM') == 'dumb':
            return False
        
        return True
    
    def colorize(self, text: str, color: str) -> str:
        """Apply color to text.
        
        Args:
            text: Text to colorize
            color: Color name or semantic name
            
        Returns:
            Colorized text
        """
        if not self.enabled:
            return text
        
        # Resolve semantic colors
        if color in self.SEMANTIC:
            color = self.SEMANTIC[color]
        
        if color not in self.COLORS:
            return text
        
        return f"{self.COLORS[color]}{text}{self.COLORS['reset']}"
    
    def bold(self, text: str) -> str:
        """Make text bold.
        
        Args:
            text: Text to format
            
        Returns:
            Bold text
        """
        return self.colorize(text, 'bold')
    
    def dim(self, text: str) -> str:
        """Make text dim.
        
        Args:
            text: Text to format
            
        Returns:
            Dim text
        """
        return self.colorize(text, 'dim')
    
    def key(self, text: str) -> str:
        """Format as key.
        
        Args:
            text: Text to format
            
        Returns:
            Key-formatted text
        """
        return self.colorize(text, 'key')
    
    def string(self, text: str) -> str:
        """Format as string value.
        
        Args:
            text: Text to format
            
        Returns:
            String-formatted text
        """
        return self.colorize(text, 'string')
    
    def number(self, text: str) -> str:
        """Format as number.
        
        Args:
            text: Text to format
            
        Returns:
            Number-formatted text
        """
        return self.colorize(text, 'number')
    
    def boolean(self, text: str) -> str:
        """Format as boolean.
        
        Args:
            text: Text to format
            
        Returns:
            Boolean-formatted text
        """
        return self.colorize(text, 'boolean')
    
    def null(self, text: str) -> str:
        """Format as null.
        
        Args:
            text: Text to format
            
        Returns:
            Null-formatted text
        """
        return self.colorize(text, 'null')
    
    def error(self, text: str) -> str:
        """Format as error.
        
        Args:
            text: Text to format
            
        Returns:
            Error-formatted text
        """
        return self.colorize(text, 'error')
    
    def success(self, text: str) -> str:
        """Format as success.
        
        Args:
            text: Text to format
            
        Returns:
            Success-formatted text
        """
        return self.colorize(text, 'success')
    
    def warning(self, text: str) -> str:
        """Format as warning.
        
        Args:
            text: Text to format
            
        Returns:
            Warning-formatted text
        """
        return self.colorize(text, 'warning')
    
    def info(self, text: str) -> str:
        """Format as info.
        
        Args:
            text: Text to format
            
        Returns:
            Info-formatted text
        """
        return self.colorize(text, 'info')
    
    def format_value(self, value: Any) -> str:
        """Format a value with appropriate color.
        
        Args:
            value: Value to format
            
        Returns:
            Formatted value string
        """
        if value is None:
            return self.null('null')
        elif isinstance(value, bool):
            return self.boolean(str(value).lower())
        elif isinstance(value, int):
            return self.number(str(value))
        elif isinstance(value, float):
            return self.number(str(value))
        elif isinstance(value, str):
            return self.string(f'"{value}"')
        else:
            return str(value)
    
    def highlight_json(self, json_str: str) -> str:
        """Highlight JSON string with colors.
        
        Args:
            json_str: JSON string to highlight
            
        Returns:
            Highlighted JSON string
        """
        if not self.enabled:
            return json_str
        
        result = []
        i = 0
        
        while i < len(json_str):
            char = json_str[i]
            
            if char == '"':
                # String
                j = i + 1
                while j < len(json_str):
                    if json_str[j] == '\\' and j + 1 < len(json_str):
                        j += 2
                    elif json_str[j] == '"':
                        j += 1
                        break
                    else:
                        j += 1
                result.append(self.string(json_str[i:j]))
                i = j
            elif char.isdigit() or (char == '-' and i + 1 < len(json_str) and json_str[i + 1].isdigit()):
                # Number
                j = i + 1
                while j < len(json_str) and (json_str[j].isdigit() or json_str[j] in '.eE+-'):
                    j += 1
                result.append(self.number(json_str[i:j]))
                i = j
            elif json_str[i:i+4] == 'true' or json_str[i:i+5] == 'false':
                # Boolean
                if json_str[i:i+4] == 'true':
                    result.append(self.boolean('true'))
                    i += 4
                else:
                    result.append(self.boolean('false'))
                    i += 5
            elif json_str[i:i+4] == 'null':
                # Null
                result.append(self.null('null'))
                i += 4
            elif char.isalpha() or char == '_':
                # Key (unquoted)
                j = i
                while j < len(json_str) and (json_str[j].isalnum() or json_str[j] == '_'):
                    j += 1
                result.append(self.key(json_str[i:j]))
                i = j
            else:
                result.append(char)
                i += 1
        
        return ''.join(result)


# Global color formatter instance
_color = ColorFormatter()


def colorize(text: str, color: str) -> str:
    """Colorize text.
    
    Args:
        text: Text to colorize
        color: Color name
        
    Returns:
        Colorized text
    """
    return _color.colorize(text, color)


def format_value(value: Any) -> str:
    """Format value with color.
    
    Args:
        value: Value to format
        
    Returns:
        Formatted value
    """
    return _color.format_value(value)


def highlight_json(json_str: str) -> str:
    """Highlight JSON string.
    
    Args:
        json_str: JSON string
        
    Returns:
        Highlighted string
    """
    return _color.highlight_json(json_str)
