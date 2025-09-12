#!/usr/bin/env python3
import os
import tempfile
from datetime import datetime


from pyabo2 import sn, mn, dn, an

import pyabo2.kn
import pyabo2.epub
import pyabo2.pdf

import pyabo2.ebook_utils


def main():
    temp_td = tempfile.TemporaryDirectory(prefix="AAA_莊春江汉译经藏_")
    date = datetime.today().strftime('%Y.%m.%d')

    for m in [mn, dn, an, sn] + list(pyabo2.kn.all_modules):
        try:
            load_from_htm = getattr(m, "load_from_htm")
        except AttributeError:
            continue
        data = load_from_htm()


        for zh_name, lang in [("莊春江漢譯經藏_繁體PDF", pyabo2.ebook_utils.TC()), ("莊春江汉译经藏_简体PDF", pyabo2.ebook_utils.SC())]:
            # continue
            for size in ("A4",):
                zh_name = zh_name + "_" + size

                filename = "{}_莊_{}_{}_{}{}.pdf".format(lang.c(m.name_han), lang.zh, size, date, lang.c("製"))
                dirname = os.path.join(temp_td.name, zh_name)
                if m in pyabo2.kn.all_modules:
                    full_path = os.path.join(dirname, "小部(不全)", filename)
                else:
                    full_path = os.path.join(dirname, filename)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                pyabo2.pdf.build_pdf(full_path, data, m, lang, size)


        for zh_name, lang in [("莊春江漢譯經藏_繁體EPUB", pyabo2.ebook_utils.TC()), ("莊春江汉译经藏_简体EPUB", pyabo2.ebook_utils.SC())]:
            epub = pyabo2.epub.build_epub(data, m, lang)
            filename = "{}_莊_{}_{}{}.epub".format(lang.c(m.name_han), lang.zh, date, lang.c("製"))
            dirname = os.path.join(temp_td.name, zh_name)
            if m in pyabo2.kn.all_modules:
                full_path = os.path.join(dirname, "小部(不全)", filename)
            else:
                full_path = os.path.join(dirname, filename)

            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            epub.write(full_path)

    print("电子书临时目录在：", temp_td.name)
    input("按回车键删目录并退出")
    temp_td.cleanup()


if __name__ == '__main__':
    main()
