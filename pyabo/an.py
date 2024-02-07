import re


from pyabo.public import Nikaya, Node, Sutta
from pyabo.public import BaseInfo, PinInfo, JiInfo, get_urltext_info

from pyabo.tools import get_sutta_urls
from pyabo import page_parsing


HTML_INDEX = "/AN/index.htm"


class _MyInfo(BaseInfo, PinInfo, JiInfo):
    def __init__(self):
        BaseInfo.__init__(self)
        PinInfo.__init__(self)
        JiInfo.__init__(self)


class ANikaya(Nikaya):
    @property
    def jis(self):
        return self.subs


class Ji(Node):
    @property
    def pins(self):
        return self.subs


class Pin(Node):
    @property
    def suttas(self):
        return self.subs


def analyse_head(lines):  # public
    info = _MyInfo()

    for line in lines:
        m = re.match(r"^(\d+)\.?(\S+品)\s*$", line)
        if m:
            info.pin_serial = m.group(1)
            info.pin_title = m.group(2)
    return info


def analyse_sutta_info(line):
    info = _MyInfo()
    # 增支部1集1經
    # 增支部6集35經/明的一部分經
    # 增支部4集19經/不應該行處第三

    m = re.match(r"^增支部(\d+)集(\d+)經$", line)
    if m:
        info.ji_serial = m.group(1)
        info.sutta_begin = m.group(2)
        info.sutta_end = m.group(2)
        return info

    m = re.match(r"^增支部(\d+)集(\d+)經/(\S+)$", line)
    if m:
        info.ji_serial = m.group(1)
        info.sutta_begin = m.group(2)
        info.sutta_end = m.group(2)
        info.sutta_title = m.group(3)
        return info
    #####

    m = re.match(r"^增支部(\d+)集(\d+)-(\d+)經$", line)
    if m:
        info.ji_serial = m.group(1)
        info.sutta_begin = m.group(2)
        info.sutta_end = m.group(3)
        return info

    m = re.match(r"^增支部(\d+)集(\d+)-(\d+)經/(\S+)$", line)
    if m:
        info.ji_serial = m.group(1)
        info.sutta_begin = m.group(2)
        info.sutta_end = m.group(3)
        info.sutta_title = m.group(4)
        return info

    # ccc bug
    m = re.match(r"^增支部(3)集(63)經\[/(恐懼經)]$", line)
    if m:
        info.ji_serial = m.group(1)
        info.sutta_begin = m.group(2)
        info.sutta_end = m.group(2)
        info.sutta_title = m.group(3)
        return info

    raise Exception(repr(line))


def make_nikaya(domain):
    sutta_urls = get_sutta_urls(domain + HTML_INDEX)

    nikaya = ANikaya()
    nikaya.title_hant = "增支部"
    nikaya.title_pali = "Aṅguttara Nikāya"
    nikaya.abbr = "AN"

    for urltext, url in sutta_urls:
        homage_listline, head_line_list, sutta_name_part, translator_part, agama_part,\
            lines, pali_text, last_modified = page_parsing.read_page(url, nikaya.local_notes)

        if nikaya.last_modified is None:
            nikaya.last_modified = last_modified
        elif nikaya.last_modified < last_modified:
            nikaya.last_modified = last_modified

        if nikaya.homage_line is None:
            nikaya.homage_line = homage_listline

        head_info = analyse_head(head_line_list)
        sutta_info = analyse_sutta_info(sutta_name_part)
        urltext_info = get_urltext_info(urltext)

        if not nikaya.jis or nikaya.jis[-1].serial != sutta_info.ji_serial:
            ji = Ji()
            ji.serial = sutta_info.ji_serial
            nikaya.jis.append(ji)

        if head_info.pin_serial is not None:
            if not nikaya.jis[-1].pins or nikaya.jis[-1].pins[-1].serial != head_info.pin_serial:

                pin = Pin()
                pin.serial = head_info.pin_serial
                pin.title = head_info.pin_title

                nikaya.jis[-1].pins.append(pin)

        sutta = Sutta()
        sutta.begin = urltext_info.sutta_begin
        sutta.end = urltext_info.sutta_end
        sutta.title = sutta_info.sutta_title

        sutta.agama_part = agama_part

        sutta.pali = pali_text

        sutta.body_lines = lines
        sutta.last_modified = last_modified

        nikaya.jis[-1].pins[-1].suttas.append(sutta)

    return nikaya
