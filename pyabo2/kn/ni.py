import re


import pyabo2.page_parsing
import pyabo2.utils


name_han = "義釋" # 大与小
name_pali = "Niddesa"
short = "Ni"
da_htmls = ["Ni/Ni{}.htm".format(x) for x in range(1, 17)]
xiao_htmls = ["Ni/Ni{}.htm".format(x) for x in range(17, 40)]
htmls = da_htmls + xiao_htmls


def load_from_htm():
    data = {}
    data["大義釋"] = _load(da_htmls)
    data["小義釋"] = _load(xiao_htmls)
    return data


def _load(_htmls):
    data = {}
    for html in _htmls:
        x = pyabo2.page_parsing.read_page(html, 2)
    #for x in pyabo2.page_parsing.read_pages(_htmls, use_read_page2=True):
        root, mtime, body_lines, notes, div_nikaya = x

        body = pyabo2.page_parsing.htm_lines_to_xml_lines(body_lines)
        body = pyabo2.page_parsing.lines_to_body(body)

        _name = pyabo2.utils.get_name2(root)

        #try:
        #   _name = pyabo2.utils.get_name(root, "說明")
        #except pyabo2.utils.AnalysisFailed as E:
        #    if html == "Ni/Ni39.htm":
        #        _name = "39.犀牛角4的說明"
        #    elif html == "Ni/Ni17.htm":
        #        _name = "17.序偈"
        #    else:
        #        raise E

        m = re.match(r"^(\d+)\. ?(\S+)$", _name)
        xml = pyabo2.utils.make_xml(m.group(1), m.group(1), m.group(2), mtime, None, body, notes)

        folder = pyabo2.utils.get_last_folder(data)
        folder["Ni{}".format(m.group(1))] = xml

    return data