import re

import pyabo2.page_parsing
import pyabo2.utils


name_han = "所行藏"
name_pali = "Cariyāpiṭaka"
short = "Cp"
htmls = ["Cp/Cp{}.htm".format(x) for x in range(1, 36)]


def load_from_htm():
    data = []
    sutta_seril = 0
    pin = None

    for htm in htmls:
        root, mtime, nikaya_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)
        matchs = pyabo2.utils.match_line(nikaya_lines, [re.compile(r"^\d+\.(.+所行)(.*)$")])
        assert len(matchs) == 1
        m = matchs[0][0]
        sutta_seril += 1
        sutta_name = m.group(1)

        suttas = pyabo2.utils.split_sutta(nikaya_lines, matchs)
        source_title_line, head_lines, body_lines = suttas[0]

        pin_matchs = pyabo2.utils.match_line(head_lines, [re.compile(r"^\d+\.(.+品)$")])
        if pin_matchs:
            assert len(pin_matchs) == 1
            pin_m = pin_matchs[0][0]
            pin_name = pin_m.group(1)
            pin = []
            data.append((pin_name, pin))

        body_lines = pyabo2.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = pyabo2.page_parsing.lines_to_body(body_lines)

        head_lines = pyabo2.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = pyabo2.page_parsing.lines_to_head(head_lines)

        sutta_nums = [
            ("SC", "Cp {}".format(sutta_seril))
        ]

        xml = pyabo2.utils.make_xml(source_page = htm,
                                    sutta_nums = sutta_nums,
                                    start = str(sutta_seril),
                                    end = str(sutta_seril),
                                    mtime = mtime,
                                    ctime = None,
                                    source_title = pyabo2.page_parsing.htm_line_to_xml_line(pyabo2.utils.strip_crlf(source_title_line)),
                                    relevant = m.group(2),
                                    title_line = sutta_name,
                                    head = head,
                                    body = body,
                                    notes = notes
                                    )

        filename = "Cp{}".format(sutta_seril)
        pin.append((filename, xml))

    return data
