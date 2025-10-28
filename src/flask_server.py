from flask import Flask, render_template, send_from_directory, request, make_response, jsonify
from flask_socketio import SocketIO, emit
import os
import uuid
import logging
from book_search_service import BookSearchService, search_book_by_name, search_book_by_isbn

base_dir = os.path.abspath(os.path.join(os.getcwd(), "..")) 
template_dir = os.path.join(base_dir, "templates")
static_dir = os.path.join(base_dir, "static")
app = Flask(__name__, template_folder=template_dir,static_folder=static_dir)
socketio=SocketIO(app)

# Initialize book search service
book_search_service = BookSearchService()

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route("/")
def results():
    session_id = request.cookies.get("session_id") or str(uuid.uuid4())
    resp = make_response(render_template("index.html"))
    resp.set_cookie("session_id", session_id, max_age=60*60*24) # When cookie expires
    return resp

@app.route("/static")
def getStatic():
    return send_from_directory(static_dir, "/static")

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

@socketio.on("Go_button_pushed")
def go(data):
    """Handle real-time search requests via SocketIO"""
    session_id = request.cookies.get("session_id")
    user_search = data.get("search", "").strip()
    
    if not user_search:
        emit("search_error", {"error": "Please enter a book name or ISBN"})
        return
    
    logging.info(f"[Session {session_id}] User searched for: {user_search}")
    
    # Emit search started event
    emit("search_started", {"search_term": user_search})
    
    try:
        # Determine if it's an ISBN or book name
        isbn_clean = user_search.replace('-', '').replace(' ', '')
        
        if isbn_clean.isdigit() and len(isbn_clean) in [10, 13]:
            # Search by ISBN
            result = search_book_by_isbn(isbn_clean)
        else:
            # Search by book name
            result = search_book_by_name(user_search)
        
        # Emit results
        emit("search_results", result)
        
    except Exception as e:
        logging.error(f"SocketIO search error: {str(e)}")
        emit("search_error", {"error": f"Search failed: {str(e)}"})

if __name__ == "__main__":
    socketio.run(app, debug=True, host="127.0.0.1", port=3000, allow_unsafe_werkzeug=True)