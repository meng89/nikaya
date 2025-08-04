import re

import pyabo2.page_parsing
import pyabo2.utils


name_han = "法句"
name_pali = "Dhammapada"
short = "Dh"
htmls = ["Dh/Dh{}.htm".format(x) for x in range(1, 27)]

# SC 的经号是每一个偈子就是一个经


def load_from_htm():
    data = []

    for htm in htmls:
        root, mtime, nikaya_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        matchs = pyabo2.utils.match_line(nikaya_lines, [re.compile(r"(\d+)\.(.+品.*)")])
        assert len(matchs) == 1

        m = matchs[0][0]
        sutta_seril = m.group(1)
        sutta_name = m.group(2)

        suttas = pyabo2.utils.split_sutta(nikaya_lines, matchs)
        assert len(suttas) == 1
        source_title_line, head_lines, body_lines = suttas[0]

        sutta_seril, title_line = pyabo2.utils.split_seril_title(source_title_line)

        head_lines = pyabo2.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = pyabo2.page_parsing.lines_to_body(head_lines)

        body = pyabo2.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = pyabo2.page_parsing.lines_to_body(body)

        sutta_num = "Dh." + sutta_seril
        sutta_nums = [
            (None, sutta_num),
        ]
        xml = pyabo2.utils.make_xml(source_page=htm,
                                    sutta_nums=sutta_nums,
                                    start=m.group(1),
                                    end=m.group(1),
                                    mtime=mtime,
                                    ctime=None,
                                    source_title=pyabo2.utils.strip_crlf(source_title_line),
                                    relevant=None,
                                    title_line=title_line,
                                    head=head,
                                    body=body,
                                    notes=notes
                                    )

        data.append((sutta_num, xml))

    return data