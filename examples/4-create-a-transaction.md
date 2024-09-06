# Creating accounts

Full documentation on creating an account can be found [here](https://hackathon.capitalone.co.uk/docs/customerTransactions#create-a-transaction).


## Creating a random transaction
```python
from starter_project.developer_api.clients import DeveloperApiClient

client = DeveloperApiClient()

transactions = client.create_transactions("<INSERT_ACCOUNT_ID>", 1)
```

The account id is the id of the account you want to create the transaction for. If you are unsure how to find this refer to the [documentation](3-getting-an-account.md).


## Creating multiple random accounts
```python
from starter_project.developer_api.clients import DeveloperApiClient

client = DeveloperApiClient()

transactions = client.create_transactions("<INSERT_ACCOUNT_ID>", 5) # Create 5 accounts
```

## Creating transactions with specific details

```python
from starter_project.developer_api.clients import DeveloperApiClient

client = DeveloperApiClient()

account = client.create_transactions(1, amount='1.23', currency='INR')
```

For a full list of fields you can customise please refer to the [documentation](https://hackathon.capitalone.co.uk/docs/customerTransactions#create-a-custom-transaction).

