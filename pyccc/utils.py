import re
import os
import bs4
import requests
from urllib.parse import urlparse, urljoin

from dateutil.parser import parse as parsedate

import pyccc.note
import pyccc.pdf
import pyccc.bookref

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

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'text={self.text!r}, '
                f'href={self.href!r}, '
                f'base={self.base_url_path!r}, '
                f'target={self.target!r})')

    def to_latex(self):
        url = urljoin(CCC_WEBSITE, urljoin(self.base_url_path, self.href))
        return "\\cccref{" + url + "}{" + self.text + "}"


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

    def to_latex(self, t):
        return ("\\twnr" +
                "{" + t(self.get_text()) + "}" +
                "{" + pyccc.pdf.note_label(self.type_, self.key[0], self.key[1]) + "}")

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


def read_page(url, book_notes):
    new_book_notes = book_notes
    try:
        last_key = list(book_notes.keys())[-1]
    except IndexError:
        last_key = 0

    url_path = urlparse(url).path

    soup, last_modified = read_url(url)

    # 巴利经文
    pali_doc = soup.find("div", {"class": "pali"})

    homage_head_listline_list = None
    sutta_name_line = None
    body_listline_list = []
    is_sutta_name_line_passed = True
    current_line = []
    # local_notes = {}

    new_local_notes_key_point = 0

    # 本地notes
    comp_doc = soup.find("div", {"class": "comp"})
    if comp_doc is not None:
        note_docs = comp_doc.find_all("span", {"id": True})
        for e in note_docs:
            _key = re.match(r"^note(\d+)$", e["id"]).group(1)
            key = last_key + int(_key)
            n = pyccc.note.separate(contents=e.contents, url_path=url_path, notes=new_book_notes, last_key=last_key)
            if n:
                new_book_notes[key] = n

    # 汉译经文
    div_nikaya_tag = soup.find("div", {"class": "nikaya"})
    for e in div_nikaya_tag.contents:
        if isinstance(e, bs4.element.NavigableString):
            ss = pyccc.bookref.split_str(e.get_text().strip("\n"))
            if is_sutta_name_line_passed:
                current_line.extend(ss)
            else:
                sutta_name_line += e.get_text()
            continue

        if isinstance(e, bs4.element.Tag):
            if e.name == "span" and e["class"] == ["sutra_name"] and sutta_name_line is None:
                sutta_name_line = e.get_text()
                is_sutta_name_line_passed = False
                homage_head_listline_list = body_listline_list
                body_listline_list = []

            elif e.name == "br":
                is_sutta_name_line_passed = True
                if current_line:
                    body_listline_list.append(current_line)
                    current_line = []

            elif e.name == "a" and "nmouseover" in e.attrs.keys():  # ccc bug
                current_line.append(e.get_text())

            elif e.name == "a" and "onmouseover" in e.attrs.keys():
                current_line.append(do_onmouseover(e, url_path, new_book_notes, last_key))

            # for CCC 原始 BUG
            elif e.name == "span" and e["class"] == ["sutra_name"] and e.get_text() == "相應部12相應83-93經/學經等（中略）十一則":
                current_line.append(e.get_text())
            # for checking
            elif e.name == "a" and "href" in e.attrs.keys():
                current_line.append(do_href(e, url_path))
            elif e.name == "div" and e["style"] == "display: none":  # for CCC BUG， SN.46.43
                pass
            else:
                raise Exception("不能识别的Tag: {}; URL: {}".format(e, url))

    assert homage_head_listline_list is not None
    assert sutta_name_line is not None
    assert len(body_listline_list) > 0

    homage_listline, head_listline_list = separate_homage(homage_head_listline_list)
    head_line_list = listline_list_to_line_list(head_listline_list)

    return (homage_listline, head_line_list, sutta_name_line, body_listline_list, new_book_notes,
            pali_doc.text, last_modified)


def separate_homage(listline_list):
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


def do_href(e, url_path):
    return Href(text=e.get_text(), href=e["href"], base_url_path=url_path, target=e["target"])


def do_onmouseover(e, url_path, book_notes, last_key):
    x = None
    m = re.match(r"^(note|local)\(this,(\d+)\);$", e["onmouseover"])
    _noteid = m.group(2)
    if m.group(1) == "note":
        noteid = _noteid
        try:
            x = TextWithNoteRef(text=e.get_text(), key=pyccc.note.match_key(noteid, e.get_text()), type_=GLOBAL)
        except pyccc.note.NoteNotMatch:
            ccc_bug(WARNING, url_path, "辞汇 \"{}\" 未匹配全局注解编号 \"{}\"".format(e.get_text(), noteid))
            x = TextWithNoteRef(text=e.get_text(), key=(noteid, list(pyccc.note.get()[noteid].keys())[0]), type_=GLOBAL)

    elif m.group(1) == "local":
        noteid = last_key + int(_noteid)
        try:
            key = pyccc.note.match_key(noteid, e.get_text(), book_notes)
            x = TextWithNoteRef(text=e.get_text(), key=key, type_=LOCAL)
        except pyccc.note.NoteNotMatch:
            ccc_bug(WARNING, url_path, "辞汇 \"{}\" 未匹配本地注解编号 \"{}\"".format(e.get_text(), noteid))
            try:
                x = TextWithNoteRef(text=e.get_text(), key=(noteid, list(book_notes[noteid].keys())[0]), type_=LOCAL)
            except KeyError:
                ccc_bug(WARNING, url_path, "未找到本地注解编号 \"{}\"".format(noteid))
                x = e.get_text()

    return x
