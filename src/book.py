from enum import Enum
from typing import *

class Condition(Enum):
    UNKNOWN = 0
    USED = 1
    NEW = 2

class Medium(Enum):
    UNKNOWN = 0
    PHYSICAL = 1
    EBOOK = 2
    INTERACTIVE = 3

class Book:
    def __init__(self, link: str, title: str, isbn: int, price: float, condition: Condition, medium Medium):
        self.link=link
        self.title=title
        self.isbn=isbn
        self.price=price
        self.condition=condition
        self.medium=medium
