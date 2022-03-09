import opencc


def _do_nothing(x):
    return x


do_nothing = _do_nothing


_table = [
    ("「", "“"),
    ("」", "”"),
    ("『", "‘"),
    ("』", "’"),
]


def convert(s):
    converter = opencc.OpenCC('tw2sp.json')
    _sc_s = converter.convert(s)
    new_sc_s = ""
    for c in _sc_s:
        new_sc_s += _convert_punctuation(c)
    return new_sc_s


def _convert_punctuation(c):
    for tp, sp in _table:
        if tp == c:
            return sp
    return c

