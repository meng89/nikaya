import re

import abo.page_parsing
import abo.utils


name_han = "法句"
name_pali = "Dhammapada"
short = "Dh"
htmls = ["Dh/Dh{}.htm".format(x) for x in range(1, 27)]

# SC 的经号是每一个偈子就是一个经


def load_from_htm():
    data = []

    for htm in htmls:
        root, mtime, nikaya_lines, notes, div_nikaya = abo.page_parsing.read_page(htm, 2)

        matchs = abo.utils.match_line(nikaya_lines, [re.compile(r"(\d+)\.(.+品.*)")])
        assert len(matchs) == 1

        m = matchs[0][0]
        sutta_serial = m.group(1)
        sutta_name = m.group(2)

        suttas = abo.utils.split_sutta(nikaya_lines, matchs)
        assert len(suttas) == 1
        source_title_line, head_lines, body_lines = suttas[0]

        sutta_serial, title_line = abo.utils.split_serial_title(source_title_line)

        head_lines = abo.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = abo.page_parsing.lines_to_head(head_lines)

        body = abo.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = abo.page_parsing.lines_to_es(body)

        sutta_num = "Dh." + sutta_serial
        sutta_nums = [
            (None, sutta_num),
        ]
        xml = abo.utils.make_xml(source_page=htm,
                                 sutta_nums=sutta_nums,
                                 start=m.group(1),
                                 end=m.group(1),
                                 mtime=mtime,
                                 ctime=None,
                                 source_title=abo.utils.strip_crlf(source_title_line),
                                 relevant=None,
                                 title_line=title_line,
                                 head=head,
                                 body_es=body,
                                 notes=notes
                                 )

        data.append((sutta_num, xml))

    return data