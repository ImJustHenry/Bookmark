from bs4 import BeautifulSoup
from typing import List, Dict, Union
import re
from fetch_html import fetch_html 

def parse_abebooks_prices(html: str) -> List[Dict[str, Union[str, float]]]:
    """
    Parses AbeBooks HTML and extracts book information.
    
    Args:
        html: HTML content as a string
        
    Returns:
        List of dictionaries containing book data (title, price, condition)
        where price is a float if parsable, otherwise None.
    """
    soup = BeautifulSoup(html, 'html.parser')
    books = []

    listings = soup.find_all('li', {'data-test-id': 'listing-item'})
    
    for listing in listings:
        book_data = {}

        title_tag = listing.find('span', {'data-test-id': 'listing-title'})
        if title_tag:
            book_data['title'] = title_tag.get_text(strip=True)
  
        price_tag = listing.find('p', {'data-test-id': 'item-price'})
        if price_tag:
            price_text = price_tag.get_text(strip=True)
            price_text = re.sub(r"[^\d.]", "", price_text)
            try:
                book_data['price'] = float(price_text)
            except ValueError:
                book_data['price'] = None
        
        condition_tag = listing.find('span', {'data-test-id': 'listing-book-condition'})
        if condition_tag:
            book_data['condition'] = condition_tag.get_text(strip=True)
        
        books.append(book_data)
    
    return books

def search_abebooks():
    """
    Prompts the user for ISBN and condition, then fetches and parses the top AbeBooks listing.
    """
    isbn = input("Enter ISBN number: ").strip()
    condition = input("Do you want 'new' or 'used' books? ").strip().lower()

    url = f"https://www.abebooks.com/servlet/SearchResults?cond={condition}&kn={isbn}"

    print(f"\nFetching HTML from: {url}")
    try:
        html_content = fetch_html(url)
        print(f"Successfully fetched {len(html_content)} characters of HTML\n")
        
        print("🔍 Parsing book data...")
        books = parse_abebooks_prices(html_content)
        
        if not books:
            print("No books found.")
            return None
        
        abeTopResult = books[0]
        
        print(f"\n{'='*60}")
        print("📖 First Book Found")
        print(f"{'='*60}")
        print(f"Title:     {abeTopResult.get('title', 'N/A')}")
        print(f"Price:     {abeTopResult.get('price', 'N/A')}")
        print(f"Condition: {abeTopResult.get('condition', 'N/A')}")
        print()
        
        return abeTopResult  
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

if __name__ == "__main__":
    search_abebooks()
