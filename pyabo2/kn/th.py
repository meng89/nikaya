import copy
import re

import pyabo2.page_parsing
import pyabo2.utils

name_han = "長老偈"
name_pali = "Theragāthā"
short = "Thag" # 例如：Thag.1.1。数字品名似乎只是为了分割大篇幅，意义不大。这里经文编号依照 suttacentral 风格重编，品不参与编排经号。

htmls = ["Th/Th{}.htm".format(x) for x in range(1, 113)]


def load_from_htm():
    data = {}
    pian_seril = None
    pian: None or dict = None
    pin: None or dict = None
    last_folder: None or dict = None

    ji_seril = None


    for htm in htmls:
        root, mtime, body_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        pian_lines = match_line(body_lines, ["集篇"])
        pin_lines = match_line(body_lines, ["品"])
        ji_lines = match_line(body_lines, [re.compile(r"^\d+.*長老偈.*$")])

        if pian_lines:
            ji_seril, line = split_seril_title(pian_lines[0][1])
            assert len(line) == 1 and isinstance(line[0], str)
            pian_seril = ji_seril
            pian_name = "{}.{}".format(ji_seril, line[0])
            pian = {}
            data[pian_name] = pian
            last_folder = pian

            pin = None
            ji_seril = 0

        if pin_lines:
            _seril, line = split_seril_title(pin_lines[0][1])
            assert len(line) == 1 and isinstance(line[0], str)
            pin_name = line[0]
            pin = {}
            pian[pin_name] = pin
            last_folder = pin

        assert ji_lines
        jis = split_sutta(body_lines, ji_lines)
        for title_line, head_lines, sutta_body_lines in jis:


            body = pyabo2.page_parsing.htm_lines_to_xml_lines(sutta_body_lines)
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


