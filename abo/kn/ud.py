import re

import abo.page_parsing
import abo.utils
from share import Info


info = Info(
    name = "優陀那",
    pali = "Udāna",
    abbr = "Ud",
    translators = ("莊春江",),
    htmls = ["Ud/Ud{:0>2d}.htm".format(x) for x in range(1, 81)]
)


def load_from_htm():
    data = []
    pin = []
    pin_name = None
    sutta_serial = 0
    for htm in info.htmls:
        root, mtime, body_lines, notes, div_nikaya = abo.page_parsing.read_page(htm, 2)

        p = re.compile(r"^優陀那(\d+)經/(.+)\((\d)\.(.+品)\)\(莊春江譯\)(.*)$")
        matches = abo.utils.match_line(body_lines, [p])
        assert len(matches) == 1

        m = matches[0][0]

        pin_serial = m.group(3)
        new_pin_name = m.group(4)

        # todo report bug
        if new_pin_name == "天生失明品":
            new_pin_name = "天生失明者品"

        if pin_name != new_pin_name:
            pin_name = new_pin_name
            pin = []
            pin_name_whole = pin_serial + "." + new_pin_name
            data.append(((int(pin_serial), int(pin_serial), new_pin_name), pin))
            sutta_serial = 0

        suttas = abo.utils.split_sutta(body_lines, matches)
        assert len(suttas) == 1

        title_line, head_lines, sutta_body_lines = suttas[0]

        body = abo.page_parsing.htm_lines_to_xml_lines(sutta_body_lines)
        body = abo.page_parsing.lines_to_es(body)

        head = abo.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = abo.page_parsing.lines_to_head(head)

        sutta_serial += 1

        sutta_num = "Ud.{}".format(m.group(1))

        sutta_num_sc = "Ud {}.{}".format(pin_serial, sutta_serial)

        sutta_nums = [
            (None, sutta_num),
            ("SC", sutta_num_sc)
        ]

        xml = abo.utils.make_xml(source_page=htm,
                                 sutta_nums=sutta_nums,
                                 start=str(sutta_serial),
                                 end=str(sutta_serial),
                                 mtime=mtime,
                                 ctime=None,
                                 source_title=abo.utils.strip_crlf(matches[0][2]),
                                 relevant=m.group(5),
                                 title_line=[m.group(2)],
                                 head=head,
                                 body_es=body,
                                 notes=notes)

        pin.append(((sutta_serial, sutta_serial, m.group(2)), xml))

    return data
