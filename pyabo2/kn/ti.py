import re

import pyabo2.page_parsing
import pyabo2.utils

from . import th

name_han = "長老尼偈"
name_pali = "Therīgāthā"
short = "Thig"

htmls = ["Ti/Ti{}.htm".format(x) for x in range(1, 74)]


def load_from_htm():
    data = []
    pian_serial = None
    pian = None

    for htm in htmls:
        root, mtime, nikaya_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        matchs = pyabo2.utils.match_line(nikaya_lines, [re.compile(r"^(\d+)\.(.+長老尼偈).*$")])
        assert len(matchs) == 1
        m = matchs[0][0]
        sutta_serial = m.group(1)
        sutta_name = m.group(2)

        jis = pyabo2.utils.split_sutta(nikaya_lines, matchs)
        assert len(jis) == 1
        source_title_line, head_lines, body_lines = jis[0]

        pian_matchs = pyabo2.utils.match_line(head_lines, [re.compile(r"^(\d+)\.(.+集篇)$")])
        if pian_matchs:
            assert len(pian_matchs) == 1
            pian_m = pian_matchs[0][0]
            pian_serial = pian_m.group(1)
            pian_name = pian_m.group(2)
            pian = []
            data.append(("{}.{}".format(pian_serial, pian_name), pian))


        body_lines = pyabo2.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = pyabo2.page_parsing.lines_to_body(body_lines)

        head_lines = pyabo2.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = pyabo2.page_parsing.lines_to_head(head_lines)

        serial, title_line = pyabo2.utils.split_serial_title(source_title_line)
        sutta_num = "Thig.{}.{}".format(pian_serial, serial)
        sutta_nums = [
            (None, sutta_num),
            ("SC", "Thig {}.{}".format(pian_serial, serial))
        ]

        title_line = pyabo2.page_parsing.htm_line_to_xml_line(title_line)
        xml = pyabo2.utils.make_xml(source_page = htm,
                                    sutta_nums = sutta_nums,
                                    start = serial,
                                    end = serial,
                                    mtime = mtime,
                                    ctime = None,
                                    source_title = pyabo2.utils.strip_crlf(source_title_line),
                                    relevant = None,
                                    title_line = title_line,
                                    head = head,
                                    body = body,
                                    notes = notes
                                    )

        pian.append((sutta_num, xml))

    return data
