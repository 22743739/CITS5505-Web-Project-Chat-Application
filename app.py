
from flask import render_template
from flask_socketio import SocketIO
from setup import app
# user routes
from user import *
# web socket
from chat import *


@app.route('/')
@app.route('/login')
# Index Page
def login():
    return render_template('login.html')


@app.route('/register')
# Register Page
def register():
    return render_template('register.html')


@app.route('/home')
# Home Page
def home():
    return render_template('home.html')


@app.route('/search')
# Search Page
def search():
    return render_template('search.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="4000")
    SocketIO.run(app)
