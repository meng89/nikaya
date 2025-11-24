import copy
import os
import re
import uuid
from datetime import datetime
import math
import posixpath
from urllib.parse import urlsplit
import urllib.parse

import epubpacker
import xl

from . import base
import hyncdzj.utils
import hyncdzj.note
from . import css
#from . import ebook_utils
#from . import suttanum_ref
from public_modules import tag_str



def build_epub(full_path, data, modules: list, lang, exit_after_done=False):
    epub = epubpacker.Epub()
    titles = []
    for module in modules:
        titles.append(lang.c(module.info.name))
    epub.meta.titles = titles

    # epub.meta.creators = ["莊春江({})".format(lang.c("譯"))] #todo
    #ts = ebook_utils.read_timestamp(data)
    #epub.meta.date = datetime.fromtimestamp(ts).astimezone().strftime("%Y-%m-%dT%H:%M:%SZ")
    epub.meta.languages = [lang.xml, "pi", "en-US"]

    my_uuid = get_uuid("".join(titles) + lang.en)
    epub.meta.identifier = my_uuid.urn

    epub.meta.others.append(xl.Element("meta", {"property": "belongs-to-collection", "id": "c01"},
                                       [lang.c("漢譯南傳大藏經")]))
    epub.meta.others.append(xl.Element("meta", {"refines": "#c01", "property": "collection-type"}, ["series"]))

    epub.userfiles[css.css1_path] = css.css1[lang.en]

    notes = hyncdzj.note.Notes()
    docs = []
    #bns = [module.short]

    #_write_cover(epub, ebook_utils.make_cover(module, data, lang), lang) #todo
    #_write_homage(module, epub.mark.kids, docs, ln, gn, lang) #todo


    for index, module in enumerate(modules, start=1):
        _make_suttas(module, epub.mark.kids, docs, [(index, None, None, module.info.name)], data, notes, lang)


    for path, xml in docs:
        xml: xl.Xml
        epub.userfiles[path] = xml.to_str(do_pretty=True,
                                          dont_do_tags=["title", "h1", "h2", "h3", "h4", "a", "span", "p"])
        epub.spine.append(path)

    for title, path, page in notes.get_pages(lang):
        epub.userfiles[path] = page
        epub.spine.append(path)

    _write_readme(epub, notes, lang)
    #_write_readme(epub, lang)

    epub.write(full_path)

    if exit_after_done:
        exit()

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


def _make_suttas(module, marks: list[epubpacker.Mark], docs, parent_branch: list, data, notes, lang):
    short = module.info.abbr

    first_doc_path = None
    #if data_name is not None:
    #    my_branch = parent_branch + [data_name]
    #else:
    #    my_branch = parent_branch[:]

    for namegroup, obj in data:
        file_index, start, end, name = namegroup
        my_branch = parent_branch + [namegroup]

        if isinstance(obj, list):
            if start is not None:
                if start == end:
                    name2 = str(start) + "." + (name or "none1")
                else:
                    name2 = str(start) + "-" + str(end) + "." + (name or "none1")

            elif start is None and isinstance(obj, list):
                # 有偈篇 和 芦苇品 这样的文件夹可以在后面添加经号范围。当然有偈篇包含的是其下的相应的范围，芦苇品包含的是其下面的经文范围
                obj_range_start, obj_range_end = read_range(obj)

                name2 = "{}({}～{})".format(name, obj_range_start, obj_range_end)

            else:
                name2 = name

            mark = epubpacker.Mark(lang.c(name2))
            marks.append(mark)

            if is_leaf(namegroup, obj) and is_join_needed(obj): # 这是最后一个目录 且 短经很多
                #_branch = my_branch + [name]
                doc_path = branch_to_doc_path(my_branch)
                html, body = make_doc(doc_path, lang, name)

                for count, (sub_namegroup, sub_obj) in enumerate(obj, start=1):
                    sutta_id = "sutta{}".format(count)
                    _, _, sutta_mark = write_sutta(short, my_branch + [sub_namegroup], sutta_id, sub_obj, notes, lang, html, body, doc_path)
                    mark.kids.append(sutta_mark)

                docs.append((doc_path, html))

            else:
                doc_path = _make_suttas(module, mark.kids, docs, my_branch, obj, notes, lang)
            mark.href = doc_path

        else:
            doc_path, html, mark = write_sutta(short, my_branch, "sutta1", obj, notes, lang)
            docs.append((doc_path, html))
            marks.append(mark)

        if first_doc_path is None:
            first_doc_path = doc_path

    return first_doc_path


def write_sutta(short, my_branch, sutta_id, obj: xl.Xml, notes, lang, html=None, body=None, doc_path=None):

    file_index, start, end, sutta_name = my_branch[-1]

    if doc_path is None:
        doc_path = branch_to_doc_path(my_branch)
        html, body = make_doc(doc_path, lang, sutta_name)

    level = max(len(my_branch), 3)

    title_h = body.ekid("h" + str(level))
    title_h.attrs["class"] = "sutta_title"
    title_h.attrs["id"] = sutta_id

    num_span = title_h.ekid("span", {"class": "sutta_num_sc"})
    num_tuples, names = branch_to_nums_and_names(my_branch)
    nums = []
    for _start, _end in num_tuples:
        if _start == _end:
            nums.append(str(_start))
        else:
            nums.append(str(_start) + "～" + str(_end))

    nums_str = ".".join([str(num) for num in nums])

    if nums_str:
        sc_a = xl.Element("a", {"href": "https://suttacentral.net/" + short + nums_str}, [short + nums_str])
        sc_a.attrs["class"] = "sutta_num_sc"
        num_span.kids.append(sc_a)

    if nums_str:
        title_h.kids.append("　")

    name_span = title_h.ekid("span", {"class": "sutta_name"})
    if names:
        h_names = "/".join([n if n else "" for n in names])
    else:
        h_names = sutta_name or "none"
    name_span.kids.append(lang.c(h_names))

    es = xml_es_to_html(obj.root.kids, obj.root, notes, doc_path, lang)
    body.kids.extend(es)

    if start == end:
        _range = str(start)
    else:
        _range = str(start) + "～" + str(end)

    mark = epubpacker.Mark("{}.{}".format(_range, lang.c(sutta_name)), href="{}#{}".format(doc_path, sutta_id))
    return doc_path, html, mark


ES = list[xl.Element | str]

def xml_es_to_html(es: ES, root, notes: hyncdzj.note.Notes, doc_path, lang) -> ES:

    new_es = []
    for e in es:
        if isinstance(e, xl.Element):
            m_t = re.match(r"^t(\d+)$", e.tag)
            m_n = re.match(r"^n\d+$", e.tag)
            if m_t:
                a = xl.Element("a", attrs={"epub:type": "noteref"})
                key = m_t.group(1)
                n_kids = _get_note_by_key(root, key)
                link = notes.add_note(n_kids)
                href = relpath(link, doc_path)
                a.attrs["href"] = href

                if len(e.kids) > 0:
                    a.attrs["class"] = "noteref"
                    a.kids.extend(xml_es_to_html(e.kids, root, notes, doc_path, lang))
                else:
                    a.attrs["class"] = "no_text_noteref"
                    a.kids.append("注")

                new_es.append(a)

            elif e.tag == "p":
                new_es.extend(xml_es_to_html(e.kids, root, notes, doc_path, lang))

            elif e.tag == "j":

                div = xl.Element("div", attrs={"class": "jizi"})
                person = ""
                len_person = 0
                if "p" in e.attrs.keys():
                    person = e.attrs["p"] + "：　"
                    len_person = len(person)

                for index, p_e in enumerate(e.kids):
                    _es = []
                    def _add(_es2):
                        if len(_es) > 0 and isinstance(_es[-1], str) and len(_es2) > 0 and isinstance(_es2[0], str):
                            _es_tail = _es[-1]
                            _es.pop(-1)
                            _es2_head = _es2[0]
                            _es2.pop(0)
                            _es.append(_es_tail + _es2_head)
                            _es.extend(_es2)
                        else:
                            _es.extend(_es2)

                    if index == 0:
                        _es.append(person)
                        if isinstance(p_e.kids[0], str) and p_e.kids[0][0] == "「":
                            len_person += 1
                    else:
                        _add(["　" * len_person])
                    _add(p_e.kids)
                    p = xl.Element("p")
                    _es3 = xml_es_to_html(_es, root, notes, doc_path, lang)
                    p.kids.extend(_es3)
                    _es = []
                    div.kids.append(p)
                new_es.append(div)

            elif m_n:
                pass

            elif e.tag == "a":
                new_es.append(e)

            else:
                raise Exception("Unknown element type: {}".format(repr(e.to_str())))

        elif isinstance(e, str):
            new_es.extend(tag_str.str_to_es(lang.c(e)))

    return new_es


def _get_note_by_key(root: xl.Element, key: str):
    for e in root.kids:
        m_n = re.match(r"^n(\d+)$", e.tag)
        if m_n:
            if key == m_n.group(1):
                return e.kids

    raise Exception("Note not found")


def branch_to_doc_path(branch: list):
    filenames = []
    for namegroup in branch:
        filename = base.fullnamegroup_to_filename(namegroup)
        filenames.append(filename)
    return posixpath.join("", *filenames) + ".xhtml"


def branch_to_nums_and_names(branch: list):
    nums = []
    names = []
    for namegroup in branch:
        file_index, start, end, name = namegroup
        if start is not None:
            nums.append((start, end))
            names.append(name)

    return nums, names


def read_range(obj):
    return read_start(obj), read_end(obj)


def read_start(obj):
    start = None
    for sub_namegroup, sub_obj in obj:
        _file_index, sub_start, _sub_end, _sub_name = sub_namegroup
        if sub_start is not None:
            start = sub_start
        else:
            if isinstance(sub_obj, list):
                start = read_start(sub_obj)

        if start is not None:
            return start

    return None


def read_end(obj: list):
    for sub_namegroup, sub_obj in obj[::-1]:
        _file_index, _sub_start, sub_end, _sub_name = sub_namegroup
        if sub_end is not None:
            return sub_end
        else:
            if isinstance(sub_obj, list):
                end = read_end(sub_obj)
                if end is not None:
                    return end

    return None


def is_join_needed(obj):
    small_page, large_page = count_page(obj)
    try:
        if small_page / large_page > 1:
            return True
        else:
            return False
    except ZeroDivisionError:
        return True


def count_page(obj):
    # 检查是否需要把这里面的所有页面都合并在一起
    # 因为有些经文字太少，一些（哪些?）阅读器没有拼页功能，导致频繁翻页，上下相关的经文不在一个页面上。
    small_page = 0
    large_page = 0

    for name, obj in obj:
        if isinstance(obj, list):
            small_page2, large_page2 = count_page(obj)
            small_page += small_page2
            large_page += large_page2
            continue

        xml = obj
        line_count = 0
        for p in xml.root.find_kids("p"):
            txt = hyncdzj.utils.line_to_txt(p.kids)
            line_count += math.ceil(len(txt)/40)

        if line_count <= 30:
            small_page += 1
        else:
            large_page += 1

    return small_page, large_page


def is_leaf(namegroup, obj):
    if namegroup[1] is not None:
        return False
    if not isinstance(obj, list):
        return False

    file_count = 0
    dir_count = 0

    for (file_index, sub_start, sub_end, sub_name), sub_obj in obj:
        if isinstance(sub_obj, list):
            dir_count += 1
        elif isinstance(sub_obj, xl.Xml) and sub_name is not None:
            file_count += 1

    if dir_count == 0:
        return True
    else:
        return False


def make_doc(doc_path, lang, title=None):
    html = xl.Element("html", {"xmlns:epub": "https://www.idpf.org/2007/ops",
                               "xmlns": "https://www.w3.org/1999/xhtml",
                               "xml:lang": lang.xml,
                               "lang": lang.xml})
    head = html.ekid("head")

    if title:
        _title = head.ekid("title", kids=[title])

    _make_css_link(head, relpath(css.css1_path, doc_path), "css1")
    #_make_css_link(head, relpath("_css/user_css1.css", doc_path), "user_css1")
    #_make_css_link(head, relpath("_css/user_css2.css", doc_path), "user_css2")
    #_make_js_link(head, relpath(js.js1_path, doc_path), "js1")
    #_make_js_link(head, relpath("_js/user_js1.js", doc_path), "user_js1")
    #_make_js_link(head, relpath("_js/user_js2.js", doc_path), "user_js2")

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


def _write_cover(epub, cover_image_path, lang):
    base_name = os.path.basename(cover_image_path)
    epub.userfiles[base_name] = open(cover_image_path, "rb").read()
    cover_doc_path = "cover.xhtml"
    html, body = make_doc(cover_doc_path, lang, "封面")
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
    ["此佛经译著权归属于元亨寺，", "由", xl.Element("a", {"href": "https://www.cbeta.org/"}, ["CBETA"],),"数字化。"],
    ["在本人读经的过程中，会按照上下文填充省略的部分，以及对不懂的词句进行了解并加上注释。若您愿意帮助填充和注释，请联系我。"],
    ["下载请访问", xl.Element("a", {"href": "{}".format(_project_link)}, ["项目主页"]),
     "或", xl.Element("a", {"href": "{}".format(_yunpan_link)}, ["云盘"]),],
    ["有任何与此电子书制作程序的相关问题也请联系我：", xl.Element("a", {"href": "mailto:{}".format(_my_mail)}, [_my_mail])]
)


def _write_readme(epub, notes, lang):
    doc_path = "readme.xhtml"
    html, body = make_doc(doc_path, lang, lang.c("製作說明"))

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
