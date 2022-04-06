#!/usr/bin/env python3
import os
import tempfile


import pyabo.book_public

from pyabo import nikayas, sn, note_thing, run_abo

import dopdf.sneb2pdf
import doepub.sn2epub


try:
    import user_config as uc
except ImportError:
    import _user_config as uc


def main():
    run_abo.make_sure_is_runing()
    domain = run_abo.get_domain()

    note_thing.load_global(domain, uc.CACHE_DIR)

    nikayas.load("sn", domain, uc.CACHE_DIR)
    nikayas.load("mn", domain, uc.CACHE_DIR)

    temprootdir_td = tempfile.TemporaryDirectory(prefix="pyabo_")

    def print_temprootdir():
        print("temprootdir: {}".format(temprootdir_td.name))

    # books_dir = os.path.join(uc.PROJECT_ROOT, "books", time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()))
    books_dir = uc.BOOKS_DIR
    os.makedirs(books_dir, exist_ok=True)

    print_temprootdir()
    #doepub.sn2epub.create(pyabo.book_public.TC(), temprootdir_td.name, books_dir, uc.EPUBCHECK)
    #doepub.sn2epub.create(pyabo.book_public.SC(), temprootdir_td.name, books_dir, uc.EPUBCHECK)
    #dopdf.sneb2pdf.create(pyabo.book_public.TC(), temprootdir_td.name, books_dir, uc.CONTEXT_BIN_PATH, uc.FONTS_DIR)
    #dopdf.sneb2pdf.create(pyabo.book_public.SC(), temprootdir_td.name, books_dir, uc.CONTEXT_BIN_PATH, uc.FONTS_DIR)

    print_temprootdir()
    while input("input e and press enter to exit:").rstrip() != "e":
        pass


if __name__ == "__main__":
    main()
