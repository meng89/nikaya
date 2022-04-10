import re


from pyabo.public import Nikaya, Node, Sutta
from pyabo.public import BaseInfo, PinInfo

from pyabo.tools import get_sutta_urls
from pyabo import page_parsing


HTML_INDEX = "/DN/index.htm"


class DNikaya(Nikaya):
    @property
    def pins(self):
        return self.subs


class _Pin(Node):
    @property
    def suttas(self):
        return self.subs


class _MyInfo(BaseInfo, PinInfo):
    def __init__(self):
        BaseInfo.__init__(self)
        PinInfo.__init__(self)


def analyse_head(lines):
    info = _MyInfo()
    for line in lines:
        m = re.match(r"^(\S、\S+品)\s*", line)
        if m:
            info.pin_title = m.group(1)
    return info


def analyse_sutta_info(line):
    info = _MyInfo()

    m = re.match(r"^長部(\d+)經/(\S+經)$", line)
    if m:
        info.sutta_serial = m.group(1)
        info.sutta_title = m.group(2)
    return info


def make_nikaya(domain):
    sutta_urls = get_sutta_urls(domain + HTML_INDEX)

    nikaya = DNikaya()
    nikaya.title_zh = '長部'
    nikaya.title_pali = 'Dīgha Nikāya',
    nikaya.abbr = 'DN'

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

        if head_info.pin_title is not None:
            if not nikaya.pins or nikaya.pins[-1].title != head_info.pin_title:
                pin = _Pin()
                pin.title = head_info.pin_title
                nikaya.pins.append(pin)

        sutta = Sutta()
        sutta.serial = sutta_info.sutta_serial
        sutta.title = sutta_info.sutta_title

        sutta.agama_part = agama_part

        sutta.pali = pali_text

        sutta.body_lines = lines
        sutta.last_modified = last_modified

        nikaya.pins[-1].suttas.append(sutta)

    return nikaya
