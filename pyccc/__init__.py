import os
import abc


CCC_WEBSITE = "https://agama.buddhason.org"


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

