import os.path
import re
import bs4
import xl

import requests
from urllib.parse import urlparse

from dateutil.parser import parse as parsedate

import pyabo.parse_original_line
from pyabo import base, note_thing



try:
    import user_config as config
except ImportError:
    import config as config


class AnalyseError(Exception):
    pass


LOCAL = "LOCAL"
GLOBAL = "GLOBAL"


def _no_translate(x: str):
    return x


no_translate = _no_translate

WARNING = "WARNING"
INFO = "INFO"


log_fd = None


def ccc_bug(type_, url, string):
    try:
        import user_config as uc
    except ImportError:
        import config as uc

    global log_fd
    if log_fd is None:
        log_fd = open(uc.LOG_PATH, "w")

    s = "<{}>: text_and_url: {}, msg: {}".format(type_, url, string)
    log_fd.write(s+"\r\n")
    print(s)


def read_pages(filenames):
    results = []
    for file_path in filenames:
        full_path = os.path.join(config.DOWNLOAD_DIR, file_path)
        last_modified = os.path.getmtime(full_path)
        data = open(full_path, "r").read()
        soup = bs4.BeautifulSoup(data, 'html5lib')


def read_page(soup):
    x = soup.prettify()
    root = xl.parse(str(soup)).root

    divs = root.find_descendants("div")

    div_nikaya = None
    div_pali = None
    div_comp = None

    for div in divs:
        if "class" in div.attrs.keys():
            if div.attrs["class"] == "nikaya":
                div_nikaya = div
            elif div.attrs["class"] == "pali":
                div_pali = div
            elif div.attrs["class"] == "comp":
                div_comp = div

    pali_doc = soup.find("div", {"class": "pali"}).text

    notes = take_comp(div_comp)

    homage_and_head_lines, sutta_name_part, translator_part, agama_part, body_lines = take_nikaya(div_nikaya)

    homage_line, _head_lines = _split_homage_and_head(homage_and_head_lines)
    head_lines = listline_list_to_line_list(_head_lines)

    return homage_line, head_lines, sutta_name_part, translator_part, agama_part, body_lines, pali_doc


def take_comp(div_comp: xl.Element):
    notes = []
    for span in div_comp.find_descendants("span"):
        id_ = span.attrs.get("id")
        if id_ is not None:
            m = re.match("^note(\d+)$", id_)
            if m:
                note = xl.Element("note")
                note.attrs["id"] = m.group(1)
                note.kids.extend(_clean_contents(span.kids))
    return notes


def _clean_contents(contents: list) -> list:
    lines = []
    line = []
    for e in contents:
        if isinstance(e, xl.Element) and e.tag == "br":
            lines.append(line)
            line = []
        elif isinstance(e, xl.Comment):
            pass
        elif isinstance(e, str):
            if e.strip("\n") != "":
                line.append(e)
        elif isinstance(e, (str, xl.Element)):
            line.append(e)
        else:
            raise Exception((type(e), repr(e)))
            # line.append(e)
    if line:
        lines.append(line)

    return lines


def take_nikaya(div_nikaya):
    contents = div_nikaya.kids
    homage_and_head_oline = []
    homage_and_head_olines = []

    sutta_name_es = None
    body_lines = []

    def _do_line(_oline):
        return pyabo.parse_original_line.do_line(oline=_oline,
                                                 funs=[note_thing.do_str,
                                                       note_thing.do_href,
                                                       note_thing.do_onmouseover_global,
                                                       note_thing.do_onmouseover_local],
                                                 **kwargs)
    while contents:
        e = contents.pop(0)
        if e.tag == "span" and e.attrs["class"] == "sutra_name":
            sutta_name_es = e.kids
            break
        elif isinstance(e, xl.Element) and e.tag == "br":
            homage_and_head_olines.append(homage_and_head_oline)
            homage_and_head_oline = []
        else:
            homage_and_head_oline.append(e)
    if homage_and_head_oline:
        homage_and_head_olines.append(homage_and_head_oline)

    homage_and_head_lines = [_do_line(_oline) for _oline in homage_and_head_olines]


    e2 = contents.pop(0)
    assert isinstance(e2, str)
    translator_line = e2.strip()
    m = re.match(r"^(.+\(莊春江譯\))(.+)$", translator_line)
    if m:
        translator_part = m.group(1)
        agama_part = m.group(2)
    else:
        translator_part = translator_line
        agama_part = None
    # todo
    _br = contents.pop(0)
    assert (isinstance(_br, xl.Element) and _br.tag == "br")

    _new_contents = []
    for e in contents:
        if e.tab == "div" and e.attrs["style"] == "display: none":
            continue
        elif e.tab == "span" and e.attrs["class"] == "sutra_name" and e.kids[0] == "相應部12相應83-93經/學經等（中略）十一則":
            _new_contents.append(e.kids[0])
        else:
            _new_contents.append(e)

    contents = _new_contents

    for oline in _clean_contents(contents):
        body_lines.append(_do_line(oline))

    return homage_and_head_lines, sutta_name_es, translator_part, agama_part, body_lines


def _split_homage_and_head(listline_list):
    homage_listline = None
    head_listline_list = []
    for listline in listline_list:
        if listline[0].startswith("對那位") and listline[-1].endswith("禮敬"):
            homage_listline = listline
        else:
            head_listline_list.append(listline)
    return homage_listline, head_listline_list



def listline_list_to_line_list(lsline_list):
    lines = []
    for lsline in lsline_list:
        line = ""
        for s in lsline:
            if isinstance(s, str):
                line += s
            elif isinstance(s, base.TextWithNoteRef):
                line += s.get_text()
            else:
                raise TypeError("Something Wrong!")
        lines.append(line)
    return lines
