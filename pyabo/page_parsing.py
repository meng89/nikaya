import re
import bs4
import requests
from urllib.parse import urlparse

from dateutil.parser import parse as parsedate

import pyabo.parse_original_line
from pyabo import base, note_thing


class AnalyseError(Exception):
    pass


LOCAL = "LOCAL"
GLOBAL = "GLOBAL"


def _no_translate(x: str):
    return x


no_translate = _no_translate

WARNING = "WARNING"
INFO = "INFO"


def ccc_bug(type_, url, string):
    s = "<CCC {}>: url: {}, msg: {}".format(type_, url, string)
    print(s)


def read_page(url, local_notes):
    url_path = urlparse(url).path
    soup, last_modified = read_url(url)
    pali_doc = soup.find("div", {"class": "pali"}).text
    sutta_temp_notes = _do_class_comp(soup.find("div", {"class": "comp"}),
                                      url_path=url_path, local_notes=local_notes)

    homage_and_head_lines, sutta_name_part, translator_part, body_lines = \
        _do_class_nikaya(list(soup.find("div", {"class": "nikaya"}).contents),
                         url_path=url_path, sutta_temp_notes=sutta_temp_notes, local_notes=local_notes)

    homage_line, _head_lines = _split_homage_and_head(homage_and_head_lines)
    head_lines = listline_list_to_line_list(_head_lines)

    return (homage_line, head_lines, sutta_name_part, translator_part,
            body_lines, pali_doc, last_modified)


def _do_class_comp(comp_doc, **kwargs):
    sutta_temp_notes = {}
    if comp_doc is not None:
        note_docs = comp_doc.find_all("span", {"id": True})
        for e in note_docs:
            _key = re.match(r"^note(\d+)$", e["id"]).group(1)
            if list(e.contents):
                for ori_line in note_thing.contents2lines(e.contents):
                    note = note_thing.do_subnote(ori_line=ori_line, sutta_temp_notes=sutta_temp_notes, **kwargs)
                    sutta_temp_notes[_key] = note
    return sutta_temp_notes


def _do_class_nikaya(contents, **kwargs):
    homage_and_head_oline = []
    homage_and_head_olines = []

    sutta_name_part = None
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
        if e.name == "span" and e["class"] == ["sutra_name"]:
            sutta_name_part = e.get_text()
            break
        elif isinstance(e, bs4.element.Tag) and e.name == "br":
            homage_and_head_olines.append(homage_and_head_oline)
            homage_and_head_oline = []
        else:
            homage_and_head_oline.append(e)
    if homage_and_head_oline:
        homage_and_head_olines.append(homage_and_head_oline)

    homage_and_head_lines = [_do_line(_oline) for _oline in homage_and_head_olines]

    e2 = contents.pop(0)
    assert isinstance(e2, bs4.element.NavigableString)
    translator_part = e2.get_text().strip("\n")
    _br = contents.pop(0)
    assert (isinstance(_br, bs4.element.Tag) and _br.name == "br")

    _new_contents = []
    for e in contents:
        if e.name == "div" and e["style"] == "display: none":
            continue
        elif e.name == "span" and e["class"] == ["sutra_name"] \
                and e.get_text() == "相應部12相應83-93經/學經等（中略）十一則":
            _new_contents.append(e.get_text())
        else:
            _new_contents.append(e)

    contents = _new_contents

    for oline in note_thing.contents2lines(contents):
        body_lines.append(_do_line(oline))

    return homage_and_head_lines, sutta_name_part, translator_part, body_lines


def _split_homage_and_head(listline_list):
    homage_listline = None
    head_listline_list = []
    for listline in listline_list:
        if listline[0].startswith("對那位") and listline[-1].endswith("禮敬"):
            homage_listline = listline
        else:
            head_listline_list.append(listline)
    return homage_listline, head_listline_list


def read_url(url: str) -> (bs4.BeautifulSoup, str):
    r = requests.get(url)
    if r.status_code == 404:
        r.raise_for_status()
    r.encoding = 'utf-8'
    last_modified = parsedate(r.headers['last-modified'])
    soup = bs4.BeautifulSoup(r.text, 'html5lib')
    return soup, last_modified


def lm_to_strdate(last_modified):
    return last_modified.strftime("%Y-%m-%d")


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
