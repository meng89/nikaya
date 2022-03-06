from pylatex import escape_latex as el

import pyccc.utils
import pyccc.suttaref
import pyccc.trans

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


def join_to_tex(line: list, bn=None or str, t=None):
    t = t or pyccc.trans.empty_trans
    s = ""
    for x in line:
        if isinstance(x, str):
            s += el(x)
        elif isinstance(x, pyccc.suttaref.SuttaRef):
            s += x.to_tex(bn)
        elif isinstance(x, pyccc.utils.Href):
            s += x.to_tex(t)
        elif isinstance(x, pyccc.utils.TextWithNoteRef):
            s += x.to_tex(t)
        else:
            raise Exception(type(x))
    return s
