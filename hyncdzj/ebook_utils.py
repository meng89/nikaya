import os
import string

import opencc

import config

import hyncdzj_book_module


_table = [
    ("「", "“"),
    ("」", "”"),
    ("『", "‘"),
    ("』", "’"),
]

class Lang:
    def c(self, s):
        return s

    @property
    def xml(self):
        return None

    @property
    def zh(self):
        return None

    @property
    def en(self):
        return None

    @property
    def han_version(self):
        return None


class TC(Lang):
    def c(self, s):
        return s

    @property
    def xml(self):
        return "zh-Hant"

    @property
    def zh(self):
        return "繁"

    @property
    def en(self):
        return "tc"

    @property
    def han_version(self):
        return "傳統中文版"


class SC(Lang):
    def __init__(self):
        self._converter = opencc.OpenCC('tw2sp.json')

    def c(self, s):
        if s:
            return self._converter.convert(s)
        else:
            return s

    @property
    def xml(self):
        return "zh-Hans"

    @property
    def zh(self):
        return "简"

    @property
    def en(self):
        return "sc"

    @property
    def han_version(self):
        return "简体版"


def make_series(module):
    for dire, ms in hyncdzj_book_module.categories:
        if module in ms:
            series = "元亨寺　漢譯南傳大藏經·" + dire
            if module in hyncdzj_book_module.dh_modules:
                series += "·小部"
            return series
    raise Exception


def make_cover_image(module, lang: Lang, version=None, width=1600, height=2560):
    # translated_date = read_mtime(data)
    filename = "{}_{}_{}".format(module.name_han, lang.zh, today())
    xhtml_filename = filename + ".xhtml"

    image_filename = "{}_{}x{}.png".format(filename, width, height)

    os.makedirs(config.HYNCDZJ_COVER_DIR, exist_ok=True)

    image_path = os.path.join(config.HYNCDZJ_COVER_DIR, image_filename)

    if not os.path.exists(image_path):
        _template_str = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cover.xhtml")).read()
        if isinstance(lang, SC):
            template_str = _template_str.replace("CJK TC", "CJK SC")
        else:
            template_str = _template_str

        t = string.Template(template_str)

        footer = "基于 CBETA 数字化成果" + today() + lang.c("製")
        if version:
            footer += " " + version
        footer += lang.han_version

        doc_str = t.substitute(
            series = lang.c(make_series),
            book_name=module.info.name,
            translator = "、".join(module.info.translators) + lang.c("譯"),
            footer = footer
        )

        open(os.path.join(config.HYNCDZJ_COVER_DIR, xhtml_filename), "w").write(doc_str)
        from html2image import Html2Image as HtI

        hti = HtI(browser_executable=config.BROWSER, output_path=config.HYNCDZJ_COVER_DIR)
                  #custom_flags=["--disable-software-rasterizer"])
        hti.screenshot(html_str=doc_str, size=(width, height), save_as=image_filename)

    return image_path


def today():
    from datetime import datetime
    import time
    return datetime.fromtimestamp(time.time()).astimezone().strftime("%Y年%m月%d日")


def read_mtime(data: list):
    from datetime import datetime
    ts = read_timestamp(data)
    return datetime.fromtimestamp(ts).astimezone().strftime("%Y年%m月%d日")


def any_min(x, y):
    if x is None:
        return y
    if y is None:
        return x
    return min(x, y)


def any_max(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return max(a, b)


def read_timestamp(data):
    import dateutil.parser
    import xl
    newest_ts = None
    for _name, obj in data:
        if isinstance(obj, list):
            newest_ts = any_max(newest_ts, read_timestamp(obj))
        elif isinstance(obj, xl.Xml):
            mtime = obj.root.find_descendants("mtime")[0]
            ts = dateutil.parser.parse(mtime.kids[0]).timestamp()
            newest_ts = any_max(newest_ts, ts)
    return newest_ts
