from boltons.setutils import IndexedSet


class Nikaya(object):
    def __init__(self):
        self.languages = ['zh-tw', 'pali']
        self.title_st = None
        self.title_pali = None

        self.abbreviation = None

        self.homage_listline = None
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

        # self.chinese = None
        self.body_listline_list = None
        self.pali = None

        self.local_note_list = None

        self.sort_name = None

        self.last_modified = None

        self.abbreviation = None


class BaseInfo(object):
    def __init__(self):
        self.sutta_begin = None
        self.sutta_end = None
        self.sutra_title = None

        self.modified = None


class PinInfo(object):
    def __init__(self):
        self.pin_serial = None
        self.pin_title = None


class PianInfo(object):
    def __init__(self):
        self.pian_serial = None
        self.pian_title = None
