#!/usr/bin/env python3

import psycopg2
import datetime

con = psycopg2.connect(database='social')
cur = con.cursor()


def initialize():
    cur.execute('''CREATE TABLE IF NOT EXISTS
        users(user_id SERIAL PRIMARY KEY,
            username VARCHAR(100),
            email VARCHAR(100),
            password VARCHAR(100),
            joined_at TIMESTAMP,
            is_admin BOOLEAN NOT NULL)''')


def add_user():
    initialize()
    cur.execute('''INSERT INTO users(username, email, password,
        joined_at, is_admin) VALUES(%s, %s, %s, %s, %s)''',(
            'dragosbus', 'dragosbus@gmail.com', '1234', datetime.datetime.now(), True))
    con.commit()
    cur.close()
    con.close()

add_user()
