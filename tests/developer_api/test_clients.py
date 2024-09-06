import json
from unittest.mock import patch, Mock

import pytest

from starter_project.developer_api.clients import DeveloperApiClient
from starter_project.developer_api.filters import Filter


class TestClients:
    TEST_KEY = "some-key"
    TEST_VALUE = "some-value"

    EXAMPLE_ACCOUNT_RESPONSE = {
        "Accounts": [
            {
                "accountId": "66512652",
                "firstname": "Blondell",
                "phoneNumber": "+44873425431",
                "developerId": "123",
                "uci": "103583",
                "riskScore": "22",
                "creditScore": "450",
                "currencyCode": "GBP",
                "productType": "Credit",
                "email": "Blondell.Bartell@emailservice.co.uk",
                "lastname": "Bartell",
                "homeAddress": "72 Richard Road, Oxford, United Kingdom",
                "state": "open",
                "creditLimit": "1000",
                "balance": "1000",
                "liveBalance": "true",
            }
        ]
    }

    EXAMPLE_TRANSACTION_RESPONSE = {
        "Transactions": [
            {
                "transactionUUID": "0673bca4-fbb2-46bd-aa76-36243305ceed",
                "accountUUID": "72965642",
                "merchantUUID": "2",
                "merchant": {
                    "name": "Capital Two",
                    "category": "Bills & Utilities",
                    "description": "Credit Card Company",
                    "pointOfSale": ["Online"],
                },
                "amount": 843.92,
                "creditDebitIndicator": "Debit",
                "currency": "GBP",
                "timestamp": "2019-05-20 10:51:33",
                "emoji": "🤑",
                "latitude": -4.38849,
                "longitude": 52.33594,
                "status": "Successful",
                "message": "Weekly groceries shopping",
                "pointOfSale": "Online",
            },
            {
                "transactionUUID": "093c805f-31c1-4721-8642-b7e9a09964f0",
                "accountUUID": "72965642",
                "merchantUUID": "3",
                "merchant": {
                    "name": "Blahbucks",
                    "category": "Food & Dining",
                    "description": "Supplying all your coffee needs",
                    "pointOfSale": ["In-store"],
                },
                "amount": 517.06,
                "creditDebitIndicator": "Credit",
                "currency": "GBP",
                "timestamp": "2019-07-09 11:47:47",
                "emoji": "🥰",
                "latitude": -1.86852,
                "longitude": 53.39733,
                "status": "Successful",
                "message": "Holiday souvenirs",
                "pointOfSale": "In-store",
            },
        ]
    }

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.client = DeveloperApiClient("dummy-token")

    @patch("requests.get")
    def test_get_account(self, mock_get):
        # Arrange
        mock_get.return_value.json.return_value = self.EXAMPLE_ACCOUNT_RESPONSE

        # Act
        account = self.client.get_account("66512652")

        # Assert
        assert account.account_id == "66512652"
        mock_get.assert_called_once()

    @patch("requests.get")
    def test_get_accounts_with_filters(self, mock_get):
        # Arrange
        mock_get.return_value.json.return_value = self.EXAMPLE_ACCOUNT_RESPONSE

        # Act
        account = self.client.get_accounts(filters=[Filter("riskScore").ge(20)])

        # Assert
        assert account[0].account_id == "66512652"
        mock_get.assert_called_once()
        mock_get.assert_called_with(
            "https://sandbox.capitalone.co.uk/developer-services-platform-pr/api/data/accounts",
            headers={
                "Authorization": "Bearer dummy-token",
                "Content-Type": "application/json",
                "Version": "1.0",
            },
            params={"riskScore": ["gte:20"]},
        )

    @patch("requests.post")
    def test_create_accounts(self, mock_post):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = self.EXAMPLE_ACCOUNT_RESPONSE
        mock_post.return_value = mock_response
        expected_num_accounts = 1

        # Act
        accounts = self.client.create_accounts(expected_num_accounts)

        # Assert
        assert len(accounts) == expected_num_accounts
        mock_post.assert_called_once()

        mock_post.assert_called_with(
            "https://sandbox.capitalone.co.uk/developer-services-platform-pr/api/data/accounts/create",
            headers={
                "Authorization": "Bearer dummy-token",
                "Content-Type": "application/json",
                "Version": "1.0",
            },
            data=json.dumps({"quantity": 1, "numTransactions": 0, "liveBalance": True}),
        )

    @patch("requests.post")
    def test_create_accounts_with_custom_fields(self, mock_post):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = self.EXAMPLE_ACCOUNT_RESPONSE
        mock_post.return_value = mock_response
        expected_num_accounts = 1

        # Act
        accounts = self.client.create_accounts(
            expected_num_accounts,
            credit_score=450,
            currency_code="GBP",
            product_type="Credit",
            risk_score=22,
            state="open",
            credit_limit="1000",
        )

        # Assert
        assert len(accounts) == expected_num_accounts
        mock_post.assert_called_once()

        mock_post.assert_called_with(
            "https://sandbox.capitalone.co.uk/developer-services-platform-pr/api/data/accounts/create",
            headers={
                "Authorization": "Bearer dummy-token",
                "Content-Type": "application/json",
                "Version": "1.0",
            },
            data=json.dumps(
                {
                    "quantity": 1,
                    "numTransactions": 0,
                    "liveBalance": True,
                    "creditScore": 450,
                    "currencyCode": "GBP",
                    "productType": "Credit",
                    "riskScore": 22,
                    "state": "open",
                    "creditLimit": "1000",
                }
            ),
        )

    @patch("requests.post")
    def test_create_transactions(self, mock_post):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = self.EXAMPLE_TRANSACTION_RESPONSE
        mock_post.return_value = mock_response
        expected_num_transactions = 2

        # Act
        transactions = self.client.create_transactions(
            "66512652", expected_num_transactions
        )

        # Assert
        mock_post.assert_called_once()

        mock_post.assert_called_with(
            "https://sandbox.capitalone.co.uk/developer-services-platform-pr/api/data/transactions/accounts/66512652/create",
            headers={
                "Authorization": "Bearer dummy-token",
                "Content-Type": "application/json",
                "Version": "1.0",
            },
            data=json.dumps({"quantity": expected_num_transactions}),
        )

    @patch("requests.post")
    def test_create_transactions_with_custom_fields(self, mock_post):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = self.EXAMPLE_TRANSACTION_RESPONSE
        mock_post.return_value = mock_response
        expected_num_transactions = 2

        # Act
        transactions = self.client.create_transactions(
            "66512652",
            expected_num_transactions,
            amount="100.00",
            credit_debit_indicator="Debit",
            currency="GBP",
            status="Successful",
        )

        # Assert
        mock_post.assert_called_once()
        mock_post.assert_called_with(
            "https://sandbox.capitalone.co.uk/developer-services-platform-pr/api/data/transactions/accounts/66512652/create",
            headers={
                "Authorization": "Bearer dummy-token",
                "Content-Type": "application/json",
                "Version": "1.0",
            },
            data=json.dumps(
                {
                    "quantity": expected_num_transactions,
                    "amount": "100.00",
                    "currency": "GBP",
                    "credit_debit_indicator": "Debit",
                    "status": "Successful",
                }
            ),)
