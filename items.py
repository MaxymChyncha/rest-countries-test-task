from dataclasses import dataclass


@dataclass
class Item:
    url: str
    name: str
    image: str
    price: float
    seller: str
