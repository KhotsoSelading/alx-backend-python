#!/usr/bin/env python3
"""
Topic: Unittests and Integration Tests
Author: Khotso Selading
Date: 16-01-2024
"""

import unittest
from unittest.mock import MagicMock, patch, PropertyMock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class, param
from typing import Dict

TEST_PAYLOAD_INDEX = 0
GPAYLOAD, GREPOS, ABCPAYLOAD = (
    TEST_PAYLOAD[TEST_PAYLOAD_INDEX][0],
    TEST_PAYLOAD[TEST_PAYLOAD_INDEX][1],
    {
        "message": "Not Found",
        "documentation_url":
        "https://docs.github.com/rest/orgs/orgs#get-an-organization",
    },
)

ORGPAYLOAD, REPOSPAYLOAD, EXPECTED_REPOS, APACHE2_REPOS = (
    TEST_PAYLOAD[TEST_PAYLOAD_INDEX])


class TestGithubOrgClient(unittest.TestCase):
    """Tests the responses of the GitHub organization client"""

    @parameterized.expand([("google", GPAYLOAD), ("abc", ABCPAYLOAD)])
    @patch("utils.get_json")
    def test_org(self, org: str, response: Dict, mock_get_json: MagicMock):
        """Checks the response of the org method"""
        mock_get_json.return_value = response
        with patch.object(GithubOrgClient, "org", new_callable=mock_get_json):
            result = GithubOrgClient(org)
            self.assertEqual(result.org, response)
            mock_get_json.assert_called_once()

    def test_public_repos_url(self):
        """Verifies the correctness of the _public_repos_url property"""
        with patch.object(GithubOrgClient, "org",
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = GPAYLOAD
            cli = GithubOrgClient("google")
            self.assertEqual(cli._public_repos_url, GPAYLOAD["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock):
        """Tests the public_repos() method with mock data"""
        mock_get_json.return_value = GREPOS
        with patch.object(GithubOrgClient, "_public_repos_url",
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = "https://api.github.com/orgs/google/repos"
            cli = GithubOrgClient("google")
            response = cli.public_repos()
            expected = ["example-repo", "example-repo2"]
            for rname in response:
                self.assertIn(rname, expected)
            mock_get_json.assert_called_once()
            mock_org.assert_called_once()

    @parameterized.expand([
        param(repo={"license": {"key": "my_license"}},
              license_key="my_license", result=True),
        param(repo={"license": {"key": "other_license"}},
              license_key="my_license", result=False)
    ])
    def test_has_license(self, repo: Dict, license_key: str, result=bool):
        """Checks if a repo has the specified license key"""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key),
                         result)


def requests_get(*args, **kwargs):
    """
    Function that mocks requests.get function
    Returns the correct json data based on the given input URL
    """
    class MockResponse:
        """Mock response"""

        def __init__(self, json_data):
            self.json_data = json_data

        def json(self):
            return self.json_data

    if args[0] == GPAYLOAD["url"]:
        return MockResponse(GPAYLOAD)
    if args[0] == GPAYLOAD["repos_url"]:
        return MockResponse(REPOSPAYLOAD)


@parameterized_class([{
    "org_payload": ORGPAYLOAD,
    "repos_payload": REPOSPAYLOAD,
    "expected_repos": EXPECTED_REPOS,
    "apache2_repos": APACHE2_REPOS
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test for the GithubOrgClient.public_repos method
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up function for TestIntegrationGithubOrgClient class
        Initializes a patcher to be used in the class methods
        """
        cls.get_patcher = patch('utils.requests.get', side_effect=requests_get)
        cls.get_patcher.start()
        cls.client = GithubOrgClient('google')

    @classmethod
    def tearDownClass(cls):
        """
        Tear down resources set up for class tests.
        Stops the patcher that had been started
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method without license"""
        self.assertEqual(self.client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos method with license"""
        self.assertEqual(self.client.public_repos(license="apache-2.0"),
                         self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
