import re

import xl

import pyabo2.page_parsing
import pyabo2.utils


name_han = "餓鬼事"
name_pali = "Petavatthu"
short = "Pv"
htmls = ["Pv/Pv{}.htm".format(x) for x in range(1, 52)]


def load_from_htm():
    data = []
    pin = None
    for htm in htmls:
        root, mtime, nikaya_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)
        p = re.compile(r"(\d+)\.(.+(?:餓鬼事|裁判官))(?:\((\d+)\.\))?\*?")
        matchs = pyabo2.utils.match_line(nikaya_lines, [p])
        assert len(matchs) == 1
        m = matchs[0][0]
        sutta_serial = m.group(3) or m.group(1)
        sutta_name = m.group(2)

        suttas = pyabo2.utils.split_sutta(nikaya_lines, matchs)
        assert len(suttas) == 1

        source_title_line, head_lines, body_lines = suttas[0]

        p = re.compile(r"^\d\.(.+品)$")
        pin_matchs = pyabo2.utils.match_line(head_lines, [p])
        if pin_matchs:
            assert len(pin_matchs) == 1
            m = pin_matchs[0][0]
            pin_name = m.group(1)
            pin = []
            data.append((pin_name, pin))

        body_lines = pyabo2.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = pyabo2.page_parsing.lines_to_body(body_lines)

        head_lines = pyabo2.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = pyabo2.page_parsing.lines_to_body(head_lines)

        sutta_num = "Pv." + sutta_serial
        sutta_nums = [
            (None, sutta_num),
            ("SC", "PV " + sutta_serial)
        ]

        xml = pyabo2.utils.make_xml(source_page=htm,
                                    sutta_nums=sutta_nums,
                                    start=sutta_serial,
                                    end=sutta_serial,
                                    mtime=mtime,
                                    ctime=None,
                                    source_title=pyabo2.utils.strip_crlf(source_title_line),
                                    relevant=None,
                                    title_line=sutta_name,
                                    head=head,
                                    body=body,
                                    notes=notes)

        pin.append((sutta_num, xml))

    return data