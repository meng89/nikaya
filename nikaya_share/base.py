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
        raise Exception(type(start), type(end))

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


ABO_WRITE_DONT_DO_TAGS = ["source_page", "sutta_num", "start", "end", "name", "mtime", "ctime", "relevant", "p", "note", "title", "source_title"]

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
            s = obj.to_str(do_pretty=True, try_self_closing=True, dont_do_tags=dont_do_tags + ABO_WRITE_DONT_DO_TAGS)
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
