#!/usr/bin/env python3

import os

from flask import Flask

from config import CCC_DIR

ROOT = os.path.join(CCC_DIR, 'agama/htdocs/agama')

app = Flask(__name__, static_folder=ROOT)


@app.route('/')
def index():
    return app.send_static_file('index.htm')


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    app.run(debug=True, port=1080, host='127.0.0.1')
