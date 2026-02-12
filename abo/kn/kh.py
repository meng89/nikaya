import re

import abo.page_parsing
import abo.utils


name_han = "小誦" # 自说经
name_pali = "Khuddakapāṭha"
short = "Kh"
htmls = ["Kh/Kh{}.htm".format(x) for x in range(1, 10)]


def load_from_htm():
    data = []

    for htm in htmls:
        root, mtime, body_lines, notes, div_nikaya = abo.page_parsing.read_page(htm, 2)

        parttern = re.compile(r"(\d)\.(三歸依|十學處|三十二行相|童問.*|.+經.*)")
        matchs = abo.utils.match_line(body_lines, [parttern])
        assert len(matchs) == 1

        m = matchs[0][0]
        sutta_serial = m.group(1)
        sutta_name = m.group(2)

        suttas = abo.utils.split_sutta(body_lines, matchs)
        assert len(suttas) == 1
        source_title_line, head_lines, body_lines = suttas[0]

        _sutta_serial, title_line = abo.utils.split_serial_title(source_title_line)

        head = abo.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = abo.page_parsing.lines_to_head(head)

        body = abo.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = abo.page_parsing.lines_to_es(body)

        _name = abo.utils.get_name2(root)

        # todo report bug
        if htm == "Kh/Kh8.htm":
            _name = "8.部分財寶經"

        sutta_num = "Kh." + sutta_serial
        sutta_nums = [
            (None, sutta_num),
            ("SC", "Kh " + sutta_serial)
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
