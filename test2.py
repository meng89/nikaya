#!/usr/bin/env python3

import xl


def main():
    html = xl.Element("html")
    body = xl.sub(html, "body", kids=["aaa", "bbb"])
    body.kids.append(xl.Element("a", {"href": "https://www.google.com"}, ["Google"]))
    print(html.to_str())
    print()
    print(xl.Xl(root=xl.pretty_insert(html)).to_str())


main()
