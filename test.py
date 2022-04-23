#!/usr/bin/env python3

import xl

e = xl.Element("span", {"name": "value"}, ["sf\tfs \r\t\n"])

es = xl.Xl(root=e).to_str()
print(es)
print()
e2 = xl.parse(es, True, "\n\t")
root = e2.root
print(repr(e2.to_str()))


