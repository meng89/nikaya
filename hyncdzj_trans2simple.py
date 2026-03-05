#!/usr/bin/env python3
import os

import config
import hyncdzj_load_from_p5a
from  hyncdzj import book_modules
import share


def main():
    for m in book_modules.all_modules:
        data_dir = os.path.join(config.HYNCDZJ_SIMPLE_XML_DIR, m.info.name)
        print(data_dir)
        name, data = hyncdzj_load_from_p5a.load_book_by_module(m)
        os.makedirs(data_dir, exist_ok=True)
        share.write_to_disk(data_dir, data)
        print()


def print_data(data):
    if isinstance(data, list):
        for name, sub in data:
            print(name)
            print_data(sub)
    else:
        print(data.to_str())


if __name__ == '__main__':
    main()
