#!/usr/bin/env python3
import os

import config


import pyabo2.ebook


import pyabo2.kn
for m in pyabo2.kn.all_modules:
    if not hasattr(m, "load_from_htm"):
        continue
    data = m.load_from_htm()
    for lang in (pyabo2.ebook.SC(), pyabo2.ebook.TC()):
        pyabo2.ebook.make_cover(module=m,data=data,lang=lang)