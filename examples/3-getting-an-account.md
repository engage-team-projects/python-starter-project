# Creating accounts

## Get an account by id
```python
from starter_project.developer_api.clients import DeveloperApiClient

client = DeveloperApiClient()

account = client.get_account("<INSERT_SOME_ID>")
```

## Get all accounts
```python
from starter_project.developer_api.clients import DeveloperApiClient

client = DeveloperApiClient()

accounts = client.get_accounts()
```

This will get all the accounts that you have currently created against your token.

## Get all accounts with filters
```python
from starter_project.developer_api.clients import DeveloperApiClient
from starter_project.developer_api.filters import Filter

client = DeveloperApiClient()

currency_code_filter = Filter('currencyCode').eq('GBP')
credit_score_gt_filter = Filter('creditScore').gt(500)
credit_score_lte_filter = Filter('creditScore').le(700)
risk_score_gte_filter = Filter('riskScore').ge(1)
risk_score_lt_filter = Filter('riskScore').lt(20)

all_filters = [
    currency_code_filter, 
    credit_score_gt_filter, 
    credit_score_lte_filter, 
    risk_score_gte_filter, 
    risk_score_lt_filter
]

client.get_accounts(filters=all_filters)
```

This will get all the accounts that you have currently created against your token that match the filters you have provided.
The filters are applied as an AND operation meaning that all filters must be met for an account to be returned.
