import os
import datetime
import posixpath
import shutil
import subprocess
import string

from boltons.setutils import IndexedSet

import xl
import epubpacker

from pyabo import book_public, page_parsing, note_thing
import dopdf
import doepub
from . import fanli, homage, notice
from . import css
from . import js


def make(nikaya, write_suttas_fun, xc: book_public.XC, temprootdir, books_dir, epubcheck):
    bn = nikaya.abbr.lower()
    mytemprootdir = os.path.join(temprootdir, "{}_epub_{}".format(bn, xc.enlang))
    os.makedirs(mytemprootdir, exist_ok=True)

    epub = create(nikaya, xc)
    bns = [nikaya.abbr]

    write_cover(epub, nikaya, xc, mytemprootdir)
    fanli.write_fanli(epub, xc)
    homage.write_homage(epub, xc, nikaya.homage_line)
    write_suttas_fun(nikaya=nikaya, epub=epub, bns=bns, xc=xc)
    write_notes(epub, nikaya, xc)
    notice.write_notice(epub, xc)

    mytemprootdir, epub_path = write2file(epub=epub, mytemprootdir=mytemprootdir, bn=bn)

    check_result = False
    if is_java_exist() and os.path.exists(epubcheck):
        check_result = check_epub(epub_path=epub_path, epubcheck=epubcheck, mytemprootdir=mytemprootdir)

    if is_java_exist() and os.path.exists(epubcheck) and check_result:
        copy2booksdir(epub_path=epub_path, nikaya=nikaya, xc=xc, books_dir=books_dir)


def is_java_exist():
    from shutil import which
    return which("java") is not None


def check_epub(epub_path, epubcheck, mytemprootdir):
    compile_cmd = "java -jar {} {} -q".format(epubcheck, epub_path)

    stdout_file = open(os.path.join(mytemprootdir, "cmd_stdout"), "w")
    stderr_file = open(os.path.join(mytemprootdir, "cmd_stderr"), "w")

    check_result = False

    def _run():
        nonlocal check_result
        print("执行检查:", repr(compile_cmd), end=" ", flush=True)
        p = subprocess.Popen(compile_cmd, cwd=mytemprootdir, shell=True,
                             stdout=stdout_file, stderr=stderr_file)
        p.communicate()
        if p.returncode != 0:
            check_result = False
        else:
            check_result = True
    _run()
    if check_result:
        print("没发现错误。")
    else:
        print("出错了！")
    return check_result


def copy2booksdir(epub_path, nikaya, xc, books_dir):
    shutil.copy(epub_path, os.path.join(books_dir, "{}_{}_莊春江{}{}_{}.epub".format(xc.c(nikaya.title_hant),
                                                                                   xc.zhlang,
                                                                                   nikaya.last_modified.strftime("%Y.%-m.%-d"),
                                                                                   xc.c("譯"),
                                                                                   datetime.datetime.now().strftime("%Y%m%d")
                                                                                   )))


def write2file(epub, mytemprootdir, bn):

    epub_path = os.path.join(mytemprootdir, "{}.epub".format(bn))
    epub.write(epub_path)
    return mytemprootdir, epub_path


def create(nikaya, xc: book_public.XC):
    epub = epubpacker.Epub()

    epub.meta.titles = [xc.c(nikaya.title_hant)]
    epub.meta.creators = ["莊春江({})".format(xc.c("譯"))]
    epub.meta.date = nikaya.last_modified.strftime("%Y-%m-%dT%H:%M:%SZ")
    epub.meta.languages = [xc.xmlang, "pi", "en-US"]

    my_uuid = doepub.get_uuid(xc.c(nikaya.title_hant) + xc.enlang)
    epub.meta.identifier = my_uuid.urn

    epub.meta.others.append(xl.Element("meta", {"property": "belongs-to-collection", "id": "c01"},
                                       ["莊春江" + xc.c("漢譯經藏")]))
    epub.meta.others.append(xl.Element("meta", {"refines": "#c01", "property": "collection-type"}, ["series"]))

    epub.userfiles[css.css1_path] = css.css1[xc.enlang]
    epub.userfiles[css.css2_path] = css.css2[xc.enlang]
    epub.userfiles[js.js1_path] = js.js1
    epub.userfiles["_css/user_css1.css"] = "/* 第一个自定义 CSS 文件 */\n\n"
    epub.userfiles["_css/user_css2.css"] = "/* 第二个自定义 CSS 文件 */\n\n"
    epub.userfiles["_js/user_js1.js"] = "// 第一个自定义 JS 文件\n\n"
    epub.userfiles["_js/user_js2.js"] = "// 第二个自定义 JS 文件\n\n"

    return epub


def write_notes(epub, nikaya, xc: book_public.XC):
    bns = [nikaya.abbr]
    _write_globalnotes(epub, bns, xc)
    first_note_doc_path = _write_localnotes(epub, nikaya.local_notes, bns, xc)
    epub.mark.kids.append(epubpacker.Mark(xc.c("註解"), first_note_doc_path))
    return epub


def _write_globalnotes(epub: epubpacker.Epub, bns, xc):
    notes = note_thing.get()
    docs = {}
    for key, note in notes.items():
        _doc_path = doepub.note_docname_calculate(page_parsing.GLOBAL, (key, "_x"))
        if _doc_path not in docs.keys():
            docs[_doc_path] = _make_note_doc(xc.c("註解二"), xc, _doc_path)
        _html, ol = docs[_doc_path]
        li = ol.ekid("li", {"id": key})

        p = li.ekid("p")
        es = []
        for subnote in note:
            es.extend(dopdf.join_to_xml(subnote, bns=bns, c=xc.c, doc_path=_doc_path))
            es.append(xl.Element("br"))
        p.kids.extend(es[:-1])

    for doc_path, (html, _ol) in docs.items():
        epub.userfiles[doc_path] = _doc_str(html)
        epub.spine.append(doc_path)


def _write_localnotes(epub: epubpacker.Epub, notes: IndexedSet, bns, xc):
    docs = {}

    for note in notes:
        _doc_path = doepub.note_docname_calculate(page_parsing.LOCAL, notes.index(note))
        if _doc_path not in docs.keys():
            docs[_doc_path] = _make_note_doc(xc.c("註解一"), xc, _doc_path)

        _html, ol = docs[_doc_path]

        li = ol.ekid("li", {"id": str(notes.index(note))})
        p = li.ekid("p")
        p.kids.extend(dopdf.join_to_xml(note, bns=bns, c=xc.c, doc_path=_doc_path))

    for doc_path, (html, _ol) in docs.items():
        epub.userfiles[doc_path] = _doc_str(html)
        epub.spine.append(doc_path)

    return list(docs.keys())[0]


def _make_note_doc(title, xc: book_public.XC, doc_path):
    html, body = make_doc(doc_path, xc, title)
    body.attrs["class"] = "note"
    sec = body.ekid("section", {"epub:type": "endnotes", "role": "doc-endnotes"})
    ol = sec.ekid("ol")
    return html, ol


def _doc_str(e):
    return xl.Xml(root=e).to_str(do_pretty=True, dont_do_tags=["p"])


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


def make_doc(doc_path, xc, title=None):
    html = xl.Element("html", {"xmlns:epub": "http://www.idpf.org/2007/ops",
                               "xmlns": "http://www.w3.org/1999/xhtml",
                               "xml:lang": xc.xmlang,
                               "lang": xc.xmlang})
    head = html.ekid("head")

    if title:
        _title = head.ekid("title", kids=[title])

    _make_css_link(head, doepub.relpath(css.css1_path, doc_path), "css1")
    _make_css_link(head, doepub.relpath("_css/user_css1.css", doc_path), "user_css1")
    _make_css_link(head, doepub.relpath("_css/user_css2.css", doc_path), "user_css2")
    _make_js_link(head, doepub.relpath(js.js1_path, doc_path), "js1")
    _make_js_link(head, doepub.relpath("_js/user_js1.js", doc_path), "user_js1")
    _make_js_link(head, doepub.relpath("_js/user_js2.js", doc_path), "user_js2")

    body = html.ekid("body")
    return html, body


def write_cover(epub, nikaya, xc: book_public.XC, _mytemprootdir):
    cover_xhtml_filename = "{}_{}_cover.xhtml".format(nikaya.abbr, xc.enlang)
    cover_img_filename = "{}_{}_cover.png".format(nikaya.abbr, xc.enlang)
    cover_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cover_images")
    os.makedirs(cover_dir, exist_ok=True)
    cover_img_path = os.path.join(cover_dir, cover_img_filename)

    if not os.path.exists(cover_img_path):
        _template_str = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cover.xhtml")).read()
        if isinstance(xc, book_public.SC):
            template_str = _template_str.replace("CJK TC", "CJK SC")
        else:
            template_str = _template_str
        t = string.Template(template_str)

        if len(nikaya.title_hant) == 2:
            title_hant = nikaya.title_hant[0] + "&nbsp;&nbsp;" + nikaya.title_hant[1]
        else:
            title_hant = nikaya.title_hant
        doc_str = \
            t.substitute(bookname_han=xc.c(title_hant),
                         bookname_pi=nikaya.title_pali,
                         han_version=xc.han_version,
                         translator="莊春江" + xc.c("譯"),
                         date=nikaya.last_modified.strftime("%Y年%-m月")
                         )
        open(os.path.join(cover_dir, cover_xhtml_filename), "w").write(doc_str)
        from html2image import Html2Image as HtI
        # Chrome 113 之前的几个版本有 bug，图像尺寸不对，所以暂时用 113 beta 版
        hti = HtI(browser_executable="google-chrome-stable", output_path=cover_dir)
        hti.screenshot(html_str=doc_str, size=(1600, 2560), save_as=cover_img_filename)
    assert os.path.exists(cover_img_path)

    cover_img_path_in_epub = posixpath.join(nikaya.abbr, cover_img_filename)
    epub.userfiles[cover_img_path_in_epub] = open(cover_img_path, "rb").read()
    epub.cover_img_path = cover_img_path_in_epub

    cover_doc_path = nikaya.abbr + "/cover.xhtml"
    html, body = make_doc(cover_doc_path, xc, "封面")
    body.attrs["style"] = "text-align: center;"

    _img = body.ekid("img", {"src": doepub.relpath(cover_img_path_in_epub, cover_doc_path),
                                "alt": "Cover Image",
                                "title": "Cover Image"})
    htmlstr = xl.Xml(root=html).to_str()
    epub.userfiles[cover_doc_path] = htmlstr
    epub.mark.kids.append(epubpacker.Mark("封面", cover_doc_path))
    epub.spine.append(cover_doc_path)
