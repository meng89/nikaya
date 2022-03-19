import xml.etree.ElementTree as ET

from pylatex import escape_latex as el

import pyccc
from pyccc import atom, atom_suttaref, page_parsing, parse_note


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


def _new_line(line):
    new_line = []
    for x in line:
        if isinstance(x, str):
            new_line.extend(atom_suttaref.parse(x))
        else:
            new_line.append(x)

    return new_line


def join_to_tex(line: list, bns: list[str], c):
    new_line = _new_line(line)
    s = ""
    for x in new_line:
        if isinstance(x, str):
            s += c(x)
        elif isinstance(x, pyccc.BaseElement):
            s += x.to_tex(bns=bns, c=c)
        else:
            raise Exception((type(x), x))
    return s


def join_to_xml(line: list, bns, c):
    new_line = _new_line(line)
    elements = []
    for x in line:
        if isinstance(x, str):
            elements.append(x)
        elif isinstance(x, pyccc.BaseElement):
            elements.append(x.to_xml(bns=bns, c=c))


def join_to_text(line: list, c=None):
    c = c or page_parsing.no_translate
    s = ""
    for x in line:
        if isinstance(x, str):
            s += x
        elif isinstance(x, pyccc.BaseElement):
            s += x.get_text()
        else:
            raise Exception(type(x))
    return c(s)


TC = "tc"
SC = "sc"


