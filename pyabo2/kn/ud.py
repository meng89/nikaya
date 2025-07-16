import os.path

import pyabo2.page_parsing

name_han = "優陀那" # 自说经
name_pali = "Udānapāḷi"
short = "Ud"
htmls = ["Ud/Ud{:0>2d}.htm".format(x) for x in range(1, 81)]


try:
    import user_config as config
except ImportError:
    import config as config


def trans_files():
    for x in pyabo2.page_parsing.read_pages(htmls):
