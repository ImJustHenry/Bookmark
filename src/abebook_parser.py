from bs4 import BeautifulSoup
from typing import List, Dict

def parse_abebooks_prices(html: str) -> List[Dict[str, str]]:
    """
    Parses AbeBooks HTML and extracts book information.
    
    Args:
        html: HTML content as a string
        
    Returns:
        List of dictionaries containing book data (title, price, condition, seller)
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
            book_data['price'] = price_tag.get_text(strip=True)
        
        condition_tag = listing.find('span', {'data-test-id': 'listing-book-condition'})
        if condition_tag:
            book_data['condition'] = condition_tag.get_text(strip=True)
        
        seller_tag = listing.find('a', {'data-test-id': 'listing-seller-link'})
        if seller_tag:
            book_data['seller'] = seller_tag.get_text(strip=True)
        
        shipping_tag = listing.find('span', {'data-test-id': 'shipping-detail'}) or \
                      listing.find('span', class_='free-shipping')
        if shipping_tag:
            book_data['shipping'] = shipping_tag.get_text(strip=True)
        
        books.append(book_data)
    
    return books
