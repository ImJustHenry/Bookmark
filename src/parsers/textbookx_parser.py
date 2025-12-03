from fetch_html import fetch_html
from bs4 import BeautifulSoup
import re
import book

def search_textbookx(isbn):
    """
    Construct the TextbookX search URL for a given ISBN.
    
    Args:
        isbn: ISBN number (int or str)
        
    Returns:
        str: URL to search TextbookX
    """
    isbn_str = str(isbn).strip()
    # TextbookX search URL format - try multiple possible formats
    # Format 1: Standard search with query parameter (most common)
    # Format 2: Alternative with /search/ path
    # Format 3: Direct ISBN search
    # We'll try the most common format first
    return f"https://www.textbookx.com/search?q={isbn_str}"

def parse(isbn):
    """
    Parse TextbookX to find book information by ISBN.
    
    Args:
        isbn: ISBN number (int or str)
        
    Returns:
        book.Book: Book object with information from TextbookX
        
    Raises:
        book.BookError: If book is not found or parsing fails
    """
    try:
        search_url = search_textbookx(isbn)
        
        # Try multiple URL formats if the first one fails
        url_formats = [
            f"https://www.textbookx.com/search?q={isbn}",
            f"https://www.textbookx.com/search/?q={isbn}",
            f"https://www.textbookx.com/textbooks?q={isbn}",
            f"https://www.textbookx.com/textbooks/?q={isbn}",
        ]
        
        html_string = None
        for url_format in url_formats:
            try:
                html_string = fetch_html(url=url_format)
                search_url = url_format  # Update to successful URL
                break
            except Exception:
                continue
        
        if html_string is None:
            raise book.BookError("Could not access TextbookX search page")
        
        soup = BeautifulSoup(html_string, 'html.parser')
        
        # Strategy 1: Look for product cards or listings
        # TextbookX typically uses product cards or listing items
        product_result = None
        
        # Try multiple selectors for product containers
        product_selectors = [
            ('div', {'class': re.compile(r'product|item|listing', re.I)}),
            ('div', {'class': re.compile(r'book-card|book-item', re.I)}),
            ('li', {'class': re.compile(r'product|item', re.I)}),
            ('article', {'class': re.compile(r'product|book', re.I)}),
        ]
        
        for tag, attrs in product_selectors:
            product_result = soup.find(tag, attrs)
            if product_result:
                break
        
        # Strategy 2: Look for search results container
        if not product_result:
            results_container = soup.find('div', class_=re.compile(r'results|search-results|products', re.I))
            if results_container:
                product_result = results_container.find('div', class_=re.compile(r'product|item|book', re.I))
        
        # Strategy 3: Look for any element with ISBN or book data
        if not product_result:
            # Try to find elements containing the ISBN
            isbn_str = str(isbn).replace('-', '').replace(' ', '')
            elements_with_isbn = soup.find_all(string=re.compile(isbn_str[-10:]))  # Last 10 digits
            if elements_with_isbn:
                # Find parent container
                for elem in elements_with_isbn[:3]:  # Check first few matches
                    parent = elem.find_parent(['div', 'li', 'article'])
                    if parent:
                        product_result = parent
                        break
        
        if not product_result:
            raise book.BookError("No product results found on TextbookX")
        
        # Extract title - try multiple strategies
        title = None
        
        # Strategy 1: Look for title in common locations
        title_selectors = [
            ('h2', {}),
            ('h3', {}),
            ('h1', {}),
            ('a', {'class': re.compile(r'title|name|book-title', re.I)}),
            ('span', {'class': re.compile(r'title|name', re.I)}),
            ('div', {'class': re.compile(r'title|name|book-title', re.I)}),
        ]
        
        for tag, attrs in title_selectors:
            title_elem = product_result.find(tag, attrs) if attrs else product_result.find(tag)
            if title_elem:
                title = title_elem.get_text(strip=True)
                if title and len(title) > 3:
                    break
        
        # Strategy 2: Look for title in link text
        if not title or len(title) < 3:
            title_link = product_result.find('a', href=True)
            if title_link:
                title = title_link.get_text(strip=True)
                if title and len(title) > 3:
                    pass  # Use this title
        
        # Strategy 3: Look for data attributes
        if not title or len(title) < 3:
            title_attr = product_result.get('data-title') or product_result.get('data-name')
            if title_attr:
                title = title_attr.strip()
        
        # Extract price - try multiple strategies
        price = None
        
        # Strategy 1: Look for price in common price classes
        price_selectors = [
            ('span', {'class': re.compile(r'price|cost|amount', re.I)}),
            ('div', {'class': re.compile(r'price|cost|amount', re.I)}),
            ('p', {'class': re.compile(r'price|cost|amount', re.I)}),
            ('strong', {'class': re.compile(r'price', re.I)}),
        ]
        
        for tag, attrs in price_selectors:
            price_elem = product_result.find(tag, attrs)
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                # Extract numeric price
                price_match = re.search(r'[\d,]+\.?\d*', price_text.replace('$', '').replace(',', ''))
                if price_match:
                    try:
                        price = float(price_match.group())
                        if 1.0 <= price <= 10000.0:  # Reasonable price range
                            break
                    except ValueError:
                        continue
        
        # Strategy 2: Look for any text containing "$" and numbers
        if price is None:
            price_elements = product_result.find_all(string=re.compile(r'\$\s*[\d,]+\.?\d*'))
            for price_elem in price_elements:
                price_text = price_elem.strip() if isinstance(price_elem, str) else price_elem.get_text(strip=True)
                price_match = re.search(r'[\d,]+\.?\d*', price_text.replace('$', '').replace(',', ''))
                if price_match:
                    try:
                        price = float(price_match.group())
                        if 1.0 <= price <= 10000.0:
                            break
                    except (ValueError, AttributeError):
                        continue
        
        # Strategy 3: Search entire product HTML for price patterns
        if price is None:
            product_html = str(product_result)
            price_patterns = [
                r'\$\s*([\d,]+\.?\d*)',
                r'price[:\s]*\$?\s*([\d,]+\.?\d*)',
                r'([\d,]+\.?\d{2})\s*USD',
            ]
            for pattern in price_patterns:
                matches = re.findall(pattern, product_html, re.IGNORECASE)
                for match in matches:
                    try:
                        price_val = float(match.replace(',', ''))
                        if 1.0 <= price_val <= 10000.0:
                            price = price_val
                            break
                    except ValueError:
                        continue
                if price:
                    break
        
        # Strategy 4: Document-wide search as last resort
        if price is None:
            all_text = soup.get_text()
            dollar_matches = re.findall(r'\$\s*([\d,]+\.?\d{2})', all_text)
            for match in dollar_matches[:5]:  # Check first 5 matches
                try:
                    price_val = float(match.replace(',', ''))
                    if 1.0 <= price_val <= 10000.0:
                        price = price_val
                        break
                except ValueError:
                    continue
        
        # Extract product link
        link = search_url  # Default to search URL
        product_link = product_result.find('a', href=True)
        if product_link:
            href = product_link.get('href', '')
            if href:
                if href.startswith('http'):
                    link = href
                elif href.startswith('/'):
                    link = f"https://www.textbookx.com{href}"
                else:
                    link = f"https://www.textbookx.com/{href}"
        
        # Validate that we found essential information
        if price is None:
            raise book.BookError("Price not found on TextbookX")
        
        if not title or len(title) < 3:
            title = "Book (TextbookX)"
        
        # Convert isbn to int if it's a string
        isbn_int = int(str(isbn).replace('-', '').replace(' ', ''))
        
        # Create and return Book object
        # TextbookX typically sells physical books, but could be either
        output = book.Book(
            link=link,
            title=title,
            isbn=isbn_int,
            price=price,
            condition=book.Condition.UNKNOWN,  # TextbookX may have condition info, but we'll default to UNKNOWN
            medium=book.Medium.PHYSICAL  # TextbookX primarily sells physical books
        )
        
        return output
        
    except book.BookError:
        raise
    except Exception as e:
        raise book.BookError(f"Error parsing TextbookX: {str(e)}")

def get_test_isbn():
    """
    Return a test ISBN that exists on TextbookX.
    
    Returns:
        int: Test ISBN number
    """
    # Using a common textbook ISBN that should be available on TextbookX
    # Clean Code is commonly available on TextbookX
    return 9780134685991  # Clean Code: A Handbook of Agile Software Craftsmanship

if __name__ == "__main__":
    # Test the parser
    test_isbn = get_test_isbn()
    print(f"Testing TextbookX parser with ISBN: {test_isbn}")
    try:
        result = parse(test_isbn)
        print(f"\n{'='*60}")
        print("✅ Book Found on TextbookX")
        print(f"{'='*60}")
        print(f"Title: {result.title}")
        print(f"ISBN: {result.isbn}")
        print(f"Price: ${result.price:.2f}")
        print(f"Link: {result.link}")
        print(f"Medium: {result.medium}")
    except book.BookError as e:
        print(f"\n❌ Error: {e.message}")

