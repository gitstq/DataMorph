#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DataMorph CLI - Lightweight Terminal Data Processing Swiss Army Knife
轻量级终端数据处理瑞士军刀

A zero-dependency CLI tool for JSON/YAML/TOML/CSV data processing.
"""

import argparse
import sys
import os
from typing import Any, Dict, List, Optional

from .parsers import JSONParser, YAMLParser, TOMLParser, CSVParser
from .query import query_data
from .formatters import TableFormatter, TreeFormatter, ColorFormatter, highlight_json


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser.
    
    Returns:
        Argument parser
    """
    parser = argparse.ArgumentParser(
        prog='datamorph',
        description='🔄 DataMorph - Lightweight Terminal Data Processing Swiss Army Knife',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Convert JSON to YAML
  datamorph convert input.json output.yaml
  
  # Query JSON data
  datamorph query 'users[*].name' < data.json
  
  # Format as table
  datamorph table data.csv
  
  # Show as tree
  datamorph tree data.json
  
  # Validate JSON
  datamorph validate data.json
  
  # Minify JSON
  datamorph minify data.json
'''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert between formats')
    convert_parser.add_argument('input', help='Input file path (use - for stdin)')
    convert_parser.add_argument('output', help='Output file path (use - for stdout)')
    convert_parser.add_argument('-f', '--from', dest='from_format', 
                                choices=['json', 'yaml', 'toml', 'csv'],
                                help='Input format (auto-detect if not specified)')
    convert_parser.add_argument('-t', '--to', dest='to_format',
                                choices=['json', 'yaml', 'toml', 'csv'],
                                required=True, help='Output format')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Query data with expression')
    query_parser.add_argument('expression', help='Query expression')
    query_parser.add_argument('-i', '--input', help='Input file (default: stdin)')
    query_parser.add_argument('-f', '--format', dest='input_format',
                              choices=['json', 'yaml', 'toml', 'csv'],
                              default='json', help='Input format')
    
    # Table command
    table_parser = subparsers.add_parser('table', help='Format data as table')
    table_parser.add_argument('input', nargs='?', help='Input file (default: stdin)')
    table_parser.add_argument('-f', '--format', dest='input_format',
                              choices=['json', 'yaml', 'toml', 'csv'],
                              help='Input format (auto-detect if not specified)')
    table_parser.add_argument('-c', '--columns', help='Columns to display (comma-separated)')
    table_parser.add_argument('-w', '--width', type=int, default=120, help='Max table width')
    
    # Tree command
    tree_parser = subparsers.add_parser('tree', help='Format data as tree')
    tree_parser.add_argument('input', nargs='?', help='Input file (default: stdin)')
    tree_parser.add_argument('-f', '--format', dest='input_format',
                             choices=['json', 'yaml', 'toml', 'csv'],
                             help='Input format (auto-detect if not specified)')
    tree_parser.add_argument('-d', '--depth', type=int, default=5, help='Max depth')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate data format')
    validate_parser.add_argument('input', help='Input file')
    validate_parser.add_argument('-f', '--format', dest='input_format',
                                 choices=['json', 'yaml', 'toml', 'csv'],
                                 help='Format to validate (auto-detect if not specified)')
    
    # Minify command
    minify_parser = subparsers.add_parser('minify', help='Minify JSON')
    minify_parser.add_argument('input', nargs='?', help='Input file (default: stdin)')
    minify_parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    
    # Pretty command
    pretty_parser = subparsers.add_parser('pretty', help='Pretty print JSON')
    pretty_parser.add_argument('input', nargs='?', help='Input file (default: stdin)')
    pretty_parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    pretty_parser.add_argument('-i', '--indent', type=int, default=2, help='Indentation')
    pretty_parser.add_argument('--no-color', action='store_true', help='Disable colors')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show data info')
    info_parser.add_argument('input', nargs='?', help='Input file (default: stdin)')
    info_parser.add_argument('-f', '--format', dest='input_format',
                             choices=['json', 'yaml', 'toml', 'csv'],
                             help='Input format (auto-detect if not specified)')
    
    return parser


def detect_format(filepath: str) -> str:
    """Detect file format from extension.
    
    Args:
        filepath: File path
        
    Returns:
        Detected format
    """
    ext = os.path.splitext(filepath)[1].lower()
    format_map = {
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.toml': 'toml',
        '.csv': 'csv',
    }
    return format_map.get(ext, 'json')


def read_input(input_path: Optional[str], input_format: Optional[str] = None) -> tuple:
    """Read input data.
    
    Args:
        input_path: Input file path (None for stdin)
        input_format: Input format (None for auto-detect)
        
    Returns:
        Tuple of (data, format)
    """
    if input_path is None or input_path == '-':
        data = sys.stdin.read()
        format_name = input_format or 'json'
    else:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = f.read()
        format_name = input_format or detect_format(input_path)
    
    return data, format_name


def parse_data(data: str, format_name: str) -> Any:
    """Parse data based on format.
    
    Args:
        data: Data string
        format_name: Format name
        
    Returns:
        Parsed data
    """
    parsers = {
        'json': JSONParser.parse,
        'yaml': YAMLParser.parse,
        'toml': TOMLParser.parse,
        'csv': lambda d: CSVParser.parse(d, has_header=True),
    }
    
    if format_name not in parsers:
        raise ValueError(f"Unknown format: {format_name}")
    
    return parsers[format_name](data)


def stringify_data(data: Any, format_name: str) -> str:
    """Stringify data to format.
    
    Args:
        data: Data to stringify
        format_name: Target format
        
    Returns:
        Formatted string
    """
    if format_name == 'json':
        return JSONParser.stringify(data, indent=2)
    elif format_name == 'yaml':
        return YAMLParser.stringify(data)
    elif format_name == 'toml':
        return TOMLParser.stringify(data)
    elif format_name == 'csv':
        return CSVParser.stringify(data) if isinstance(data, list) else str(data)
    else:
        raise ValueError(f"Unknown format: {format_name}")


def write_output(data: str, output_path: Optional[str]):
    """Write output data.
    
    Args:
        data: Data string to write
        output_path: Output file path (None for stdout)
    """
    if output_path is None or output_path == '-':
        print(data)
    else:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(data)


def cmd_convert(args):
    """Handle convert command."""
    # Read input
    data, from_format = read_input(args.input, args.from_format)
    
    # Parse
    parsed = parse_data(data, from_format)
    
    # Convert
    result = stringify_data(parsed, args.to_format)
    
    # Write output
    write_output(result, args.output)
    
    return 0


def cmd_query(args):
    """Handle query command."""
    # Read input
    data, format_name = read_input(args.input, args.input_format)
    
    # Parse
    parsed = parse_data(data, format_name)
    
    # Query
    result = query_data(parsed, args.expression)
    
    # Output
    if isinstance(result, (dict, list)):
        print(JSONParser.stringify(result, indent=2))
    else:
        print(result)
    
    return 0


def cmd_table(args):
    """Handle table command."""
    # Read input
    data, format_name = read_input(args.input, args.input_format)
    
    # Parse
    parsed = parse_data(data, format_name)
    
    # Get columns
    columns = args.columns.split(',') if args.columns else None
    
    # Format
    formatter = TableFormatter(parsed, max_width=args.width)
    print(formatter.format(columns))
    
    return 0


def cmd_tree(args):
    """Handle tree command."""
    # Read input
    data, format_name = read_input(args.input, args.input_format)
    
    # Parse
    parsed = parse_data(data, format_name)
    
    # Format
    formatter = TreeFormatter(parsed, max_depth=args.depth)
    print(formatter.format())
    
    return 0


def cmd_validate(args):
    """Handle validate command."""
    # Read input
    data, format_name = read_input(args.input, args.input_format)
    
    # Validate
    validators = {
        'json': JSONParser.validate,
        'yaml': YAMLParser.validate,
        'toml': TOMLParser.validate,
        'csv': CSVParser.validate,
    }
    
    is_valid = validators[format_name](data)
    
    if is_valid:
        print(f"✅ Valid {format_name.upper()}")
        return 0
    else:
        print(f"❌ Invalid {format_name.upper()}")
        return 1


def cmd_minify(args):
    """Handle minify command."""
    # Read input
    data, _ = read_input(args.input, 'json')
    
    # Minify
    result = JSONParser.minify(data)
    
    # Write output
    write_output(result, args.output)
    
    return 0


def cmd_pretty(args):
    """Handle pretty command."""
    # Read input
    data, _ = read_input(args.input, 'json')
    
    # Parse
    parsed = JSONParser.parse(data)
    
    # Pretty print
    result = JSONParser.stringify(parsed, indent=args.indent)
    
    # Add colors if enabled
    if not args.no_color and sys.stdout.isatty():
        result = highlight_json(result)
    
    # Write output
    write_output(result, args.output)
    
    return 0


def cmd_info(args):
    """Handle info command."""
    # Read input
    data, format_name = read_input(args.input, args.input_format)
    
    # Parse
    parsed = parse_data(data, format_name)
    
    # Get info
    info = get_data_info(parsed)
    
    # Print info
    print(f"📊 Data Information")
    print(f"   Format: {format_name.upper()}")
    print(f"   Type: {info['type']}")
    print(f"   Size: {info['size']} items" if info['size'] else "")
    print(f"   Depth: {info['depth']}")
    if info['keys']:
        print(f"   Keys: {', '.join(info['keys'][:10])}" + ("..." if len(info['keys']) > 10 else ""))
    
    return 0


def get_data_info(data: Any, depth: int = 0) -> Dict:
    """Get information about data.
    
    Args:
        data: Data to analyze
        depth: Current depth
        
    Returns:
        Info dictionary
    """
    info = {
        'type': type(data).__name__,
        'size': None,
        'depth': depth,
        'keys': [],
    }
    
    if isinstance(data, dict):
        info['size'] = len(data)
        info['keys'] = list(data.keys())
        max_child_depth = depth
        for value in data.values():
            child_info = get_data_info(value, depth + 1)
            max_child_depth = max(max_child_depth, child_info['depth'])
        info['depth'] = max_child_depth
    elif isinstance(data, list):
        info['size'] = len(data)
        max_child_depth = depth
        for item in data:
            child_info = get_data_info(item, depth + 1)
            max_child_depth = max(max_child_depth, child_info['depth'])
        info['depth'] = max_child_depth
    
    return info


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    commands = {
        'convert': cmd_convert,
        'query': cmd_query,
        'table': cmd_table,
        'tree': cmd_tree,
        'validate': cmd_validate,
        'minify': cmd_minify,
        'pretty': cmd_pretty,
        'info': cmd_info,
    }
    
    if args.command in commands:
        try:
            return commands[args.command](args)
        except FileNotFoundError as e:
            print(f"❌ Error: {e}", file=sys.stderr)
            return 1
        except ValueError as e:
            print(f"❌ Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"❌ Unexpected error: {e}", file=sys.stderr)
            return 1
    else:
        parser.print_help()
        return 0


if __name__ == '__main__':
    sys.exit(main())
