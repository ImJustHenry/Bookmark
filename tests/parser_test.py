import unittest
import abebook_parser
import book
def test_parser_follows_standard(parser_object):
    try:
        book_result: book.Book = parser_object.parse(9798991511100, book.Condition.NEW)
    except TypeError:
    if type(book_result) != book.Book:
        return False
    if book_result.pric