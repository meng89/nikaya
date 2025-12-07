from typing import List, Tuple, Union
import os
import re
import shutil

import xl

import abo.utils


def _split(name):
    return re.match(r"^(\d+)_(.+?)(\.xml)?$", name)


def split_serial(name):
    return _split(name).group(1)


def split_name(name):
    return _split(name).group(2)


Entry = Tuple[str, Union[xl.Xml, List["Entry"]]]
Folder = List[Entry]


def load_from_disk(path) -> list:
    data = []
    entries = os.listdir(path)
    entries.sort(key=split_serial)
    for entry in entries:
        entry_path = os.path.join(path, entry)

        if os.path.isdir(entry_path):
            name = split_name(entry)
            v = load_from_disk(entry_path)

        elif os.path.isfile(entry_path):
            name = os.path.basename(entry_path)
            #name = os.path.splitext(name)[0]
            name = split_name(name)
            v = xl.parse(open(entry_path, "r").read())
        else:
            raise Exception("Unknow File: {}".format(entry_path))

        data.append((name, v))
    return data


def write_to_disk(path, data: list, delete_existed=False):
    if os.path.exists(path) and delete_existed is True:
        shutil.rmtree(path)
    os.makedirs(path)
    width = len(str(len(data)))
    for i, (name, obj) in enumerate(data, 1):
        file_name = f"{i:>{width}}_{name}"
        sub_path = os.path.join(path, file_name)
        if isinstance(obj, list):
            write_to_disk(sub_path, obj)
        elif isinstance(obj, xl.Xml):
            s = obj.to_str(do_pretty=True, try_self_closing=True, dont_do_tags=abo.utils.WRITE_DONT_DO_TAGS)
            with open(sub_path + ".xml", "w") as f:
                f.write(s)
