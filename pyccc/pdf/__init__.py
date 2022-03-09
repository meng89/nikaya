from pylatex import escape_latex as el

from pyccc import atom, atom_suttaref, atom_note, page_parsing

_url_table = [
    ("%", "\\letterpercent"),
    ("#", "\\letterhash"),
    ("\\", "\\letterescape"),
]


def el_url(s):
    return _el(s, _url_table)


def _el(s, table=None):
    table = _url_table or table
    ns = ""
    for c in s:
        ns += _el_char(c, table)
    return ns


def _el_char(c, table):
    for (a, b) in table:
        if c == a:
            return b + " "
    return c


def join_to_tex(line: list, bns: list[str], c=None):
    s = ""
    for x in line:
        if isinstance(x, str):
            s += el(c(x))
        elif isinstance(x, atom_suttaref.SuttaRef):
            s += x.to_tex(bns=bns)
        elif isinstance(x, atom.Href):
            s += x.to_tex(c)
        elif isinstance(x, atom.TextWithNoteRef):
            s += x.to_tex(c)
        elif isinstance(x, atom_note.NoteKeywordDefault):
            s += x.to_tex(bns=bns, t=c)
        else:
            raise Exception(type(x))
    return s


def join_to_text(line: list, c=None):
    c = c or page_parsing.no_translate
    s = ""
    for x in line:
        if isinstance(x, str):
            s += x
        elif isinstance(x, atom_suttaref.SuttaRef):
            s += x.get_text()
        elif isinstance(x, atom.Href):
            s += x.get_text()
        elif isinstance(x, atom.TextWithNoteRef):
            s += x.get_text()
        elif isinstance(x, atom_note.NoteKeywordDefault):
            s += x.get_text()
        else:
            raise Exception(type(x))
    return c(s)


