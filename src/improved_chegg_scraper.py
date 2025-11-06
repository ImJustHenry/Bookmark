import requests
from bs4 import BeautifulSoup
import logging
import re
import time
import random
from urllib.parse import urlencode, quote
from UserAgentFaker import GetFakeUserAgent

class ImprovedCheggScraper:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.chegg.com"
        self._setup_session()
        
    def _setup_session(self):
        """Setup session with realistic browser behavior"""
        self.session.headers.update({
            'User-Agent': GetFakeUserAgent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        })
        
    def _update_headers(self):
        """Update headers with new user agent and realistic browser behavior"""
        self.session.headers.update({
            'User-Agent': GetFakeUserAgent(),
            'Referer': 'https://www.google.com/',
        })
        
    def get_book_price(self, isbn, max_retries=3):
        """
        Enhanced book price scraping with multiple strategies
        """
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    self._update_headers()
                    time.sleep(random.uniform(2, 5))  # Random delay
                
                logging.info(f"Attempt {attempt + 1}: Searching for ISBN: {isbn}")
                
                # Strategy 1: Try to get book info from Google Books first
                book_info = self._get_book_info_from_google_books(isbn)
                if not book_info:
                    book_info = {'isbn': isbn, 'title': '', 'author': ''}
                
                # Strategy 2: Try different search approaches
                search_strategies = [
                    self._search_by_isbn,
                    self._search_by_title,
                    self._search_by_author_title,
                    self._search_direct_urls
                ]
                
                for strategy in search_strategies:
                    try:
                        result = strategy(isbn, book_info)
                        if result and result.get('price'):
                            return result
                    except Exception as e:
                        logging.warning(f"Strategy {strategy.__name__} failed: {e}")
                        continue
                
                # Strategy 3: Try alternative book retailers as fallback
                return self._fallback_search(isbn, book_info)
                
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed for ISBN {isbn}: {str(e)}")
                if attempt == max_retries - 1:
                    return self._create_fallback_result(isbn, book_info)
                    
        return None
    
    def _get_book_info_from_google_books(self, isbn):
        """Get book info from Google Books API as fallback"""
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(__file__))
            from google_books_api import get_book_by_isbn
            
            result = get_book_by_isbn(isbn)
            if result:
                return {
                    'title': result.get('title', ''),
                    'author': result.get('author', ''),
                    'isbn': isbn
                }
        except Exception as e:
            logging.warning(f"Google Books fallback failed: {e}")
        return None
    
    def _search_by_isbn(self, isbn, book_info):
        """Search using ISBN directly"""
        search_urls = [
            f"{self.base_url}/search?query={isbn}",
            f"{self.base_url}/search?q={isbn}",
            f"{self.base_url}/search?query=ISBN {isbn}",
            f"{self.base_url}/search?query=isbn:{isbn}",
        ]
        
        for url in search_urls:
            response = self._make_request(url)
            if response and self._has_search_results(response, isbn):
                return self._extract_from_search_page(response, isbn, book_info)
        return None
    
    def _search_by_title(self, isbn, book_info):
        """Search using book title"""
        if not book_info.get('title'):
            return None
            
        title = book_info['title']
        search_urls = [
            f"{self.base_url}/search?query={quote(title)}",
            f"{self.base_url}/search?query={quote(title)} textbook",
            f"{self.base_url}/search?query={quote(title)} book",
        ]
        
        for url in search_urls:
            response = self._make_request(url)
            if response and self._has_search_results(response, isbn):
                return self._extract_from_search_page(response, isbn, book_info)
        return None
    
    def _search_by_author_title(self, isbn, book_info):
        """Search using author and title"""
        if not book_info.get('title') or not book_info.get('author'):
            return None
            
        author = book_info['author'].split(',')[0].strip()  # Get first author
        title = book_info['title']
        
        search_queries = [
            f"{author} {title}",
            f"{title} {author}",
            f"{author} {title} textbook",
        ]
        
        for query in search_queries:
            url = f"{self.base_url}/search?query={quote(query)}"
            response = self._make_request(url)
            if response and self._has_search_results(response, isbn):
                return self._extract_from_search_page(response, isbn, book_info)
        return None
    
    def _search_direct_urls(self, isbn, book_info):
        """Try direct URL patterns"""
        direct_urls = [
            f"{self.base_url}/textbooks/isbn-{isbn}",
            f"{self.base_url}/textbooks/{isbn}",
            f"{self.base_url}/books/{isbn}",
            f"{self.base_url}/textbook/{isbn}",
        ]
        
        for url in direct_urls:
            response = self._make_request(url)
            if response and response.status_code == 200:
                return self._extract_from_product_page(response, isbn, book_info)
        return None
    
    def _make_request(self, url):
        """Make HTTP request with error handling"""
        try:
            response = self.session.get(url, allow_redirects=True, timeout=30)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.error(f"Request error for URL {url}: {str(e)}")
            return None
    
    def _has_search_results(self, response, isbn):
        """Check if response contains search results"""
        if not response:
            return False
            
        content = response.text.lower()
        
        # Check for indicators of search results
        search_indicators = [
            'search results',
            'textbook',
            'book',
            'price',
            'rent',
            'buy',
            'isbn'
        ]
        
        has_indicators = any(indicator in content for indicator in search_indicators)
        has_isbn = isbn in response.text
        
        return has_indicators or has_isbn
    
    def _extract_from_search_page(self, response, isbn, book_info):
        """Extract book info from search results page"""
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for product cards or result items
            result_selectors = [
                '.product-item',
                '.search-result-item',
                '.book-item',
                '.textbook-item',
                '[data-testid*="product"]',
                '[data-testid*="book"]',
                '.result-item'
            ]
            
            results = []
            for selector in result_selectors:
                results.extend(soup.select(selector))
            
            if not results:
                # Try to find any div that might contain book info
                results = soup.find_all('div', string=lambda text: text and isbn in text)
            
            for result in results:
                book_data = self._extract_book_from_element(result, isbn, book_info)
                if book_data and book_data.get('price'):
                    return book_data
            
            # If no specific results found, try to extract from page content
            return self._extract_from_page_content(soup, isbn, book_info)
            
        except Exception as e:
            logging.error(f"Error extracting from search page: {e}")
            return None
    
    def _extract_from_product_page(self, response, isbn, book_info):
        """Extract book info from product page"""
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            return self._extract_from_page_content(soup, isbn, book_info)
        except Exception as e:
            logging.error(f"Error extracting from product page: {e}")
            return None
    
    def _extract_book_from_element(self, element, isbn, book_info):
        """Extract book info from a specific element"""
        try:
            book_data = {
                'isbn': isbn,
                'title': book_info.get('title', ''),
                'author': book_info.get('author', ''),
                'price': '',
                'availability': '',
                'url': '',
                'source': 'Chegg'
            }
            
            # Extract title
            title_selectors = ['h1', 'h2', 'h3', '.title', '.book-title', '.product-title']
            for selector in title_selectors:
                title_elem = element.select_one(selector)
                if title_elem:
                    book_data['title'] = title_elem.get_text(strip=True)
                    break
            
            # Extract price
            price_selectors = ['.price', '.book-price', '.product-price', '[data-testid*="price"]']
            for selector in price_selectors:
                price_elem = element.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    price_match = re.search(r'\$[\d,]+\.?\d*', price_text)
                    if price_match:
                        book_data['price'] = price_match.group()
                        break
            
            # Extract URL
            link_elem = element.select_one('a')
            if link_elem and link_elem.get('href'):
                href = link_elem.get('href')
                if href.startswith('/'):
                    book_data['url'] = self.base_url + href
                else:
                    book_data['url'] = href
            
            return book_data
            
        except Exception as e:
            logging.error(f"Error extracting from element: {e}")
            return None
    
    def _extract_from_page_content(self, soup, isbn, book_info):
        """Extract book info from general page content"""
        try:
            book_data = {
                'isbn': isbn,
                'title': book_info.get('title', ''),
                'author': book_info.get('author', ''),
                'price': '',
                'availability': '',
                'url': '',
                'source': 'Chegg'
            }
            
            # Look for price patterns in the entire page
            price_patterns = [
                r'\$[\d,]+\.?\d*',
                r'Price:?\s*\$[\d,]+\.?\d*',
                r'Rent:?\s*\$[\d,]+\.?\d*',
                r'Buy:?\s*\$[\d,]+\.?\d*'
            ]
            
            page_text = soup.get_text()
            for pattern in price_patterns:
                matches = re.findall(pattern, page_text)
                if matches:
                    book_data['price'] = matches[0]
                    break
            
            # Look for availability
            availability_patterns = [
                r'(In Stock|Available|Out of Stock|Not Available)',
                r'(Rent|Buy|Purchase)',
            ]
            
            for pattern in availability_patterns:
                match = re.search(pattern, page_text, re.IGNORECASE)
                if match:
                    book_data['availability'] = match.group(1)
                    break
            
            return book_data if book_data.get('price') else None
            
        except Exception as e:
            logging.error(f"Error extracting from page content: {e}")
            return None
    
    def _fallback_search(self, isbn, book_info):
        """Fallback search using alternative methods"""
        # This could integrate with other scrapers or APIs
        return self._create_fallback_result(isbn, book_info)
    
    def _create_fallback_result(self, isbn, book_info):
        """Create a fallback result when scraping fails"""
        return {
            'isbn': isbn,
            'title': book_info.get('title', ''),
            'author': book_info.get('author', ''),
            'price': 'Not Available',
            'availability': 'Unknown',
            'url': f"{self.base_url}/search?query={isbn}",
            'source': 'Chegg (Search Required)',
            'note': 'Manual search may be required'
        }
