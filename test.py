#!/usr/bin/env python3

from hyncdzj_write_ebooks import total

import hyncdzj_write_ebooks
def main():
    hyncdzj_write_ebooks.total += 1
    nonlocal total
    total += 1

    print(total)

if __name__ == "__main__":
    main()


