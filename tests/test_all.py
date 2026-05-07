#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for DataMorph."""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datamorph.parsers import JSONParser, YAMLParser, TOMLParser, CSVParser
from datamorph.query import query_data
from datamorph.formatters import TableFormatter, TreeFormatter


class TestJSONParser(unittest.TestCase):
    """Test JSON parser."""
    
    def test_parse(self):
        """Test parsing JSON string."""
        data = '{"name": "test", "value": 123}'
        result = JSONParser.parse(data)
        self.assertEqual(result['name'], 'test')
        self.assertEqual(result['value'], 123)
    
    def test_stringify(self):
        """Test stringifying to JSON."""
        data = {'name': 'test', 'value': 123}
        result = JSONParser.stringify(data)
        self.assertIn('"name"', result)
        self.assertIn('"test"', result)
    
    def test_validate(self):
        """Test validation."""
        self.assertTrue(JSONParser.validate('{"valid": true}'))
        self.assertFalse(JSONParser.validate('{"invalid": }'))
    
    def test_minify(self):
        """Test minification."""
        data = '{"name": "test", "value": 123}'
        result = JSONParser.minify(data)
        self.assertNotIn(' ', result)
        self.assertNotIn('\n', result)


class TestYAMLParser(unittest.TestCase):
    """Test YAML parser."""
    
    def test_parse(self):
        """Test parsing YAML string."""
        data = '''
name: test
value: 123
items:
  - a
  - b
'''
        result = YAMLParser.parse(data)
        self.assertEqual(result['name'], 'test')
        self.assertEqual(result['value'], 123)
        self.assertEqual(result['items'], ['a', 'b'])
    
    def test_stringify(self):
        """Test stringifying to YAML."""
        data = {'name': 'test', 'value': 123}
        result = YAMLParser.stringify(data)
        self.assertIn('name:', result)
        self.assertIn('test', result)


class TestTOMLParser(unittest.TestCase):
    """Test TOML parser."""
    
    def test_parse(self):
        """Test parsing TOML string."""
        data = '''
name = "test"
value = 123

[items]
a = 1
b = 2
'''
        result = TOMLParser.parse(data)
        self.assertEqual(result['name'], 'test')
        self.assertEqual(result['value'], 123)
        self.assertEqual(result['items']['a'], 1)
    
    def test_stringify(self):
        """Test stringifying to TOML."""
        data = {'name': 'test', 'value': 123}
        result = TOMLParser.stringify(data)
        self.assertIn('name =', result)
        self.assertIn('test', result)


class TestCSVParser(unittest.TestCase):
    """Test CSV parser."""
    
    def test_parse(self):
        """Test parsing CSV string."""
        data = '''name,value
test,123
foo,456'''
        result = CSVParser.parse(data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'test')
        self.assertEqual(result[0]['value'], 123)
    
    def test_stringify(self):
        """Test stringifying to CSV."""
        data = [{'name': 'test', 'value': 123}]
        result = CSVParser.stringify(data)
        self.assertIn('name,value', result)
        self.assertIn('test,123', result)


class TestQueryEngine(unittest.TestCase):
    """Test query engine."""
    
    def test_field_access(self):
        """Test field access."""
        data = {'name': 'test', 'value': 123}
        result = query_data(data, 'name')
        self.assertEqual(result, 'test')
    
    def test_nested_access(self):
        """Test nested field access."""
        data = {'user': {'name': 'test'}}
        result = query_data(data, 'user.name')
        self.assertEqual(result, 'test')
    
    def test_array_access(self):
        """Test array access."""
        data = {'items': ['a', 'b', 'c']}
        result = query_data(data, 'items[0]')
        self.assertEqual(result, 'a')
    
    def test_filter(self):
        """Test filtering."""
        data = {
            'users': [
                {'name': 'Alice', 'age': 30},
                {'name': 'Bob', 'age': 25},
            ]
        }
        result = query_data(data, 'users[?age > 28]')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Alice')


class TestFormatters(unittest.TestCase):
    """Test formatters."""
    
    def test_table_formatter(self):
        """Test table formatting."""
        data = [{'name': 'test', 'value': 123}]
        formatter = TableFormatter(data)
        result = formatter.format()
        self.assertIn('name', result)
        self.assertIn('test', result)
    
    def test_tree_formatter(self):
        """Test tree formatting."""
        data = {'name': 'test', 'items': ['a', 'b']}
        formatter = TreeFormatter(data)
        result = formatter.format()
        self.assertIn('name', result)
        self.assertIn('items', result)


if __name__ == '__main__':
    unittest.main()
