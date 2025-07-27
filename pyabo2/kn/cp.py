import re

import pyabo2.page_parsing
import pyabo2.utils
from . import th


name_han = "所行藏"
name_pali = "Cariyāpiṭaka"
short = "Cp"
htmls = ["Cp/Cp{}.htm".format(x) for x in range(1, 36)]


def load_from_htm():
    data = {}
    seril = 0
    pin = None


    for htm in htmls:
        root, mtime, body_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        pin_lines = th.match_line(body_lines, [re.compile(r"^\d+.*品.*$")])

        if pin_lines:
            _seril, line = th.split_seril_title(pin_lines[0][1])
            assert len(line) == 1 and isinstance(line[0], str)
            pin_name = line[0]
            pin = {}
            data[pin_name] = pin

        sutta_lines = th.match_line(body_lines, [re.compile(r"^\d+.*所行.*$")])

        assert len(sutta_lines) == 1
        suttas = th.split_sutta(body_lines, sutta_lines)
        assert len(suttas) == 1

        title_line, head_lines, sutta_body_lines = suttas[0]

        body = pyabo2.page_parsing.htm_lines_to_xml_lines(sutta_body_lines)
        body = pyabo2.page_parsing.lines_to_body(body)

        head = pyabo2.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = pyabo2.page_parsing.lines_to_head(head)

        _seril, title_line = th.split_seril_title(title_line)

        seril += 1

        sutta_num = "{}.{}".format(short, seril)

        title_line = pyabo2.page_parsing.htm_line_to_xml_line(title_line)
        print(th.line_to_txt(title_line))
        xml = pyabo2.utils.make_xml(source_page=htm,
                                    sutta_num = sutta_num,
                                    start = str(seril),
                                    end = str(seril),
                                    mtime = mtime,
                                    ctime = None,
                                    title_line = title_line,
                                    head = head,
                                    body = body,
                                    notes = notes
                                    )

        filename = sutta_num
        pin[filename] = xml

    return data