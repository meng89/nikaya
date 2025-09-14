#!/usr/bin/env python3

import os

import config
from pyabo2 import sn, mn, dn, an
import pyabo2.kn
import base

import pyabo2.kn.su

def main():
    #for module in [pyabo2.kn.su]:
    for module in [sn, mn, dn, an] + list(pyabo2.kn.all_modules):
        try:
            load_from_htm = getattr(module, "load_from_htm")
        except AttributeError:
            pass
        else:
            data = load_from_htm()
            base.write_to_disk(os.path.join(config.XML_DIR, module.short), data, True)

if __name__ == "__main__":
    main()
