import copy
import re

import pyabo2.page_parsing
import pyabo2.utils


name_han = "長老偈"
name_pali = "Theragāthā"
short = "Thag" # 例如：Thag.1.1。数字品名似乎只是为了分割大篇幅，意义不大。这里经文编号依照 suttacentral 风格重编，品不参与计算经号。

htmls = ["Th/Th{}.htm".format(x) for x in range(1, 113)]


def load_from_htm():
    data = []
    pian_serial = None
    pian = None
    ji_serial = 0

    last = None

    for htm in htmls:
        root, mtime, nikaya_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        matchs = pyabo2.utils.match_line(nikaya_lines, [re.compile(r"^\d+\.(.+長老偈).*$")])

        jis = pyabo2.utils.split_sutta(nikaya_lines, matchs)

        _, _head_lines , _ = jis[0]

        pian_p = re.compile(r"^(\d+)\.(.+集篇)$")
        pian_matchs = pyabo2.utils.match_line(_head_lines, [pian_p])
        if pian_matchs:
            assert len(pian_matchs) == 1
            pian_m = pian_matchs[0][0]
            pian = []
            pian_serial = pian_m.group(1)
            pian_name = pian_m.group(2)
            pian_num = pian_serial + "." + pian_name
            data.append((pian_num, pian))
            last = pian
            ji_serial = 0

        pin_p = re.compile(r"^\d+\.(.+品)$")
        pin_matchs = pyabo2.utils.match_line(_head_lines, [pin_p])
        if pin_matchs:
            assert len(pin_matchs) == 1
            pin_m = pin_matchs[0][0]
            pin = []
            pian.append((pin_m.group(1), pin))
            last = pin


        for index, (source_title_line, head_lines, body_lines) in enumerate(jis):
            m = matchs[index][0]
            ji_serial += 1
            sutta_name = m.group(1)

            body_lines = pyabo2.page_parsing.htm_lines_to_xml_lines(body_lines)
            body = pyabo2.page_parsing.lines_to_body(body_lines)

            head_lines = pyabo2.page_parsing.htm_lines_to_xml_lines(head_lines)
            head = pyabo2.page_parsing.lines_to_head(head_lines)

            sutta_num = "Thag.{}.{}".format(pian_serial, ji_serial)

            sutta_nums = [
                (None, sutta_num),
                ("SC", "Thag {}.{}".format(pian_serial, ji_serial))
            ]

            xml = pyabo2.utils.make_xml(source_page = htm,
                                        sutta_nums = sutta_nums,
                                        start = str(ji_serial),
                                        end = str(ji_serial),
                                        mtime = mtime,
                                        ctime = None,
                                        source_title = pyabo2.utils.strip_crlf(source_title_line),
                                        relevant=None,
                                        title_line = sutta_name,
                                        head = head,
                                        body = body,
                                        notes = notes,
                                        )

            last.append((sutta_num, xml))

    return data
