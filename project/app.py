#!/usr/bin/env python3

from flask import Flask
from flask.ext.login import UserMixin
import model


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello'


if __name__ == '__main__':
    app.run(debug=True)
