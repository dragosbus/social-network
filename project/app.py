#!/usr/bin/env python3

from flask import Flask, url_for, request, redirect, render_template, flash, session, escape
import model
import psycopg2
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'some_secret'

user_session = None


@app.route('/')
def index():
    global user_session

    if 'user-email' in session:
        users = model.get_users()
        for user in users:
            if escape(session['user-email']) == user[2]:
                user_session = user

        return render_template('index.html', user=user_session, sess=True)

    return render_template('index.html', sess=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['user-email']
        user_pass = request.form['user-password']

        users = model.get_users()
        user_session = None
        error = None

        for user in users:
            if user_email == user[2]:
                user_session = user

        if user_session == None:
            error = 'User not exist'
        else:
            if user_session[3] != user_pass:
                error = 'Wrong Password'

        if error:
            flash(error)
        else:
            session['user-email'] = request.form['user-email']
            return redirect(url_for('index'))

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
            if user_username == user[1] and user_email == user[2]:
                error = 'The username and email is already taken'
            if user_username == user[1]:
                error = 'The username is already taken'
            if user_email == user[2]:
                error = 'The email is already taken'
            if error:
                flash(error)
                return render_template('register.html')

        query = '''INSERT INTO users(username, email, password, joined_at, is_admin)
                   VALUES(%s, %s, %s, %s, %s)'''
        values = (user_username, user_email, user_pass, datetime.now(), False)

        model.add_user(query, values)
        flash('Registered Successfuly!')
        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user-email', None)
    return redirect(url_for('index'))


@app.route('/profile')
def profile():
    global user_session
    
    return render_template('profile.html', sess=True, user=user_session)


if __name__ == '__main__':
    app.run(debug=True)
