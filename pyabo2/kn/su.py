import re

import pyabo2.page_parsing
import pyabo2.utils


name_han = "經集"
name_pali = "Suttanipāta"
short = "Su"
htmls = ["Su/Su{}.htm".format(x) for x in range(1, 74)]

# todo report  Su/Su.js Su48htm 应为 Su48.htm


def load_from_htm():
    data = {}

    for htm in htmls:
        root, mtime, body_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        body = pyabo2.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = pyabo2.page_parsing.lines_to_body(body)

        _name = pyabo2.utils.get_name2(root)

        # todo report bug
        if htm == "Su/Su19.htm":
            _name = "7.婆羅門法經"
        elif htm == "Su/Su43.htm":
            _name = "5.最高的八個一組經"


        m = re.match(r"^(\d+)\.(\S+)$", _name)

        if htm == "Su/Su55.htm":
            start = None
            end = None
            name = "序偈"
        else:
            start = m.group(1)
            end = m.group(1)
            name = m.group(2)

        pin_name = pyabo2.utils.get_pin_name2(body_lines)
        if htm == "Su/Su39.htm":
            pin_name = "4.八偈品"
        if pin_name:
            data[pin_name] = {}

        xml = pyabo2.utils.make_xml(start, end, name, mtime, None, body, notes)

        folder = pyabo2.utils.get_last_folder(data)
        m = re.match("Su/Su(\d+).htm", htm)
        seril = m.group(1)
        folder["Su{}".format(seril)] = xml

    return data