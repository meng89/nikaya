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

fonttex_filename = "type-imp-myfonts.tex"


def write_fonttex(work_dir):
    fonttex = open(os.path.join(utils.PROJECT_ROOT, "tex", fonttex_filename), "r").read()
    new_fonttex = fonttex.replace("file:../fonts", "file:" + os.path.expanduser(user_config.FONTS_DIR))
    with open(os.path.join(work_dir, fonttex_filename), "w") as new_fonttex_file:
        new_fonttex_file.write(new_fonttex)


def write_main(main_file: typing.TextIO, t):
    nikaya = pyccc.sn.get()
    _head_t = open(os.path.join(utils.PROJECT_ROOT, "tex", "sn.tex"), "r").read()
    strdate = utils.lm_to_strdate(nikaya.last_modified)
    _head = Template(_head_t).substitute(date=strdate, suttas=suttas_filename, notes=notes_filename)
    main_file.write(_head)


def write_suttas(latex_io: typing.TextIO, t):
    nikaya = pyccc.sn.get()

    for pian in nikaya.pians:
        latex_io.write("\\pian" +
                       "{" + pian.title + "}" +
                       "{" + pian.xiangyings[0].serial + "}" +
                       "{" + pian.xiangyings[-1].serial + "}\n")

        for xiangying in pian.xiangyings:
            latex_io.write("\\xiangying" +
                           "{" + xiangying.serial + "}" +
                           "{" + xiangying.title + "}\n")

            for pin in xiangying.pins:
                if pin.title is not None:
                    latex_io.write("\\pin" +
                                   "{" + pin.title + "}" +
                                   "{" + pin.suttas[0].serial_start + "}" +
                                   "{" + pin.suttas[-1].serial_end + "}\n")

                for sutta in pin.suttas:
                    latex_io.write("\\sutta" +
                                   "{" + sutta.serial_start + "}" +
                                   "{" + sutta.serial_end + "}" +
                                   "{" + sutta.title + "}\n")

                    latex_io.write("\n\nSN.\\somenamedheadnumber{chapter}{current}.x\n\n")

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
                latex_io.write("\n\n")
            latex_io.write("\\page\n\n")


def write_notes(notes_file, book_notes, t):
    notes_to_latex(pyccc.utils.LOCAL, book_notes, notes_file, BN)
    notes_to_latex(pyccc.utils.GLOBAL, pyccc.note.get(), notes_file, BN)


def notes_to_latex(type_, notes, latex_io: typing.TextIO, bookname, trans=None):
    t = trans or utils.no_translate
    for notekey, note in notes.items():
        latex_io.write("\\startNote\n")
        for subnotekey, subnote in note.items():
            latex_io.write("    \\subnote" +
                           "{" + note_label(type_, notekey, subnotekey) + "}" +
                           "{" + (subnotekey or "\\null") + "}" +
                           "{" + (subnote.head or "\\null") + "}" +
                           "{" + bookref.join_to_latex(subnote.body, bookname) + "}\n\n")

        latex_io.write("\\stopNote\n\n")


def build(work_dir, out_dir, tex_filename):
    my_env = os.environ.copy()
    my_env["PATH"] = os.path.expanduser(user_config.CONTEXT_BIN_PATH) + ":" + my_env["PATH"]
    compile_cmd = "context --path={} {}/{}".format(work_dir, work_dir, tex_filename)

    stdout_file = open(os.path.join(out_dir, "cmd_stdout"), "w")
    stderr_file = open(os.path.join(out_dir, "cmd_stderr"), "w")

    def _run():
        print("running command:", compile_cmd, end=" ", flush=True)
        p = subprocess.Popen(compile_cmd, cwd=out_dir, shell=True, env=my_env,
                             stdout=stdout_file, stderr=stderr_file)
        out, err = p.communicate()
        if p.returncode != 0:
            print("error:", err.decode())
        print("done!")
    _run()
    stdout_file.close()
    stderr_file.close()


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

        write_fonttex(work_dir)

        with open(work_dir + "/" + main_filename, "w") as main_file:
            write_main(main_file, utils.no_translate)

        with open(work_dir + "/" + suttas_filename, "w") as suttas_file:
            write_suttas(suttas_file, utils.no_translate)

        with open(work_dir + "/" + notes_filename, "w") as notes_file:
            write_notes(notes_file, nikaya.book_notes, utils.no_translate)

        build(work_dir=work_dir, out_dir=out_dir, tex_filename=main_filename)
        #shutil.move(os.path.join(out_dir, "sn.pdf"), os.path.join(bookdir, "sn_tc_eb.pdf"))
