#!/usr/bin/env python3

from flask import Flask, url_for, request, redirect, render_template
import model


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user_username = request.form['username']
        user_email = request.form['user-email']
        user_pass = request.form['user-password']
        repeat_pass = request.form['repeat-password']

        if user_username:
            return 'Hello {}'.format(user_username)
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
