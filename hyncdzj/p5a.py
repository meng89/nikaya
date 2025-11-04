#!/usr/bin/env python3

import os
import re

import config


def all_xmls(dir_=config.XMLP5A_DIR):
    xmls = []
    for one in os.listdir(dir_, ):
        path = os.path.join(dir_, one)
        if os.path.isfile(path) and one.lower().endswith(".xml"):
            xmls.append(path)
        elif os.path.isdir(path):
            xmls.extend(all_xmls(path))

    return sorted(xmls)


def n_xmls():
    xmls = []
    for x in all_xmls():
        if "/N/" in x:
            xmls.append(x)
    return xmls

def get_xmls_by_serial(juan):
    xmls = []
    for xml in n_xmls():
        m = re.match(r"^.*?(\d+)\.xml$", xml)
        if int(m.group(1)) == juan:
            xmls.append(xml)
    return xmls



if __name__ == "__main__":
    print(get_xmls_by_serial(6))

