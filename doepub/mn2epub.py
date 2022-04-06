import xl
import epubpacker

from pyabo import nikayas, book_public, base_suttaref
import dopdf
import doepub

from . import epub_public


def write_suttas(nikaya, epub: epubpacker.Epub, bns, xc, _test=False):
    c = xc.c
    for pian in nikaya.pians:

        def _write_pian_part(_body):
            pian_id = "pian"
            xl.sub(_body, "h1", {"class": "title", "id": pian_id}, [c(pian.title)])
            nonlocal pian_toc

        pian_toc = epubpacker.Toc(
            c(pian.title) + "({}~{})".format(pian.pins[0].suttas[0].serial, pian.pins[-1].sutta[-1].serial))
        epub.root_toc.append(pian_toc)

        for index in range(len(pian.pins)):
            xiangying = pian.pins[index]
            xy_id = "mn"
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

                    # SN.1.1 诸天相应/暴流之渡過經

                    h4 = xl.sub(body, "h4", {"id": "{}".format(sutta_id)})
                    _a = xl.sub(h4, "a", {"class": "title",
                                          "href": "{}".format(base_suttaref.SuttaRef(sutta_id).get_cccurl())})
                    xl.sub(_a, "span", {"class": "sutta_id"}, [sutta_id])
                    xl.sub(_a, "span", {"class": "space_in_sutta_title"}, [" "])
                    xl.sub(_a, "span", {"class": "xy_name_in_sutta_title"}, [c(xiangying.title)])
                    xl.sub(_a, "span", {"class": "slash_in_sutta_title"}, ["/"])
                    xl.sub(_a, "span", kids=[c(sutta.title)])

                    # xl.sub(body, "h4", {"id": sutta_id}, [sutta_num + ". " + c(sutta.title)])
                    sutta_toc = epubpacker.Toc(sutta_num + ". " + c(sutta.title), href=doc_path + "#" + sutta_id)
                    sutta_father_toc.kids.append(sutta_toc)

                    for body_listline in sutta.body_lines:
                        p = xl.sub(body, "p")
                        _x = dopdf.join_to_xml(body_listline, bns=bns, c=c, doc_path=doc_path)
                        p.kids.extend(_x)

            htmlstr = xl.Xl(root=xl.pretty_insert(html, dont_do_tags=["p", "a"])).to_str()

            epub.userfiles[doc_path] = htmlstr
            epub.spine.append(doc_path)


def make(xc: book_public.XC, temprootdir, books_dir, epubcheck):
    nikaya = nikayas.get("mn")

    epub_public.make(nikaya, write_suttas, xc, temprootdir, books_dir, epubcheck)
