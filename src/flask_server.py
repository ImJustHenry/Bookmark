
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
import os
template_dir = os.path.abspath(os.getcwd()+'/templates')
static_dir = os.path.abspath(os.getcwd()+'/static')
app = Flask(__name__, template_folder=template_dir,static_folder=static_dir)
socketio=SocketIO(app)
print()

@app.route("/")
def results():
    return render_template('index.html')

@app.route("/static")
def getStatic():
    return send_from_directory(static_dir, "/static")

@socketio.on("Go_button_pushed")
def go():
    print("yeet")

socketio.run(app)