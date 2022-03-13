#!/usr/bin/env python3

class Base(object):
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'text={self.text!r})')

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return repr(self) == repr(other)
        else:
            return False

    def __hash__(self):
        return hash(repr(self))


class A(Base):
    pass



b1 = A("hehe")
b2 = A("hehe")

print(b1 == b2)
print(A)
s = set()

s.add((b1,))
s.add((b2,))
print(s)
