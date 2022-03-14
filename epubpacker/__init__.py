class Epub(object):
    def __init__(self):
        self.tocs = []
        self.root_dir = None
        self.files = {}

    def write(self, path):
        if not self.root_dir or not self.files:
            raise EpubError


class Toc(object):
    def __init__(self):
        self.title = None
        self.href = None
        self.kids = []


class _Spine(object):
    pass


class _Meta(object):
    pass


class EpubError(Exception):
    pass


def demo():
    epub = Epub()
    epub.files["pages/sn.1.1.xhtml"] = b"xxx"
