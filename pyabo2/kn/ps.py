import xl

import pyabo2.page_parsing


name_han = "無礙解道" #
name_pali = "Paṭisambhidāmagga"
short = "Ps"
htmls = ["Ps/Ps{}.htm".format(x) for x in range(1, 31)]



def get_name(root: xl.Element):
    tanlun_list = []
    for span in root.find_descendants("span"):
        if len(span.kids)  >= 0 and isinstance(span.kids[0], str):
            kid = span.kids[0].strip()
            if kid.endswith("談論"):
                tanlun_list.append(kid)
            else:
                print(kid)
    assert len(tanlun_list) == 1
    return tanlun_list[0]

def get_pin(body: xl.Element):
    pin_list = []
    for p in body.kids:
        if len(p.kids) == 1 and isinstance(p.kids[0], str):
            kid = p.kids[0].strip()
            if kid.endswith("品"):
                pin_list.append(kid)
    assert len(pin_list) == 1
    return pin_list[0]


def load_from_htm():
    data = {}
    for x in pyabo2.page_parsing.read_pages(htmls):
        open("1.xml", "w").write(x.to_str(try_self_closing=True))

        print(get_pin(x.find_kids("")))