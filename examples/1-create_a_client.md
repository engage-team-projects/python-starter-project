# Create a client

You can create a client in two different ways. 
1. Create a client without a token, and it will be pulled from the `DEVAPI_TOKEN` environment variable.
2. Create the client and pass your token in the constructor.

Option 1 is preferred as it will keep your token out of your code.If you aren't sure how to set an environment variable, you can find instructions [here](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html).
If you don't have access to a token, you can find instructions [here](https://hackathon.capitalone.co.uk/docs/intro#access).
## Create a client without a token
```python
from starter_project.developer_api.clients import DeveloperApiClient

client = DeveloperApiClient()
```

## Create a client with a token
```python
from starter_project.developer_api.clients import DeveloperApiClient

client = DeveloperApiClient('<MY_TOKEN>') # Pass your token here
```
