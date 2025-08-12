#!/usr/bin/env python3

import pyabo2.kn
import pyabo2.epub

import pyabo2.ebook_utils



def main():
    for lang in pyabo2.ebook_utils.TC(), pyabo2.ebook_utils.SC():
        for m in pyabo2.kn.all_modules:
            data = m.load_from_htm()
            epub = pyabo2.epub.make_epub(data, m, lang)


if __name__ == '__main__':
    main()
