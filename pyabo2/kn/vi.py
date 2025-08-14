import re

import xl

import pyabo2.page_parsing
import pyabo2.utils


name_han = "天宮事"
name_pali = "Vimānavatthu"
short = "Vi"
htmls = ["Vi/Vi{}.htm".format(x) for x in range(1, 86)]



def load_from_htm():
    data = []
    sexual_tiangong = None
    pin = None

    sutta_serial = None

    after_18 = False

    for htm in htmls:
        root, mtime, nikaya_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)


        p = re.compile(r"^(\d+)\.(.+(?:天宮事|忠貞者).*)$")

        if htm == "Vi/Vi18.htm" or after_18:
            after_18 = True
            p = re.compile(r"^(\d+)\.(.+天宮事.*)\((\d+)\.\)(.+)?\*?$")

        matchs = pyabo2.utils.match_line(nikaya_lines, [p])
        assert len(matchs) == 1
        m = matchs[0][0]

        try:
            sutta_serial = m.group(3)
        except IndexError:
            sutta_serial = m.group(1)
        sutta_name = m.group(2)

        try:
            relevant = m.group(4)
        except IndexError:
            relevant = None

        suttas = pyabo2.utils.split_sutta(nikaya_lines, matchs)
        assert len(suttas) == 1
        source_title_line, head_lines, body_lines = suttas[0]


        p = re.compile(r"^\d\.(女子天宮|男子天宮)$")
        sexual_matchs = pyabo2.utils.match_line(head_lines, [p])
        if sexual_matchs:
            assert len(sexual_matchs) == 1
            m = sexual_matchs[0][0]
            s_tg_name = m.group(1)
            sexual_tiangong = []
            data.append((s_tg_name, sexual_tiangong))
            pin = None

        p = re.compile(r"^\d\.(.+品)$")
        pin_matchs = pyabo2.utils.match_line(head_lines, [p])
        if pin_matchs:
            assert len(pin_matchs)
            m = pin_matchs[0][0]
            pin_name = m.group(1)
            pin = []
            sexual_tiangong.append((pin_name, pin))


        head_lines = pyabo2.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = pyabo2.page_parsing.lines_to_body(head_lines)

        body = pyabo2.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = pyabo2.page_parsing.lines_to_body(body)

        sutta_num = "Vi.{}".format(sutta_serial)
        sutta_nums = [
            (None, sutta_num),
            ("SC", "Vv {}".format(sutta_serial))
        ]

        xml = pyabo2.utils.make_xml(source_page = htm,
                                    sutta_nums = sutta_nums,
                                    start = sutta_serial,
                                    end = sutta_serial,
                                    mtime = mtime,
                                    ctime = None,
                                    source_title = pyabo2.utils.strip_crlf(source_title_line),
                                    relevant = relevant,
                                    title_line = [sutta_name],
                                    head = head,
                                    body = body,
                                    notes = notes
                                    )
        pin.append((sutta_num, xml))

    return data
