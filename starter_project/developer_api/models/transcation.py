from dataclasses import dataclass
from enum import Enum

from bidict import bidict

from starter_project.developer_api.models.merchant import Merchant
from starter_project.developer_api.models.product_type import ProductType

TRANSACTION_SERVICE_MAPPING = bidict(
    {
        "transaction_uuid": "transactionUUID",
        "account_uuid": "accountUUID",
        "merchant_uuid": "merchantUUID",
        "merchant": "merchant",
        "amount": "amount",
        "credit_debit_indicator": "creditDebitIndicator",
        "currency": "currency",
        "timestamp": "timestamp",
        "emoji": "emoji",
        "latitude": "latitude",
        "longitude": "longitude",
        "status": "status",
        "message": "message",
        "point_of_sale": "pointOfSale",
    }
)


class TransactionStatus(Enum):
    SUCCESSFUL = "Successful"
    PENDING = "Pending"
    FLAGGED = "Flagged"
    DECLINED = "Declined"


@dataclass
class Transaction:
    transaction_uuid: str
    account_uuid: str
    merchant_uuid: str
    merchant: Merchant
    credit_debit_indicator: ProductType
    currency: str
    timestamp: str
    emoji: str
    latitude: float
    longitude: float
    status: TransactionStatus
    message: str
    point_of_sale: str
    amount: float

    def serialize(self):
        object_dict = self.__dict__.copy()
        # Updates private property names
        serialized_object = {
            TRANSACTION_SERVICE_MAPPING[key]: object_dict[key]
            for key in object_dict.keys()
        }
        serialized_object["merchant"] = serialized_object["merchant"].serialize()
        return serialized_object

    @classmethod
    def deserialize(cls, object_dict):
        # Deserialize to object from dictionary and convert types
        print(object_dict)
        mapped_object_dict = {
            TRANSACTION_SERVICE_MAPPING.inverse[key]: object_dict[key]
            for key in object_dict.keys()
        }
        mapped_object_dict["latitude"] = float(mapped_object_dict["latitude"])
        mapped_object_dict["longitude"] = float(mapped_object_dict["longitude"])
        print(mapped_object_dict)
        return cls(**mapped_object_dict)
