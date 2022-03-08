import os
import typing
from string import Template
import shutil
import subprocess

import pyccc
import pyccc.sn
import pyccc.note
from pyccc import utils
from pyccc.pdf import globalnote_label, localnote_label

import user_config


suttas_filename = "suttas.tex"
localnotes_filename = "localnotes.tex"
globalnotes_filename = "globalnotes.tex"
fonttex_filename = "type-imp-myfonts.tex"
creator_note_filename = "creator_note.tex"
read_note_filename = "read_note.tex"


def tex_dir():
    return os.path.join(utils.PROJECT_ROOT, "tex")


def write_fontstex(work_dir):
    fonttex = open(os.path.join(tex_dir(), fonttex_filename), "r").read()
    new_fonttex = fonttex.replace("file:../fonts", "file:" + os.path.expanduser(user_config.FONTS_DIR))
    with open(os.path.join(work_dir, fonttex_filename), "w") as new_fonttex_file:
        new_fonttex_file.write(new_fonttex)


def write_main(main_file: typing.TextIO, bns, t):
    nikaya = pyccc.sn.get()
    homage = pyccc.pdf.join_to_tex(nikaya.homage_listline, bns, t)
    _head_t = open(os.path.join(utils.PROJECT_ROOT, "tex", "sn.tex"), "r").read()
    strdate = utils.lm_to_strdate(nikaya.last_modified)
    _head = Template(_head_t).substitute(date=strdate, suttas=suttas_filename,
                                         homage=homage,
                                         localnotes=localnotes_filename, globalnotes=globalnotes_filename)
    main_file.write(_head)


def write_suttas(latex_io: typing.TextIO, bns, t):
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
                                   "{" + pin.suttas[0].begin + "}" +
                                   "{" + pin.suttas[-1].end + "}\n")

                for sutta in pin.suttas:
                    latex_io.write("\\sutta" +
                                   "{" + sutta.begin + "}" +
                                   "{" + sutta.end + "}" +
                                   "{" + sutta.title + "}\n")

                    for body_listline in sutta.body_lines:
                        latex_io.write(pyccc.pdf.join_to_tex(body_listline, bns, t))

                        latex_io.write("\n\n")
                    latex_io.write("\n\n")
                latex_io.write("\n\n")
            latex_io.write("\\page\n\n")


def write_localnotes(latex_io: typing.TextIO, notes, bns, t):
    for subnote in notes:
        latex_io.write("\\startNote\n")
        latex_io.write("" +
                       "\\subnoteref{" + localnote_label(notes.index(subnote)) + "}" +
                       pyccc.pdf.join_to_tex(subnote, bns, t) + "\n")
        latex_io.write("\\stopNote\n\n")


def write_globalnotes(latex_io: typing.TextIO, bns, t):
    notes = pyccc.note.get()
    for notekey, note in notes.items():
        latex_io.write("\\startNote\n")
        for subnotekey, line in note.items():
            latex_io.write("" +
                           "\\subnoteref{" + globalnote_label(notekey, subnotekey) + "}" +
                           "\\subnotekey{" + (subnotekey or "\\null") + "}" +
                           pyccc.pdf.join_to_tex(line, bns, t) + "\n\n")
        latex_io.write("\\stopNote\n\n")


def build(sources_dir, out_dir, tex_filename):
    my_env = os.environ.copy()
    my_env["PATH"] = os.path.expanduser(user_config.CONTEXT_BIN_PATH) + ":" + my_env["PATH"]
    compile_cmd = "context --path={} {}/{}".format(sources_dir, sources_dir, tex_filename)

    stdout_file = open(os.path.join(out_dir, "cmd_stdout"), "w")
    stderr_file = open(os.path.join(out_dir, "cmd_stderr"), "w")

    def _run():
        print("running command:", compile_cmd, end=" ", flush=True)
        p = subprocess.Popen(compile_cmd, cwd=out_dir, shell=True, env=my_env,
                             stdout=stdout_file, stderr=stderr_file)
        p.communicate()
        if p.returncode != 0:
            input("command run wrong")
        print("done!")
    _run()
    stdout_file.close()
    stderr_file.close()


def make_keys():
    pass


def make(key, temprootdir, bookdir):
    main_filename = "sn.tex"
    sn_tc_eb = "sn_tc_eb"
    bns = [pyccc.sn.BN]
    t = utils.no_translate

    if key == sn_tc_eb:
        nikaya = pyccc.sn.get()
        sources_dir = os.path.join(temprootdir, sn_tc_eb, "work")
        os.makedirs(sources_dir, exist_ok=True)
        out_dir = os.path.join(temprootdir, sn_tc_eb, "out")
        os.makedirs(out_dir, exist_ok=True)

        write_fontstex(sources_dir)

        with open(sources_dir + "/" + main_filename, "w") as f:
            write_main(f, bns, t)

        with open(sources_dir + "/" + suttas_filename, "w") as f:
            write_suttas(f, bns, t)

        with open(sources_dir + "/" + localnotes_filename, "w") as f:
            write_localnotes(f, nikaya.local_notes, bns, t)

        with open(sources_dir + "/" + globalnotes_filename, "w") as f:
            write_globalnotes(f, bns, t)

        shutil.copy(os.path.join(tex_dir(), read_note_filename), sources_dir)
        shutil.copy(os.path.join(tex_dir(), creator_note_filename), sources_dir)

        build(sources_dir=sources_dir, out_dir=out_dir, tex_filename=main_filename)
        # shutil.move(os.path.join(out_dir, "sn.pdf"), os.path.join(bookdir, "sn_tc_eb.pdf"))