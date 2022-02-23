import os
import typing
from string import Template

from pylatex import escape_latex as el

import pyccc.sn
import pyccc.note
from pyccc import utils, bookref
from pyccc.sn import BN


def to_latex(latex_io: typing.TextIO, translate_fun=None):
    nikaya = pyccc.sn.get()

    _head_t = open(os.path.join(utils.PROJECT_ROOT, "latex", "head2.tex"), "r").read()
    strdate = utils.lm_to_strdate(nikaya.last_modified)
    _head = Template(_head_t).substitute(date=strdate)
    latex_io.write(_head)

    book_local_notes = {}
    next_local_key = 1
    for pian in nikaya.pians:
        latex_io.write("\\bookmarksetup{open=true}\n")
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
                                twnr = e
                                (_notekey, subnotekey) = twnr.get_number()
                                if twnr.get_type() == utils.GLOBAL:
                                    notekey = _notekey
                                # twnr.get_type() == utils.LOCAL:
                                else:
                                    notekey = str(next_local_key)
                                    book_local_notes[notekey] = sutta.local_notes[_notekey]
                                    next_local_key += 1

                                latex_io.write("\\twnr" +
                                               "{" + el(twnr.get_text()) + "}" +
                                               "{" + note_label(twnr.type_, notekey, subnotekey) + "}")

                            elif isinstance(e, bookref.BookRef):
                                latex_io.write(e.to_latex(BN))

                            elif isinstance(e, utils.Href):
                                latex_io.write("\\href" +
                                               "{" + el(e.href) + "}" +
                                               "{" + el(e.text) + "}")
                            else:
                                raise Exception

                        latex_io.write("\n\n")
                    latex_io.write("\n\n")

    notes_to_latex(pyccc.utils.LOCAL, book_local_notes, latex_io, BN)
    notes_to_latex(pyccc.utils.GLOBAL, pyccc.note.get(), latex_io, BN)
    _tail = open(os.path.join(utils.PROJECT_ROOT, "latex", "tail.tex"), "r").read()
    latex_io.write(_tail)


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


def note_label(type_, notekey, subnotekey):
    return el(("" if type_ == pyccc.utils.GLOBAL else pyccc.pdf.LOCAL_NOTE_KEY_PREFIX) +
              str(notekey) + "." + str(subnotekey))
