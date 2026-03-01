import dataclasses
import os
import shutil
import re
from typing import Tuple

import opencc

import xl


ABO = 1
HYNCDZJ = 2


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


# 汉译南传大藏经里有这些生僻字，一些字体里不包含，所以这里做转化

MAP = {
    "缠𦈐": "缠缚",
    "如丝之所𦈐": "如丝之所连",
    "如丝之𦈐": "如丝之连",
    "𦈐结": "连结",
    "𦈐系": "连系",
    "说之𦈐": "说之连",
    "其发𦈐而中入尸体": "其发连而中入尸体",
    "令断贪瞋痴慢见之𦈐": "令断贪瞋痴慢见之连",
    "𦈐平坦之道如竹之屈曲": "连平坦之道如竹之屈曲",
    "𦈐锁": "连锁",
    "𦈐发者": "结发者",
    "丝所𦈐": "丝所连",
    "𦈐丝": "连丝",
    "𦈐之丝": "连之丝",
    "此如𦈐索之众生": "此如连索之众生",

    "𪎊": "麨",
    "𨱎": "鍮",
    "𪸩": "辉",

    "𨅬": "躏",

    "𫟃婆": "纴婆",
    "饮𫍢": "饮饶",
    "盾𫓴": "盾矛",
    "𫘣": "悍",
    "𩙥": "颰",
    "𪡀": "嘺",

    #"𫭟阇洲": "",
}


def _sc_convert(s):
    for k, v in MAP.items():
        s = s.replace(k, v)
    return s


class Lang:
    def c(self, s):
        return s

    @property
    def xml(self):
        return None

    @property
    def zh(self):
        return None

    @property
    def en(self):
        return None

    @property
    def han_version(self):
        return None


class TC(Lang):
    def c(self, s):
        return s

    @property
    def xml(self):
        return "zh-Hant"

    @property
    def zh(self):
        return "繁"

    @property
    def en(self):
        return "tc"

    @property
    def han_version(self):
        return "傳統中文版"


class SC(Lang):
    def __init__(self):
        self._converter = opencc.OpenCC('tw2sp.json')

    def c(self, s):
        if s:
            x = self._converter.convert(s)
            x = _sc_convert(x)
            return x
        else:
            return s

    @property
    def xml(self):
        return "zh-Hans"

    @property
    def zh(self):
        return "简"

    @property
    def en(self):
        return "sc"

    @property
    def han_version(self):
        return "简体版"


def get_catalog(m, tree, catalog=None):
    catalog = catalog or []
    for x in tree:
        if x is m:
            return True, catalog
        elif isinstance(x, tuple):
            result, value = get_catalog(m, x[1], catalog + [x[0]])
            if result:
                return result, value
    return False, None