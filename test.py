#!/usr/bin/env python3
import re


P_SN = r"(SN)\.(\d+\.\d+)"
P_AN = r"(AN)\.(\d+\.\d+)"


string = "[text1 SN.1.1, AN.2.1 text2]"

def parse(s: str):
    # [some text SN.1.1, AN.2.1 some text] ->
    # [some text <a href="xxx.xhtml#SN.1.1">SN.1.1</a>, <a href="https://AN.2.1">AN.2.1</a> some text]

    list_s = []
    offset = 0
    for m in re.finditer("|".join([P_SN, P_AN]), s):
        print(m.string)
        (begin, end) = m.span()
        list_s.append(s[offset:begin])
        list_s.append("X>"+s[begin:end])
        offset = end
    if offset < len(s):
        list_s.append(s[offset:])

    return list_s

print(parse(string))