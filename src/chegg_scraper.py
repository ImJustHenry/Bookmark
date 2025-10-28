import requests
from bs4 import BeautifulSoup
import logging
import re
from urllib.parse import urlencode
import time
from UserAgentFaker import GetFakeUserAgent
import book

class CheggScraper:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.chegg.com"
        self._update_headers()
        
    def _update_headers(self):
        """Update headers with random user agent (based on existing Scrapebot.py pattern)"""
        self.session.headers.update({
            'User-Agent': GetFakeUserAgent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def get_book_price(self, isbn, max_retries=3):
        """
        Scrape book price information from Chegg using ISBN
        Enhanced with retry logic and multiple strategies (based on existing Scrapebot.py pattern)
        
        Args:
            isbn (str): 10 or 13 digit ISBN
            max_retries (int): Maximum number of retry attempts
            
        Returns:
            dict: Book information including title, author, price, etc.
        """
        for attempt in range(max_retries):
            try:
                # Rotate user agent on each retry
                if attempt > 0:
                    self._update_headers()
                    time.sleep(2)  # Wait between retries
                
                logging.info(f"Attempt {attempt + 1}: Searching for ISBN: {isbn}")
                
                # Strategy 1: Search for the book using ISBN
                search_url = self._build_search_url(isbn)
                response = self._make_request(search_url, isbn)
                
                if response:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    book_info = self._extract_book_info(soup, isbn)
                    
                    if book_info:
                        return book_info
                
                # Strategy 2: Try direct URL construction
                direct_url = f"{self.base_url}/textbooks/isbn-{isbn}"
                logging.info(f"Trying direct URL: {direct_url}")
                
                response = self._make_request(direct_url, isbn)
                if response and response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    book_info = self._extract_book_info(soup, isbn)
                    
                    if book_info:
                        return book_info
                
                # Strategy 3: Try alternative URL patterns
                alt_urls = [
                    f"{self.base_url}/textbooks/{isbn}",
                    f"{self.base_url}/books/{isbn}",
                    f"{self.base_url}/search?isbn={isbn}"
                ]
                
                for alt_url in alt_urls:
                    response = self._make_request(alt_url, isbn)
                    if response and response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        book_info = self._extract_book_info(soup, isbn)
                        
                        if book_info:
                            return book_info
                
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed for ISBN {isbn}: {str(e)}")
                if attempt == max_retries - 1:
                    logging.error(f"All attempts failed for ISBN {isbn}")
                    return None
                    
        return None
    
    def _make_request(self, url, isbn):
        """
        Make HTTP request with proper error handling (based on Scrapebot.py pattern)
        """
        try:
            response = self.session.get(url, allow_redirects=True, timeout=30)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.error(f"Request error for URL {url}: {str(e)}")
            return None
    
    def _build_search_url(self, isbn):
        """Build Chegg search URL for ISBN"""
        search_params = {
            'query': isbn,
            'type': 'textbook'
        }
        return f"{self.base_url}/search?{urlencode(search_params)}"
    
    def _extract_book_info(self, soup, isbn):
        """Extract book information from Chegg page"""
        try:
            book_info = {
                'isbn': isbn,
                'title': '',
                'author': '',
                'price': '',
                'availability': '',
                'url': '',
                'source': 'Chegg'
            }
            
            # Try to find book title - multiple selectors
            title_selectors = [
                'h1[data-testid="product-title"]',
                '.product-title',
                'h1.title',
                '.book-title',
                'h1'
            ]
            
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    book_info['title'] = title_elem.get_text(strip=True)
                    break
            
            # Try to find author information
            author_selectors = [
                '[data-testid="author-name"]',
                '.author-name',
                '.book-author',
                '.product-author'
            ]
            
            for selector in author_selectors:
                author_elem = soup.select_one(selector)
                if author_elem:
                    book_info['author'] = author_elem.get_text(strip=True)
                    break
            
            # Try to find price information
            price_selectors = [
                '[data-testid="price"]',
                '.price',
                '.book-price',
                '.product-price',
                '.rental-price',
                '.buy-price'
            ]
            
            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    # Extract numeric price
                    price_match = re.search(r'\$[\d,]+\.?\d*', price_text)
                    if price_match:
                        book_info['price'] = price_match.group()
                        break
            
            # Try to find availability
            availability_selectors = [
                '[data-testid="availability"]',
                '.availability',
                '.stock-status',
                '.in-stock'
            ]
            
            for selector in availability_selectors:
                avail_elem = soup.select_one(selector)
                if avail_elem:
                    book_info['availability'] = avail_elem.get_text(strip=True)
                    break
            
            # Get the current URL
            book_info['url'] = soup.find('meta', property='og:url')
            if book_info['url']:
                book_info['url'] = book_info['url'].get('content', '')
            
            # Check if we found meaningful information
            if book_info['title'] or book_info['price']:
                return book_info
            
            # If no specific book info found, try to extract from search results
            return self._extract_from_search_results(soup, isbn)
            
        except Exception as e:
            logging.error(f"Error extracting book info: {str(e)}")
            return None
    
    def _extract_from_search_results(self, soup, isbn):
        """Extract book info from search results page"""
        try:
            # Look for search result items
            result_items = soup.select('.search-result-item, .product-item, .book-item')
            
            for item in result_items:
                # Check if this result matches our ISBN
                item_text = item.get_text()
                if isbn in item_text:
                    book_info = {
                        'isbn': isbn,
                        'title': '',
                        'author': '',
                        'price': '',
                        'availability': '',
                        'url': '',
                        'source': 'Chegg'
                    }
                    
                    # Extract title
                    title_elem = item.select_one('.title, .book-title, h3, h4')
                    if title_elem:
                        book_info['title'] = title_elem.get_text(strip=True)
                    
                    # Extract price
                    price_elem = item.select_one('.price, .book-price')
                    if price_elem:
                        price_text = price_elem.get_text(strip=True)
                        price_match = re.search(r'\$[\d,]+\.?\d*', price_text)
                        if price_match:
                            book_info['price'] = price_match.group()
                    
                    # Extract URL
                    link_elem = item.select_one('a')
                    if link_elem and link_elem.get('href'):
                        href = link_elem.get('href')
                        if href.startswith('/'):
                            book_info['url'] = self.base_url + href
                        else:
                            book_info['url'] = href
                    
                    return book_info
            
            return None
            
        except Exception as e:
            logging.error(f"Error extracting from search results: {str(e)}")
            return None


def get_chegg_prices(isbn):
    chegg_scraper = CheggScraper()
    result = chegg_scraper.get_book_price(isbn)
    if result==None:
        return None
    book_result = book.Book(result['url'],result['title'],isbn,float(result['price.buy-price']),book.Condition.NEW,book.Medium.PHYSICAL)
    return book_result