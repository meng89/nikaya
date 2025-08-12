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
import pyabo2.note
from . import css, js
from . import ebook_utils
from base import Folder, Entry



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


# 有偈篇
#     1.諸天相應
#         蘆葦品
#             1.暴流之渡過經
#             2.解脫經
#     2.天子相應


def write_suttas(module, marks, userfiles, branch: list, data, gn, lang):
    for name, obj in data:
        def _make_doc():
            doc_path = posixpath.join(*branch, name) + ".xhtml"
            return make_doc(doc_path, lang)

        if isinstance(obj, list):
            if is_leaf(obj) and need_join(obj):
                html, body = _make_doc()
                write_one_folder(marks, userfiles, module, branch, html, body, obj, gn, lang)
            else:
                new_branch = branch + [name]
                write_suttas(module, marks, userfiles, new_branch, obj, gn, lang)

        else:
            html, body = _make_doc()
            write_one_doc(marks, userfiles, module, branch, None, html, body, obj, gn, lang)


def write_one_doc(marks, userfiles, module, branch, doc_path, html, body, obj: xl.Xml, gn, lang):
    title = get_sutta_name(obj.root)

    if doc_path is None:
        doc_path = posixpath.join("",*(branch[0:-1]+[title])) + ".xhtml"

    h = body.ekid("h" + str(len(branch) + 1))

    sutta_num = get_sutta_num(obj.root)
    if sutta_num == 0:
        h.kids.append(sutta_num)

    serialized_nodes = get_serialized_nodes(branch)
    if serialized_nodes:
        head = "{}/{}".format(serialized_nodes[0], title)
    else:
        head = title

    h.kids.append(head)

    for xml_p in obj.root.find_descendants("p"):
        html_p = body.ekid("p")
        html_p.kids.extend(xml_to_html(xml_p.kids, gn, doc_path, lang))



def write_one_folder(marks, userfiles, module, branch, html, body, obj, gn, lang):
    doc_path = posixpath.join("", *branch) + ".xhtml"
    h = body.ekid("h{}".format(len(branch)))
    h.kids.append(branch[-1])
    for sub_name, sub_obj in obj:
        sub_branch = branch + [sub_name]
        write_one_doc(marks, userfiles, module, sub_branch, doc_path, html, body, sub_obj, gn, lang)


ES = list[xl.Element | str]

def xml_to_html(es: ES, gn: pyabo2.note.GlobalNotes, doc_path, lang) -> ES:
    new_es = []
    for e in es:
        if isinstance(e, xl.Element):
            if e.tag == "gn":
                a = xl.Element("a", attrs={"epub:type": "noteref"})
                link = gn.get_link(e.attrs["id"])
                href = relpath(link, doc_path)
                a.attrs["href"] = href
                a.kids.extend(xml_to_html(e.kids, gn, doc_path, lang))
                new_es.append(a)

        elif isinstance(e, str):
            new_es.append(lang.c(e))

    return new_es



def get_sutta_name(root: xl.Element):
    return root.find_descendants("title")[0].kids[0]


def get_sutta_num(root: xl.Element):
    for sutta_num in root.find_descendants("sutta_nums"):
        if sutta_num.attrs.get("type") is None:
            return sutta_num.kids[0]
    return None


def get_serialized_nodes(branch: list, nodes=None):
    nodes = nodes or []
    for node in branch:
        m = re.match(r"^\d+\.(.+)$", node)
        if m:
            nodes.append(m.group(1))
    return nodes



def get_path(data, obj, path=None):
    path = path or []
    for _, sub_obj in data:

        if obj is sub_obj:
            return path

        if isinstance(sub_obj, list):
            path.append(sub_obj)
            path2 = get_path(sub_obj, obj, path)
            if path2:
                return path2

    return None




def need_attach_range(name, obj):
    # 有偈篇 和 芦苇品 这样的文件夹可以在后面添加经号范围。当然有偈篇包含的是其下的相应的范围，芦苇品包含的是其下面的经文范围
    if isinstance(obj, list) and not re.match(r"^\d+\..+$", name):
        return True
    else:
        return False

def read_range(obj):
    return read_start(obj), read_end(obj)

def read_start(obj):
    sub_name, sub_obj = obj[0]
    if isinstance(sub_obj, list):
        m = re.match(r"^(\d+)\..+$", sub_name)
        if m:
            return m.group(1)
        else:
            return read_start(sub_obj)
    else:
        return obj.root.find_descendants("start")[0].kids[0]

def read_end(obj):
    sub_name, sub_obj = obj[-1]
    if isinstance(sub_obj, list):
        m = re.match(r"^(\d+)\..+$", sub_name)
        if m:
            return m.group(1)
        else:
            return read_end(sub_obj)
    else:
        return obj.root.find_descendants("end")[0].kids[0]


def is_serialized_folder(name, obj):
    if isinstance(obj, list) and re.match(r"^(\d+)\..+$", name):
        return True
    return False


def need_join(obj):
    # 检查是否需要把这里面的所有页面都合并在一起
    # 因为有些经文字太少，一些（哪些?）阅读器没有拼页功能，导致频繁翻页，上下相关的经文不在一个页面上。
    small_page = 0
    large_page = 0

    for name, xml in obj:
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

    if small_page / large_page > 1:
        return True
    else:
        return False



def is_leaf(obj):
    if not isinstance(obj, list):
        return False

    if isinstance(obj[0], xl.Xml):
        return True
    else:
        return False



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

