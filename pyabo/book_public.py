import opencc
import abc

# TC = "tc"
# SC = "sc"


def do_nothing(x):
    return x


_table = [
    ("「", "“"),
    ("」", "”"),
    ("『", "‘"),
    ("』", "’"),
]


def convert2sc(s):
    if s:
        converter = opencc.OpenCC('tw2sp.json')
        return converter.convert(s)
    else:
        return s


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


class XC(object):
    @property
    @abc.abstractmethod
    def c(self):
        pass

    @property
    @abc.abstractmethod
    def xmlang(self):
        pass

    @property
    @abc.abstractmethod
    def zhlang(self):
        pass

    @property
    @abc.abstractmethod
    def enlang(self):
        pass

    @property
    @abc.abstractmethod
    def han_version(self):
        pass


class TC(XC):
    @property
    def c(self):
        return do_nothing

    @property
    def xmlang(self):
        return "zh-Hant"

    @property
    def zhlang(self):
        return "繁"

    @property
    def enlang(self):
        return "tc"

    @property
    def han_version(self):
        return "傳統中文版"


class SC(XC):
    @property
    def c(self):
        return convert2sc

    @property
    def xmlang(self):
        return "zh-Hans"

    @property
    def zhlang(self):
        return "简"

    @property
    def enlang(self):
        return "sc"

    @property
    def han_version(self):
        return "机转简体版"
