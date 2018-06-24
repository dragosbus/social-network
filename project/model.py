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


def add_user(q, values):
    con = psycopg2.connect(database='social')
    cur = con.cursor()
    cur.execute(q, values)
    con.commit()
    cur.close()
    con.close()

def get_users():
    con = psycopg2.connect(database='social')
    cur = con.cursor()
    cur.execute('''SELECT * FROM users''')
    res = cur.fetchall();
    cur.close()
    con.close()

    return res
