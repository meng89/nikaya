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

import pyabo2.kn.mi


total = 0
jobs =  []
running = []
finished = 0

max_processes = os.cpu_count()
def try_run_job(do_print=True):
    global running, finished

    # 清理
    new_running = []
    count = 0
    for name, p in running:
        if p.is_alive():
            new_running.append((name, p))
        else:
            count += 1
            finished += 1
            if do_print:
                print("Running: {:2}, Finished: {:2}/{} ({:3}%)".format(
                    len(running) - count, finished, total, int((finished/total) * 100)), end="", flush=True)
                print("  {} ✅".format(name))

    running = new_running

    while True:
        if len(jobs) == 0 or len(running) == max_processes:
            break

        name, func, args = jobs[0]
        p = Process(target=func, args=args)
        p.start()
        running.append((name, p))
        jobs.pop(0)


def main(nopdf, noepub):
    start_time = time.time()
    print("进程数:", max_processes)

    global total

    epub_jobs = []

    temp_td = tempfile.TemporaryDirectory(prefix="AAA_莊春江汉译经藏_")
    date = datetime.today().strftime('%Y.%m.%d')

    all_modules = [sn, an, mn, dn] + pyabo2.kn.all_modules
    #all_modules = [pyabo2.kn.mi]
    for count, m in enumerate(all_modules, start=1):
        try:
            load_from_htm = getattr(m, "load_from_htm")
        except AttributeError:
            continue
        print("Loading data: {:2}/{} {}".format(count, len(all_modules), m.name_han), end="", flush=True)
        data = load_from_htm()
        print(" ✅")
        time.sleep(0.1)

        for zh_name, lang in [("莊春江汉译经藏_简体PDF", pyabo2.ebook_utils.SC()), ("莊春江漢譯經藏_繁體PDF", pyabo2.ebook_utils.TC())]:
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
                jobs.append(job)
                total += 1
                try_run_job()

        for zh_name, lang in [("莊春江汉译经藏_简体EPUB", pyabo2.ebook_utils.SC()), ("莊春江漢譯經藏_繁體EPUB", pyabo2.ebook_utils.TC())]:
            if noepub:
                continue
            filename = "{}_莊_{}_{}{}.epub".format(lang.c(m.name_han), lang.zh, date, lang.c("製"))
            dirname = os.path.join(temp_td.name, zh_name)
            if m in pyabo2.kn.all_modules:
                full_path = os.path.join(dirname, "小部(不全)", filename)
            else:
                full_path = os.path.join(dirname, filename)

            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            jobs.append((filename, pyabo2.epub.build_epub, (full_path, data, m, lang, True)))
            total += 1
            try_run_job()

    jobs.extend(epub_jobs)

    while jobs or running:
        time.sleep(0.01)
        try_run_job(True)

    end_time = time.time()
    print()
    print("用时: {:.2f}s".format(end_time - start_time))

    print()
    print("电子书临时目录在：", temp_td.name)
    while True:
        if input("键入 q 并回车，删除临时目录并退出:").strip().lower() == "q":
            break
    temp_td.cleanup()


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


