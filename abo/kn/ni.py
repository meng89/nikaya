import re

import abo.page_parsing
import abo.utils
from share import Info


da_htmls = ["Ni/Ni{}.htm".format(x) for x in range(1, 17)]
xiao_htmls = ["Ni/Ni{}.htm".format(x) for x in range(17, 40)]


info = Info(
    name = "義釋", #
    pali = "Niddesa",
    abbr = "Ni",
    translators = ("莊春江",),
    htmls = da_htmls + xiao_htmls,
)


# 与 SC 经号差别较大


def load_from_htm():
    data = [
        ((None, None, "大義釋"), load_(da_htmls)),
        ((None, None, "小義釋"), load_(xiao_htmls))
    ]
    return data


def load_(htmls_):
    data = []
    for htm in htmls_:
        root, mtime, body_lines, notes, div_nikaya = abo.page_parsing.read_page(htm, 2)

        m = abo.utils.get_name(root, re.compile(r"^(\d+)\.(.+(?:的說明|…)|序偈)$"))

        body = abo.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = abo.page_parsing.lines_to_es(body)

        xml = abo.utils.make_xml(source_page = htm,
                                 sutta_nums = [],
                                 start = m.group(1),
                                 end = m.group(1),
                                 mtime = mtime,
                                 ctime = None,
                                 source_title = None,
                                 relevant = None,
                                 title_line = [m.group(2)],
                                 head = None,
                                 body_es= body,
                                 notes = notes
                                 )
        m = re.match(r"Ni/(.*).htm", htm)
        data.append(((None, None, m.group(1)), xml))

    return data
