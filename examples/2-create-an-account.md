# Creating accounts

Full documentation on creating an account can be found [here](https://hackathon.capitalone.co.uk/docs/customerAccounts#create-a-random-account).

## Creating a random account
```python
from starter_project.developer_api.clients import DeveloperApiClient

client = DeveloperApiClient()

account = client.create_accounts(1)
```

## Creating multiple random accounts
```python
from starter_project.developer_api.clients import DeveloperApiClient

client = DeveloperApiClient()

accounts = client.create_accounts(5) # Create 5 accounts
```

## Creating account with specific details

```python
from starter_project.developer_api.clients import DeveloperApiClient

client = DeveloperApiClient()

account = client.create_accounts(1, account_type='Savings', balance=1000)
```

For a full list of fields you can customise please refer to the [documentation](https://hackathon.capitalone.co.uk/docs/customerAccounts#create-a-custom-account).

