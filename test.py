#!/usr/bin/env python3

import os
import dateutil.parser

import requests
import urllib.parse

try:
    import user_config as config
except ImportError:
    import config as config

import pyabo

_path = "Su/Su31.htm"


def sync(filename):
    file_path = os.path.join(config.DOWNLOAD_DIR, filename)
    if os.path.exists(file_path):
        local_mtime = os.path.getmtime(file_path)
        remote_mtime = None
        if local_mtime != remote_mtime:
            download(filename)
    else:
        download(filename)


def download(filename):
    url = urllib.parse.urljoin(pyabo.ABO_WEBSITE, filename)
    print(url)
    if config.SOCKS5_PROXY is not None:
        proxies = {'http': "socks5://{}".format(config.SOCKS5_PROXY),
                   "https": "socks5://{}".format(config.SOCKS5_PROXY)}
        r = requests.get(url, proxies=proxies)
    else:
        r = requests.get(url)
    last_modified_str = r.headers['Last-Modified']

    dt = dateutil.parser.parse(last_modified_str)
    mtime = dt.timestamp()

    file_path = os.path.join(config.DOWNLOAD_DIR, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    f = open(file_path, "wb")
    f.write(r.content)
    f.close()

    atime = os.path.getatime(file_path)
    os.utime(file_path, (atime, mtime))


if __name__ == "__main__":
    sync(_path)
