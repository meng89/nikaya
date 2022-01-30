import re

import bs4
import requests


class AnalyseError(Exception):
    pass



class LocalNote(object):
    """
    <span id="note1">「為了智與持念的程度」(ñāṇamattāya paṭissatimattāya)，智髻比丘長老英譯為「為僅夠的理解與深切注意」
    """
    def __init__(self, type_, num, note):
        self._type = type_
        self._num = num
        self._note = note

    def __repr__(self):
        return repr({"type": self._type, "No.": self._num, "text": self._note})


class NoteTypeLocal(object):
    pass
class NoteTypeGlobal(object):
    pass



class TextNeedNote(object):
    """<a onmouseover="note(this,1);">像這樣被我聽聞</a>"""
    def __init__(self, text, note_type, note_num):
        self._text = text
        self._note_type = note_type
        self._note_num = note_num

    def __repr__(self):
        return repr({"text": self._text, "type": self._note_type, "No.": self._note_num})


def read_sutta_page(url):

    soup, last_modified = read_url(url)

    div_nikaya_tag = soup.find("div", {"class": "nikaya"})
    pali_doc = soup.find("div", {"class": "pali"})

    x = []
    # input(div_nikaya_tag)
    line_list = []
    line = []
    for x in div_nikaya_tag.contents:
        if isinstance(x, bs4.element.NavigableString):
            line.append(x.get_text())

        if isinstance(x, bs4.element.Tag):
            if x.name == "span" and x["class"] == "sutra_name":
                line.append(x.get_text())

            elif x.name == "br":
                # 剔除行尾空白
                # if len(line) > 0:
                #   line.append(line.pop().rstrip())
                line_list.append(line)
                line = []

            elif x.name == "a" and x["onMouseover"] is not None:
                m = re.match(r"^(note|local)\(this,(\d+)\);$", x["onMouseover"])
                type_ = None
                if m.group(1) == "note":
                    type_ = NoteTypeGlobal
                elif m.group(1) == "local":
                    type_ = NoteTypeLocal

                tnn = TextNeedNote(text=x.get_text(), note_num=x.get_text(), note_type=type_)
                line.append(tnn)

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
            local_note_list.append(LocalNote(type_=NoteTypeLocal, num=id_, note=x.get_text()))

    return line_list, local_note_list, pali_doc.text, last_modified


def read_url(url: str) -> (bs4.BeautifulSoup, str):
    r = requests.get(url)
    if r.status_code == 404:
        r.raise_for_status()
    r.encoding = 'utf-8'
    last_modified = r.headers['last-modified']
    soup = bs4.BeautifulSoup(r.text, 'html5lib')
    return soup, last_modified
