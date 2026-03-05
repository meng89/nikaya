import os
import re
import uuid
import posixpath
import string
from urllib.parse import urlsplit

import cn2an

import epubpacker
import xl

import config
import share
from . import ebook_utils
import share.note
from share import new_page_or_not, epub_utils


def get_coll_by_translation(translation, lang):
    if translation is share.HYNCDZJ:
        return lang.c("元亨寺·漢譯南傳大藏經")
    else:
        return "莊春江·" + lang.c("漢譯經藏")


def create_epub(translation, title, collection, translators, identifier, lang, position=None):
    epub = epubpacker.Epub()
    epub.meta.identifier = identifier
    epub.meta.titles = [title]
    epub.meta.languages = [lang.xml, "pi", "en-US"]

    epub.meta.creators.append((list(translators), "trl")) #trl aut
    if translation is share.HYNCDZJ:
        epub.meta.contributors.append(("CBETA https://https://cbeta.org", "red"))
    epub.meta.contributors.append(("https://github.com/meng89/nikaya", "bkp"))

    epub.meta.others.append(xl.Element("meta", {"property": "belongs-to-collection", "id": "c01"},[collection]))
    epub.meta.others.append(xl.Element("meta", {"refines": "#c01", "property": "collection-type"}, ["set"])) # series
    if position:
        epub.meta.others.append(xl.Element("meta", {"refines": "#c01", "property": "group-position"}, [position]))
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


def build_epub_one_book(translation, cover_dir, full_file_name, info_datas, translators, lang, tag):
    collection = get_coll_by_translation(translation, lang)
    title = collection

    my_uuid = get_uuid(title + lang.en)

    epub = create_epub(translation, title, collection, translators, my_uuid.urn, lang)

    notes = share.note.Notes()

    if translation is share.HYNCDZJ:
        book_info = share.Info(name="漢譯南傳大藏經", pali="Tipiṭaka", translators=tuple(translators))
        image_path = ebook_utils.make_hyncdzj_cover_image(cover_dir, book_info, lang, tag, onebook=True)
    else:

        book_info = share.Info(name="漢譯經藏", pali="Sutta Piṭaka", translators=tuple(translators))
        image_path =  ebook_utils.make_abo_cover_image(cover_dir, book_info, lang, onebook=True)
    _write_cover(epub, image_path, lang)

    if translation is share.HYNCDZJ:
        _write_homage_hyncdzj(epub, lang)
    else:
        _write_fanli(epub, lang)
        _write_homage_abo(epub, lang)

    doc_files = {}

    def _xyz(_info_datas, _marks, _pngs=None, _depth=0):
        _pngs = _pngs or []
        for _sub in _info_datas:
            assert isinstance(_sub, tuple)
            if len(_sub) == 3:
                _name, _info, _data = _sub
                _mark = epubpacker.Mark(_name)
                _marks.append(_mark)
                _ds_depth = new_page_or_not.get_data_depth(_data)
                write_tree(translation, _info, _ds_depth, _pngs + [(None, None, _name)], [], _data, _depth, doc_files, _mark.kids, notes, lang, [], 0,
                           1, None, None, None)

            if len(_sub) == 2:
                _name, _sub_list = _sub
                _mark = epubpacker.Mark(_name)
                _marks.append(_mark)
                _xyz(_sub_list, _mark.kids, _pngs + [(None, None, _name)], _depth + 1)

    _xyz(info_datas, epub.mark.kids)

    write_css(epub, lang)
    write_note_spile(notes, epub, lang)
    write_doc_files(doc_files, epub)

    if translation is share.HYNCDZJ:
        _write_readme(README_HYNCDZJ, epub, notes, lang)
    else:
        _write_readme(README_ABO, epub, notes, lang)

    make_marks_href(epub.mark.kids)

    epub.write(full_file_name)

    write_css(epub, lang)


def build_epub(translation, cover_dir, full_path, data, info, lang, tag):
    collection = get_coll_by_translation(translation, lang)
    if translation is share.HYNCDZJ:
        title = lang.c("元亨寺·" + info.name)
    else:
        title = "莊春江·" + lang.c(info.name)

    my_uuid = get_uuid(title + lang.en)

    count = share.get_count_by_info(info)
    epub = create_epub(translation, title, collection, info.translators, my_uuid.urn, lang, str(count))

    notes = share.note.Notes()

    if translation is share.HYNCDZJ:
        image_path = ebook_utils.make_hyncdzj_cover_image(cover_dir, info, lang, tag, onebook=False)
    else:
        image_path = ebook_utils.make_abo_cover_image(cover_dir, info, lang, onebook=False)
    _write_cover(epub, image_path, lang)

    if translation is share.HYNCDZJ:
        _write_homage_hyncdzj(epub, lang)
    else:
        _write_fanli(epub, lang)
        _write_homage_abo(epub, lang)

    write_css(epub, lang)

    doc_files = {}
    ds_depth = new_page_or_not.get_data_depth(data)
    write_tree(translation, info, ds_depth, [], [], data, -1, doc_files, epub.mark.kids, notes, lang, [], 0, 1, None, None, None)

    for path, xml in doc_files.items():
        xml: xl.Xml
        epub.userfiles[path] = xml.to_str(do_pretty=True,
                                          dont_do_tags=["title", "h1", "h2", "h3", "h4", "h5", "h6", "h7", "a", "span", "p"])
        epub.spine.append(path)

    for title, path, page in notes.get_pages(lang):
        epub.userfiles[path] = page
        epub.spine.append(path)

    if translation is share.HYNCDZJ:
        _write_readme(README_HYNCDZJ, epub, notes, lang)
    else:
        _write_readme(README_ABO, epub, notes, lang)

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
    return x or "—"


"""
经的上级标题需要写入第一个经里。
"""

def write_tree(translation, info, ds_depth, p_ngs, ngs, obj, root_depth, doc_files, marks, notes, lang, marks_and_headings, depth, id_count, doc_path, html, body, doc_depth=None):
    sub_marks = marks

    if ngs:
        mark, heading = make_mh(info, ngs, obj, marks, depth, id_count, lang)
        marks_and_headings.append((mark, heading))
        sub_marks = mark.kids
    # 在第一个需要合并的经之前的节点创建 doc

    if doc_path is None:
        merge_or_not = new_page_or_not.merge_or_not(ngs, obj, ds_depth)
        # 下级如果没有分页，此级就要合并
        if merge_or_not:
            doc_depth = root_depth + depth
            doc_path, html, body = write_docs(doc_files, p_ngs + ngs, doc_depth, lang, info)

    for sub_id_count, (namegroup, sub) in enumerate(obj, 1):
        s_ngs = ngs + [namegroup]

        if isinstance(sub, xl.Element):
            write_doc(info, p_ngs, s_ngs, root_depth, sub, doc_files, sub_marks, notes, lang,
                      marks_and_headings, depth + 1, sub_id_count, doc_path, body, doc_depth)
        else:
            write_tree(translation, info, ds_depth, p_ngs, s_ngs, sub, root_depth, doc_files, sub_marks, notes, lang,
                       marks_and_headings, depth + 1, sub_id_count, doc_path, html, body, doc_depth)


def write_doc(info, p_ngs, ngs, root_depth, obj, doc_files, marks, notes, lang, marks_and_headings, depth, id_count, doc_path, body, doc_depth):
    if doc_path is None:
        doc_depth = root_depth + depth
        doc_path, html, body = write_docs(doc_files, p_ngs + ngs, doc_depth, lang, info)

    # 把上级的 heading 写入文档先
    write_marks_and_headings(marks_and_headings, body, doc_path)

    if ngs:
        mark, heading = make_mh(info, ngs, obj, marks, depth, id_count, lang)
        mark.href = "{}#{}".format(doc_path, heading.attrs["id"])
        body.kids.append(heading)

    for e in obj.kids:
        if isinstance(e, xl.Element) and re.match(r"^n\d+$", e.tag):
            break

        else:
            html_es = xml_es_to_html([e], obj, notes, doc_depth, lang)
            body.kids.extend(html_es)


def make_mh(info, namegroups, obj, marks, depth, id_count, lang):
    mark, heading, _, _, _, _, = make_mark_and_heading(info, namegroups, obj, depth, lang)
    heading.attrs["id"] = "id_{}_{}".format(depth, id_count)
    marks.append(mark)
    return mark, heading

def write_docs(doc_files, ngs, depth, lang, info):
    test_path = [share.namegroup_to_filename(ng) for ng in ngs]
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


def make_mark_and_heading(info, namegroups, obj, heading_level, lang):
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
        a = xl.Element("a", {"class": "sc_link", "href": "https://suttacentral.net/" + range_str}, [range_str])
        epub_heading.kids.append(a)
        epub_heading.kids.append(" ")
        is_serial = True
        mark_name = ranges[-1] + "." + or_kong(serial_names[-1]) + mark_range
    else:
        range_str = None
        name_str = or_kong(names[-1])
        mark_name = or_kong(names[-1]) + mark_range
        is_serial = False

    epub_mark = epubpacker.Mark(mark_name)
    epub_heading.kids.append(name_str)

    source_page = get_source_page(obj)
    if source_page is not None:
        epub_heading.kids.append(" ")
        _a = xl.Element("a", {"class": "abo_translate", "href": config.ABO_WEBSITE + "/" + source_page}, ["（莊春江" + lang.c("譯") + "）"])
        epub_heading.kids.append(_a)

    return epub_mark, epub_heading, is_serial, mark_name, range_str, name_str


def get_source_page(obj):
    if not isinstance(obj, xl.Element):
        return None

    for e in obj.kids:
        if isinstance(e, xl.Element) and e.tag == "meta":
            for e2 in e.kids:
                if isinstance(e2, xl.Element) and e2.tag == "source_page":
                    return e2.kids[0]
    return None


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
    return share.filename_to_namegroup(s)

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

def xml_es_to_html(es: ES, root, notes: share.note.Notes, doc_depth, lang) -> ES:
    new_es = []
    for e in es:
        if isinstance(e, xl.Element):
            m_t = re.match(r"^t(\d+)$", e.tag) # 本地注解
            m_n = re.match(r"^n\d+$", e.tag) # doc n元素
            m_g = re.match(r"^g(\d+)$", e.tag) # 庄春江 全局注解
            if m_t:
                a = xl.Element("a", attrs={"epub:type": "noteref"})
                key = m_t.group(1)

                n_kids = get_note_by_key(root, key)
                if n_kids is None: # 庄春江 缺失注解
                    new_es.extend(e.kids)
                    continue

                link = notes.add_note(n_kids)
                a.attrs["href"] = "../" * doc_depth + link
                if len(e.kids) > 0:
                    a.kids.extend(xml_es_to_html(e.kids, root, notes, doc_depth, lang))
                else:
                    a.attrs["class"] = "no_text_noteref"
                    a.kids.append("注")

                new_es.append(a)

            elif m_g:
                abo_gn = share.note.get_abo_global_notes()
                a = xl.Element("a", attrs={"epub:type": "noteref"})
                n_kids = abo_gn.get_es(m_g.group(1))
                link = notes.add_note(n_kids)
                a.attrs["href"] = "../" * doc_depth + link
                a.kids.extend(xml_es_to_html(e.kids, root, notes, doc_depth, lang))
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
            elif e.tag == "meta":
                pass
            elif e.tag == "span":
                new_es.extend(e.kids)
            elif e.tag == "br":
                pass
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
    #print("Note not found:", key)
    return None
    raise Exception("Note not found", repr(key))


def write_css(epub, lang):
    css_t = open(os.path.join(config.RESOURCE_DIR, "style.css"), "r").read()

    if isinstance(lang, share.SC):
        heading_font_name = """ "Microsoft YaHei", "PingFang SC", "思源黑体 CN", "Noto Sans CJK SC" """
        body_font_name = """ "Source Han Serif SC", "Noto Serif CJK SC", "SimSun", "Songti SC" """

    else:
        heading_font_name = """ "Microsoft JhengHei", "PingFang TC", "思源黑體 TW", "Noto Sans CJK TC" """
        body_font_name = """ "Source Han Serif TC", "Noto Serif CJK TC", "PMingLiU", "Songti TC" """

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

    href = "../" * depth + "style.css"
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

HOMAGE_LINE = [
    "歸命彼世尊",
    "應供等覺者"
]

def _write_homage_hyncdzj(epub, lang):
    doc_path = "homage.xhtml"
    html, body = make_doc(0, lang, lang.c("禮敬偈"))
    body.attrs["class"] = "hyncdzj_homage"

    for line in HOMAGE_LINE:
        p = body.ekid("p")
        p.kids.append(lang.c(line))

    htmlstr = xl.Xml(root=html).to_str(do_pretty=True, dont_do_tags=["p"])
    epub.userfiles[doc_path] = htmlstr
    epub.spine.append(doc_path)
    epub.mark.kids.append(epubpacker.Mark(lang.c("禮敬偈"), doc_path))



def _write_homage_abo(epub, lang):
    doc_path = "homage.xhtml"
    html, body = make_doc(0, lang, lang.c("禮敬世尊"))
    body.attrs["class"] = "abo_homage"

    p = body.ekid("p")
    p.kids = ["對那位世尊、阿羅漢、遍正覺者禮敬"]

    htmlstr = xl.Xml(root=html).to_str(do_pretty=True, dont_do_tags=["p"])
    epub.userfiles[doc_path] = htmlstr
    epub.spine.append(doc_path)
    epub.mark.kids.append(epubpacker.Mark(lang.c("禮敬世尊"), doc_path))


FANLI = (
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

def _write_fanli(epub, lang):
    doc_path = "fanli.xhtml"
    html, body = make_doc(0, lang, "凡例")
    body.attrs["class"] = "fanli"
    _h1 = body.ekid("h1", {"class": "title"}, ["凡例"])

    for line in FANLI:
        _p = body.ekid("p")
        _p.kids.append(lang.c(line))

    htmlstr = xl.Xml(root=html).to_str(do_pretty=True, dont_do_tags=["p"])
    epub.userfiles[doc_path] = htmlstr
    epub.spine.append(doc_path)
    epub.mark.kids.append(epubpacker.Mark("凡例", doc_path))


_releases_link = "https://github.com/meng89/hyncdzj/releases"
_releases_e = xl.Element("a", {"href": _releases_link}, [_releases_link])

_jianguoyun_link = "https://www.jianguoyun.com/p/DbBOkGwQnbmtChjWkpIGIAA"
_jianguoyun_e = xl.Element("a", {"href": _jianguoyun_link}, [_jianguoyun_link])

_lanzouyun_link = "https://wwaxq.lanzouv.com/b019vpg2hi"
_lanzhouyun_e = xl.Element("a", {"href": _lanzouyun_link}, [_lanzouyun_link])

_googleyunpan_link = "https://drive.google.com/drive/folders/1kCVtONm0Jq0LRz0Fp3WATg-F74dRGx4K?usp=sharing"
_googleyunpan_e = xl.Element("a", {"href": _googleyunpan_link}, [_googleyunpan_link])

_my_mail = "observerchan@gmail.com"
_my_mail_e = xl.Element("a", {"href": "mailto:{}".format(_my_mail)}, [_my_mail])
_cbeta = xl.Element("a", {"href": "https://www.cbeta.org/"}, ["CBETA"],)

README_SHARE = [
    ["点击标题前面的经号，如 SN1.1，可以打开 SuttaCentral.net 网站里含有此章节其它译文列表的页面。",
     "部分书籍没有整理出对应的经号，已有的经号有可能有对应错误。"],
    ["推荐在电脑上使用 Okular 阅读莊春江 PDF，使用 Calibre 里的 E-book viewer 阅读 EPUB。"],
    ["获取莊春江和元亨寺的各种版本电子书：合订本，分割本、简体、繁体、PDF 以及 EPUB，请访问下面的云盘。"
     "云盘里也收录蕭式球老师翻译的现代白话四部尼柯耶。"],
    ["蓝奏云，密码 123456："],
    [_lanzhouyun_e, " "],
    ["坚果云，需要登录："],
    [_jianguoyun_e],
    ["Google 云盘："],
    [_googleyunpan_e],
    # ("如果打不开上面的链接，请尝试这个云盘链接：", xl.Element("a", {"href": "{}".format(_yunpan_link)}, [_yunpan_link])),
    ["如有任何与此电子书制作程序相关的问题，或者电子书获取困难，请联系我："],
    [_my_mail_e],
]

README_HYNCDZJ = [
    ["此佛经译著权归属于元亨寺及其译者。电子书基于 ", _cbeta, " 数字化数据制作。"],
] + README_SHARE

_ccc_e = xl.Element("a", {"href": "https://agama.buddhason.org"}, ["莊春江讀經站"])
README_ABO = [
    ["此汉译佛经数据来自", _ccc_e, "，一切相关权利归于译者或权利所持有人。"],
    ["本生经因未翻译完成，所以未制作电子书。"],
    ["原文是繁体中文，简体版由程序转换，可能会出现转换错误。电子书的目录以及经文标题部分可能有一些修改，正文部分与原页面相同，但可能丢失了链接和文字格式等元数据。"],
    ["点击经文的标题后面括号里的译者会打开莊春江读经站的经文原页，原页有巴利语对照，及与经文相关的其它经文链接。"],
] + README_SHARE

def _write_readme(readme, epub, notes, lang):
    doc_path = "readme.xhtml"
    html, body = make_doc(0, lang, lang.c("說明"))

    body.attrs["class"] = "readme"

    _h1 = body.ekid("h1", {"class": "title"}, [lang.c("說明")])
    for line in readme:
        _p = body.ekid("p", kids=xml_es_to_html(line, html, notes, doc_path, lang))

    htmlstr = xl.Xml(root=html).to_str(do_pretty=True, dont_do_tags=["p"])
    epub.userfiles[doc_path] = htmlstr
    epub.spine.append(doc_path)
    epub.mark.kids.append(epubpacker.Mark(lang.c("說明"), doc_path))


def get_uuid(s):
    return uuid.uuid5(uuid.NAMESPACE_URL, "https://github.com/meng89/nikaya" + " " + s)
