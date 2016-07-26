import re


from public import Nikaya, Node, Sutra
from public import BaseInfo, PinInfo


from tools import get_sutra_urls, split_chinese_lines
from utils import read_text


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

    # 長部14經/譬喻大經(大品[第二])(莊春江譯)
    m = re.match('^長部(\d+)經/(\S+經)\((\S+品)\[\S+\]\)\(莊春江譯\)$', lines[-1])
    if m:
        info.sutra_serial_start = m.group(1)
        info.sutra_serial_end = m.group(1)

        info.sutra_title = m.group(2)

        info.pin_title = m.group(3)

    return info


def make_nikaya(sutra_urls):

    nikaya = _MyNikaya()
    nikaya.title_chinese = '長部'
    nikaya.title_pali = 'Digha Nikāya',
    nikaya.abbreviation = 'DN'

    for url in sutra_urls:

        chinese, pali, modified = read_text(url)

        header_lines, main_lines = split_chinese_lines(chinese)

        info = analyse_header(header_lines)

        if info.pin_title is not None:
            if not nikaya.pins or nikaya.pins[-1].title != info.pin_title:

                pin = _Pin()
                pin.serial = info.pin_serial
                pin.title = info.pin_title

                nikaya.pins.append(pin)

        sutra = Sutra()

        sutra.serial_start = info.sutra_serial_start
        sutra.serial_end = info.sutra_serial_end

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
