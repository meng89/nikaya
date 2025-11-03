import re

import cn2an

from hyncdzj import base

info = base.Info(4, "長部", ("通妙",), "DN")

def change_name_fun(name):
    m = re.match(r"^([一二三四五六七八九十〇]+)　(\S+經)$", name)
    if m:
        return "DN {} {}".format(cn2an.cn2an(m.group(1), "normal"), m.group(2))
    else:
        return name
