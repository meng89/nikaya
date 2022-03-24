#!/usr/bin/env python3
import os
import time
import tempfile

import pyccc.book_public

from pyccc import sn, atom_note, run_ccc

import dopdf.sneb2pdf
import doepub.sn2epub


try:
    import user_config as uc
except ImportError:
    import _user_config as uc


def main():
    run_ccc.make_sure_is_runing()
    domain = run_ccc.get_domain()

    atom_note.load_global(domain, uc.CACHE_DIR)
    pyccc.sn.load(domain, uc.CACHE_DIR)

    temprootdir_td = tempfile.TemporaryDirectory(prefix="pyccc_")

    def print_temprootdir():
        print("temprootdir: {}".format(temprootdir_td.name))

    # books_dir = os.path.join(uc.PROJECT_ROOT, "books", time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()))
    books_dir = uc.BOOKS_DIR
    os.makedirs(books_dir, exist_ok=True)

    print_temprootdir()
    #doepub.sn2epub.make(pyccc.book_public.TC(), temprootdir_td.name, books_dir)
    doepub.sn2epub.make(pyccc.book_public.SC(), temprootdir_td.name, books_dir)
    dopdf.sneb2pdf.make(pyccc.book_public.TC(), temprootdir_td.name, uc.CONTEXT_BIN_PATH, uc.FONTS_DIR, books_dir)
    dopdf.sneb2pdf.make(pyccc.book_public.SC(), temprootdir_td.name, uc.CONTEXT_BIN_PATH, uc.FONTS_DIR, books_dir)

    print_temprootdir()
    while input("input e and press enter to exit:").rstrip() != "e":
        pass


if __name__ == "__main__":
    main()
