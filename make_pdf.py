#!/usr/bin/env python3
import os
import time
import tempfile
import subprocess
import pathlib

import pyccc.pdf.sn2pdf
import run_ccc

from pyccc import sn, atom_note


try:
    import user_config as uc
except ImportError:
    import _user_config as uc


def main():
    run_ccc.make_sure_is_runing()
    domain = run_ccc.get_domain()

    atom_note.load_global(domain)
    pyccc.sn.load(domain, uc.CACHE_DIR)

    temprootdir_td = tempfile.TemporaryDirectory(prefix="pyccc_")

    def print_temprootdir():
        print("temprootdir: {}".format(temprootdir_td.name))

    books_dir = os.path.join(uc.PROJECT_ROOT, "books", time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()))
    # os.makedirs(books_dir, exist_ok=True)

    print_temprootdir()
    pyccc.pdf.sn2pdf.make("sn_tc_eb", temprootdir_td.name, uc.CONTEXT_BIN_PATH, uc.FONTS_DIR, books_dir)

    print_temprootdir()
    while input("input e and press enter to exit:").rstrip() != "e":
        pass


if __name__ == "__main__":
    main()
