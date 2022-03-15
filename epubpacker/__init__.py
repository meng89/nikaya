import os.path
import zipfile
import xml.etree.ElementTree as ET
import uuid


# XML 不是我的坑，够用就行。仅为 Nikaya 服务
# XML 不是我的坑，够用就行。仅为 Nikaya 服务
# XML 不是我的坑，够用就行。仅为 Nikaya 服务


ROOT_OF_OPF = 'EPUB'


class Epub(object):
    def __init__(self):
        self.meta = Meta()
        self.files = {}
        self.toc_title = None
        self.root_toc = []
        self.spine = []

    def write(self, package_opf_path):
        if not self.files:
            raise EpubError

        z = zipfile.ZipFile(package_opf_path, 'w', compression=zipfile.ZIP_DEFLATED)
        z.writestr('mimetype', 'application/epub+zip'.encode('ascii'), compress_type=zipfile.ZIP_STORED)
        for filename, data in self.files.items():
            z.writestr(ROOT_OF_OPF + "/" + filename, data)

########################################################################################################################

        nav_html = ET.Element("html")
        ET.SubElement(ET.SubElement(nav_html, "head"), "title").text = self.toc_title
        body = ET.SubElement(nav_html, "body")
        nav = ET.SubElement(body, "nav", {"epub:type": "toc"})
        ol = ET.SubElement(nav, "ol")
        for toc in self.root_toc:
            toc.to_et(ol)

        ET.tostring(nav_html)

########################################################################################################################

        dc_id_id = uuid.uuid4().hex
        _package = ET.Element("package", {"version": "3.0",
                                          "unique-identifier": dc_id_id,
                                          "xml:lang": self.meta.languages[0],
                                          "xmlns": "http://www.idpf.org/2007/opf"})
        self.meta.to_et(_package, dc_id_id)

        manifest = ET.SubElement(_package, "manifest")

        for filename in self.files.keys():
            _, ext = os.path.splitext(filename)
            if ext.lower() == "xhtml":
                media_type = "application/xhtml+xml"
            elif ext.lower() == "css":
                media_type = "text/css"
            elif ext.lower() == "js":
                media_type = "text/javascript"
            else:
                raise EpubError

            _item = ET.SubElement(manifest, "item", {"media-type": media_type,
                                                     "href": filename,
                                                     "id": filename,
                                                     "properties": "scripted"})
        spine = ET.SubElement(_package, "spine")
        for one in self.spine:
            ET.SubElement(spine, "itemref", {"idref": one})

        d = "EPUB"
        name = "package.opf"
        i = 1
        package_opf_path = d + "/" + name
        while package_opf_path in z.namelist():
            package_opf_path = "real" + str(i) + name

        z.writestr(package_opf_path, ET.tostring(_package, encoding="utf8", method="xml"))
########################################################################################################################

        _container = ET.Element("container", {"version": "1.0",
                                              "xmlns": "urn:oasis:names:tc:opendocument:xmlns:container"})
        _rootfiles = ET.SubElement(_container, "rootfiles")
        _rootfile = ET.SubElement(_rootfiles, "rootfile", {"media-type": "application/oebps-package+xml",
                                                           "full-package_opf_path": "EPUB/package.opf"})
        z.writestr("META-INF/container.xml", ET.tostring(_container, encoding="utf8", method="xml")


class Meta(object):
    def __init__(self):
        self.identifier = ""
        self.titles = []
        self.languages = []

    def to_et(self, parent, dc_id_id):
        metadata = ET.SubElement(parent, "metadata", {"xmlns:dc": "http://purl.org/dc/elements/1.1/"})
        if self.identifier:
            dc_id = ET.SubElement(metadata, "dc:identifier", {"id": dc_id_id})
            dc_id.text = self.identifier
        for title in self.titles:
            _title = ET.SubElement(metadata, "dc:title")
            _title.text = title
        for lang in self.languages:
            _lang = ET.SubElement(metadata, "dc:language")
            _lang.text = lang


class Toc(object):
    def __init__(self, title, href):
        self.title = title
        self.href = href
        self.kids = []

    def to_et(self, parent):
        li = ET.SubElement(parent, "li")
        ET.SubElement(li, "a", {"href": self.href})
        if self.kids:
            ol = ET.SubElement(li, "ol")
            for kid in self.kids:
                kid.to_et(ol)




class Vertebrae(object):
    def __init__(self, path):
        self.path = path


class EpubError(Exception):
    pass
