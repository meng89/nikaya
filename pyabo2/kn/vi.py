import re

import xl

import pyabo2.page_parsing
import pyabo2.utils


name_han = "天宮事"
name_pali = "Vimānavatthu"
short = "Vi"
htmls = ["Vi/Vi{}.htm".format(x) for x in range(1, 86)]


def _get_tiangong_name(body_lines):
    tiangongs = []
    for line in body_lines:
        if len(line) == 1 and isinstance(line[0], str):
            kid = line[0].strip()
            if kid.endswith("天宮"):
                m = re.match(r"^\d+\.(\S+)$", kid)
                tiangongs.append(m.group(1))


    if len(tiangongs) > 1:
        raise pyabo2.utils.AnalysisFailed(tiangongs)

    if tiangongs:
        return tiangongs[0]
    else:
        return None


def load_from_htm():
    data = {}

    tiangong: dict or None = None

    for htm in htmls:
        root, mtime, body_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        body = pyabo2.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = pyabo2.page_parsing.lines_to_body(body)

        tiangong_name = _get_tiangong_name(body_lines)
        if tiangong_name:
            tiangong = {}
            data[tiangong_name] = tiangong

        pin_name = pyabo2.utils.get_pin_name2(body_lines)
        if pin_name:
            last = pyabo2.utils.get_last_folder(data)
            tiangong[pin_name] = {}

        _name = pyabo2.utils.get_name2(root)

        m = re.match(r"^(\d+)\.(\S+)$", _name)
        if m:
            start = m.group(1)
            end = m.group(1)
            name = m.group(2)
        m = re.match(r"^(椅子)(\d)$", _name)
        if m:
            start = m.group(2)
            end = m.group(2)
            name = _name

        xml = pyabo2.utils.make_xml(start, end, name, mtime, None, body, notes)

        folder = pyabo2.utils.get_last_folder(data)
        m = re.match("Vi/Vi(\d+).htm", htm)
        seril = m.group(1)
        folder["Vi{}".format(seril)] = xml

    return data