#!/usr/bin/env python3

"""
Topic: Unittests and Integration Tests
Author: Khotso Selading
Date: 01-02-2024
"""

import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from client import GithubOrgClient, get_json
from parameterized import parameterized, parameterized_class
from utils import memoize
from fixtures import TEST_PAYLOAD
from typing import Dict


GPAYLOAD = {
    "login": "google",
    "id": 1342004,
    "url": "https://api.github.com/orgs/google",
    "description": "Google ❤️ Open Source",
    "name": "Google",
    "repos_url": "https://api.github.com/orgs/google/repos",
    "email": "opensource@google.com",
    "twitter_username": "GoogleOSS",
    "followers": 35341,
    "following": 0,
    "created_at": "2012-01-18T01:30:18Z",
    "updated_at": "2021-12-30T01:40:20Z",
}

ORGPAYLOAD = TEST_PAYLOAD[0][0]
REPOSPAYLOAD = TEST_PAYLOAD[0][1]
EXPECTED_REPOS = TEST_PAYLOAD[0][2]
APACHE2_REPOS = TEST_PAYLOAD[0][3]


class TestGithubOrgClient(unittest.TestCase):
    """
    TestGithubOrgClient
    """
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: MagicMock):
        """
        test_org
        """
        mock_get_json.return_value = {"repos_url": "http://example.com"}
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
            )
        self.assertEqual(result, mock_get_json.return_value)

    def test_public_repos_url(self):
        """tests the _public_repos_url property"""
        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as cm:
            cm.return_value = GPAYLOAD
            cli = GithubOrgClient("google")
            self.assertEqual(
                cli._public_repos_url,
                "https://api.github.com/orgs/google/repos",
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo: Dict, license_key: str,
                         expected_result: bool):
        """
        test_org
        """
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key), expected_result)


def requests_get(*args, **kwargs):
    """
    Function that mocks requests.get function
    Returns the correct json data based on the given input url
    """
    class MockResponse:
        """
        Mock response
        """

        def __init__(self, json_data):
            self.json_data = json_data

        def json(self):
            return self.json_data

    if args[0] == "https://api.github.com/orgs/google":
        return MockResponse(TEST_PAYLOAD[0][0])
    if args[0] == TEST_PAYLOAD[0][0]["repos_url"]:
        return MockResponse(TEST_PAYLOAD[0][1])


@parameterized_class([{"org_payload": ORGPAYLOAD,
                       "repos_payload": REPOSPAYLOAD,
                       "expected_repos": EXPECTED_REPOS,
                       "apache2_repos": APACHE2_REPOS}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    test_org
    """

    @classmethod
    def setUpClass(cls):
        """
        test_org
        """
        cls.get_patcher = patch('utils.requests.get', side_effect=requests_get)
        cls.mock_requests_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """
        test_org
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        test_org
        """
        client = GithubOrgClient("google")
        self.mock_requests_get.side_effect = [
            Mock(json=lambda: self.org_payload),
            Mock(json=lambda: self.repos_payload)
        ]
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        test_org
        """
        client = GithubOrgClient("google")
        self.mock_requests_get.side_effect = [
            Mock(json=lambda: self.org_payload),
            Mock(json=lambda: self.repos_payload)
        ]
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
