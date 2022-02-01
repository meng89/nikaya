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


class Href(object):
    def __init__(self, text, href, target):
        self.text = text
        self.href = href
        self.target = target


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

    def get_text(self):
        return self._text


def read_page(url):
    soup, last_modified = read_url(url)

    div_nikaya_tag = soup.find("div", {"class": "nikaya"})
    pali_doc = soup.find("div", {"class": "pali"})

    homage_head_listline_list = None
    sutta_name_line = None
    body_listline_list = []
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
                            print("<CCC WARNING>: url: {}; -> not onmouseover: {}".format(url, x))
                        break

                type_ = None
                if m.group(1) == "note":
                    type_ = GLOBAL
                elif m.group(1) == "local":
                    type_ = LOCAL

                tnn = TextNeedNote(text=x.get_text(), number=m.group(2), type_=type_)
                current_line.append(tnn)

            # for CCC 原始 BUG
            elif x.name == "span" and x["class"] == ["sutra_name"] and x.get_text() == "相應部12相應83-93經/學經等（中略）十一則":
                current_line.append(x.get_text())
            # for checking
            elif x.name == "a" and "href" in x.attrs.keys():
                current_line.append(Href(text=x.get_text(), href=x["href"], target=x["target"]))
            elif x.name == "div" and x["style"] == "display: none":  # for CCC BUG， SN.46.43
                print("<CCC INFO>: url: {}; -> needless tag: {}".format(url, x))
                continue
            else:
                raise Exception("不能识别的Tag: {}; URL: {}".format(x, url))

    comp_doc = soup.find("div", {"class": "comp"})
    local_note_list = []
    if comp_doc is not None:
        note_docs = comp_doc.find_all("span", {"id": True})
        for x in note_docs:
            id_ = re.match(r"^note(\d+)$", x["id"]).group(1)
            local_note_list.append(LocalNote(type_=LOCAL, number=id_, note=x.get_text()))

    assert homage_head_listline_list is not None
    assert sutta_name_line is not None
    assert len(body_listline_list) > 0

    homage_listline, head_listline_list = separate_homage(homage_head_listline_list)
    head_line_list = listline_list_to_line_list(head_listline_list)

    if False:
        pprint(homage_listline)
        pprint(head_line_list)
        pprint(sutta_name_line)
        pprint(body_listline_list)
        pprint(local_note_list)

    return homage_listline, head_line_list, sutta_name_line, body_listline_list, pali_doc.text, last_modified


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
    last_modified = r.headers['last-modified']
    soup = bs4.BeautifulSoup(r.text, 'html5lib')
    return soup, last_modified


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


