import re
from datetime import datetime

import xl


def get_last_folder(data: dict):
    last_folder = None
    for _, v in data.items():
        if isinstance(v, dict):
            last_folder = v

    if last_folder is None:
        return data
    else:
        return get_last_folder(last_folder)


class AnalysisFailed(Exception):
    pass


def get_name(root, pattern):
    names = []
    for span in root.find_descendants("span"):
        if len(span.kids) > 0 and isinstance(span.kids[0], str):
            kid = span.kids[0].strip()
            m = re.match(pattern, kid)
            if m:
                names.append(m)
    if len(names) != 1:
        open("get_name_debug.xml", "w").write(root.to_str())
        debug_print_es(root.find_descendants("span"))
        raise AnalysisFailed(names)
    return names[0]


def get_name2(root):
    names = []
    for span in root.find_descendants("span"):
        if len(span.kids) > 0 and span.attrs.get("style") == "font-size: 18pt" and isinstance(span.kids[0], str):
            kid = span.kids[0].strip()
            names.append(kid)
    if len(names) != 1:
        open("get_name_debug.xml", "w").write(root.to_str())
        debug_print_es(root.find_descendants("span"))
        raise AnalysisFailed(names)
    return names[0]


def debug_print_es(l):
    s = ""
    for x in l:
        if isinstance(x, str):
            s += x
        elif isinstance(x, xl.Element):
            s += x.to_str()
        else:
            raise Exception
    print(s)

              # SN.1.1   1     1
def make_xml(source_page, sutta_num, start, end, mtime, ctime, title_line, head, body, notes):
    doc = xl.Element("doc")
    meta = doc.ekid("meta")

    source_page_e = meta.ekid("source_page")
    source_page_e.kids.append(source_page)

    sutta_num_e = meta.ekid("sutta_num")
    if sutta_num:
        sutta_num_e.kids.append(sutta_num)

    start_e = meta.ekid("start")
    if start is not None:
        start_e.kids.append(start)

    end_e = meta.ekid("end")
    if end is not None:
        end_e.kids.append(end)

    name_e = meta.ekid("title")
    name_e.kids.extend(title_line)

    mtime_e = meta.ekid("mtime")
    mtime_str = datetime.fromtimestamp(mtime).astimezone().strftime('%Y-%m-%d %H:%M:%S %z')
    mtime_e.kids.append(mtime_str)

    ctime_e = meta.ekid("ctime")
    if ctime:
        ctime_e.kids.append(ctime)

    if head:
        doc.kids.append(head)
    else:
        doc.ekid("head")
    doc.kids.append(body)
    doc.kids.append(notes)
    xml = xl.Xml(root=doc)
    return xml


def get_pin_name(body_lines):
    pin_list = []
    for line in body_lines:
        if len(line) == 1 and isinstance(line[0], str):
            kid = line[0].strip()
            if kid.endswith("品"):
                m = re.match(r"^(\d+\.)?(\S+)$", kid)
                pin_list.append(m.group(2))

    if pin_list:
        return pin_list[0]
    else:
        return None


def get_pin_name2(body_lines):
    pin_list = []
    for line in body_lines:
        if len(line) == 1 and isinstance(line[0], str):
            kid = line[0].strip()
            if kid.endswith("品"):
                m = re.match(r"^(\d+\.\S+)$", kid)
                pin_list.append(m.group(1))


    if len(pin_list) > 1:
        raise AnalysisFailed(pin_list)

    if pin_list:
        return pin_list[0]
    else:
        return None