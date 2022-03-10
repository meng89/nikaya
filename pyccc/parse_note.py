import re


from pyccc import atom_suttaref, pdf

P1 = r"(南傳作)(「.+?」)"
P2 = r"(\(i+\))(「.+?」)"
P3 = r"(菩提比丘長老英譯為)(「.+?」)"

PATTERNS = (P1, P2, P3)


class NoteSubKey(object):
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'text={self.text!r})')


class NoteKeywordDefault(object):
    def __init__(self, text):
        self.text = text
        self._tex_cmd = self.__class__.__name__

    def get_text(self):
        return self.text

    def _contents(self):
        return atom_suttaref.parse(self.text)

    def to_tex(self, bns, c):
        return "\\" + self._tex_cmd + "{" + pdf.join_to_tex(line=self._contents(), bns=bns, c=c) + "}"

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'text={self.text!r})')


class NoteKeywordAgama(NoteKeywordDefault):
    pass


class NoteKeywordNikaya(NoteKeywordDefault):
    pass


class NoteKeywordBhikkhuBodhi(NoteKeywordDefault):
    pass


class NoteKeywordBhikkhuNanamoli(NoteKeywordDefault):
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
                line.extend([NoteSubKey(m.group(1)), NoteKeywordNikaya(m.group(2))])
            elif p == P3:
                line.extend([m.group(1), NoteKeywordBhikkhuBodhi(m.group(2))])
            else:
                raise Exception
            return line
    raise Exception


_s = """(1)「方便」，南傳作(i)「努力」(yoga)，菩提比丘長老英譯為「努力；盡力；致力」(an exertion)。""" \
     """"(ii)「精進」(vāyāmo)，菩提比丘長老英譯為「努力於」(make an effort in)。""" \
     """(iii)「法門；方法」(pariyāyaṃ)，菩提比丘長老英譯為「方法」(a method, SN.35.153)。"""
