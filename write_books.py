#!/usr/bin/env python3
import os
import tempfile
from datetime import datetime
import time
import sys
import config

from multiprocessing import Process

from pyabo2 import sn, mn, dn, an

import pyabo2.kn
import pyabo2.epub
import pyabo2.pdf

import pyabo2.ebook_utils

def sp(s):
    for c in s:
        print(c, end='', flush=True)
        time.sleep(0.02)


def main(nopdf, noepub):
    pdf_jobs = []
    epub_jobs = []




    temp_td = tempfile.TemporaryDirectory(prefix="AAA_莊春江汉译经藏_")
    date = datetime.today().strftime('%Y.%m.%d')

    all_modules = [sn, an, mn, dn] + list(pyabo2.kn.all_modules)
    for count, m in enumerate(all_modules, start=1):
        try:
            load_from_htm = getattr(m, "load_from_htm")
        except AttributeError:
            continue
        sp("Loading data: {:2}/{} {}".format(count, len(all_modules), m.name_han))
        data = load_from_htm()
        sp(" ✅\n")
        time.sleep(0.5)

        for zh_name, lang in [("莊春江漢譯經藏_繁體PDF", pyabo2.ebook_utils.TC()), ("莊春江汉译经藏_简体PDF", pyabo2.ebook_utils.SC())]:
            if nopdf:
                continue
            for size in ("A4",):
                zh_name = zh_name + "_" + size

                filename = "{}_莊_{}_{}_{}{}.pdf".format(lang.c(m.name_han), lang.zh, size, date, lang.c("製"))
                dirname = os.path.join(temp_td.name, zh_name)
                if m in pyabo2.kn.all_modules:
                    full_path = os.path.join(dirname, "小部(不全)", filename)
                else:
                    full_path = os.path.join(dirname, filename)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                job = (filename, pyabo2.pdf.build_pdf, (full_path, data, m, lang, size, True))
                pdf_jobs.append(job)
        for zh_name, lang in [("莊春江漢譯經藏_繁體EPUB", pyabo2.ebook_utils.TC()), ("莊春江汉译经藏_简体EPUB", pyabo2.ebook_utils.SC())]:
            if noepub:
                continue
            filename = "{}_莊_{}_{}{}.epub".format(lang.c(m.name_han), lang.zh, date, lang.c("製"))
            dirname = os.path.join(temp_td.name, zh_name)
            if m in pyabo2.kn.all_modules:
                full_path = os.path.join(dirname, "小部(不全)", filename)
            else:
                full_path = os.path.join(dirname, filename)

            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            epub_jobs.append((filename, pyabo2.epub.build_epub, (full_path, data, m, lang, True)))



    while True:
        if jobs:
            if run_job(jobs[0])
                #sp("Running: {:2}, Finished: {:2}/{} ({:3}%)     ".format(len(processes), finished, total, int((finished/total) * 100)))


    print("\n\n")
    print("电子书临时目录在：", temp_td.name)
    while True:
        if input("输入 exit 后按下回车键，会删目录并退出:").strip().lower() == "exit":
            break
    temp_td.cleanup()


finished = 0
def run_job(running_jobs):
    new_running = []
    for name, p in running_jobs:
        if p.is_alive():
            new_running.append((name, p))
        else:
            finished += 1

    running = new_running

    while True:
        if len(jobs) < 0 or len(running) == os.cpu_count() + os.cpu_count() // 4:
            break

    task = os.cpu_count() + os.cpu_count() // 4
    if len(running) < task:
        filename, func, args = job
        p = Process(target=func, args=args)
        p.start()
        running.append((filename, p))
        return True
    else:
        jobs.insert(0, job)
        return False


if __name__ == '__main__':
    sys_args = [arg.lower() for arg in sys.argv[1:]]
    _nopdf = False
    _noepub = False
    if "debug" in sys_args:
        config.DEBUG = True
    if "nopdf" in sys_args:
        _nopdf = True
    if "noepub" in sys_args:
        _noepub = True
    main(_nopdf, _noepub)


