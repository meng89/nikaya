#!/usr/bin/env python3
import re


class A(object):
    pass


class B(A):
    pass


if isinstance(B(), A):
    print("yes")