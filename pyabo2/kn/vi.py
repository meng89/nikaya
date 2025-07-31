import re

import xl

import pyabo2.page_parsing
import pyabo2.utils


name_han = "天宮事"
name_pali = "Vimānavatthu"
short = "Vi"
htmls = ["Vi/Vi{}.htm".format(x) for x in range(1, 86)]



def load_from_htm():
    data = []
    pin = None
    pin_seril = None

    sutta_seril = 0

    for htm in htmls:
        root, mtime, nikaya_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)
        p = re.compile(r"^(\d+)\.(.+(?:經|所問|偈))(?:\(\d+\.\))?(.*)$")
        matchs = pyabo2.utils.match_line(nikaya_lines, [p, p2])
        print(matchs)
        assert len(matchs) == 1
        m = matchs[0][0]

        print(m.group(1), m.group(2), m.group(3))

        suttas = pyabo2.utils.split_sutta(nikaya_lines, matchs)
        assert len(suttas) == 1
        source_title_line, head_lines, body_lines = suttas[0]

        #_sutta_seril, title_line = pyabo2.utils.split_seril_title(source_title_line)

        pin_matchs = pyabo2.utils.match_line(head_lines, [re.compile(r"^(\d+)\.(.+品(?:\(.+品\))?)$")])
        if pin_matchs:
            assert len(pin_matchs) == 1
            pin_m = pin_matchs[0][0]
            pin_seril = pin_m.group(1)
            pin_num = "{}.{}".format(pin_m.group(1), pin_m.group(2))
            pin = []
            data.append((pin_num, pin))
            sutta_seril = 0

        head_lines = pyabo2.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = pyabo2.page_parsing.lines_to_body(head_lines)

        body = pyabo2.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = pyabo2.page_parsing.lines_to_body(body)

        sutta_seril += 1
        sutta_num = "Su.{}.{}".format(pin_seril, sutta_seril)
        sutta_nums = [
            (None, sutta_num)
        ]

        xml = pyabo2.utils.make_xml(source_page=htm,
                                    sutta_nums=sutta_nums,
                                    start=str(sutta_seril),
                                    end=str(sutta_seril),
                                    mtime=mtime,
                                    ctime=None,
                                    source_title=source_title_line,
                                    relevant=m.group(3),
                                    title_line=m.group(2),
                                    head=head,
                                    body=body,
                                    notes=notes
                                    )
        pin.append((sutta_num, xml))

    return data



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


def load_from_htm2():
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