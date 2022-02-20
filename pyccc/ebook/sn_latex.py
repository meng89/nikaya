import os
import typing
from string import Template

from pylatex import escape_latex as el

import pyccc.sn
from pyccc import utils, bookref
from pyccc.sn import _nikaya, LOCAL_NOTE_KEY_PREFIX, BN


def to_latex(latex_io: typing.TextIO, translate_fun=None):

    _head_t = open(os.path.join(utils.PROJECT_ROOT, "latex", "head2.tex"), "r").read()
    strdate = utils.lm_to_strdate(_nikaya.last_modified)
    _head = Template(_head_t).substitute(date=strdate)
    latex_io.write(_head)

    book_local_notes = {}
    next_local_key = 1
    for pian in _nikaya.pians:
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
                    latex_io.write("\\labal{subsec:" + pyccc.sn.BN + "." + xiangying.serial + "." +
                                   sutta.serial_start + "}\n")
                    for body_listline in sutta.body_listline_list:
                        for e in body_listline:
                            if isinstance(e, str):
                                latex_io.write(el(e))
                            elif isinstance(e, utils.TextWithNoteRef):
                                twnr = e
                                if twnr.get_type() == utils.GLOBAL:
                                    (notenum, subnotenum) = twnr.get_number()
                                    latex_dest = "note.{}.{}".format(notenum, subnotenum)
                                else:
                                    assert twnr.get_type() == utils.LOCAL
                                    (notenum, subnotenum) = twnr.get_number()
                                    note_key = LOCAL_NOTE_KEY_PREFIX + str(next_local_key)
                                    latex_dest = "note.{}.{}".format(note_key, subnotenum)
                                    book_local_notes[note_key] = sutta.local_notes[notenum]
                                    next_local_key += 1

                                latex_io.write("\\twnr{{{}}}{{{}}}".format(el(twnr.get_text()), latex_dest))

                            elif isinstance(e, bookref.BookRef):
                                latex_io.write(e.to_latex(BN))

                            elif isinstance(e, utils.Href):
                                latex_io.write("\\href{{{}}}{{{}}}".format(el(e.href), el(e.text)))
                            else:
                                raise Exception("What?")
                        latex_io.write("\n\n")

    _tail = open(os.path.join(utils.PROJECT_ROOT, "latex", "tail.tex"), "r").read()
    latex_io.write(_tail)


def notes_to_latex(notes, latex_io: typing.TextIO, bookname, trans=None):
    t = trans or utils.no_translate
    for notekey, note in notes.items():
        latex_io.write("\\begin{EnvNote}\n")
        for subnotesum, subnote in note.item():
            latex_io.write("  \\subnote{{{}}}{{{}}}\n".format(subnote.head,
                                                              bookref.join_to_latex(subnote.body, bookname)))

        latex_io.write("\\end{EvnNote}\n")



