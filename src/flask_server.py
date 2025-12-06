import sys
import os

#ensure that Python can find src and parsers
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "parsers"))

from flask import Flask, render_template, send_from_directory, request, make_response, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit
import pickle
import os
import uuid
import logging
from book_search_service import BookSearchService, search_book_by_name, search_book_by_isbn
import book_finder
import google_books_api
import book
from ai import get_recommendations
import base64
# Calculate base directory - use file location for reliability
# flask_server.py is in src/, so go up one level to get project root
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Fallback: try current working directory if templates not found
if not os.path.exists(os.path.join(base_dir, "templates")):
    # In CI, templates might be in current working directory
    cwd = os.getcwd()
    if os.path.exists(os.path.join(cwd, "templates")):
        base_dir = cwd
    # Or try parent of cwd
    elif os.path.exists(os.path.join(os.path.dirname(cwd), "templates")):
        base_dir = os.path.dirname(cwd)

template_dir = os.path.join(base_dir, "templates")
static_dir = os.path.join(base_dir, "static")
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
socketio=SocketIO(app)

# Initialize book search service
#book_search_service = BookSearchService()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Global variable for best book (from main branch)
# best_book = book.Book("", "", 0, 0, book.Condition.UNKNOWN, book.Medium.UNKNOWN, "")

@app.route("/")
def home(): #renamed this from "results" to "home" for clarity
    session_id = request.cookies.get("session_id") or str(uuid.uuid4())
    resp = make_response(render_template("index.html"))
    resp.set_cookie("session_id", session_id, max_age=60*60*24) # When cookie expires

    return resp

@app.route("/static")
def getStatic():
    return send_from_directory(static_dir, "/static")

@app.route("/results")
def results_page():
    best_book_pickle_str = request.cookies.get("best_book")
    best_book = pickle.loads(base64.b64decode(best_book_pickle_str))
    # Use getattr with defaults in case attributes don't exist
    description = getattr(best_book, 'description', 'No description available.')
    image = getattr(best_book, 'image', '')
    return render_template("ResultsPage.html", link = best_book.link, title =  best_book.title, price =  best_book.price, isbn =  best_book.isbn, description = description, image = image)

@app.route("/api/search/book", methods=["POST"])
def search_book_api():
    """API endpoint to search for books by name"""
    try:
        data = request.get_json()
        book_name = data.get("book_name", "").strip()
        
        if not book_name:
            return jsonify({"error": "Book name is required"}), 400
        
        logging.info(f"API search request for book: {book_name}")
        result = search_book_by_name(book_name)
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"API search error: {str(e)}")
        return jsonify({"error": "Search failed", "details": str(e)}), 500

@app.route("/api/search/isbn", methods=["POST"])
def search_isbn_api():
    """API endpoint to search for books by ISBN"""
    try:
        data = request.get_json()
        isbn = data.get("isbn", "").strip()
        
        if not isbn:
            return jsonify({"error": "ISBN is required"}), 400
        
        # Basic ISBN validation
        isbn_clean = isbn.replace('-', '').replace(' ', '')
        if not isbn_clean.isdigit() or len(isbn_clean) not in [10, 13]:
            return jsonify({"error": "Invalid ISBN format"}), 400
        
        logging.info(f"API search request for ISBN: {isbn}")
        result = search_book_by_isbn(isbn_clean)
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"API ISBN search error: {str(e)}")
        return jsonify({"error": "ISBN search failed", "details": str(e)}), 500

@app.route("/api/health")
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Bookmark! Book Search API",
        "features": ["Google Books", "Chegg", "AbeBooks"]
    })

@app.route("/load")
def load_screen():
    return render_template("load.html")


@socketio.on("Go_button_pushed")
def go(data):
    session_id = request.cookies.get("session_id") 
    user_search = data.get("search", "").strip()
    
    # if not user_search:
    #     emit("search_error", {"error": "Please enter a book name or ISBN"})
    #     return
    
    logging.info(f"[Session {session_id}] User searched for: {user_search}")
    
    # Emit search started event
    emit("search_started", {"search_term": user_search})
  

   # try:
    googleBooksAPIObject = google_books_api.GoogleBooksAPI()
    book_results = googleBooksAPIObject.search_book_by_name(user_search)
    if book_results and len(book_results) > 0:
        isbn = book_results[0]['isbn']
        found_book = book_finder.find_cheapest_book(isbn)
        if found_book != None:
            best_book = found_book
            best_book.description = book_results[0].get('description', 'No description available.')
            best_book.image = book_results[0].get('thumbnail', '')
            best_book_pickle_str = base64.b64encode(pickle.dumps(best_book)).decode('ascii')
            socketio.emit('set_best_book_cookie', best_book_pickle_str)
            socketio.emit('redirect', url_for('results_page'))
   
"""    
    except Exception as e:
        logging.error(f"SocketIO search error: {str(e)}")
        emit("search_error", {"error": f"Search failed: {str(e)}"})
        """

@socketio.on('get_ai_recommendations')
def handle_ai_recommendations(data):
    logging.info(f"AI request received: {data}")
    current_book = data['currentBook']
    history = data['history'] 

    try:
        recommendations = get_recommendations(history, current_book)
        logging.info(f"Recommendations: {recommendations}")
        emit('ai_recommendations', recommendations)
    except Exception as e:
        logging.error(f"AI error: {str(e)}")
        emit('ai_error', str(e))


# Prevents the server from starting during tests or imports
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=3000, allow_unsafe_werkzeug=True)
