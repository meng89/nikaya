import re
import bs4
import requests.exceptions

import utils
data = None


def load_data(url: str):
    global data
    d = {}
    for x in range(20):
        try:
            soup = utils.read_url(url+"/note/note{}.htm".format(x))[0]
        except requests.exceptions.HTTPError:
            break

        for div in soup.find_all(name="div", attrs={"id": True}):
            note_no = re.match(r"^div(\d+)$", div["id"]).group(1)
            line_list = []
            for c in div.contents:
                if c.name == "br":
                    pass
                else:
                    line_list.append(c.get_text())
            d[note_no] = line_list

