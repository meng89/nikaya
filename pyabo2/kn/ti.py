import re

import pyabo2.page_parsing
import pyabo2.utils

from . import th

name_han = "長老尼偈"
name_pali = "Therīgāthā"
short = "Thig"

htmls = ["Ti/Ti{}.htm".format(x) for x in range(1, 74)]


def load_from_htm():
    data = {}
    pian_seril = None
    pian: None or dict = None

    for htm in htmls:
        root, mtime, body_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        pian_lines = th.match_line(body_lines, ["集篇"])
        ji_lines = th.match_line(body_lines, [re.compile(r"^\d+.*長老尼偈.*$")])

        if pian_lines:
            seril, line = th.split_seril_title(pian_lines[0][1])
            assert len(line) == 1 and isinstance(line[0], str)
            pian_seril = seril
            pian_name = "{}.{}".format(seril, line[0])
            pian = {}
            data[pian_name] = pian


        assert ji_lines
        jis = th.split_sutta(body_lines, ji_lines)
        for title_line, head_lines, sutta_body_lines in jis:


            body = pyabo2.page_parsing.htm_lines_to_xml_lines(sutta_body_lines)
            body = pyabo2.page_parsing.lines_to_body(body)

            head = pyabo2.page_parsing.htm_lines_to_xml_lines(head_lines)
            head = pyabo2.page_parsing.lines_to_head(head)

            seril, title_line = th.split_seril_title(title_line)
            sutta_num = "Thag.{}.{}".format(pian_seril, seril)

            title_line = pyabo2.page_parsing.htm_line_to_xml_line(title_line)
            print(th.line_to_txt(title_line))
            xml = pyabo2.utils.make_xml(source_page=htm,
                                        sutta_num = sutta_num,
                                        start = seril,
                                        end = seril,
                                        mtime = mtime,
                                        ctime = None,
                                        title_line = title_line,
                                        head = head,
                                        body = body,
                                        notes = notes
                                        )

            filename = sutta_num
            pian[filename] = xml

    return data
