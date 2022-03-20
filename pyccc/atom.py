from urllib.parse import urljoin

import pyccc.epub
import xl


import pyccc.pdf

from pyccc import atom_note


class Href(pyccc.BaseElement):
    def __init__(self, text, href, base_url_path, target):
        self.text = text
        self.href = href
        self.base_url_path = base_url_path
        self.target = target

    def get_text(self):
        return self.text

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'text={self.text!r}, '
                f'href={self.href!r}, '
                f'base={self.base_url_path!r}, '
                f'target={self.target!r})')

    def _url(self):
        return urljoin(pyccc.CCC_WEBSITE, urljoin(self.base_url_path, self.href))

    def to_tex(self, c, **kwargs):
        return "\\ccchref{" + c(self.text) + "}{" + pyccc.pdf.el_url(self._url()) + "}"

    def to_xml(self, c, **kwargs):
        return xl.Element("a", {"href": self._url()}, [c(self.text)])


class TextWithNoteRef(pyccc.BaseElement):
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
               "{" + atom_note.note_to_texlabel(self.type_, self.key) + "}"

    def to_xml(self, c, doc_path, **kwargs):
        href = pyccc.epub.note_href_calculate(self.type_, self.key)
        return xl.Element("a", {"epub:type": "noteref", "href": pyccc.epub.relpath(href, doc_path)}, [self.text])

    def get_text(self):
        return self.text

    def get_type(self):
        return self.type_

    def get_number(self):
        return self.key
