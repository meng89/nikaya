import os
import typing
from string import Template
import shutil
import subprocess

from pylatex import escape_latex as el

import pyccc.sn
import pyccc.note
from pyccc import utils, bookref
from pyccc.pdf import note_label
from pyccc.sn import BN

import user_config

suttas_filename = "suttas.tex"
notes_filename = "notes.tex"


def write_main(main_file: typing.TextIO, t):
    nikaya = pyccc.sn.get()
    _head_t = open(os.path.join(utils.PROJECT_ROOT, "latex", "sn.tex"), "r").read()
    strdate = utils.lm_to_strdate(nikaya.last_modified)
    _head = Template(_head_t).substitute(date=strdate, suttas=suttas_filename, notes=notes_filename)
    main_file.write(_head)


def write_suttas(latex_io: typing.TextIO, t):
    nikaya = pyccc.sn.get()

    for pian in nikaya.pians:
        latex_io.write("\\bookmarksetup{open=true}\n")
        # latex_io.write("\\pian" +
        #               "{" + pian.title + "}" +
        #               "{" + pian.xiangyings[0].serial + "}" +
        #               "{" + pian.xiangyings[-1].serial + "}")

        latex_io.write("\\part{{{} ({}-{})}}\n".format(pian.title,
                                                       pian.xiangyings[0].serial,
                                                       pian.xiangyings[-1].serial))

        for xiangying in pian.xiangyings:
            latex_io.write("\\bookmarksetup{open=false}\n")
            latex_io.write("\\chapter{{{}. {}}}\n".format(xiangying.serial, xiangying.title))

            for pin in xiangying.pins:
                if pin.title is not None:
                    latex_io.write("\\section{{{} ({}-{})}}\n".format(pin.title,
                                                                      pin.suttas[0].begin,
                                                                      pin.suttas[-1].end))

                for sutta in pin.suttas:
                    latex_io.write("\\subsection{" + sutta.serial + ". " + sutta.title + "}\n")
                    latex_io.write("\\label{subsec:" + pyccc.sn.BN + "." + xiangying.serial + "." +
                                   sutta.begin + "}\n")

                    for body_listline in sutta.body_listline_list:
                        for e in body_listline:
                            if isinstance(e, str):
                                latex_io.write(el(e))
                            elif isinstance(e, utils.TextWithNoteRef):
                                latex_io.write(e.to_tex(t))

                            elif isinstance(e, bookref.SuttaRef):
                                latex_io.write(e.to_tex(BN))

                            elif isinstance(e, utils.Href):
                                latex_io.write(e.to_tex())
                            else:
                                raise Exception

                        latex_io.write("\n\n")
                    latex_io.write("\n\n")


def write_notes(notes_file, book_notes, t):
    notes_to_latex(pyccc.utils.LOCAL, book_notes, notes_file, BN)
    notes_to_latex(pyccc.utils.GLOBAL, pyccc.note.get(), notes_file, BN)


def notes_to_latex(type_, notes, latex_io: typing.TextIO, bookname, trans=None):
    t = trans or utils.no_translate
    for notekey, note in notes.items():
        latex_io.write("\\begin{EnvNote}\n")
        for subnotekey, subnote in note.items():
            latex_io.write("    \\subnote" +
                           "{" + note_label(type_, notekey, subnotekey) + "}" +
                           "{" + (subnotekey or "\\null") + "}" +
                           "{" + (subnote.head or "\\null") + "}" +
                           "{" + bookref.join_to_tex(subnote.body, bookname) + "}\n")

        latex_io.write("\\end{EnvNote}\n")


def build(work_dir, out_dir, tex_filename):
    compile_cmd = "lualatex -file-line-error -interaction=nonstopmode -synctex=1 -output-format=pdf" \
                  " -output-directory={} {}".format(out_dir, tex_filename)

    def _run():
        print("run command:", compile_cmd, end="", flush=True)
        p = subprocess.Popen(compile_cmd, cwd=work_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode != 0:
            print("error:", err.decode())
        print("done!")

    _run()
    _run()


def make_keys():
    pass


def make(key, temprootdir, bookdir):
    main_filename = "sn.tex"
    sn_tc_eb = "sn_tc_eb"

    if key == sn_tc_eb:
        nikaya = pyccc.sn.get()
        work_dir = os.path.join(temprootdir, sn_tc_eb, "work")
        os.makedirs(work_dir, exist_ok=True)
        out_dir = os.path.join(temprootdir, sn_tc_eb, "out")
        os.makedirs(out_dir, exist_ok=True)

        with open(work_dir + "/" + main_filename, "w") as main_file:
            write_main(main_file, utils.no_translate)

        with open(work_dir + "/" + suttas_filename, "w") as suttas_file:
            write_suttas(suttas_file, utils.no_translate)

        with open(work_dir + "/" + notes_filename, "w") as notes_file:
            write_notes(notes_file, nikaya.local_notes, utils.no_translate)

        build(work_dir=work_dir, out_dir=out_dir, tex_filename=main_filename)
        shutil.move(os.path.join(out_dir, "sn.pdf"), os.path.join(bookdir, "sn_tc_eb.pdf"))
