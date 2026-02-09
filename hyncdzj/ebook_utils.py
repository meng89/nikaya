import os
import string

import selenium.webdriver
import opencc

import config
from hyncdzj import book_modules


_table = [
    ("「", "“"),
    ("」", "”"),
    ("『", "‘"),
    ("』", "’"),
]

MAP = {
    "缠𦈐": "缠缚",
    "如丝之所𦈐": "如丝之所连",
    "如丝之𦈐": "如丝之连",
    "𦈐结": "连结",
    "𦈐系": "连系",
    "说之𦈐": "说之连",
    "其发𦈐而中入尸体": "其发连而中入尸体",
    "令断贪瞋痴慢见之𦈐": "令断贪瞋痴慢见之连",
    "𦈐平坦之道如竹之屈曲": "连平坦之道如竹之屈曲",
    "𦈐锁": "连锁",
    "𦈐发者": "结发者",
    "丝所𦈐": "丝所连",
    "𦈐丝": "连丝",
    "𦈐之丝": "连之丝",
    "此如𦈐索之众生": "此如连索之众生",

    "𪎊": "麨",
    "𨱎": "鍮",
    "𪸩": "辉",

    "𨅬": "躏",

    "𫟃婆": "纴婆",
    "饮𫍢": "饮饶",
    "盾𫓴": "盾矛",
    "𫘣": "悍",
    "𩙥": "颰",
    "𪡀": "嘺",

    "𫭟阇洲": "",


}
def _sc_convert(s):
    for k, v in MAP.items():
        s = s.replace(k, v)
    return s


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
            x = self._converter.convert(s)
            x = _sc_convert(x)
            return x
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
    for dire, ms in book_modules.categories:
        if module in ms:
            series = "元亨寺　漢譯南傳大藏經·" + dire
            if module in book_modules.dh_modules:
                series += "·小部"
            return series
    raise Exception



def xxx(m):
    name = m.info.name
    #if name.endswith("經"):
    #    name = name[:-1]

    if m in book_modules.jing[1] or m in book_modules.dh_modules or m in book_modules.wai[1]:
        background_color = "#4ea455"
        font_color = "#5F005A"
        book_name_font_size = "20vh"

    elif m in book_modules.lv[1]:
        background_color = "orange"
        font_color = "#073c9f"
        book_name_font_size = "20vh"

    elif m in book_modules.lun[1]:
        background_color = "#228fbd"
        font_color = "#5c1c01"
        book_name_font_size = "20vh"
    else:
        raise Exception(m.info.name)

    if m in book_modules.dh_modules or m in book_modules.wai[1]:
        background_color = "#abc476"
        font_color = "#71356c"
        book_name_font_size = "12.5vh"


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
        _template_str = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../resource/cover.xhtml")).read()
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
            book_name_font_name = "AR PL UKai CN"
        else:
            font_name = "Source Han Sans TW"
            book_name_font_name = "AR PL UKai TW"

        new_name, background_color, font_color, book_name_font_size, book_name_space_margin = xxx(module)

        dharma_wheel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "../resource/Original_Dharma_Wheel.svg")

        doc_str = t.substitute(
            dharma_wheel_path = dharma_wheel_path,
            background_color = background_color,
            font_color = font_color,
            series_font_name = font_name,
            #book_name_font_name = font_name + " Heavy", # + Medium",
            book_name_font_name = book_name_font_name,
            book_name_font_size = book_name_font_size,
            book_name_space_margin = book_name_space_margin,
            translate_font_name = font_name,
            footer_font_name = font_name + " Medium",
            series = lang.c(make_series(module)),
            book_name="<span class=\"space\">&#8204;</span>".join(lang.c(new_name)),
            translator = "、".join(module.info.translators),
            translate = "　" + lang.c("譯"),
            footer = lang.c("基于 CBETA 資料") + "　" + footer2,
        )

        cover_xhtml_path = os.path.join(config.HYNCDZJ_COVER_DIR, xhtml_filename)
        open(cover_xhtml_path, "w").write(doc_str)


        profile = selenium.webdriver.FirefoxProfile()
        profile.set_preference("app.update.auto", False)
        profile.set_preference("app.update.enabled", False)

        options = selenium.webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.profile=profile

        driver = selenium.webdriver.Firefox(options=options)
        driver.set_window_size(width, height + config.WINDOW_HEIGHT_OFFSET)
        driver.get("file://" + cover_xhtml_path)
        driver.save_screenshot(image_path)
        driver.close()
        driver.quit()
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
