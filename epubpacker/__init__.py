import os.path
import zipfile
import xml.etree.ElementTree as ET
from xml.dom import minidom
import uuid


# XML 和 EPUB 不是我的坑，够用就行。仅为 Nikaya 服务
# XML 和 EPUB 不是我的坑，够用就行。仅为 Nikaya 服务
# XML 和 EPUB 不是我的坑，够用就行。仅为 Nikaya 服务


def _prettxml(s):
    return minidom.parseString(s).toprettyxml(indent="   ")


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

########################################################################################################################

        nav_html = ET.Element("html", {"xmlns:epub": "http://www.idpf.org/2007/ops",
                                       "xmlns": "http://www.w3.org/1999/xhtml"})
        ET.SubElement(ET.SubElement(nav_html, "head"), "title").text = self.toc_title
        body = ET.SubElement(nav_html, "body")
        nav = ET.SubElement(body, "nav", {"epub:type": "toc"})
        ol = ET.SubElement(nav, "ol")
        for toc in self.root_toc:
            toc.to_et(ol)

        name = "toc.xhtml"
        i = 1
        toc_xhtml = ROOT_OF_OPF + "/" + name
        while toc_xhtml in z.namelist():
            toc_xhtml = "real" + str(i) + name
            i += 1

        self.files[toc_xhtml] = _prettxml(ET.tostring(nav_html, encoding="utf8", method="xml"))


########################################################################################################################

        dc_id_id = "id"
        _package = ET.Element("package", {"version": "3.0",
                                          "unique-identifier": dc_id_id,
                                          "xml:lang": self.meta.languages[0],
                                          "xmlns": "http://www.idpf.org/2007/opf"})
        self.meta.to_et(_package, dc_id_id)

        meta = ET.SubElement(_package, "meta", {"property": "dcterms:modified"})
        meta.text = ""

        manifest = ET.SubElement(_package, "manifest")

        for filename in self.files.keys():
            _, ext = os.path.splitext(filename)
            if ext.lower() == ".xhtml":
                media_type = "application/xhtml+xml"
            elif ext.lower() == ".css":
                media_type = "text/css"
            elif ext.lower() == ".js":
                media_type = "text/javascript"
            else:
                raise EpubError(ext)

            attrib = {"media-type": media_type,
                      "href": filename,
                      "id": filename
                      }
            if filename == toc_xhtml:
                attrib["properties"] = "nav"
            _item = ET.SubElement(manifest, "item", attrib)

        spine = ET.SubElement(_package, "spine")
        for one in self.spine:
            ET.SubElement(spine, "itemref", {"idref": one})

        name = "package.opf"
        i = 1
        package_opf_path = ROOT_OF_OPF + "/" + name
        while package_opf_path in z.namelist():
            package_opf_path = "real" + str(i) + name
            i += 1

        z.writestr(package_opf_path, _prettxml(ET.tostring(_package, encoding="utf8", method="xml")))


########################################################################################################################

        for filename, data in self.files.items():
            z.writestr(ROOT_OF_OPF + "/" + filename, data)

        self.files.pop(toc_xhtml)

########################################################################################################################

        _container = ET.Element("container", {"version": "1.0",
                                              "xmlns": "urn:oasis:names:tc:opendocument:xmlns:container"})
        _rootfiles = ET.SubElement(_container, "rootfiles")
        _rootfile = ET.SubElement(_rootfiles, "rootfile", {"media-type": "application/oebps-package+xml",
                                                           "full-path": "EPUB/package.opf"})
        z.writestr("META-INF/container.xml", _prettxml(ET.tostring(_container, encoding="utf8", method="xml")))


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
