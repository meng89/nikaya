import xl

import pyccc.pdf
from pyccc import sn


def write_suttas(epub, bns, c, test=False):
    nikaya = sn.get()
    html = xl.Element("x")
    head = xl.Element("x")
    body = xl.Element("x")

    def make_html():
        nonlocal html, head, body
        html = xl.Element("html", {"xmlns": "http://www.w3.org/1999/xhtml",
                                   "xml:lang": "zh-Hant",
                                   "lang": "zh-Hant"})
        head = xl.sub(html, "head")
        body = xl.sub(html, "body")

    make_html()

    for pian in nikaya.pians:
        xl.sub(body, "h1", kids=[c(pian.title)])

        for xiangying in pian.xiangyings:
            _xy_title = c(xiangying.serial + ". " + xiangying.title)
            head.kids.append(xl.Element("title", kids=[_xy_title]))
            xl.sub(body, "h2", kids=[_xy_title])

            for pin in xiangying.pins:
                if pin.title is not None:
                    xl.sub(body, "h3", {"id": "sn1pin1"}, kids=[c(pin.title)])

                for sutta in pin.suttas:
                    xl.sub(body, "h4", kids=[c(sutta.title)])
                    for body_listline in sutta.body_lines:
                        p = xl.sub(body, "p")
                        p.kids.extend(pyccc.pdf.join_to_xml(body_listline, bns=bns, c=c))

            htmlstr = xl.Xl(doc_type=xl.DocType(doc_type_name="html",
                                                system_id="-//W3C//DTD XHTML 1.0 Transitional//EN",
                                                public_id="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"),
                            root=html).to_str()

            epub.files["sn/SN.{}.xhtml".format(xiangying.serial)] = htmlstr
            make_html()


