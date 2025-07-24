import re

import pyabo2.page_parsing
import pyabo2.utils


name_han = "法句"
name_pali = "Dhammapada"
short = "Dh"
htmls = ["Dh/Dh{}.htm".format(x) for x in range(1, 27)]



def load_from_htm():
    data = {}

    for htm in htmls:
        root, mtime, body_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        body = pyabo2.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = pyabo2.page_parsing.lines_to_body(body)

        _name = pyabo2.utils.get_name2(root)

        m = re.match(r"^(\d+)\.(\S+)$", _name)
        xml = pyabo2.utils.make_xml(m.group(1), m.group(1), m.group(2), mtime, None, body, notes)

        folder = pyabo2.utils.get_last_folder(data)
        folder["Dh{}".format(m.group(1))] = xml

    return data