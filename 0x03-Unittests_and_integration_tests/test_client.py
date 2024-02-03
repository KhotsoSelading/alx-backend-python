#!/usr/bin/env python3

"""
Topic: Unittests and Integration Tests
Author: Khotso Selading
Date: 01-02-2024
"""

from unittest.mock import patch, Mock
from client import GithubOrgClient, get_json
from parameterized import parameterized, parameterized_class
from utils import memoize
import unittest
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        mock_get_json.return_value = {"repos_url": "http://example.com"}
        client = GithubOrgClient(org_name)
        result = client.org()
        mock_get_json.assert_called_once_with("http://example.com")
        self.assertEqual(result, mock_get_json.return_value)

    @patch('client.GithubOrgClient.org',
           return_value={"repos_url": "http://example.com"})
    def test_public_repos_url(self, mock_org):
        client = GithubOrgClient("google")
        result = client._public_repos_url()
        mock_org.assert_called_once()
        self.assertEqual(result, "http://example.com/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected_result):
        client = GithubOrgClient("google")
        with patch('client.GithubOrgClient._public_repos_url',
                   return_value="http://example.com/repos"), \
             patch('client.get_json', return_value=[repo]):
            result = client.has_license(license_key)
        self.assertEqual(result, expected_result)


@parameterized_class("org_payload", "repos_payload", "expected_repos",
                     "apache2_repos")
class TestIntegrationGithubOrgClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch('client.requests.get')
        cls.mock_requests_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("google")
        self.mock_requests_get.side_effect = [
            Mock(json=lambda: self.org_payload),
            Mock(json=lambda: self.repos_payload)
        ]
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("google")
        self.mock_requests_get.side_effect = [
            Mock(json=lambda: self.org_payload),
            Mock(json=lambda: self.repos_payload)
        ]
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


class TestMemoize(unittest.TestCase):

    class TestClass:

        def a_method(self):
            return 42

        @memoize
        def a_property(self):
            return self.a_method()

    @patch.object(TestClass, 'a_method')
    def test_memoize(self, mock_a_method):
        instance = self.TestClass()
        result_1 = instance.a_property()
        result_2 = instance.a_property()
        mock_a_method.assert_called_once()
        self.assertEqual(result_1, result_2)


class TestGetJson(unittest.TestCase):

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('client.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        mock_get.return_value.json.return_value = test_payload
        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


if __name__ == "__main__":
    unittest.main()
