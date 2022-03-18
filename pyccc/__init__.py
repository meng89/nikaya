import os
import abc


CCC_WEBSITE = "https://agama.buddhason.org"

TEX_DIR = PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tex")

assert os.path.isdir(TEX_DIR)


class BaseElement(object):
    @abc.abstractmethod
    def get_text(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def __repr__(self):
        pass

    @abc.abstractmethod
    def to_tex(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def to_xml(self, *args, **kwargs):
        pass

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return repr(self) == repr(other)
        else:
            return False

    def __hash__(self):
        return hash(repr(self))

