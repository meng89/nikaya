import xl
import epubpacker
from pyccc import book_public
import dopdf

_lines = ("此佛经来源于莊春江工作站，一切相关权利归于译者。当前是2022年3月份，仍在订正经文中。",

          "电纸书制作工具也在开发调整当中，请用此链接获取最新的电子书："
          "https://github.com/meng89/nikaya/tree/dev/books",

          "如果打不开上面的链接，请尝试下面的云盘链接："
          "https://www.jianguoyun.com/p/DbVa44QQnbmtChiojLEE",
          )


def write_homage(epub: epubpacker.Epub, xc: book_public.XC):
    doc_path = "notice.xhtml"
    html = xl.Element("html", {"xmlns:epub": "http://www.idpf.org/2007/ops",
                               "xmls": "http://www.w3.org/1999/xhtml",
                               "xml:lang": xc.xmlang,
                               "lang": xc.xmlang})
    head = xl.sub(html, "head")
    _title = xl.sub(head, "title", kids=[xc.c("制作说明")])

    body = xl.sub(html, "body")
    _h1 = xl.sub(body, "h1", kids=["电子书制作说明"])
    for line in _lines:
        body.kids.append(xl.Element("p", kids=[line]))

    htmlstr = xl.Xl(root=xl.pretty_insert(html, dont_do_tags=["p"])).to_str()
    epub.userfiles[doc_path] = htmlstr
    epub.spine.append(doc_path)
    epub.root_toc.append(epubpacker.Toc(xc.c("制作说明"), doc_path))
