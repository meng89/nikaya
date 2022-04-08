import abc


import xl


cjk_table = [
    (0x2000, 0x206F),
    (0x2190, 0x21FF),
    (0x2200, 0x22FF),
    (0x2460, 0x257f),
    (0x2E80, 0x2EFF),
    (0x3000, 0x9FFF),
    (0xf900, 0xfaff),
    (0xfe30, 0xfe4f),

    (0xff00, 0xffef),

    (0x20000, 0x2a6df),
    (0x2a700, 0x2b73f),
    (0x2b740, 0x2b81f),
    (0x2b820, 0x2ceaf),
    (0x2ceb0, 0x2ebef),
    (0x2f800, 0x2fa1f),
    (0x30000, 0x3134f),
]

latin_table = [
    (0x0000, 0x02ff),
    (0x1d00, 0x1dbf),
    (0x1e00, 0x1fff),
    (0x2070, 0x209f),
    (0x2100, 0x218f),
    (0x2c60, 0x2c7f),
    (0xa720, 0xa7ff),
    (0xab30, 0xab6f),
]

tibetan_table = [
    (0x0f00, 0x0fff),
]


def is_cjk(c):
    for begin, end in cjk_table:
        if begin <= ord(c) <= end:
            return True
    return False


def is_latin(c):
    for begin, end in latin_table:
        if begin <= ord(c) <= end:
            return True
    return False


def is_tibetan(c):
    for begin, end in tibetan_table:
        if begin <= ord(c) <= end:
            return True
    return False


def split2basestr(s):
    basestrs = []
    last_type = None
    last = ""

    def _reset_last():
        nonlocal last_type, last
        if last:
            basestrs.append(last_type(last))
        last = ""

    for c in s:
        # U+2700..U+27BF  ->  U+2460..U+24FF
        # ccc_bug mark
        if c == "➀":
            c = "①"
        elif c == "➁":
            c = "②"

        if is_cjk(c):
            if last_type == CjkStr:
                pass
            else:
                if last:
                    _reset_last()
                last_type = CjkStr
            last += c

        elif is_latin(c):
            if last_type == LatinStr:
                pass
            else:
                if last:
                    _reset_last()
                last_type = LatinStr
            last += c

        elif is_tibetan(c):
            if last_type == TibetanStr:
                pass
            else:
                if last:
                    _reset_last()
                last_type = TibetanStr
            last += c

        else:
            raise Exception(c)

    _reset_last()
    return basestrs


def str2es(s):
    return [bs.to_e() for bs in split2basestr(s)]


class BaseStr(object):
    def __init__(self, text):
        self.text = text

    @property
    @abc.abstractmethod
    def _xml_class(self):
        pass

    def to_tex(self):
        return self.text

    def to_e(self):
        span = xl.Element("span", {"class": self._xml_class})
        span.kids.append(self.text)
        return span

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'text={self.text!r})')


class CjkStr(BaseStr):
    @property
    def _xml_class(self):
        return "cjk"


class LatinStr(BaseStr):
    @property
    def _xml_class(self):
        return "lat"


class TibetanStr(BaseStr):
    @property
    def _xml_class(self):
        return "tib"
