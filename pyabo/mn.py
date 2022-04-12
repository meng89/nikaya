import re

from pyabo.public import Nikaya, Node, Sutta
from pyabo.public import BaseInfo, PianInfo, PinInfo


from pyabo.tools import get_sutta_urls

from pyabo import page_parsing


HTML_INDEX = '/MN/index.htm'
BN = "MN"


class MNikaya(Nikaya):
    @property
    def pians(self):
        return self.subs


class _Pian(Node):
    @property
    def pins(self):
        return self.subs


class _Pin(Node):
    @property
    def suttas(self):
        return self.subs


class _MyInfo(BaseInfo, PianInfo, PinInfo):
    def __init__(self):
        BaseInfo.__init__(self)
        PianInfo.__init__(self)
        PinInfo.__init__(self)


def analyse_head(lines):
    info = _MyInfo()

    # 根本五十則篇
    # 1.根本法門品
    for line in lines:
        m = re.match(r"^(\S+篇)\s*$", line)
        if m:
            info.pian_title = m.group(1)
            continue
        m = re.match(r"^(\d+)\.(\S+品)\s*$", line)
        if m:
            info.pin_serial = m.group(1)
            info.pin_title = m.group(2)
            continue

        if line.strip() == "中部":
            continue

    return info


def analyse_sutta_info(line):
    info = _MyInfo()
    m = re.match(r"^中部(\d+)經/(\S+經\S*)$", line)
    if m:
        info.sutta_serial = m.group(1)
        info.sutta_title = m.group(2)
        return info

    raise Exception(repr(line))


def make_nikaya(domain):
    sutta_urls = get_sutta_urls(domain + HTML_INDEX)

    nikaya = MNikaya()
    nikaya.title_hant = '中部'
    nikaya.title_pali = 'Majjhima Nikāya',
    nikaya.abbr = 'MN'

    for _urltext, url in sutta_urls:
        homage_listline, head_line_list, sutta_name_part, translator_part, agama_part, lines, \
            pali_text, last_modified = page_parsing.read_page(url, nikaya.local_notes)

        if nikaya.last_modified is None:
            nikaya.last_modified = last_modified
        elif nikaya.last_modified < last_modified:
            nikaya.last_modified = last_modified

        if nikaya.homage_line is None:
            nikaya.homage_line = homage_listline

        head_info = analyse_head(head_line_list)
        sutta_info = analyse_sutta_info(sutta_name_part)

        if head_info.pian_title is not None:
            if not nikaya.pians or nikaya.pians[-1].title != head_info.pian_title:
                pian = _Pian()
                pian.title = head_info.pian_title
                nikaya.pians.append(pian)

        if head_info.pin_title is not None:
            if not nikaya.pians[-1].pins or nikaya.pians[-1].pins[-1].title != head_info.pin_title:
                pin = _Pin()
                pin.serial = head_info.pin_serial
                pin.title = head_info.pin_title
                nikaya.pians[-1].pins.append(pin)

        sutta = Sutta()
        sutta.serial = sutta_info.sutta_serial
        sutta.title = sutta_info.sutta_title

        sutta.agama_part = agama_part

        sutta.pali = pali_text

        sutta.body_lines = lines
        sutta.last_modified = last_modified

        nikaya.pians[-1].pins[-1].suttas.append(sutta)

    return nikaya
