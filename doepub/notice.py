import epubpacker
from pyccc import book_public


_doc = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html
        PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-Hant" lang="zh-Hant">
<head>
    <title>说明</title>
</head>
<body>
<h1>说明</h1>
<p>此佛经来源于<a href="https://agama.buddhason.org">莊春江工作站</a>，一切相关权利归于译者。当前是2022年3月份，译者仍在订正经文中。
联系译者请前往译者网站留言。</p>
<p>电子书制作工具也在开发调整当中，请至制作程序项目主页阅读说明以获取制作好的电子书：
 <a href="https://github.com/meng89/nikaya">https://github.com/meng89/nikaya</a></p>
<p>如果打不开上面的链接，请尝试这个云盘链接：
 <a href="https://www.jianguoyun.com/p/DbVa44QQnbmtChiojLEE">https://www.jianguoyun.com/p/DbVa44QQnbmtChiojLEE</a></p>
<p>此电子书制作程序的相关问题请联系我：<a href="mailto:me@chenmeng.org">me@chenmeng.org</a></p>
</body>
</html>
"""


def write_notice(epub: epubpacker.Epub, xc: book_public.XC):
    doc_path = "notice.xhtml"
    epub.userfiles[doc_path] = _doc
    epub.spine.append(doc_path)
    epub.root_toc.append(epubpacker.Toc(xc.c("说明"), doc_path))
