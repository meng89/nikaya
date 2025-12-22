
import re

import cn2an

from hyncdzj import base

info = base.Info(5, "中部", ("通妙",), "MN")


def change_name_fun(name):
    m = re.match(r"^\S+　(\S+)篇[上下]$", name)
    if m:
        return m.group(1)

    m = re.match(r"第([一二三四五六七八九十〇]+)　(\S+經)", name)
    if m:
        return "{}.{}".format(cn2an.cn2an(m.group(1), "normal"), m.group(2))
    return name


def change(raw_data):
    data = _change(raw_data)
    data = merge(data)
    return data


def _change(raw_data):
    new_data = []
    for name, obj in raw_data:
        namegroup = None
        m = re.match(r"\S+品[上|下]?　(.+品)[上|下]?$", name)
        if m:
            namegroup = (None, None, m.group(1).replace("　", ""))

        m = re.match(r"第([一二三四五六七八九十〇]+)　(\S+經)", name)
        if m:
            start = end = cn2an.cn2an(m.group(1), "normal")
            namegroup = start, end, m.group(2)

        if isinstance(obj, list):
            new_obj = _change(obj)
        else:
            new_obj = obj
        namegroup = namegroup or (None, None, name)
        new_data.append((namegroup, new_obj))

    return new_data

def merge(data):
    data = data
    while True:
        is_merged, data = merge2(data)
        if not is_merged:
            break
    return data

def merge2(data):
    is_merged = False
    tmp_data = {}
    for name, obj in data:

        if isinstance(obj, list):
            is_merged2, new_obj = merge2(obj)
            if is_merged2:
                is_merged = True
        else:
            new_obj = obj

        if name in list(tmp_data.keys()) and isinstance(tmp_data[name], list) and isinstance(new_obj, list):
            new_obj = tmp_data[name] + new_obj
            is_merged = True

        tmp_data[name] = new_obj

    return is_merged, list(tmp_data.items())
