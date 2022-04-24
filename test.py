#!/usr/bin/env python3

import xl

e = xl.Element("span", {"name": "value"}, ["ss"])
xl.sub(e, "span2", {"class": "sutta"}, ["ss3"])

print(e.to_str2(do_pretty=True))

