import os
import typing
from string import Template
import tempfile
import subprocess

from pylatex import escape_latex as el

import pyccc.sn
import pyccc.note
from pyccc import utils, bookref
from pyccc.pdf import note_label
from pyccc.sn import BN


def write_main(main_file: typing.TextIO, t):
    nikaya = pyccc.sn.get()
    _head_t = open(os.path.join(utils.PROJECT_ROOT, "latex", "sn.tex"), "r").read()
    strdate = utils.lm_to_strdate(nikaya.last_modified)
    _head = Template(_head_t).substitute(date=strdate)
    main_file.write(_head)


def write_suttas(latex_io: typing.TextIO, t):
    nikaya = pyccc.sn.get()

    for pian in nikaya.pians:
        latex_io.write("\\bookmarksetup{open=true}\n")
        #latex_io.write("\\pian" +
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
                                                                      pin.suttas[0].serial_start,
                                                                      pin.suttas[-1].serial_end))

                for sutta in pin.suttas:
                    latex_io.write("\\subsection{" + sutta.serial + ". " + sutta.title + "}\n")
                    latex_io.write("\\label{subsec:" + pyccc.sn.BN + "." + xiangying.serial + "." +
                                   sutta.serial_start + "}\n")

                    for body_listline in sutta.body_listline_list:
                        for e in body_listline:
                            if isinstance(e, str):
                                latex_io.write(el(e))
                            elif isinstance(e, utils.TextWithNoteRef):
                                latex_io.write(e.to_latex(t))

                            elif isinstance(e, bookref.BookRef):
                                latex_io.write(e.to_latex(BN))

                            elif isinstance(e, utils.Href):
                                latex_io.write(e.to_latex())
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
                           "{" + bookref.join_to_latex(subnote.body, bookname) + "}\n")

        latex_io.write("\\end{EnvNote}\n")


def build(work_dir, out_dir, tex_filename):
    os.makedirs(out_dir, exist_ok=True)
    compile_cmd = "lualatex -file-line-error -interaction=nonstopmode -synctex=1 -output-format=pdf" \
                  " -output-directory={} {}".format(out_dir, tex_filename)

    def run():
        print("run {}  ...".format(compile_cmd), end="")
        p = subprocess.Popen(compile_cmd, cwd=work_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode != 0:
            print(err.decode())
        print("done!")
    run()
    run()


def make_keys():
    pass


def make(key):
    main_filename = "sn.tex"
    suttas_filename = "suttas.tex"
    notes_filename = "notes.tex"

    if key == "sn_tc_eb":
        nikaya = pyccc.sn.get()
        work_td = tempfile.TemporaryDirectory()
        out_td = tempfile.TemporaryDirectory()
        build(work_dir=work_td.name, out_dir=out_td.name, tex_filename="sn_tc.tex")

        with open(work_td.name + "/" + main_filename, "w") as main_file:
            write_main(main_file, utils.no_translate)

        with open(work_td.name + "/" + suttas_filename, "w") as suttas_file:
            write_suttas(suttas_file, utils.no_translate)

        with open(work_td.name + "/" + notes_filename, "w") as notes_file:
            write_notes(notes_file, nikaya.book_notes, utils.no_translate)

