import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from book import Book, Condition, Medium

class BookfinderTest(unittest.TestCase):

    def testMinPriceSuccess(self):
        cheap = Book("cheap.com", "Cheap Book", 1234567890, 12.99, Condition.USED, Medium.PHYSICAL)
        middle = Book("medium.com", "Medium Book", 9087654321, 23.99, Condition.NEW, Medium.INTERACTIVE)
        expensive = Book("expensive.com", "Expensive Book", 5730864219, 40.99, Condition.NEW, Medium.PHYSICAL)

        books = [cheap, middle, expensive]
        cheapest = min(books)

        self.assertEqual(cheapest.price, 12.99)
        self.assertEqual(cheapest.title, "Cheap Book")

    def testEmptyList(self):
        books = []
        result = min(books) if books else None
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()