#!/usr/bin/env python3

import os

import config
import pyabo2.kn
import base


def main():
    for module in pyabo2.kn.all_modules:
        try:
            load_from_htm = getattr(module, "load_from_htm")
        except AttributeError:
            pass
        else:
            data = load_from_htm()
            base.write_to_disk(os.path.join(config.XML_DIR, module.short), data, True)


def main2():
    import pyabo2.kn.su as m
    data = m.load_from_htm()
    base.write_to_disk(os.path.join(config.XML_DIR, m.short), data, True)


if __name__ == "__main__":
    main2()

