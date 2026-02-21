import os
import re
import uuid
import math
import posixpath
import string
import sys
from urllib.parse import urlsplit

import cn2an

import epubpacker
import xl

import config
from nikaya_share import base
from . import ebook_utils
from nikaya_share import utils
import hyncdzj.note
from nikaya_share import new_page_or_not, epub_utils
from hyncdzj.book_modules import all_infos


import sys
sys.setrecursionlimit(1000000)


def write_tree_to_userfiles(pre_path, tree, userfiles):
    for name, obj in tree:
        my_path = posixpath.join(pre_path, name)
        if isinstance(obj, xl.Xml):
            pass


def make_tree_data(data_infos):
    tree_data = []
    data2 = []
    for info, data in data_infos:
        for dirs, infos2 in all_infos:
            for info2 in infos2:
                if info2 == info:
                    make_tree_data2(info.name, data, dirs, tree_data)
                    data2.append((len(dirs), info, data))

    return tree_data, data2

def make_tree_data2(name, obj, dirs, data):
    for dir_ in dirs:
        data = make_sub_data(data, dir_)
    data.append(((None, None, name), obj))
    return data

def make_sub_data(data, name):
    for (_, _, name2), sub in data:
        if name == name2:
            return sub
    sub_data = []
    data.append(((None, None, name), sub_data))
    return sub_data


def build_epub_collection(title, cover_dir, full_path, data_infos, lang, tag):
    all_book_data, data2 = make_tree_data(data_infos)
    book_names = [lang.c(title)]
    for info, data in data_infos:
        data.append((lang.c(info.name), data))

    my_uuid = get_uuid("".join(book_names) + lang.en)
    epub = make_epub(title, title, my_uuid.urn)

    notes = hyncdzj.note.Notes()
    doc_files = {}
    translators = []
    for len_dirs, info, data in data2:
        book_data = [((None, None, lang.c(info.name)), data)]
        print(lang.c(info.name))
        write_tree5(info, all_book_data, -len_dirs, book_data, doc_files, epub.mark.kids, notes, lang, [], 1, 1, None, None, None)
        translators.extend(info.translators)

    book_info = base.Info(name="漢譯南傳大藏經", pali="Tipiṭaka", translators=tuple(translators))
    image_path = ebook_utils.make_cover_image(cover_dir, book_info, lang, tag, collection=True)
    _write_cover(epub, image_path, lang)

    notes = hyncdzj.note.Notes()
    _write_readme(epub, notes, lang)

    write_doc_files(doc_files, epub)
    write_note_spile(notes, epub, lang)

    make_marks_href(epub.mark.kids)

    epub.write(full_path)

    write_css(epub, lang)



def make_epub(title, collection, identifier):
    epub = epubpacker.Epub()
    epub.meta.titles = [title]
    epub.meta.identifier = identifier
    epub.meta.others.append(xl.Element("meta", {"property": "belongs-to-collection", "id": "c01"},
                                       [collection]))
    epub.meta.others.append(xl.Element("meta", {"refines": "#c01", "property": "collection-type"}, ["series"]))
    return epub

def write_doc_files(doc_files, epub):
    for path, xml in doc_files.items():
        xml: xl.Xml
        epub.userfiles[path] = xml.to_str(do_pretty=True,
                                          dont_do_tags=["title", "h1", "h2", "h3", "h4", "h5", "h6", "h7", "a", "span",
                                                        "p"])
        epub.spine.append(path)

def write_note_spile(notes, epub, lang):
    for title, path, page in notes.get_pages(lang):
        epub.userfiles[path] = page
        epub.spine.append(path)


def build_epub(cover_dir, full_path, data, info, lang, tag):
    epub = epubpacker.Epub()
    title = lang.c(info.name)
    epub.meta.titles = [title]

    # epub.meta.creators = ["莊春江({})".format(lang.c("譯"))] #todo
    #ts = ebook_utils.read_timestamp(data)
    #epub.meta.date = datetime.fromtimestamp(ts).astimezone().strftime("%Y-%m-%dT%H:%M:%SZ")
    epub.meta.languages = [lang.xml, "pi", "en-US"]

    my_uuid = get_uuid(title + lang.en)
    epub.meta.identifier = my_uuid.urn

    epub.meta.others.append(xl.Element("meta", {"property": "belongs-to-collection", "id": "c01"},
                                       [lang.c("漢譯南傳大藏經")]))
    epub.meta.others.append(xl.Element("meta", {"refines": "#c01", "property": "collection-type"}, ["series"]))

    write_css(epub, lang)

    notes = hyncdzj.note.Notes()
    docs = []
    #bns = [module.short]

    image_path = ebook_utils.make_cover_image(cover_dir, info, lang, tag)
    _write_cover(epub, image_path, lang)
    #_write_homage(module, epub.mark.kids, docs, ln, gn, lang) #todo

    doc_files = {}
    book_data = [((None, None, lang.c(info.name)), data)]
    write_tree5(info, data, 0, data, doc_files, epub.mark.kids, notes, lang, [], 1, 1, None, None, None, 0)

    for path, xml in doc_files.items():
        xml: xl.Xml
        epub.userfiles[path] = xml.to_str(do_pretty=True,
                                          dont_do_tags=["title", "h1", "h2", "h3", "h4", "h5", "h6", "h7", "a", "span", "p"])
        epub.spine.append(path)

    for title, path, page in notes.get_pages(lang):
        epub.userfiles[path] = page
        epub.spine.append(path)

    _write_readme(epub, notes, lang)
    #_write_readme(epub, lang)

    make_marks_href(epub.mark.kids)

    epub.write(full_path)


def make_marks_href(marks):
    for mark in marks:
        make_mark_href(mark)


def make_mark_href(mark):
    for sub_mark in mark.kids:
        sub_href = make_mark_href(sub_mark)
        if mark.href is None:
            mark.href = sub_href
    return mark.href


# refs = [("PS/Ps1.html", "id", "PS/PS.1.xhtml", "id2")]


def _find_path(id_, docs):
    for path, e in docs:
        if _get_id(id_, e):
            return True, path
    return False, None

def _get_id(id_, e: xl.Element):
    for kid in e.kids:
        if isinstance(kid, xl.Element):
            if kid.attrs.get("id") == id_:
                return True
            if _get_id(id_, kid):
                return True

    return False


# 有偈篇
#     1.諸天相應
#         蘆葦品
#             1.暴流之渡過經
#             2.解脫經
#     2.天子相應

def or_kong(x):
    return x or "【空】"


class IdGenerate:
    def __init__(self):
        self._serial = 1
    def get_one(self):
        _id = "id{}".format(self._serial)
        self._serial += 1
        return _id

def get_last_doc(docs):
    for namegroup, (new_html, new_body) in docs:
        pass


"""
经的上级标题需要写入第一个经里。


"""

def write_tree5(info, book_data, level_offset, obj, doc_files, marks, notes, lang, marks_and_headings, depth, id_count, doc_path, html, body, doc_depth=None):
    sub_marks = marks
    namegroups = new_page_or_not.get_keys(book_data, obj, [])
    if namegroups:
        mark, heading = make_mh(info, namegroups, obj, marks, depth, id_count, level_offset)
        marks_and_headings.append((mark, heading))
        sub_marks = mark.kids
    print("heihei:", namegroups)
    # 在第一个需要合并的经之前的节点创建 doc
    if doc_path is None:
        _, sub = obj[0]
        sub_new_page = new_page_or_not.new_page_or_not_smart(book_data, sub)
        # 下级如果没有分页，此级就要合并
        if sub_new_page is False:
            doc_path, html, body = write_docs(doc_files, namegroups, depth, lang, info)
            doc_depth = depth

    for sub_id_count, (namegroup, sub) in enumerate(obj, 1):


        if isinstance(sub, xl.Element):
            doc_path, html, body = write_doc5(info, book_data, level_offset, sub, doc_files, sub_marks, notes, lang,
                                              marks_and_headings, depth + 1, sub_id_count, doc_path, html, body, doc_depth)
        else:
            doc_path, html, body = write_tree5(info, book_data, level_offset, sub, doc_files, sub_marks, notes, lang,
                                               marks_and_headings, depth + 1, sub_id_count, doc_path, html, body, doc_depth)

    new_page = new_page_or_not.new_page_or_not_smart(book_data, obj)
    if new_page:
        doc_path, html, body = None, None, None
    return doc_path, html, body


def write_doc5(info, book_data, level_offset, obj, doc_files, marks, notes, lang, marks_and_headings, depth, id_count, doc_path, html, body, doc_depth):
    namegroups = new_page_or_not.get_keys(book_data, obj, [])

    if doc_path is None:
        doc_path, html, body = write_docs(doc_files, namegroups, depth, lang, info)
        doc_depth = depth

    # 把上级的 heading 写入文档先
    write_marks_and_headings(marks_and_headings, body, doc_path)

    if namegroups:
        mark, heading = make_mh(info, namegroups, obj, marks, depth, id_count, level_offset)
        mark.href = "{}#{}".format(doc_path, heading.attrs["id"])
        body.kids.append(heading)

    for e in obj.kids:
        if isinstance(e, xl.Element) and re.match(r"^n\d+$", e.tag):
            break

        else:
            html_es = xml_es_to_html([e], obj, notes, doc_depth, lang)
            body.kids.extend(html_es)

    new_page = new_page_or_not.new_page_or_not_smart(book_data, obj)
    if new_page:
        doc_path, html, body = None, None, None
    return doc_path, html, body


def make_mh(info, namegroups, obj, marks, depth, id_count, level_offset):
    mark, heading, _, _, _, _, = make_mark_and_heading(info, namegroups, obj, depth, level_offset)
    heading.attrs["id"] = "id_{}_{}".format(depth, id_count)
    marks.append(mark)
    return mark, heading

def write_docs(doc_files, namegroups, depth, lang, info):
    test_path = [base.namegroup_to_filename(_ng) for _ng in namegroups]
    if not test_path:
        test_path = [lang.c(info.name)]
    doc_path = epub_utils.make_safe_path(doc_files.keys(), posixpath.join(*test_path) + ".xhtml")
    html, body = make_doc(depth, lang)
    doc_files[doc_path] = html
    return doc_path, html, body

def write_marks_and_headings(marks_and_headings, body, doc_path):
    for index, (m, h) in enumerate(marks_and_headings):
        body.kids.insert(index, h)
        m.href = "{}#{}".format(doc_path, h.attrs["id"])
    marks_and_headings.clear()


def make_mark_and_heading(info, namegroups, obj, heading_level, level_offset):
    start, end, name = namegroups[-1]
    if start is None:
        range_start, range_end = read_range(obj)
        if range_start is None:
            mark_range = ""
        else:
            mark_range = "({}～{})".format(range_start, range_end)
    else:
        mark_range = ""

    epub_heading = xl.Element("h{}".format(heading_level)) #max(heading_level + level_offset, 1)))
    serials = []
    serial_names = []
    last_start = None
    names = []
    for (start, end, name) in namegroups:
        if start is not None:
            serials.append((start, end))
            serial_names.append(name)
        names.append(name)
        last_start = start

    if last_start is not None:
        ranges = []
        for _start, _end in serials:
            if _start == _end:
                ranges.append(str(_start))
            else:
                ranges.append(str(_start) + "～" + str(_end))

        _range_str = ".".join(ranges)
        name_str = "/".join([or_kong(sn) for sn in serial_names])

        range_str = info.abbr + _range_str
        a = xl.Element("a", {"href": "https://suttacentral.net/" + range_str}, [range_str])
        epub_heading.kids.append(a)
        epub_heading.kids.append("　")
        epub_heading.kids.append(name_str)
        is_serial = True
        mark_name = ranges[-1] + "." + or_kong(serial_names[-1]) + mark_range
        epub_mark = epubpacker.Mark(mark_name)
    else:
        range_str = None
        name_str = or_kong(names[-1])
        epub_heading.kids.append(name_str)
        mark_name = or_kong(names[-1]) + mark_range
        epub_mark = epubpacker.Mark(mark_name)
        is_serial = False

    return epub_mark, epub_heading, is_serial, mark_name, range_str, name_str


def read_range(obj):
    return read_start(obj), read_end(obj)


def read_start(obj):
    if isinstance(obj, xl.Element):
        for e in obj.kids:
            if isinstance(e, xl.Element) and e.tag.startswith("sub"):
                start, _end, _name = sub_to_namegroup(e)
                if start is not None:
                    return start
        return None
    # is isinstance(obj, list)
    for sub_namegroup, sub_obj in obj:
        start, _end, _name = sub_namegroup
        if start is not None:
            return start
        else:
            start = read_start(sub_obj)
            if start is not None:
                return start
    return None

def read_end(obj: list):
    if isinstance(obj, xl.Element):
        for e in obj.kids[::-1]:
            if isinstance(e, xl.Element) and e.tag.startswith("sub"):
                _start, end, _name = sub_to_namegroup(e)
                if end is not None:
                    return end
        return None

    for sub_namegroup, sub_obj in obj[::-1]:
        _start, end, _name = sub_namegroup
        if end is not None:
            return end
        else:
            end = read_end(sub_obj)
            if end is not None:
                return end

    return None


# <sub>1</sub>
# <sub>1.xxx</sub>
# <sub><t3>1</t3></sub>
# <sub><t3>1.xxx</t3></sub>
# <sub>xxx</sub>


def sub_to_namegroup(e):
    s = read_text_from_sub(e)
    s = "1_" + s  #在头部添加适配 filename_to_namegroup 的虚字符
    return base.filename_to_namegroup(s)

def read_serial_from_sub(e):
    s = read_text_from_sub(e)
    m = re.match(r"^(\d+)$", s)
    if m:
        return m.group(1), None
    m = re.match(r"^(\d+)\.(.+)$", s)
    if m:
        return m.group(1), None
    m = re.match(r"^(.+)$", s)
    if m:
        return None, m.group(1)
    return None

def read_text_from_sub(e):
    s = read_text_from_sub2(e)
    try:
        s2 = str(cn2an.cn2an(s, "normal"))
    except ValueError:
        s2 = s
    return s2

def read_text_from_sub2(e):
    s = ""
    for x in e.kids:
        if isinstance(x, str):
            s += x
        else:
            s += read_text_from_sub2(x)
    return s

def read_name_es_from_sub(e):
    y = False
    name_es = []
    for x in e.kids:
        if not y and isinstance(x, str) and x in "1234567890.":
            pass
        else:
            y = True
            name_es.append(x)
    return name_es


ES = list[xl.Element | str]

def xml_es_to_html(es: ES, root, notes: hyncdzj.note.Notes, doc_depth, lang) -> ES:
    new_es = []
    for e in es:
        if isinstance(e, xl.Element):
            m_t = re.match(r"^t(\d+)$", e.tag)
            m_n = re.match(r"^n\d+$", e.tag)
            if m_t:
                a = xl.Element("a", attrs={"epub:type": "noteref"})
                key = m_t.group(1)
                n_kids = get_note_by_key(root, key)
                link = notes.add_note(n_kids)
                href = relpath(link, "x/" * (doc_depth -2) + "xyz")
                a.attrs["href"] = href

                if len(e.kids) > 0:
                    a.attrs["class"] = "noteref"
                    a.kids.extend(xml_es_to_html(e.kids, root, notes, doc_depth, lang))
                else:
                    a.attrs["class"] = "no_text_noteref"
                    a.kids.append("注")

                new_es.append(a)

            elif e.tag == "p":
                p = xl.Element("p")
                p.kids.extend(xml_es_to_html(e.kids, root, notes, doc_depth, lang))
                new_es.append(p)

            elif e.tag == "j":
                poem_wrapper = xl.Element("div", attrs={"class": "poem_wrapper"})
                poem_author = xl.Element("div", attrs={"class": "poem_author"})
                poem = xl.Element("div", attrs={"class": "poem"})
                poem_wrapper.kids.extend([poem_author, poem])
                if "a" in e.attrs.keys():
                    p = poem_author.ekid("p")
                    p.kids.extend(xml_es_to_html([e.attrs["a"]], root, notes, doc_depth, lang))

                add_space = False
                if isinstance(e.kids[0].kids[0], str) and e.kids[0].kids[0][0] == "「":
                    add_space = True
                for p in e.kids:
                    p2 = poem.ekid("p")
                    _new_es = xml_es_to_html(p.kids, root, notes, doc_depth, lang)
                    if isinstance(p.kids[0], str) and p.kids[0][0] == "「":
                        p2_kids = _new_es
                    else:
                        if add_space:
                            p2_kids = [" 　"] + _new_es
                        else:
                            p2_kids = _new_es
                    p2.kids.extend(p2_kids)
                new_es.append(poem_wrapper)

            elif m_n:
                pass

            elif e.tag == "a":
                new_es.append(e)
            elif e.tag == "list":
                new_es.append(e)
            elif e.tag == "table":
                new_es.append(e)
            else:
                raise Exception("Unknown element type: {}".format(repr(e.to_str())))

        elif isinstance(e, str):
            new_es.append(e)
            #new_es.extend(tag_str.str_to_es(e))
    return new_es


def join_html_zwnj(es):
    new_es = []
    for e in es:
        if isinstance(e, str):
            for char in e:
                new_es.append(char)
                new_es.append(xl.HtmlZWNJ())
        elif isinstance(e, xl.Element):
            e.kids[:] = join_html_zwnj(e.kids)
            new_es.append(e)
    return new_es


def get_note_by_key(root: xl.Element, key: str):
    for e in root.kids:
        m_n = re.match(r"^n(\d+)$", e.tag)
        if m_n:
            if key == m_n.group(1):
                return e.kids

    raise Exception("Note not found")




def write_css(epub, lang):
    css_t = open(os.path.join(config.RESOURCE_DIR, "style.css"), "r").read()

    if isinstance(lang, ebook_utils.SC):
        heading_font_name = """ "Microsoft YaHei", "PingFang SC", "思源黑体 CN" """
        body_font_name = """ "Source Han Serif SC", "SimSun", "Songti SC" """

    else:
        heading_font_name = """ "Microsoft JhengHei", "PingFang TC", "思源黑體 TW" """
        body_font_name = """ "Source Han Serif TC", "PMingLiU", "Songti TC" """

    css_str = string.Template(css_t).substitute(
        heading_font_name = heading_font_name,
        body_font_name = body_font_name,
    )
    epub.userfiles["style.css"] = css_str


def make_doc(depth, lang, title=None):
    html = xl.Element("html", {"xmlns:epub": "http://www.idpf.org/2007/ops",
                               "xmlns": "http://www.w3.org/1999/xhtml",
                               "xml:lang": lang.xml,
                               "lang": lang.xml})
    head = html.ekid("head")

    if title:
        _title = head.ekid("title", kids=[title])

    href = "../" * (depth - 2) + "style.css"
    link = head.ekid("link", {"rel": "stylesheet", "type": "text/css", "href": href})
    link.attrs["id"] = "css1"

    body = html.ekid("body")
    return html, body


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


def _write_cover(epub, cover_image_path, lang):
    base_name = os.path.basename(cover_image_path)
    epub.userfiles[base_name] = open(cover_image_path, "rb").read()
    cover_doc_path = "cover.xhtml"
    html, body = make_doc(2, lang, "封面")
    #body.attrs["style"] = "text-align: center;"
    body.attrs["class"] = "cover"

    _img = body.ekid("img", {"src": relpath(base_name, cover_doc_path),
                             "alt": "Cover Image",
                             "title": "Cover Image"})
    htmlstr = xl.Xml(root=html).to_str()
    epub.userfiles[cover_doc_path] = htmlstr
    epub.mark.kids.append(epubpacker.Mark("封面", cover_doc_path))
    epub.spine.append(cover_doc_path)


def _write_homage(_module, marks, docs, notes, lang):
    doc_path = "homage.xhtml"
    html, body = make_doc(doc_path, lang, lang.c("禮敬偈"))
    body.attrs["class"] = "homage"

    #outdiv = body.ekid("div", {"class": "homage_out"})
    #indiv = outdiv.ekid("div", {"class": "homage_in"})

    kids = []
    p = body.ekid("p")
    p.kids.extend(xml_es_to_html(kids, html, notes, doc_path, lang))
    #indiv.kids.append())

    docs.append((doc_path, html))
    marks.append(epubpacker.Mark(lang.c("禮敬偈"), doc_path))


_project_link = "https://github.com/meng89/hyncdzj/books"
_yunpan_link = "https://www.jianguoyun.com/p/DbBOkGwQnbmtChjWkpIGIAA"
_my_mail = "observerchan@gmail.com"

ZZSM = (
    ["此佛经译著权归属于元亨寺及其译者。", xl.Element("a", {"href": "https://www.cbeta.org/"}, ["CBETA"],)," 做了数字化工作。"],
    # ["在本人读经的过程中，会按照上下文填充省略的部分，以及对不懂的词句进行了解并加上注释。若您愿意帮助填充和注释，请联系我。"],
    ["下载请访问", xl.Element("a", {"href": "{}".format(_project_link)}, ["项目主页"]),
     "或", xl.Element("a", {"href": "{}".format(_yunpan_link)}, ["云盘"]),],
    ["如有任何与此电子书制作程序相关的问题，或者电子书获取困难，请联系我：", xl.Element("a", {"href": "mailto:{}".format(_my_mail)}, [_my_mail])]
)


def _write_readme(epub, notes, lang):
    doc_path = "readme.xhtml"
    html, body = make_doc(1, lang, lang.c("製作說明"))

    body.attrs["class"] = "readme"

    _h1 = body.ekid("h1", {"class": "title"}, [lang.c("製作說明")])
    for line in ZZSM:
        _p = body.ekid("p", kids=xml_es_to_html(line, html, notes, doc_path, lang))

    htmlstr = xl.Xml(root=html).to_str(do_pretty=True, dont_do_tags=["p"])
    epub.userfiles[doc_path] = htmlstr
    epub.spine.append(doc_path)
    epub.mark.kids.append(epubpacker.Mark(lang.c("製作說明"), doc_path))


def get_uuid(s):
    return uuid.uuid5(uuid.NAMESPACE_URL, "https://github.com/meng89/nikaya" + " " + s)
