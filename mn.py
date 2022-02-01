import re


from public import Nikaya, Node, Sutta
from public import BaseInfo, PinInfo


from tools import get_sutra_urls, split_chinese_lines
from utils import read_sutta_page


class _MyNikaya(Nikaya):
    @property
    def pins(self):
        return self.subs


class _Pin(Node):
    @property
    def sutras(self):
        return self.subs


class _MyInfo(BaseInfo, PinInfo):
    def __init__(self):
        BaseInfo.__init__(self)
        PinInfo.__init__(self)


def analyse_header(lines):  # public
    """
    :param lines:
     :type lines: list
    :return:
    :rtype: _MyInfo
    """

    info = _MyInfo()

    # 中部1經/根本法門經(根本法門品[1])(莊春江譯)
    # 中部24經接力車經(譬喻品[3])(莊春江譯)
    m = re.match('^\S+?(\d+)經/?(\S+經)\((\S+品)\[(\d+)\]\)\(莊春江譯\)\s*$', lines[-1])
    if m:
        info.sutta_serial_start = m.group(1)
        info.sutta_serial_end = m.group(1)

        info.sutra_title = m.group(2)

        info.pin_title = m.group(3)
        info.pin_serial = m.group(4)

    return info


def make_nikaya(sutra_urls):
    nikaya = _MyNikaya()
    nikaya.title_st = '中部'
    nikaya.title_pali = 'Majjhima Nikāya',
    nikaya.abbreviation = 'MN'

    for url in sutra_urls:

        chinese, pali, modified = read_sutta_page(url)

        header_lines, main_lines = split_chinese_lines(chinese)

        info = analyse_header(header_lines)

        if info.pin_serial is not None:
            if not nikaya.pins or nikaya.pins[-1].serial != info.pin_serial:

                pin = _Pin()
                pin.serial = info.pin_serial
                pin.title = info.pin_title

                nikaya.pins.append(pin)

        sutra = Sutta()

        sutra.serial_start = info.sutta_serial_start
        sutra.serial_end = info.sutta_serial_end

        sutra.pali = pali
        sutra.chinese = chinese

        sutra.main_lines = main_lines

        sutra.modified = modified

        sutra.serial = sutra.serial_start

        sutra.title = info.sutra_title

        sutra.sec_title = sutra.serial + ' ' + sutra.title

        sutra.abbreviation = '{}.{}'.format(nikaya.abbreviation, sutra.serial)

        nikaya.pins[-1].sutras.append(sutra)

    return nikaya


def add_sec_title_range(nikaya):
    for pin in nikaya.pins:
        pin.sec_title = '{} ({}-{})'.format(pin.title, pin.sutras[0].serial_start, pin.sutras[-1].serial_end)

    return nikaya


def get_nikaya(url):
    sutra_urls = get_sutra_urls(url)
    nikaya = make_nikaya(sutra_urls)

    nikaya = add_sec_title_range(nikaya)

    return nikaya
