import os
import string

import selenium.webdriver
import config

from nikaya_share import SC


def make_cover_image(cover_dir, info, lang, width=1600, height=2560, onebook=False):
    # translated_date = read_mtime(data)
    filename = "{}_{}_{}".format(info.name, lang.zh, today())
    xhtml_filename = filename + ".xhtml"

    image_filename = "{}_{}x{}.png".format(filename, width, height)

    os.makedirs(cover_dir, exist_ok=True)

    image_path = os.path.join(cover_dir, image_filename)

    if not os.path.exists(image_path):
        _template_str = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cover.xhtml")).read()
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
