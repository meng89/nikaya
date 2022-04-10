import re

import xl
import epubpacker

from pyabo import nikayas, book_public, base_suttaref
import dopdf

from . import epub_public


def write_suttas(nikaya, epub: epubpacker.Epub, bns, xc, _test=False):
    c = xc.c
    for pin in nikaya.pins:
        pin_id = "pin"

        def _write_pin_title(_body):
            xl.sub(_body, "h1", {"class": "title", "id": pin_id}, [c(pin.title)])

        pin_toc = epubpacker.Toc(
            c(pin.title) + "({}~{})".format(pin.suttas[0].serial, pin.suttas[-1].serial))

        epub.root_toc.append(pin_toc)

        for sutta in pin.suttas:
            sutta_id = "DN.{}".format(sutta.serial)
            doc_path = base_suttaref.docpath_calculate(sutta_id)
            html, body = epub_public.make_doc(doc_path=doc_path, xc=xc, title=c(sutta.title))
            body.attrs["class"] = "sutta"

            if pin.suttas.index(sutta) == 0:
                _write_pin_title(body)
                pin_toc.href = doc_path + "#" + pin_id

            title_e = xl.sub(body, "h2", {"class": "title", "id": "{}".format(sutta_id)})

            _a = xl.sub(title_e, "a", {"href": "{}".format(base_suttaref.SuttaRef(sutta_id).get_cccurl())})
            _a.kids.append(sutta_id)
            title_e.kids.append(" ")
            xl.sub(title_e, "span", {"class": "sutta_id"}, kids=[c(sutta.title)])
            if sutta.agama_part is not None:
                title_e.kids.append(" ")
                xl.sub(title_e, "span", {"class": "agama_part"},
                       kids=dopdf.join_to_xml([sutta.agama_part], bns, c, doc_path, tag_unicode_range=False))

            sutta_toc = epubpacker.Toc(sutta.serial + ". " + c(sutta.title), href=doc_path + "#" + sutta_id)
            pin_toc.kids.append(sutta_toc)

            write_bodylines(nikaya, sutta, sutta.body_lines, body, bns, c, doc_path)

            htmlstr = xl.Xl(root=xl.pretty_insert(html, dont_do_tags=["p", "a", "h2"])).to_str()

            epub.userfiles[doc_path] = htmlstr
            epub.spine.append(doc_path)


def write_bodylines(_nikaya, _sutta, body_lines, body, bns, c, doc_path):
    for line in body_lines:
        if len(line) == 0:
            xl.sub(body, "br")
            continue

        p = xl.sub(body, "p")
        tag_unicode_range = True

        text = dopdf.join_to_text(line)
        if text == text.lstrip():

            p.attrs["class"] = "subtitle"
            tag_unicode_range = False

        if isinstance(line[-1], str):
            # DN.22 (375) 中多余一个换行符，所以不能用 .* 匹配
            m = re.match(r"^([\s\S]*)(\(\d+\))$", line[-1])
            if m:
                line = line[:-1]
                line.append(m.group(1))
                line.append(xl.Element("span", {"class": "tail_number"}, [m.group(2)]))

        _x = dopdf.join_to_xml(line, bns=bns, c=c, doc_path=doc_path, tag_unicode_range=tag_unicode_range)
        p.kids.extend(_x)


def make(xc: book_public.XC, temprootdir, books_dir, epubcheck):
    nikaya = nikayas.get("dn")
    epub_public.make(nikaya, write_suttas, xc, temprootdir, books_dir, epubcheck)
