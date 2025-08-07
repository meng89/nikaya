import re

import pyabo2.page_parsing
import pyabo2.utils


name_han = "長老阿波陀那" #譬喻
name_pali = "Therāpadāna"

htmls = ["Ap/Ap{}.htm".format(x) for x in range(1, 564)]

# 品名都是首经的名字，意义不大。这里经文编号依照 suttacentral 风格重编，品不参与编排经号。

short = "Tha-ap"


def load_from_htm():
    return load_from_htm_real(htmls, short)


def load_from_htm_real(_htmls, _short):
    data = []
    pin = None
    sutta_serial = 0
    for htm in _htmls:
        root, mtime, nikaya_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        matchs = pyabo2.utils.match_line(nikaya_lines, [re.compile(r"^\d+(?:-\d)?\.?(.+阿波陀那).*$")])
        assert len(matchs) == 1
        m = matchs[0][0]
        sutta_serial += 1
        sutta_name = m.group(1)

        aps = pyabo2.utils.split_sutta(nikaya_lines, matchs)
        source_title_line, head_lines, body_lines = aps[0]

        pin_matchs = pyabo2.utils.match_line(head_lines, [re.compile(r"^\d+\.(.+品).*$")])
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


        sutta_num = "{} {}".format(_short, sutta_serial)
        sutta_nums = [
            ("SC", sutta_num)
        ]

        xml = pyabo2.utils.make_xml(source_page = htm,
                                    sutta_nums = sutta_nums,
                                    start = str(sutta_serial),
                                    end = str(sutta_serial),
                                    mtime = mtime,
                                    ctime = None,
                                    source_title = pyabo2.page_parsing.htm_line_to_xml_line(pyabo2.utils.strip_crlf(source_title_line)),
                                    relevant = None,
                                    title_line = sutta_name,
                                    head = head,
                                    body = body,
                                    notes = notes
                                    )

        filename = "{}{}".format(_short, sutta_serial)
        pin.append((filename, xml))

    return data
