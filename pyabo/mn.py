import re
import pickle
import os


from pyabo.public import Nikaya, Node, Sutta
from pyabo.public import BaseInfo, PinInfo


from pyabo.tools import get_sutta_urls

from pyabo import page_parsing


HTML_INDEX = '/SN/index.htm'
BN = "SN"


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


def analyse_head(lines):  # public
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
        info.sutta_begin = m.group(1)
        info.sutta_end = m.group(1)

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
        homage_listline, head_line_list, sutta_name_part, translator_part, lines, \
            pali_text, last_modified = page_parsing.read_page(url, nikaya.local_notes)

        if nikaya.last_modified is None:
            nikaya.last_modified = last_modified
        elif nikaya.last_modified < last_modified:
            nikaya.last_modified = last_modified

        head_info = analyse_head(head_line_list)
        sutta_info = analyse_sutta_info(sutta_name_part)

        if info.pin_serial is not None:
            if not nikaya.pins or nikaya.pins[-1].serial != info.pin_serial:

                pin = _Pin()
                pin.serial = info.pin_serial
                pin.title = info.pin_title

                nikaya.pins.append(pin)

        sutra = Sutta()

        sutra.begin = info.sutta_begin
        sutra.end = info.sutta_end

        sutra.pali = pali
        sutra.chinese = chinese

        sutra.body_lines = main_lines

        sutra.last_modified = modified

        sutra.serial = sutra.begin

        sutra.title = info.sutra_title

        sutra.sec_title = sutra.serial + ' ' + sutra.title

        sutra.abbreviation = '{}.{}'.format(nikaya.abbreviation, sutra.serial)

        nikaya.pins[-1].suttas.append(sutra)

    return nikaya


def add_sec_title_range(nikaya):
    for pin in nikaya.pins:
        pin.sec_title = '{} ({}-{})'.format(pin.title, pin.suttas[0].begin, pin.suttas[-1].end)

    return nikaya


def get_nikaya(url):
    sutra_urls = get_sutta_urls(url)
    nikaya = make_nikaya(sutra_urls)

    nikaya = add_sec_title_range(nikaya)

    return nikaya


_nikaya = _MyNikaya()
_is_loaded = False


def load(domain, cache_dir):
    global _nikaya
    data_path = os.path.join(cache_dir, "mn")
    try:
        with open(data_path, "rb") as rf:
            _nikaya = pickle.load(rf)
    except (FileNotFoundError, ModuleNotFoundError):
        sutra_urls = get_sutta_urls(domain + HTML_INDEX)
        _nikaya = make_nikaya(sutra_urls)
        # _nikaya = add_sec_title_range(nikaya)
        with open(data_path, "wb") as wf:
            pickle.dump(_nikaya, wf)

    global _is_loaded
    _is_loaded = True


def get():
    if _is_loaded:
        return _nikaya
    else:
        raise Exception
