from flask import Flask, render_template, send_from_directory, request, make_response
from flask_socketio import SocketIO
import os
import uuid
import book_finder
import google_books_api

base_dir = os.path.abspath(os.path.join(os.getcwd(), "..")) 
template_dir = os.path.join(base_dir, "templates")
static_dir = os.path.join(base_dir, "static")
app = Flask(__name__, template_folder=template_dir,static_folder=static_dir)
socketio=SocketIO(app)
print()

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
    return render_template("ResultsPage.html")

@socketio.on("Go_button_pushed")
def go(data):
    session_id = request.cookies.get("session_id")
    user_search = data.get("search", "")
    googleBooksAPIObject = google_books_api.GoogleBooksAPI()
    isbn = googleBooksAPIObject.search_book_by_name(user_search)[0]['isbn']
    print(f"[Session {session_id}] User searched for: {user_search}")
    result = book_finder.find_cheapest_book(isbn)
    if result != None:
        print(result.link)
    else:
        print("No books found :(")


socketio.run(app)