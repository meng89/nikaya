import re
from datetime import datetime, timezone


import xl

import pyabo2.page_parsing
import pyabo2.utils


name_han = "無礙解道" #
name_pali = "Paṭisambhidāmagga"
short = "Ps"
htmls = ["Ps/Ps{}.htm".format(x) for x in range(1, 31)]



def get_name(root):
    tanlun_list = []
    for span in root.find_descendants("span"):
        if len(span.kids)  > 0 and isinstance(span.kids[0], str):
            kid = span.kids[0].strip()
            if kid.endswith("談論"):
                tanlun_list.append(kid)
            else:
                pass
    assert len(tanlun_list) == 1
    return tanlun_list[0]


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


def make_xml(start, end, name, mtime, ctime, body, notes):
    doc = xl.Element("doc")
    meta = doc.ekid("meta")

    start_e = meta.ekid("start")
    start_e.kids.append(start)

    end_e = meta.ekid("end")
    end_e.kids.append(end)

    name_e = meta.ekid("name")
    name_e.kids.append(name)

    mtime_e = meta.ekid("mtime")
    mtime_str = datetime.fromtimestamp(mtime, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    mtime_e.kids.append(mtime_str)

    ctime_e = meta.ekid("ctime")
    if ctime:
        ctime_e.kids.append(ctime)

    doc.kids.append(body)
    doc.kids.append(notes)
    xml = xl.Xml(root=doc)
    return xml


def load_from_htm():
    data = {}
    for x in pyabo2.page_parsing.read_pages(htmls, use_read_page2=True):
        root, mtime, body_lines, notes, div_nikaya = x
        #open("1.xml", "w").write(x.to_str(try_self_closing=True))

        body = pyabo2.page_parsing.lines_to_body(body_lines)

        pin_name = get_pin_name(body_lines)
        _name = get_name(root)
        m = re.match(r"^(\d+)\.(\S+)$", _name)
        xml = make_xml(m.group(1), m.group(1), m.group(2), mtime, None, body, notes)

        name = m.group(2)

        if pin_name:
            data[pin_name] = {}

        folder = pyabo2.utils.get_last_folder(data)
        folder["Ps{}".format(m.group(1))] = xml

    return data
