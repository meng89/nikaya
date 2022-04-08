import os
import datetime
import shutil
import subprocess

from boltons.setutils import IndexedSet

import xl
import epubpacker

from pyabo import nikayas, sn, book_public, page_parsing, base_suttaref, note_thing
import dopdf
import doepub
from . import fanli, homage, notice
from .css import public, public_path, font_path, font_css


def write_suttas(nikaya, epub: epubpacker.Epub, bns, xc, _test=False):
    c = xc.c
    for pian in nikaya.pians:

        def _write_pian_part(_body):
            pian_id = "pian"
            xl.sub(_body, "h1", {"class": "title", "id": pian_id}, [c(pian.title)])
            nonlocal pian_toc

        pian_toc = epubpacker.Toc(
            c(pian.title) + "({}~{})".format(pian.xiangyings[0].serial, pian.xiangyings[-1].serial))
        epub.root_toc.append(pian_toc)

        for index in range(len(pian.xiangyings)):
            xiangying = pian.xiangyings[index]
            xy_id = "sn"
            doc_path = base_suttaref.docpath_calculate("SN.{}.1".format(xiangying.serial))
            # html, head, body = _make_sutta_doc(xc, doc_path)

            _xy_title = c(xiangying.serial + ". " + xiangying.title)
            html, body = doepub.make_doc(doc_path=doc_path, xc=xc, title=_xy_title)
            body.attrs["class"] = "sutta"

            if index == 0:
                _write_pian_part(body)
                pian_toc.href = doc_path + "#" + xy_id

            # head.kids.append(xl.Element("title", kids=[_xy_title]))

            xl.sub(body, "h2", {"class": "title", "id": xy_id}, kids=[_xy_title])
            xy_toc = epubpacker.Toc(_xy_title, doc_path + "#" + xy_id)
            pian_toc.kids.append(xy_toc)

            for pin in xiangying.pins:
                if pin.title is not None:
                    pin_id = "pin" + pin.serial
                    xl.sub(body, "h3", {"class": "title", "id": pin_id}, kids=[c(pin.title)])
                    pin_toc = epubpacker.Toc(c(pin.title + "({}~{})".format(pin.suttas[0].begin,
                                                                            pin.suttas[-1].end)),
                                             href=doc_path + "#" + pin_id)
                    xy_toc.kids.append(pin_toc)
                    sutta_father_toc = pin_toc
                else:
                    sutta_father_toc = xy_toc

                for sutta in pin.suttas:
                    if sutta.begin == sutta.end:
                        sutta_num = sutta.begin
                    else:
                        sutta_num = "{}~{}".format(sutta.begin, sutta.end)

                    sutta_id = "SN.{}.{}".format(xiangying.serial, sutta.begin)
                    sutta_safe_title = sutta.title or ""

                    # SN.1.1 诸天相应/暴流之渡過經

                    h4 = xl.sub(body, "h4", {"id": "{}".format(sutta_id)})
                    _a = xl.sub(h4, "a", {"class": "title",
                                          "href": "{}".format(base_suttaref.SuttaRef(sutta_id).get_cccurl())})
                    xl.sub(_a, "span", {"class": "sutta_id"}, [sutta_id])
                    xl.sub(_a, "span", {"class": "space_in_sutta_title"}, [" "])
                    xl.sub(_a, "span", {"class": "xy_name_in_sutta_title"}, [c(xiangying.title)])
                    xl.sub(_a, "span", {"class": "slash_in_sutta_title"}, ["/"])
                    xl.sub(_a, "span", kids=[c(sutta_safe_title)])
                    xl.sub(h4, "span", {"class": "agama_part"},
                           kids=dopdf.join_to_xml([sutta.agama_part], bns, c, doc_path))

                    if sutta.title:
                        sutta_toc_title = sutta_num + ". " + c(sutta.title)
                    else:
                        sutta_toc_title = sutta_num
                    sutta_toc = epubpacker.Toc(sutta_toc_title, href=doc_path + "#" + sutta_id)
                    sutta_father_toc.kids.append(sutta_toc)

                    for body_listline in sutta.body_lines:
                        p = xl.sub(body, "p")
                        _x = dopdf.join_to_xml(body_listline, bns=bns, c=c, doc_path=doc_path)
                        p.kids.extend(_x)

            htmlstr = xl.Xl(root=xl.pretty_insert(html, dont_do_tags=["p", "a", "h4"])).to_str()

            epub.userfiles[doc_path] = htmlstr
            epub.spine.append(doc_path)


def _make_note_doc(title, xc: book_public.XC, doc_path):
    html, body = doepub.make_doc(doc_path, xc, title)
    body.attrs["class"] = "note"
    sec = xl.sub(body, "section", {"epub:type": "endnotes", "role": "doc-endnotes"})
    ol = xl.sub(sec, "ol")
    return html, ol


def _doc_str(e):
    return xl.Xl(root=xl.pretty_insert(e, dont_do_tags=["p"])).to_str()


def write_localnotes(epub: epubpacker.Epub, notes: IndexedSet, bns, xc):
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


def write_globalnotes(epub: epubpacker.Epub, bns, xc):
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


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    return which(name) is not None


def check_epub(epub_path, epubcheck, mytemprootdir):
    compile_cmd = "java -jar {} {} -q".format(epubcheck, epub_path)

    stdout_file = open(os.path.join(mytemprootdir, "cmd_stdout"), "w")
    stderr_file = open(os.path.join(mytemprootdir, "cmd_stderr"), "w")

    def _run():
        print("运行:", compile_cmd, end=" ", flush=True)
        p = subprocess.Popen(compile_cmd, cwd=mytemprootdir, shell=True,
                             stdout=stdout_file, stderr=stderr_file)
        p.communicate()
        if p.returncode != 0:
            return False
        return True

    if not _run():
        print("出错！")
        return
    else:
        print("成功！")


def make(xc: book_public.XC, temprootdir, books_dir, epubcheck):
    bns = [sn.BN]

    mytemprootdir = os.path.join(temprootdir, "sn_epub_" + xc.enlang)
    os.makedirs(mytemprootdir, exist_ok=True)

    nikaya = nikayas.get("sn")

    epub = epubpacker.Epub()
    doepub.write_epub_cssjs(epub)

    epub.meta.titles = [xc.c("相應部")]
    epub.meta.creators = ["莊春江({})".format(xc.c("譯"))]
    epub.meta.date = nikaya.last_modified.strftime("%Y-%m-%dT%H:%M:%SZ")
    epub.meta.languages = [xc.xmlang, "pi", "en-US"]

    my_uuid = doepub.get_uuid(xc.c("相應部") + xc.enlang)
    epub.meta.identifier = my_uuid.urn

    epub.meta.others.append(xl.Element("meta", {"property": "belongs-to-collection", "id": "c01"},
                                       ["莊春江" + xc.c("漢譯經藏")]))
    epub.meta.others.append(xl.Element("meta", {"refines": "#c01", "property": "collection-type"}, ["series"]))

    epub.userfiles[public_path] = public
    epub.userfiles[font_path[xc.enlang]] = font_css[xc.enlang]

    fanli.write_fanli(epub, xc)
    homage.write_homage(epub, xc, nikaya.homage_line)

    write_suttas(nikaya, epub, bns, xc)
    first_note_doc_path = write_localnotes(epub, nikaya.local_notes, bns, xc)
    write_globalnotes(epub, bns, xc)
    epub.root_toc.append(epubpacker.Toc(xc.c("註解"), first_note_doc_path))

    notice.write_notice(epub, xc)

    epub_path = os.path.join(mytemprootdir, "sn.epub")
    epub.write(epub_path)

    if is_tool("java") and os.path.exists(epubcheck):
        check_epub(epub_path=epub_path, epubcheck=epubcheck, mytemprootdir=mytemprootdir)

    shutil.copy(epub_path,
                os.path.join(books_dir, "{}_{}_{}{}_{}.epub".format(xc.c("相應部"),
                                                                    xc.zhlang,
                                                                    "莊",
                                                                    nikaya.last_modified.strftime("%y%m"),
                                                                    datetime.datetime.now().strftime("%Y%m%d"))))
