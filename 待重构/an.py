import re


from pyabo.public import BaseInfo, PinInfo
from pyabo.public import Nikaya, Node, Sutta


from pyabo.tools import get_sutta_urls, split_chinese_lines
from pyabo.utils import read_page


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
        s += 'sutra: "{}", "{}"'.format(self.sutta_begin, self.sutta_title)
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
    # 增支部4集19經/不應該行處第三(莊春江譯)
    m = re.match('^增支部(\d+)集(\d+(?:-\d+)?)經(?:/?(\S+經?(\S+)?|))\(莊春江譯\)$', lines[-1])
    if m:
        info.ji_serial = m.group(1)

        serial = m.group(2).split('-')

        if len(serial) == 1:
            info.sutta_begin = serial[0]
            info.sutta_end = serial[0]
        else:
            info.sutta_begin = serial[0]
            info.sutta_end = serial[1]

        info.sutta_title = m.group(3)

    return info


def add_sec_title_range(nikaya):
    for ji in nikaya.jis:
        ji.sec_title = '{} 集'.format(ji.serial)

        for pin in ji.pins:
            pin.sec_title = '{} ({}-{})'.format(pin.title, pin.suttas[0].begin, pin.suttas[-1].end)

    return nikaya


def make_nikaya(sutra_urls):

    nikaya = MyNikaya()
    nikaya.title_zh = '增支部'
    nikaya.title_pali = 'Aṅguttara nikāya',
    nikaya.abbr = 'AN'

    for url in sutra_urls:

        chinese, pali, modified = read_page(url)

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

        sutra = Sutta()

        sutra.begin = info.sutta_begin
        sutra.end = info.sutta_end

        sutra.pali = pali
        sutra.chinese = chinese

        sutra.body_lines = main_lines

        sutra.last_modified = modified

        if sutra.begin == sutra.end:
            sutra.serial = sutra.begin
        else:
            sutra.serial = '{}-{}'.format(sutra.begin, sutra.end)

        if info.sutta_title:
            sutra.title = info.sutta_title
        else:
            sutra.title = ''

        if sutra.title:
            sutra.sec_title = sutra.serial + ' ' + sutra.title
        else:
            sutra.sec_title = sutra.serial

        sutra.abbreviation = '{}.{}.{}'.format(nikaya.abbr,
                                               nikaya.jis[-1].serial,
                                               sutra.serial)

        nikaya.jis[-1].pins[-1].suttas.append(sutra)

    return nikaya


def get_nikaya(url):
    sutra_urls = get_sutta_urls(url)
    nikaya = make_nikaya(sutra_urls)

    nikaya = add_sec_title_range(nikaya)
    return nikaya
