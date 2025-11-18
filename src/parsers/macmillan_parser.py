from fetch_html import fetch_html
from bs4 import BeautifulSoup
def search_macmillan(isbn):
    return f"https://www.macmillanlearning.com/college/us/search/?text={isbn}"
    
def parse(isbn):
    search_string = search_macmillan(isbn)
    html_string = fetch_html(url=search_string)
    soup = BeautifulSoup(html_string, 'html.parser')
    price_element = soup \
    .find("div",{"class" : "priceandvaluetag"}) \
    .find("p",{"class":"text-right"}) \
    .find("strong")
    price_text_with_dollar=price_element.get_text()
    price=float(price_text_with_dollar.replace("$",""))
    return price
    