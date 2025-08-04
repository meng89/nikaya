import re

import pyabo2.page_parsing
import pyabo2.utils
from pyabo2.utils import get_name, make_xml, get_pin_name
from . import th


name_han = "無礙解道经" #
name_pali = "Paṭisambhidāmagga"
short = "Ps"
htmls = ["Ps/Ps{}.htm".format(x) for x in range(1, 31)]



def load_from_htm():
    data = []
    pin = None
    pin_seril = None
    for htm in htmls:
        root, mtime, body_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        p = re.compile(r"^(\d+)\.(.+的談論)$")
        matches = pyabo2.utils.match_line(body_lines, [p])
        assert len(matches) == 1

        m = matches[0][0]

        sutta_seril = m.group(1)
        sutta_name = m.group(2)

        suttas = pyabo2.utils.split_sutta(body_lines, matches)
        assert len(suttas) == 1

        title_line, head_lines, sutta_body_lines = suttas[0]

        pin_matchs = pyabo2.utils.match_line(head_lines, [re.compile(r"^(?:(\d)\.)?(.+品)$")])
        if pin_matchs:
            assert len(pin_matchs) == 1
            pin_m = pin_matchs[0][0]
            pin_seril = pin_m.group(1) or "1"
            pin_name = pin_m.group(2)
            pin_name_whole = pin_seril + "." + pin_name
            pin = []
            data.append((pin_name_whole, pin))

        body = pyabo2.page_parsing.htm_lines_to_xml_lines(sutta_body_lines)
        body = pyabo2.page_parsing.lines_to_body(body)

        head = pyabo2.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = pyabo2.page_parsing.lines_to_head(head)

        sutta_num = "Ps.{}.{}".format(pin_seril, sutta_seril)

        sutta_nums = [
            (None, sutta_num),
            ("SC", "Ps {}.{}".format(pin_seril, sutta_seril))
        ]

        xml = pyabo2.utils.make_xml(source_page=htm,
                                    sutta_nums=sutta_nums,
                                    start=str(sutta_seril),
                                    end=str(sutta_seril),
                                    mtime=mtime,
                                    ctime=None,
                                    source_title=pyabo2.utils.strip_crlf(matches[0][2]),
                                    relevant=None,
                                    title_line=m.group(1),
                                    head=head,
                                    body=body,
                                    notes=notes)

        pin.append((sutta_num, xml))

    return data
