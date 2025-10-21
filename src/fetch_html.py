import requests
from UserAgentFaker import GetFakeUserAgent

def fetch_html(url: str) -> str:
    """Fetches the given URL and returns the HTML content as a string."""
    headers = {
        "User-Agent": GetFakeUserAgent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    resp = requests.get(url, headers=headers, allow_redirects=True, timeout=30)
    resp.raise_for_status() 
    return resp.text  


    
