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
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="zh-Hant" lang="zh-Hant">
<head>
<title>Hello Book</title>
</head>
<body>
<a>Chapter 1 Hello</a><br/>
<a id="hello_word">Hello World!</a>
<a epub:type="noteref" href="#footnote_1">注1</a><aside epub:type="footnote" id="footnote_1">this is note 1</aside><br/>
<a epub:type="noteref" href="#footnote_3">注3</a><br/>
<p>This is some body text with a footnote reference. <a class="noteref" epub:type="noteref" href="#note1">1</a></p>

asfljsflskjf

<aside class="footnote" epub:type="footnote" id="note1">1: This is a corresponding note</aside>
<br/>
aslfjsalfjslfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
lfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjlfkjsalfjdajjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj

  <aside epub:type="footnote" id="footnote_1">this is note 1</aside>
  <aside epub:type="footnote" id="footnote_2">这是注释内容2</aside>
  <aside epub:type="footnote" id="footnote_3">这是注释内容3</aside>
</body>
</html>
"""
    epub.spine.append("pages/hello.xhtml")
    chapter1_toc = Toc("chapter 1 Hello", "pages/hello.xhtml")
    chapter1_toc.kids.append(Toc("section 1 Hello world", "pages/hello.xhtml#hello_word"))
    epub.root_toc.append(chapter1_toc)
    epub.write("hello.epub")


sample()
