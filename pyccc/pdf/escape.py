_map = [
    ("\\", "\\textbackslash"),
    ("#", "\\#"),
    ("$", "\\textdollar"),
    ("%", "\\percent"),
    ("&", "\\&"),
    ("^", "\\textcircumflex"),
    ("_", "\\textunderscore"),
    ("{", "\\textbraceleft"),
    ("|", "\\textbar"),
    ("}", "\\textbraceright"),
    ("~", "\\textasciitilde"),
]

_url_map = [
    ("%", "\\letterpercent"),
    ("#", "\\letterhash"),
    ("\\", "\\letterescape"),
]


def el(s, table=None):
    table = _url_map or table
    ns = ""
    for c in s:
        ns += _el_char(c, table)
    return ns


def el_url(s):
    return el(s, _url_map)


def _el_char(c, table):
    for (a, b) in table:
        if c == a:
            return "{" + b + "}"
    return c


print(el("sfs\\f.ht{ml#2"))
