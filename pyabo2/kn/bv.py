import re

import pyabo2.page_parsing
import pyabo2.utils


name_han = "佛種姓"
name_pali = "Buddhavaṃsa"
short = "Bv"
htmls = ["Bv/Bv{}.htm".format(x) for x in range(1, 30)]


def load_from_htm():
    data = []
    for htm in htmls:
        root, mtime, nikaya_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        # todo report 3.燃燈佛種性
        matchs = pyabo2.utils.match_line(nikaya_lines, [re.compile(r"^(\d+)\.(.*(?:佛種性|佛種姓|寶物經行處章|蘇昧達的願求說|種種佛章|遺骨的分配說)).*$")])
        assert len(matchs) == 1

        m = matchs[0][0]
        sutta_serial = m.group(1)
        sutta_name = m.group(2)

        suttas = pyabo2.utils.split_sutta(nikaya_lines, matchs)
        source_title_line, head_lines, body_lines = suttas[0]


        body_lines = pyabo2.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = pyabo2.page_parsing.lines_to_body(body_lines)

        head_lines = pyabo2.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = pyabo2.page_parsing.lines_to_head(head_lines)

        sutta_num = "{}.{}".format(short, sutta_serial)
        sutta_nums = [
            (None, sutta_num),
            ("SC", "{} {}".format(short, sutta_serial))
        ]

        xml = pyabo2.utils.make_xml(source_page = htm,
                                    sutta_nums = sutta_nums,
                                    start = sutta_serial,
                                    end = sutta_serial,
                                    mtime = mtime,
                                    ctime = None,
                                    source_title = pyabo2.page_parsing.htm_line_to_xml_line(pyabo2.utils.strip_crlf(source_title_line)),
                                    relevant = None,
                                    title_line = sutta_name,
                                    head = head,
                                    body = body,
                                    notes = notes
                                    )

        data.append((sutta_num, xml))

    return data
