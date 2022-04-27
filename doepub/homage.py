import xl
import epubpacker
from pyabo import book_public
import dopdf
from . import epub_public


def write_homage(epub: epubpacker.Epub, xc: book_public.XC, line):
    doc_path = "homage.xhtml"
    html, body = epub_public.make_doc(doc_path, xc, "禮敬世尊")
    body.attrs["class"] = "homage"
    head = html.find_kids("head")[0]
    style = xl.Element("style", attrs={"type": "text/css"})
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
    head.kids.insert(0, style)

    outdiv = xl.sub(body, "div", {"class": "out"})
    indiv = xl.sub(outdiv, "div", {"class": "in homage"})
    span = xl.sub(indiv, "span")

    span.kids.extend(dopdf.join_to_xml(line, bns=[], c=xc.c, doc_path=doc_path))
    htmlstr = xl.Xml(root=html).to_str(do_pretty=True, dont_do_tags=["span"])
    epub.userfiles[doc_path] = htmlstr
    epub.spine.append(doc_path)
    epub.root_toc.append(epubpacker.Toc(xc.c("禮敬世尊"), doc_path))
