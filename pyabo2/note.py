import os
import re
import math

import bs4

import xl

import config
import pyabo2.epub

htmls = ["note/note{}.htm".format(x) for x in range(10)]


def load_from_htm():
    for htm in htmls:
        pass


_gn = None

def get_gn():
    global _gn
    if _gn is None:
        _gn = GlobalNotes()
    return _gn



class GlobalNotes:
    def __init__(self):
        self.note_name = "全局註解"
        self._notes = {}

    @property
    def notes(self):
        if self._notes == {}:
            for html in htmls:
                data = open(os.path.join(config.DOWNLOAD_DIR, html), "r").read()
                soup = bs4.BeautifulSoup(data, 'html5lib')
                root = xl.parse(str(soup)).root
                for div in root.find_descendants("div"):
                    if div.tag == "div" and div.attrs.get("id") is not None:
                        m = re.match(r"^div(\d+)$", div.attrs.get("id"))
                        self._notes[m.group(1)] = div.kids
        return self._notes

    @staticmethod
    def _get_page_index(note_id):
        return math.ceil(int(note_id) / 100)

    def _get_page_path(self, note_id):
        return "note/note{}.xhtml".format(self._get_page_index(note_id))

    def get_link(self, note_id):
        return self._get_page_path(note_id) + "#{}".format(note_id)

    def get_es(self, note_id):
        return self.notes.get(note_id)

    def get_pages(self, lang):
        xhtmls = []
        last_page_path = None
        last_ol = None

        for note_id, note in self.notes.items():
            _path = self._get_page_path(note_id)
            if _path != last_page_path:
                last_page_path = _path
                title = self.note_name+"第{}页".format(self._get_page_index(note_id))
                html, body = pyabo2.epub.make_doc(last_page_path, lang, lang.c(title))
                h1 = body.ekid("h1")
                h1.kids.append(title)
                section = body.ekid("section")
                section.attrs["epub:type"] = "endnotes"
                section.attrs["role"] = "doc-endnotes"
                ol = section.ekid("ol")
                last_html = html
                last_ol = ol
                xhtmls.append((title, last_page_path, last_html))

            li = last_ol.ekid("li")
            li.attrs["id"] = note_id
            p = li.ekid("p")
            p.kids.extend(note)

        pages = []
        for title, path, xhtml in xhtmls:
            pages.append((title, path, xhtml.to_str()))

        return pages


    def write_epub(self):
        pass


class LocalNotes(GlobalNotes):
    def __init__(self):
        super().__init__()
        self.note_name = "全局註解"
        self._notes = {}

    @property
    def notes(self):
        return self._notes

    def add(self, note):
        _id = str(len(note) + 1)
        self.notes[_id] = note
        return self.get_link(_id)
