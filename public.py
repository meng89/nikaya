class Nikaya(object):
    def __init__(self):
        self.languages = ['zh-tw', 'pali']
        self.title_chinese = None
        self.title_pali = None

        self.abbreviation = None

        self.subs = []


class Node(object):
    def __init__(self):
        self.title = None
        self.serial = None

        self.sec_title = None

        self.subs = []


class Sutra(object):
    def __init__(self):
        self.title = None
        self.sec_title = None

        self.serial = None
        self.serial_start = None
        self.serial_end = None

        self.chinese = None
        self.main_lines = None
        self.pali = None

        self.sort_name = None

        self.modified = None

        self.abbreviation = None


class BaseInfo(object):
    def __init__(self):
        self.sutra_serial_start = None
        self.sutra_serial_end = None
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
