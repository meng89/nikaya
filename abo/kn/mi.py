import abo.page_parsing
import abo.utils
from nikaya_share import Info


info = Info(
    name = "彌蘭王問經",
    pali = "Milindapañha",
    abbr = "Mi",
    translators = ("莊春江",),
    htmls = ["Mi/Mi{}.htm".format(x) for x in range(1, 37)],
)


d = {
    "外談論": ["沙竭城", "過去業", "彌蘭王", "摩訶先那", "尊者那先", "證須陀洹", "證阿羅漢", "到沙竭城", "彌蘭往見"],

    "彌蘭之問": ["大品", "時間品", "伺品", "涅槃品", "佛陀品", "念品", "無色…品", "問答反思"],
    "難題之問": ["前言", "神通力品", "不該壞品", "被遣離品", "一切知品", "深交品"],
    "推論之問": ["佛陀品", "無虛妄品", "委散…品", "推論品"],
    "比喻之問": ["本母", "驢子品", "海洋品", "地品", "白蟻品", "獅子品", "猴子品", "水瓶品", "結論"]
}


def load_from_htm():
    data = []

    index = 0
    for l1_name, sutta_names in d.items():
        l1 = []
        data.append(((None, None, l1_name), l1))

        for sutta_name in sutta_names:
            index += 1
            htm = "Mi/Mi{}.htm".format(index)
            root, mtime, body_lines, notes, div_nikaya = abo.page_parsing.read_page(htm, 2)

            body = abo.page_parsing.htm_lines_to_xml_lines(body_lines)
            body = abo.page_parsing.lines_to_es(body)

            xml = abo.utils.make_xml(source_page=htm,
                                     sutta_nums=[],
                                     start=str(index),
                                     end=str(index),
                                     mtime=mtime,
                                     ctime=None,
                                     source_title=None,
                                     relevant=None,
                                     title_line=[sutta_name],
                                     head=None,
                                     body_es=body,
                                     notes=notes
                                     )

            l1.append(((None, None, sutta_name), xml))

    return data
