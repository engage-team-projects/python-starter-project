# Creating accounts

## Get an account by id
```python
from starter_project.developer_api.clients import DeveloperApiClient

client = DeveloperApiClient()

transaction = client.get_transaction("<INSERT_ACCOUNT_ID>", "INSERT_TRANSACTION_ID")
```

## Get all accounts

```python
from starter_project.developer_api.clients import DeveloperApiClient

client = DeveloperApiClient()

transactions = client.get_transactions()
```

This will get all the accounts that you have currently created against your token.

## Get all accounts with filters
```python
from starter_project.developer_api.clients import DeveloperApiClient
from starter_project.developer_api.filters import Filter

client = DeveloperApiClient()

currency_code_filter = Filter('currency').eq('GBP')
lat_gt_filter = Filter('latitude').gt(1.5)
lat_lte_filter = Filter('latitude').le(2.5)
long_gte_filter = Filter('longitude').ge(1)
long_lt_filter = Filter('longitude').lt(20.6)

all_filters = [
    currency_code_filter,
    lat_gt_filter,
    lat_lte_filter,
    long_gte_filter,
    long_lt_filter
]

client.get_transactions(filters=all_filters)
```

This will get all the accounts that you have currently created against your token that match the filters you have provided.
The filters are applied as an AND operation meaning that all filters must be met for an account to be returned.
