import requests
import json
from typing import Dict, List, Optional, Union
import logging

class GoogleBooksAPI:
    """
    Google Books API integration for searching books by name and extracting ISBN information.
    """
    
    def __init__(self):
        self.base_url = "https://www.googleapis.com/books/v1/volumes"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def search_book_by_name(self, book_name: str, max_results: int = 5) -> List[Dict]:
        """
        Search for books by name using Google Books API.
        
        Args:
            book_name (str): The name/title of the book to search for
            max_results (int): Maximum number of results to return
            
        Returns:
            List[Dict]: List of book information dictionaries
        """
        try:
            params = {
                'q': book_name,
                'maxResults': max_results,
                'printType': 'books'  # Only physical books
            }
            
            logging.info(f"Searching Google Books for: {book_name}")
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            books = []
            
            if 'items' in data:
                for item in data['items']:
                    book_info = self._extract_book_info(item)
                    if book_info:
                        books.append(book_info)
            
            logging.info(f"Found {len(books)} books from Google Books")
            return books
            
        except requests.RequestException as e:
            logging.error(f"Google Books API request failed: {str(e)}")
            return []
        except Exception as e:
            logging.error(f"Error searching Google Books: {str(e)}")
            return []
    
    def _extract_book_info(self, item: Dict) -> Optional[Dict]:
        """
        Extract relevant book information from Google Books API response item.
        
        Args:
            item (Dict): Single book item from Google Books API response
            
        Returns:
            Optional[Dict]: Extracted book information or None if invalid
        """
        try:
            volume_info = item.get('volumeInfo', {})
            
            # Extract basic information
            title = volume_info.get('title', '')
            authors = volume_info.get('authors', [])
            author = ', '.join(authors) if authors else 'Unknown Author'
            
            # Extract ISBN information
            isbn_10 = None
            isbn_13 = None
            
            industry_identifiers = volume_info.get('industryIdentifiers', [])
            for identifier in industry_identifiers:
                id_type = identifier.get('type', '')
                id_value = identifier.get('identifier', '')
                
                if id_type == 'ISBN_10':
                    isbn_10 = id_value
                elif id_type == 'ISBN_13':
                    isbn_13 = id_value
            
            # Prefer ISBN-13, fallback to ISBN-10
            isbn = isbn_13 or isbn_10
            
            if not isbn or not title:
                return None
            
            # Extract additional information
            published_date = volume_info.get('publishedDate', '')
            publisher = volume_info.get('publisher', '')
            description = volume_info.get('description', '')
            page_count = volume_info.get('pageCount', 0)
            
            # Get book cover image
            image_links = volume_info.get('imageLinks', {})
            thumbnail = image_links.get('thumbnail', '')
            
            # Get Google Books link
            google_books_link = item.get('selfLink', '')
            
            book_info = {
                'title': title,
                'author': author,
                'isbn_10': isbn_10,
                'isbn_13': isbn_13,
                'isbn': isbn,  # Primary ISBN for searching
                'published_date': published_date,
                'publisher': publisher,
                'description': description,
                'page_count': page_count,
                'thumbnail': thumbnail,
                'google_books_link': google_books_link,
                'source': 'Google Books'
            }
            
            return book_info
            
        except Exception as e:
            logging.error(f"Error extracting book info: {str(e)}")
            return None
    
    def get_book_by_isbn(self, isbn: str) -> Optional[Dict]:
        """
        Get book information by ISBN using Google Books API.
        
        Args:
            isbn (str): ISBN number (10 or 13 digits)
            
        Returns:
            Optional[Dict]: Book information or None if not found
        """
        try:
            # Clean ISBN
            isbn_clean = isbn.replace('-', '').replace(' ', '')
            
            params = {
                'q': f'isbn:{isbn_clean}',
                'maxResults': 1
            }
            
            logging.info(f"Searching Google Books by ISBN: {isbn_clean}")
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'items' and len(data['items']) > 0:
                book_info = self._extract_book_info(data['items'][0])
                return book_info
            
            return None
            
        except Exception as e:
            logging.error(f"Error searching by ISBN {isbn}: {str(e)}")
            return None

def search_books_by_name(book_name: str) -> List[Dict]:
    """
    Convenience function to search books by name.
    
    Args:
        book_name (str): Name of the book to search for
        
    Returns:
        List[Dict]: List of book information dictionaries
    """
    api = GoogleBooksAPI()
    return api.search_book_by_name(book_name)

def get_book_by_isbn(isbn: str) -> Optional[Dict]:
    """
    Convenience function to get book by ISBN.
    
    Args:
        isbn (str): ISBN number
        
    Returns:
        Optional[Dict]: Book information or None
    """
    api = GoogleBooksAPI()
    return api.get_book_by_isbn(isbn)

if __name__ == "__main__":
    # Test the Google Books integration
    logging.basicConfig(level=logging.INFO)
    
    # Test search by name
    print("Testing Google Books search by name...")
    books = search_books_by_name("Clean Code")
    
    if books:
        print(f"\nFound {len(books)} books:")
        for i, book in enumerate(books[:3], 1):
            print(f"\n{i}. {book['title']}")
            print(f"   Author: {book['author']}")
            print(f"   ISBN: {book['isbn']}")
            print(f"   Published: {book['published_date']}")
    else:
        print("No books found.")
    
    # Test search by ISBN
    print("\n" + "="*50)
    print("Testing Google Books search by ISBN...")
    if books:
        test_isbn = books[0]['isbn']
        book = get_book_by_isbn(test_isbn)
        if book:
            print(f"Found book by ISBN {test_isbn}: {book['title']}")
        else:
            print(f"No book found for ISBN {test_isbn}")
