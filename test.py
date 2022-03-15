#!/usr/bin/env python3
from epubpacker import Epub, Toc
import uuid


def sample():
    epub = Epub()
    epub.meta.titles = ["Hello Book"]
    epub.meta.identifier = "identifier_" + uuid.uuid4().hex
    epub.meta.languages = ["zh-Hant", "pi"]
    epub.files["pages/hello.xhtml"] = b"""
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>Hello Book</head>
  <body>
    <a>HELLO</a><br/>
    <a name="hello_word">Hello, world</a><br/>
  </body>
</html>
"""
    epub.spine.append("pages/hello.xhtml")
    chapter1_toc = Toc("chapter 1 Hello", "pages/hello.xhtml")
    chapter1_toc.kids.append(Toc("section 1 Hello world", "pages/hello.xhtml#hello_word"))
    epub.root_toc.append(chapter1_toc)
    epub.write("hello.epub")


sample()

