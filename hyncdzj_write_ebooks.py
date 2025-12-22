#!/usr/bin/env python3
import os
import tempfile
from datetime import datetime
import time
import sys
import config
import shutil

import multiprocessing
multiprocessing.set_start_method("fork") # only POSIX
from multiprocessing import Process

from hyncdzj.book_modules import sn, mn, dn, an
from hyncdzj.book_modules import (kn_ap, kn_bv, kn_cp, kn_ps, kn_pv, kn_ud, kn_vv, kn_dhp, kn_iti, kn_jat, kn_khp, kn_snp,
                         kn_thag, kn_thig, kn_nid1, kn_nid2)
all_modules = [sn, an, mn, dn] + [kn_ap, kn_bv, kn_cp, kn_ps, kn_pv, kn_ud, kn_vv, kn_dhp, kn_iti, kn_jat, kn_khp, kn_snp,
                         kn_thag, kn_thig, kn_nid1, kn_nid2]
import hyncdzj.base
import hyncdzj.epub
#import hyncdzj.pdf

from hyncdzj import book_modules

import hyncdzj.ebook_utils

all_modules = []
for _, ms in book_modules.categories:
    for _m in ms:
        all_modules.append(_m)


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

    temp_td = tempfile.TemporaryDirectory(prefix="AAA_汉译南传大藏经_")
    config.HYNCDZJ_COVER_DIR = os.path.join(temp_td.name, "cover")
    date = datetime.today().strftime('%Y.%m.%d')

    #all_modules = [sn, an, mn, dn] # + pyabo2.kn.all_modules
    #all_modules = [pyabo2.kn.mi]
    dirs = set()
    for count, m in enumerate(all_modules, start=1):

        print("Loading data: {:2}/{} {}".format(count, len(all_modules), m.info.name), end="", flush=True)
        simple_filled_path = os.path.join(config.SIMPLE_FILLED_DIR, m.info.name)
        simple_filling_path = os.path.join(config.SIMPLE_FILLING_DIR, m.info.name)

        if os.path.exists(simple_filled_path):
            data = hyncdzj.base.load_from_disk(simple_filled_path)
            tag = "已充填"
        elif os.path.exists(simple_filling_path):
            data = hyncdzj.base.load_from_disk(simple_filling_path)
            tag = "充填中"
        else:
            simple_path = os.path.join(config.SIMPLE_DOC_DIR, m.info.name)
            data = hyncdzj.base.load_from_disk(simple_path)
            tag = None

        print(" ✅")
        time.sleep(0.1)

        for zh_name, lang in [("汉译南传大藏经_简体PDF", hyncdzj.ebook_utils.SC()), ("漢譯南傳大藏經_繁體PDF", hyncdzj.ebook_utils.TC())]:
            continue #todo

            if nopdf:
                continue
            for size in ("A4",):
                zh_name = zh_name + "_" + size

                filename = "{}_元亨寺_{}_{}_{}{}.pdf".format(lang.c(m.name_han), lang.zh, size, date, lang.c("製"))
                dirname = os.path.join(temp_td.name, zh_name)

                full_path = os.path.join(dirname, filename)

                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                job = (filename, pyabo2.pdf.build_pdf, (full_path, data, m, lang, tag, size, True))
                jobs.append(job)
                total += 1
                try_run_job()

        for zh_name, lang in [("元亨寺_汉译南传大藏经_简体_EPUB_" + date, hyncdzj.ebook_utils.SC()),
                              ("元亨寺_漢譯南傳大藏經_繁體_EPUB_" + date, hyncdzj.ebook_utils.TC())]:

            dirs.add(zh_name)
            filename = lang.c(m.info.name)
            if tag:
                filename += "_{}".format(tag)
            filename += ".epub"

            dirname = os.path.join(temp_td.name, zh_name)
            full_path = os.path.join(dirname, filename)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            jobs.append((filename, hyncdzj.epub.build_epub, (full_path, data, m, lang, tag, True)))
            total += 1
            try_run_job()


    jobs.extend(epub_jobs)

    while jobs or running:
        time.sleep(0.01)
        try_run_job(True)

    end_time = time.time()

    print(dirs)
    for dir_name in dirs:
        output_dirname = os.path.join(temp_td.name, dir_name)
        shutil.make_archive(output_dirname, 'zip', output_dirname)

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
