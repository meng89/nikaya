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
import pyabo2.utils
import pyabo2.note
from . import css, js
from . import ebook_utils
from . import suttanum_ref
from . import tag_str


def make_epub(data, module, lang):
    epub = epubpacker.Epub()

    epub.meta.titles = [lang.c(module.name_han)]
    epub.meta.creators = ["莊春江({})".format(lang.c("譯"))]
    ts = ebook_utils.read_timestamp(data)
    epub.meta.date = datetime.fromtimestamp(ts).astimezone().strftime("%Y-%m-%dT%H:%M:%SZ")
    epub.meta.languages = [lang.xml, "pi", "en-US"]

    my_uuid = get_uuid(lang.c(module.name_han) + lang.en)
    epub.meta.identifier = my_uuid.urn

    epub.meta.others.append(xl.Element("meta", {"property": "belongs-to-collection", "id": "c01"},
                                       ["莊春江" + lang.c("漢譯經藏")]))
    epub.meta.others.append(xl.Element("meta", {"refines": "#c01", "property": "collection-type"}, ["series"]))

    epub.userfiles[css.css1_path] = css.css1[lang.en]
    #epub.userfiles[css.css2_path] = css.css2[lang.en]
    epub.userfiles[js.js1_path] = js.js1
    #epub.userfiles["_css/user_css1.css"] = "/* 第一个自定义 CSS 文件 */\n\n"
    #epub.userfiles["_css/user_css2.css"] = "/* 第二个自定义 CSS 文件 */\n\n"
    #epub.userfiles["_js/user_js1.js"] = "// 第一个自定义 JS 文件\n\n"
    #epub.userfiles["_js/user_js2.js"] = "// 第二个自定义 JS 文件\n\n"

    ln = pyabo2.note.LocalNotes()
    gn = pyabo2.note.get_gn()
    docs = []
    refs = []
    bns = [module.short]

    _write_cover(epub, ebook_utils.make_cover(module, data, lang), lang)
    _write_fanli(bns, epub, ln, gn, lang)
    _write_homage(bns, module, epub.mark.kids, docs, ln, gn, lang)

    _make_suttas(bns, module, epub.mark.kids, docs, refs, [], data, ln, gn, lang)

    _inbookref_to_href(docs)

    for path, xml in docs:
        epub.userfiles[path] = xml.to_str()
        epub.spine.append(path)

    for title, path, page in ln.get_pages(bns, lang):
        epub.userfiles[path] = page
        epub.spine.append(path)

    for title, path, page in gn.get_pages(bns, lang):
        epub.userfiles[path] = page
        epub.spine.append(path)

    _write_readme(epub, lang)

    return epub

# refs = [("PS/Ps1.html", "id", "PS/PS.1.xhtml", "id2")]

def _inbookref_to_href(docs):
    new_docs = []
    for path, e in docs:
        new_e = copy.deepcopy(e)
        _e_inbookref_to_href(path, new_e, docs)
        new_docs.append((path, new_e))
    return new_docs

def _e_inbookref_to_href(path, e: xl.Element, docs):
    for kid in e.kids:
        if isinstance(kid, xl.Element):
            # <a in_book_ref="SN.1.1">xxx</a> ->
            # 1. <a href="sn/sn.1.1.xhtml#SN.1.1>xxx</a>
            # 2. <a href="#SN.1.1>xxx</a>
            ref = kid.attrs.get("inbookref")
            if ref:
                result = _find_path(ref, docs)
                if result[0]:
                    kid.attrs["href"] = relpath(result, path) + "#" + ref
                    kid.attrs.pop("inbookref")
            _e_inbookref_to_href(path, kid, docs)

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


def _make_suttas(bns, module, marks: list[epubpacker.Mark], docs, refs, branch: list, data, ln, gn, lang):
    first_doc_path = None

    for name, obj in data:
        if isinstance(obj, list):
            new_branch = branch + [name]
            if need_attach_range(name, obj):
                start, end = read_range(obj)
                name2 = "{}({}～{})".format(name, start, end)
            else:
                name2 = name
            mark = epubpacker.Mark(lang.c(name2))
            marks.append(mark)

            if is_leaf(obj) and need_join(obj):
                doc_path = posixpath.join("", *branch) + ".xhtml"
                html, body = make_doc(doc_path, lang, branch[-1])
                h = body.ekid("h{}".format(len(branch)))
                h.kids.append(branch[-1])
                for sub_name, sub_obj in obj:
                    sub_branch = branch + [sub_name]
                    write_one_doc(bns, sub_branch, doc_path, body, sub_obj, refs, ln, gn, lang)
                docs.append((doc_path, html))

            else:
                doc_path = _make_suttas(bns, module, mark.kids, docs, refs, new_branch, obj, ln, gn, lang)
            mark.href = doc_path

        else:
            title = get_sutta_name(obj.root)
            start, end = get_sutta_range(obj.root)
            if start == end:
                _range = start
            else:
                _range = start + "～" + end

            new_branch = branch + [title]
            doc_path = posixpath.join("",*new_branch) + ".xhtml"
            html, body = make_doc(doc_path, lang, title)
            write_one_doc(bns, new_branch, doc_path, body, obj, refs, ln, gn, lang)
            docs.append((doc_path, html))
            marks.append(epubpacker.Mark("{}.{}".format(_range, lang.c(title)), href=doc_path))

        if first_doc_path is None:
            first_doc_path = doc_path

    return first_doc_path



def write_one_doc(bns, branch, doc_path, body, obj: xl.Xml, refs, ln, gn, lang):
    h = body.ekid("h" + str(len(branch) + 1))
    h.attrs["class"] = "title"

    sne = xl.Element("span", {"class": "sutta_num"})

    sutta_num = get_sutta_num(obj.root)
    sutta_num_sc = get_sutta_num_sc(obj.root)

    if sutta_num is not None:
        #x = suttanum_ref.make_suttanum_xml(sutta_num, bns)
        #print(x[1].to_str())
        sne.kids.append(sutta_num)

    if sutta_num and sutta_num_sc:
        sne.kids.append("/")

    if sutta_num_sc is not None:
        sc_a = xl.Element("a", {"href": "https://suttacentral.net/" + sutta_num_sc.replace(" ","")}, [sutta_num_sc])
        sc_a.attrs["class"] = "sutta_name"
        sne.kids.append(sc_a)

    if sutta_num and sutta_num_sc:
        h.kids.append(sne)
        h.kids.append("　")

    serialized_nodes = []
    for node in branch[0: -1]:
        m = re.match(r"^\d+\.(.+)$", node)
        if m:
            serialized_nodes.append(m.group(1))
    assert len(serialized_nodes) <= 1

    a = h.ekid("a")
    a.attrs["href"] = urllib.parse.urljoin(config.ABO_WEBSITE,get_source_page(obj.root))
    if serialized_nodes:
        name = "{}/{}".format(serialized_nodes[0], branch[-1])
    else:
        name = branch[-1]

    a.kids.append(lang.c(name))

    xml_body = obj.root.find_descendants("body")[0]
    for xml_p in xml_body.find_descendants("p"):
        html_p = body.ekid("p")
        html_p.kids.extend(_xml_es_to_html(bns, xml_p.kids, obj.root, ln, gn, doc_path, lang))


ES = list[xl.Element | str]

def _xml_es_to_html(bns, es: ES, root, ln, gn: pyabo2.note.GlobalNotes, doc_path, lang) -> ES:
    new_es = []
    for e in es:
        if isinstance(e, xl.Element):
            if e.tag == "gn":
                a = xl.Element("a", attrs={"epub:type": "noteref"})
                link = gn.get_link(e.attrs["id"])
                href = relpath(link, doc_path)
                a.attrs["href"] = href
                a.attrs["class"] = "noteref"
                a.kids.extend(_xml_es_to_html(bns, e.kids, root, ln, gn, doc_path, lang))
                new_es.append(a)

            elif e.tag == "ln":
                a = xl.Element("a", attrs={"epub:type": "noteref"})
                _id = e.attrs["id"]
                link = _get_ln_link_by_id(root, ln, _id)
                href = relpath(link, doc_path)
                a.attrs["href"] = href
                a.attrs["class"] = "noteref"
                a.kids.extend(_xml_es_to_html(bns, e.kids, root, ln, gn, doc_path, lang))

            elif e.tag == "a" and "href" in e.attrs.keys() and "id" in e.attrs.keys():
                new_es.append(e)
            elif e.tag == "a" and "href" in e.attrs.keys() and "target" in e.attrs.keys():
                new_es.append(e)
            elif e.tag == "span" and "style" in e.attrs.keys():
                new_es.append(e)
            elif len(e.kids) == 0:
                pass
            else:
                print(e.to_str())
                raise Exception("Unknown element type")

        elif isinstance(e, str):
            new_es.extend(tag_str.str_to_es(lang.c(e)))
            #new_es.extend(suttanum_ref.make_suttanum_xml(lang.c(e), bns))

    return new_es


def _get_ln_link_by_id(root, ln, id_):
    for note in root.find_descendants("notes")[0].kids:
        if note.attrs.get("id") == id_:
            link = ln.add(note.kids)
            return link

    return ln.add("*没有注解*")



def get_sutta_range(root: xl.Element):
    start = root.find_descendants("start")[0].kids[0]
    end = root.find_descendants("end")[0].kids[0]
    return start, end

def get_sutta_name(root: xl.Element):
    x = root.find_descendants("title")[0].kids[0]
    # input(x)
    return x

def get_sutta_num(root: xl.Element):
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
    sub_name, sub_obj = obj[0]
    if isinstance(sub_obj, list):
        m = re.match(r"^(\d+)\..+$", sub_name)
        if m:
            return m.group(1)
        else:
            return read_start(sub_obj)
    else:
        return sub_obj.root.find_descendants("start")[0].kids[0]

def read_end(obj):
    sub_name, sub_obj = obj[-1]
    if isinstance(sub_obj, list):
        m = re.match(r"^(\d+)\..+$", sub_name)
        if m:
            return m.group(1)
        else:
            return read_end(sub_obj)
    else:
        return sub_obj.root.find_descendants("end")[0].kids[0]


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
                               "xml:lang": lang.xml,
                               "lang": lang.xml})
    head = html.ekid("head")

    if title:
        _title = head.ekid("title", kids=[title])

    _make_css_link(head, relpath(css.css1_path, doc_path), "css1")
    #_make_css_link(head, relpath("_css/user_css1.css", doc_path), "user_css1")
    #_make_css_link(head, relpath("_css/user_css2.css", doc_path), "user_css2")
    _make_js_link(head, relpath(js.js1_path, doc_path), "js1")
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
    body.attrs["style"] = "text-align: center;"

    _img = body.ekid("img", {"src": relpath(base_name, cover_doc_path),
                             "alt": "Cover Image",
                             "title": "Cover Image"})
    htmlstr = xl.Xml(root=html).to_str()
    epub.userfiles[cover_doc_path] = htmlstr
    epub.mark.kids.append(epubpacker.Mark("封面", cover_doc_path))
    epub.spine.append(cover_doc_path)


def _write_homage(bns, _module, marks, docs, ln, gn, lang):
    doc_path = "homage.xhtml"
    html, body = make_doc(doc_path, lang, lang.c("禮敬世尊"))
    body.attrs["class"] = "homage"

    outdiv = body.ekid("div", {"class": "homage_out"})
    indiv = outdiv.ekid("div", {"class": "homage_in"})

    kids = xl.parse("""<p>對那位<gn id="12">世尊</gn>、<gn id="5">阿羅漢</gn>、<gn id="6">遍正覺者</gn>禮敬</p>""").root.kids
    p = indiv.ekid("p")
    p.kids.extend(_xml_es_to_html(bns, kids, html, ln, gn, doc_path, lang))
    #indiv.kids.append())

    docs.append((doc_path, html))
    marks.append(epubpacker.Mark(lang.c("禮敬世尊"), doc_path))


_project_link = "https://github.com/meng89/nikaya"
_yunpan_link = "https://www.jianguoyun.com/p/DbVa44QQnbmtChiojLEE"
_my_mail = "observerchan@gmail.com"



_fanli = (
    "1.巴利語經文與經號均依 tipitaka.org (緬甸版)。",

    "2.巴利語經文之譯詞，依拙編《簡要巴漢辭典》，詞性、語態儘量維持與巴利語原文相同，並採「直譯」原則。"
    "譯文之「性、數、格、語態」儘量符合原文，「呼格」(稱呼；呼叫某人)以標點符號「！」表示。",

    "3.註解中作以比對的英譯，採用Bhikkhu Ñaṇamoli and Bhikkhu Bodhi,Wisdom Publication,1995年版譯本為主。",

    "4.《顯揚真義》(Sāratthappakāsinī, 核心義理的說明)為《相應部》的註釋書，"
    "《破斥猶豫》(Papañcasūdaṇī, 虛妄的破壞)為《中部》的註釋書，"
    "《吉祥悅意》(Sumaṅgalavilāsinī, 善吉祥的優美)為《長部》的註釋書，"
    "《滿足希求》(Manorathapūraṇī, 心願的充滿)為《增支部》的註釋書，"
    "《勝義光明》(paramatthajotikā, 最上義的說明)為《小部/經集》等的註釋書，"
    "《勝義燈》(paramatthadīpanī, 最上義的註釋)為《小部/長老偈》等的註釋書。",

    "5.前後相關或對比的詞就可能以「；」區隔強調，而不只限於句或段落。"
)

def _write_fanli(bns, epub, ln, gn, lang):
    doc_path = "fanli.xhtml"
    html, body = make_doc(doc_path, lang, "凡例")
    body.attrs["class"] = "fanli"
    _h1 = body.ekid("h1", {"class": "title"}, ["凡例"])

    for one in _fanli:
        _p = body.ekid("p", kids=_xml_es_to_html(bns, [one], html, ln, gn, doc_path, lang))

    htmlstr = xl.Xml(root=html).to_str(do_pretty=True, dont_do_tags=["p"])
    epub.userfiles[doc_path] = htmlstr
    epub.spine.append(doc_path)
    epub.mark.kids.append(epubpacker.Mark("凡例", doc_path))


_lines = (
    ("此汉译佛经数据来源于", xl.Element("a", {"href": "https://agama.buddhason.org"}, ["莊春江讀經站"]),"，一切相关权利归于译者。"),
    ("原译文是繁体中文，简体版由程序转换，可能会出现转换错误。电子书目录以及经文标题部分可能有一些修改，正文部分与原页面相同，但可能丢失了一部分链接和格式等元数据。",
     "页面标题的经号里，以小数点隔离书籍缩写与数字的是原经号，如：Ud.1。无小数点的是suttacentral.net网站风格的经号，如：Ud1.1，点击可以打开suttacentral.net网站对应的其它语言译文的页面。",
     "部分书籍没有整理出对应的经号，已有的经号有可能会有对应错误。如有发现，请帮忙指正，谢谢！"),
    ("要获取最新制成的电子书，请访问项目主页：",
     xl.Element("a", {"href": "{}".format(_project_link)}, [_project_link])),
    #("如果打不开上面的链接，请尝试这个云盘链接：", xl.Element("a", {"href": "{}".format(_yunpan_link)}, [_yunpan_link])),
    ("若难以下载电子书，或者有对此电子书相关的其它问题，请联系我：", xl.Element("a", {"href": "mailto:{}".format(_my_mail)}, [_my_mail]))
)

def _write_readme(epub, lang):
    doc_path = "readme.xhtml"
    html, body = make_doc(doc_path, lang, "电子书说明")

    body.attrs["class"] = "readme"

    _h1 = body.ekid("h1", {"class": "title"}, ["电子书说明"])
    for line in _lines:
        _p = body.ekid("p", kids=list(line))

    htmlstr = xl.Xml(root=html).to_str(do_pretty=True, dont_do_tags=["p"])
    epub.userfiles[doc_path] = htmlstr
    epub.spine.append(doc_path)
    epub.mark.kids.append(epubpacker.Mark(lang.c("电子书说明"), doc_path))


def get_uuid(s):
    return uuid.uuid5(uuid.NAMESPACE_URL, "https://github.com/meng89/nikaya" + " " + s)
