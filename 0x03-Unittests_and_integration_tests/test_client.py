#!/usr/bin/env python3

"""
Topic: Unittests and Integration Tests
Author: Khotso Selading
Date: 01-02-2024
"""
import unittest
from unittest.mock import MagicMock, patch, PropertyMock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class, param
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
GREPOS = [
    {
        "id": 123456789,
        "name": "example-repo",
        "full_name": "google/example-repo",
        "description": "An example repository from Google",
        "html_url": "https://github.com/google/example-repo",
        "created_at": "2022-01-01T12:00:00Z",
        "updated_at": "2022-02-01T14:30:00Z",
    },
    {
        "id": 123456799,
        "name": "example-repo2",
        "full_name": "google/example-repo",
        "description": "An example repository from Google",
        "html_url": "https://github.com/google/example-repo",
        "created_at": "2022-01-01T12:00:00Z",
        "updated_at": "2022-02-01T14:30:00Z",
    },
]
ABCPAYLOAD = {
    "message": "Not Found",
    "documentation_url":
    "https://docs.github.com/rest/orgs/orgs#get-an-organization",
}

ORGPAYLOAD = TEST_PAYLOAD[0][0]
REPOSPAYLOAD = TEST_PAYLOAD[0][1]
EXPECTED_REPOS = TEST_PAYLOAD[0][2]
APACHE2_REPOS = TEST_PAYLOAD[0][3]


class TestGithubOrgClient(unittest.TestCase):
    """Test responses for a GitHub organization client."""

    @parameterized.expand([("google", GPAYLOAD), ("abc", ABCPAYLOAD)])
    @patch("utils.get_json")
    def test_org(self, org: str, response: Dict, mock_get_json: MagicMock):
        """Test basic response of method calls."""
        mock_get_json.return_value = response
        mock_get_json.return_value = response
        result = GithubOrgClient(org)
        self.assertEqual(result.org, response)
        self.assertEqual(result.org, response)
        mock_get_json.assert_called_once()

    def test_public_repos_url(self):
        """Test the _public_repos_url property."""
        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as cm:
            cm.return_value = GPAYLOAD
            cli = GithubOrgClient("google")
            self.assertEqual(
                cli._public_repos_url,
                "https://api.github.com/orgs/google/repos",
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock):
        """Test the public_repos() method with mocking."""
        mock_get_json.return_value = GREPOS
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as cm:
            cm.return_value = "https://api.github.com/orgs/google/repos"
            cli = GithubOrgClient("google")
            response = cli.public_repos()
            expected = ["example-repo", "example-repo2"]
            for rname in response:
                self.assertIn(rname, expected)
            mock_get_json.assert_called_once()
            cm.assert_called_once()

    @parameterized.expand([
        param(repo={"license": {"key": "my_license"}},
              license_key="my_license", result=True),
        param(repo={"license": {"key": "other_license"}},
              license_key="my_license", result=False)
    ])
    def test_has_license(self, repo: Dict, license_key: str, result=bool):
        """Check if a repo has the specified license key."""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key), result)


def requests_get(*args, **kwargs):
    """
    Function that mocks requests.get function.
    Returns the correct JSON data based on the given input URL.
    """
    class MockResponse:
        """
        Mock response class.
        """

        def __init__(self, json_data):
            self.json_data = json_data

        def json(self):
            return self.json_data

    if args[0] == "https://api.github.com/orgs/google":
        return MockResponse(TEST_PAYLOAD[0][0])
    if args[0] == TEST_PAYLOAD[0][0]["repos_url"]:
        return MockResponse(TEST_PAYLOAD[0][1])


@parameterized_class([{
    "org_payload": ORGPAYLOAD,
    "repos_payload": REPOSPAYLOAD,
    "expected_repos": EXPECTED_REPOS,
    "apache2_repos": APACHE2_REPOS
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test for the GithubOrgClient.public_repos method.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up function for TestIntegrationGithubOrgClient class.
        Sets up a patcher to be used in the class methods.
        """
        cls.get_patcher = patch('utils.requests.get', side_effect=requests_get)
        cls.get_patcher.start()
        cls.client = GithubOrgClient('google')

    @classmethod
    def tearDownClass(cls):
        """
        Tear down resources set up for class tests.
        Stops the patcher that had been started.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test public_repos method without license.
        """
        self.assertEqual(self.client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test public_repos method with license.
        """
        self.assertEqual(
            self.client.public_repos(license="apache-2.0"),
            self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
