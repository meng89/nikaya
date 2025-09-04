import os.path
import re

import xl

import base
import pyabo2.page_parsing
import pyabo2.utils


name_han = "增支部"
name_pali = "Aṅguttara Nikāya"
short = "AN"
htmls = ["AN/AN{:0>4d}.htm".format(x) for x in range(1, 1765)]


def load_from_htm():
    data = []
    jp = None
    ze = None
    pin = None
    jp_seril = 0
    for htm in htmls:
        root, mtime, body_lines, notes, div_nikaya = pyabo2.page_parsing.read_page(htm, 2)

        p = re.compile(r"^增支部(\d+)集(\d+)(?:-(\d+))?經(?:/(\S+))?\(莊春江譯\)(.*)$")

        # 增支部3集63經[/恐懼經](莊春江譯)[SA.758]
        p2 = re.compile(r"^增支部(3)集(63)(\d)?經\[/(恐懼經)]\(莊春江譯\)(\[SA\.758])")

        matched = pyabo2.utils.match_line(body_lines, [p,p2])
        #if htm in ("AN/AN1527.htm", "AN/AN1529.htm", "AN/AN1532.htm"):
        #    matched.pop(-1)

        #assert len(matched) == 1



        _, head_lines, _ = pyabo2.utils.split_sutta(body_lines, matched)[0]

        jp_p = re.compile(r"^(\S+集篇)經典")
        jp_matched = pyabo2.utils.match_line(head_lines, [jp_p])
        if jp_matched:
            jp_seril += 1
            assert len(jp_matched) == 1
            jp_m = jp_matched[0][0]
            jp_name = jp_m.group(1)
            jp = []
            data.append(("{}.{}".format(jp_seril, jp_name), jp))
            ze = None
            pin = None

        ze_p = re.compile(r"^\d+\.(\S+則)")
        ze_matched = pyabo2.utils.match_line(head_lines, [ze_p])
        if ze_matched:
            assert len(ze_matched) == 1
            ze_m = ze_matched[0][0]
            ze_name = ze_m.group(1)
            ze = []
            jp.append((ze_name, ze))
            pin = None

        pin_p = re.compile(r"^\d+\.(\S+品\S*)")
        pin_p2 = re.compile(r"^\(\d+\) ?\d+\.(\S+品)")
        pin_matched = pyabo2.utils.match_line(head_lines, [pin_p, pin_p2])
        if pin_matched:
            assert len(pin_matched) == 1
            pin_m = pin_matched[0][0]
            pin_name = pin_m.group(1)
            pin = []
            if ze is not None:
                folder = ze
            else:
                folder = jp
            folder.append((pin_name, pin))


        suttas = pyabo2.utils.split_sutta(body_lines, matched)
        for index, match in enumerate(matched):
            m = matched[0][0]
            #jp_seril = m.group(1)
            start = m.group(2)
            end = m.group(3)
            if end is None:
                end = start
            name = m.group(4)

            source_title_line, head_lines, sutta_body_lines = suttas[index]

            body = pyabo2.page_parsing.htm_lines_to_xml_lines(sutta_body_lines)
            body = pyabo2.page_parsing.lines_to_body(body)

            head = pyabo2.page_parsing.htm_lines_to_xml_lines(head_lines)
            head = pyabo2.page_parsing.lines_to_head(head)

            if start == end:
                sutta_seril = "{}".format(start)
            else:
                sutta_seril = "{}-{}".format(start, end)
            sutta_num_abo = "AN.{}.{}".format(jp_seril, sutta_seril)
            sutta_num_sc = "AN {}.{}".format(jp_seril, sutta_seril)

            sutta_nums = [
                (None, sutta_num_abo),
                ("SC", sutta_num_sc)
            ]
            xml = pyabo2.utils.make_xml(source_page=htm,
                                        sutta_nums=sutta_nums,
                                        start=str(int(start)),
                                        end=str(int(end)),
                                        mtime=mtime,
                                        ctime=None,
                                        source_title=pyabo2.utils.strip_crlf(matched[0][2]),
                                        relevant=m.group(5),
                                        title_line=[name or "无名"],
                                        head=head,
                                        body=body,
                                        notes=notes)

            if pin is not None:
                folder = pin
            elif ze is not None:
                folder = ze
            else:
                raise Exception
            folder.append((sutta_num_sc, xml))
        #check_e(xml.root)

    return data


def check_e(e: xl.Element):
    print(e.tag)
    for kid in e.kids:
        if kid is None:
            print("xyz")
            exit()
        elif isinstance(kid, xl.Element):
            check_e(kid)
