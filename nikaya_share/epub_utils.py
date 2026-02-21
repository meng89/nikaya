#!/usr/bin/env python3


import posixpath
import pathlib


def make_safe_path(paths, path, width=3):
    if not paths:
        parts = list(pathlib.Path(path).parts)
        safe_path = []
        for part in parts:
            safe_path.append(str(1).zfill(3) + "_" + part)
        return posixpath.join(*safe_path)

    max_length, max_same_dirs = get_max_same_dirs(paths, path)

    same_head = list(pathlib.Path(max_same_dirs[0]).parts)
    safe_heads = same_head[0:max_length]

    parts = list(pathlib.Path(path).parts)

    change = parts[max_length]

    tail = parts[max_length + 1:]

    counts = []
    for path in max_same_dirs:
        _dir1 = list(pathlib.Path(path).parts)
        count = int(_dir1[max_length].split("_", maxsplit=1)[0])
        counts.append(count)

    count = 1
    while True:
        if count not in counts:
            break
        else:
            count += 1

    safe_change = str(count).zfill(3) + "_" + change

    safe_tail = []
    for x in tail:
        safe_tail.append(str(1).zfill(3) + "_" + x)

    safe = safe_heads + [safe_change] + safe_tail

    return posixpath.join(*safe)


def get_max_same_dirs(paths, path):
    same_dirs = []
    for x in paths:
        length = get_common_lenght(x, path)
        same_dirs.append((length, x))


    same_dirs2 = []
    max_length = max([x for x, y in same_dirs] + [0])
    for x, y in same_dirs:
        if x == max_length:
            same_dirs2.append(y)

    return max_length, same_dirs2


def get_common_lenght(path1, path2):
    _dir1 = list(pathlib.Path(path1).parts)[0:-1]
    dir1 = [p.split("_", maxsplit=1)[1] for p in _dir1]
    dir2 = list(pathlib.Path(path2).parts)[0:-1]
    common = get_common_prefix(dir1, dir2)
    return len(common)


def get_common_prefix(list1, list2):
    prefix = []
    # 使用 zip 遍历两个列表，直到较短的那个结束
    for item1, item2 in zip(list1, list2):
        if item1 == item2:
            prefix.append(item1)
        else:
            break
    return prefix


def main():
    keys = [
        "001_a/001_b/001_c.xhtml",
        "001_a/002_x/003_c.xhtml",

        "002_z/003_b"
    ]

    path = "a/b/c.xhtml/x/y/z"
    #path = "q"
    print(keys)
    print()

    print(make_safe_path(keys, path))


if __name__ == "__main__":
    main()
