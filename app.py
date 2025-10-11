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
    """Main page for Bookmark! textbook price comparison"""
    return render_template('index.html')

@app.route('/api/search/chegg', methods=['POST'])
def search_chegg():
    """Search for book prices on Chegg by ISBN"""
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
                "source": "Chegg"
            },
            "9780201633610": {
                "isbn": "9780201633610",
                "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
                "author": "Gang of Four",
                "price": "$52.50",
                "availability": "In Stock",
                "url": "https://www.chegg.com/textbooks/design-patterns-9780201633610",
                "source": "Chegg"
            },
            "9780321125217": {
                "isbn": "9780321125217",
                "title": "Effective Java",
                "author": "Joshua Bloch",
                "price": "$38.75",
                "availability": "In Stock",
                "url": "https://www.chegg.com/textbooks/effective-java-9780321125217",
                "source": "Chegg"
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
        logging.error(f"Error in search_chegg: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/search', methods=['POST'])
def search_all_retailers():
    """Search for book prices across multiple retailers"""
    try:
        data = request.get_json()
        isbn = data.get('isbn', '').strip()
        
        if not isbn:
            return jsonify({'error': 'ISBN is required'}), 400
        
        # Validate ISBN format
        isbn_clean = isbn.replace('-', '').replace(' ', '')
        if not isbn_clean.isdigit() or len(isbn_clean) not in [10, 13]:
            return jsonify({'error': 'Invalid ISBN format. Please enter a 10 or 13 digit ISBN.'}), 400
        
        results = {
            'isbn': isbn_clean,
            'timestamp': datetime.now().isoformat(),
            'retailers': {}
        }
        
        # Search Chegg
        try:
            chegg_result = scraper.get_book_price(isbn_clean)
            if chegg_result:
                results['retailers']['chegg'] = chegg_result
        except Exception as e:
            logging.error(f"Chegg search failed: {str(e)}")
            results['retailers']['chegg'] = {'error': 'Chegg search failed'}
        
        # TODO: Add other retailers here (Amazon, eBay, etc.)
        # results['retailers']['amazon'] = search_amazon(isbn_clean)
        # results['retailers']['ebay'] = search_ebay(isbn_clean)
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        logging.error(f"Error in search_all_retailers: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/info')
def api_info():
    """API information endpoint"""
    return jsonify({
        'name': 'Bookmark! Textbook Price Comparison API',
        'version': '1.0.0',
        'description': 'Compare textbook prices across multiple retailers',
        'endpoints': {
            'POST /api/search': 'Search all retailers for book prices',
            'POST /api/search/chegg': 'Search Chegg specifically',
            'GET /health': 'Health check endpoint',
            'GET /api/info': 'API information'
        },
        'retailers': ['Chegg', 'Amazon (coming soon)', 'eBay (coming soon)']
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
