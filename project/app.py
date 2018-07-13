#!/usr/bin/env python3

from flask import Flask, url_for, request, redirect, render_template, flash, jsonify
import model
import psycopg2

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

        query = 'SELECT * FROM users WHERE username = %s'
        values = (user_email, )
        users = model.get_users(query, values)

        print(users)

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

    return redirect(url_for('index'))


@app.route('/profile')
def profile():

    date = str(user_session[4])[:11].replace('-', '/')



@app.route('/find', methods=['GET','POST'])
def find():
    if request.method == 'POST':
        input_val = request.form['find_user']
        query = '''SELECT username from users WHERE username
            LIKE %s'''
        values = ('{}%'.format(input_val), )
        users = model.get_users(query, values)
        return render_template('find.html',sess=True, users=users)
    return render_template('find.html')


@app.route('/profile/edit', methods=['GET','POST'])
def edit_profile():
    global user_session
    if request.method == 'POST':
        new_first_name = request.form['first_name']
        new_last_name = request.form['last_name']
        query = 'UPDATE users SET first_name=%s, last_name=%s WHERE username = %s'
        values = (new_first_name, new_last_name, user_session[1])
        model.update_user(query, values)
        flash('Edited Successfuly!')
        return redirect(url_for('index'))
    return render_template('edit.html', sess=True, user=user_session)


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
