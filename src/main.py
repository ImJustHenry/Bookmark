from fetch_html import fetch_html
from abebook_parser import parse_abebooks_prices

def main():
    url = "https://www.abebooks.com/book-search/kw/9781118449196/"
    
    print("Fetching HTML from AbeBooks...")
    try:
        html_content = fetch_html(url)
        print(f"Successfully fetched {len(html_content)} characters of HTML\n")
        
        print("Parsing book data...")
        books = parse_abebooks_prices(html_content)
        
        if not books:
            print("No books found.")
            return None
        
        first_book = books[0]
        
        print(f"{'='*60}")
        print("First Book Found")
        print(f"{'='*60}")
        print(f"Title:     {first_book.get('title', 'N/A')}")
        print(f"Price:     {first_book.get('price', 'N/A')}")
        print(f"Condition: {first_book.get('condition', 'N/A')}")
        print(f"Seller:    {first_book.get('seller', 'N/A')}")
        print(f"Shipping:  {first_book.get('shipping', 'N/A')}")
        print()
        
        return first_book  
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

if __name__ == "__main__":
    main()
