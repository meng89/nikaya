import re

import abo.page_parsing
import abo.utils
from share import Info


info = Info(
    name = "所行藏",
    pali = "Cariyāpiṭaka",
    abbr = "Cp",
    translators = ("莊春江",),
    htmls = ["Cp/Cp{}.htm".format(x) for x in range(1, 36)],
)


def load_from_htm():
    data = []
    sutta_serial = 0
    pin = None

    for htm in info.htmls:
        root, mtime, nikaya_lines, notes, div_nikaya = abo.page_parsing.read_page(htm, 2)
        matchs = abo.utils.match_line(nikaya_lines, [re.compile(r"^\d+\.(.+所行)(.*)$")])
        assert len(matchs) == 1
        m = matchs[0][0]
        sutta_serial += 1
        sutta_name = m.group(1)

        suttas = abo.utils.split_sutta(nikaya_lines, matchs)
        source_title_line, head_lines, body_lines = suttas[0]

        pin_matchs = abo.utils.match_line(head_lines, [re.compile(r"^\d+\.(.+品)$")])
        if pin_matchs:
            assert len(pin_matchs) == 1
            pin_m = pin_matchs[0][0]
            pin_name = pin_m.group(1)
            pin = []
            data.append(((None, None, pin_name), pin))

        body_lines = abo.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = abo.page_parsing.lines_to_es(body_lines)

        head_lines = abo.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = abo.page_parsing.lines_to_head(head_lines)

        sutta_nums = [
            ("SC", "Cp {}".format(sutta_serial))
        ]

        xml = abo.utils.make_xml(source_page = htm,
                                 sutta_nums = sutta_nums,
                                 start = str(sutta_serial),
                                 end = str(sutta_serial),
                                 mtime = mtime,
                                 ctime = None,
                                 source_title = abo.page_parsing.htm_line_to_xml_line(abo.utils.strip_crlf(source_title_line)),
                                 relevant = m.group(2),
                                 title_line = [sutta_name],
                                 head = head,
                                 body_es= body,
                                 notes = notes
                                 )

        filename = "Cp{}".format(sutta_serial)
        pin.append(((int(sutta_serial), int(sutta_serial), sutta_name), xml))

    return data
