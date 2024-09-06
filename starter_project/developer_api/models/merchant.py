from dataclasses import dataclass


@dataclass
class Merchant:
    name: str
    category: str
    description: str
    pointOfSale: list[str]
