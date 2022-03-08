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


def el(s):
    ns = ""
    for c in s:
        ns += _el_char(c)
    return ns


def _el_char(c):
    for (a, b) in _map:
        if c == a:
            return "{" + b + "}"
    return c


print(el("sfs\\f.ht{ml#2"))
