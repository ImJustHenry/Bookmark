from fetch_html import fetch_html
from bs4 import BeautifulSoup
import re
import json
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
        # Strategy 1: Look for product search results - they're in <li> elements with class "product-search-result__wrapper"
        product_result = soup.find('li', class_=re.compile(r'product-search-result__wrapper', re.I))
        
        # Strategy 2: If not found, try looking for any product-related elements
        if not product_result:
            # Try finding by data attributes or other patterns
            product_result = soup.find('li', class_=re.compile(r'product', re.I))
        
        # Strategy 3: Look for JSON data embedded in script tags (React component data)
        if not product_result:
            script_tags = soup.find_all('script', type='application/json', class_=re.compile(r'js-react-on-rails-component', re.I))
            for script in script_tags:
                try:
                    data = json.loads(script.string)
                    if 'assetProps' in data or 'formattedPrice' in data:
                        # Found product data in JSON, extract it
                        asset_props = data.get('assetProps', {})
                        if asset_props:
                            title = asset_props.get('title', '')
                            price_str = data.get('formattedPrice', '')
                            product_url = data.get('productUrl', '')
                            
                            if title and price_str:
                                # Extract price from formatted string like "$52.99 USD"
                                price_match = re.search(r'[\d,]+\.?\d*', price_str.replace('$', '').replace('USD', '').replace(',', ''))
                                if price_match:
                                    price = float(price_match.group())
                                    link = f"https://www.vitalsource.com{product_url}" if product_url and not product_url.startswith('http') else (product_url if product_url else search_url)
                                    isbn_int = int(str(isbn).replace('-', '').replace(' ', ''))
                                    
                                    return book.Book(
                                        link=link,
                                        title=title,
                                        isbn=isbn_int,
                                        price=price,
                                        condition=book.Condition.UNKNOWN,
                                        medium=book.Medium.EBOOK
                                    )
                except (json.JSONDecodeError, ValueError, KeyError):
                    continue
        
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
        
        # Extract price - try multiple strategies
        price = None
        
        # Strategy 1: Look for span with class containing "font-3" and "u-weight--bold"
        price_elem = product_result.find('span', class_=re.compile(r'font-3.*u-weight--bold|block.*font-3', re.I))
        if price_elem:
            price_text = price_elem.get_text(strip=True)
            price_match = re.search(r'[\d,]+\.?\d*', price_text.replace('$', '').replace('USD', '').replace(',', ''))
            if price_match:
                try:
                    price = float(price_match.group())
                except ValueError:
                    pass
        
        # Strategy 2: Look for any text containing "$" and numbers
        if price is None:
            price_elements = product_result.find_all(string=re.compile(r'\$\s*[\d,]+\.?\d*'))
            for price_elem in price_elements:
                price_text = price_elem.strip() if isinstance(price_elem, str) else price_elem.get_text(strip=True)
                price_match = re.search(r'[\d,]+\.?\d*', price_text.replace('$', '').replace('USD', '').replace(',', ''))
                if price_match:
                    try:
                        price = float(price_match.group())
                        break
                    except (ValueError, AttributeError):
                        continue
        
        # Strategy 3: Look in <p> tags that might contain price
        if price is None:
            p_tags = product_result.find_all('p')
            for p in p_tags:
                p_text = p.get_text(strip=True)
                if '$' in p_text and re.search(r'\d+', p_text):
                    price_match = re.search(r'[\d,]+\.?\d*', p_text.replace('$', '').replace('USD', '').replace(',', ''))
                    if price_match:
                        try:
                            price = float(price_match.group())
                            break
                        except ValueError:
                            continue
        
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
    # Effective Java is commonly available on Vitalsource
    return 9780134686042  # Effective Java, 3rd Edition

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

