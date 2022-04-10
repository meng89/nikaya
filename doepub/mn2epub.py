import xl
import epubpacker

from pyabo import nikayas, book_public, base_suttaref
import dopdf
import doepub

from . import epub_public, dn2epub


def write_suttas(nikaya, epub: epubpacker.Epub, bns, xc, _test=False):
    c = xc.c
    for pian in nikaya.pians:
        pian_id = "pian"

        def _write_pian_title(_body):
            xl.sub(_body, "h1", {"class": "title", "id": pian_id}, [c(pian.title)])

        pian_toc = epubpacker.Toc(
            c(pian.title) + "({}~{})".format(pian.pins[0].suttas[0].serial, pian.pins[-1].suttas[-1].serial))
        epub.root_toc.append(pian_toc)

        for pin in pian.pins:
            pin_id = "pin"

            def _write_pin_title(_body):
                xl.sub(_body, "h2", {"class": "title", "id": pin_id}, [c(pin.title)])

            pin_toc = epubpacker.Toc(
                c(pin.title) + "({}~{})".format(pin.suttas[0].serial, pin.suttas[-1].serial))
            pian_toc.kids.append(pin_toc)

            for sutta in pin.suttas:
                sutta_id = "MN.{}".format(sutta.serial)
                doc_path = base_suttaref.docpath_calculate(sutta_id)
                html, body = doepub.make_doc(doc_path=doc_path, xc=xc, title=c(sutta.title))
                body.attrs["class"] = "sutta"

                if pin.suttas.index(sutta) == 0:
                    if pian.pins.index(pin) == 0:
                        # 同时也是篇中第一品， 要添加篇 title
                        _write_pian_title(body)
                        pian_toc.href = doc_path + "#" + pian_id
                    # 品中第一经， 至少要添加品 title
                    _write_pin_title(body)
                    pin_toc.href = doc_path + "#" + pin_id

                title_e = xl.sub(body, "h3", {"class": "title", "id": "{}".format(sutta_id)})
                _a = xl.sub(title_e, "a", {"href": "{}".format(base_suttaref.SuttaRef(sutta_id).get_cccurl())})
                _a.kids.append(sutta_id)
                title_e.kids.append(" ")
                xl.sub(title_e, "span", kids=[c(sutta.title)])
                if sutta.agama_part is not None:
                    title_e.kids.append(" ")
                    xl.sub(title_e, "span", {"class": "agama_part"},
                           kids=dopdf.join_to_xml([sutta.agama_part], bns, c, doc_path, tag_unicode_range=False))

                sutta_toc = epubpacker.Toc(sutta.serial + ". " + c(sutta.title), href=doc_path + "#" + sutta_id)
                pin_toc.kids.append(sutta_toc)

                dn2epub.write_bodylines(nikaya, sutta, sutta.body_lines, body, bns, c, doc_path)

                htmlstr = xl.Xl(root=xl.pretty_insert(html, dont_do_tags=["p", "a", "h3"])).to_str()

                epub.userfiles[doc_path] = htmlstr
                epub.spine.append(doc_path)


def make(xc: book_public.XC, temprootdir, books_dir, epubcheck):
    nikaya = nikayas.get("mn")
    epub_public.make(nikaya, write_suttas, xc, temprootdir, books_dir, epubcheck)
