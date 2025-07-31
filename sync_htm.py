#!/usr/bin/env python3

import os
import time

import dateutil.parser

import requests
import urllib.parse

try:
    import user_config as config
except ImportError:
    import config as config

import pyabo

import pyabo2.kn
import pyabo2.note


# _headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}


def r_mtime(session):
    last_modified_str = session.headers['Last-Modified']
    dt = dateutil.parser.parse(last_modified_str)
    return dt.timestamp()


def sync(filename,  session, fresh_time=None, check_mtime=True):
    url = urllib.parse.urljoin(pyabo.ABO_WEBSITE, filename)
    file_path = os.path.join(config.DOWNLOAD_DIR, filename)

    # 没有文件时，要下载
    if not os.path.exists(file_path):
        print("File not found:", filename)
        download(filename, session)
        return


    ctime = os.path.getctime(file_path)
    if fresh_time is not None:
        # 不新鲜了，要检查远端的修改时间
        if time.time() - ctime > fresh_time:
            print("Not Fresh enough:", filename)
            if check_mtime:
                local_mtime = os.path.getmtime(file_path)
                r = session.head(url)
                remote_mtime = r_mtime(r)
                # 修改时间和远程不一样，要下载
                if local_mtime != remote_mtime:
                    print("Not same mtimes:", filename)
                    download(filename, session)
                else:
                    file_path = os.path.join(config.DOWNLOAD_DIR, filename)
                    with open(file_path, "rb") as f:
                        data = f.read()
                    os.remove(file_path)
                    with open(file_path, "wb")as f:
                        f.write(data)
                    atime = os.path.getatime(file_path)
                    os.utime(file_path, (atime, local_mtime))


            else:
                download(filename, session)


def download(filename, session):
    url = urllib.parse.urljoin(pyabo.ABO_WEBSITE, filename)
    print("Download:", url)
    if config.SOCKS5_PROXY is not None:
        proxies = {'http': "socks5://{}".format(config.SOCKS5_PROXY),
                   "https": "socks5://{}".format(config.SOCKS5_PROXY)}
        r = session.get(url, proxies=proxies)
    else:
        r = session.get(url)

    mtime = r_mtime(r)
    file_path = os.path.join(config.DOWNLOAD_DIR, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass

    f = open(file_path, "wb")
    f.write(r.content)
    f.close()

    atime = os.path.getatime(file_path)
    os.utime(file_path, (atime, mtime))


def main(fresh_time, check_mtime):
    session = requests.Session()
    for module in [pyabo2.note] + list(pyabo2.kn.all_modules):
        for filename in module.htmls:
            sync(filename, session, fresh_time, check_mtime)


if __name__ == "__main__":
    main(fresh_time=60 * 60 * 24 * 2, check_mtime=True)
