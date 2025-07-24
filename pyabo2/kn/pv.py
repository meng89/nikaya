import re

import xl

import pyabo2.page_parsing
import pyabo2.utils


name_han = "餓鬼事"
name_pali = "Petavatthu"
short = "Pv"
htmls = ["Pv/Pv{}.htm".format(x) for x in range(1, 52)]


def load_from_htm():
    data = {}
    pin: None or dict = None
    for htm in htmls:
        root, mtime, body_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        body = pyabo2.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = pyabo2.page_parsing.lines_to_body(body)

        pin_name = pyabo2.utils.get_pin_name2(body_lines)
        if pin_name:
            pin = {}
            data[pin_name] = pin

        _name = pyabo2.utils.get_name2(root)

        # todo report
        if htm == "Pv/Pv34.htm":
            _name = "9.欺瞞的裁判官"
        elif htm == "Pv/Pv44.htm":
            _name = "9.食糞女"

        m = re.match(r"^(\d+)\.(\S+)$", _name)
        print(_name)
        start = m.group(1)
        end = m.group(1)
        name = m.group(2)

        xml = pyabo2.utils.make_xml(start, end, name, mtime, None, body, notes)


        m = re.match("Pv/Pv(\d+).htm", htm)
        seril = m.group(1)
        pin["Pv{}".format(seril)] = xml

    return data