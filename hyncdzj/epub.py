import copy
import os
import re
import uuid
from datetime import datetime
import math
import posixpath
from tokenize import maybe
from urllib.parse import urlsplit
import urllib.parse

import epubpacker
import xl

from . import base
from . import ebook_utils
import hyncdzj.utils
import hyncdzj.note
from . import css
#from . import ebook_utils
#from . import suttanum_ref
from public_modules import tag_str



def build_epub(full_path, data, module, lang, tag, exit_after_done=False):
    epub = epubpacker.Epub()
    title = module.info.name
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

    epub.userfiles[css.css1_path] = css.css1[lang.en]

    notes = hyncdzj.note.Notes()
    docs = []
    #bns = [module.short]

    _write_cover(epub, ebook_utils.make_cover_image(module, lang, tag), lang)
    #_write_homage(module, epub.mark.kids, docs, ln, gn, lang) #todo


    # _make_suttas(module, epub.mark.kids, docs, [(1, None, None, module.info.name)], data, notes, lang)

    write_tree(module, data, epub.mark.kids, docs, [(1, None, None, module.info.name)], notes, lang)

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

    make_marks_href(epub.mark.kids)

    epub.write(full_path)

    if exit_after_done:
        exit()

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


def write_tree(module, data, marks, docs, parent_namegroups, notes, lang):
    for namegroup, obj in data:
        file_index, start, end, name = namegroup

        cur_namegroups = parent_namegroups + [namegroup]
        doc_path = branch_to_doc_path(cur_namegroups)
        html, body = make_doc(doc_path, lang, name)

        # 短经合并到一个页面
        if isinstance(obj, list) and is_leaf(namegroup, obj) and is_join_needed(obj):
            docs.append((doc_path, html))
            mark, heading, _ = make_mark_and_heading(module, cur_namegroups, 1)
            marks.append(mark)
            # body.kids.append(heading)
            write_leaf_to_page(module, obj, mark.kids, cur_namegroups, notes, lang, doc_path, html, body)

        elif isinstance(obj, xl.Xml):
            docs.append((doc_path, html))
            mark, heading, _ = make_mark_and_heading(module, cur_namegroups, 2)
            marks.append(mark)
            heading.attrs["id"] = "doc_1"
            mark.href = doc_path + "#doc_1"
            write_doc_to_page(module, obj, mark.kids, cur_namegroups, notes, lang, doc_path, html, body, "doc_1")

        else:
            assert isinstance(obj, list)
            mark, heading, _ = make_mark_and_heading(module, cur_namegroups, 1)
            marks.append(mark)
            write_tree(module, obj, mark.kids, docs, cur_namegroups, notes, lang)


def write_leaf_to_page(module, data, marks, parent_branch, notes, lang, doc_path, html, body):
    for count, (namegroup, obj) in enumerate(data, start=1):
        cur_namegroups = parent_branch + [namegroup]
        doc_id = "doc_" + str(count)
        mark, heading, _ = make_mark_and_heading(module, cur_namegroups, 2)
        marks.append(mark)
        heading.attrs["id"] = doc_id
        mark.href = doc_path + "#" + doc_id
        body.kids.append(heading)
        write_doc_to_page(module, obj, mark.kids, parent_branch, notes, lang, doc_path, html, body, doc_id)


def write_doc_to_page(module, obj, marks, cur_namegroups, notes, lang, doc_path, html, body, doc_id):
    sub_count = 0
    for e in obj.root.kids:
        if isinstance(e, xl.Element) and re.match(r"^n\d+$", e.tag):
            break

        elif isinstance(e, xl.Element) and e.tag == "sub":
            name_group = sub_to_namegroup(e)
            mark, heading, is_serial = make_mark_and_heading(module, cur_namegroups + [name_group], 3)
            heading.attrs["class"] = "sub"
            heading.attrs["id"] = "sub_" + str(sub_count)
            if is_serial:
                heading.attrs["class"] = heading.attrs["class"] + " serial_sub"
            mark.href = doc_path + "#" + heading.attrs["id"]
            marks.append(mark)
            body.kids.append(heading)
            sub_count += 1

        elif isinstance(e, xl.Element) and e.tag.startswith("sub"):
            name_group = sub_to_namegroup(e)
            mark, heading, is_serial = make_mark_and_heading(module, cur_namegroups + [name_group], 3)
            heading.attrs["class"] = "sub"
            heading.attrs["id"] = "sub_" + str(sub_count)
            mark.href = doc_path + "#" + heading.attrs["id"]
            marks.append(mark)
            body.kids.append(heading)
            sub_count += 1

        else:
            html_es = xml_es_to_html([e], obj.root, notes, doc_path, lang)
            body.kids.extend(html_es)


def make_mark_and_heading(module, namegroups, heading_level):
    heading = xl.Element("h{}".format(heading_level))
    serials = []
    serial_names = []
    last_start = None
    names = []
    for (file_index, start, end, name) in namegroups:
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


        range_str = ".".join(ranges)
        name_str = "/".join([or_kong(sn) for sn in serial_names])

        range_and_name = module.info.abbr + range_str
        a = xl.Element("a", {"href": "https://suttacentral.net/" + range_and_name}, [range_and_name])
        heading.kids.append(a)
        heading.kids.append("　")
        heading.kids.append(name_str)
        is_serial = True

        mark = epubpacker.Mark(ranges[-1] + "." + or_kong(serial_names[-1]))
    else:
        heading.kids.append(or_kong(names[-1]))
        mark = epubpacker.Mark(or_kong(names[-1]))
        is_serial = False

    return mark, heading, is_serial


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
    s = ""
    for x in e.kids:
        if isinstance(x, str):
            s += x
        else:
            s += read_text_from_sub(x)
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


def make_mark_name(namegroup, obj):
    fileindex, start, end, name = namegroup
    if start is not None:
        if start == end:
            range_ = str(start)
        else:
            range_ = str(start) + "～" + str(end)

        if name is not None:
            mark_name = range_ + "." + name
        else:
            mark_name = range_

    # 有偈篇 和 芦苇品 这样的文件夹可以在后面添加经号范围。当然有偈篇包含的是其下的相应的范围，芦苇品包含的是其下面的经文范围
    elif start is None and isinstance(obj, list):
        obj_range_start, obj_range_end = read_range(obj)
        if obj_range_start is None:
            mark_name = name
        else:
            mark_name = "{}({}～{})".format(name, obj_range_start, obj_range_end)
    else:
        mark_name = name
    return mark_name


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
                if obj_range_start is None:
                    name2 = name
                else:
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
        mark_range = start
    else:
        mark_range = "{}～{}".format(str(start), str(end))

    if mark_range is not None:
        mark_name = "{}.{}".format(mark_range, lang.c(sutta_name))
    else:
        mark_name = lang.c(sutta_name)

    mark = epubpacker.Mark(mark_name, href="{}#{}".format(doc_path, sutta_id))
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
                p = xl.Element("p")
                p.kids.extend(xml_es_to_html(e.kids, root, notes, doc_path, lang))
                new_es.append(p)

            elif e.tag == "j":

                div = xl.Element("div", attrs={"class": "jizi"})
                person = ""
                len_person = 0
                if "p" in e.attrs.keys():
                    person = e.attrs["p"] + "　"

                else:
                    person = "　" * 6

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
                    p.kids.extend(join_html_zwnj(_es3))
                    _es = []
                    div.kids.append(p)
                new_es.append(div)

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
            new_es.extend(tag_str.str_to_es(lang.c(e)))

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
    html = xl.Element("html", {"xmlns:epub": "http://www.idpf.org/2007/ops",
                               "xmlns": "http://www.w3.org/1999/xhtml",
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
