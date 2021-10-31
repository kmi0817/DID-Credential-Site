from app import app
from flask import render_template, redirect, url_for, session, request


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mypage')
def mypage() :
    return render_template('mypage.html')
@app.route('/signin')
def singin() :
    return render_template('signin.html')

@app.route('/signup')
def singup() :
    return render_template('signup.html')

@app.route('/tutorials')
def tutorials() :
    return render_template('tutorial.html')

@app.route('/credential')
def credential() :
    return render_template('credential.html')

@app.route('/credential-issued')
def credential_issued() :
    return render_template('credential_issued.html')