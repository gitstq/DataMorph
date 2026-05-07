#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CSV parser for DataMorph."""

import csv
import sys
from typing import Any, Dict, List, Optional, Union
from io import StringIO


class CSVParser:
    """CSV parser with streaming support and flexible options."""
    
    @staticmethod
    def parse(data: str, delimiter: str = ',', quotechar: str = '"',
              has_header: bool = True, encoding: str = "utf-8") -> List[Dict[str, Any]]:
        """Parse CSV string to list of dictionaries.
        
        Args:
            data: CSV string to parse
            delimiter: Field delimiter (default: ',')
            quotechar: Quote character (default: '"')
            has_header: Whether first row is header (default: True)
            encoding: String encoding
            
        Returns:
            List of dictionaries (if has_header) or list of lists
        """
        reader = csv.reader(StringIO(data), delimiter=delimiter, quotechar=quotechar)
        rows = list(reader)
        
        if not rows:
            return []
        
        if has_header:
            headers = rows[0]
            result = []
            for row in rows[1:]:
                if row:  # Skip empty rows
                    row_dict = {}
                    for i, value in enumerate(row):
                        if i < len(headers):
                            row_dict[headers[i]] = CSVParser._parse_value(value)
                    result.append(row_dict)
            return result
        else:
            return [[CSVParser._parse_value(cell) for cell in row] for row in rows if row]
    
    @staticmethod
    def parse_file(filepath: str, delimiter: str = ',', quotechar: str = '"',
                   has_header: bool = True, encoding: str = "utf-8") -> List[Dict[str, Any]]:
        """Parse CSV file to list of dictionaries.
        
        Args:
            filepath: Path to CSV file
            delimiter: Field delimiter
            quotechar: Quote character
            has_header: Whether first row is header
            encoding: File encoding
            
        Returns:
            List of dictionaries or list of lists
        """
        with open(filepath, "r", encoding=encoding, newline='') as f:
            reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar)
            rows = list(reader)
        
        if not rows:
            return []
        
        if has_header:
            headers = rows[0]
            result = []
            for row in rows[1:]:
                if row:
                    row_dict = {}
                    for i, value in enumerate(row):
                        if i < len(headers):
                            row_dict[headers[i]] = CSVParser._parse_value(value)
                    result.append(row_dict)
            return result
        else:
            return [[CSVParser._parse_value(cell) for cell in row] for row in rows if row]
    
    @staticmethod
    def parse_stream(stream=None, delimiter: str = ',', quotechar: str = '"',
                     has_header: bool = True) -> List[Dict[str, Any]]:
        """Parse CSV from stdin stream.
        
        Args:
            stream: Input stream (default: stdin)
            delimiter: Field delimiter
            quotechar: Quote character
            has_header: Whether first row is header
            
        Returns:
            List of dictionaries or list of lists
        """
        if stream is None:
            stream = sys.stdin
        data = stream.read()
        return CSVParser.parse(data, delimiter, quotechar, has_header)
    
    @staticmethod
    def stringify(data: List[Any], delimiter: str = ',', quotechar: str = '"',
                  include_header: bool = True, encoding: str = "utf-8") -> str:
        """Convert list of dictionaries to CSV string.
        
        Args:
            data: List of dictionaries or list of lists
            delimiter: Field delimiter
            quotechar: Quote character
            include_header: Whether to include header row
            encoding: String encoding
            
        Returns:
            CSV string
        """
        if not data:
            return ""
        
        output = StringIO()
        writer = csv.writer(output, delimiter=delimiter, quotechar=quotechar)
        
        if isinstance(data[0], dict):
            # List of dictionaries
            headers = list(data[0].keys())
            if include_header:
                writer.writerow(headers)
            for row in data:
                writer.writerow([row.get(h, '') for h in headers])
        else:
            # List of lists
            for row in data:
                writer.writerow(row)
        
        return output.getvalue()
    
    @staticmethod
    def validate(data: str, delimiter: str = ',', quotechar: str = '"') -> bool:
        """Validate CSV string.
        
        Args:
            data: CSV string to validate
            delimiter: Field delimiter
            quotechar: Quote character
            
        Returns:
            True if valid, False otherwise
        """
        try:
            reader = csv.reader(StringIO(data), delimiter=delimiter, quotechar=quotechar)
            list(reader)
            return True
        except csv.Error:
            return False
    
    @staticmethod
    def _parse_value(value: str) -> Any:
        """Parse a string value to appropriate Python type.
        
        Args:
            value: String value to parse
            
        Returns:
            Parsed value (int, float, bool, None, or string)
        """
        if not value or value.strip() == '':
            return None
        
        value = value.strip()
        
        # Boolean
        if value.lower() in ('true', 'yes', '1'):
            return True
        if value.lower() in ('false', 'no', '0'):
            return False
        
        # None
        if value.lower() in ('null', 'none', 'nil', ''):
            return None
        
        # Integer
        try:
            return int(value)
        except ValueError:
            pass
        
        # Float
        try:
            return float(value)
        except ValueError:
            pass
        
        return value
    
    @staticmethod
    def detect_delimiter(data: str) -> str:
        """Detect the delimiter used in CSV data.
        
        Args:
            data: CSV string
            
        Returns:
            Detected delimiter character
        """
        delimiters = [',', ';', '\t', '|', ':']
        lines = data.strip().split('\n')
        
        if not lines:
            return ','
        
        # Count occurrences in first few lines
        counts = {d: 0 for d in delimiters}
        for line in lines[:5]:
            for d in delimiters:
                counts[d] += line.count(d)
        
        # Return the most common delimiter
        return max(counts, key=counts.get) if max(counts.values()) > 0 else ','
    
    @staticmethod
    def get_columns(data: List[Dict[str, Any]]) -> List[str]:
        """Get column names from parsed CSV data.
        
        Args:
            data: Parsed CSV data (list of dicts)
            
        Returns:
            List of column names
        """
        if not data or not isinstance(data[0], dict):
            return []
        return list(data[0].keys())
    
    @staticmethod
    def filter_rows(data: List[Dict[str, Any]], column: str, 
                    operator: str, value: Any) -> List[Dict[str, Any]]:
        """Filter rows based on condition.
        
        Args:
            data: Parsed CSV data
            column: Column name to filter on
            operator: Comparison operator (eq, ne, gt, lt, gte, lte, contains)
            value: Value to compare against
            
        Returns:
            Filtered list of rows
        """
        ops = {
            'eq': lambda a, b: a == b,
            'ne': lambda a, b: a != b,
            'gt': lambda a, b: a > b if a is not None and b is not None else False,
            'lt': lambda a, b: a < b if a is not None and b is not None else False,
            'gte': lambda a, b: a >= b if a is not None and b is not None else False,
            'lte': lambda a, b: a <= b if a is not None and b is not None else False,
            'contains': lambda a, b: b in str(a) if a is not None else False,
        }
        
        if operator not in ops:
            raise ValueError(f"Unknown operator: {operator}")
        
        op_func = ops[operator]
        return [row for row in data if column in row and op_func(row[column], value)]
    
    @staticmethod
    def sort_rows(data: List[Dict[str, Any]], column: str, 
                  reverse: bool = False) -> List[Dict[str, Any]]:
        """Sort rows by column.
        
        Args:
            data: Parsed CSV data
            column: Column name to sort by
            reverse: Sort in descending order
            
        Returns:
            Sorted list of rows
        """
        return sorted(data, key=lambda x: (x.get(column) is None, x.get(column)), reverse=reverse)
