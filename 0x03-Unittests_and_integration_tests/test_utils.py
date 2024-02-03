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


class TestAccessNestedMap(unittest.TestCase):
    """
    test_org
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        """
        test_org
        """
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected_result)

    @parameterized.expand([
        ({}, ("a",), KeyError, "a"),
        ({"a": 1}, ("a", "b"), KeyError, "b")
    ])
    def test_access_nested_map_exception(self, nested_map, path,
                                         expected_exception, expected_message):
        """
        test_org
        """
        with self.assertRaises(expected_exception) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_message)


class TestGetJson(unittest.TestCase):
    """
    test_org
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        test_org
        """
        mock_get.return_value.json.return_value = test_payload
        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    test_org
    """

    class TestClass:
        """
        test_org
        """

        def a_method(self):
            """
            test_org
            """
            return 42

        @memoize
        def a_property(self):
            """
            test_org
            """
            return self.a_method()

    @patch.object(TestClass, 'a_method')
    def test_memoize(self, mock_a_method):
        """
        test_org
        """
        instance = self.TestClass()
        result_1 = instance.a_property()
        result_2 = instance.a_property()
        mock_a_method.assert_called_once()
        self.assertEqual(result_1, result_2)


if __name__ == "__main__":
    unittest.main()
