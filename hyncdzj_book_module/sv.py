# 律藏/经分别
import re

from hyncdzj import base

info = base.Info(1, "經分別", ("通妙",), "SV")


def change_name_fun(name):
    m = re.match(r"^(經分別)[一二]", name)
    if m:
        return m.group(1)

    m = re.match(r"(大分別〔比丘戒〕)[一二]", name)
    if m:
        return m.group(1)

    return name


