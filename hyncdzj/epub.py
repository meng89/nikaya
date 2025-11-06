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

import config
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
    if len(modules) == 1:
        module = modules[0]
        _make_suttas(module, epub.mark.kids, docs, [], module.info.abbr, data, notes, lang)
    elif len(modules) > 1:
        for module in modules:
            _make_suttas(module, epub.mark.kids, docs, [], module.info.abbr, data, notes, lang)


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


def _make_suttas(module, marks: list[epubpacker.Mark], docs, parent_branch: list, data_name, data, notes, lang):
    first_doc_path = None
    if data_name is not None:
        my_branch = parent_branch + [data_name]
    else:
        my_branch = parent_branch[:]

    for name, obj in data:
        if isinstance(obj, list):
            new_branch = my_branch + [name]

            if need_attach_range(name, obj):
                start, end = read_range(obj)
                name2 = "{}({}～{})".format(name, start, end)
            else:
                name2 = name

            mark = epubpacker.Mark(lang.c(name2))
            marks.append(mark)

            if is_leaf(obj) and need_join(obj): # 这是最后一个目录 且 短经很多
                _branch = my_branch + [name]
                doc_path = posixpath.join("", *new_branch) + ".xhtml"
                html, body = make_doc(doc_path, lang, new_branch[-1])

                for count, (sub_name, sub_obj) in enumerate(obj, start=1):
                    sutta_id = "sutta{}".format(count)
                    _, _, sutta_mark = write_sutta(parent_branch, sutta_id, sub_obj, notes, lang, html, body, doc_path)
                    mark.kids.append(sutta_mark)

                docs.append((doc_path, html))

            else:
                doc_path = _make_suttas(module, mark.kids, docs, my_branch, name, obj, notes, lang)
            mark.href = doc_path


        else:
            doc_path, html, mark = write_sutta(my_branch, "sutta1", obj, notes, lang)
            docs.append((doc_path, html))
            marks.append(mark)

        if first_doc_path is None:
            first_doc_path = doc_path

    return first_doc_path



def write_sutta(parent_branch, sutta_id, obj: xl.Xml, notes, lang, html=None, body=None, doc_path=None):
    sutta_name = get_sutta_name(obj.root)
    my_branch = parent_branch + [sutta_name]

    if doc_path is None:
        doc_path = posixpath.join("",*my_branch) + ".xhtml"
        html, body = make_doc(doc_path, lang, sutta_name)

    level = max(len(my_branch), 3)

    h = body.ekid("h" + str(level))
    h.attrs["class"] = "sutta_title"
    h.attrs["id"] = sutta_id

    sne = xl.Element("span", {"class": "sutta_nums"})

    sutta_num_abo = get_sutta_num_abo(obj.root)
    sutta_num_sc = get_sutta_num_sc(obj.root)

    if sutta_num_sc is not None:
        sc_a = xl.Element("a", {"href": "https://suttacentral.net/" + sutta_num_sc.replace(" ","")}, [sutta_num_sc])
        sc_a.attrs["class"] = "sutta_num_sc"
        sne.kids.append(sc_a)

    if sutta_num_abo and sutta_num_sc:
        sne.kids.append("/")

    if sutta_num_abo is not None:
        span = xl.Element("span", {"class": "sutta_num_abo"})
        span.kids.append(sutta_num_abo)
        #x = suttanum_ref.make_suttanum_xml(sutta_num, bns)
        #print(x[1].to_str())
        sne.kids.append(span)

    if sutta_num_abo and sutta_num_sc:
        h.kids.append(sne)
        h.kids.append("　")
    #####################################################
    serialized_nodes = []
    for node in parent_branch:
        m = re.match(r"^\d+\.(.+)$", node)
        if m:
            serialized_nodes.append(m.group(1))
    assert len(serialized_nodes) <= 1

    span = h.ekid("span", {"class": "sutta_name"})
    if serialized_nodes:
        name = "{}/{}".format(serialized_nodes[0], sutta_name)
    else:
        name = sutta_name

    span.kids.append(lang.c(name))

    xml_body = obj.root.find_descendants("body")[0]
    for xml_p in xml_body.find_descendants("p"):
        html_p = body.ekid("p")
        html_p.kids.extend(xml_es_to_html(xml_p.kids, obj.root, notes, doc_path, lang))


    start, end = get_sutta_range(obj.root)
    if start == end:
        _range = start
    else:
        _range = start + "～" + end

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

            elif e.tag == "j":
                if "p" in e.attrs.keys():
                    p = xl.Element("p")
                    p.kids.append(e.attrs["p"])
                    p.attrs["class"] = "person"
                    new_es.append(p)
                for p_e in e.kids:
                    p = xl.Element("p")
                    p.attrs["class"] = "ji"
                    p.kids.extend(xml_es_to_html(p_e.kids, root, notes, doc_path, lang))
                    new_es.append(p)

            elif m_n:
                pass

            else:
                print(e.to_str())
                raise Exception("Unknown element type")

        elif isinstance(e, str):
            #print("str:", e)
            new_es.extend(tag_str.str_to_es(lang.c(e)))
            #new_es.extend(suttanum_ref.make_suttanum_xml(lang.c(e), bns))

    return new_es


def _get_note_by_key(root: xl.Element, key: str):
    for e in root.kids:
        m_n = re.match(r"^n(\d+)$", e.tag)
        if m_n:
            if key == m_n.group(1):
                return e.kids

    raise Exception("Note not found")


def get_sutta_range(root: xl.Element):
    start = root.find_descendants("start")[0].kids[0]
    end = root.find_descendants("end")[0].kids[0]
    return start, end

def get_sutta_name(root: xl.Element):
    x = root.find_descendants("title")[0].kids[0]
    # input(x)
    return x

def get_sutta_num_abo(root: xl.Element):
    for sutta_num in root.find_descendants("sutta_num"):
        if sutta_num.attrs.get("type") is None:
            return sutta_num.kids[0]
    return None

def get_sutta_num_sc(root: xl.Element):
    for sutta_num in root.find_descendants("sutta_num"):
        if sutta_num.attrs.get("type") == "SC":
            return sutta_num.kids[0]
    return None

def get_source_page(root: xl.Element):
    return root.find_descendants("source_page")[0].kids[0]


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
    start = None
    for sub_name, sub_obj in obj:
        m1 = re.match(r"(\d+)\..+$", sub_name)
        m2 = re.match(r"^(\d+)-\d+\..+$", sub_name)
        m = m1 or m2
        if m:
            start = m.group(1)
        else:
            if isinstance(sub_obj, list):
                start = read_start(sub_obj)

        if start is not None:
            return start
    raise Exception("Start not found")


def read_end(obj: list):
    end = None
    for sub_name, sub_obj in obj[::-1]:
        m1 = re.match(r"(\d+)\..+$", sub_name)
        m2 = re.match(r"^\d+-(\d+)\..+$", sub_name)
        m = m1 or m2
        if m:
            end = m.group(1)
        else:
            if isinstance(sub_obj, list):
                end = read_end(sub_obj)
        if end is not None:
            return end
    raise Exception("End not found")


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
        xml: xl.Xml
        line_count = 0
        root = xml.root
        body = root.find_kids("body")[0]
        for p in body.find_kids("p"):
            txt = hyncdzj.utils.line_to_txt(p.kids)
            line_count += math.ceil(len(txt)/40)

        if line_count <= 30:
            small_page += 1
        else:
            large_page += 1
    try:
        if small_page / large_page > 1:
            return True
        else:
            return False
    except ZeroDivisionError:
        return True



def is_leaf(obj):
    if isinstance(obj, list):
        if isinstance(obj[0][1], xl.Xml):
            return True
        else:
            return False
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
