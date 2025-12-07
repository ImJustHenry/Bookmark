from fetch_html import fetch_html
from bs4 import BeautifulSoup
import re
import book

def search_vitalsource(isbn):
    """
    Construct the Vitalsource search URL for a given ISBN.
    """
    isbn_str = str(isbn).strip()
    return f"https://www.vitalsource.com/textbooks?q={isbn_str}"

def parse(isbn):
    """
    Parse Vitalsource to find book information by ISBN.
    """
    try:
        search_url = search_vitalsource(isbn)
        html_string = fetch_html(url=search_url)
        if not html_string or len(html_string) < 500:
            raise book.BookError("Empty or invalid response from Vitalsource")
        
        soup = BeautifulSoup(html_string, 'html.parser')
        
        # Extract title from <title> or og:title
        title = None
        title_tag = soup.find("title")
        if title_tag and title_tag.get_text(strip=True):
            title_text = title_tag.get_text(strip=True)
            title = title_text.split('|')[0].strip()
        
        if not title:
            og_title = soup.find("meta", property="og:title")
            if og_title and og_title.get("content"):
                title = og_title["content"].split('|')[0].strip()
        
        if not title:
            title = "Book (Vitalsource)"
        
        # Extract price from first $ amount in the page
        price = None
        price_matches = re.findall(r'\$\s*([\d,]+\.?\d*)', html_string)
        for match in price_matches:
            try:
                price_val = float(match.replace(',', ''))
                if 1.0 <= price_val <= 10000.0:
                    price = price_val
                    break
            except ValueError:
                continue
        
        if price is None:
            raise book.BookError("Price not found on Vitalsource")
        
        # Extract product link from <link rel="canonical"> or fallback to search URL
        link_tag = soup.find("link", rel="canonical")
        link = link_tag.get("href") if link_tag and link_tag.get("href") else search_url
        
        isbn_int = int(str(isbn).replace('-', '').replace(' ', ''))
        
        return book.Book(
            link=link,
            title=title,
            isbn=isbn_int,
            price=price,
            condition=book.Condition.UNKNOWN,
            medium=book.Medium.EBOOK
        )
        
    except book.BookError:
        raise
    except Exception as e:
        raise book.BookError(f"Error parsing Vitalsource: {str(e)}")

def get_test_isbn():
    # Test ISBN available on Vitalsource
    return 9781948703611  # Chicken 20 Ways

if __name__ == "__main__":
    test_isbn = get_test_isbn()
    print(f"Testing Vitalsource parser with ISBN: {test_isbn}")
    try:
        result = parse(test_isbn)
        if result:
            print(f"\n{'='*60}")
            print("✅ Book Found on Vitalsource")
            print(f"{'='*60}")
            print(f"Title: {result.title}")
            print(f"ISBN: {result.isbn}")
            print(f"Price: ${result.price:.2f}")
            print(f"Link: {result.link}")
            print(f"Medium: {result.medium}")
        else:
            print("❌ No valid book found or price missing")
    except book.BookError as e:
        print(f"\n❌ Error: {e.message}")
