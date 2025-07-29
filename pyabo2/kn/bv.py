import re

import pyabo2.page_parsing
import pyabo2.utils
from . import th


name_han = "佛種姓"
name_pali = "Buddhavaṃsa"
short = "Bv"
htmls = ["Bv/Bv{}.htm".format(x) for x in range(1, 30)]




def load_from_htm():
    data = {}
    for htm in htmls:
        root, mtime, body_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        # todo report 3.燃燈佛種性
        sutta_lines = pyabo2.utils.match_line(body_lines, [re.compile(r"^\d+.*(佛種性|佛種姓|寶物經行處章|蘇昧達的願求說|種種佛章|遺骨的分配說).*$")])
        if sutta_lines[0][1][0] == "\n3.燃燈佛種性\n":
            sutta_lines[0][1][0] = "\n3.燃燈佛種姓\n"

        assert len(sutta_lines) == 1
        suttas = th.split_sutta(body_lines, sutta_lines)
        assert len(suttas) == 1

        title_line, head_lines, sutta_body_lines = suttas[0]

        body = pyabo2.page_parsing.htm_lines_to_xml_lines(sutta_body_lines)
        body = pyabo2.page_parsing.lines_to_body(body)

        head = pyabo2.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = pyabo2.page_parsing.lines_to_head(head)

        seril, title_line = th.split_seril_title(title_line)

        sutta_num = "{}.{}".format(short, seril)

        title_line = pyabo2.page_parsing.htm_line_to_xml_line(title_line)
        print(th.line_to_txt(title_line))
        xml = pyabo2.utils.make_xml(source_page=htm,
                                    sutta_num = sutta_num,
                                    start = str(seril),
                                    end = str(seril),
                                    mtime = mtime,
                                    ctime = None,
                                    title_line = title_line,
                                    head = head,
                                    body = body,
                                    notes = notes
                                    )

        filename = sutta_num
        data[filename] = xml

    return data