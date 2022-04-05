import re
import os
import pickle

import bs4
import requests.exceptions


from pyabo import base, page_parsing, base_note
import dopdf
from pyabo.parse_original_line import do_line

LOCAL_NOTE_KEY_PREFIX = "x"

_global_notes = {}
_is_loaded = False


def get():
    if _is_loaded:
        return _global_notes
    else:
        raise Exception


def load_global(domain: str, cache_dir):
    global _global_notes

    data_path = os.path.join(cache_dir, "globalnotes")
    try:
        with open(data_path, "rb") as rf:
            _global_notes = pickle.load(rf)
    except (FileNotFoundError, ModuleNotFoundError):
        for i in range(100):
            try:
                url_path = "/note/note{}.htm".format(i)
                soup = page_parsing.read_url(domain + url_path)[0]
            except requests.exceptions.HTTPError:
                break

            for div in soup.find_all(name="div", attrs={"id": True}):
                note_no = re.match(r"^div(\d+)$", div["id"]).group(1)
                _global_notes[note_no] = do_globalnote(list(div.contents), url_path=url_path)

        with open(data_path, "wb") as wf:
            pickle.dump(_global_notes, wf)
    global _is_loaded
    _is_loaded = True


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


def do_globalnote(contents, **kwargs):
    lines = contents2lines(contents)
    parsed_lines = []
    for line in lines:
        parsed_lines.append(do_subnote(line, **kwargs))
    return parsed_lines


def do_subnote(ori_line, **kwargs):
    line = []
    first = ori_line.pop(0)
    assert isinstance(first, (str, bs4.element.NavigableString))
    m = re.match(r"^(?P<subkey>\(\d+\))?(:?(?P<agama>「.*?(?:SA|GA|MA|DA|AA).*?」)|(?P<nikaya>「.+?」))(?P<left>.*)$",
                 str(first))
    if m:
        if m.group("subkey"):
            line.append(base_note.NoteSubKeyHead(m.group("subkey")))
        if m.group("agama"):
            line.append(base_note.NoteKeywordAgamaHead(m.group("agama")))
        if m.group("nikaya"):
            line.append(base_note.NoteKeywordNikayaHead(m.group("nikaya")))
        if m.group("left"):
            ori_line.insert(0, m.group("left"))
    else:  # 此為「攝頌」...
        ori_line.insert(0, first)

    line.extend(do_line(oline=ori_line,
                        funs=[do_note_str, do_href, do_onmouseover_global, do_onmouseover_local],
                        **kwargs))
    return line


def do_note_str(e, **_kwargs):
    if isinstance(e, (str, bs4.element.NavigableString)):
        return True, base_note.split_str(str(e).strip("\n"))
    else:
        return False, None


def do_str(e, **_kwargs):
    if isinstance(e, (str, bs4.element.NavigableString)):
        return True, [e.strip("\n")]
    else:
        return False, e


def do_href(e, url_path, **_kwargs):
    if e.name == "a" and "href" in e.attrs.keys():
        return True, [base.Href(text=e.get_text(), href=e["href"], base_url_path=url_path, target=e["target"])]
    else:
        return False, e


def do_onmouseover_global(e, url_path, **_kwargs):
    if e.name == "a" and "onmouseover" in e.attrs.keys():
        m = re.match(r"^note\(this,(\d+)\);$", e["onmouseover"])
        if m:
            key = m.group(1)
            try:
                sub_note_key = key_hit(key, e.get_text())

            except NoteNotMatch:
                page_parsing.ccc_bug(page_parsing.WARNING, url_path,
                                     "辞汇 \"{}\" 未匹配全局注解编号 \"{}\"".format(e.get_text(), key))
                sub_note_key = (key, 0)

            except NoteNotFound:
                page_parsing.ccc_bug(page_parsing.WARNING, url_path,
                                     "辞汇 \"{}\" 未找到全局注解编号 \"{}\"".format(e.get_text(), key))
                return True, [e.get_text()]

            return True, [base.TextWithNoteRef(text=e.get_text(), key=sub_note_key, type_=page_parsing.GLOBAL)]

    # ccc bug
    elif e.name == "a" and "nmouseover" in e.attrs.keys():
        return True, [e.get_text()]

    return False, e


def do_onmouseover_local(e, url_path, sutta_temp_notes, local_notes):
    if e.name == "a" and "onmouseover" in e.attrs.keys():
        m = re.match(r"^local\(this,(\d+)\);$", e["onmouseover"])
        if m:
            key = m.group(1)
            try:
                note = tuple(sutta_temp_notes[key])
            except KeyError:
                page_parsing.ccc_bug(page_parsing.WARNING, url_path, "未找到本地注解编号 \"{}\"".format(key))
                x = e.get_text()
            else:
                local_notes.add(note)
                k = local_notes.index(note)
                x = base.TextWithNoteRef(text=e.get_text(), key=k, type_=page_parsing.LOCAL)
            return True, [x]
    return False, e


class NoteNotMatch(Exception):
    pass


class NoteNotFound(Exception):
    pass


def key_hit(num, text, notes=None):
    if notes is None:
        _notes = _global_notes
    else:
        _notes = notes
    if num not in _notes.keys():
        raise NoteNotFound((num, text))

    for index in range(len(_notes[num])):
        if text in dopdf.join_to_text(_notes[num][index]):
            return num, index
    raise NoteNotMatch((num, text))


def match_key(num, text, notes=None):
    if notes is None:
        _notes = _global_notes
    else:
        _notes = notes
    if num not in _notes.keys():
        raise NoteNotMatch((num, text))

    for subnum, subnote in _notes[num].items():
        if text in dopdf.join_to_text(subnote):
            return num, subnum

    raise NoteNotMatch((num, text))


def note_to_texlabel(type_, key):
    if type_ == page_parsing.GLOBAL:
        return globalnote_to_texlabel(key[0], key[1])
    else:
        return localnote_to_texlabel(key)


def globalnote_to_texlabel(notekey, subnotekey):
    return str(notekey) + "." + str(subnotekey).replace("(", "").replace(")", "")


def localnote_to_texlabel(key):
    return LOCAL_NOTE_KEY_PREFIX + str(key)
