import re


from public import BaseInfo, PianInfo, PinInfo
from public import Nikaya, Node, Sutra


from tools import get_sutra_urls, split_chinese_lines
from utils import read_text


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
        s += 'sutra    : "{}", "{}"'.format(self.sutra_serial_start, self.sutra_title)
        return s


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


def analyse_header(lines):  # public
    """
    :param lines:
     :type lines: list
    :return:
    :rtype: _MyInfo
    """

    info = _MyInfo()

    for line in lines[:-1]:

        m = re.match('^\((\d)\)(\S+篇)\s*$', line)
        if m:
            info.pian_serial = m.group(1)
            info.pian_title = m.group(2)
            continue

        m = re.match('^(因緣篇)\s*$', line)
        if m:
            info.pian_serial = '2'
            info.pian_title = m.group(1)
            continue

        m = re.match('^(\d+)\.?(\S+品)\s*$', line)
        if m:
            info.pin_serial = m.group(1)
            info.pin_title = m.group(2)
            continue

        m = re.match('\d+[./](?:\(\d+\))?\.?(.+相應)\s*$', line)
        if m:
            info.xiangying_title = m.group(1)
            continue

    m = re.match('^ *相+應部?(\d+)相應 ?第?(\d+(?:-\d+)?)經(?:/(.+?經.*?))?\((?:\S+?)相應/(?:\S+?)篇/(?:\S+?)\)', lines[-1])
    if m:
        info.xiangying_serial = m.group(1)

        serial = m.group(2).split('-')

        if len(serial) == 1:
            info.sutra_serial_start = serial[0]
            info.sutra_serial_end = serial[0]
        else:
            info.sutra_serial_start = serial[0]
            info.sutra_serial_end = serial[1]

        info.sutra_title = m.group(3)

    # “略去”的经文
    m = re.match('^相應部(48)相應 (83)-(114)經\s*$', lines[-1])
    if m:
        info.xiangying_serial = m.group(1)
        info.sutra_serial_start = m.group(2)
        info.sutra_serial_end = m.group(3)

    m = re.match('^相應部(48)相應 (137)-(168)經\s*', lines[-1])
    if m:
        info.xiangying_serial = m.group(1)
        info.sutra_serial_start = m.group(2)
        info.sutra_serial_end = m.group(3)

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
    nikaya.title_chinese = '相應部'
    nikaya.title_pali = 'Saṃyutta Nikāya',
    nikaya.abbreviation = 'SN'

    for url in sutra_urls:

        chinese, pali, modified = read_text(url)

        header_lines, main_lines = split_chinese_lines(chinese)

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
            pin.title = '(未分品)'
            nikaya.pians[-1].xiangyings[-1].pins.append(pin)

        sutra = Sutra()

        sutra.serial_start = info.sutra_serial_start
        sutra.serial_end = info.sutra_serial_end

        sutra.pali = pali
        sutra.chinese = chinese

        sutra.main_lines = main_lines

        sutra.modified = modified

        if sutra.serial_start == sutra.serial_end:
            sutra.serial = sutra.serial_start
        else:
            sutra.serial = '{}-{}'.format(sutra.serial_start, sutra.serial_end)

        if info.sutra_title:
            sutra.title = info.sutra_title
        else:
            sutra.title = ''

        if sutra.title:
            sutra.sec_title = sutra.serial + ' ' + sutra.title
        else:
            sutra.sec_title = sutra.serial

        sutra.abbreviation = '{}.{}.{}'.format(nikaya.abbreviation,
                                               nikaya.pians[-1].xiangyings[-1].serial,
                                               sutra.serial)

        nikaya.pians[-1].xiangyings[-1].pins[-1].sutras.append(sutra)

    return nikaya


def get_nikaya(url):
    sutra_urls = get_sutra_urls(url)
    nikaya = make_nikaya(sutra_urls)

    nikaya = add_sec_title_range(nikaya)
    return nikaya
