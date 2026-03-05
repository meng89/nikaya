import os
import string

import selenium.webdriver

import config
from hyncdzj import book_modules
from nikaya_share import SC


_table = [
    ("「", "“"),
    ("」", "”"),
    ("『", "‘"),
    ("』", "’"),
]


def make_series(info):
    for folders, infos in book_modules.all_infos:
        if info in infos:
            return "·".join(["元亨寺　漢譯南傳大藏經"] + folders)

    return "元亨寺"
    raise Exception(info)

def xxx(info):
    name = info.name
    #if name.endswith("經"):
    #    name = name[:-1]

    if info in book_modules.jing_infos[1] or info in book_modules.xiao_infos[1] or info in book_modules.wai_infos[1]:
        background_color = "#4ea455"
        font_color = "#5F005A"
        series_font_size = "7vw"
        book_name_font_size = "20vh"
        translator_font_size = "9vh"

    elif info in book_modules.lv_infos[1]:
        background_color = "orange"
        font_color = "#073c9f"
        series_font_size = "7vw"
        book_name_font_size = "20vh"
        translator_font_size = "9vh"

    elif info in book_modules.lun_infos[1]:
        background_color = "#228fbd"
        font_color = "#5c1c01"
        series_font_size = "7vw"
        book_name_font_size = "20vh"
        translator_font_size = "9vh"

    elif info.name == "漢譯南傳大藏經":
        background_color = "white"
        font_color = "black"
        series_font_size = "7vw"
        book_name_font_size = "13vh"
        translator_font_size = "4vh"

    else:
        raise Exception(info.name)

    if info in book_modules.xiao_infos[1] or info in book_modules.wai_infos[1]:
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

    return name, background_color, font_color, book_name_font_size, book_name_space_margin, translator_font_size, series_font_size


def make_hyncdzj_cover_image(cover_dir, info, lang, tag=None, width=1600, height=2560, onebook=False):
    # translated_date = read_mtime(data)
    filename = "{}_{}_{}".format(info.name, lang.zh, today())
    xhtml_filename = filename + ".xhtml"

    image_filename = "{}_{}x{}.png".format(filename, width, height)

    os.makedirs(cover_dir, exist_ok=True)

    image_path = os.path.join(cover_dir, image_filename)

    if not os.path.exists(image_path):
        _template_str = open(os.path.join(config.RESOURCE_DIR, "hyncdzj_cover.xhtml")).read()
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

        new_name, background_color, font_color, book_name_font_size, book_name_space_margin, translator_font_size, series_font_size = xxx(info)

        dharma_wheel_path = os.path.join(config.RESOURCE_DIR, "Original_Dharma_Wheel.svg")

        doc_str = t.substitute(
            dharma_wheel_path = dharma_wheel_path,
            background_color = background_color,
            font_color = font_color,
            series_font_name = font_name,
            series_font_size = series_font_size,
            #book_name_font_name = font_name + " Heavy", # + Medium",
            book_name_font_name = book_name_font_name,
            book_name_font_size = book_name_font_size,
            book_name_space_margin = book_name_space_margin,
            translate_font_name = font_name,
            translator_font_size = translator_font_size,
            footer_font_name = font_name + " Medium",
            series = lang.c(make_series(info)),
            book_name="<span class=\"space\">&#8204;</span>".join(lang.c(new_name)),
            translator = "、".join(info.translators),
            translate = "　" + lang.c("譯"),
            footer = lang.c("基于 CBETA 資料") + "　" + footer2,
        )

        cover_xhtml_path = os.path.join(cover_dir, xhtml_filename)
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


def make_abo_cover_image(cover_dir, info, lang, width=1600, height=2560, onebook=False):
    # translated_date = read_mtime(data)
    filename = "{}_{}_{}".format(info.name, lang.zh, today())
    xhtml_filename = filename + ".xhtml"

    image_filename = "{}_{}x{}.png".format(filename, width, height)

    os.makedirs(cover_dir, exist_ok=True)

    image_path = os.path.join(cover_dir, image_filename)

    if not os.path.exists(image_path):
        _template_str = open(os.path.join(config.RESOURCE_DIR, "abo_cover.xhtml")).read()
        if isinstance(lang, SC):
            template_str = _template_str.replace("CJK TC", "CJK SC")
        else:
            template_str = _template_str

        t = string.Template(template_str)

        if len(info.name) == 2:
            # 半角：&nbsp;
            # 全角：&emsp;
            title_hant = info.name[0] + "&#160;&#160;" + info.name[1]
        else:
            title_hant = info.name

        if title_hant == "長老尼阿波陀那":
            title_hant = "長老尼<br/><nobr>阿波陀那</nobr>"
        elif title_hant == "長老阿波陀那":
            title_hant = "長&#160;&#160;老<br/><nobr>阿波陀那</nobr>"
        else:
            title_hant = "<nobr>{}</nobr>".format(title_hant)

        doc_str = t.substitute(han=lang.c(title_hant),
                               pali=info.pali,
                               version=lang.han_version,
                               translator="莊春江" + lang.c("譯"),
                               # translated=lang.c(translated_date + " 更新"),
                               created=lang.c(today() + " 製作"),
                               )

        cover_xhtml_path = os.path.join(cover_dir, xhtml_filename)
        open(cover_xhtml_path, "w").write(doc_str)

        options = selenium.webdriver.FirefoxOptions()
        options.add_argument("--headless")
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
