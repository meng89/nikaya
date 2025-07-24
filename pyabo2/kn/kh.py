import re

import pyabo2.page_parsing
import pyabo2.utils


name_han = "小誦" # 自说经
name_pali = "Khuddakapāṭha"
short = "Kh"
htmls = ["Kh/Kh{}.htm".format(x) for x in range(1, 10)]


def load_from_htm():
    data = {}

    for htm in htmls:
        root, mtime, body_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        body = pyabo2.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = pyabo2.page_parsing.lines_to_body(body)

        _name = pyabo2.utils.get_name2(root)

        # todo report bug
        if htm == "Kh/Kh8.htm":
            _name = "8.部分財寶經"

        m = re.match(r"^(\d+)\.(\S+)$", _name)
        xml = pyabo2.utils.make_xml(m.group(1), m.group(1), m.group(2), mtime, None, body, notes)

        folder = pyabo2.utils.get_last_folder(data)
        folder["Kh{}".format(m.group(1))] = xml

    return data
