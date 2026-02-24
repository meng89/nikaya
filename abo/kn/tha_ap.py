import re

import abo.page_parsing
import abo.utils
from nikaya_share import Info


info = Info(
    name = "長老阿波陀那", #譬喻
    pali = "Therāpadāna",
    translators = ("莊春江",),
    abbr = "Tha-ap",
    htmls = ["Ap/Ap{}.htm".format(x) for x in range(1, 564)]
)

# 品名都是首经的名字，意义不大。这里经文编号依照 suttacentral 风格重编，品不参与编排经号。


def load_from_htm():
    return load_from_htm_real(info.htmls, info.abbr)


def load_from_htm_real(_htmls, _short):
    data = []
    pin = None
    sutta_serial = 0
    for htm in _htmls:
        root, mtime, nikaya_lines, notes, div_nikaya = abo.page_parsing.read_page(htm, 2)

        matchs = abo.utils.match_line(nikaya_lines, [re.compile(r"^\d+(?:-\d)?\.?(.+阿波陀那).*$")])
        assert len(matchs) == 1
        m = matchs[0][0]
        sutta_serial += 1
        sutta_name = m.group(1)

        aps = abo.utils.split_sutta(nikaya_lines, matchs)
        source_title_line, head_lines, body_lines = aps[0]

        pin_matchs = abo.utils.match_line(head_lines, [re.compile(r"^\d+\.(.+品).*$")])
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


        sutta_num = "{} {}".format(_short, sutta_serial)
        sutta_nums = [
            ("SC", sutta_num)
        ]

        xml = abo.utils.make_xml(source_page = htm,
                                 sutta_nums = sutta_nums,
                                 start = str(sutta_serial),
                                 end = str(sutta_serial),
                                 mtime = mtime,
                                 ctime = None,
                                 source_title = abo.page_parsing.htm_line_to_xml_line(abo.utils.strip_crlf(source_title_line)),
                                 relevant = None,
                                 title_line = [sutta_name],
                                 head = head,
                                 body_es= body,
                                 notes = notes
                                 )

        filename = "{}{}".format(_short, sutta_serial)
        pin.append(((int(sutta_serial), int(sutta_serial), sutta_name), xml))

    return data
