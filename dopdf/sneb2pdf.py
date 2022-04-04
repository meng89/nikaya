import datetime
import os
import typing
from string import Template
import shutil
import subprocess
import re


import pyccc
from pyccc import atom_note, atom_suttaref, page_parsing, sn, book_public
import dopdf

main_filename = "sn.tex"
suttas_filename = "suttas.tex"
localnotes_filename = "localnotes.tex"
globalnotes_filename = "globalnotes.tex"
fonttex_filename = "type-imp-myfonts.tex"
creator_note_filename = "creator_note.tex"
read_note_filename = "read_note.tex"


def findfile(start, name):
    for relpath, dirs, files in os.walk(start):
        if name in files:
            full_path = os.path.join(start, relpath, name)
            return os.path.normpath(os.path.abspath(full_path))


def write_fontstex(work_dir, fonts_dir):
    fonttex = open(os.path.join(dopdf.TEX_DIR, fonttex_filename), "r", encoding="utf-8").read()

    for fontpath in re.findall("file:(.*(?:ttf|otf))", fonttex):
        fontabspath = findfile(fonts_dir, os.path.basename(fontpath))
        fonttex = fonttex.replace(fontpath, fontabspath.replace("\\", "/"))

    with open(os.path.join(work_dir, fonttex_filename), "w", encoding="utf-8") as new_fonttex_file:
        new_fonttex_file.write(fonttex)


def write_main(main_file: typing.TextIO, bns, c):
    nikaya = sn.get()
    homage = dopdf.join_to_tex(nikaya.homage_listline, bns, c)
    _head_t = open(os.path.join(dopdf.TEX_DIR, "sn.tex"), "r", encoding='utf-8').read()
    strdate = page_parsing.lm_to_strdate(nikaya.last_modified)
    _head = Template(_head_t).substitute(date=strdate, suttas=suttas_filename,
                                         homage=homage,
                                         localnotes=localnotes_filename, globalnotes=globalnotes_filename)
    main_file.write(_head)


def write_suttas(latex_io: typing.TextIO, bns, c, test=False):
    nikaya = sn.get()

    for pian in nikaya.pians:
        latex_io.write("\\pian" +
                       "{" + c(pian.title) + "}" +
                       "{" + pian.xiangyings[0].serial + "}" +
                       "{" + pian.xiangyings[-1].serial + "}\n")

        for xiangying in pian.xiangyings:
            latex_io.write("\\xiangying" +
                           "{" + xiangying.serial + "}" +
                           "{" + c(xiangying.title) + "}\n")

            for pin in xiangying.pins:
                if pin.title is not None:
                    latex_io.write("\\pin" +
                                   "{" + c(pin.title) + "}" +
                                   "{" + pin.suttas[0].begin + "}" +
                                   "{" + pin.suttas[-1].end + "}\n")

                for sutta in pin.suttas:
                    def _cccurl():
                        _SR = atom_suttaref.SuttaRef("SN" + "." + xiangying.serial + "." + sutta.begin)
                        return _SR.get_cccurl()

                    latex_io.write("\\sutta" +
                                   "{" + sutta.begin + "}" +
                                   "{" + sutta.end + "}" +
                                   "{" + c(sutta.title) + "}" +
                                   "{" + _cccurl() + "}\n")

                    for body_listline in sutta.body_lines:
                        latex_io.write(dopdf.join_to_tex(body_listline, bns, c))

                        latex_io.write("\n\n")
                    latex_io.write("\n\n")
                    if test:
                        break
                latex_io.write("\n\n")
                if test:
                    break
            latex_io.write("\\page\n\n")
            if test:
                break


def write_localnotes(latex_io: typing.TextIO, notes, bns, c, test):
    count = 0
    for subnote in notes:
        latex_io.write("\\startitemgroup[noteitems]\n")
        latex_io.write("\\item" +
                       "\\subnoteref{" + atom_note.localnote_to_texlabel(notes.index(subnote)) + "}" +
                       dopdf.join_to_tex(subnote, bns, c) + "\n")
        latex_io.write("\\stopitemgroup\n\n")
        count += 1
        if test and count == 50:
            break


def write_globalnotes(latex_io: typing.TextIO, bns, c, test):
    count = 0
    notes = atom_note.get()
    for notekey, note in notes.items():
        latex_io.write("\\startitemgroup[noteitems]\n")
        for index in range(len(note)):
            latex_io.write("\\item" +
                           "\\subnoteref{" + atom_note.globalnote_to_texlabel(notekey, index) + "}" +
                           dopdf.join_to_tex(note[index], bns, c) + "\n")
        latex_io.write("\\stopitemgroup\n\n")
        count += 1
        if test and count == 50:
            break


def build(sources_dir, out_dir, tex_filename, context_bin_path, lang):
    my_env = os.environ.copy()
    if os.name == "posix":
        my_env["PATH"] = os.path.expanduser(context_bin_path) + ":" + my_env["PATH"]
    elif os.name == "nt":
        my_env["PATH"] = os.path.expanduser(context_bin_path) + ";" + my_env["PATH"]

    compile_cmd = "context --path={} {}/{} --mode={}".format(sources_dir, sources_dir, tex_filename, lang)

    stdout_file = open(os.path.join(out_dir, "cmd_stdout"), "w", encoding="utf-8")
    stderr_file = open(os.path.join(out_dir, "cmd_stderr"), "w", encoding="utf-8")

    def _run():
        print("运行:", compile_cmd, end=" ", flush=True)
        p = subprocess.Popen(compile_cmd, cwd=out_dir, shell=True, env=my_env,
                             stdout=stdout_file, stderr=stderr_file)
        p.communicate()
        if p.returncode != 0:
            input("出错！")
        print("完成！")
    _run()
    stdout_file.close()
    stderr_file.close()


def make_keys():
    pass


def make(xc, temprootdir, context_bin_path, fonts_dir, bookdir, test=False):
    bns = [sn.BN]

    mytemprootdir = os.path.join(temprootdir, "sn_pdf_" + xc.enlang)

    if True:
        nikaya = sn.get()
        sources_dir = os.path.join(mytemprootdir, "work")
        os.makedirs(sources_dir, exist_ok=True)
        out_dir = os.path.join(mytemprootdir, "out")
        os.makedirs(out_dir, exist_ok=True)

        write_fontstex(sources_dir, fonts_dir)

        with open(sources_dir + "/" + main_filename, "w", encoding="utf-8") as f:
            write_main(f, bns, xc.c)

        with open(sources_dir + "/" + suttas_filename, "w", encoding="utf-8") as f:
            write_suttas(f, bns, xc.c, test)

        with open(sources_dir + "/" + localnotes_filename, "w", encoding="utf-8") as f:
            write_localnotes(f, nikaya.local_notes, bns, xc.c, test)

        with open(sources_dir + "/" + globalnotes_filename, "w", encoding="utf-8") as f:
            write_globalnotes(f, bns, xc.c, test)

        shutil.copy(os.path.join(dopdf.TEX_DIR, read_note_filename), sources_dir)
        shutil.copy(os.path.join(dopdf.TEX_DIR, creator_note_filename), sources_dir)

        build(sources_dir=sources_dir, out_dir=out_dir, tex_filename=main_filename,
              context_bin_path=context_bin_path, lang=xc.enlang)

        shutil.copy(os.path.join(out_dir, "sn.pdf"),
                    os.path.join(bookdir, "{}_{}_莊{}_{}.pdf".format(xc.c("相應部"),
                                                                    xc.zhlang,
                                                                    nikaya.last_modified.strftime("%y%m"),
                                                                    datetime.datetime.now().strftime("%Y%m%d"))))
