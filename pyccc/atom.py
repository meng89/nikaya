from urllib.parse import urljoin

import pyccc.pdf

from pyccc import atom_note


class Href(object):
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

    def to_tex(self, t):
        url = urljoin(pyccc.CCC_WEBSITE, urljoin(self.base_url_path, self.href))
        return "\\ccchref{" + t(self.text) + "}{" + pyccc.pdf.el_url(url) + "}"


class TextWithNoteRef(object):
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

    def to_tex(self, t):
        return "\\twnr" +\
               "{" + t(self.get_text()) + "}" + \
               "{" + atom_note.note_label(self.type_, self.key) + "}"

    def get_text(self):
        return self.text

    def get_type(self):
        return self.type_

    def get_number(self):
        return self.key
