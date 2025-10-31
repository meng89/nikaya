import re
import config

import xl


P_SA = re.compile(r"(SA\.\d+)")
P_SN = re.compile(r"(SN\.\d+\.\d+)")
P_MA = re.compile(r"(MA\.\d+)")
P_MN = re.compile(r"(MN\.\d+)")
P_DA = re.compile(r"(DA\.\d+)")
P_DN = re.compile(r"(DN\.\d+)")
P_UD = re.compile(r"(Ud\.\d+)")
P_IT = re.compile(r"(It\.\d+)")
P_MI = re.compile(r"(Mi\.\d+)")
P_NI = re.compile(r"(Ni\.\d+)")
P_PS = re.compile(r"(Ps\.\d+)")
P_AA = re.compile(r"(AA\.\d+\.\d+)")
P_AN = re.compile(r"(AN\.\d+\.\d+)")

PATTERNS = [P_SA, P_SN, P_MA, P_MN, P_DA, P_DN, P_UD, P_IT, P_MI, P_NI, P_PS, P_AA, P_AN]


string = "text1 SN.1.1, SN.1.31, AN.2.1 text2"


def _make_cccurl(s, pattern):
    bn, num = _split_bn_num(s)
    if pattern in [P_SA, P_MA, P_MN, P_DA, P_DN, P_UD, P_IT, P_NI, P_AA]:
        return "{}/{}/dm.php?keyword={}".format(config.ABO_WEBSITE, bn, num)
    elif pattern in (P_SN, P_AN):
        return "{}/{}/{}.php?keyword={}".format(config.ABO_WEBSITE, bn, bn.lower(), num)
    elif pattern in (P_MI, P_NI, P_PS):
        return "{}/{}/{}{}.htm".format(config.ABO_WEBSITE, bn, bn, num)

    raise Exception("What?")


def _split_bn_num(s):
    m = re.match(r"([a-zA-Z]+)+\.(.+)", s)
    return m.group(1), m.group(2)


def _make_xml(s, pattern, bns):
    bn, num = _split_bn_num(s)
    if bn in bns:
        a = xl.Element("a", {"inbookref": s, "class": "suttaref_inbook"})
    else:
        a = xl.Element("a", {"href": _make_cccurl(s, pattern)})
    a.kids.append(s)
    return a


def make_suttanum_xml(s, bns):
    return _make_suttanum(s, PATTERNS, bns, _make_xml)


def make_suttanum_tex(s, bns):
    #todo
    raise Exception("TODO")


def _make_suttanum(s: str, patterns: list[re.Pattern], bns, func):
    # [some text SN.1.1, AN.2.1 some text] ->
    # [some text <a href="xxx.xhtml#SN.1.1">SN.1.1</a>, <a href="https://AN.2.1">AN.2.1</a> some text]
    if not patterns:
        return [s]

    new_patterns = patterns.copy()
    p = new_patterns.pop()
    pieces = re.split(p, s)

    new_pieces = []
    for index, piece in enumerate(pieces):
        if index % 2 == 0:
            new_pieces.extend(_make_suttanum(piece, new_patterns, bns, func))
        else:
            obj = func(piece, p, bns)
            new_pieces.append(obj)

    return new_pieces
