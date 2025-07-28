import re

import pyabo2.page_parsing
import pyabo2.utils
from . import th


# 与 c
name_han = "大義釋" # 大与小
name_pali = "Mahāniddesa"
short = "Mnd"


da_htmls = ["Ni/Ni{}.htm".format(x) for x in range(1, 17)]

xiao_htmls = ["Ni/Ni{}.htm".format(x) for x in range(17, 40)]


def load_from_htm():
    data = []
    data = {}
    data["大義釋"] = load_(da_htmls)
    data["小義釋"] = load_(xiao_htmls)


def load_(htmls_):
    data = {}
    for htm in htmls_:
        root, mtime, body_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        sutta_lines = th.match_line(body_lines, [re.compile(r"^\d+.*的說明$")])

        suttas = th.split_sutta(body_lines, sutta_lines)

        assert len(sutta_lines) == 1
        for title_line, head_lines, sutta_body_lines in suttas:
            body = pyabo2.page_parsing.htm_lines_to_xml_lines(sutta_body_lines)
            body = pyabo2.page_parsing.lines_to_body(body)

            head = pyabo2.page_parsing.htm_lines_to_xml_lines(head_lines)
            head = pyabo2.page_parsing.lines_to_head(head)

            seril, title_line = th.split_seril_title(title_line)

            title_line = pyabo2.page_parsing.htm_line_to_xml_line(title_line)

            xml = pyabo2.utils.make_xml(source_page=htm,
                                        sutta_num = None,
                                        start = str(seril),
                                        end = str(seril),
                                        mtime = mtime,
                                        ctime = None,
                                        title_line = title_line,
                                        head = head,
                                        body = body,
                                        notes = notes
                                        )
            m = re.match(r"Ni/(.*).htm", htm)

            data[m.group(1)] = xml

    return data