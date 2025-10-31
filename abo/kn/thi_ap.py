from . import tha_ap


name_han = "長老尼阿波陀那" #譬喻
name_pali = "Therīapadāna"

htmls = ["Ap/Ap{}.htm".format(x) for x in range(564, 604)]

# 品名都是首经的名字，意义不大。这里经文编号依照 suttacentral 风格重编，品不参与编排经号。

short = "Thi-ap" # 长老尼


def load_from_htm():
    return tha_ap.load_from_htm_real(htmls, short)
