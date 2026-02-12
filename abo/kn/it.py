import re


import abo.page_parsing
from abo.utils import get_last_folder

name_han = "如是語"
name_pali = "Itivuttaka"
short = "It"
htmls = ["It/It{:0>3d}.htm".format(x) for x in range(1, 113)]


def load_from_htm():
    data = []
    jipian_name = None
    jipian: None | list = None
    pin: None | list = None

    for htm in htmls:
        root, mtime, body_lines, notes, div_nikaya = abo.page_parsing.read_page(htm, 2)

        p = re.compile(r"^如是語(\d+)經/(.+)\((.*集篇)\)\(莊春江譯\)(.*)$")
        matches = abo.utils.match_line(body_lines, [p])
        assert len(matches) == 1

        m = matches[0][0]

        new_jipian_name = m.group(3)

        if jipian_name != new_jipian_name:
            jipian = []
            jipian_name = new_jipian_name
            data.append((jipian_name, jipian))
            pin = None


        suttas = abo.utils.split_sutta(body_lines, matches)
        assert len(suttas) == 1

        title_line, head_lines, sutta_body_lines = suttas[0]

        pin_matchs = abo.utils.match_line(head_lines, [re.compile(r"^(?:\d\.)?(.+品)$")])
        if pin_matchs:
            assert len(pin_matchs) == 1
            pin_m = pin_matchs[0][0]
            pin_name = pin_m.group(1)
            pin = []
            jipian.append((pin_name, pin))

        body = abo.page_parsing.htm_lines_to_xml_lines(sutta_body_lines)
        body = abo.page_parsing.lines_to_es(body)

        head = abo.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = abo.page_parsing.lines_to_head(head)

        sutta_serial = m.group(1)

        sutta_num = "{}.{}".format(short, sutta_serial)
        sutta_nums = [
            (None, sutta_num),
            ("SC", "Iti {}".format(sutta_serial))
        ]

        xml = abo.utils.make_xml(source_page=htm,
                                 sutta_nums=sutta_nums,
                                 start=sutta_serial,
                                 end=sutta_serial,
                                 mtime=mtime,
                                 ctime=None,
                                 source_title=abo.utils.strip_crlf(matches[0][2]),
                                 relevant=m.group(4),
                                 title_line=[m.group(2)],
                                 head=head,
                                 body_es=body,
                                 notes=notes)

        if pin is not None:
            pin.append((sutta_num, xml))
        else:
            jipian.append((sutta_num, xml))

    return data