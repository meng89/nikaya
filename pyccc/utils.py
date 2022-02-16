import re
import os
import bs4
import requests
from urllib.parse import urlparse

from dateutil.parser import parse as parsedate

import pyccc.note

PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CACHE_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, "cache"))
os.makedirs(CACHE_DIR, exist_ok=True)

CCC_WEBSITE = "https://agama.buddhason.org"


class AnalyseError(Exception):
    pass


class LocalNote(object):
    """
    <span id="note1">「為了智與持念的程度」(ñāṇamattāya paṭissatimattāya)，智髻比丘長老英譯為「為僅夠的理解與深切注意」
    """

    def __init__(self, type_, number, note):
        self._type = type_
        self._number = number
        self._note = note

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'type_={self._type!r}, '
                f'number={self._number!r}, '
                f'note={self._note!r})')


LOCAL = "LOCAL"
GLOBAL = "GLOBAL"


def _no_translate(x: str):
    return x


no_translate = _no_translate


class Href(object):
    def __init__(self, text, href, target):
        self.text = text
        self.href = href
        self.target = target

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'text={self.text!r}, '
                f'href={self.href!r}, '
                f'target={self.target!r})')


class TextNeedNote(object):
    """<a onmouseover="note(this,1);">像這樣被我聽聞</a>"""

    def __init__(self, text, type_, key):
        self._text = text
        self._type = type_
        self._key = key

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'text={self._text!r}, '
                f'type_={self._type!r}, '
                f'number={self._key!r})')

    def get_text(self):
        return self._text

    def get_type(self):
        return self._type

    def get_number(self):
        return self._key


WARNING = "WARNING"
INFO = "INFO"


def ccc_bug(type_, url, string):
    s = "<CCC {}>: url: {}, msg: {}".format(type_, url, string)
    print(s)


def read_page(url):
    url_path = urlparse(url).path

    soup, last_modified = read_url(url)

    pali_doc = soup.find("div", {"class": "pali"})

    homage_head_listline_list = None
    sutta_name_line = None
    body_listline_list = []
    is_sutta_name_line_passed = True
    current_line = []
    local_notes = {}
    local_notes_keys = []  # 检查 bug 用

    comp_doc = soup.find("div", {"class": "comp"})
    if comp_doc is not None:
        note_docs = comp_doc.find_all("span", {"id": True})
        for x in note_docs:
            key = re.match(r"^note(\d+)$", x["id"]).group(1)
            if key in local_notes.keys():
                ccc_bug(WARNING, url_path, "本地注解 KEY 冲突，key: {}, 自动加1，不知对错".format(key))
                key = str(int(key) + 1)

            n = pyccc.note.separate(x.contents)
            if n:
                local_notes[key] = n

    div_nikaya_tag = soup.find("div", {"class": "nikaya"})
    for x in div_nikaya_tag.contents:
        if isinstance(x, bs4.element.NavigableString):
            s = "".join(x.get_text().splitlines())
            if is_sutta_name_line_passed:
                current_line.append(s)
            else:
                sutta_name_line += s
            continue

        if isinstance(x, bs4.element.Tag):
            _onmouseover = "onmouseover"  # for CCC BUG
            _nmouseover = "nmouseover"  # for CCC BUG

            if x.name == "span" and x["class"] == ["sutra_name"] and sutta_name_line is None:
                sutta_name_line = x.get_text()
                is_sutta_name_line_passed = False
                homage_head_listline_list = body_listline_list
                body_listline_list = []

            elif x.name == "br":
                is_sutta_name_line_passed = True
                if current_line:
                    body_listline_list.append(current_line)
                    current_line = []

            # elif x.name == "a" and x["onmouseover"] is not None:
            elif x.name == "a" and (_onmouseover in x.attrs.keys() or _nmouseover in x.attrs.keys()):
                m = None
                for xmouserver in (_onmouseover, _nmouseover):
                    if xmouserver in x.attrs.keys():
                        m = re.match(r"^(note|local)\(this,(\d+)\);$", x[xmouserver])
                        if xmouserver == "nmouseover":  # for CCC BUG
                            ccc_bug(WARNING, url_path, "not onmouseover:" + str(x))
                        break

                if m.group(1) == "note":
                    tnn = TextNeedNote(text=x.get_text(), key=pyccc.note.match_key(m.group(2), x.get_text()),
                                       type_=GLOBAL)
                    current_line.append(tnn)

                elif m.group(1) == "local":

                    try:
                        key = pyccc.note.match_key(m.group(2), x.get_text(), local_notes)
                        tnn = TextNeedNote(text=x.get_text(), key=key, type_=LOCAL)
                        local_notes_keys.append(key)
                        current_line.append(tnn)
                    except pyccc.note.NoteNotMatch:
                        current_line.append(x.get_text())

            # for CCC 原始 BUG
            elif x.name == "span" and x["class"] == ["sutra_name"] and x.get_text() == "相應部12相應83-93經/學經等（中略）十一則":
                current_line.append(x.get_text())
            # for checking
            elif x.name == "a" and "href" in x.attrs.keys():
                current_line.append(Href(text=x.get_text(), href=x["href"], target=x["target"]))
            elif x.name == "div" and x["style"] == "display: none":  # for CCC BUG， SN.46.43
                ccc_bug(INFO, url_path, "needless tag: " + str(x))
                continue
            else:
                raise Exception("不能识别的Tag: {}; URL: {}".format(x, url))

    # 检查本地注解key 是否相同：
    no_note_keys = set(local_notes_keys) - set(local_notes.keys())
    if no_note_keys:
        ccc_bug(WARNING, url, "丢失note：{}".format(list(no_note_keys)))

    assert homage_head_listline_list is not None
    assert sutta_name_line is not None
    assert len(body_listline_list) > 0

    homage_listline, head_listline_list = separate_homage(homage_head_listline_list)
    head_line_list = listline_list_to_line_list(head_listline_list)

    return (homage_listline, head_line_list, sutta_name_line, body_listline_list, local_notes,
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
            elif isinstance(s, TextNeedNote):
                line += s.get_text()
            else:
                raise TypeError("Something Wrong!")
        lines.append(line)
    return lines
