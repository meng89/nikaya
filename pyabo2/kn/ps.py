import re

import pyabo2.page_parsing
import pyabo2.utils
from pyabo2.utils import get_name, make_xml, get_pin_name

name_han = "無礙解道" #
name_pali = "Paṭisambhidāmagga"
short = "Ps"
htmls = ["Ps/Ps{}.htm".format(x) for x in range(1, 31)]


def load_from_htm():
    data = {}
    for htm in htmls:
        x = pyabo2.page_parsing.read_page(htm, 2)
    #for x in pyabo2.page_parsing.read_pages(htmls, use_read_page2=True):
        root, mtime, body_lines, notes, div_nikaya = x

        body = pyabo2.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = pyabo2.page_parsing.lines_to_body(body)

        pin_name = get_pin_name(body_lines)
        _name = get_name(root, "談論")
        #_name = pyabo2.utils.get_name2(root)
        m = re.match(r"^(\d+)\.(\S+)$", _name)
        xml = make_xml(m.group(1), m.group(1), m.group(2), mtime, None, body, notes)

        name = m.group(2)

        if pin_name:
            data[pin_name] = {}

        folder = pyabo2.utils.get_last_folder(data)
        folder["Ps{}".format(m.group(1))] = xml

    return data
