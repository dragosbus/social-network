#!/usr/bin/env python3

from flask import Flask, url_for, request, redirect, render_template, flash
import model
import psycopg2
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_username = request.form['username']
        user_email = request.form['user-email']
        user_pass = request.form['user-password']
        repeat_pass = request.form['repeat-password']

        users = model.get_users()
        error = None
        for user in users:
            if user_username == user[1]:
                error = 'Username exist'
            if user_email == user[2]:
                error = 'Email exist'
            flash(error)
            return render_template('register.html')

        query = '''INSERT INTO users(username, email, password, joined_at, is_admin)
                   VALUES(%s, %s, %s, %s, %s)'''
        values = (user_username, user_email, user_pass, datetime.now(), False)

        model.add_user(query, values)


    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
