import re


import xl
import epubpacker


from pyabo import nikayas, book_public, base_suttaref
import dopdf
import doepub
from . import DocpathCalcError
from . import epub_public


def hit_docpath_and_id(suttaid):
    m = re.match(r"SN\.(\d+)\.(\d+)", suttaid)
    if not m:
        raise DocpathCalcError("不能识别的 Sutta ID: " + repr(suttaid))
    xy_serial = m.group(1)
    sutta_serial = m.group(2)
    nikaya = nikayas.get("sn")

    for pian in nikaya.pians:
        for xy in pian.xiangyings:
            if xy.serial == xy_serial:
                for pin in xy.pins:
                    for sutta in pin.suttas:
                        if int(sutta.begin) <= int(sutta_serial) <= int(sutta.end):
                            return ("sn/SN.{}.xhtml".format(xy_serial),
                                    "SN.{}.{}".format(xy_serial, sutta.begin))

    raise DocpathCalcError("找不到 Sutta ID: " + repr(suttaid))


def write_suttas(nikaya, epub: epubpacker.Epub, bns, xc, _test=False):
    c = xc.c
    for pian in nikaya.pians:
        pian_id = "pian{}".format(nikaya.pians.index(pian))

        def _write_pian_part(_body):
            xl.sub(_body, "h1", {"class": "title", "id": pian_id}, [c(pian.title)])
            nonlocal pian_toc

        pian_toc = epubpacker.Toc(
            c(pian.title) + "({}~{})".format(pian.xiangyings[0].serial, pian.xiangyings[-1].serial))
        epub.root_toc.append(pian_toc)

        for xiangying in pian.xiangyings:
            xy_id = "sn"
            doc_path = hit_docpath_and_id("SN.{}.1".format(xiangying.serial))[0]
            _xy_title = xiangying.serial + ". " + c(xiangying.title)
            html, body = doepub.make_doc(doc_path=doc_path, xc=xc, title=_xy_title)
            body.attrs["class"] = "sutta"

            if pian.xiangyings.index(xiangying) == 0:
                _write_pian_part(body)
                pian_toc.href = doc_path + "#" + xy_id

            xl.sub(body, "h2", {"class": "title", "id": xy_id}, kids=[_xy_title])
            xy_toc = epubpacker.Toc(_xy_title, doc_path + "#" + xy_id)
            pian_toc.kids.append(xy_toc)

            for pin in xiangying.pins:
                if pin.title is not None:
                    pin_id = "pin{}".format(xiangying.pins.index(pin))
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

                    if sutta.title:
                        sutta_toc_title = sutta_num + ". " + c(sutta.title)
                    else:
                        sutta_toc_title = sutta_num + c(" 經")

                    sutta_id = "SN.{}.{}".format(xiangying.serial, sutta.begin)
                    
                    title_sutta_id = "SN.{}.{}".format(xiangying.serial, sutta_num)

                    sutta_safe_title = sutta.title or ""

                    h4 = xl.sub(body, "h4", {"class": "title",
                                             "id": "{}".format(sutta_id)})
                    title_e = h4
                    _a = xl.sub(h4, "a", {"class": "sutta_id",
                                          "href": "{}".format(base_suttaref.SuttaRef(sutta_id).get_cccurl())},
                                kids=[title_sutta_id])
                    title_e.kids.append(" ")
                    xl.sub(title_e, "span", {"class": "xiangying_title"}, [c(xiangying.title)])
                    title_e.kids.append("/")
                    xl.sub(title_e, "span", kids=[c(sutta_safe_title)])
                    if sutta.agama_part is not None:
                        title_e.kids.append(" ")
                        xl.sub(title_e, "span", {"class": "agama_part"},
                               kids=dopdf.join_to_xml([sutta.agama_part], bns, c, doc_path, tag_unicode_range=False))

                    sutta_toc = epubpacker.Toc(sutta_toc_title, href=doc_path + "#" + sutta_id)
                    sutta_father_toc.kids.append(sutta_toc)

                    for body_listline in sutta.body_lines:
                        p = xl.sub(body, "p")
                        _x = dopdf.join_to_xml(body_listline, bns=bns, c=c, doc_path=doc_path)
                        p.kids.extend(_x)

            htmlstr = xl.Xl(root=xl.pretty_insert(html, dont_do_tags=["p", "a", "h4"])).to_str()

            epub.userfiles[doc_path] = htmlstr
            epub.spine.append(doc_path)


def make(xc: book_public.XC, temprootdir, books_dir, epubcheck):
    nikaya = nikayas.get("sn")
    epub_public.make(nikaya, write_suttas, xc, temprootdir, books_dir, epubcheck)
