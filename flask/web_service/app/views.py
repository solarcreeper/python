from app import app
from flask import render_template

@app.route('/')
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')