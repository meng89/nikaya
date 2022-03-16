#!/usr/bin/env python3
from epubpacker import Epub, Toc
import uuid


def sample():
    epub = Epub()
    epub.meta.titles = ["Hello Book"]
    epub.meta.identifier = "identifier_" + uuid.uuid4().hex
    epub.meta.languages = ["zh-Hant", "pi"]
    epub.files["pages/hello.xhtml"] = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>Hello Book</title>
</head>
<body>
<a>Chapter 1 Hello</a><br/>
<a id="hello_word">Hello World!</a>
<a epub:type="noteref" href="#footnote_1">注1</a>
<a epub:type="noteref" href="#footnote_2">注2</a>
<a epub:type="noteref" href="#footnote_3">注3</a>
<section epub:type="footnotes">
  <aside epub:type="footnote" id="footnote_1">这是注释内容1</aside>
  <aside epub:type="footnote" id="footnote_2">这是注释内容2</aside>
  <aside epub:type="footnote" id="footnote_3">这是注释内容3</aside>
</section>
</body>
</html>
"""
    epub.spine.append("pages/hello.xhtml")
    chapter1_toc = Toc("chapter 1 Hello", "pages/hello.xhtml")
    chapter1_toc.kids.append(Toc("section 1 Hello world", "pages/hello.xhtml#hello_word"))
    epub.root_toc.append(chapter1_toc)
    epub.write("hello.epub")


sample()
