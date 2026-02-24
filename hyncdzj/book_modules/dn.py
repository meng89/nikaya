import re

import cn2an

from nikaya_share import Info


info = Info(
    serial = 4,
    name = "長部",
    pali = "Dīgha Nikāya",
    translators = ("通妙",),
    abbr = "DN",
)

def change_name_fun(name):
    m = re.match(r"^([一二三四五六七八九十〇]+)　(\S+經)$", name)
    if m:
        return "{}.{}".format(cn2an.cn2an(m.group(1), "normal"), m.group(2))
    else:
        return name


def merge_sutta(data):
    pass
