import copy
import re

import pyabo2.page_parsing
import pyabo2.utils

name_han = "長老偈"
name_pali = "Theragāthā"
short = "Thag" # 例如：Thag.1.1。数字品名似乎只是为了分割大篇幅，意义不大。这里经文编号依照 suttacentral 风格重编，品不参与编排经号。

htmls = ["Th/Th{}.htm".format(x) for x in range(1, 113)]


def load_from_htm():
    data = []
    pian_seril = None
    pian = None
    pin = None


    ji_seril = None


    for htm in htmls:
        root, mtime, nikaya_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        matchs = pyabo2.utils.match_line(nikaya_lines, [re.compile(r"^\d+\.(.+長老偈).*$")])

        jis = pyabo2.utils.split_sutta(nikaya_lines, matchs)
        for source_title_line, head_lines, body_lines in jis:
            pian_p = re.compile(r"^(\d+)\.(.+集篇)$")
            pian_matchs = pyabo2.utils.match_line(head_lines, [pian_p])
            if pian_matchs:
                assert len(pian_matchs) == 1
                pian_m = pian_matchs[0][0]
                pian = []
                pian_num = pian_m.group(1) + pian_m.group(2)
                data.append((pian_num, pian))
                pin = None

            pin_p = re.compile(r"^\d+\.(.+品)$")
            pin_matchs = pyabo2.utils.match_line(head_lines, [pin_p])
            if pin_matchs:
                assert len(pin_matchs) == 1
                pin_m = pin_matchs[0][0]
                pin = []
                pian.append((pin_m.group(1), pin))



            body = pyabo2.page_parsing.htm_lines_to_xml_lines(body_lines)
            body = pyabo2.page_parsing.lines_to_body(body)

            head = pyabo2.page_parsing.htm_lines_to_xml_lines(head_lines)
            head = pyabo2.page_parsing.lines_to_head(head)

            seril, title_line = split_seril_title(title_line)
            if pin is not None:
                ji_seril += 1
            else:
                ji_seril = seril
            sutta_num = "Thag.{}.{}".format(pian_seril, ji_seril)

            title_line = pyabo2.page_parsing.htm_line_to_xml_line(title_line)
            print(line_to_txt(title_line))
            xml = pyabo2.utils.make_xml(source_page=htm,
                                        sutta_num = sutta_num,
                                        start = str(ji_seril),
                                        end = str(ji_seril),
                                        mtime = mtime,
                                        ctime = None,
                                        title_line = title_line,
                                        head = head,
                                        body = body,
                                        notes = notes
                                        )

            filename = sutta_num
            last_folder[filename] = xml

    return data





def strip_line(line: list):
    new_line = copy.deepcopy(line)
    if isinstance(new_line[0], str):
        new_line[0] = new_line[0].lstrip()
    if isinstance(new_line[-1], str):
        new_line[-1] = new_line[-1].rstrip()
    return new_line


