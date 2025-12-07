import sys
import os

# Get the directory where this file is located
_current_dir = os.path.dirname(os.path.abspath(__file__))
PARSER_PATH = os.path.join(_current_dir, "parsers")
parser_modules = []
sys.path.insert(0, PARSER_PATH)
import importlib


def import_parsers():
    filenames = os.listdir(PARSER_PATH)
    for f in filenames:
        if f.endswith(".py"):
            name = f[:-3]
            module = importlib.import_module(name)
            parser_modules.append(module)

def _run_parser(parser_class,isbn, book_list):
    out = None
    try:
        out = parser_class.parse(isbn)

        if out.price is None or out.price == 0:
            return
    except:
        return
    else:
        book_list.append(out)

def find_cheapest_book(isbn):
    import_parsers()
    book_objects = []
    for p in parser_modules:
        _run_parser(p,isbn,book_objects)
    print(book_objects)
    if book_objects == []:
        return None
    
    return min(book_objects)

