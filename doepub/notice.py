import epubpacker
import xl

from . import epub_public
from pyabo import book_public


_project_link = "https://github.com/meng89/nikaya"
_yunpan_link = "https://www.jianguoyun.com/p/DbVa44QQnbmtChiojLEE"
_my_mail = "me@chenmeng.org"


_lines = (
    ("此汉译佛经数据来源于", xl.Element("a", {"href": "https://agama.buddhason.org"}, ["莊春江工作站"]),
     "，一切相关权利归于译者。联系译者请前往译者网站留言。"),
    ("电子书制作工具也在开发调整当中，请至制作程序项目主页阅读说明以获取制作好的电子书：",
     xl.Element("a", {"href": "{}".format(_project_link)}, [_project_link])),
    ("如果打不开上面的链接，请尝试这个云盘链接：", xl.Element("a", {"href": "{}".format(_yunpan_link)}, [_yunpan_link])),
    ("有此电子书制作程序的相关问题请联系我：", xl.Element("a", {"href": "mailto:{}".format(_my_mail)}, [_my_mail]))
)


def write_notice(epub: epubpacker.Epub, xc: book_public.XC):
    doc_path = "notice.xhtml"
    html, body = epub_public.make_doc(doc_path, xc, "说明")

    body.attrs["class"] = "notice"

    _h1 = xl.sub(body, "h1", {"class": "title"}, ["说明"])
    for line in _lines:
        _p = xl.sub(body, "p", kids=line)

    htmlstr = xl.Xml(root=html).to_str(do_pretty=True, dont_do_tags=["p"])
    epub.userfiles[doc_path] = htmlstr
    epub.spine.append(doc_path)
    epub.root_toc.append(epubpacker.Toc(xc.c("说明"), doc_path))
