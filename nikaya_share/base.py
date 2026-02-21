import dataclasses
import os
import shutil
import re
from typing import List, Tuple, Union

import xl


@dataclasses.dataclass
class Info:
    # 汉语名
    name: str
    # 巴利语名
    pali: str
    # 译者
    translators: tuple[str, ...]
    # xml-p5a 路径 “N07/N07n0004.xml” 之 “4”,
    serial: int | None = None
    # 缩写
    abbr: str = None
    # 原作者
    authors: tuple[tuple, ...] = None
    # abo htmls
    htmls: list | None = None


NameGroup = Tuple[int|None, int|None, str|None]

FullNameGroup = Tuple[int, int|None, int|None, str|None]


def namegroup_to_filename(namegroup: NameGroup) -> str:
    start, end, name = namegroup
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
        raise Exception(start, end)

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

    return filename


def filename_to_namegroup(filename: str) -> NameGroup:
    if filename.endswith(".xml"):
        filename = filename[:-4]

    # 1_1.xxx
    m = re.match(r"(\d+)_(\d+)\.(.+)$", filename)
    if m:
        return int(m.group(2)), int(m.group(2)), m.group(3)

    # 1_1
    m = re.match(r"(\d+)_(\d+)$", filename)
    if m:
        return int(m.group(2)), int(m.group(2)), None


    # 1_1-2.xxx
    m = re.match(r"(\d+)_(\d+)-(\d+)\.(.+)$", filename)
    if m:
        return int(m.group(2)), int(m.group(3)), m.group(4)

    # 1_1-2
    m = re.match(r"(\d+)_(\d+)-(\d+)$", filename)
    if m:
        return int(m.group(2)), int(m.group(3)), None

    # 1_xxx
    m = re.match(r"(\d+)_(.+)$", filename)
    if m and True:
        return None, None, m.group(2)

    # 1_
    m = re.match(r"(\d+)_$", filename)
    if m:
        return None, None, None

    raise Exception(repr(filename))


def add_space_before_note(doc: xl.Element):
    new_doc = xl.Element(doc.tag)
    for index, e in enumerate(doc.kids):
        if isinstance(e, xl.Element) and e.tag == "n1":
            new_doc.kids.insert(index, " ")
        new_doc.kids.append(e)

    return new_doc



ABO_WRITE_DONT_DO_TAGS = ["source_page", "sutta_num", "start", "end", "name", "mtime", "ctime", "relevant", "p", "note", "title", "source_title"]

def write_to_disk(path, data: list):
    dont_do_tags = ["p", "sub"]
    for x in range(1, 1000):
        dont_do_tags.append("n" + str(x))

    if os.path.exists(path):
        shutil.rmtree(path)

    os.makedirs(path, exist_ok=True)
    width = len(str(len(data)))
    for index, (name_group, obj) in enumerate(data, 1):
        file_name = namegroup_to_filename(name_group)
        file_name = f"{index:>0{width}}_{file_name}"
        sub_path = os.path.join(path, file_name)
        if isinstance(obj, list):
            write_to_disk(sub_path, obj)
        elif isinstance(obj, (xl.Xml, xl.Element)):
            new_obj = add_space_before_note(obj)
            s = new_obj.to_str(do_pretty=True, try_self_closing=True, dont_do_tags=dont_do_tags + ABO_WRITE_DONT_DO_TAGS)
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
            xml = xl.parse(open(entry_path, "r").read(), ignore_blank=True, unignore_blank_parent_tags=[""])
            v = xml.root
        else:
            raise Exception("Unknow File: {}".format(entry_path))
        data.append((fullnamegroup, v))

    return data
