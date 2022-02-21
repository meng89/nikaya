import re
import bs4
import requests.exceptions

import pyccc.bookref
from . import utils
from . import bookref

_global_notes = {}


class SubNote(object):
    def __init__(self, head: str or None, body: list):
        self.head = head
        self.body = body

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'head={self.head!r}, '
                f'body={self.body!r})')


def load_global(domain: str):
    global _global_notes
    for i in range(100):
        try:
            base_url = "/note/note{}.htm".format(i)
            soup = utils.read_url(domain + base_url)[0]
        except requests.exceptions.HTTPError:
            break

        for div in soup.find_all(name="div", attrs={"id": True}):
            note_no = re.match(r"^div(\d+)$", div["id"]).group(1)
            _global_notes[note_no] = separate(div.contents, base_url)


def separate(contents, base_url):
    note = {}
    subkey = None
    subnote = SubNote(head=None, body=[])
    listline=[]
    for e in contents:
        if isinstance(e, bs4.element.NavigableString) and subnote.body == []:
            text = e.get_text()
            m = re.match(r"^「(.*?)」(.*)$", text)
            if m:
                subnote.head = m.group(1)
                subnote.body = bookref.split_str(m.group(2))
                continue

            m = re.match(r"^\((\d)\)「(.*?)」(.*)$", text)
            if m:
                subkey = m.group(1)
                subnote.head = m.group(2)
                subnote.body = bookref.split_str(m.group(3))
                continue

            subnote.head = None
            subnote.body = bookref.split_str(text)

        elif isinstance(e, bs4.element.NavigableString):
            subnote.body.extend(bookref.split_str(e.get_text()))

        elif e.name == "a" and "href" in e.attrs.keys():
            subnote.body.append(utils.Href(text=e.get_text(), href=e["href"], base_url_path=base_url,
                                           target=e["target"]))

        elif e.name == "br":
            note[subkey] = subnote
            subkey = None
            subnote = SubNote(head=None, body=[])

        elif e.name == "a" and "onmouseover" in e.attrs.keys():

        else:
            raise TypeError(str(e))

    if subnote.body:
        note[subkey] = subnote

    return note


class NoteNotMatch(Exception):
    pass


def match_key(num, text, notes=None):
    if notes is None:
        _notes = _global_notes
    else:
        _notes = notes
    if num not in _notes.keys():
        raise NoteNotMatch((num, text))

    for subnum, subnote in _notes[num].items():
        if (subnote.head is not None and text in subnote.head) or _in_list(text, subnote.body):
            return num, subnum

    raise NoteNotMatch((num, text))


def _in_list(text, body):
    for e in body:
        if isinstance(e, pyccc.bookref.BookRef):
            continue
        if text in e:
            return True
    return False


def get():
    return _global_notes
