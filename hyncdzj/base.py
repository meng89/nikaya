import shutil
import re
import os

from typing import List, Tuple, Union

import opencc

import xl


def to_sc(s):
    return opencc.OpenCC("t2s.json").convert(s)


def piece_key():
    from uuid import uuid4
    return str(uuid4())


class Meta:
    def __init__(self, e):
        self._e = e


class Metadata:
    def __init__(self, term=None):
        if isinstance(term, str):
            xml = xl.parse(term)
            self._meta = xml.root
        elif isinstance(term, xl.Element):
            self._meta = term
        else:
            self._meta = xl.Element("meta")

    def __bool__(self):
        return bool(self._meta.kids)

    def get_element(self):
        return self._meta

    def to_str(self, *args, **kwargs):
        return self._meta.to_str(*args, **kwargs)


_doc_dont_do_tags = ["p", "s", "note", "h1"]

def cover_element(old_e: xl.Element, cover_fun):
    new_e = xl.Element(cover_fun(old_e.tag))
    for key, value in old_e.attrs.items():
        new_e.attrs[cover_fun(key)] = cover_fun(value)

    for kid in old_e.kids:
        if isinstance(kid, xl.Element):
            new_kid = cover_element(kid, cover_fun)
        else:
            new_kid = cover_fun(kid)
        new_e.kids.append(new_kid)
    return new_e


# 原始转Python Object
def _split_note(body:xl.Element) -> tuple:
    new_body, notes_kids, _ = _split_note2(body, 1)
    notes = xl.Element("notes", kids=notes_kids)

    return new_body, notes

def _split_note2(e:xl.Element, note_index:int) -> tuple:
    if isinstance(e, xl.Element) and e.tag == "ewn":
        a = xl.Element("a")
        a.attrs["n"] = str(note_index)
        a.kids.extend(e.kids[0].kids)

        note = xl.Element("note")
        note.attrs["n"] = str(note_index)
        note.kids.extend(e.kids[1].kids)

        note_index += 1
        return a, [note], note_index

    elif isinstance(e, xl.Element):
        notes = []
        new_e = xl.Element(e.tag, e.attrs)
        for kid in e.kids:
            new_kid, new_notes, note_index = _split_note2(kid, note_index)
            new_e.kids.append(new_kid)
            notes.extend(new_notes)

        return new_e, notes, note_index

    else:
        return e, [], note_index


def human_to_machine(xml):
    _doc = xml.root
    body = _doc.find_kids("body")[0]
    notes = _doc.find_kids("notes")[0]
    ps = _doc.find_kids("ps")[0]

    new_body = _merge_note(body, notes)

    new_root = xl.Element("doc")
    new_xml = xl.Xml(new_root)
    new_root.kids.append(new_body)
    new_root.kids.append(ps)

    return new_xml


def _merge_note(e: xl.Element, notes):
    new_e = xl.Element(e.tag, attrs=e.attrs)
    for term in e.kids:
        if isinstance(term, xl.Element):
            if term.tag == "a" and "n" in term.attrs.keys():
                ewn = xl.Element("ewn")
                a = ewn.ekid("a")
                a.kids.extend(term.kids)

                note = _hit_note(notes, term.attrs["n"])
                ewn.kids.append(note)
            else:
                new_e.kids.append(_merge_note(term, notes))

        if isinstance(term, str):
            new_e.kids.append(term)
    return new_e

def _hit_note(notes, num):
    for note in notes:
        if note.attrs["n"] == num:
            new_note = xl.Element("note")
            new_note.kids.extend(note.kids)
            return new_note
    raise Exception


########################################################################################################################


def is_pts_ref(x):
    if isinstance(x, xl.Element):
        if x.tag == "ref":
            if "cRef" in x.attrs.keys():
                if re.match("^PTS", x.attrs["cRef"]):
                    if len(x.kids) == 0:
                        return True
    return False


def is_num_p(x):
    if isinstance(x, xl.Element):
        if x.tag == "p":
            if len(x.kids) == 1:
                if re.match(r"^[〇一二三四五六七八九十※～]+$", x.kids[0]):
                    return True
    return False


Entry = Tuple[str, Union[xl.Xml, List["Entry"]]]
Folder = List[Entry]


NameGroup = Tuple[int|None, int|None, str|None]

FullNameGroup = Tuple[int, int|None, int|None, str|None]


def fullnamegroup_to_filename(namegroup: FullNameGroup, index_width=0) -> str:
    file_index, start, end, name = namegroup
    if isinstance(start, int):
        assert isinstance(end, int)
        if start == end:
            range_ = str(start)
        else:
            range_ = str(start) + "-" + str(end)

    elif start is None:
        assert end is None
        range_ = ""
    else:
        raise Exception

    if name is None:
        name = ""

    if range_ == "" and  name == "":
        filename = ""
    elif range_ == "" and name != "":
        filename = name

    elif range_ != "" and name == "":
        filename = range_
    elif range_ != "" and name != "":
        filename = range_ + "." + name


    else:
        print(namegroup, repr(range_), repr(name))
        raise Exception

    file_name = f"{file_index:>0{index_width}}_{filename}"
    return file_name


def filename_to_namegroup(filename: str) -> FullNameGroup:
    if filename.endswith(".xml"):
        filename = filename[:-4]

    # 1_1.xxx
    m = re.match(r"(\d+)_(\d+)\.(.+)$", filename)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(2)), m.group(3)

    # 1_1
    m = re.match(r"(\d+)_(\d+)$", filename)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(2)), None


    # 1_1-2.xxx
    m = re.match(r"(\d+)_(\d+)-(\d+)\.(.+)$", filename)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)

    # 1_1-2
    m = re.match(r"(\d+)_(\d+)-(\d+)$", filename)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3)), None

    # 1_xxx
    m = re.match(r"(\d+)_(.+)$", filename)
    if m and True:
        return int(m.group(1)), None, None, m.group(2)

    # 1_
    m = re.match(r"(\d+)_$", filename)
    if m:
        return int(m.group(1)), None, None, None

    raise Exception(repr(filename))


def add_space_before_note(doc: xl.Element):
    for index, e in enumerate(doc.kids):
        if isinstance(e, xl.Element) and e.tag.startswith("n"):
            doc.kids.insert(index, " ")
            return


def write_to_disk(path, data: list):
    dont_do_tags = ["p", "sub"]
    for x in range(1, 1000):
        dont_do_tags.append("n" + str(x))

    if os.path.exists(path):
        shutil.rmtree(path)

    os.makedirs(path, exist_ok=True)
    width = len(str(len(data)))
    for i, (name_group, obj) in enumerate(data, 1):
        file_name = fullnamegroup_to_filename(tuple([i] + list(name_group)), width)
        sub_path = os.path.join(path, file_name)
        if isinstance(obj, list):
            write_to_disk(sub_path, obj)
        elif isinstance(obj, (xl.Xml, xl.Element)):
            add_space_before_note(obj)
            s = obj.to_str(do_pretty=True, try_self_closing=True, dont_do_tags=dont_do_tags)
            with open(sub_path + ".xml", "w") as f:
                f.write(s)
        else:
            raise Exception("wrong type:", type(obj))


def load_from_disk(path) -> list:
    data = []
    entries = os.listdir(path)
    entries.sort()
    for entry in entries:
        entry_path = os.path.join(path, entry)

        fullnamegroup = filename_to_namegroup(entry)

        if os.path.isdir(entry_path):
            v = load_from_disk(entry_path)
        elif os.path.isfile(entry_path):
            xml = xl.parse(open(entry_path, "r").read(),ignore_blank=True, unignore_blank_parent_tags=[""])
            v = xml.root
        else:
            raise Exception("Unknow File: {}".format(entry_path))
        data.append((fullnamegroup, v))

    return data



def split_file_serial_from_filename(name):
    x = re.match(r"^(\d+)_(.*?)(\.xml)?$", name).group(1)
    assert x is not None
    return x

def extract_filename_from_filename(name):
    x = re.match(r"^\d+_(.*?)(?:\.xml)?$", name).group(1)
    assert x is not None
    return x


def print_tree(data, indent=2):
    for namegroup, obj in data:
        print(" "*indent + repr(namegroup))
        if isinstance(obj, list):
            print_tree(obj, indent + 2)
