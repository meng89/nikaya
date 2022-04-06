from boltons.setutils import IndexedSet


class Nikaya(object):
    def __init__(self):
        self.languages = ['zh-tw', 'pali']
        self.title_zh = None
        self.title_pali = None
        self.abbr = None

        self.homage_line = None
        self.last_modified = None
        self.local_notes = IndexedSet()
        self.subs = []


class Node(object):
    def __init__(self):
        self.title = None
        self.serial = None

        self.sec_title = None

        self.subs = []


class Sutta(object):
    def __init__(self):
        self.title = None
        self.sec_title = None

        self.serial = None
        self.begin = None
        self.end = None

        self.body_lines = None
        self.pali = None

        self.sort_name = None

        self.last_modified = None

        self.abbreviation = None


class BaseInfo(object):
    def __init__(self):
        self.sutta_begin = None  # for SN
        self.sutta_end = None  # for SN
        self.sutta_title = None

        self.sutta_serial = None  # for MN
        self.modified = None


class PinInfo(object):
    def __init__(self):
        self.pin_serial = None
        self.pin_title = None


class PianInfo(object):
    def __init__(self):
        self.pian_serial = None
        self.pian_title = None
