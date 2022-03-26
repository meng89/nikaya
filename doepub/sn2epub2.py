import os
import datetime
import shutil

from boltons.setutils import IndexedSet

import xl
import epubpacker

from pyccc import sn, book_public, page_parsing, atom_suttaref, atom_note
import dopdf
import doepub
from . import fanli, homage, notice

css = """
p{margin: 0.3em;}
"""

css_path = "_static/sutta.css"


def _make_doc(xc: book_public.XC, doc_path):
    html = xl.Element("html", {"xmlns:epub": "http://www.idpf.org/2007/ops",
                               "xmlns": "http://www.w3.org/1999/xhtml",
                               "xml:lang": xc.xmlang,
                               "lang": xc.xmlang})
    head = xl.sub(html, "head")
    _link = xl.sub(head, "link", {"rel": "stylesheet", "type": "text/css", "href": doepub.relpath(css_path, doc_path)})
    body = xl.sub(html, "body")
    return html, head, body


def write_suttas(epub: epubpacker.Epub, bns, xc, _test=False):
    c = xc.c
    nikaya = sn.get()
    for pian in nikaya.pians:

        pian_toc = epubpacker.Toc(
            c(pian.title) + "({}~{})".format(pian.xiangyings[0].serial, pian.xiangyings[-1].serial))
        epub.root_toc.append(pian_toc)

        for index in range(len(pian.xiangyings)):
            xiangying = pian.xiangyings[index]
            xy_id = "sn"
            doc_path = atom_suttaref.docpath_calculate("SN.{}.1".format(xiangying.serial))
            html, head, body = _make_doc(xc, doc_path)
            pian_id = "pian"
            pian_sec = xl.sub(body, "section", {"epub:type": "part", "id": pian_id})
            h1 = xl.sub(pian_sec, "h1", kids=[c(pian.title)])
            if index == 0:
                pian_toc.href = doc_path + "#" + xy_id
            else:
                h1.attrs["style"] = "display: none;"

            _xy_title = xiangying.serial + ". " + c(xiangying.title)
            head.kids.append(xl.Element("title", kids=[_xy_title]))
            xy_sec = xl.sub(pian_sec, "section", {"epub:type": "chapter", "id": xy_id}, )
            _h2 = xl.sub(xy_sec, "h2", {"id": xy_id}, kids=[_xy_title])
            xy_toc = epubpacker.Toc(_xy_title, doc_path + "#" + xy_id)
            pian_toc.kids.append(xy_toc)

            for pin in xiangying.pins:
                if pin.title is not None:
                    pin_id = "pin" + pin.serial
                    xl.sub(xy_sec, "h3", {"id": pin_id}, kids=[c(pin.title)])
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
                    xl.sub(xy_sec, "h4", {"id": sutta_id}, [sutta_num + ". " + c(sutta.title)])
                    sutta_toc = epubpacker.Toc(sutta_num + ". " + c(sutta.title), href=doc_path + "#" + sutta_id)
                    sutta_father_toc.kids.append(sutta_toc)

                    for body_listline in sutta.body_lines:
                        p = xl.sub(xy_sec, "p")
                        _x = dopdf.join_to_xml(body_listline, bns=bns, c=c, doc_path=doc_path)
                        p.kids.extend(_x)

            htmlstr = xl.Xl(root=xl.pretty_insert(html, dont_do_tags=["p"])).to_str()

            epub.userfiles[doc_path] = htmlstr
            epub.spine.append(doc_path)


def _make_note_doc(title, xc: book_public.XC):
    html = xl.Element("html", {"xmlns:epub": "http://www.idpf.org/2007/ops",
                               "xmlns": "http://www.w3.org/1999/xhtml",
                               "xml:lang": xc.xmlang,
                               "lang": xc.xmlang})
    head = xl.sub(html, "head")
    _title = xl.sub(head, "title", kids=[title])
    style = xl.sub(head, "style", {"type": "text/css"})
    style.kids.append("""
     /* section {font-size: small;} */
     ol {list-style:none;}
    """)
    body = xl.sub(html, "body")

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
            docs[_doc_path] = _make_note_doc(xc.c("註解一"), xc)

        _html, ol = docs[_doc_path]

        li = xl.sub(ol, "li", {"id": str(notes.index(note))})
        p = xl.sub(li, "p")
        p.kids.extend(dopdf.join_to_xml(note, bns=bns, c=xc.c, doc_path=_doc_path))

    for doc_path, (html, _ol) in docs.items():
        epub.userfiles[doc_path] = _doc_str(html)
        epub.spine.append(doc_path)

    return list(docs.keys())[0]


def write_globalnotes(epub: epubpacker.Epub, bns, xc):
    notes = atom_note.get()
    docs = {}
    for key, note in notes.items():
        _doc_path = doepub.note_docname_calculate(page_parsing.GLOBAL, (key, "_x"))
        if _doc_path not in docs.keys():
            docs[_doc_path] = _make_note_doc(xc.c("註解二"), xc)
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


def make(xc: book_public.XC, temprootdir, books_dir):
    bns = [sn.BN]

    mytemprootdir = os.path.join(temprootdir, "sn_epub_" + xc.enlang)
    os.makedirs(mytemprootdir, exist_ok=True)

    sn_data = sn.get()

    epub = epubpacker.Epub()
    epub.meta.titles = [xc.c("相應部")]
    epub.meta.creators = ["莊春江({})".format(xc.c("譯"))]
    epub.meta.date = sn_data.last_modified.strftime("%Y-%m-%dT%H:%M:%SZ")
    epub.meta.languages = [xc.xmlang, "pi", "en-US"]

    my_uuid = doepub.get_uuid(xc.c("相應部") + xc.enlang)
    epub.meta.identifier = my_uuid.urn

    epub.userfiles[css_path] = css

    fanli.write_fanli(epub, xc)
    homage.write_homage(epub, xc, sn_data.homage_listline)

    write_suttas(epub, bns, xc)
    first_note_doc_path = write_localnotes(epub, sn_data.local_notes, bns, xc)
    write_globalnotes(epub, bns, xc)
    epub.root_toc.append(epubpacker.Toc(xc.c("註解"), first_note_doc_path))

    notice.write_notice(epub, xc)

    epub_path = os.path.join(mytemprootdir, "sn.epub")
    epub.write(epub_path)

    shutil.copy(epub_path,
                os.path.join(books_dir, "{}_{}_{}{}_{}.epub".format(xc.c("相應部"),
                                                                    xc.zhlang,
                                                                    "莊",
                                                                    sn_data.last_modified.strftime("%y%m"),
                                                                    datetime.datetime.now().strftime("%Y%m%d"))))