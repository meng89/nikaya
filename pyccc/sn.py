import os
import re
import typing
import pickle

from public import BaseInfo, PianInfo, PinInfo
from public import Nikaya, Node, Sutta

from tools import get_sutta_urls

import pyccc.note

import utils
from utils import read_page

# from jinja2 import Template
# from mako.template import Template
from string import Template

from pylatex.utils import escape_latex as el

HTML_INDEX = '/SN/index.htm'

LOCAL_NOTE_KEY_PREFIX = "e"


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
        s += 'sutra    : "{}", "{}"'.format(self.sutta_serial_start, self.sutra_title)
        return s


# "有偈篇"
# "諸天相應" 1 必须有编号
# "蘆葦品"
# "暴流之渡過經" 1 必须编号
# SN.1.1

# 经太短，不应该一经一页
# 有时某个相应经太少，没有品，相应下面就是经，不应该建立空品多折叠一下


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
    def suttas(self):
        return self.subs


_nikaya = MyNikaya()


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


def analyse_sutta_name_line(line):
    info = _MyInfo()

    m = re.match(r"^ *相+應部?(\d+)相應 ?第?(\d+(?:-\d+)?)經(?:/(.+?經.*?))?\((?:\S+?)相應/(?:\S+?)篇/(?:\S+?)\)", line)
    if m:
        # info.xiangying_serial = m.group(1)

        serial = m.group(2).split('-')

        if len(serial) == 1:
            info.sutta_serial_start = serial[0]
            info.sutta_serial_end = serial[0]
        else:
            info.sutta_serial_start = serial[0]
            info.sutta_serial_end = serial[1]

        info.sutra_title = m.group(3)

    # “略去”的经文
    m = re.match(r"^相應部(48)相應 (83)-(114)經\s*$", line)
    if m:
        # info.xiangying_serial = m.group(1)
        info.sutta_serial_start = m.group(2)
        info.sutta_serial_end = m.group(3)

    m = re.match(r"^相應部(48)相應 (137)-(168)經\s*", line)
    if m:
        # info.xiangying_serial = m.group(1)
        info.sutta_serial_start = m.group(2)
        info.sutta_serial_end = m.group(3)

    return info


def add_sec_title_range(nikaya):
    for pian in nikaya.pians:
        pian.sec_title = '{} ({}-{})'.format(pian.title, pian.xiangyings[0].serial, pian.xiangyings[-1].serial)

        for xiangying in pian.xiangyings:
            for pin in xiangying.pins:
                pin.sec_title = '{} ({}-{})'.format(pin.title, pin.suttas[0].serial_start, pin.suttas[-1].serial_end)

    return nikaya


def make_nikaya(sutta_urls):
    nikaya = MyNikaya()
    nikaya.title_st = '相應部'
    nikaya.title_pali = 'Saṃyutta Nikāya'
    nikaya.abbreviation = 'SN'

    for url in sutta_urls:
        omage_listline, head_line_list, sutta_name_line, body_listline_list, local_note_dict, \
            pali_text, last_modified = read_page(url)

        if nikaya.last_modified is None:
            nikaya.last_modified = last_modified
        elif nikaya.last_modified < last_modified:
            nikaya.last_modified = last_modified

        if nikaya.omage_listline is None:
            nikaya.omage_listline = omage_listline

        head_info = analyse_head(head_line_list)
        sutta_info = analyse_sutta_name_line(sutta_name_line)

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

        sutta.serial_start = sutta_info.sutta_serial_start
        sutta.serial_end = sutta_info.sutta_serial_end

        sutta.pali = pali_text
        # sutta.chinese = line_list

        sutta.body_listline_list = body_listline_list

        sutta.local_note_dict = local_note_dict

        sutta.last_modified = last_modified

        if sutta.serial_start == sutta.serial_end:
            sutta.serial = sutta.serial_start
        else:
            sutta.serial = '{}-{}'.format(sutta.serial_start, sutta.serial_end)

        if sutta_info.sutra_title:
            sutta.title = sutta_info.sutra_title
        else:
            sutta.title = ''

        if sutta.title:
            sutta.sec_title = sutta.serial + ' ' + sutta.title
        else:
            sutta.sec_title = sutta.serial

        sutta.abbreviation = '{}.{}.{}'.format(nikaya.abbreviation,
                                               nikaya.pians[-1].xiangyings[-1].serial,
                                               sutta.serial)

        nikaya.pians[-1].xiangyings[-1].pins[-1].suttas.append(sutta)
    return nikaya


def load(domain):
    nikaya_filename = "sn_data"
    global _nikaya
    data_path = os.path.join(utils.PICKLE_DIR, nikaya_filename)

    try:
        with open(data_path, "rb") as rf:
            _nikaya = pickle.load(rf)
    except FileNotFoundError:
        sutra_urls = get_sutta_urls(domain + HTML_INDEX)
        nikaya = make_nikaya(sutra_urls)
        _nikaya = add_sec_title_range(nikaya)
        with open(data_path, "wb") as wf:
            pickle.dump(_nikaya, wf)


def to_latex(latex_io: typing.TextIO, bibtex_io: typing.TextIO, translate_fun=None):

    _head_t = open(os.path.join(utils.ROOT_DIR, "../latex", "head.tex"), "r").read()
    strdate = utils.lm_to_strdate(_nikaya.last_modified)
    _head = Template(_head_t).substitute(date=strdate, bib_path="sn_tc_notes.bib")
    latex_io.write(_head)

    book_local_note_dict = {}
    next_local_key = 1
    for pian in _nikaya.pians:
        latex_io.write("\\bookmarksetup{open=true}\n")
        latex_io.write("\\part{{{} ({}-{})}}\n".format(pian.title,
                                                       pian.xiangyings[0].serial,
                                                       pian.xiangyings[-1].serial))

        for xiangying in pian.xiangyings:
            latex_io.write("\\bookmarksetup{open=false}\n")
            latex_io.write("\\chapter{{{}. {}}}\n".format(xiangying.serial, xiangying.title))

            for pin in xiangying.pins:
                if pin.title is not None:
                    latex_io.write("\\section{{{} ({}-{})}}\n".format(pin.title,
                                                                      pin.suttas[0].serial_start,
                                                                      pin.suttas[-1].serial_end))

                for sutta in pin.suttas:
                    latex_io.write("\\subsection{{{}. {}}}\n".format(sutta.serial, sutta.title))
                    for body_listline in sutta.body_listline_list:
                        for e in body_listline:
                            if isinstance(e, str):
                                latex_io.write(el(e))
                            elif isinstance(e, utils.TextNeedNote):
                                tnd = e
                                if tnd.get_type() == utils.GLOBAL:
                                    note_key = tnd.get_number()
                                else:
                                    assert tnd.get_type() == utils.LOCAL
                                    note_key = LOCAL_NOTE_KEY_PREFIX + str(next_local_key)
                                    book_local_note_dict[note_key] = sutta.local_note_dict[tnd.get_number()]
                                    next_local_key += 1

                                latex_io.write("{}\\mycite{{{}}}".format(el(tnd.get_text()), note_key))

                            elif isinstance(e, utils.Href):
                                latex_io.write("\\href{{{}}}{{{}}}".format(el(e.href),
                                                                           el(e.text)))
                            else:
                                raise Exception("WTH?")
                        latex_io.write("\n\n")

    _tail = open(os.path.join(utils.ROOT_DIR, "../latex", "tail.tex"), "r").read()
    latex_io.write(_tail)

    local_note_bibtex_string = notes_to_bibtex(book_local_note_dict)
    bibtex_io.write(local_note_bibtex_string)

    global_note_bibtex_string = notes_to_bibtex(pyccc.note.get())
    bibtex_io.write(global_note_bibtex_string)


def notes_to_bibtex(notes):
    from pybtex.database import BibliographyData, Entry
    s = ""
    for citekey, listline_list in notes.items():
        bib_data = BibliographyData(
            {
                citekey: Entry("misc", [
                    ("note", note_to_latex(listline_list))
                ])
            }
        )
        s += bib_data.to_string("bibtex")
        s += "\n"
    return s


def note_to_latex(listline_list: iter, trans=None):
    t = trans or utils.no_translate
    elted_line = []
    for listline in listline_list:
        strline = ""
        for e in listline:
            if isinstance(e, str):
                strline += el(t(e))
            else:
                assert isinstance(e, utils.Href)
                strline += "\\href{{{}}}{{{}}}".format(e.href, el(t(e.text)))
        elted_line.append(strline)

    return "\\par\n".join(elted_line)