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
    data = []
    pin = []
    pin_name = None
    sutta_seril = 0
    for htm in htmls:
        root, mtime, body_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        p = re.compile(r"^(\d+)\.(.+的談論)$")
        matches = pyabo2.utils.match_line(body_lines, [p])
        assert len(matches) == 1

        m = matches[0][0]

        sutta_seril = m.group(1)
        sutta_name = m.group(2)

        # todo report bug
        if new_pin_name == "天生失明品":
            new_pin_name = "天生失明者品"

        if pin_name != new_pin_name:
            pin_name = new_pin_name
            pin = []
            pin_name_whole = pin_seril + "." + new_pin_name
            data.append((pin_name_whole, pin))
            sutta_seril = 0

        suttas = pyabo2.utils.split_sutta(body_lines, matches)
        assert len(suttas) == 1

        title_line, head_lines, sutta_body_lines = suttas[0]

        body = pyabo2.page_parsing.htm_lines_to_xml_lines(sutta_body_lines)
        body = pyabo2.page_parsing.lines_to_body(body)

        head = pyabo2.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = pyabo2.page_parsing.lines_to_head(head)


        pin_matchs = pyabo2.utils.match_line(head_lines, [re.compile(r"^(\d)\.(.+品)$")])
        if pin_matchs:
            assert len(pin_matchs) == 1
            pin_m = pin_matchs[0][0]



        sutta_seril += 1

        sutta_num = "Ud.{}.{}".format(pin_seril, sutta_seril)

        sutta_nums = [
            (None, sutta_num),
            ("SC", "Ud {}.{}".format(pin_seril, sutta_seril))
        ]

        xml = pyabo2.utils.make_xml(source_page=htm,
                                    sutta_nums=sutta_nums,
                                    start=str(sutta_seril),
                                    end=str(sutta_seril),
                                    mtime=mtime,
                                    ctime=None,
                                    source_title=pyabo2.utils.strip_crlf(matches[0][2]),
                                    relevant=m.group(4),
                                    title_line=m.group(1),
                                    head=head,
                                    body=body,
                                    notes=notes)

        pin.append((sutta_num, xml))

    return data


def load_from_htm():
    data = {}
    pin = None
    seril = 0
    for htm in htmls:
        root, mtime, body_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        pin_lines = pyabo2.utils.match_line(body_lines, [re.compile(r"^\d?.*品$")])
        if pin_lines:
            # todo report
            if pin_lines[0][1][0] == "\u3000大品\n":
                pin_lines[0][1][0] = "\u30001.大品\n"
            _seril, line = th.split_seril_title(pin_lines[0][1])
            assert len(line) == 1 and isinstance(line[0], str)
            pin_name = line[0]
            pin = {}
            data[pin_name] = pin

        sutta_lines = pyabo2.utils.match_line(body_lines, [re.compile(r"^\d+.*的談論$")])
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
