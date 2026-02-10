import re

from nikaya_share import base


info = base.Info(
    serial = 1,
    name = "經分別",
    pali = "Suttavibhaṅga",
    translators = ("通妙",),
    abbr = "SV",
)


def change_name_fun(name):
    m = re.match(r"^(經分別)[一二]", name)
    if m:
        return m.group(1)

    m = re.match(r"(大分別〔比丘戒〕)[一二]", name)
    if m:
        return m.group(1)

    return name
