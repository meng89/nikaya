import re


from public import BaseInfo, PinInfo
from public import Nikaya, Node, Sutra


from tools import get_sutra_urls, split_chinese_lines
from utils import read_text


class _MyInfo(BaseInfo, PinInfo):
    def __init__(self):
        BaseInfo.__init__(self)
        PinInfo.__init__(self)

        self.ji_serial = None
        self.ji_title = None

    def __repr__(self):
        s = ''
        s += 'ji   : "{}", "{}"\n'.format(self.ji_serial, self.ji_title)
        s += 'pin  : "{}", "{}"\n'.format(self.pin_serial, self.pin_title)
        s += 'sutra: "{}", "{}"'.format(self.sutra_serial_start, self.sutra_title)
        return s


class MyNikaya(Nikaya):
    @property
    def jis(self):
        return self.subs


class Ji(Node):
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

        m = re.match('^(\d+)\.?(\S+品)\s*$', line)
        if m:
            info.pin_serial = m.group(1)
            info.pin_title = m.group(2)
            continue

    # 增支部
    # 增支部1集1經(莊春江譯)
    # 增支部6集35經/明的一部分經(莊春江譯)
    m = re.match('^增支部(\d+)集(\d+(?:-\d+)?)經(?:/?(\S+經(\S+)?|))\(莊春江譯\)$', lines[-1])
    if m:
        info.ji_serial = m.group(1)

        serial = m.group(2).split('-')

        if len(serial) == 1:
            info.sutra_serial_start = serial[0]
            info.sutra_serial_end = serial[0]
        else:
            info.sutra_serial_start = serial[0]
            info.sutra_serial_end = serial[1]

        info.sutra_title = m.group(3)

    return info


def add_sec_title_range(nikaya):
    for ji in nikaya.jis:
        ji.sec_title = '{} 集'.format(ji.serial)

        for pin in ji.pins:
            pin.sec_title = '{} ({}-{})'.format(pin.title, pin.sutras[0].serial_start, pin.sutras[-1].serial_end)

    return nikaya


def make_nikaya(sutra_urls):

    nikaya = MyNikaya()
    nikaya.title_chinese = '增支部'
    nikaya.title_pali = 'Aṅguttara nikāya',
    nikaya.abbreviation = 'AN'

    for url in sutra_urls:

        chinese, pali, modified = read_text(url)

        header_lines, main_lines = split_chinese_lines(chinese)

        info = analyse_header(header_lines)

        if info.ji_serial is not None:
            if not nikaya.jis or nikaya.jis[-1].serial != info.ji_serial:
                ji = Ji()
                ji.serial = info.ji_serial

                nikaya.jis.append(ji)

        if info.pin_serial is not None:
            if not nikaya.jis[-1].pins or nikaya.jis[-1].pins[-1].serial != info.pin_serial:
                pin = Pin()
                pin.serial = info.pin_serial
                pin.title = info.pin_title

                nikaya.jis[-1].pins.append(pin)

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
                                               nikaya.jis[-1].serial,
                                               sutra.serial)

        nikaya.jis[-1].pins[-1].sutras.append(sutra)

    return nikaya


def get_nikaya(url):
    sutra_urls = get_sutra_urls(url)
    nikaya = make_nikaya(sutra_urls)

    nikaya = add_sec_title_range(nikaya)
    return nikaya
