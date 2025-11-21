from fetch_html import fetch_html
from bs4 import BeautifulSoup
import book
def search_macmillan(isbn):
    return f"https://www.macmillanlearning.com/college/us/search/?text={isbn}"
    
def parse(isbn):
    search_string = search_macmillan(isbn)
    html_string = fetch_html(url=search_string)
    print(search_string)
    soup = BeautifulSoup(html_string, 'html.parser')
    # CHECK IF THERE IS NOT A PRICE AND VALUE TAG
    if not soup.find("div",{"class" : "priceandvaluetag"}):
        raise book.BookError("Book not found on site!")
    # GET PRICE
    price_element = soup \
    .find("div",{"class" : "priceandvaluetag"}) \
    .find("p",{"class":"text-right"}) \
    .find("strong")
    price_text_with_dollar=price_element.get_text()
    price=float(price_text_with_dollar.replace("$",""))
    # GET TITLE
    title_element = soup \
    .find("a",{"class" : "btn-search-icbutton searchTextHide"})
    title = title_element.get_text()
    output = book.Book(
        link=search_string,
        title=title,isbn=isbn,
        price=price,
        condition=book.Condition.UNKNOWN,
        medium=book.Medium.UNKNOWN
        )
    return output

def get_test_isbn():
    return 9781319221478 # Worlds of History, Volume 1