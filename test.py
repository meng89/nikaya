#!/usr/bin/env python3
#from epubpacker import Epub, Toc

import zipfile

def main():
    epub = Epub()
    epub.files["pages/hello.xhtml"] = b"""
<a>HELLO</a><br/>
<a name="hello_word">Hello, world</a><br/>
"""
    epub.spine.append("pages/hello.xhtml")
    chapter1_toc = Toc("chapter 1 Hello", "pages/hello.xhtml")
    chapter1_toc.kids.append(Toc("section 1 Hello world", "pages/hello.xhtml#hello_word"))
    epub.root_toc.append(chapter1_toc)
    epub.write("hello.epub")



z = zipfile.ZipFile("x", "w")
z.writestr("a/b.txt", "hello")
z.writestr("a/c.txt", "hello2")
z.is
