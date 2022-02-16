import re
import bs4
import requests.exceptions

from . import utils
from . import bookref

_global_notes = {}


class SubNote(object):
    def __init__(self, head: str, body: list):
        self.head = head
        self.body = body


def load_global(domain: str):
    global _global_notes
    for i in range(100):
        try:
            soup = utils.read_url(domain + "/note/note{}.htm".format(i))[0]
        except requests.exceptions.HTTPError:
            break

        for div in soup.find_all(name="div", attrs={"id": True}):
            note_no = re.match(r"^div(\d+)$", div["id"]).group(1)
            _global_notes[note_no] = separate(div.contents)


def separate(contents):
    dictsubnote = {}
    for one in contents:
        if isinstance(one, bs4.element.NavigableString):
            text = one.get_text()
            m = re.match(r"^「(.*?)」(.*)$", text)
            if m:
                dictsubnote["1"] = SubNote(head=m.group(1), body=bookref.split(m.group(2)))
                continue
            m = re.match(r"^\((\d)\)「(.*?)」(.*)$", text)
            if m:
                dictsubnote[m.group(1)] = SubNote(head=m.group(2), body=bookref.split(m.group(3)))
                continue
        elif one.name == "br":
            pass
        elif one.name == "a" and "href" in one.attrs.keys():
            assert Exception(contents)
            # cur_subnote.body.append(utils.Href(text=one.get_text(), href=one["href"], target=one["target"]))
    return dictsubnote


class NoteNotMatch(Exception):
    pass


def match_key(num, text, notes=None):
    notes = notes or _global_notes
    for subnum, subnote in notes[num]:
        if re.match(subnote.head, text) or re.match(subnote.body, text):
            return num, subnum
    assert NoteNotMatch


def get():
    return _global_notes
