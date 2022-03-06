#!/usr/bin/env python3

def a(a1, **kwargs):
    print("a1 in a:", a1)
    print("kwargw in a:", kwargs)
    b(**kwargs)


def b(a2, **kwargs):
    print("a2 in b:", a2)
    print("kwargw in b:", kwargs)


a(x=1,y=2,z=3,a2="a2",a1="a1")