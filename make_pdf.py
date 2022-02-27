#!/usr/bin/env python3
import os
import time
import subprocess
import pathlib

import pyccc.pdf.sn2pdf
import run_ccc
import pyccc.utils
import pyccc.note
from pyccc import sn

import tempfile


def main():
    run_ccc.make_sure_is_runing()
    domain = run_ccc.get_domain()

    pyccc.note.load_global(domain)
    pyccc.sn.load(domain)

    temprootdir_td = tempfile.TemporaryDirectory(prefix="pyccc_")

    def print_temprootdir():
        print("temprootdir: {}".format(temprootdir_td.name))

    books_dir = os.path.join(pyccc.utils.PROJECT_ROOT, "books", time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()))
    os.makedirs(books_dir, exist_ok=True)

    print_temprootdir()
    pyccc.pdf.sn2pdf.make("sn_tc_eb", temprootdir_td.name, books_dir)

    print_temprootdir()
    while input("input e and press enter to exit:").rstrip() != "e":
        pass


if __name__ == "__main__":
    main()
