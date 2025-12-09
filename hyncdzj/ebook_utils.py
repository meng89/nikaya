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



def xxx(m):
    if m in hyncdzj_book_module.jing[1] or m in hyncdzj_book_module.dh_modules or m in hyncdzj_book_module.wai[1]:
        background_color = "#20855D"
        font_color = "#5E1633"
        book_name_font_size = "18vw"

    elif m in hyncdzj_book_module.lv[1]:
        background_color = "orange"
        font_color = "#073c9f"
        book_name_font_size = "18vw"

    elif m in hyncdzj_book_module.lun[1]:
        background_color = "#263CAB"
        font_color = "#ab9526"
        book_name_font_size = "18vw"
    else:
        print("hehe:", m.info.name)
        print()
        raise Exception(m.info.name)

    if m in hyncdzj_book_module.dh_modules or m in hyncdzj_book_module.wai[1]:
        book_name_font_size = "10vw"


    book_name_latter_spacing = "0em"
    match len(m.info.name):
        case 2:
            book_name_latter_spacing = "2em"
        case 3:
            book_name_latter_spacing = "1em"
        case 4:
            book_name_latter_spacing = "0.5em"
        case _:
            book_name_latter_spacing = "0em"

    return background_color, font_color, book_name_font_size, book_name_latter_spacing





def make_cover_image(module, lang: Lang, tag=None, width=1600, height=2560):
    # translated_date = read_mtime(data)
    filename = "{}_{}_{}".format(module.info.name, lang.zh, today())
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

        footer = "基于 CBETA 數位化成果" + today() + lang.c("製")
        if tag:
            footer += " " + tag
        footer += lang.han_version

        if isinstance(lang, SC):
            font_name = "Source Han Sans CN"
        else:
            font_name = "Source Han Sans TW"

        background_color, font_color, book_name_font_size, book_name_latter_spacing = xxx(module)
        doc_str = t.substitute(
            background_color = background_color,
            font_color = font_color,
            series_font_name = font_name,
            book_name_font_name = font_name,
            book_name_font_size = book_name_font_size,
            book_name_latter_spacing = book_name_latter_spacing,
            translate_font_name = font_name,
            footer_font_name = font_name,
            series = lang.c(make_series(module)),
            book_name=module.info.name,
            translator = "、".join(module.info.translators),
            translate = lang.c("譯"),
            footer = footer,
        )

        open(os.path.join(config.HYNCDZJ_COVER_DIR, xhtml_filename), "w").write(doc_str)
        from html2image import Html2Image as HtI

        hti = HtI(browser_executable=config.BROWSER, output_path=config.HYNCDZJ_COVER_DIR, custom_flags=['--virtual-time-budget=1000'])
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
