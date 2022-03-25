import xl
import epubpacker
from pyccc import book_public
import dopdf


def write_homage(epub: epubpacker.Epub, xc: book_public.XC, line):
    html = xl.Element("html", {"xmlns:epub": "http://www.idpf.org/2007/ops",
                               "xmlns": "http://www.w3.org/1999/xhtml",
                               "xml:lang": xc.xmlang,
                               "lang": xc.xmlang})
    head = xl.sub(html, "head")
    _title = xl.sub(head, "title", kids=[xc.c("禮敬世尊")])
    style = xl.sub(head, "style", attrs={"type": "text/css"})
    style.kids.append("""
.out {
    margin: 36vh 0 0 0;
    text-align: center;
}

.in {
    height: auto;
    font-size: 5vw;
    display: inline;
}"""
                      )
    body = xl.sub(html, "body")
    outdiv = xl.sub(body, "div", {"class": "out"})
    indiv = xl.sub(outdiv, "div", {"class": "in"})
    doc_path = "homage.xhtml"
    indiv.kids.extend(dopdf.join_to_xml(line, bns=[], c=xc.c, doc_path=doc_path))
    htmlstr = xl.Xl(root=xl.pretty_insert(html, dont_do_tags=["p"])).to_str()
    epub.userfiles[doc_path] = htmlstr
    epub.spine.append(doc_path)
    epub.root_toc.append(epubpacker.Toc(xc.c("禮敬世尊"), doc_path))
