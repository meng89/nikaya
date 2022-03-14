#!/usr/bin/env python3
from epubpacker import Epub, Toc


def main():
    epub = Epub()
    epub.files["pages/hello.xhtml"] = b"<a>Hello, world</a>"
    chapter1_toc = Toc("chapter 1 Hello", "pages/hello.xhtml")
    chapter1_toc.kids.append(Toc("section 1 Hello world", "pages/hello.xhtml#section1"))
    epub.root_toc.append(chapter1_toc)
    epub.write("hello.epub")


main()
