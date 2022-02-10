#!/usr/bin/env python3
import os
import subprocess
import pathlib

import run_ccc
import pyccc.note
from pyccc import sn

import tempfile


def build(work_dir, out_dir, tex_filename):
    os.makedirs(out_dir, exist_ok=True)
    compile_cmd = "lualatex -file-line-error -interaction=nonstopmode -synctex=1 -output-format=pdf" \
                  " -output-directory={} {}".format(out_dir, tex_filename)
    biber_cmd = "biber {}/{}".format(out_dir, pathlib.Path(tex_filename).stem)

    print("1. run {}".format(compile_cmd))
    p = subprocess.Popen(compile_cmd, cwd=work_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if p.returncode != 0:
        print(err.decode())

    print("2. run {}".format(biber_cmd))
    p = subprocess.Popen(biber_cmd, cwd=work_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if p.returncode != 0:
        print(err.decode())

    print("3. run {}".format(compile_cmd))
    p = subprocess.Popen(compile_cmd, cwd=work_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if p.returncode != 0:
        print(err.decode())


def main():
    run_ccc.make_sure_is_runing()
    domain = run_ccc.get_domain()

    pyccc.note.load_global(domain)
    pyccc.sn.load(domain)

    work_td = tempfile.TemporaryDirectory()
    out_td = tempfile.TemporaryDirectory()
    tex_filename = "sn_tc.tex"
    tex_file = open(work_td.name + "/" + tex_filename, "w")
    bib_filename = "sn_tc_notes.bib"
    bib_file = open(work_td.name + "/" + bib_filename, "w")
    sn.to_latex(tex_file, bib_file)
    tex_file.close()
    bib_file.close()

    def print_dir():
        print("work dir: {}".format(work_td.name))
        print("out  dir: {}".format(out_td.name))
    print_dir()
    build(work_dir=work_td.name, out_dir=out_td.name, tex_filename="sn_tc.tex")
    print_dir()
    while input("input e and press enter to exit:").rstrip() != "e":
        pass


if __name__ == "__main__":
    main()
