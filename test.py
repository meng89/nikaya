#!/usr/bin/env python3
import os.path

import base

import pyabo2.kn.it as it


try:
    import user_config as config
except ImportError:
    import config as config


data = it.load_from_htm()

base.write_to_disk(os.path.join(config.XML_DIR, it.short), data, True)