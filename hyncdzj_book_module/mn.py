
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
        return "MN {}　{}".format(cn2an.cn2an(m.group(1), "normal"), m.group(2))

    return name
