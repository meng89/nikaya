import math


class Notes:
    def __init__(self):
        self.note_name = "註解"
        self._notes = []
        self._filename = "note"

    @property
    def notes(self):
        return self._notes

    @staticmethod
    def _get_page_index(note_id):
        return math.ceil(int(note_id + 1) / 100)

    def _get_page_path(self, note_id):
        return "note/{}{}.xhtml".format(self._filename, self._get_page_index(note_id))

    def add_note(self, es: list):
        length = len(self._notes)
        self._notes.append(es)
        return self._get_page_path(length) + "#{}".format(length)

    def get_pages(self, lang):
        from . import epub
        xhtmls = []
        last_page_path = None
        last_ol = None

        last_html = None

        for index, note in enumerate(self.notes):
            _path = self._get_page_path(index)
            if _path != last_page_path:
                last_page_path = _path
                title = self.note_name+"第{}页".format(self._get_page_index(index))
                html, body = epub.make_doc(last_page_path, lang, title)
                body.attrs["class"] = "note"
                #last_html = html
                h1 = body.ekid("h1")
                h1.kids.append(title)
                section = body.ekid("section")
                section.attrs["epub:type"] = "endnotes"
                section.attrs["role"] = "doc-endnotes"
                ol = section.ekid("ol")
                last_html = html
                last_ol = ol
                xhtmls.append((title, last_page_path, last_html))

            li = last_ol.ekid("li")
            li.attrs["id"] = str(index)
            #p = li.ekid("p")
            li.kids.extend(epub.xml_es_to_html(note, last_html, self, last_page_path, lang))

        pages = []
        for title, path, xhtml in xhtmls:
            pages.append((title, path, xhtml.to_str(do_pretty=True)))

        return pages
