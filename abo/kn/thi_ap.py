from . import tha_ap
from share import Info


info = Info(
    name = "長老尼阿波陀那", #譬喻
    pali = "Therīapadāna",
    abbr = "Thi-ap", # 长老尼
    translators = ("莊春江",),
    htmls = ["Ap/Ap{}.htm".format(x) for x in range(564, 604)],
)

# 品名都是首经的名字，意义不大。这里经文编号依照 suttacentral 风格重编，品不参与编排经号。

def load_from_htm():
    return tha_ap.load_from_htm_real(info.htmls, info.abbr)
