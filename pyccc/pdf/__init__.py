from pylatex import escape_latex as el

import pyccc.utils

LOCAL_NOTE_KEY_PREFIX = "x"


def note_label(type_, notekey, subnotekey):
    return el(("" if type_ == pyccc.utils.GLOBAL else pyccc.pdf.LOCAL_NOTE_KEY_PREFIX) +
              str(notekey) + "." + str(subnotekey).replace("(", "").replace(")", ""))
