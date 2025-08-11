import os
import re
import math

import bs4

import xl

import config

htmls = ["note/note{}.htm".format(x) for x in range(10)]




def load_from_htm():
    for htm in htmls:
        pass


class GlobalNotes:
    def __init__(self):
        self.notes = {}
        for html in htmls:
            data = open(os.path.join(config.DOWNLOAD_DIR, html), "r").read()
            soup = bs4.BeautifulSoup(data, 'html5lib')
            root = xl.parse(str(soup)).root
            for div in root.find_descendants("div"):
                if div.tag == "div" and div.attrs.get("id") is not None:
                    m = re.match(r"^div(\d+)$", div.attrs.get("id"))
                    self.notes[m.group(1)] = div.kids

    @staticmethod
    def get_link(note_id):
        page_index = math.ceil(int(note_id) / 100)
        return "note/note{}.htm#note{}".format(page_index, note_id)

    def get_es(self, note_id):
        return self.notes.get(note_id)

    def write_epub(self):
        pass
