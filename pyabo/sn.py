import re

from pyabo.public import BaseInfo, PianInfo, PinInfo
from pyabo.public import Nikaya, Node, Sutta


from pyabo.tools import get_sutta_urls

from pyabo import page_parsing


HTML_INDEX = '/SN/index.htm'

LOCAL_NOTE_KEY_PREFIX = "e"

BN = "SN"


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
        s += 'sutra    : "{}", "{}"'.format(self.sutta_begin, self.sutta_title)
        return s


# "有偈篇"
# "諸天相應" 1 必须有编号
# "蘆葦品"
# "暴流之渡過經" 1 必须编号
# SN.1.1

# 经太短，不应该一经一页
# 有些相应经太少，没有品，相应下面就是经，不应该建立空品多折叠一下


class SNikaya(Nikaya):
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
    def suttas(self):
        return self.subs


_nikaya = SNikaya()
_is_loaded = False


def analyse_head(lines):  # public
    info = _MyInfo()
    for line in lines:
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

        m = re.match(r"(\d+)[./](?:\(\d+\))?\.?(.+相應)\s*$", line)
        if m:
            info.xiangying_serial = m.group(1)
            info.xiangying_title = m.group(2)
            continue

    return info


def analyse_sutta_info(line):
    info = _MyInfo()
    # m = re.match(r"^ *相+應部?(\d+)相應 ?第?(\d+(?:-\d+)?)經(?:/(.+?經.*?))?", line)
    m = re.match(r"^ *相+應部?(\d+)相應 ?第?(\d+(?:-\d+)?)經/(.+經[^(]*).*$", line)
    if m:
        serial = m.group(2).split('-')
        if len(serial) == 1:
            info.sutta_begin = serial[0]
            info.sutta_end = serial[0]
        else:
            info.sutta_begin = serial[0]
            info.sutta_end = serial[1]
        info.sutta_title = m.group(3)
        return info

    m = re.match(r"^相應部\d+相應 ?(\d+)-(\d+)經$", line)
    if m:
        info.sutta_begin = m.group(1)
        info.sutta_end = m.group(2)
        return info

    raise Exception(repr(line))


def make_nikaya(domain):
    sutta_urls = get_sutta_urls(domain + HTML_INDEX)

    nikaya = SNikaya()
    nikaya.title_zh = '相應部'
    nikaya.title_pali = 'Saṃyutta Nikāya'
    nikaya.abbr = 'SN'
    for _urltext, url in sutta_urls:
        homage_listline, head_line_list, sutta_name_part, translator_part, agama_part, \
            lines, pali_text, last_modified = page_parsing.read_page(url, nikaya.local_notes)

        if nikaya.last_modified is None:
            nikaya.last_modified = last_modified
        elif nikaya.last_modified < last_modified:
            nikaya.last_modified = last_modified

        if nikaya.homage_line is None:
            nikaya.homage_line = homage_listline

        head_info = analyse_head(head_line_list)
        sutta_info = analyse_sutta_info(sutta_name_part)

        if head_info.pian_serial is not None:
            if not nikaya.subs or nikaya.subs[-1].serial != head_info.pian_serial:
                pian = Pian()
                pian.serial = head_info.pian_serial
                pian.title = head_info.pian_title

                nikaya.subs.append(pian)

        if head_info.xiangying_serial is not None:
            if not nikaya.subs[-1].subs or nikaya.subs[-1].subs[-1].serial != head_info.xiangying_serial:
                xiangying = XiangYing()
                xiangying.serial = head_info.xiangying_serial
                xiangying.title = head_info.xiangying_title

                xiangying.sec_title = '{} {}'.format(xiangying.serial, xiangying.title)

                nikaya.subs[-1].subs.append(xiangying)

        if head_info.pin_serial is not None:
            if not nikaya.subs[-1].subs[-1].subs or nikaya.subs[-1].subs[-1].subs[-1].serial != head_info.pin_serial:
                pin = Pin()
                pin.serial = head_info.pin_serial
                pin.title = head_info.pin_title

                nikaya.subs[-1].subs[-1].subs.append(pin)

        if not nikaya.pians[-1].xiangyings[-1].pins:
            pin = Pin()
            pin.serial = 1
            pin.title = None
            nikaya.pians[-1].xiangyings[-1].pins.append(pin)

        sutta = Sutta()

        sutta.begin = sutta_info.sutta_begin
        sutta.end = sutta_info.sutta_end
        sutta.agama_part = agama_part

        sutta.pali = pali_text

        sutta.body_lines = lines

        sutta.last_modified = last_modified

        sutta.title = sutta_info.sutta_title

        nikaya.pians[-1].xiangyings[-1].pins[-1].suttas.append(sutta)
    return nikaya
