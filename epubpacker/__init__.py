import posixpath
import zipfile
import datetime

import xl


# EPUB 不是我的坑，够用就行。仅为 Nikaya 服务
# EPUB 不是我的坑，够用就行。仅为 Nikaya 服务
# EPUB 不是我的坑，够用就行。仅为 Nikaya 服务


def _path2id(s):
    news = ""
    for c in s:
        if c == "_":
            news += "__"
        elif c == "/":
            news += "_s_"
        else:
            news += c
    return news


ROOT_OF_OPF = 'OEBPS'

USER_DIR = "user_dir"


class Epub(object):
    def __init__(self):
        self.cover_img_path = None
        self.meta = Meta()
        self.userfiles = {}
        self.toc_title = None
        self.root_toc = []
        self._spine = []

    @property
    def spine(self):
        return self._spine

    def write(self, filename):
        if not self.userfiles:
            raise EpubError

        z = zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_DEFLATED)
        z.writestr('mimetype', 'application/epub+zip'.encode('ascii'), compress_type=zipfile.ZIP_STORED)

########################################################################################################################
        nav_html = xl.Element("html", {"xmlns:epub": "http://www.idpf.org/2007/ops",
                                       "xmlns": "http://www.w3.org/1999/xhtml",
                                       "xml:lang": self.meta.languages[0]
                                       })
        head = xl.sub(nav_html, "head")
        title_text = self.toc_title or "Table of contents"
        _title = xl.sub(head, "title", kids=[title_text])
        body = xl.sub(nav_html, "body")
        nav = xl.sub(body, "nav", {"epub:type": "toc"})
        _h1 = xl.sub(nav, "h1", kids=[title_text])
        ol = xl.sub(nav, "ol")
        for toc in self.root_toc:
            toc.to_et(ol)

        name = "toc.xhtml"
        i = 1
        toc_xhtml = name
        while toc_xhtml in z.namelist():
            toc_xhtml = "real" + str(i) + name
            i += 1

        z.writestr(posixpath.join(ROOT_OF_OPF, toc_xhtml), xl.Xl(root=xl.pretty_insert(nav_html)).to_str())


########################################################################################################################

        dc_id_id = "ididid"
        _package = xl.Element("package", {"version": "3.0",
                                          "unique-identifier": dc_id_id,
                                          "xml:lang": self.meta.languages[0],
                                          "xmlns": "http://www.idpf.org/2007/opf"})

        self.meta.to_et(_package, dc_id_id)

        manifest = xl.sub(_package, "manifest")

        _toc_item = xl.sub(manifest, "item", {"media-type": "application/xhtml+xml",
                                              "href": toc_xhtml,
                                              "id": _path2id(toc_xhtml),
                                              "properties": "nav"
                                              })
        for filename in self.userfiles.keys():
            attrib = {}
            _, ext = posixpath.splitext(filename)
            if ext.lower() == ".xhtml":
                media_type = "application/xhtml+xml"

                xml = xl.parse(self.userfiles[filename])
                if xml.root.find_all("script"):
                    attrib["properties"] = "scripted"
            elif ext.lower() == ".css":
                media_type = "text/css"
            elif ext.lower() == ".js":
                media_type = "text/javascript"
            elif ext.lower() == ".png":
                media_type = "image/png"
            else:
                raise EpubError(ext)

            attrib.update(
                {"media-type": media_type,
                 "href": posixpath.join(USER_DIR, filename),
                 "id": _path2id(filename)
                 }
            )

            if filename == self.cover_img_path:
                if "properties" in attrib.keys():
                    attrib["properties"] = attrib["properties"] + " cover-image"
                else:
                    attrib["properties"] = "cover-image"

            _item = xl.sub(manifest, "item", attrib)

        spine = xl.sub(_package, "spine")
        for one in self.spine:
            xl.sub(spine, "itemref", {"idref": _path2id(one)})

        name = "package.opf"
        i = 1
        package_opf_path = posixpath.join(ROOT_OF_OPF, name)
        while package_opf_path in z.namelist():
            package_opf_path = "real" + str(i) + name
            i += 1

        z.writestr(package_opf_path, xl.Xl(root=xl.pretty_insert(_package)).to_str())


########################################################################################################################

        for filename, data in self.userfiles.items():
            z.writestr(posixpath.join(ROOT_OF_OPF, USER_DIR, filename), data)

########################################################################################################################

        _container = xl.Element("container", {"version": "1.0",
                                              "xmlns": "urn:oasis:names:tc:opendocument:xmlns:container"})
        _rootfiles = xl.sub(_container, "rootfiles")
        _rootfile = xl.sub(_rootfiles, "rootfile", {"media-type": "application/oebps-package+xml",
                                                    "full-path": posixpath.join(ROOT_OF_OPF, "package.opf")})
        z.writestr("META-INF/container.xml", xl.Xl(root=xl.pretty_insert(_container)).to_str())


class Meta(object):
    def __init__(self):
        self.identifier = ""
        self.titles = []
        self.languages = []
        self.creators = []
        self.date = ""
        self.others = []

    def to_et(self, parent, dc_id_id):
        metadata = xl.sub(parent, "metadata", {"xmlns:dc": "http://purl.org/dc/elements/1.1/"})
        _meta = xl.sub(metadata,
                       "meta",
                       {"property": "dcterms:modified"},
                       [datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")])
        if self.identifier:
            _dc_id = xl.sub(metadata, "dc:identifier", {"id": dc_id_id}, [self.identifier])
        for title in self.titles:
            _title = xl.sub(metadata, "dc:title", kids=[title])
        for lang in self.languages:
            _lang = xl.sub(metadata, "dc:language", kids=[lang])
        for creator in self.creators:
            _creator = xl.sub(metadata, "dc:creator", kids=[creator])
        if self.date:
            _date = xl.sub(metadata, "dc:date", kids=[self.date])

        for other in self.others:
            if not isinstance(other, xl.Element):
                raise TypeError(other)
            metadata.kids.append(other)


class Toc(object):
    def __init__(self, title, href=None):
        self.title = title
        self.href = href
        self.kids = []

    def to_et(self, parent):
        li = xl.sub(parent, "li")
        try:
            xl.sub(li, "a", {"href": posixpath.normpath(posixpath.join(USER_DIR, self.href))}, [self.title])
        except TypeError:
            raise TypeError(self.title, self.href)
        if self.kids:
            ol = xl.sub(li, "ol")
            for kid in self.kids:
                kid.to_et(ol)


class Vertebrae(object):
    def __init__(self, path):
        self.path = path


class EpubError(Exception):
    pass
