import requests

url = "https://www.abebooks.com/servlet/SearchResults?ds=20&kn=abby%20jimenez%20books"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Fetch the page
resp = requests.get(url, headers=headers, allow_redirects=True, timeout=30)
resp.raise_for_status()

# Get HTML content
html = resp.text

# Save to file
with open("page.html", "w", encoding="utf-8") as f:
    f.write(html)

# Print HTML as a string
print(html)

print("Saved page.html — length:", len(html))
