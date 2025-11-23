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
    def __init__(self, link: str, title: str, isbn: int, price: float, condition: Condition, medium: Medium, description: str = "No description available.", image: str = ""):
        self.link=link
        self.title=title
        self.isbn=isbn
        self.price=price
        self.condition=condition
        self.medium=medium
    
    def __lt__(self,other):
        return self.price < other.price

    def __gt__(self,other):
        return self.price > other.price

class BookError(Exception):
    def __init__(self, message="Book ERROR!"):
        self.message = message
        super().__init__(self.message)
