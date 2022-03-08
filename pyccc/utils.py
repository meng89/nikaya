import re
import os
import bs4
import requests
from urllib.parse import urlparse, urljoin

from dateutil.parser import parse as parsedate

import pyccc.note
import pyccc.pdf
import pyccc.suttaref

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CACHE_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, "cache"))
os.makedirs(CACHE_DIR, exist_ok=True)

CCC_WEBSITE = "https://agama.buddhason.org"


class AnalyseError(Exception):
    pass


LOCAL = "LOCAL"
GLOBAL = "GLOBAL"


def _no_translate(x: str):
    return x


no_translate = _no_translate


class Href(object):
    def __init__(self, text, href, base_url_path, target):
        self.text = text
        self.href = href
        self.base_url_path = base_url_path
        self.target = target

    def get_text(self):
        return self.text

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'text={self.text!r}, '
                f'href={self.href!r}, '
                f'base={self.base_url_path!r}, '
                f'target={self.target!r})')

    def to_tex(self, t):
        url = urljoin(CCC_WEBSITE, urljoin(self.base_url_path, self.href))
        return "\\ccchref{" + url + "}{" + t(self.text) + "}"


class TextWithNoteRef(object):
    """<a onmouseover="note(this,1);">像這樣被我聽聞</a>"""

    def __init__(self, text, type_, key):
        self.text = text
        self.type_ = type_
        self.key = key

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'text={self.text!r}, '
                f'type_={self.type_!r}, '
                f'number={self.key!r})')

    def to_tex(self, t):
        return "\\twnr" +\
               "{" + t(self.get_text()) + "}" + \
               "{" + pyccc.pdf.note_label(self.type_, self.key) + "}"

    def get_text(self):
        return self.text

    def get_type(self):
        return self.type_

    def get_number(self):
        return self.key


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
                note = pyccc.note._do_subnote2(contents=list(e.contents), sutta_temp_notes=sutta_temp_notes, **kwargs)
                sutta_temp_notes[_key] = note
    return sutta_temp_notes


def _do_class_nikaya(contents, **kwargs):
    # is_sutta_name_line_passed = False
    homage_and_head_lines = []
    sutta_name_part = None
    translator_part = None
    body_lines = []

    def _do_line():
        return pyccc.note._do_line(contents=contents,
                                   funs=[pyccc.note._do_xstr, pyccc.note._do_href,
                                         pyccc.note._do_onmouseover_global, pyccc.note._do_onmouseover_local],
                                   **kwargs)

    while contents:
        if contents[0].name == "span" and contents[0]["class"] == ["sutra_name"]:
            e = contents.pop(0)
            sutta_name_part = e.get_text().strip("\n")
            _line = _do_line()
            if _line:
                assert len(_line) == 1
                translator_part = _line[0]
            break
        else:
            line = _do_line()
            if line:
                homage_and_head_lines.append(line)

    contents = [e for e in contents if not (isinstance(e, bs4.element.Tag) and e.name == "div")]
    while contents:
        if contents[0].name == "div" and contents[0]["style"] == "display: none":
            contents.pop(0)
            continue
        elif contents[0].name == "span" and contents[0]["class"] == ["sutra_name"] \
                and contents[0].get_text() == "相應部12相應83-93經/學經等（中略）十一則":
            e = contents.pop(0)
            body_lines.append(e.get_text())
            continue

        line = _do_line()
        if line:
            body_lines.append(line)

    return homage_and_head_lines, sutta_name_part, translator_part, body_lines


def _split_homage_and_head(listline_list):
    homage_listline = None
    head_listline_list = []
    for listline in listline_list:
        if listline[0] == "對那位" and listline[-1] == "禮敬":
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
            elif isinstance(s, TextWithNoteRef):
                line += s.get_text()
            else:
                raise TypeError("Something Wrong!")
        lines.append(line)
    return lines


def _do_href(e, url_path):
    return
