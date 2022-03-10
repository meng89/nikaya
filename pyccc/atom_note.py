import re

import bs4
import requests.exceptions

from pyccc import atom, pdf, atom_suttaref, page_parsing, parse_note
from pyccc.parse_original_line import _do_line2, _do_line

LOCAL_NOTE_KEY_PREFIX = "x"

_global_notes = {}


def load_global(domain: str):
    global _global_notes
    for i in range(100):
        try:
            url_path = "/note/note{}.htm".format(i)
            soup = page_parsing.read_url(domain + url_path)[0]
        except requests.exceptions.HTTPError:
            break

        for div in soup.find_all(name="div", attrs={"id": True}):
            note_no = re.match(r"^div(\d+)$", div["id"]).group(1)
            # _global_notes[note_no] = separate(div.contents, base_url, {}, IndexedSet())
            _global_notes[note_no] = _do_globalnote2(list(div.contents), url_path=url_path)


# 断言：
# local note 没有 sub note；
# global note 不会引用其它 note；


def contents2lines(contents: list):
    lines = []
    line = []
    for e in contents:
        if isinstance(e, bs4.element.Tag) and e.name == "br":
            lines.append(line)
            line = []
        else:
            line.append(e)
    if line:
        lines.append(line)
    return lines


def _do_globalnote2(contents, **kwargs):
    lines = contents2lines(contents)
    parsed_lines = []
    for line in lines:
        parsed_lines.append(_do_subnote2(line, **kwargs))
    return parsed_lines


def _do_subnote2(ori_line, **kwargs):
    line = []
    first = ori_line.pop(0)
    assert isinstance(first, (str, bs4.element.NavigableString))
    m = re.match(r"^(?P<subkey>\(\d+\))?(:?(?P<agama>「.*?(?:SA|GA|MA|DA|AA).*?」)|(?P<nikaya>「.+?」))(?P<left>.*)$",
                 str(first))
    if not m:
        raise Exception((type(first), first))
    if m.group("subkey"):
        line.append(m.group("subkey"))
    if m.group("agama"):
        line.append(m.group("agama"))  # todo
    if m.group("nikaya"):
        line.append(m.group("nikaya"))  # todo
    if m.group("left"):
        ori_line.insert(0, m.group("left"))

    line.extend(_do_line2(olines=ori_line,
                          funs=[_do_note_xstr2, _do_href, _do_onmouseover_global, _do_onmouseover_local],
                          **kwargs))
    return line


def _do_globalnote(contents: list, **kwargs):
    note = {}

    while contents:
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
        subnote = _do_subnote(contents, **kwargs)
        note[subkey] = subnote

    return note


def _do_localnote(**kwargs):
    subnote, contents = _do_subnote(**kwargs)
    assert contents == []
    return subnote


def _do_subnote(contents: list, **kwargs):
    first = contents.pop(0)
    assert isinstance(first, (str, bs4.element.NavigableString))
    line = []
    text = str(first)
    m = re.match(r"^(「.*?(?:SA|GA|MA|DA|AA).*?」)(.*)$", text)
    if m:
        line.append(NoteKeywordAgama(m.group(1)))
        left_text = m.group(2)
    else:
        m = re.match(r"^(「.*?」)(.*)$", text)
        if m:
            line.append(NoteKeywordDefault(m.group(1)))
            left_text = m.group(2)
        else:
            left_text = text

    contents.insert(0, left_text)
    left_line = _do_line(contents=contents,
                         funs=[_do_note_xstr2, _do_href, _do_onmouseover_global, _do_onmouseover_local],
                         **kwargs)
    return line + left_line


class NoteKeywordDefault(object):
    def __init__(self, text):
        self.text = text
        self._tex_cmd = "notekeyworddefault"

    def get_text(self):
        return self.text

    def _contents(self):
        return atom_suttaref.parse(self.text)

    def to_tex(self, bns, t):
        return "\\" + self._tex_cmd + "{" + pdf.join_to_tex(line=self._contents(), bns=bns, c=t) + "}"


class NoteKeywordNikaya(NoteKeywordDefault):
    def __init__(self, text):
        super().__init__(text)
        self._tex_cmd = "notekeywordnikaya"


class NoteKeywordAgama(NoteKeywordDefault):
    def __init__(self, text):
        super().__init__(text)
        self._tex_cmd = "notekeywordagama"


def ___do_lines(contents, funs, **kwargs):
    lines = []
    while contents:
        listline, contents = _do_line(contents, funs, **kwargs)
        lines.append(listline)
    return lines


def _do_note_xstr2(e, **kwargs):
    if isinstance(e, (str, bs4.element.NavigableString)):
        return True, parse_note.split_str(str(e).strip("\n"))
    else:
        return False, None


def _do_note_xstr(e, **kwargs):
    line = []
    if isinstance(e, (str, bs4.element.NavigableString)):
        m = re.match(r"^(.*南傳作)(「.*?」)(.*)$", str(e).strip("\n"))
        if m:
            line.extend(atom_suttaref.parse(m.group(1)))
            line.append(NoteKeywordNikaya(m.group(2)))
            line.extend(atom_suttaref.parse(m.group(3)))

        else:
            line.extend(atom_suttaref.parse(str(e).strip("\n")))
        return True, line
    else:
        return False, e


def _do_xstr(e, **kwargs):
    if isinstance(e, (str, bs4.element.NavigableString)):
        return True, atom_suttaref.parse(str(e).strip("\n"))
    else:
        return False, e


def _do_href(e, url_path, **kwargs):
    if e.name == "a" and "href" in e.attrs.keys():
        return True, [atom.Href(text=e.get_text(), href=e["href"], base_url_path=url_path, target=e["target"])]
    else:
        return False, e


def _do_onmouseover_global(e, url_path, **kwargs):
    if e.name == "a" and "onmouseover" in e.attrs.keys():
        m = re.match(r"^note\(this,(\d+)\);$", e["onmouseover"])
        if m:
            key = m.group(1)
            try:
                sub_note_key = match_key(key, e.get_text())

            except NoteNotMatch:
                page_parsing.ccc_bug(page_parsing.WARNING, url_path,
                                     "辞汇 \"{}\" 未匹配全局注解编号 \"{}\"".format(e.get_text(), key))
                sub_note_key = (key, list(get()[key].keys())[0])

            return True, [atom.TextWithNoteRef(text=e.get_text(), key=sub_note_key, type_=page_parsing.GLOBAL)]
    # ccc bug
    elif e.name == "a" and "nmouseover" in e.attrs.keys():
        return True, [e.get_text()]

    return False, e


def _do_onmouseover_local(e, url_path, sutta_temp_notes, local_notes):
    if e.name == "a" and "onmouseover" in e.attrs.keys():
        m = re.match(r"^local\(this,(\d+)\);$", e["onmouseover"])
        if m:
            key = m.group(1)

            try:
                _note = sutta_temp_notes[key]
                note = tuple(_note)
                # todo
            except KeyError:
                page_parsing.ccc_bug(page_parsing.WARNING, url_path, "未找到本地注解编号 \"{}\"".format(key))
                x = e.get_text()
            else:
                local_notes.add(note)
                k = local_notes.index(note)
                # todo mathc
                x = atom.TextWithNoteRef(text=e.get_text(), key=k, type_=page_parsing.LOCAL)

            return True, [x]

    return False, e


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
        if text in pdf.join_to_text(subnote):
            return num, subnum

    raise NoteNotMatch((num, text))


def get():
    return _global_notes


def note_label(type_, key):
    if type_ == page_parsing.GLOBAL:
        return globalnote_label(key[0], key[1])
    else:
        return localnote_label(key)


def globalnote_label(notekey, subnotekey):
    return str(notekey) + "." + str(subnotekey).replace("(", "").replace(")", "")


def localnote_label(key):
    return LOCAL_NOTE_KEY_PREFIX + str(key)
