import re

import pyabo2.page_parsing
import pyabo2.utils


# 与 SC 经号差别较大

name_han = "大義釋" # 大与小
name_pali = "Mahāniddesa"
short = "Ni"


da_htmls = ["Ni/Ni{}.htm".format(x) for x in range(1, 17)]

xiao_htmls = ["Ni/Ni{}.htm".format(x) for x in range(17, 40)]


htmls = da_htmls + xiao_htmls


def load_from_htm():
    data = [
        ("大義釋", load_(da_htmls)),
        ("小義釋", load_(xiao_htmls))
    ]
    return data


def load_(htmls_):
    data = []
    for htm in htmls_:
        root, mtime, body_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        m = pyabo2.utils.get_name(root, re.compile(r"^(\d+)\.(.+(?:的說明|…)|序偈)$"))

        body = pyabo2.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = pyabo2.page_parsing.lines_to_body(body)

        xml = pyabo2.utils.make_xml(source_page = htm,
                                    sutta_nums = [],
                                    start = m.group(1),
                                    end = m.group(1),
                                    mtime = mtime,
                                    ctime = None,
                                    source_title=None,
                                    relevant = None,
                                    title_line = m.group(2),
                                    head = None,
                                    body = body,
                                    notes = notes
                                    )
        m = re.match(r"Ni/(.*).htm", htm)
        data.append((m.group(1), xml))

    return data
