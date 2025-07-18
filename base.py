#KISS
#KISS
#KISS

import os
import re

import xl


def _split(name):
    return re.match(r"^(\d+)_(.+)$", name)


def split_serial(name):
    return _split(name).group(1)


def split_name(name):
    return _split(name).group(2)


class Folder:
    def __init__(self, path=None):
        self.conts = {}
        if path:
            entries = os.listdir(path)
            entries.sort(key=split_serial)

            for entry in entries:
                entry_path = os.path.join(path, entry)

                if os.path.isdir(entry_path):
                    name = split_name(entry)
                    value = Folder(entry_path)

                elif os.path.isfile(entry_path):
                    name = os.path.basename(entry_path)
                    value = Doc(entry_path)
                else:
                    raise Exception("Unknow File: {}".format(entry_path))

                self.conts[name] = value

    def write(self, path):
        os.makedirs(path, exist_ok=True)
        index = 1
        for name, obj in self.conts.items():
            obj.write(os.path.join(path, "{}_{}".format(index, name)))


class Doc:
    def __init__(self, path=None):
        if path:
            xml = xl.parse(open(path, "r").read())
            root = xml.root
            self._meta = root.find_kids("meta")[0]
            self._body = root.find_kids("body")[0]
        else:
            self._meta = xl.Element("meta")
            self._body = xl.Element("body")


    def write(self, path):
        root = xl.Element("doc")
        root.kids.extend([self._meta, self._body])
        xml = xl.Xml(root)
        with open(path, "w") as f:
            f.write(xml.to_str(new_line_after_kid=True, do_pretty=True, dont_do_tags=["body"], try_self_closing=True))


def load(path) -> dict:
    data = {}
    entries = os.listdir(path)
    entries.sort(key=split_serial)
    for entry in entries:
        entry_path = os.path.join(path, entry)

        if os.path.isdir(entry_path):
            name = split_name(entry)
            value = load(entry_path)

        elif os.path.isfile(entry_path):
            name = os.path.basename(entry_path)
            value = xl.parse(open(entry_path, "r").read())
        else:
            raise Exception("Unknow File: {}".format(entry_path))
        data[name] = value

    return data



def write(path, data):
    for k, v in data.items():

        if isinstance(v, dict):
            write(os.path.join(path, k), v)