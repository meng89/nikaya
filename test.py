#!/usr/bin/env python3

import re

def split_name(s):
    m = re.match(r"^\d+_(.+)$", s)
    return m.group(1)


print(split_name("123_sf s.xml"))

