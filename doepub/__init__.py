import uuid


import epubpacker
import xl


import posixpath
from urllib.parse import urlsplit

from pyabo import page_parsing

from . import css, js


def relpath(path1, path2):
    """
     ("note/note0.xhtml", "sn/sn01.xhtml") -> "../note/note0.xhtml"
     ("sn/sn21.xhtml#SN.21.1, "sn/sn21.xhtml") -> "#SN.21.1"
    """

    path1_2 = posixpath.normpath(urlsplit(path1).path)
    fragment = urlsplit(path1).fragment

    path2_2 = posixpath.normpath(path2)

    if path1_2 == path2_2:
        if not fragment:
            raise ValueError("How to link to self without a tag id?")
        else:
            return "#" + fragment
    else:
        return posixpath.relpath(path1_2, posixpath.dirname(path2_2)) + (("#" + fragment) if fragment else "")


MAX_NUMBER_OF_NOTES_PER_PAGE = 50


def note_href_calculate(type_, key):
    return note_docname_calculate(type_, key) + "#" + noteid(type_, key)


def note_docname_calculate(type_, key):
    if type_ == page_parsing.GLOBAL:
        return "note/globalnote{}.xhtml".format(int(key[0]) // MAX_NUMBER_OF_NOTES_PER_PAGE)
    else:
        return "note/localnote{}.xhtml".format(key // MAX_NUMBER_OF_NOTES_PER_PAGE)


def noteid(type_, key):
    if type_ == page_parsing.GLOBAL:
        return str(key[0])
    else:
        return str(key)


def get_uuid(s):
    return uuid.uuid5(uuid.NAMESPACE_URL, "https://github.com/meng89/nikaya" + " " + s)


class DocpathCalcError(Exception):
    pass
