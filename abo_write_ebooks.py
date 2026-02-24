#!/usr/bin/env python3
import os
import tempfile
from datetime import datetime
import time
import sys
import config
import shutil
import zipfile

import abo.kn
import abo.ebook_utils

import nikaya_share
import hyncdzj_write_ebooks
from hyncdzj_write_ebooks import max_processes, total, jobs
from hyncdzj_write_ebooks import read_args, format_seconds, try_run_job, wating_job_done, get_load_path, get_data

import hyncdzj.pdf
import hyncdzj.epub

running = []
finished = 0


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
        my_modules = abo.all_modules
    else:
        my_modules = []
        for x in books.split(","):
            for m in abo.all_modules:
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
        print("books:", [m.__name__.split(".")[-1] for m in abo.all_modules])
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
    temp_td = tempfile.TemporaryDirectory(prefix="A_莊春江_汉译经藏_")
    print("电子书目录：", temp_td.name)
    print("进程数:", max_processes)


    cover_dir = os.path.join(temp_td.name, "莊春江_cover")
    date = datetime.today().strftime('%Y.%m.%d')

    dirs = set()
    files = set()

    for lang in my_langs:
        zh_name = lang.c("莊春江_漢譯經藏")

        for count, m in enumerate(my_modules, start=1):
            load_path = os.path.join(config.ABO_XML_DIR, m.info.name)
            tag = None

            data = get_data(lang, m.info, load_path)

            catalog = [lang.c(x) for x in abo.get_catalog_by_module(m)]

            if "pdf" in my_types:
                for layout in my_layouts:
                    for font in my_fonts:

                        package_dir = "{}_{}_PDF_{}_{}_{}".format(zh_name, lang.zh, layout, font, date)

                        file_name = "{}".format(lang.c(m.info.name))
                        if tag:
                            file_name += "_{}".format(tag)
                        file_name += ".pdf"

                        dirs.add(package_dir)

                        full_file_name = os.path.join(temp_td.name, package_dir, *catalog, file_name)

                        os.makedirs(os.path.dirname(full_file_name), exist_ok=True)
                        job = (
                            "{}/{}_{}/{}".format(lang.zh, layout, font, file_name),
                            hyncdzj.pdf.build_pdf,
                            (nikaya_share.ABO, cover_dir, full_file_name, data, m.info, lang, layout, font, tag, True)
                        )
                        jobs.append(job)

                        hyncdzj_write_ebooks.total += 1
                        try_run_job()

            if "epub" in my_types:
                file_name = "{}".format(lang.c(m.info.name))
                if tag:
                    file_name += "_{}".format(tag)
                file_name += ".epub"

                package_dir = "{}_{}_EPUB_{}".format(zh_name, lang.zh, date)

                dirs.add(package_dir)

                full_file_name = os.path.join(temp_td.name, package_dir, *catalog, file_name)

                os.makedirs(os.path.dirname(full_file_name), exist_ok=True)

                jobs.append(
                    ("{}/{}".format(lang.zh, file_name),
                     hyncdzj.epub.build_epub,
                     (nikaya_share.ABO, cover_dir, full_file_name, data, m.info, lang, tag))
                )

                hyncdzj_write_ebooks.total += 1
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


if __name__ == '__main__':
    _kwargs = read_args()
    main(**_kwargs)
