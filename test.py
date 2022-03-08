#!/usr/bin/env python3
_map = [
    ("\\", "{\\textbackslash}"),  # 必须第一个
    ("#", "{\\#}"),
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


def el(s: str):
    ns = ""
    x = False
    for char in s:
        for (a, b) in _map:
            if char == a:
                ns = ns + "{" + b + "}"
                x = True
                break
        if not x:
            ns += char
            x = False
    return ns


print(el("sfsf.html#2"))
