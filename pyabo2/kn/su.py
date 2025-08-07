import re

from jinja2 import meta

import pyabo2.page_parsing
import pyabo2.utils


name_han = "經集"
name_pali = "Suttanipāta"
short = "Su"
htmls = ["Su/Su{}.htm".format(x) for x in range(1, 74)]


# 原网页头部经号和页面经号略乱。使用 SC 经号

# todo report  Su/Su.js Su48htm 应为 Su48.htm


def load_from_htm():
    data = []
    pin = None
    pin_serial = None

    sutta_serial = 0

    for htm in htmls:
        root, mtime, nikaya_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)
        p = re.compile(r"^(\d+)\.(.+(?:經|所問|偈))(?:\(\d+\.\))?(.*)$")
        p2 = re.compile(r"^(\d*)(序　偈)\(\d+\.\)(.*)$")
        matchs = pyabo2.utils.match_line(nikaya_lines, [p, p2])
        assert len(matchs) == 1
        m = matchs[0][0]

        suttas = pyabo2.utils.split_sutta(nikaya_lines, matchs)
        assert len(suttas) == 1
        source_title_line, head_lines, body_lines = suttas[0]

        #_sutta_serial, title_line = pyabo2.utils.split_serial_title(source_title_line)

        pin_matchs = pyabo2.utils.match_line(head_lines, [re.compile(r"^(\d+)\.(.+品(?:\(.+品\))?)$")])
        if pin_matchs:
            assert len(pin_matchs) == 1
            pin_m = pin_matchs[0][0]
            pin_serial = pin_m.group(1)
            pin_num = "{}.{}".format(pin_m.group(1), pin_m.group(2))
            pin = []
            data.append((pin_num, pin))
            sutta_serial = 0

        head_lines = pyabo2.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = pyabo2.page_parsing.lines_to_body(head_lines)

        body = pyabo2.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = pyabo2.page_parsing.lines_to_body(body)

        sutta_serial += 1
        sutta_num = "Su.{}.{}".format(pin_serial, sutta_serial)
        sutta_nums = [
            (None, sutta_num)
        ]

        xml = pyabo2.utils.make_xml(source_page=htm,
                                    sutta_nums=sutta_nums,
                                    start=str(sutta_serial),
                                    end=str(sutta_serial),
                                    mtime=mtime,
                                    ctime=None,
                                    source_title=source_title_line,
                                    relevant=m.group(3),
                                    title_line=m.group(2),
                                    head=head,
                                    body=body,
                                    notes=notes
                                    )
        pin.append((sutta_num, xml))

    return data
