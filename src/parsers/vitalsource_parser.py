from fetch_html import fetch_html
from bs4 import BeautifulSoup
import re
import book

def search_vitalsource(isbn):
    """
    Construct the Vitalsource search URL for a given ISBN.
    
    Args:
        isbn: ISBN number (int or str)
        
    Returns:
        str: URL to search Vitalsource
    """
    isbn_str = str(isbn).strip()
    return f"https://www.vitalsource.com/textbooks?q={isbn_str}"

def parse(isbn):
    """
    Parse Vitalsource to find book information by ISBN.
    
    Args:
        isbn: ISBN number (int or str)
        
    Returns:
        book.Book: Book object with information from Vitalsource
        
    Raises:
        book.BookError: If book is not found or parsing fails
    """
    try:
        search_url = search_vitalsource(isbn)
        html_string = fetch_html(url=search_url)
        soup = BeautifulSoup(html_string, 'html.parser')
        
        # Vitalsource uses React and embeds data in JSON scripts, but also renders HTML
        # Look for product search results - they're in <li> elements with class "product-search-result__wrapper"
        product_result = soup.find('li', class_=re.compile(r'product-search-result__wrapper', re.I))
        
        if not product_result:
            raise book.BookError("No product results found on Vitalsource")
        
        # Extract title from h2 with class "product-search-result__title"
        title_elem = product_result.find('h2', class_=re.compile(r'product-search-result__title', re.I))
        if title_elem:
            title = title_elem.get_text(strip=True)
        else:
            # Fallback: try to find any h2 in the result
            title_elem = product_result.find('h2')
            if title_elem:
                title = title_elem.get_text(strip=True)
            else:
                title = None
        
        # Extract price from span with class containing "font-3" and "u-weight--bold"
        # Price format: "$52.99 USD"
        price_elem = product_result.find('span', class_=re.compile(r'font-3.*u-weight--bold|block.*font-3', re.I))
        if not price_elem:
            # Try alternative: look for text containing "$" and "USD"
            price_elem = product_result.find(string=re.compile(r'\$\d+.*USD'))
        
        price = None
        if price_elem:
            if isinstance(price_elem, str):
                price_text = price_elem.strip()
            else:
                price_text = price_elem.get_text(strip=True)
            
            # Extract numeric price value (remove $, USD, commas)
            price_match = re.search(r'[\d,]+\.?\d*', price_text.replace('$', '').replace('USD', '').replace(',', ''))
            if price_match:
                try:
                    price = float(price_match.group())
                except ValueError:
                    pass
        
        # Extract product link from <a> tag with href containing "/products/"
        link = search_url  # Default to search URL
        product_link = product_result.find('a', href=re.compile(r'/products/', re.I))
        if product_link:
            href = product_link.get('href', '')
            if href:
                if href.startswith('http'):
                    link = href
                else:
                    link = f"https://www.vitalsource.com{href}"
        
        # Validate that we found essential information
        if price is None:
            raise book.BookError("Price not found on Vitalsource")
        
        if not title or len(title) < 3:
            # If no title found, use a generic title
            title = "Book (Vitalsource)"
        
        # Convert isbn to int if it's a string
        isbn_int = int(str(isbn).replace('-', '').replace(' ', ''))
        
        # Create and return Book object
        # Vitalsource is for ebooks, so medium is EBOOK
        output = book.Book(
            link=link,
            title=title,
            isbn=isbn_int,
            price=price,
            condition=book.Condition.UNKNOWN,  # Vitalsource doesn't specify condition for ebooks
            medium=book.Medium.EBOOK  # Vitalsource specializes in ebooks
        )
        
        return output
        
    except book.BookError:
        raise
    except Exception as e:
        raise book.BookError(f"Error parsing Vitalsource: {str(e)}")

def get_test_isbn():
    """
    Return a test ISBN that exists on Vitalsource.
    
    Returns:
        int: Test ISBN number
    """
    # Using a common textbook ISBN that should be available on Vitalsource
    return 9780134685991  # Clean Code: A Handbook of Agile Software Craftsmanship

if __name__ == "__main__":
    # Test the parser
    test_isbn = get_test_isbn()
    print(f"Testing Vitalsource parser with ISBN: {test_isbn}")
    try:
        result = parse(test_isbn)
        print(f"\n{'='*60}")
        print("✅ Book Found on Vitalsource")
        print(f"{'='*60}")
        print(f"Title: {result.title}")
        print(f"ISBN: {result.isbn}")
        print(f"Price: ${result.price:.2f}")
        print(f"Link: {result.link}")
        print(f"Medium: {result.medium}")
    except book.BookError as e:
        print(f"\n❌ Error: {e.message}")

