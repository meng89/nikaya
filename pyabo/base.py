from urllib.parse import urljoin

import xl


import pyabo
from pyabo import note_thing
import dopdf
import doepub
import doepub.basestr


class Href(pyabo.BaseElement):
    def __init__(self, text, href, base_url_path):
        self.text = text
        self.href = href
        self.base_url_path = base_url_path

    def get_text(self):
        return self.text

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'text={self.text!r}, '
                f'href={self.href!r}, '
                f'base={self.base_url_path!r})')

    def _url(self):
        return urljoin(pyabo.ABO_WEBSITE, urljoin(self.base_url_path, self.href))

    def to_tex(self, c, **kwargs):
        return "\\ccchref{" + c(self.text) + "}{" + dopdf.el_url(self._url()) + "}"

    def to_es(self, c, tag_unicode_range, **kwargs):
        return [xl.Element("a", {"href": self._url()}, doepub.basestr.str2es(c(self.text), tag_unicode_range))]


class TextWithNoteRef(pyabo.BaseElement):
    """<a onmouseover="note(this,1);">像這樣被我聽聞</a>"""

    def __init__(self, text, type_, key):
        self.text = text
        self.type_ = type_
        self.key = key

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'text={self.text!r}, '
                f'type_={self.type_!r}, '
                f'number={self.key!r})')

    def to_tex(self, c, **kwargs):
        return "\\twnr" +\
               "{" + c(self.get_text()) + "}" + \
               "{" + note_thing.note_to_texlabel(self.type_, self.key) + "}"

    def to_es(self, c, doc_path, tag_unicode_range, **kwargs):
        href = doepub.note_href_calculate(self.type_, self.key)
        return [xl.Element("a",
                           {"epub:type": "noteref",
                                 "href": doepub.relpath(href, doc_path),
                                 "class": "noteref"},
                           doepub.basestr.str2es(c(self.text), tag_unicode_range))]

    def get_text(self):
        return self.text

    def get_type(self):
        return self.type_

    def get_number(self):
        return self.key
