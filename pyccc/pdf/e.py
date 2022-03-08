_map = [
    ("\\", "\\textbackslash"),  # 必须第一个
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


def el(s: str):
    ns = None
    for a, b in _map:
        ns = s.replace(a, b)
    return ns
