import re
import xml.etree.ElementTree as ET

import pyccc
from pyccc import atom, lang_convert

P_SA = r"(SA)\.(\d+)"
P_SN = r"(SN)\.(\d+\.\d+)"
P_MA = r"(MA)\.(\d+)"
P_MN = r"(MN)\.(\d+)"
P_DA = r"(DA)\.(\d+)"
P_DN = r"(DN)\.(\d+)"
P_UD = r"(Ud)\.(\d+)"
P_IT = r"(It)\.(\d+)"
P_MI = r"(Mi)\.(\d+)"
P_NI = r"(Ni)\.(\d+)"
P_PS = r"(Ps)\.(\d+)"
P_AA = r"(AA)\.(\d+\.\d+)"
P_AN = r"(AN)\.(\d+\.\d+)"

PATTERNS = [P_SA, P_SN, P_MA, P_MN, P_DA, P_DN, P_UD, P_IT, P_MI, P_NI, P_PS, P_AA, P_AN]


def make_suttaname_href_link(suttaname):
    return suttaname2htmlpath(suttaname) + "#" + suttaname


def suttaname2htmlpath(suttaname):
    p, xn, num = split_suttaname(suttaname)
    if p == P_SN:
        xiangying_num, _sutta_num = num.split(".")
        return "../sn/sn.{}.xhtml".format(xiangying_num)
    else:
        # todo other
        raise Exception


def split_suttaname(text):
    m = None
    for p in PATTERNS:
        m = re.match("^{}$".format(p), text)
        if m:
            return p, m.group(1), m.group(2)
    assert m


class SuttaRef(pyccc.BaseElement):
    def __init__(self, text):
        self.text = text
        self._pattern, self._bn, self._sec_num = split_suttaname(text)

    def get_text(self):
        return self._bn + "." + self._sec_num

    def get_cccurl(self):
        if self._pattern in [P_SA, P_MA, P_MN, P_DA, P_DN, P_UD, P_IT, P_NI, P_AA]:
            return "{}/{}/dm.php?keyword={}".format(pyccc.CCC_WEBSITE, self._bn, self._sec_num)
        elif self._pattern in (P_SN, P_AN):
            return "{}/{}/{}.php?keyword={}".format(pyccc.CCC_WEBSITE, self._bn, self._bn.lower(), self._sec_num)
        elif self._pattern in (P_MI, P_NI, P_PS):
            return "{}/{}/{}{}.htm".format(pyccc.CCC_WEBSITE, self._bn, self._bn, self._sec_num)

    def to_tex(self, bns: list[str], **kwargs):
        if self._bn in bns:
            return "\\suttaref{" + self.get_text() + "}"
        else:
            return pyccc.atom.Href(self.get_text(),
                                   self.get_cccurl(),
                                   pyccc.CCC_WEBSITE, "").to_tex(lang_convert.do_nothing)

    def to_xml(self, bns, **kwargs):
        if self._bn in bns:
            a = ET.Element("a", {"href": make_suttaname_href_link(self.get_text())})
        else:
            a = ET.Element("a", {"href": self.get_cccurl()})
        return a

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'text={self.text!r})')


def parse(s: str):
    # "[some text SN.1.1, AN.2.1 some text]"
    list_s = []
    offset = 0
    for m in re.finditer("|".join(PATTERNS), s):
        (begin, end) = m.span()
        list_s.append(s[offset:begin])
        list_s.append(SuttaRef(s[begin:end]))
        offset = end
    if offset < len(s):
        list_s.append(s[offset:])

    return list_s


def xn2filename(xn):
    if xn == "SN":
        return ""