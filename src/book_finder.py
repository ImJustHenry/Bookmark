import abebook_parser
import chegg_scraper
import book

def find_cheapest_book(isbn):

    book_objects = []

    abebooks_book = abebook_parser.get_abebooks_prices(isbn)
    if abebooks_book!=None:
        book_objects.append(abebooks_book)
    
    chegg_book = chegg_scraper.get_chegg_prices(isbn)
    if chegg_book!=None:
        book_objects.append(chegg_book)

    if book_objects == []:
        return None
    
    return min(book_objects)

