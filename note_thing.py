import re
import bs4
import requests.exceptions

import utils
_data = {}


def load_global(domain: str):
    global _data
    for i in range(100):
        try:
            soup = utils.read_url(domain + "/note/note{}.htm".format(i))[0]
        except requests.exceptions.HTTPError:
            break

        for div in soup.find_all(name="div", attrs={"id": True}):
            note_no = re.match(r"^div(\d+)$", div["id"]).group(1)

            listline_list = read_one_note(div.contents)

            _data[note_no] = listline_list


def read_one_note(contents):
    """
    解析每条 noto
    :param contents:
    :return:
    """
    listline_list = []
    listline = []
    for one in contents:
        if isinstance(one, bs4.element.NavigableString):
            listline.append(one.get_text())
        elif one.name == "br":
            if listline:
                listline_list.append(listline)
                listline = []
        elif one.name == "a" and "href" in one.attrs.keys():
            listline.append(utils.Href(text=one.get_text(), href=one["href"], target=one["target"]))
    if listline:
        listline_list.append(listline)
    return listline_list


def get():
    return _data
