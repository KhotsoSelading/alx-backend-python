#!/usr/bin/env python3
"""
Topic: Unittests and Integration Tests
Author: Khotso Selading
Date: 01-02-2024
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, memoize, get_json
from typing import Dict, Sequence, Union


class TestAccessNestedMap(unittest.TestCase):
    """
    test_org
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map: Dict, path: Sequence,
                               expected_result: Union[Dict, int]):
        """ test_org """
        self.assertEqual(access_nested_map(nested_map, path), expected_result)


if __name__ == "__main__":
    unittest.main()
