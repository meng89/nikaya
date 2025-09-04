import os.path
import re


import xl

import base
import pyabo2.page_parsing
import pyabo2.utils


name_han = "中部"
name_pali = "Majjhima Nikāya"
short = "MN"
htmls = ["MN/MN{:0>3d}.htm".format(x) for x in range(1, 153)]


def load_from_htm():
    data = []
    jd = None
    pin = None

    for htm in htmls:
        root, mtime, body_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        # 中部1經/根本法門經(根本法門品[1])(莊春江譯)[MA.106, AA.44.6]
        p = re.compile(r"^中部(\d+)經/(\S+經\S*?)\(\S+\)\(莊春江譯\)(.*)")
        matched = pyabo2.utils.match_line(body_lines, [p])
        assert len(matched) == 1
        m = matched[0][0]
        start = end = m.group(1)
        name = m.group(2)
        relevant = m.group(3)

        source_title_line, head_lines, sutta_body_lines = pyabo2.utils.split_sutta(body_lines, matched)[0]

        jd_m = re.compile(r"^(\S+經典)")
        jd_matched = pyabo2.utils.match_line(head_lines, [jd_m])
        if jd_matched:
            assert len(jd_matched) == 1
            m = jd_matched[0][0]
            jd_name = m.group(1)
            jd = []
            data.append((jd_name, jd))
            pin = None


        pin_m = re.compile(r"^\d+\.(\S+品)")
        pin_matched = pyabo2.utils.match_line(head_lines, [pin_m])
        if pin_matched:
            assert len(pin_matched) == 1
            m = pin_matched[0][0]
            pin_name = m.group(1)
            pin = []
            jd.append((pin_name, pin))

        body = pyabo2.page_parsing.htm_lines_to_xml_lines(sutta_body_lines)
        body = pyabo2.page_parsing.lines_to_body(body)

        head = pyabo2.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = pyabo2.page_parsing.lines_to_head(head)

        sutta_num_abo = "MN.{}".format(start)

        sutta_num_sc = "MN {}".format(start)

        sutta_nums = [
            (None, sutta_num_abo),
            ("SC", sutta_num_sc)
        ]

        xml = pyabo2.utils.make_xml(source_page=htm,
                                    sutta_nums=sutta_nums,
                                    start=start,
                                    end=end,
                                    mtime=mtime,
                                    ctime=None,
                                    source_title=pyabo2.utils.strip_crlf(matched[0][2]),
                                    relevant=relevant,
                                    title_line=[name],
                                    head=head,
                                    body=body,
                                    notes=notes)

        pin.append((sutta_num_sc, xml))

    return data
