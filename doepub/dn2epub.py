import xl
import epubpacker

from pyabo import nikayas, book_public, base_suttaref
import dopdf
import doepub

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
            html, body = doepub.make_doc(doc_path=doc_path, xc=xc, title=c(sutta.title))
            body.attrs["class"] = "sutta"

            if pin.suttas.index(sutta) == 0:
                _write_pin_title(body)
                pin_toc.href = doc_path + "#" + pin_id

            h2 = xl.sub(body, "h2", {"id": "{}".format(sutta_id)})
            _a = xl.sub(h2, "a", {"class": "title",
                                  "href": "{}".format(base_suttaref.SuttaRef(sutta_id).get_cccurl())})
            xl.sub(_a, "span", {"class": "sutta_id"}, [sutta_id])
            xl.sub(_a, "span", {"class": "space_in_sutta_title"}, [" "])
            xl.sub(_a, "span", kids=[c(sutta.title)])

            sutta_toc = epubpacker.Toc(sutta.serial + ". " + c(sutta.title), href=doc_path + "#" + sutta_id)
            pin_toc.kids.append(sutta_toc)

            for line in sutta.body_lines:
                p = xl.sub(body, "p")

                text = dopdf.join_to_text(line)
                if text != text.lstrip(text):
                    p.attrs["class"] = "ps_title"
                _x = dopdf.join_to_xml(line, bns=bns, c=c, doc_path=doc_path)
                p.kids.extend(_x)

            htmlstr = xl.Xl(root=xl.pretty_insert(html, dont_do_tags=["p", "a"])).to_str()

            epub.userfiles[doc_path] = htmlstr
            epub.spine.append(doc_path)


def make(xc: book_public.XC, temprootdir, books_dir, epubcheck):
    nikaya = nikayas.get("dn")
    epub_public.make(nikaya, write_suttas, xc, temprootdir, books_dir, epubcheck)
