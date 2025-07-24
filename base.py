#KISS
#KISS
#KISS

import os
import re
import shutil

import xl


def _split(name):
    return re.match(r"^(\d+)_(.+?)(\.xml)?$", name)


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


class Doc2:
    def __init__(self, path=None):
        if path:
            s = open(path, "w").read()
            xml = xl.parse(s)
            self._doc = xml.root
        else:
            doc = xl.Element("doc")
            meta = doc.ekid("meta")
            translator = meta.ekid("translator")
            translator.kids.append("莊春江")
            doc.ekid("body")
            doc.ekid("notes")
            self._doc = doc

    def  _get_meta_element(self, tag):
        meta = self._doc.find_kids("meta")[0]
        es = meta.find_kids(tag)
        if es:
            return es[0]
        else:
            e = meta.ekid(tag)
            return e

    def _get_meta_sub(self, tag):
        e  = self._get_meta_element(tag)
        if e.kids:
            return e.kids[0]
        return None

    def _set_meta_sub(self, tag, value):
        e = self._get_meta_element(tag)
        if value is None:
            e.kids = []
        else:
            e.kids = [value]

    @property
    def mtime(self) -> str or None:
        return self._get_meta_sub("mtime")
    @mtime.setter
    def mtime(self, value: str):
        self._set_meta_sub("mtime", value)

    @property
    def start(self) -> str or None:
        return self._get_meta_sub("start")
    @start.setter
    def start(self, value: str):
        self._set_meta_sub("start", value)

    @property
    def end(self) -> str or None:
        return self._get_meta_sub("end")
    @end.setter
    def end(self, value: str):
        self._set_meta_sub("end", value)

    @property
    def name(self) -> str or None:
        return self._get_meta_sub("name")
    @name.setter
    def name(self, value: str):
        self._set_meta_sub("name", value)

    @property
    def relevant(self) -> str or None:
        return self._get_meta_sub("relevant")
    @relevant.setter
    def relevant(self, value: str):
        self._set_meta_sub("relevant", value)

    @property
    def ps(self):
        body = self._doc.find_kids("body")[0]
        return body.kids

    def ns(self):
        notes = self._doc.find_kids("notes")[0]
        return notes.kids


    @property
    def str(self) -> str:
        return xl.Xml(self._doc).to_str(do_pretty=True, dont_do_tags=["start", "end", "name", "mtime", "relevent", "p", "note"])


def load_from_disk(path) -> dict:
    data = {}
    entries = os.listdir(path)
    entries.sort(key=split_serial)
    for entry in entries:
        entry_path = os.path.join(path, entry)

        if os.path.isdir(entry_path):
            name = split_name(entry)
            v = load_from_disk(entry_path)

        elif os.path.isfile(entry_path):
            name = os.path.basename(entry_path)
            #name = os.path.splitext(name)[0]
            name = split_name(name)
            v = xl.parse(open(entry_path, "r").read())
        else:
            raise Exception("Unknow File: {}".format(entry_path))
        print(name)
        data[name] = v
    return data


def write_to_disk(path, data: dict, delete_existed=False):
    if os.path.exists(path) and delete_existed is True:
        shutil.rmtree(path)
    os.makedirs(path)
    for i, (k, v) in enumerate(data.items(), 1):
        name = "{:0>4}_{}".format(i, k)
        sub_path = os.path.join(path, name)
        if isinstance(v, dict):
            write_to_disk(sub_path, v)
        elif isinstance(v, xl.Xml):
            s = v.to_str(do_pretty=True, try_self_closing=True, dont_do_tags=["start", "end", "name", "mtime", "relevent", "p", "note"])
            with open(sub_path + ".xml", "w") as f:
                f.write(s)
