import opencc


def do_nothing(x):
    return x


_table = [
    ("「", "“"),
    ("」", "”"),
    ("『", "‘"),
    ("』", "’"),
]


def convert2sc(s):
    converter = opencc.OpenCC('tw2sp.json')
    return converter.convert(s)


def convert_all(s):
    new_sc_s = ""
    for c in convert2sc(s):
        new_sc_s += _convert_punctuation(c)
    return new_sc_s


def _convert_punctuation(c):
    for tp, sp in _table:
        if tp == c:
            return sp
    return c
