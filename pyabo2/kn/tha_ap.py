import re


import pyabo2.page_parsing
import pyabo2.utils
from . import th


name_han = "長老阿波陀那" #譬喻
name_pali = "Therāpadāna"

htmls = ["Ap/Ap{}.htm".format(x) for x in range(1, 564)]

# 品名都是首经的名字，意义不大。这里经文编号依照 suttacentral 风格重编，品不参与编排经号。

short = "Tha-ap"


def load_form_htm():
    return load_from_htm_real(htmls, short)

def load_from_htm_real(_htmls, _short):
    data = {}
    pin: None or dict = None
    seril = 0
    for htm in _htmls:
        root, mtime, body_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        pin_lines = th.match_line(body_lines, [re.compile(r"^\d+.*品.*$")])
        ap_lines = th.match_line(body_lines, [re.compile(r"^\d+.*阿波陀那.*$")])

        if pin_lines:
            _seril, line = th.split_seril_title(pin_lines[0][1])
            assert len(line) == 1 and isinstance(line[0], str)
            pin_name = line[0]
            pin = {}
            data[pin_name] = pin


        assert len(ap_lines) == 1
        aps = th.split_sutta(body_lines, ap_lines)
        for title_line, head_lines, sutta_body_lines in aps:


            body = pyabo2.page_parsing.htm_lines_to_xml_lines(sutta_body_lines)
            body = pyabo2.page_parsing.lines_to_body(body)

            head = pyabo2.page_parsing.htm_lines_to_xml_lines(head_lines)
            head = pyabo2.page_parsing.lines_to_head(head)

            # todo report
            if title_line[0] == "\n3-8賓頭盧婆羅墮若[↝AN.1.195]":
                title_line[0] = "\n3-8.賓頭盧婆羅墮若[↝AN.1.195]"

            _seril, title_line = th.split_seril_title(title_line)
            #m = re.match("3-(\d)", seril)
            #if m:
            #    seril = str(int(m.group(1)) + 2)

            seril += 1

            sutta_num = "{}.{}".format(_short, seril)

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
            pin[filename] = xml

    return data