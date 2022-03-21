import re

import pyccc
import dopdf

P1 = r"(南傳作)(「.+?」)"
P2 = r"(\(i+\))(「.+?」)"
P3 = r"(菩提比丘長老英譯為)(「.+?」)"

PATTERNS = (P1, P2, P3)


class NoteTagBase(pyccc.BaseElement):

    def __init__(self, text):
        self.text = text
        self._tex_cmd = self.__class__.__name__

    def get_text(self):
        return self.text

    def to_tex(self, bns, c, **kwargs):
        return "\\" + self._tex_cmd + "{" + dopdf.join_to_tex(line=[self.text], bns=bns, c=c) + "}"

    def to_xml(self, *args, **kwargs):
        return self.text

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'text={self.text!r})')


_s = """(1)「自作(SA)」，南傳作(i)「自作者」(attakāre)，Maurice Walshe先生英譯為「自己的力量」(self-power, DN.2)，""" \
    """坦尼沙羅比丘長老英譯為「自己引起的」(self-caused, DN.2)，""" \
    """菩提比丘長老英譯為「自己發動」self-initiative, AN.6.38)，K. Nizamis英譯為「自己行為者」(self-doer, AN.6.38)。""" \
    """(ii)「自己作的」(sayaṃkataṃ)，菩提比丘長老英譯為「被自己創造」(created by oneself, SN.12.17)。"""


class NoteSubKeyHead(NoteTagBase):
    pass


class NoteKeywordAgamaHead(NoteTagBase):
    pass


class NoteKeywordNikayaHead(NoteTagBase):
    pass


class NoteSubEntryKey(NoteTagBase):
    pass


class NoteKeywordAgama(NoteTagBase):
    pass


class NoteKeywordNikaya(NoteTagBase):
    pass


class NoteKeywordBhikkhuBodhi(NoteTagBase):
    pass


class NoteKeywordBhikkhuNanamoli(NoteTagBase):
    pass


def split_str(s: str):
    list_s = []
    offset = 0
    for m in re.finditer("|".join(PATTERNS), s):
        (begin, end) = m.span()
        list_s.append(s[offset:begin])
        list_s.extend(split_notekeyword(s[begin:end]))
        offset = end
    if offset < len(s):
        list_s.append(s[offset:])

    return list_s


def split_notekeyword(s):
    line = []
    for p in PATTERNS:
        m = re.match("^{}$".format(p), s)
        if m:
            if p == P1:
                line.extend([m.group(1), NoteKeywordNikaya(m.group(2))])
            elif p == P2:
                line.extend([NoteSubEntryKey(m.group(1)), NoteKeywordNikaya(m.group(2))])
            elif p == P3:
                line.extend([m.group(1), NoteKeywordBhikkhuBodhi(m.group(2))])
            else:
                raise Exception
            return line
    raise Exception


_s = """(1)「方便」，南傳作(i)「努力」(yoga)，菩提比丘長老英譯為「努力；盡力；致力」(an exertion)。""" \
     """"(ii)「精進」(vāyāmo)，菩提比丘長老英譯為「努力於」(make an effort in)。""" \
     """(iii)「法門；方法」(pariyāyaṃ)，菩提比丘長老英譯為「方法」(a method, SN.35.153)。"""
