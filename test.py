#!/usr/bin/env python3
import xl

xmlstr = """<?xml version="1.0" encoding="utf-8" standalone="no"?>
<student number="1001">
       <name>zhangSan</name>
       <age>23</age>
       <sex>male</sex>
</student>
<student number="1002">
       <name>liSi</name>
       <age>32</age>
       <sex>female</sex>
</student>"""


xl_ = xl.parse(xmlstr)
print(xl_.to_str())