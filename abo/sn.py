import re

import abo.page_parsing
import abo.utils
from nikaya_share import base


info = base.Info(
    name = "相應部",
    pali = "Saṃyutta Nikāya",
    translators = ("莊春江",),
    abbr = "SN",
    htmls = ["SN/SN{:0>4d}.htm".format(x) for x in range(1, 1807)],
)


def load_from_htm():
    data = []
    pian = []
    xy = []
    pin = []

    for htm in info.htmls:
        root, mtime, body_lines, notes, div_nikaya = abo.page_parsing.read_page(htm, 2)

        # 相應部1相應1經/暴流之渡過經(諸天相應/有偈篇/祇夜)(莊春江譯)[SA.1267]
        # 相應部12相應72-81經/生經等十則(因緣相應/因緣篇/修多羅)(莊春江譯)
        # 相應部35相應 171-173經/苦-意欲等經(處相應/處篇/修多羅)(莊春江譯)
        # 相應45相應4經/若奴索尼婆羅門經(道相應/大篇/修多羅)(莊春江譯)[SA.769]
        p = re.compile(r"^相應部?(\d+)相應 ?(\d+)(?:-(\d+))?經/(.+)\(.+\)\(莊春江譯\)(.*)")

        # 相應部48相應 83-114經
        p2 = re.compile(r"^相應部(48)相應 (83)-(114)經()()()")

        # 相應部48相應 137-168經(根相應/大篇/修多羅)(莊春江譯)
        # ...
        p3 = re.compile(r"相應部(\d+)相應 ?(\d+)-(\d+)經\(\S+\)\(莊春江譯\)()()()")

        matched = abo.utils.match_line(body_lines, [p, p2, p3])

        if htm == "SN/SN0345.htm":
            matched.pop(-1)

        assert len(matched) == 1
        m = matched[0][0]
        xy_seril_1 = int(m.group(1))
        start = int(m.group(2))
        if m.group(3) is None:
            end = start
        else:
            end = int(m.group(3))

        name = m.group(4)
        tail = m.group(5)

        source_title_line, head_lines, sutta_body_lines = abo.utils.split_sutta(body_lines, matched)[0]

        pian_p = re.compile(r"^(?:\(\d\))?(.+篇)")
        pian_matched = abo.utils.match_line(head_lines, [pian_p])
        if pian_matched:
            assert len(pian_matched) == 1
            pian_m = pian_matched[0][0]
            pian_name = pian_m.group(1)
            pian = []
            data.append(((None, None, pian_name), pian))
            xy = None
            pin = None

        xy_p = re.compile(r"^(\d+)\.(?:\(\d+\)\.?)?(.+?相應)")
        xy_matched = abo.utils.match_line(head_lines, [xy_p])
        if xy_matched:
            assert len(xy_matched) == 1
            xy_m = xy_matched[0][0]
            xy_seril_2 = int(xy_m.group(1))
            assert xy_seril_1 == xy_seril_2
            xy_name = xy_m.group(2)
            xy = []
            pian.append(((xy_seril_2, xy_seril_2, xy_name), xy))
            pin = None

        pin_p = re.compile(r"^\d+\.(.+品)")
        pin_matched = abo.utils.match_line(head_lines, [pin_p])
        if pin_matched:
            assert len(pin_matched) == 1
            pin_m = pin_matched[0][0]
            pin_name = pin_m.group(1)
            pin = []
            xy.append(((None, None, pin_name), pin))


        if pin is not None:
            folder = pin
        else:
            folder = xy

        body = abo.page_parsing.htm_lines_to_xml_lines(sutta_body_lines)
        body_es = abo.page_parsing.lines_to_es(body)

        head = abo.page_parsing.htm_lines_to_xml_lines(head_lines)
        head = abo.page_parsing.lines_to_head(head)

        if start == end:
            sutta_num_abo = "SN.{}.{}".format(xy_seril_1, start)
            sutta_num_sc = "SN {}.{}".format(xy_seril_1, start)
        else:
            sutta_num_abo = "SN.{}.{}-{}".format(xy_seril_1, start, end)
            sutta_num_sc = "SN {}.{}-{}".format(xy_seril_1, start, end)


        sutta_nums = [
            (None, sutta_num_abo),
            ("SC", sutta_num_sc)
        ]

        xml = abo.utils.make_xml(source_page=htm,
                                 sutta_nums=sutta_nums,
                                 start=str(start),
                                 end=str(end),
                                 mtime=mtime,
                                 ctime=None,
                                 source_title=abo.utils.strip_crlf(matched[0][2]),
                                 relevant=tail,
                                 title_line=[name],
                                 head=head,
                                 body_es=body_es,
                                 notes=notes)

        folder.append(((start, end, name), xml))

    return data
