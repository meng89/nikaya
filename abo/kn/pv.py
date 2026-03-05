import re

import abo.page_parsing
import abo.utils
from share import Info


info = Info(
    name = "餓鬼事",
    pali = "Petavatthu",
    abbr = "Pv",
    translators = ("莊春江",),
    htmls = ["Pv/Pv{}.htm".format(x) for x in range(1, 52)],
)


def load_from_htm():
    data = []
    pin = None
    for htm in info.htmls:
        root, mtime, nikaya_lines, notes, div_nikaya = abo.page_parsing.read_page(htm, 2)
        p = re.compile(r"(\d+)\.(.+(?:餓鬼事|裁判官))(?:\((\d+)\.\))?\*?")
        matchs = abo.utils.match_line(nikaya_lines, [p])
        assert len(matchs) == 1
        m = matchs[0][0]
        sutta_serial = m.group(3) or m.group(1)
        sutta_name = m.group(2)

        suttas = abo.utils.split_sutta(nikaya_lines, matchs)
        assert len(suttas) == 1

        source_title_line, head_lines, body_lines = suttas[0]

        p = re.compile(r"^\d\.(.+品)$")
        pin_matchs = abo.utils.match_line(head_lines, [p])
        if pin_matchs:
            assert len(pin_matchs) == 1
            m = pin_matchs[0][0]
            pin_name = m.group(1)
            pin = []
            data.append(((None, None, pin_name), pin))

        body_lines = abo.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = abo.page_parsing.lines_to_es(body_lines)

        head_lines = abo.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = abo.page_parsing.lines_to_head(head_lines)

        sutta_num = "Pv." + sutta_serial
        sutta_nums = [
            (None, sutta_num),
            ("SC", "PV " + sutta_serial)
        ]

        xml = abo.utils.make_xml(source_page = htm,
                                 sutta_nums = sutta_nums,
                                 start = sutta_serial,
                                 end = sutta_serial,
                                 mtime = mtime,
                                 ctime = None,
                                 source_title = abo.utils.strip_crlf(source_title_line),
                                 relevant = None,
                                 title_line = [sutta_name],
                                 head = head,
                                 body_es= body,
                                 notes = notes)

        pin.append(((int(sutta_serial), int(sutta_serial), sutta_name), xml))

    return data