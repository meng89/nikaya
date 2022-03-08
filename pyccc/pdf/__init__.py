from typing import Callable

from pylatex import escape_latex as el

import pyccc.utils
import pyccc.suttaref
import pyccc.trans
import pyccc.note

LOCAL_NOTE_KEY_PREFIX = "x"


def note_label(type_, key):
    if type_ == pyccc.utils.GLOBAL:
        return globalnote_label(key[0], key[1])
    else:
        return localnote_label(key)


def globalnote_label(notekey, subnotekey):
    return str(notekey) + "." + str(subnotekey).replace("(", "").replace(")", "")


def localnote_label(key):
    return LOCAL_NOTE_KEY_PREFIX + str(key)


def join_to_tex(line: list, bns: list[str], t=None):
    s = ""
    for x in line:
        if isinstance(x, str):
            s += el(t(x))
        elif isinstance(x, pyccc.suttaref.SuttaRef):
            s += x.to_tex(bns=bns)
        elif isinstance(x, pyccc.utils.Href):
            s += x.to_tex(t)
        elif isinstance(x, pyccc.utils.TextWithNoteRef):
            s += x.to_tex(t)
        elif isinstance(x, pyccc.note.NoteKeywordDefault):
            s += x.to_tex(bns=bns, t=t)
        else:
            raise Exception(type(x))
    return s


def join_to_text(line: list, t=None):
    t = t or pyccc.utils.no_translate
    s = ""
    for x in line:
        if isinstance(x, str):
            s += x
        elif isinstance(x, pyccc.suttaref.SuttaRef):
            s += x.get_text()
        elif isinstance(x, pyccc.utils.Href):
            s += x.get_text()
        elif isinstance(x, pyccc.utils.TextWithNoteRef):
            s += x.get_text()
        elif isinstance(x, pyccc.note.NoteKeywordDefault):
            s += x.get_text()
        else:
            raise Exception(type(x))
    return t(s)
