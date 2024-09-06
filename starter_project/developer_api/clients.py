import json
import os
import re
from collections import defaultdict

import requests

from starter_project.developer_api.filters import FilterRelation
from starter_project.developer_api.models import (
    ProductType,
    AccountState,
    Account,
    TransactionStatus,
    Transaction,
)


class DeveloperApiClient:
    MONETARY_PATTERN = r"^-?\d+(\.\d{1,2})?$"
    SERVICE_URL = (
        "https://sandbox.capitalone.co.uk/developer-services-platform-pr/api/data"
    )
    CONTENT_TYPE = "application/json"
    VERSION = "1.0"

    ACCOUNTS_JSON_KEY = "Accounts"
    TRANSACTIONS_JSON_KEY = "Transactions"

    def __init__(self, bearer_auth_token=None):
        if bearer_auth_token is None:
            bearer_auth_token = os.environ["DEVAPI_TOKEN"]
        self._headers = {
            "Authorization": f"Bearer {bearer_auth_token}",
            "Content-Type": self.CONTENT_TYPE,
            "Version": self.VERSION,
        }

    def _get(self, base_url: str, query_params: dict = {}):
        url = f"{self.SERVICE_URL}/{base_url}"
        response = requests.get(url, headers=self._headers, params=query_params)
        return response.json()

    def _post(self, base_url: str, payload: dict):
        """

        :param base_url:
        :param payload:
        """
        url = f"{self.SERVICE_URL}/{base_url}"
        response = requests.post(url, headers=self._headers, data=json.dumps(payload))
        if 200 <= response.status_code < 300:
            return response.json()
        raise ValueError("TODO: Needs better networking response")

    @staticmethod
    def _construct_query_params_from_filters(filters: list[FilterRelation]):
        # Filter is present so run filter reduction algorithm
        query_params = defaultdict(list)
        for filter_ in filters:
            query_params[filter_.key].append(
                f"{filter_.relation.value}:{filter_.value}"
            )

        return dict(query_params)

    def create_accounts(
        self,
        quantity: int,
        num_transactions: int = 0,
        live_balance: bool = True,
        balance: str = None,
        credit_score: int = None,
        currency_code: str = None,
        product_type: ProductType = None,
        risk_score: int = None,
        state: AccountState = None,
        credit_limit: str = None,
    ):
        """Creates an account with customised account information if specified.
        :param credit_limit:
        :param state:
        :param risk_score:
        :param product_type:
        :param currency_code:
        :param credit_score:
        :param balance:
        :param live_balance:
        :param quantity:
        :param num_transactions:
        """
        base_url = "accounts/create"
        payload = {
            "quantity": quantity,
            "numTransactions": num_transactions,
            "liveBalance": live_balance,
        }
        if balance is not None:
            payload["balance"] = balance
        if credit_score is not None:
            payload["creditScore"] = credit_score
        if currency_code is not None:
            payload["currencyCode"] = currency_code
        if product_type is not None:
            payload["productType"] = product_type
        if risk_score is not None:
            payload["riskScore"] = risk_score
        if state is not None:
            payload["state"] = state
        if credit_limit is not None:
            payload["creditLimit"] = credit_limit

        accounts_data = self._post(base_url, payload)
        accounts = accounts_data.get(self.ACCOUNTS_JSON_KEY, [])
        return [Account.deserialize(account) for account in accounts]

    def get_accounts(self, filters: list[FilterRelation] = []):
        """Gets all accounts created with your authorization token.

        :param filters: A list of optional filter to use when requesting all accounts
        """
        base_url = "accounts"

        query_params = self._construct_query_params_from_filters(filters)
        accounts_response = self._get(base_url, query_params=query_params)
        accounts = accounts_response.get(self.ACCOUNTS_JSON_KEY, [])
        return [Account.deserialize(account) for account in accounts]

    def get_account(self, account_id: str):
        """Gets a specific accounts data using an account's ID.

        :param account_id: The Account ID of the account you're looking for.
        """
        base_url = f"accounts/{account_id}"
        account = self._get(base_url)[self.ACCOUNTS_JSON_KEY][0]
        return Account.deserialize(account)

    def create_transactions(
        self,
        account_id: str,
        quantity: int,
        amount: float = None,
        currency: str = None,
        credit_debit_indicator: ProductType = None,
        emoji: str = None,
        status: TransactionStatus = None,
    ):
        """Creates a group of transactions associated with the account you provide.

        :param status:
        :param emoji:
        :param credit_debit_indicator:
        :param amount:
        :param currency:
        :param account_id: The Account ID of the account you're looking to populate with transactions
        :param quantity: The number of transactions you wish to create. You can create up to 25 at one time
        :return: A list of transactions created
        """

        base_url = f"transactions/accounts/{account_id}/create"
        payload = {"quantity": quantity}

        if amount is not None:
            if not re.match(self.MONETARY_PATTERN, f"{amount}"):
                raise ValueError("amount must be a valid monetary value")
            payload["amount"] = amount
        if currency is not None:
            payload["currency"] = currency
        if credit_debit_indicator is not None:
            payload["credit_debit_indicator"] = credit_debit_indicator
        if emoji is not None:
            payload["emoji"] = emoji
        if status is not None:
            payload["status"] = status

        transactions_data = self._post(base_url, payload)
        transactions = transactions_data.get(self.TRANSACTIONS_JSON_KEY, [])

        return [Transaction.deserialize(transaction) for transaction in transactions]

    def get_transactions(
        self, account_id: str, transaction_filters: list[FilterRelation] = []
    ):
        """Creates a group of transactions associated with the account you provide.

        :param account_id: The Account ID of the account you're looking to populate with transactions
        :param quantity: The number of transactions you wish to create. You can create up to 25 at one time
        :param transaction_filters: A list of optional filters to use when requesting all transactions
        :return: A list of transactions created
        """
        base_url = f"transactions/accounts/{account_id}/transactions"
        query_params = self._construct_query_params_from_filters(transaction_filters)
        transactions_response = self._get(base_url, query_params=query_params)
        accounts = transactions_response._get(self.TRANSACTIONS_JSON_KEY, [])
        return [Transaction.deserialize(account) for account in accounts]

    def get_transaction(self, account_id: str, transaction_id: str):
        """Gets a specific transaction associated with a specific account you provide.

        :param account_id: The Account ID of the account you're looking for.
        :param transaction_id: The transaction ID of the transaction you're looking for.
        :return: The transaction associated with the account and transaction ID you provided.
        """
        base_url = f"transactions/accounts/{account_id}/transactions/{transaction_id}"
        return self._get(base_url)
