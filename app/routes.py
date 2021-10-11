from app import app
from flask import render_template, redirect, url_for, session, request


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin')
def singin() :
    return render_template('signin.html')

@app.route('/credential')
def credential() :
    return render_template('credential.html')