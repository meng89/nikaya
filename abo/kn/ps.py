import re

import abo.page_parsing
import abo.utils
from share import Info


info = Info(
    name = "無礙解道", #
    pali = "Paṭisambhidāmagga",
    abbr = "Ps",
    translators = ("莊春江",),
    htmls = ["Ps/Ps{}.htm".format(x) for x in range(1, 31)],
)


def load_from_htm():
    data = []
    pin = None
    pin_serial = None
    for htm in info.htmls:
        root, mtime, body_lines, notes, div_nikaya = abo.page_parsing.read_page(htm, 2)

        p = re.compile(r"^(\d+)\.(.+的談論)$")
        matches = abo.utils.match_line(body_lines, [p])
        assert len(matches) == 1

        m = matches[0][0]

        sutta_serial = m.group(1)
        sutta_name = m.group(2)

        suttas = abo.utils.split_sutta(body_lines, matches)
        assert len(suttas) == 1

        title_line, head_lines, sutta_body_lines = suttas[0]

        pin_matchs = abo.utils.match_line(head_lines, [re.compile(r"^(?:(\d)\.)?(.+品)$")])
        if pin_matchs:
            assert len(pin_matchs) == 1
            pin_m = pin_matchs[0][0]
            pin_serial = pin_m.group(1) or "1"
            pin_name = pin_m.group(2)
            pin_name_whole = pin_serial + "." + pin_name
            pin = []
            data.append(((int(pin_serial), int(pin_serial), pin_name), pin))

        body = abo.page_parsing.htm_lines_to_xml_lines(sutta_body_lines)
        body = abo.page_parsing.lines_to_es(body)

        head = abo.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = abo.page_parsing.lines_to_head(head)

        sutta_num = "Ps.{}.{}".format(pin_serial, sutta_serial)

        sutta_nums = [
            (None, sutta_num),
            ("SC", "Ps {}.{}".format(pin_serial, sutta_serial))
        ]

        xml = abo.utils.make_xml(source_page=htm,
                                 sutta_nums=sutta_nums,
                                 start=str(sutta_serial),
                                 end=str(sutta_serial),
                                 mtime=mtime,
                                 ctime=None,
                                 source_title=abo.utils.strip_crlf(matches[0][2]),
                                 relevant=None,
                                 title_line=[m.group(2)],
                                 head=head,
                                 body_es=body,
                                 notes=notes)

        pin.append(((int(sutta_serial), int(sutta_serial), m.group(2)), xml))

    return data
