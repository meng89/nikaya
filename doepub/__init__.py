import uuid

import epubpacker
import xl

import posixpath
from urllib.parse import urlsplit, urlunsplit

from pyccc import page_parsing

from . import css


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
            raise ValueError("How to link to self without a tag id?")
        else:
            return "#" + fragment
    else:
        return posixpath.relpath(path1_2, posixpath.dirname(path2_2)) + (("#" + fragment) if fragment else "")


MAX_NUMBER_OF_NOTES_PER_PAGE = 50


def note_href_calculate(type_, key):
    return note_docname_calculate(type_, key) + "#" + noteid(type_, key)


def note_docname_calculate(type_, key):
    if type_ == page_parsing.GLOBAL:
        return "note/globalnote{}.xhtml".format(int(key[0]) // MAX_NUMBER_OF_NOTES_PER_PAGE)
    else:
        return "note/localnote{}.xhtml".format(key // MAX_NUMBER_OF_NOTES_PER_PAGE)


def noteid(type_, key):
    if type_ == page_parsing.GLOBAL:
        return str(key[0])
    else:
        return str(key)


def get_uuid(s):
    return uuid.uuid5(uuid.NAMESPACE_URL, "https://github.com/meng89/nikaya" + " " + s)


def attch_cssjs(epub):
    pass


def _make_css_link(head, href):
    xl.sub(head, "link", {"rel": "stylesheet", "type": "text/css", "href": href})


def _make_js_link(head, src):
    xl.sub(head, "script", {"type": "text/javascript", "src": src})


def make_doc(doc_path, xc, title=None):
    html = xl.Element("html", {"xmlns:epub": "http://www.idpf.org/2007/ops",
                               "xmlns": "http://www.w3.org/1999/xhtml",
                               "xml:lang": xc.xmlang,
                               "lang": xc.xmlang})
    head = xl.sub(html, "head")

    if title:
        _title = xl.sub(head, "title", kids=[title])

    _make_css_link(head, relpath(css.font_path[xc.enlang], doc_path))
    _make_css_link(head, relpath(css.public_path, doc_path))

    _make_css_link(head, relpath("_css/css1.css", doc_path))
    _make_css_link(head, relpath("_css/css2.css", doc_path))
    _make_js_link(head, relpath("_js/js1.js", doc_path))
    _make_js_link(head, relpath("_js/js2.js", doc_path))

    body = xl.sub(html, "body")
    return html, body


def write_epub_cssjs(epub: epubpacker.Epub):
    epub.userfiles[css.public_path] = css.public
    epub.userfiles["_css/css1.css"] = "/* 第一个自定义 CSS 文件 */\n\n"
    epub.userfiles["_css/css2.css"] = "/* 第二个自定义 CSS 文件 */\n\n"
    epub.userfiles["_js/js1.js"] = "// 第一个自定义 JS 文件\n\n"
    epub.userfiles["_js/js2.js"] = "// 第二个自定义 JS 文件\n\n"

