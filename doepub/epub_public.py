import os
import datetime
import shutil
import subprocess

from boltons.setutils import IndexedSet

import xl
import epubpacker

from pyabo import book_public, page_parsing, note_thing
import dopdf
import doepub
from . import fanli, homage, notice
from .css import public, public_path, font_path, font_css


def make(nikaya, write_suttas_fun, xc: book_public.XC, temprootdir, books_dir, epubcheck):
    epub = create(nikaya, xc)
    bns = [nikaya.abbr]
    write_suttas_fun(nikaya=nikaya, epub=epub, bns=bns, xc=xc)
    epub = write_notes(epub, nikaya, xc)

    notice.write_notice(epub, xc)
    mytemprootdir, epub_path = write2file(epub=epub, xc=xc, temprootdir=temprootdir, bn=nikaya.abbr.lower())

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
        print("运行:", compile_cmd, end=" ", flush=True)
        p = subprocess.Popen(compile_cmd, cwd=mytemprootdir, shell=True,
                             stdout=stdout_file, stderr=stderr_file)
        p.communicate()
        if p.returncode != 0:
            check_result = False
        else:
            check_result = True
    _run()
    if check_result:
        print("成功！")
    else:
        print("出错！")
    return check_result


def copy2booksdir(epub_path, nikaya, xc, books_dir):
    shutil.copy(epub_path,
                os.path.join(books_dir, "{}_{}_{}{}_{}.epub".format(xc.c(nikaya.title_zh),
                                                                    xc.zhlang,
                                                                    "莊",
                                                                    nikaya.last_modified.strftime("%y%m"),
                                                                    datetime.datetime.now().strftime("%Y%m%d"))))


def write2file(epub, temprootdir, xc, bn):
    mytemprootdir = os.path.join(temprootdir, "{}_epub_{}".format(bn, xc.enlang))
    os.makedirs(mytemprootdir, exist_ok=True)

    epub_path = os.path.join(mytemprootdir, "{}.epub".format(bn))
    epub.write(epub_path)
    return mytemprootdir, epub_path


def create(nikaya, xc: book_public.XC):
    epub = epubpacker.Epub()
    doepub.write_epub_cssjs(epub)

    epub.meta.titles = [xc.c(nikaya.title_zh)]
    epub.meta.creators = ["莊春江({})".format(xc.c("譯"))]
    epub.meta.date = nikaya.last_modified.strftime("%Y-%m-%dT%H:%M:%SZ")
    epub.meta.languages = [xc.xmlang, "pi", "en-US"]

    my_uuid = doepub.get_uuid(xc.c(nikaya.title_zh) + xc.enlang)
    epub.meta.identifier = my_uuid.urn

    epub.meta.others.append(xl.Element("meta", {"property": "belongs-to-collection", "id": "c01"},
                                       ["莊春江" + xc.c("漢譯經藏")]))
    epub.meta.others.append(xl.Element("meta", {"refines": "#c01", "property": "collection-type"}, ["series"]))

    epub.userfiles[public_path] = public
    epub.userfiles[font_path[xc.enlang]] = font_css[xc.enlang]

    fanli.write_fanli(epub, xc)
    homage.write_homage(epub, xc, nikaya.homage_line)

    return epub


def write_notes(epub, nikaya, xc: book_public.XC):
    bns = [nikaya.abbr]
    _write_globalnotes(epub, bns, xc)
    first_note_doc_path = _write_localnotes(epub, nikaya.local_notes, bns, xc)
    epub.root_toc.append(epubpacker.Toc(xc.c("註解"), first_note_doc_path))
    return epub


def _write_localnotes(epub: epubpacker.Epub, notes: IndexedSet, bns, xc):
    docs = {}

    for note in notes:
        _doc_path = doepub.note_docname_calculate(page_parsing.LOCAL, notes.index(note))
        if _doc_path not in docs.keys():
            docs[_doc_path] = _make_note_doc(xc.c("註解一"), xc, _doc_path)

        _html, ol = docs[_doc_path]

        li = xl.sub(ol, "li", {"id": str(notes.index(note))})
        p = xl.sub(li, "p")
        p.kids.extend(dopdf.join_to_xml(note, bns=bns, c=xc.c, doc_path=_doc_path))

    for doc_path, (html, _ol) in docs.items():
        epub.userfiles[doc_path] = _doc_str(html)
        epub.spine.append(doc_path)

    return list(docs.keys())[0]


def _write_globalnotes(epub: epubpacker.Epub, bns, xc):
    notes = note_thing.get()
    docs = {}
    for key, note in notes.items():
        _doc_path = doepub.note_docname_calculate(page_parsing.GLOBAL, (key, "_x"))
        if _doc_path not in docs.keys():
            docs[_doc_path] = _make_note_doc(xc.c("註解二"), xc, _doc_path)
        _html, ol = docs[_doc_path]
        li = xl.sub(ol, "li", {"id": key})

        p = xl.sub(li, "p")
        es = []
        for subnote in note:
            es.extend(dopdf.join_to_xml(subnote, bns=bns, c=xc.c, doc_path=_doc_path))
            es.append(xl.Element("br"))
        p.kids.extend(es[:-1])

    for doc_path, (html, _ol) in docs.items():
        epub.userfiles[doc_path] = _doc_str(html)
        epub.spine.append(doc_path)


def _make_note_doc(title, xc: book_public.XC, doc_path):
    html, body = doepub.make_doc(doc_path, xc, title)
    body.attrs["class"] = "note"
    sec = xl.sub(body, "section", {"epub:type": "endnotes", "role": "doc-endnotes"})
    ol = xl.sub(sec, "ol")
    return html, ol


def _doc_str(e):
    return xl.Xl(root=xl.pretty_insert(e, dont_do_tags=["p"])).to_str()
