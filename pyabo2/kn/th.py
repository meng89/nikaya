import re

import xl

import pyabo2.page_parsing
import pyabo2.utils


name_han = "長老偈"
name_pali = "Theragāthā"
short = "Th"
htmls = ["Th/Th{}.htm".format(x) for x in range(1, 113)]


def load_from_htm():
    data = {}
    jipian: None or dict = None
    for htm in htmls:
        root, mtime, body_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        _name = pyabo2.utils.get_name2(root)

        matched_lines = match_line(body_lines, ["集篇"])
        print(matched_lines)


def line_to_txt(line: list):
    s = ""
    for x in line:
        if isinstance(x, str):
            s += x
        elif isinstance(x, xl.Element):
            s += line_to_txt(x.kids)
        else:
            raise Exception(x)

    return s



def match_line(lines: list, ends_list):
    matched_lines = []
    for index, line in enumerate(lines):
        txt = line_to_txt(line).strip()
        #print(repr(txt))
        for ends in ends_list:
            if txt.endswith(ends):
                matched_lines.append((index, line))

    return matched_lines
