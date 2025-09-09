import os
import string
import abc

import opencc

import config


def do_nothing(x):
    return x


_table = [
    ("「", "“"),
    ("」", "”"),
    ("『", "‘"),
    ("』", "’"),
]


def convert2sc(s):
    if s:
        converter = opencc.OpenCC('tw2sp.json')
        return converter.convert(s)
    else:
        return s


def convert_all(s):
    new_sc_s = ""
    for c in convert2sc(s):
        new_sc_s += _convert_punctuation(c)
    return new_sc_s


def _convert_punctuation(c):
    for tp, sp in _table:
        if tp == c:
            return sp
    return c


class Lang(abc.ABC):
    @property
    @abc.abstractmethod
    def c(self):
        pass

    @property
    @abc.abstractmethod
    def xml(self):
        pass

    @property
    @abc.abstractmethod
    def zh(self):
        pass

    @property
    @abc.abstractmethod
    def en(self):
        pass

    @property
    @abc.abstractmethod
    def han_version(self):
        pass


class TC(Lang):
    @property
    def c(self):
        return do_nothing

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
    @property
    def c(self):
        return convert2sc

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


def make_cover(module, data, lang: Lang, width=1600, height=2560):
    translated_date = read_mtime(data)
    filename = "{}_{}_{}_{}".format(module.name_han, lang.zh, translated_date, today())
    xhtml_filename = filename + ".xhtml"

    image_filename = "{}_{}x{}".format(width, height, ".png")

    os.makedirs(config.COVER_DIR, exist_ok=True)

    image_path = os.path.join(config.COVER_DIR, image_filename)

    if not os.path.exists(image_path):
        _template_str = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cover.xhtml")).read()
        if isinstance(lang, SC):
            template_str = _template_str.replace("CJK TC", "CJK SC")
        else:
            template_str = _template_str

        t = string.Template(template_str)

        if len(module.name_han) == 2:
            # 半角：&nbsp;
            # 全角：&emsp;
            title_hant = module.name_han[0] + "&nbsp;&nbsp;" + module.name_han[1]
        else:
            title_hant = module.name_han

        if title_hant == "長老尼阿波陀那":
            title_hant = "長老尼<br/><nobr>阿波陀那</nobr>"
        elif title_hant == "長老阿波陀那":
            title_hant = "長&nbsp;&nbsp;老<br/><nobr>阿波陀那</nobr>"
        else:
            title_hant = "<nobr>{}</nobr>".format(title_hant)

        doc_str = t.substitute(han=lang.c(title_hant),
                               pali=module.name_pali,
                               version=lang.han_version,
                               translator="莊春江" + lang.c("譯"),
                               translated=lang.c(translated_date + " 更新"),
                               created=lang.c(today() + " 製作"),
                               )

        open(os.path.join(config.COVER_DIR, xhtml_filename), "w").write(doc_str)
        from html2image import Html2Image as HtI

        hti = HtI(browser_executable=config.BROWSER, output_path=config.COVER_DIR)
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
