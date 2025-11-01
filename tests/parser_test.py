import sys
PARSER_PATH = "./src/parsers/"
parser_modules = []
sys.path.insert(0,"./src/")
sys.path.insert(0,PARSER_PATH)
import unittest
import importlib
import book
import os


def import_parsers():
    
    filenames = os.listdir(PARSER_PATH)
    for f in filenames:
        if f.endswith(".py"):
            name = f[:-3]
            module = importlib.import_module(name)
            parser_modules.append(module)

class test_parsers(unittest.TestCase):
    def test_parsers_follows_standard(self):
        import_parsers()
        for p in parser_modules:
            with self.subTest(p=p):
                book_result = p.parse(9798991511100)
                self.assertTrue(type(book_result) == book.Book)

                
   

if __name__ == '__main__':
    unittest.main()