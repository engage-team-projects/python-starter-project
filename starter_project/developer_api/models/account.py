from dataclasses import dataclass
from enum import Enum

from bidict import bidict

from starter_project.developer_api.models.product_type import ProductType

# Used to map the account fields from pythonic style to api expectation bidirectionally
ACCOUNT_SERVICE_MAPPING = bidict(
    {
        "account_id": "accountId",
        "firstname": "firstname",
        "phone_number": "phoneNumber",
        "developer_id": "developerId",
        "uci": "uci",
        "risk_score": "riskScore",
        "credit_score": "creditScore",
        "currency_code": "currencyCode",
        "product_type": "productType",
        "email": "email",
        "lastname": "lastname",
        "home_address": "homeAddress",
        "state": "state",
        "live_balance": "liveBalance",
        "credit_limit": "creditLimit",
        "balance": "balance",
    }
)


class AccountState(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    SUSPENDED = "suspended"
    FLAGGED = "flagged"


@dataclass
class Account:
    account_id: str
    firstname: str
    phone_number: str
    developer_id: str
    uci: str
    risk_score: int
    credit_score: int
    currency_code: str
    product_type: ProductType
    email: str
    lastname: str
    home_address: str
    state: AccountState
    live_balance: bool
    credit_limit: float
    balance: float

    def serialize(self):
        object_dict = self.__dict__.copy()
        return {
            ACCOUNT_SERVICE_MAPPING[key]: object_dict[key] for key in object_dict.keys()
        }

    @classmethod
    def deserialize(cls, object_dict):
        # Deserialize to object from dictionary and convert types
        mapped_object_dict = {
            ACCOUNT_SERVICE_MAPPING.inverse[key]: object_dict[key]
            for key in object_dict.keys()
        }
        mapped_object_dict["risk_score"] = int(mapped_object_dict["risk_score"])
        mapped_object_dict["credit_score"] = int(mapped_object_dict["credit_score"])
        mapped_object_dict["live_balance"] = bool(mapped_object_dict["live_balance"])
        mapped_object_dict["balance"] = float(mapped_object_dict["balance"])
        mapped_object_dict["credit_limit"] = float(mapped_object_dict["credit_limit"])
        return cls(**mapped_object_dict)

    def __repr__(self):
        return (
            f'Account(account_id="{self.account_id}", firstname="{self.firstname}", '
            f'phone_number="{self.phone_number}", developer_id="{self.developer_id}", '
            f'uci="{self.uci}", risk_score={self.risk_score}, '
            f'credit_score={self.credit_score}, currency_code="{self.currency_code}", '
            f'product_type="{self.product_type}", email="{self.email}", '
            f'lastname="{self.lastname}", home_address="{self.home_address}", '
            f'state="{self.state}", credit_limit="{self.credit_limit}", '
            f'balance="{self.balance}", live_balance="{self.live_balance}")'
        )
