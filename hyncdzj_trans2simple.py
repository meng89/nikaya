#!/usr/bin/env python3
import os

import config
from hyncdzj import base
import hyncdzj_load_from_p5a
import hyncdzj_book_module


def main():
    for category, ms in hyncdzj_book_module.categories:
        for m in ms:
            name, data = hyncdzj_load_from_p5a.load_book_by_module(m)
            data_dir = os.path.join(config.SIMPLE_DOC_DIR, m.info.name)
            os.makedirs(data_dir, exist_ok=True)
            print(data_dir)
            base.write_to_disk(data_dir, data)


def print_data(data):
    if isinstance(data, list):
        for name, sub in data:
            print(name)
            print_data(sub)
    else:
        print(data.to_str())


if __name__ == '__main__':
    main()
