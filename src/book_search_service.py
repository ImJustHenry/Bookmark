from typing import Dict, List, Optional, Union
import logging
from google_books_api import GoogleBooksAPI, search_books_by_name
from fetch_html import fetch_html
from book import Book, Condition, Medium

class BookSearchService:
    """
    Unified book search service that integrates Google Books API with price scrapers.
    """
    
    def __init__(self):
        self.google_books = GoogleBooksAPI()
        
    def search_by_book_name(self, book_name: str, max_results: int = 3) -> Dict:
        """
        Search for books by name and get prices from multiple retailers.
        
        Args:
            book_name (str): Name of the book to search for
            max_results (int): Maximum number of book results to return
            
        Returns:
            Dict: Search results with book information and prices
        """
        try:
            logging.info(f"Starting comprehensive search for: {book_name}")
            
            # Step 1: Search Google Books to get book information and ISBNs
            google_books_results = self.google_books.search_book_by_name(book_name, max_results)
            
            if not google_books_results:
                return {
                    'success': False,
                    'error': f'No books found for "{book_name}"',
                    'books': []
                }
            
            # Step 2: For each book found, search for prices on different retailers
            books_with_prices = []
            
            for book_info in google_books_results:
                isbn = book_info.get('isbn')
                if not isbn:
                    continue
                
                # Search prices on different retailers
                prices = self._search_prices_by_isbn(isbn)
                
                # Combine book info with prices
                book_with_prices = {
                    'book_info': book_info,
                    'prices': prices,
                    'best_price': self._find_best_price(prices)
                }
                
                books_with_prices.append(book_with_prices)
            
            return {
                'success': True,
                'search_term': book_name,
                'books_found': len(books_with_prices),
                'books': books_with_prices
            }
            
        except Exception as e:
            logging.error(f"Error in search_by_book_name: {str(e)}")
            return {
                'success': False,
                'error': f'Search failed: {str(e)}',
                'books': []
            }
    
    def search_by_isbn(self, isbn: str) -> Dict:
        """
        Search for book prices by ISBN across multiple retailers.
        
        Args:
            isbn (str): ISBN number
            
        Returns:
            Dict: Search results with book information and prices
        """
        try:
            logging.info(f"Searching by ISBN: {isbn}")
            
            # Step 1: Get book information from Google Books
            book_info = self.google_books.get_book_by_isbn(isbn)
            
            if not book_info:
                return {
                    'success': False,
                    'error': f'No book found for ISBN {isbn}',
                    'book_info': None,
                    'prices': {}
                }
            
            # Step 2: Search for prices on different retailers
            prices = self._search_prices_by_isbn(isbn)
            
            return {
                'success': True,
                'book_info': book_info,
                'prices': prices,
                'best_price': self._find_best_price(prices)
            }
            
        except Exception as e:
            logging.error(f"Error in search_by_isbn: {str(e)}")
            return {
                'success': False,
                'error': f'ISBN search failed: {str(e)}',
                'book_info': None,
                'prices': {}
            }
    
   
    
    def _find_best_price(self, prices: Dict[str, Union[Dict, str]]) -> Optional[Dict]:
        """
        Find the best (lowest) price from all retailers.
        
        Args:
            prices (Dict): Prices from different retailers
            
        Returns:
            Optional[Dict]: Best price information or None
        """
        best_price = None
        best_value = float('inf')
        
        for retailer, price_info in prices.items():
            if isinstance(price_info, dict) and 'price' in price_info:
                try:
                    # Extract numeric value from price string
                    price_str = price_info['price'].replace('$', '').replace(',', '')
                    price_value = float(price_str)
                    
                    if price_value < best_value:
                        best_value = price_value
                        best_price = {
                            'retailer': retailer,
                            'price': price_info['price'],
                            'url': price_info.get('url', ''),
                            'condition': price_info.get('condition', ''),
                            'availability': price_info.get('availability', '')
                        }
                except (ValueError, TypeError):
                    continue
        
        return best_price

# Convenience functions
def search_book_by_name(book_name: str) -> Dict:
    """Search for books by name across multiple retailers."""
    service = BookSearchService()
    return service.search_by_book_name(book_name)

def search_book_by_isbn(isbn: str) -> Dict:
    """Search for book prices by ISBN across multiple retailers."""
    service = BookSearchService()
    return service.search_by_isbn(isbn)

if __name__ == "__main__":
    # Test the unified search service
    logging.basicConfig(level=logging.INFO)
    
    print("Testing unified book search service...")
    
    # Test search by name
    print("\n1. Testing search by book name:")
    result = search_book_by_name("Clean Code")
    
    if result['success']:
        print(f"Found {result['books_found']} books for '{result['search_term']}'")
        for i, book in enumerate(result['books'][:2], 1):
            print(f"\nBook {i}: {book['book_info']['title']}")
            print(f"Author: {book['book_info']['author']}")
            print(f"ISBN: {book['book_info']['isbn']}")
            
            if book['best_price']:
                print(f"Best Price: {book['best_price']['price']} at {book['best_price']['retailer']}")
            
            print("All prices:")
            for retailer, price_info in book['prices'].items():
                if isinstance(price_info, dict):
                    print(f"  {retailer}: {price_info['price']}")
                else:
                    print(f"  {retailer}: {price_info}")
    else:
        print(f"Search failed: {result['error']}")
    
    # Test search by ISBN
    print("\n" + "="*60)
    print("2. Testing search by ISBN:")
    isbn_result = search_book_by_isbn("9780134685991")
    
    if isbn_result['success']:
        book_info = isbn_result['book_info']
        print(f"Book: {book_info['title']}")
        print(f"Author: {book_info['author']}")
        
        if isbn_result['best_price']:
            best = isbn_result['best_price']
            print(f"Best Price: {best['price']} at {best['retailer']}")
        
        print("All prices:")
        for retailer, price_info in isbn_result['prices'].items():
            if isinstance(price_info, dict):
                print(f"  {retailer}: {price_info['price']}")
            else:
                print(f"  {retailer}: {price_info}")
    else:
        print(f"ISBN search failed: {isbn_result['error']}")
