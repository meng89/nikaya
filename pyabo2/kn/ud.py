import os.path
import re


import xl

import base
import pyabo2.page_parsing

name_han = "優陀那" # 自说经
name_pali = "Udānapāḷi"
short = "Ud"
htmls = ["Ud/Ud{:0>2d}.htm".format(x) for x in range(1, 81)]


try:
    import user_config as config
except ImportError:
    import config as config


def load_from_htm():
    data = {}
    for html in htmls:
        x = pyabo2.page_parsing.read_page(html, 2)
        _root, mtime, homage_line, head_lines, sutta_name_part, translator_part, agama_part, body, notes, pali_doc = x

        p = re.compile(r"^優陀那(\d)經/(.+)\(\d\.(.+品)\)\(莊春江譯\)(.*)$")

        doc = xl.Element("doc")
        meta = doc.ekid("meta")
        doc.kids.append(body)
        doc.kids.append(notes)
        xml = xl.Xml(root=doc)

        m = re.match(r"\(\d+\.(\S+品)", translator_part)
        pin_name = m.group(1)

        # todo report bug
        if pin_name == "天生失明品":
            pin_name = "天生失明者品"

        if pin_name not in data.keys():
            data[pin_name] = {}
        pin = data[pin_name]

        m = re.match(r"^優陀那(\d+)經/(\S+)$", sutta_name_part[0])

        start = meta.ekid("start")
        start.kids.append(m.group(1))
        end = meta.ekid("end")
        end.kids.append(m.group(1))
        name = meta.ekid("name")
        name.kids.append(m.group(2))

        filename = "Ud{}".format(m.group(1))

        pin[filename] = xml

    return data


def write_to_epub(data):
    pass