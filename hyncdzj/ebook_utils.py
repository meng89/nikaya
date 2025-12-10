import os
import string
import time

import selenium.webdriver

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
    name = m.info.name
    if name.endswith("經"):
        name = name[:-1]

    if m in hyncdzj_book_module.jing[1] or m in hyncdzj_book_module.dh_modules or m in hyncdzj_book_module.wai[1]:
        background_color = "#4ea455"
        font_color = "#5F005A"
        book_name_font_size = "30vw"

    elif m in hyncdzj_book_module.lv[1]:
        background_color = "orange"
        font_color = "#073c9f"
        book_name_font_size = "30vw"

    elif m in hyncdzj_book_module.lun[1]:
        background_color = "#228fbd"
        font_color = "#5c1c01"
        book_name_font_size = "30vw"
    else:
        raise Exception(m.info.name)

    if m in hyncdzj_book_module.dh_modules or m in hyncdzj_book_module.wai[1]:
        background_color = "#abc476"
        font_color = "#71356c"
        book_name_font_size = "20vw"


    book_name_space_margin = "0em"
    match len(name):
        case 2:
            book_name_space_margin = "0.7em"
        case 3:
            book_name_space_margin = "0.3em"
        case 4:
            book_name_space_margin = "0.1em"
        case 5:
            book_name_space_margin = "0.1em"
        case _:
            book_name_space_margin = "0em"

    return name, background_color, font_color, book_name_font_size, book_name_space_margin


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

        footer2_list = [today() + lang.c("製")]
        if tag:
            footer2_list.append(lang.c(tag))

        if isinstance(lang, SC):
            footer2_list.append("简体版")
        else:
            footer2_list.append("傳統漢字版")

        footer2 = "　".join(footer2_list)

        if isinstance(lang, SC):
            font_name = "Source Han Sans CN"
        else:
            font_name = "Source Han Sans TW"

        new_name, background_color, font_color, book_name_font_size, book_name_space_margin = xxx(module)
        doc_str = t.substitute(
            background_color = background_color,
            font_color = font_color,
            series_font_name = font_name,
            book_name_font_name = font_name + " Medium",
            book_name_font_size = book_name_font_size,
            book_name_space_margin = book_name_space_margin,
            translate_font_name = font_name,
            footer_font_name = font_name,
            series = lang.c(make_series(module)),
            book_name="<span class=\"space\">&#8204;</span>".join(lang.c(new_name)),
            translator = "、".join(module.info.translators),
            translate = "　" + lang.c("譯"),
            footer1 = lang.c("基于 CBETA 數位化成果"),
            footer2 = footer2,
        )

        cover_xhtml_path = os.path.join(config.HYNCDZJ_COVER_DIR, xhtml_filename)
        open(cover_xhtml_path, "w").write(doc_str)

        options = selenium.webdriver.FirefoxOptions()
        options.add_argument("--headless")
        #options.add_argument("--window-size=1600x2560")
        driver = selenium.webdriver.Firefox(options=options)
        driver.set_window_size(width, height + config.WINDOW_HEIGHT_OFFSET)
        driver.get("file://" + cover_xhtml_path)
        driver.save_screenshot(image_path)
        driver.close()
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
