#!/usr/bin/env python3
"""
Topic: Unittests and Integration Tests
Author: Khotso Selading
Date: 01-02-2024
"""
import unittest
from unittest.mock import MagicMock, Mock, patch
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized, param  # type: ignore
from typing import Dict, Sequence, Union


class TestAccessNestedMap(unittest.TestCase):
    """Test class for utils.access_nested_map."""

    @parameterized.expand(
        [
            param(nested_map={"a": 1}, path=("a",), result=1),
            param(nested_map={"a": {"b": 2}}, path=("a",), result={"b": 2}),
            param(nested_map={"a": {"b": 2}}, path=("a", "b"), result=2),
        ]
    )
    def test_access_nested_map(
        self, nested_map: Dict, path: Sequence, result: Union[Dict, int]
    ):
        """Test the utils.access_nested_map method."""
        self.assertEqual(access_nested_map(nested_map, path), result)

    @parameterized.expand(
        [
            param(nested_map={}, path=("a",)),
            param(nested_map={"a": 1}, path=("a", "b")),
        ]
    )
    def test_access_nested_map_exception(
        self, nested_map: Dict, path: Sequence
    ):
        """Test KeyError exception raise in utils.access_nested_map."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)

        msg = str(context.exception).strip("'")
        self.assertEqual(msg, path[-1])


class TestGetJson(unittest.TestCase):
    """Creates a mock for testing HTTP requests in get_json."""

    @parameterized.expand(
        [
            param(
                test_url="http://example.com", test_payload={"payload": True}
            ),
            param(
                test_url="http://holberton.io", test_payload={"payload": False}
            ),
        ]
    )
    @patch("utils.requests.get")
    def test_get_json(
        self,
        response: Union[MagicMock, Mock],
        test_url: str,
        test_payload: Dict[str, bool],
    ):
        """Test JSON response from HTTP request."""
        json = Mock(return_value=test_payload)
        response.return_value.json = json
        self.assertEqual(test_payload, get_json(test_url))


class TestMemoize(unittest.TestCase):
    """A class for testing memoization of the @memoize decorator."""

    def test_memoize(self):
        """Test the @memoize decorator."""

        class TestClass:
            """Dummy class for testing memoize method."""

            def a_method(self):
                """Method to be memoized."""
                return 42

            @memoize
            def a_property(self):
                """The memoized property that calls a_method."""
                return self.a_method()

        with patch.object(
            TestClass, "a_method", new_callable=Mock
        ) as mock_a_method:
            """Mocking the a_method."""
            mock_a_method.return_value = 42
            test_obj = TestClass()
            self.assertEqual(test_obj.a_property, 42)
            self.assertEqual(test_obj.a_property, 42)
            mock_a_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
