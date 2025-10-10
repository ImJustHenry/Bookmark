# Chegg Book Price Scraper API

A Flask-based API that scrapes book prices from Chegg using ISBN numbers. This backend service provides book information including title, author, price, and availability.

## Features

- 🔍 **ISBN Search**: Search for books using 10 or 13 digit ISBN numbers
- 💰 **Price Information**: Get current book prices from Chegg
- 📚 **Book Details**: Retrieve title, author, and availability information
- 🚀 **RESTful API**: Clean JSON API endpoints
- ⚡ **Rate Limiting**: Built-in rate limiting to respect Chegg's servers
- 🛡️ **Error Handling**: Comprehensive error handling and validation

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project files**
   ```bash
   cd /Users/revateesadammalapati/Book
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **The API will be available at**
   ```
   http://localhost:5000
   ```

## API Usage

### Endpoints

#### GET `/`
Returns API information and usage instructions.

**Response:**
```json
{
  "name": "Chegg Book Price Scraper API",
  "version": "1.0.0",
  "endpoints": {
    "POST /api/search": "Search for book prices by ISBN",
    "GET /health": "Health check endpoint"
  }
}
```

#### POST `/api/search`
Search for book prices by ISBN.

**Request Body:**
```json
{
  "isbn": "9781234567890"
}
```

**Success Response:**
```json
{
  "success": true,
  "book": {
    "isbn": "9781234567890",
    "title": "Introduction to Algorithms",
    "author": "Thomas H. Cormen",
    "price": "$89.99",
    "availability": "In Stock",
    "url": "https://www.chegg.com/textbooks/...",
    "source": "Chegg"
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Book not found or unable to retrieve price information"
}
```

#### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Example Usage

#### Using curl:
```bash
# Search for a book
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"isbn": "9780134685991"}'

# Check API health
curl http://localhost:5000/health
```

#### Using Python requests:
```python
import requests

# Search for a book
response = requests.post(
    'http://localhost:5000/api/search',
    json={'isbn': '9780134685991'}
)

if response.status_code == 200:
    data = response.json()
    if data['success']:
        book = data['book']
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print(f"Price: {book['price']}")
    else:
        print(f"Error: {data['error']}")
```

## Important Notes

### Rate Limiting
- The API includes a 1-second delay between requests to respect Chegg's servers
- Avoid making too many requests in a short time period

### Legal Considerations
- This scraper is for educational purposes
- Always respect Chegg's Terms of Service
- Consider implementing proper robots.txt compliance
- Use responsibly and don't overload their servers

### Error Handling
- Invalid ISBN format (must be 10 or 13 digits)
- Books not found on Chegg
- Network/connection issues
- Chegg website structure changes

### Limitations
- Dependent on Chegg's website structure (may break if they change their HTML)
- No authentication or API key required (web scraping approach)
- Rate limited to prevent abuse

## Project Structure

```
Book/
├── app.py                     # Main Flask application
├── chegg_scraper.py          # Enhanced Chegg web scraping logic
├── user_agent_faker.py       # User agent rotation utility
├── chegg_scrapebot.py        # Standalone scraper (command line)
├── enhanced_scraper_test.py  # Comprehensive test suite
├── test_api.py              # Basic API tests
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Dependencies

- **Flask**: Web framework for the API
- **requests**: HTTP library for web scraping
- **beautifulsoup4**: HTML parsing library
- **lxml**: XML/HTML parser backend
- **python-dotenv**: Environment variable management

## Troubleshooting

### Common Issues

1. **"Book not found" errors**
   - Verify the ISBN is correct (10 or 13 digits)
   - Check if the book exists on Chegg
   - Try with different ISBN formats (with/without dashes)

2. **Connection errors**
   - Check your internet connection
   - Chegg might be blocking requests (try with different User-Agent)

3. **Empty responses**
   - Chegg's website structure might have changed
   - Check the scraper logs for detailed error messages

### Debug Mode
Run the application in debug mode for detailed logging:
```bash
FLASK_ENV=development python app.py
```

## Contributing

Feel free to improve the scraper by:
- Adding support for more book retailers
- Improving error handling
- Adding caching mechanisms
- Implementing better rate limiting strategies

## Disclaimer

This tool is for educational purposes only. Please respect Chegg's Terms of Service and use responsibly. The authors are not responsible for any misuse of this software.
