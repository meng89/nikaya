#!/usr/bin/env python3
import os
import tempfile
from datetime import datetime
import time
import sys
import config
import shutil
import zipfile
import multiprocessing
multiprocessing.set_start_method("fork") # only POSIX
from multiprocessing import Process

import nikaya_share
import hyncdzj.base
import hyncdzj.epub
import hyncdzj.pdf
from hyncdzj import book_modules
import hyncdzj.ebook_utils


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
        if len(jobs) == 0 or len(running) >= max_processes:
            break

        name, func, args = jobs[0]
        p = Process(target=func, args=args)
        p.start()
        running.append((name, p))
        jobs.pop(0)


def wating_job_done():
    while jobs or running:
        time.sleep(0.01)
        try_run_job(True)


sc_datas = []
tc_datas = []
def get_data(lang, info, load_dir):
    tc_data = None
    for info2, data in tc_datas:
        if info2 == info:
            tc_data = data

    if tc_data is None:
        print("Loading Data: {:2}".format(info.name), end="", flush=True)
        tc_data = nikaya_share.load_from_disk(load_dir)
        print(" ✅")
        tc_datas.append((info, tc_data))

    if isinstance(lang, nikaya_share.TC):
        return tc_data

    for info2, data in sc_datas:
        if info2 == info:
            return data
    #print("机换数据: {:2}".format(info.name), end="", flush=True)
    sc_data = hyncdzj.trans_data(tc_data, lang.c)
    #print(" ✅")
    sc_datas.append((info, sc_data))
    return sc_data

def get_load_path(info):
    simple_filled_path = os.path.join(config.SIMPLE_FILLED_DIR, info.name)
    simple_filling_path = os.path.join(config.SIMPLE_FILLING_DIR, info.name)

    if os.path.exists(simple_filled_path):
        load_path = simple_filled_path
        tag = "已充填"
    elif os.path.exists(simple_filling_path):
        load_path = simple_filling_path
        tag = "充填中"
    else:
        load_path = os.path.join(config.HYNCDZJ_SIMPLE_XML_DIR, info.name)
        tag = None

    return load_path, tag


def main(_help=False, debug=False, types=None, langs=None, books=None, onebook=False, layouts=None, fonts=None):
    config.DEBUG = debug

    all_types = ["pdf", "epub"]
    if types:
        my_types = types.split(",")
    else:
        my_types = all_types

    all_langs = [nikaya_share.SC(), nikaya_share.TC()]
    if langs:
        my_langs = []
        for lang in langs.split(","):
            for _lang in all_langs:
                if lang == _lang.en:
                    my_langs.append(_lang)
    else:
        my_langs = all_langs

    if books is None:
        my_modules = book_modules.all_modules
    else:
        my_modules = []
        for x in books.split(","):
            for m in book_modules.all_modules:
                if x == m.__name__.split(".")[-1]:
                    my_modules.append(m)


    all_layouts = hyncdzj.pdf.layouts.keys()
    if layouts:
        my_layouts = []
        _ls = layouts.split(",")
        for _l in _ls:
            for layout in all_layouts:
                if layout.startswith(_l):
                    my_layouts.append(layout)
    else:
        my_layouts = all_layouts

    all_fonts = hyncdzj.pdf.fonts.keys()
    if fonts:
        my_fonts = []
        for _l in fonts.split(","):
            if _l in all_fonts:
                my_fonts.append(_l)
    else:
        my_fonts = all_fonts

    if _help:
        print("types:", all_types)
        print("langs:", [lang.en for lang in all_langs])
        print("books:", [m.__name__.split(".")[-1] for m in book_modules.all_modules])
        print("onebook:", onebook)
        print("layouts:", list(all_layouts))
        print("fonts:", list(all_fonts))
        print()
        print("命令行举例，只制作《相应部》和《中部》的简体版，不要 EPUB，且包含所有页面布局为 letter 开头的 PDF：")
        print("./hyncdzj_write_ebooks.py books=sn,mn langs=sc types=pdf layouts=letter")
        print()
        exit()

    print("显示简略使用说明：", sys.argv[0], "help")
    print()
    start_time = time.time()
    temp_td = tempfile.TemporaryDirectory(prefix="A_元亨寺_汉译南传大藏经_")
    print("电子书目录：", temp_td.name)
    print("进程数:", max_processes)

    global total

    cover_dir = os.path.join(temp_td.name, "元亨寺_cover")
    date = datetime.today().strftime('%Y.%m.%d')

    dirs = set()
    files = set()

    for lang in my_langs:
        zh_name = lang.c("元亨寺_漢譯南傳大藏經")

        if onebook:
            tag = None
            info_datas = []

            for m2 in book_modules.all_modules:
                load_path, tag2 = get_load_path(m2.info)
                tag = tag2 or tag
                info_datas.append((m2.info, get_data(lang, m2.info, load_path)))

                if config.DEBUG:
                    break
            file_name = "{}_{}".format(zh_name, lang.c("合訂本"))


            if "pdf" in my_types:
                for layout in my_layouts:
                    for font in my_fonts:

                        if tag:
                            file_name += "_{}".format(tag)
                        file_name += "_{}_{}".format(lang.zh, date)
                        file_name += ".pdf"
                        files.add(file_name)
                        full_file_name = os.path.join(temp_td.name, file_name)
                        job = (
                            "{}/{}".format(lang.zh, file_name),
                            hyncdzj.pdf.build_epub_one_book,
                            (nikaya_share.HYNCDZJ, cover_dir, full_file_name, info_datas, lang, layout, font, tag)
                        )
                        jobs.append(job)
                        total += 1
                        try_run_job()

            if "epub" in my_types:
                if tag:
                    file_name += "_{}".format(tag)
                file_name += "_{}_{}".format(lang.zh, date)
                file_name += ".epub"
                files.add(file_name)
                full_file_name = os.path.join(temp_td.name, file_name)

                job = (
                    "{}/{}".format(lang.zh, file_name),
                    hyncdzj.epub.build_epub_one_book,
                    (nikaya_share.HYNCDZJ, zh_name, cover_dir, full_file_name, info_datas, lang, tag)
                )
                jobs.append(job)
                total += 1
                try_run_job()

        for count, m in enumerate(my_modules, start=1):
            load_path, tag = get_load_path(m.info)

            data = get_data(lang, m.info, load_path)

            classi = [lang.c(x) for x in book_modules.get_classification(m)]

            if "pdf" in my_types:
                for layout in my_layouts:
                    for font in my_fonts:

                        package_dir = "{}_{}_PDF_{}_{}_{}".format(zh_name, lang.zh, layout, font, date)

                        file_name = "{}".format(lang.c(m.info.name))
                        if tag:
                            file_name += "_{}".format(tag)
                        file_name += ".pdf"

                        dirs.add(package_dir)

                        full_file_name = os.path.join(temp_td.name, package_dir, *classi, file_name)

                        os.makedirs(os.path.dirname(full_file_name), exist_ok=True)

                        job = (
                            "{}/{}_{}/{}".format(lang.zh, layout, font, file_name),
                            hyncdzj.pdf.build_pdf,
                            (nikaya_share.HYNCDZJ, cover_dir, full_file_name, data, m.info, lang, layout, font, tag)
                        )

                        jobs.append(job)
                        total += 1
                        try_run_job()

            if "epub" in my_types:
                file_name = "{}".format(lang.c(m.info.name))
                if tag:
                    file_name += "_{}".format(tag)
                file_name += ".epub"

                package_dir = "{}_{}_EPUB_{}".format(zh_name, lang.zh, date)

                dirs.add(package_dir)

                full_file_name = os.path.join(temp_td.name, package_dir, *classi, file_name)

                os.makedirs(os.path.dirname(full_file_name), exist_ok=True)

                jobs.append(
                    ("{}/{}".format(lang.zh, file_name),
                     hyncdzj.epub.build_epub,
                     (nikaya_share.HYNCDZJ, cover_dir, full_file_name, data, m.info, lang, tag))
                )

                total += 1
                try_run_job()

    wating_job_done()

    end_time = time.time()

    if not debug:
        for dir_name in dirs:
            output_dirname = os.path.join(temp_td.name, dir_name)
            shutil.make_archive(output_dirname, 'zip', output_dirname)

            shutil.rmtree(output_dirname)

        for file_name in files:
            full_file_name = os.path.join(temp_td.name, file_name)
            zf = zipfile.ZipFile(full_file_name + ".zip", "w")
            zf.write(full_file_name, arcname=os.path.basename(file_name))
            zf.close()

            os.remove(full_file_name)

        shutil.rmtree(cover_dir)


    print()
    print("用时:", format_seconds(end_time - start_time))

    print()
    print("电子书临时目录在：", temp_td.name)
    while True:
        if input("键入 q 并回车，删除临时目录并退出:").strip().lower() == "q":
            break
    temp_td.cleanup()


def read_args():
    kwargs = {}
    for x in sys.argv[1:]:
        if "=" in x:
            k, v = x.split("=")
            kwargs[k] = v
        else:
            if x == "help":
                x = "_help"
            kwargs[x] = True
    return kwargs


def format_seconds(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    parts = []
    if d > 0: parts.append(f"{d}d")
    if h > 0: parts.append(f"{h}h")
    if m > 0: parts.append(f"{m}m")
    if s > 0 or not parts: parts.append(f"{s}s")

    return " ".join(parts)


if __name__ == '__main__':
    _kwargs = read_args()
    main(**_kwargs)
