#!/usr/bin/env python3

import time
import threading

from flask import Flask

try:
    import user_config as uc
except ImportError:
    import _user_config as uc

_is_runing = False

_url = None

app = Flask(__name__, static_folder=uc.INDEX_DIR)


@app.route('/')
def index():
    return app.send_static_file('index.htm')


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)


class RunCccThread(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self._host = host
        self._port = port

    def run(self):
        app.run(host=self._host, port=self._port, debug=False, use_reloader=False)


def get_domain():
    return _url


def is_runing():
    return _is_runing


def make_sure_is_runing():
    host = "127.0.0.1"
    port = 8080
    global _is_runing
    if not _is_runing:
        run_ccc_thread = RunCccThread(host, port)
        run_ccc_thread.daemon = True
        run_ccc_thread.start()

        _is_runing = True

        global _url
        _url = "http://{}:{}".format(host, port)
    time.sleep(2)
