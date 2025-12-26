import re

import xl

from hyncdzj import base

info = base.Info(7, "增支部", ("葉慶春", "關世謙", "郭哲彰"), "AN")

def _p(e):
    kids_s = get_only_str(e)
    m = re.match(r"^([〇一二三四五六七八九十]+)$", kids_s)

    if isinstance(e, xl.Element) \
            and e.tag == "p" \
            and len(e.kids) >= 1 \
            and re.match(r"^[〇一二三四五六七八九十※～]+$", kids_s):
        new_e = xl.Element("sub")
        new_e.kids.extend(e.kids)
        return True, [new_e]
    else:
        return False, None


def get_only_str(e):
    s = ""
    for x in e.kids:
        if isinstance(x, str):
            s += x
        elif isinstance(x, xl.Element) and x.tag == "ref":
            s += get_only_str(x)
    return s


def filter_xml_body(e: xl.Element | str):
    import hyncdzj_load_from_p5a
    my_fun_list = hyncdzj_load_from_p5a.default_filter_fun_list.copy()
    my_fun_list.remove(hyncdzj_load_from_p5a.filter_chinese_numerals_p)
    my_fun_list.append(_p)
    return hyncdzj_load_from_p5a.filter_xml_body(e, my_fun_list)
