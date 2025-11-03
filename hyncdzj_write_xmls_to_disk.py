#!/usr/bin/env python3

import types
import os


import config
import load_from_p5a


def write_to_disk(modules: [types.ModuleType, ...] = None):
    from book_module import sn
    from book_module import sv
    modules = modules or [sn, sv]

    for m in modules:
        book = load_from_p5a.load_book_by_module(m)
        book.write_for_machine(os.path.join(config.SIMPLE_DIR, m.info.name))


if __name__ == '__main__':
    write_to_disk()
