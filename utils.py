import re

import bs4
import requests

from pprint import pprint


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


class TextNeedNote(object):
    """<a onmouseover="note(this,1);">像這樣被我聽聞</a>"""
    def __init__(self, text, type_, number):
        self._text = text
        self._type = type_
        self._number = number

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'text={self._text!r}, '
                f'type_={self._type!r}, '
                f'number={self._number!r})')


def read_sutta_page(url):

    soup, last_modified = read_url(url)

    div_nikaya_tag = soup.find("div", {"class": "nikaya"})
    pali_doc = soup.find("div", {"class": "pali"})

    head_lines = None
    sutta_name_line = None
    sutta_lines = []
    is_sutta_name_line_passed = True
    current_line = []
    for x in div_nikaya_tag.contents:

        if isinstance(x, bs4.element.NavigableString):
            s = "".join(x.get_text().splitlines())
            if is_sutta_name_line_passed:
                current_line.append(s)
            else:
                sutta_name_line += s
            continue

        if isinstance(x, bs4.element.Tag):
            if x.name == "span" and x["class"] == ["sutra_name"] and sutta_name_line is None:
                sutta_name_line = x.get_text()
                is_sutta_name_line_passed = False
                head_lines = sutta_lines
                sutta_lines = []

            elif x.name == "br":
                is_sutta_name_line_passed = True
                if current_line:
                    sutta_lines.append(current_line)
                    current_line = []

            elif x.name == "a" and x["onmouseover"] is not None:
                m = re.match(r"^(note|local)\(this,(\d+)\);$", x["onmouseover"])
                type_ = None
                if m.group(1) == "note":
                    type_ = GLOBAL
                elif m.group(1) == "local":
                    type_ = LOCAL

                tnn = TextNeedNote(text=x.get_text(), number=m.group(2), type_=type_)
                current_line.append(tnn)

            # for checking
            else:
                raise Exception("不能识别的Tag: {}\n"
                                "  URL: {}".format(x, url))

    comp_doc = soup.find("div", {"class": "comp"})
    local_note_list = []
    if comp_doc is not None:
        note_docs = comp_doc.find_all("span", {"id": True})
        for x in note_docs:
            id_ = re.match(r"^note(\d+)$", x["id"]).group(1)
            local_note_list.append(LocalNote(type_=LOCAL, number=id_, note=x.get_text()))

    pprint(head_lines)
    pprint(sutta_name_line)
    pprint(sutta_lines)
    pprint(local_note_list)
    assert head_lines is not None
    assert sutta_name_line is not None
    assert len(sutta_lines) > 0

    return head_lines, sutta_name_line, sutta_lines, pali_doc.text, last_modified


def read_url(url: str) -> (bs4.BeautifulSoup, str):
    r = requests.get(url)
    if r.status_code == 404:
        r.raise_for_status()
    r.encoding = 'utf-8'
    last_modified = r.headers['last-modified']
    soup = bs4.BeautifulSoup(r.text, 'html5lib')
    return soup, last_modified
