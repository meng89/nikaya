import re

import abo.page_parsing
import abo.utils
from share import Info


info = Info(
    name = "長部",
    pali = "Digha Nikāya",
    translators = ("莊春江",),
    abbr = "DN",
    htmls = ["DN/DN{:0>2d}.htm".format(x) for x in range(1, 35)],
)


def load_from_htm():
    data = []
    pin = []

    for htm in info.htmls:
        root, mtime, body_lines, notes, div_nikaya = abo.page_parsing.read_page(htm, 2)

        # 長部1經/梵網經(戒蘊品[第一])(莊春江譯)[DA.21]
        p = re.compile(r"^長部(\d+)經/(\S+經)\(\S+\)\(莊春江譯\)(.*)")
        matched = abo.utils.match_line(body_lines, [p])
        assert len(matched) == 1
        m = matched[0][0]
        start = end = serial = m.group(1)
        name = m.group(2)
        relevant = m.group(3)

        source_title_line, head_lines, sutta_body_lines = abo.utils.split_sutta(body_lines, matched)[0]

        pin_p = re.compile(r"^\S+、(\S+品)(?:經典)?")
        pin_matched = abo.utils.match_line(head_lines, [pin_p])
        if pin_matched:
            assert len(pin_matched) == 1
            pin_m = pin_matched[0][0]
            pin_name = pin_m.group(1)
            pin = []
            data.append(((None, None, pin_name), pin))

        body = abo.page_parsing.htm_lines_to_xml_lines(sutta_body_lines)
        body = abo.page_parsing.lines_to_es(body)

        head = abo.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = abo.page_parsing.lines_to_head(head)

        sutta_num_abo = "DN.{}".format(serial)
        sutta_num_sc = "DN {}".format(serial)
        sutta_nums = [
            (None, sutta_num_abo),
            ("SC", sutta_num_sc)
        ]

        xml = abo.utils.make_xml(source_page=htm,
                                 sutta_nums=sutta_nums,
                                 start=start,
                                 end=end,
                                 mtime=mtime,
                                 ctime=None,
                                 source_title=abo.utils.strip_crlf(matched[0][2]),
                                 relevant=relevant,
                                 title_line=[name],
                                 head=head,
                                 body_es=body,
                                 notes=notes)

        pin.append(((int(start), int(end), name), xml))

    return data
