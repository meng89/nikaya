import re

import abo.page_parsing
import abo.utils
from nikaya_share import Info


info = Info(
    name = "佛種姓",
    pali = "Buddhavaṃsa",
    abbr = "Bv",
    translators = ("莊春江",),
    htmls = ["Bv/Bv{}.htm".format(x) for x in range(1, 30)],
)


def load_from_htm():
    data = []
    for htm in info.htmls:
        root, mtime, nikaya_lines, notes, div_nikaya = abo.page_parsing.read_page(htm, 2)

        # todo report 3.燃燈佛種性
        matchs = abo.utils.match_line(nikaya_lines, [re.compile(r"^(\d+)\.(.*(?:佛種性|佛種姓|寶物經行處章|蘇昧達的願求說|種種佛章|遺骨的分配說)).*$")])
        assert len(matchs) == 1

        m = matchs[0][0]
        sutta_serial = m.group(1)
        sutta_name = m.group(2)

        suttas = abo.utils.split_sutta(nikaya_lines, matchs)
        source_title_line, head_lines, body_lines = suttas[0]


        body_lines = abo.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = abo.page_parsing.lines_to_es(body_lines)

        head_lines = abo.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = abo.page_parsing.lines_to_head(head_lines)

        sutta_num = "{}.{}".format(info.abbr, sutta_serial)
        sutta_nums = [
            (None, sutta_num),
            ("SC", "{} {}".format(info.abbr, sutta_serial))
        ]

        xml = abo.utils.make_xml(source_page = htm,
                                 sutta_nums = sutta_nums,
                                 start = sutta_serial,
                                 end = sutta_serial,
                                 mtime = mtime,
                                 ctime = None,
                                 source_title = abo.page_parsing.htm_line_to_xml_line(abo.utils.strip_crlf(source_title_line)),
                                 relevant = None,
                                 title_line = [sutta_name],
                                 head = head,
                                 body_es= body,
                                 notes = notes
                                 )

        data.append(((int(sutta_serial), int(sutta_serial), sutta_name), xml))

    return data
