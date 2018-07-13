#!/usr/bin/env python3

from flask import Flask, url_for, request, redirect, render_template, flash, jsonify, session
import model
import psycopg2
from functools import wraps

from datetime import datetime


app = Flask(__name__)
app.secret_key = 'some_secret'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['user-email']
        user_pass = request.form['user-password']
        #get user from db who match the input fields
        query = 'SELECT * FROM users WHERE email = %s'
        values = (user_email, )
        users = model.get_users(query, values)

        if len(users):
            user_session_email = users[0][2]
            user_session_pass = users[0][3]

            if user_pass == user_session_pass:
                session['logged_in'] = True
                session['username'] = user_email
                flash('Welcome {}'.format(users[0][1]))
                return redirect(url_for('index'))
            else:
                flash('Incorrect password')
                return render_template('login.html')
        else:
            flash("User not exist")
            return render_template('login.html')

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


#Check if user is logged is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Log In')
            return redirect(url_for('login'))
    return wrap


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/profile')
@is_logged_in
def profile():
    session_user_email = session['username']

    query = 'SELECT * from users WHERE email = %s'
    values = (session_user_email,)
    user = model.get_users(query, values)

    date = str(user[0][4])
    date = date[:11].replace('-','/')

    return render_template('profile.html', user=user[0], date=date)



@app.route('/find', methods=['GET','POST'])
def find():
    if request.method == 'POST':
        input_val = request.form['find_user']
        query = '''SELECT username from users WHERE username
            LIKE %s'''
        values = ('{}%'.format(input_val), )
        users = model.get_users(query, values)
        return render_template('find.html')
    return render_template('find.html')


@app.route('/profile/edit', methods=['GET','POST'])
@is_logged_in
def edit_profile():
    session_user_email = session['username']

    if request.method == 'POST':
        new_first_name = request.form['first_name']
        new_last_name = request.form['last_name']

        query = 'UPDATE users SET first_name=%s, last_name=%s WHERE email = %s'
        values = (new_first_name, new_last_name, session_user_email)
        model.update_user(query, values)

        flash('Edited Successfuly!')
        return redirect(url_for('profile'))
    return render_template('edit.html')


@app.route('/', methods=['GET','POST'])
def add_post():
    global user_session
    if request.method == 'POST':
        value_post = request.form['new-post']
        query = 'INSERT INTO posts(value, user_id) VALUES(%s, %s)'
        values = (value_post, user_session[0])
        model.add_user(query, values)
    return render_template('index.html', sess=True, user=user_session)

@app.route('/posts')
def get_posts():
    global user_session
    if user_session:
        datajs = []
        query = 'SELECT value from posts WHERE user_id = %s'
        values = (user_session[0], )
        all_data = model.get_users(query, values)
        for data in all_data:
            datajs.append(data[0])
        return jsonify({user_session[1]: datajs})
    return 'Must be logged'



if __name__ == '__main__':
    app.run(debug=True)
