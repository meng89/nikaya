#!/usr/bin/env python3

import xl

e = xl.Element("span", {"sf": """ a"'b """}, ["sffs"])

es = xl.Xl(root=e).to_str()
print(es)
e2 = xl.parse(es)
print(e2.to_str())

print(e2.root.attrs)
