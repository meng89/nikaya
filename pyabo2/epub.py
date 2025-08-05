import uuid
from datetime import datetime
import math

import epubpacker
import xl

import pyabo2.utils
from . import css, js
from . import ebook_utils



def make_epub(data, module, lang):
    epub = epubpacker.Epub()

    epub.meta.titles = [lang.c(module.name_han)]
    epub.meta.creators = ["莊春江({})".format(lang.c("譯"))]
    ts = ebook_utils.read_timestamp(data)
    epub.meta.date = datetime.fromtimestamp(ts).astimezone().strftime("%Y-%m-%dT%H:%M:%SZ")
    epub.meta.languages = [lang.xmlang, "pi", "en-US"]

    my_uuid = get_uuid(lang.c(module.name_han) + lang.enlang)
    epub.meta.identifier = my_uuid.urn

    epub.meta.others.append(xl.Element("meta", {"property": "belongs-to-collection", "id": "c01"},
                                       ["莊春江" + lang.c("漢譯經藏")]))
    epub.meta.others.append(xl.Element("meta", {"refines": "#c01", "property": "collection-type"}, ["series"]))

    epub.userfiles[css.css1_path] = css.css1[lang.enlang]
    epub.userfiles[css.css2_path] = css.css2[lang.enlang]
    epub.userfiles[js.js1_path] = js.js1
    epub.userfiles["_css/user_css1.css"] = "/* 第一个自定义 CSS 文件 */\n\n"
    epub.userfiles["_css/user_css2.css"] = "/* 第二个自定义 CSS 文件 */\n\n"
    epub.userfiles["_js/user_js1.js"] = "// 第一个自定义 JS 文件\n\n"
    epub.userfiles["_js/user_js2.js"] = "// 第二个自定义 JS 文件\n\n"

    return epub


def write_suttas(epub, module, data, lang):
    for name, obj in data:
        if is_leaf(obj) and need_join_one_page(obj):





def need_join_one_page(obj):
    # 检查是否把这里面的所有页面都合并在一起
    # 因为有些经太短小，一些（哪些?）阅读器没有拼页功能，导致频繁翻页，上下相关的经文不在一个页面上。
    small_page = 0
    large_page = 0

    for xml in obj:
        real_line = 0
        root = xml.root
        body = root.find("body")[0]
        for p in body.find("p"):
            txt = pyabo2.utils.line_to_txt(p.kids)
            real_line += math.ceil(len(txt)/40)

        if real_line <= 30:
            small_page += 1
        else:
            large_page += 1

    if small_page/large_page > 1:
        return True
    else:
        return False



def is_leaf(obj: list):
    if isinstance(obj[0], list):
        return False
    else:
        return True





def write_cover(epub, module, data, lang):
    pass

def write_homage(epub, module, data, lang):
    pass

def write_notes(epub, module, data, lang):
    pass


def get_uuid(s):
    return uuid.uuid5(uuid.NAMESPACE_URL, "https://github.com/meng89/nikaya" + " " + s)

