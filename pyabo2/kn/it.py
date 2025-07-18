import re


import xl



import pyabo2.page_parsing


name_han = "如是語"
name_pali = "Itivuttaka"
short = "It"
htmls = ["It/It{:0>3d}.htm".format(x) for x in range(1, 113)]


class Doc:
    def __init__(self):
        self.xml = xl.Xml()


def get_last_folder(data: dict):
    last_folder = None
    for _, v in data.items():
        if isinstance(v, dict):
            last_folder = v

    if last_folder is None:
        return data
    else:
        return get_last_folder(last_folder)


def load_from_htm():
    data = {}
    pian = None or dict
    for result in pyabo2.page_parsing.read_pages(htmls):
        mtime, homage_line, head_lines, sutta_name_part, translator_part, agama_part, body, notes, pali_doc = result

        doc = xl.Element("doc")
        meta = doc.ekid("meta")
        doc.kids.append(body)
        doc.kids.append(notes)
        xml = xl.Xml(root=doc)


        m = re.match(r"\((\S+篇)\)", translator_part)
        if "篇" in translator_part:
            assert m
            pian_name = m.group(1)
            if pian_name not in data.keys():
                data[pian_name] = {}
            pian = data[pian_name]



        for line in head_lines:
            s = line[0].strip()

            m = re.match(r".*(第\S+品)", s)
            if "品" in s:
                pin_name = m.group(1)
                pin = {}
                pian[pin_name] = pin

        m =  re.match(r"如是語(\d+)經/(\S+經)", sutta_name_part[0])
        start = meta.ekid("start"); start.kids.append(m.group(1))
        end = meta.ekid("end"); end.kids.append(m.group(1))
        name = meta.ekid("name"); name.kids.append(m.group(2))
        relevant = meta.ekid("relevent")
        if agama_part:
            relevant.kids.append(agama_part)

        filename = "It{}".format(m.group(1))
        last_folder = get_last_folder(data)
        last_folder[filename] = xml

    #print(data)
    return data





