from flask import Flask, request, jsonify, render_template
from chegg_scraper import CheggScraper
import logging
from datetime import datetime
import time

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize the scraper
scraper = CheggScraper()

@app.route('/')
def index():
    """Serve the main HTML interface"""
    return render_template('index.html')

@app.route('/api/info')
def api_info():
    """API information endpoint"""
    return jsonify({
        'name': 'Chegg Book Price Scraper API',
        'version': '1.0.0',
        'endpoints': {
            'POST /api/search': 'Search for book prices by ISBN',
            'GET /health': 'Health check endpoint',
            'GET /api/info': 'API information'
        },
        'usage': {
            'search': {
                'method': 'POST',
                'url': '/api/search',
                'body': {'isbn': '9781234567890'},
                'response': 'Book information including title, author, price, etc.'
            }
        }
    })

@app.route('/api/search', methods=['POST'])
def search_book():
    """API endpoint to search for book prices by ISBN"""
    try:
        data = request.get_json()
        isbn = data.get('isbn', '').strip()
        
        if not isbn:
            return jsonify({'error': 'ISBN is required'}), 400
        
        # Validate ISBN format (basic validation)
        isbn_clean = isbn.replace('-', '').replace(' ', '')
        if not isbn_clean.isdigit() or len(isbn_clean) not in [10, 13]:
            return jsonify({'error': 'Invalid ISBN format. Please enter a 10 or 13 digit ISBN.'}), 400
        
        # Add rate limiting (simple implementation)
        time.sleep(1)  # 1 second delay between requests
        
        # Demo mode - return mock data to show how API works
        demo_books = {
            "9780134685991": {
                "isbn": "9780134685991",
                "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
                "author": "Robert C. Martin",
                "price": "$45.99",
                "availability": "In Stock",
                "url": "https://www.chegg.com/textbooks/clean-code-9780134685991",
                "source": "Chegg (Demo)"
            },
            "9780201633610": {
                "isbn": "9780201633610",
                "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
                "author": "Gang of Four",
                "price": "$52.50",
                "availability": "In Stock",
                "url": "https://www.chegg.com/textbooks/design-patterns-9780201633610",
                "source": "Chegg (Demo)"
            },
            "9780321125217": {
                "isbn": "9780321125217",
                "title": "Effective Java",
                "author": "Joshua Bloch",
                "price": "$38.75",
                "availability": "In Stock",
                "url": "https://www.chegg.com/textbooks/effective-java-9780321125217",
                "source": "Chegg (Demo)"
            }
        }
        
        # Check if we have demo data for this ISBN
        if isbn_clean in demo_books:
            book_info = demo_books[isbn_clean]
        else:
            # Try to scrape from Chegg (will likely fail due to protection)
            book_info = scraper.get_book_price(isbn_clean)
        
        if book_info:
            return jsonify({
                'success': True,
                'book': book_info,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Book not found or unable to retrieve price information'
            }), 404
            
    except Exception as e:
        logging.error(f"Error in search_book: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=4000)
