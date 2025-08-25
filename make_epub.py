#!/usr/bin/env python3
import os
import tempfile
from datetime import datetime

import pyabo2.kn
import pyabo2.epub

import pyabo2.ebook_utils


temp_td = tempfile.TemporaryDirectory(prefix="AAA_pyabo_")

date = datetime.today().strftime('%Y.%m.%d')

def main():

    for m in pyabo2.kn.all_modules:
    #for m in [pyabo2.kn.pv]:
        try:
            load_from_htm = getattr(m, "load_from_htm")
        except AttributeError:
            continue
        data = load_from_htm()

        for lang in pyabo2.ebook_utils.TC(), pyabo2.ebook_utils.SC():
            epub = pyabo2.epub.make_epub(data, m, lang)
            filename = "{}_莊_{}_{}{}.epub".format(lang.c(m.name_han), lang.zh, date, lang.c("製"))
            full_path = os.path.join(temp_td.name, filename)
            epub.write(full_path)


if __name__ == '__main__':
    main()
    input("Press any key to exit")
