import re


import xl
import epubpacker


from pyabo import nikayas, book_public, base_suttaref
import dopdf

from . import epub_public, DocpathCalcError


def hit_docpath_and_id(suttaid):
    m = re.match(r"AN\.(\d+)\.(\d+)", suttaid)
    if not m:
        raise DocpathCalcError("不能识别的 Sutta ID: " + repr(suttaid))
    ji_serial = m.group(1)
    sutta_serial = m.group(2)
    nikaya = nikayas.get("an")

    for ji in nikaya.jis:
        if ji.serial == ji_serial:
            for pin in ji.pins:
                for sutta in pin.suttas:
                    if int(sutta.begin) <= int(sutta_serial) <= int(sutta.end):
                        return ("an/AN.{}.{}-{}.xhtml".format(ji_serial, sutta.begin, sutta.end),
                                "AN.{}.{}".format(ji_serial, sutta.begin))

    raise DocpathCalcError("找不到 Sutta ID: " + repr(suttaid))


def write_suttas(nikaya, epub: epubpacker.Epub, bns, xc, _test=False):
    c = xc.c

    docs = {}
    for ji in nikaya.jis:
        ji_id = "ji"
        ji_title = "第{}集".format(ji.serial)

        def _write_ji_title(_body):
            xl.sub(_body, "h1", {"class": "title", "id": ji_id}, [ji_title])

        ji_toc = epubpacker.Toc(ji_title)

        epub.root_toc.append(ji_toc)

        for pin in ji.pins:
            pin_id = "pin"

            def _write_pin_title(_body):
                xl.sub(_body, "h2", {"class": "title", "id": pin_id}, [c(pin.title)])

            pin_toc = epubpacker.Toc(
                "{}. {}({}~{})".format(pin.serial, pin.title, pin.suttas[0].begin, pin.suttas[-1].end))
            ji_toc.kids.append(pin_toc)

            for sutta in pin.suttas:
                sutta_id = "AN.{}.{}".format(ji.serial, sutta.begin)
                doc_path = hit_docpath_and_id(sutta_id)[0]
                try:
                    html, body = docs[doc_path]
                except KeyError:
                    html, body = epub_public.make_doc(doc_path=doc_path, xc=xc, title=c(pin.title))
                    docs[doc_path] = (html, body)

                body.attrs["class"] = "sutta"

                if pin.suttas.index(sutta) == 0:
                    if ji.pins.index(pin) == 0:
                        _write_ji_title(body)
                        ji_toc.href = doc_path + "#" + ji_id
                    _write_pin_title(body)
                    pin_toc.href = doc_path + "#" + pin_id

                title_e = xl.sub(body, "h3", {"class": "title", "id": "{}".format(sutta_id)})
                _a = xl.sub(title_e, "a", {"href": "{}".format(base_suttaref.SuttaRef(sutta_id).get_cccurl())})

                if sutta.begin == sutta.end:
                    title_sutta_id = sutta_id
                else:
                    title_sutta_id = "{}~{}".format(sutta_id, sutta.end)

                if sutta.begin == sutta.end:
                    sutta_serial = sutta.begin
                else:
                    sutta_serial = "{}~{}".format(sutta.begin, sutta.end)

                if sutta.title:
                    sutta_title = sutta.title
                    sutta_toc_title = sutta_serial + ". " + c(sutta.title)
                else:
                    sutta_title = ""
                    sutta_toc_title = sutta_serial + c(" 經")

                xl.sub(title_e, "span", {"class": "sutta_id"}, [title_sutta_id])
                title_e.kids.append(" ")
                xl.sub(title_e, "span", kids=[c(sutta_title)])
                if sutta.agama_part:
                    title_e.kids.append(" ")
                    xl.sub(title_e, "span", {"class": "agama_part"},
                           kids=dopdf.join_to_xml([sutta.agama_part], bns, c, doc_path, tag_unicode_range=False))

                sutta_toc = epubpacker.Toc(sutta_toc_title, href=doc_path + "#" + sutta_id)
                pin_toc.kids.append(sutta_toc)

                for line in sutta.body_lines:
                    p = xl.sub(body, "p")
                    _x = dopdf.join_to_xml(line, bns=bns, c=c, doc_path=doc_path)
                    p.kids.extend(_x)

    for doc_path, (html, _) in docs.items():
        htmlstr = xl.Xl(root=xl.pretty_insert(html, dont_do_tags=["p", "a"])).to_str()
        epub.userfiles[doc_path] = htmlstr
        epub.spine.append(doc_path)


def make(xc: book_public.XC, temprootdir, books_dir, epubcheck):
    nikaya = nikayas.get("an")
    epub_public.make(nikaya, write_suttas, xc, temprootdir, books_dir, epubcheck)
