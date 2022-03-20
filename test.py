#!/usr/bin/env python3

from compiler.ast import flatten

a = [1, 2, 3, 4, 5, 6]
b = ['a', 'b', 'c', 'd', 'e']

c = flatten(zip(a, b))

print(c)


