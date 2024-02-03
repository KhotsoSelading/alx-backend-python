#!/usr/bin/env python3
"""
Topic: Unittests and Integration Tests
Author: Khotso Selading
Date: 16-01-2024
"""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class."""

    @patch('client.GithubOrgClient.get_json')
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org method with mocked get_json."""
        client = GithubOrgClient(org_name)
        client.org()
        mock_get_json.assert_called_once_with(
            f'https://api.github.com/orgs/{org_name}')

    @patch.object(
            GithubOrgClient, 'org',
            return_value={'repos_url': 'http://example.com'})
    @patch('client.GithubOrgClient.get_json')
    @parameterized.expand([
        ("http://example.com", {"repo1": "data1"}),
        ("http://holberton.io", {"repo2": "data2"})
    ])
    def test_public_repos_url(self, mock_get_json_org, mock_get_json, test_url,
                              test_payload):
        """Test GithubOrgClient._public_repos_url method with mocked get_json
        and org."""
        client = GithubOrgClient("test_org")
        result = client._public_repos_url()
        mock_get_json_org.assert_called_once()
        mock_get_json.assert_called_once_with("http://example.com")
        self.assertEqual(
            result, f'{test_url}?client_id=test_id&client_secret=test_secret')

    @patch('client.GithubOrgClient._public_repos_url',
           return_value='http://example.com')
    @patch('client.GithubOrgClient.get_json')
    @parameterized.expand([
        ({"repo1": "data1"},),
        ({"repo2": "data2"},)
    ])
    def test_public_repos(self, mock_get_json_url, mock_get_json,
                          repos_payload):
        """Test GithubOrgClient.public_repos method with mocked get_json and
        public_repos_url."""
        client = GithubOrgClient("test_org")
        result = client.public_repos()
        mock_get_json_url.assert_called_once()
        mock_get_json.assert_called_once_with('http://example.com')
        self.assertEqual(result, repos_payload)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """Test GithubOrgClient.has_license method with various inputs."""
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


@parameterized_class(('org_payload', 'repos_payload', 'expected_repos',
                      'apache2_repos'), [
    (org_payload, repos_payload, expected_repos, apache2_repos)
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test cases for the GithubOrgClient class."""
    @classmethod
    @patch('client.requests.get')
    def setUpClass(cls, mock_requests_get):
        """Set up the class with mock requests.get."""
        cls.get_patcher = patch('client.requests.get')
        cls.mock_requests_get = mock_requests_get
        cls.mock_requests_get.side_effect = cls.side_effect
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down the class and stop the patcher."""
        cls.get_patcher.stop()

    @staticmethod
    def side_effect(url):
        """Side effect method to return corresponding
        payloads based on the URL."""
        if 'orgs/test_org' in url:
            return Mock(json=Mock(return_value=org_payload))
        elif 'orgs/test_org/repos' in url:
            return Mock(json=Mock(return_value=repos_payload))
        else:
            return Mock(json=Mock(return_value={}))

    def test_public_repos(self):
        """Test GithubOrgClient.public_repos method in an integration test."""
        client = GithubOrgClient("test_org")
        result = client.public_repos()
        self.assertEqual(result, expected_repos)

    def test_public_repos_with_license(self):
        """Test GithubOrgClient.public_repos method with license
        argument in an integration test."""
        client = GithubOrgClient("test_org")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, apache2_repos)


if __name__ == "__main__":
    unittest.main()
