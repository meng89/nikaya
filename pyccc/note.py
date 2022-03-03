import re
import bs4
import requests.exceptions

from boltons.setutils import IndexedSet

import pyccc.suttaref
from . import utils

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
            _global_notes[note_no] = separate(div.contents, base_url, {}, IndexedSet())


# 断言：
# local note 没有 sub note；
# global note 不会引用其它 note；


def _do_note(contents: list):
    note = {}

    while True:
        first = contents.pop(0)
        assert isinstance(first, bs4.element.NavigableString)
        text = first.get_text()

        m = re.match(r"^(\(\d+\))(.*)$", text)
        if m:
            subkey = m.group(1)
            left = m.group(2)
        else:
            subkey = None
            left = text

        contents.insert(0, left)
        subnote, left = _do_subnote(contents)
        note[subkey] = subnote

        if not contents:
            break
        else:
            first = contents.pop()
            if first.name == "br":
                continue
    return note


def _do_subnote(contents: list):
    first = contents.pop(0)
    assert isinstance(first, bs4.element.NavigableString)
    text = first.get_text()
    m = re.match(r"^(「.*?」)(.*)$", text)
    if m:
        head = m.group(1)
        left_text = m.group(2)
    else:
        head = None
        left_text = text

    contents.insert(0, left_text)

    splited, left, = _do(contents)
    body = splited
    return SubNote(head, body), left


def _do_normal_lines(contents):
    lines = []
    listline = []

    for e in contents:
        if e.name == "br":
            lines.append(listline)
        else:
            answer, x = _do(e)
            if answer:
                listline.extend(x)
            else:
                raise TypeError(str(e))


def _do(e):
    funs = [_do_xstr, _do_href, _do_onmouseover]
    for fun in funs:
        answer, x = fun(e=e, url_path=url_path, temp_notes=temp_notes, localnotes=localnotes)
        if answer:
            return answer, x
    return False, None


def _do_xstr(e, args):
    if isinstance(e, bs4.element.NavigableString):
        return True, pyccc.suttaref.split_str(e.get_text())
    elif isinstance(e, str):
        return True, pyccc.suttaref.split_str(e)
    else:
        return False, e


def _do_href(e, url_path):
    if e.name == "a" and "href" in e.attrs.keys():
        return True, [pyccc.utils.do_href(e, url_path)]
    else:
        return False, e


def _do_onmouseover(e, url_path, temp_notes, local_notes):
    if e.name == "a" and "onmouseover" in e.attrs.keys():
        try:
            x = pyccc.utils.do_onmouseover_globalnote(e, url_path)
        except pyccc.utils.NoteLocaltionError:
            x, _local_notes = pyccc.utils.do_onmouseover_localnote(e, url_path, temp_notes, local_notes)

        return True, [x]
    else:
        return False, e


def separate(contents, url_path, temp_notes, local_notes):
    note = {}
    subkey = None
    subnote = SubNote(head=None, body=[])
    listline = []
    for e in contents:
        if isinstance(e, bs4.element.NavigableString) and subnote.body == []:
            text = e.get_text()
            m = re.match(r"^(「.*?」)(.*)$", text)
            if m:
                subnote.head = m.group(1)
                subnote.body = pyccc.suttaref.split_str(m.group(2))
                continue

            m = re.match(r"^(\(\d+\))(「.*?」)(.*)$", text)
            if m:
                subkey = m.group(1)
                subnote.head = m.group(2)
                subnote.body = pyccc.suttaref.split_str(m.group(3))
                continue

            subnote.head = None
            subnote.body = pyccc.suttaref.split_str(text)

        elif isinstance(e, bs4.element.NavigableString):
            subnote.body.extend(pyccc.suttaref.split_str(e.get_text()))

        elif e.name == "a" and "href" in e.attrs.keys():
            subnote.body.append(pyccc.utils.do_href(e, url_path))

        elif e.name == "a" and "onmouseover" in e.attrs.keys():
            try:
                x = pyccc.utils.do_onmouseover_globalnote(e, url_path)
            except pyccc.utils.NoteLocaltionError:
                x, _local_notes = pyccc.utils.do_onmouseover_localnote(e, url_path, temp_notes, local_notes)

            subnote.body.append(x)

        elif e.name == "br":
            note[subkey] = subnote
            subkey = None
            subnote = SubNote(head=None, body=[])

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
        if isinstance(e, pyccc.suttaref.SuttaRef):
            continue
        if text in e:
            return True
    return False


def get():
    return _global_notes
