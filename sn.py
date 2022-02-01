import re

from public import BaseInfo, PianInfo, PinInfo
from public import Nikaya, Node, Sutta

from tools import get_sutra_urls, split_chinese_lines
from utils import read_sutta_page

from pylatex.utils import escape_latex

HTML_INDEX = '/SN/index.htm'


class _MyInfo(BaseInfo, PianInfo, PinInfo):
    def __init__(self):
        BaseInfo.__init__(self)
        PianInfo.__init__(self)
        PinInfo.__init__(self)

        self.xiangying_serial = None
        self.xiangying_title = None

    def __repr__(self):
        s = ''
        s += 'pian     : "{}", "{}"\n'.format(self.pian_serial, self.pian_title)
        s += 'xiangying: "{}", "{}"\n'.format(self.xiangying_serial, self.xiangying_title)
        s += 'pin      : "{}", "{}"\n'.format(self.pin_serial, self.pin_title)
        s += 'sutra    : "{}", "{}"'.format(self.sutta_serial_start, self.sutra_title)
        return s


# "有偈篇"
# "諸天相應" 1 必须有编号
# "蘆葦品"
# "暴流之渡過經" 1 必须编号
# SN.1.1

# 经太短，一个相应里的经典不应该在新页面
# 有时某个相应经太少，没有品，相应下面就是经，不应该建立空品多折叠一下


class MyNikaya(Nikaya):
    @property
    def pians(self):
        return self.subs


class Pian(Node):
    @property
    def xiangyings(self):
        return self.subs


class XiangYing(Node):
    @property
    def pins(self):
        return self.subs


class Pin(Node):
    @property
    def sutras(self):
        return self.subs


_nikaya = MyNikaya()


def analyse_header(lines):  # public

    info = _MyInfo()

    for line in lines[:-1]:

        m = re.match(r"^\((\d)\)(\S+篇)\s*$", line)
        if m:
            info.pian_serial = m.group(1)
            info.pian_title = m.group(2)
            continue

        m = re.match(r"^(因緣篇)\s*$", line)
        if m:
            info.pian_serial = '2'
            info.pian_title = m.group(1)
            continue

        m = re.match(r"^(\d+)\.?(\S+品)\s*$", line)
        if m:
            info.pin_serial = m.group(1)
            info.pin_title = m.group(2)
            continue

        m = re.match(r"\d+[./](?:\(\d+\))?\.?(.+相應)\s*$", line)
        if m:
            info.xiangying_title = m.group(1)
            continue

    m = re.match(r"^ *相+應部?(\d+)相應 ?第?(\d+(?:-\d+)?)經(?:/(.+?經.*?))?\((?:\S+?)相應/(?:\S+?)篇/(?:\S+?)\)",
                 lines[-1])
    if m:
        info.xiangying_serial = m.group(1)

        serial = m.group(2).split('-')

        if len(serial) == 1:
            info.sutta_serial_start = serial[0]
            info.sutta_serial_end = serial[0]
        else:
            info.sutta_serial_start = serial[0]
            info.sutta_serial_end = serial[1]

        info.sutra_title = m.group(3)

    # “略去”的经文
    m = re.match(r"^相應部(48)相應 (83)-(114)經\s*$", lines[-1])
    if m:
        info.xiangying_serial = m.group(1)
        info.sutta_serial_start = m.group(2)
        info.sutta_serial_end = m.group(3)

    m = re.match(r"^相應部(48)相應 (137)-(168)經\s*", lines[-1])
    if m:
        info.xiangying_serial = m.group(1)
        info.sutta_serial_start = m.group(2)
        info.sutta_serial_end = m.group(3)

    return info


def add_sec_title_range(nikaya):
    for pian in nikaya.pians:
        pian.sec_title = '{} ({}-{})'.format(pian.title, pian.xiangyings[0].serial, pian.xiangyings[-1].serial)

        for xiangying in pian.xiangyings:
            for pin in xiangying.pins:
                pin.sec_title = '{} ({}-{})'.format(pin.title, pin.sutras[0].serial_start, pin.sutras[-1].serial_end)

    return nikaya


def make_nikaya(sutra_urls):
    nikaya = MyNikaya()
    nikaya.title_st = '相應部'
    nikaya.title_pali = 'Saṃyutta Nikāya'
    nikaya.abbreviation = 'SN'

    for url in sutra_urls:

        # line_list, local_note_list, pali, last_modified = read_sutta_page(url)
        head_lines, sutta_name_line, sutta_lines, pali_doc_text, last_modified = read_sutta_page(url)

        header_lines, main_lines = split_chinese_lines(line_list)

        info = analyse_header(header_lines)

        if info.pian_serial is not None:
            if not nikaya.subs or nikaya.subs[-1].serial != info.pian_serial:
                pian = Pian()
                pian.serial = info.pian_serial
                pian.title = info.pian_title

                nikaya.subs.append(pian)

        if info.xiangying_serial is not None:
            if not nikaya.subs[-1].subs or nikaya.subs[-1].subs[-1].serial != info.xiangying_serial:
                xiangying = XiangYing()
                xiangying.serial = info.xiangying_serial
                xiangying.title = info.xiangying_title

                xiangying.sec_title = '{} {}'.format(xiangying.serial, xiangying.title)

                nikaya.subs[-1].subs.append(xiangying)

        if info.pin_serial is not None:
            if not nikaya.subs[-1].subs[-1].subs or nikaya.subs[-1].subs[-1].subs[-1].serial != info.pin_serial:
                pin = Pin()
                pin.serial = info.pin_serial
                pin.title = info.pin_title

                nikaya.subs[-1].subs[-1].subs.append(pin)

        if not nikaya.pians[-1].xiangyings[-1].pins:
            pin = Pin()
            pin.serial = 1
            pin.title = None
            nikaya.pians[-1].xiangyings[-1].pins.append(pin)

        sutta = Sutta()

        sutta.serial_start = info.sutta_serial_start
        sutta.serial_end = info.sutta_serial_end

        sutta.pali = pali
        sutta.chinese = line_list

        sutta.main_lines = main_lines

        sutta.modified = last_modified

        if sutta.serial_start == sutta.serial_end:
            sutta.serial = sutta.serial_start
        else:
            sutta.serial = '{}-{}'.format(sutta.serial_start, sutta.serial_end)

        if info.sutra_title:
            sutta.title = info.sutra_title
        else:
            sutta.title = ''

        if sutta.title:
            sutta.sec_title = sutta.serial + ' ' + sutta.title
        else:
            sutta.sec_title = sutta.serial

        sutta.abbreviation = '{}.{}.{}'.format(nikaya.abbreviation,
                                               nikaya.pians[-1].xiangyings[-1].serial,
                                               sutta.serial)

        nikaya.pians[-1].xiangyings[-1].pins[-1].sutras.append(sutta)

    return nikaya


def load_nikaya(url):
    global _nikaya
    sutra_urls = get_sutra_urls(url + HTML_INDEX)
    nikaya = make_nikaya(sutra_urls)
    _nikaya = add_sec_title_range(nikaya)


def to_latex(path=None, note=None, lang=None):
    # f = open(path, "w")
    for pian in _nikaya.pians:
        print(pian.title)

