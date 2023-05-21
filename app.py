
from flask import Flask, render_template

# Create App
app = Flask(__name__, static_url_path='/static', template_folder='static')
app.debug = True


# Index Page
@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

# Register Page
@app.route('/register')
def register():
    return render_template('register.html')

# Home Page
@app.route('/home')
def home():
    return render_template('home.html')

# Search Page
@app.route('/search')
def search():
    return render_template('search.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000")
