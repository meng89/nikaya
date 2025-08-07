import os.path
import re
import uuid
from datetime import datetime
import math
import posixpath
from urllib.parse import urlsplit

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
            write_one_page(epub, module, obj, lang)


def write_sutta(epub, module, data, lang):
    pass


def write_one_page(epub, module, parent_path, name, obj, lang):
    doc_path = posixpath.join(parent_path, name) + ".xhtml"
    html, body = make_doc(doc_path, lang, title=name)

    for sub_name, sub_obj in obj:


def sub_range(sub_data):
    for name, obj in sub_data:
        if isinstance(obj, list):
            m = re.match(r"^(\d+)\..+$", name)
            if m:
                return get_range_list(sub_data)
        elif isinstance(obj, xl.Xml):
            return get_range_xml(sub_data)

    raise Exception("No serial type found")


def is_serialized_list(name, obj):
    if isinstance(obj, list) and re.match(r"^(\d+)\..+$", name):
        return True
    return False


def get_range_list(data):
    start = None
    end = None
    for name, obj in data:
        if isinstance(obj, list):
            m = re.match(r"^(\d+)\..+$", name)
            start = ebook_utils.any_min(start, m.group(1))
            end = ebook_utils.any_max(start, m.group(1))

            sub_start, sub_end = get_range_list(obj)
            start = ebook_utils.any_min(start, sub_start)
            end = ebook_utils.any_max(end, sub_end)

    return start, end


def get_range_xml(data):
    start = None
    end = None
    for name, obj in data:
        if isinstance(obj, xl.Xml):
            start = ebook_utils.any_min(start, obj.root.find_descendants("start")[0].kids[0])
            end = ebook_utils.any_max(end, obj.root.find_descendants("end")[0].kids[0])
        elif isinstance(obj, list):
            _start, _end = get_range_xml(data)
            start = ebook_utils.any_min(start, _start)
            end = ebook_utils.any_max(end, _end)
    return start, end


def need_join_one_page(obj):
    # 检查是否把这里面的所有页面都合并在一起
    # 因为有些经太短小，一些（哪些?）阅读器没有拼页功能，导致频繁翻页，上下相关的经文不在一个页面上。
    small_page = 0
    large_page = 0

    for xml in obj:
        line_count = 0
        root = xml.root
        body = root.find("body")[0]
        for p in body.find("p"):
            txt = pyabo2.utils.line_to_txt(p.kids)
            line_count += math.ceil(len(txt)/40)

        if line_count <= 30:
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



def make_doc(doc_path, lang, title=None):
    html = xl.Element("html", {"xmlns:epub": "http://www.idpf.org/2007/ops",
                               "xmlns": "http://www.w3.org/1999/xhtml",
                               "xml:lang": lang.xmlang,
                               "lang": lang.xmlang})
    head = html.ekid("head")

    if title:
        _title = head.ekid("title", kids=[title])

    _make_css_link(head, relpath(css.css1_path, doc_path), "css1")
    _make_css_link(head, relpath("_css/user_css1.css", doc_path), "user_css1")
    _make_css_link(head, relpath("_css/user_css2.css", doc_path), "user_css2")
    _make_js_link(head, relpath(js.js1_path, doc_path), "js1")
    _make_js_link(head, relpath("_js/user_js1.js", doc_path), "user_js1")
    _make_js_link(head, relpath("_js/user_js2.js", doc_path), "user_js2")

    body = html.ekid("body")
    return html, body


def _make_css_link(head, href, id_=None):
    link = head.ekid("link", {"rel": "stylesheet", "type": "text/css", "href": href})
    if id_:
        link.attrs["id"] = id_
    return link


def _make_js_link(head, src, id_=None):
    script = head.ekid("script", {"type": "text/javascript", "src": src})
    if id_:
        script.attrs["id"] = id_
    return script


def relpath(path1, path2):
    """
     ("note/note0.xhtml", "sn/sn01.xhtml") -> "../note/note0.xhtml"
     ("sn/sn21.xhtml#SN.21.1, "sn/sn21.xhtml") -> "#SN.21.1"
    """

    path1_2 = posixpath.normpath(urlsplit(path1).path)
    fragment = urlsplit(path1).fragment

    path2_2 = posixpath.normpath(path2)

    if path1_2 == path2_2:
        if not fragment:
            raise ValueError("How to link to itself without a tag id?")
        else:
            return "#" + fragment
    else:
        return posixpath.relpath(path1_2, posixpath.dirname(path2_2)) + (("#" + fragment) if fragment else "")


def write_cover(epub, module, data, lang):
    pass

def write_homage(epub, module, data, lang):
    pass

def write_notes(epub, module, data, lang):
    pass


def get_uuid(s):
    return uuid.uuid5(uuid.NAMESPACE_URL, "https://github.com/meng89/nikaya" + " " + s)

