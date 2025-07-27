import re

import pyabo2.page_parsing
import pyabo2.utils
from pyabo2.utils import get_name, make_xml, get_pin_name
from . import th


name_han = "無礙解道" #
name_pali = "Paṭisambhidāmagga"
short = "Ps"
htmls = ["Ps/Ps{}.htm".format(x) for x in range(1, 31)]


def load_from_htm():
    data = {}
    pin = None
    seril = 0
    for htm in htmls:
        root, mtime, body_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        pin_lines = th.match_line(body_lines, [re.compile(r"^\d?.*品$")])
        if pin_lines:
            # todo report
            if pin_lines[0][1][0] == "\u3000大品\n":
                pin_lines[0][1][0] = "\u30001.大品\n"
            _seril, line = th.split_seril_title(pin_lines[0][1])
            assert len(line) == 1 and isinstance(line[0], str)
            pin_name = line[0]
            pin = {}
            data[pin_name] = pin

        sutta_lines = th.match_line(body_lines, [re.compile(r"^\d+.*的談論$")])
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
        xml = make_xml(htm, sutta_num, str(seril), str(seril), mtime, None, title_line, head, body, notes)

        pin[sutta_num] = xml

    return data
