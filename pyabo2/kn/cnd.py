from . import mnd

name_han = "大義釋" # 大与小
name_pali = "Mahāniddesa"
short = "Cnd"

htmls = ["Ni/Ni{}.htm".format(x) for x in range(17, 40)]


def load_from_htm():
    return mnd.load_(htmls, short)
