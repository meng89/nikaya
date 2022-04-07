#!/usr/bin/env python3
import os
import tempfile


import pyabo.book_public

from pyabo.book_public import TC, SC

from pyabo import nikayas, sn, note_thing, run_abo

from dopdf import sneb2pdf
from doepub import sn2epub, mn2epub, dn2epub, an2epub


try:
    import user_config as uc
except ImportError:
    import _user_config as uc


def main():
    run_abo.make_sure_is_runing()
    domain = run_abo.get_domain()

    note_thing.load_global(domain, uc.CACHE_DIR)

    for xn in "sn", "mn", "dn", "an":
        nikayas.load(xn, domain, uc.CACHE_DIR)

    temprootdir_td = tempfile.TemporaryDirectory(prefix="pyabo_")

    def print_temprootdir():
        print("temprootdir: {}".format(temprootdir_td.name))

    # books_dir = os.path.join(uc.PROJECT_ROOT, "books", time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()))
    books_dir = uc.BOOKS_DIR
    os.makedirs(books_dir, exist_ok=True)

    print_temprootdir()

    #sn2epub.make(TC(), temprootdir_td.name, books_dir, uc.EPUBCHECK)
    #sn2epub.make(SC(), temprootdir_td.name, books_dir, uc.EPUBCHECK)
    #sneb2pdf.make(TC(), temprootdir_td.name, books_dir, uc.CONTEXT_BIN_PATH, uc.FONTS_DIR)
    #sneb2pdf.make(SC(), temprootdir_td.name, books_dir, uc.CONTEXT_BIN_PATH, uc.FONTS_DIR)
    #mn2epub.make(TC(), temprootdir_td.name, books_dir, uc.EPUBCHECK)
    #dn2epub.make(TC(), temprootdir_td.name, books_dir, uc.EPUBCHECK)
    an2epub.make(TC(), temprootdir_td.name, books_dir, uc.EPUBCHECK)

    while input("input e and press enter to exit:").rstrip() != "e":
        pass


if __name__ == "__main__":
    main()
