class Epub(object):
    def __init__(self):
        self.tocs = []
        self.root = None

    def write(self):
        if not self.root:
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
