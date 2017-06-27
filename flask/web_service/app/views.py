from app import app
from flask import render_template

@app.route('/')
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/slavefile.html')
@app.route('/slavefile')
def slavefile():
    return render_template('slavefile.html')

@app.route('/basefile.html')
@app.route('/basefile')
def basefile():
    return render_template('basefile.html')

@app.route('/allfile.html')
@app.route('/allfile')
def allfile():
    return render_template('allfile.html')

@app.route('/allconfig.html')
@app.route('/allconfig')
def allconfig():
    return render_template('allconfig.html')

@app.route('/newconfig.html')
@app.route('/newconfig')
def newconfig():
    return render_template('newconfig.html')