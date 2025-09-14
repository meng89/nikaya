#!/usr/bin/env python3
import os
import tempfile
from datetime import datetime
import time

from multiprocessing import Process


from pyabo2 import sn, mn, dn, an

import pyabo2.kn
import pyabo2.epub
import pyabo2.pdf

import pyabo2.ebook_utils
from pyabo2.kn import ps


def main():
    temp_td = tempfile.TemporaryDirectory(prefix="AAA_莊春江汉译经藏_")
    date = datetime.today().strftime('%Y.%m.%d')

    jobs = []

    #for m in list(pyabo2.kn.all_modules) + [dn, mn, sn, an]:
    for m in list(pyabo2.kn.all_modules) + [sn, an, mn, dn]:
        try:
            load_from_htm = getattr(m, "load_from_htm")
        except AttributeError:
            continue
        data = load_from_htm()

        for zh_name, lang in [("莊春江漢譯經藏_繁體PDF", pyabo2.ebook_utils.TC()), ("莊春江汉译经藏_简体PDF", pyabo2.ebook_utils.SC())]:
        #for zh_name, lang in [("莊春江汉译经藏_简体PDF", pyabo2.ebook_utils.SC())]:
            #continue
            for size in ("A4",):
                zh_name = zh_name + "_" + size

                filename = "{}_莊_{}_{}_{}{}.pdf".format(lang.c(m.name_han), lang.zh, size, date, lang.c("製"))
                dirname = os.path.join(temp_td.name, zh_name)
                if m in pyabo2.kn.all_modules:
                    full_path = os.path.join(dirname, "小部(不全)", filename)
                else:
                    full_path = os.path.join(dirname, filename)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                #pyabo2.pdf.build_pdf(full_path, data, m, lang, size)
                jobs.append((filename, pyabo2.pdf.build_pdf, (full_path, data, m, lang, size, True)))
                #p = Process(target=pyabo2.pdf.build_pdf, args=(full_path, data, m, lang, size, True))
                #p.start()
                #ps.append((filename, p))

        for zh_name, lang in [("莊春江漢譯經藏_繁體EPUB", pyabo2.ebook_utils.TC()), ("莊春江汉译经藏_简体EPUB", pyabo2.ebook_utils.SC())]:
        #for zh_name, lang in [("莊春江汉译经藏_简体EPUB", pyabo2.ebook_utils.SC())]:
            filename = "{}_莊_{}_{}{}.epub".format(lang.c(m.name_han), lang.zh, date, lang.c("製"))
            dirname = os.path.join(temp_td.name, zh_name)
            if m in pyabo2.kn.all_modules:
                full_path = os.path.join(dirname, "小部(不全)", filename)
            else:
                full_path = os.path.join(dirname, filename)

            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            #pyabo2.epub.build_epub(full_path, data, m, lang)
            jobs.append((filename, pyabo2.epub.build_epub, (full_path, data, m, lang, True)))
            #p = Process(target=pyabo2.epub.build_epub, args=(full_path, data, m, lang, True))
            #p.start()
            #ps.append((filename, p))

    processes = []

    #for filename, func, args in jobs:
    #    p = Process(target=func, args=args)
    #    p.start()
    #    processes.append((filename, p))

    total = len(jobs)
    task = os.cpu_count() + os.cpu_count() // 4
    finished = 0
    while True:
        while len(processes) < task and len(jobs) > 0:
            try:
                filename, func, args = jobs.pop(0)
                p = Process(target=func, args=args)
                p.start()
                processes.append((filename, p))
            except IndexError:
                continue

        last_time = time.time()
        new_processes = []

        for filename, process in processes:
            process.join(timeout=0.01)
            if process.is_alive():
                new_processes.append((filename, process))
            else:
                finished += 1
                print(filename + " ✅️")
        processes = new_processes

        if len(processes) == 0:
            break
        else:
            cur_time = time.time()
            sleep_time = 1 - (cur_time - last_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

            print(" "*60 + "running: {}, finished: {}/{}".format(len(processes), finished, total))

    print("\n\n")
    print("电子书临时目录在：", temp_td.name)
    while True:
        if input("输入 exit 后按下回车键，会删目录并退出:").strip().lower() == "exit":
            break
    temp_td.cleanup()


if __name__ == '__main__':
    main()
