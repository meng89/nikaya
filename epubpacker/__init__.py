import zipfile


ROOT_OF_OPF = 'EPUB'


class Epub(object):
    def __init__(self):
        self.meta = Meta()
        self.files = {}
        self.root_toc = []
        self.spine = []

    def write(self, path):
        if not self.files:
            raise EpubError

        z = zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED)
        z.writestr('mimetype', 'application/epub+zip'.encode('ascii'), compress_type=zipfile.ZIP_STORED)
        for filename, data in self.files.items():
            z.writestr(ROOT_OF_OPF + "/" + filename, data)


class Meta(object):
    def __init__(self):
        self.title = None


class Toc(object):
    def __init__(self, title, href):
        self.title = title
        self.href = href
        self.kids = []


class Vertebrae(object):
    def __init__(self, path):
        self.path = path


class EpubError(Exception):
    pass


