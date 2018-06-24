#!/usr/bin/env python3

from flask import Flask, url_for, request, redirect, render_template
import model


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
