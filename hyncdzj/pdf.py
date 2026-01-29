import typing
import re
import os
import string
import subprocess
import shutil
import math

from datetime import datetime

import xl

import config
from . import epub, ebook_utils, utils
from public_modules import tag_str

MAIN = "main.tex"
SUTTAS = "suttas.tex"

layouts = {
    "A4": {
        "cover_size": (2480, 3508),
        "max_hanzi_in_line": 40,
        "max_line_in_page": 43,
    },

    "B6": {
        "cover_size": (1512, 2150),
        "max_hanzi_in_line": 28,
        "max_line_in_page": 29,
    },

    "xperia10v": {
        "cover_size": (1080, 2520),
        "max_hanzi_in_line": 29,
        "max_line_in_page": 15,
    },

    "ipad9th": {
        "cover_size": (1620, 2160),
        "max_hanzi_in_line": 29,
        "max_line_in_page": 15,
    },

    "kobo_forma": {
        "cover_size": (1440, 1920),
        "max_hanzi_in_line": 27,
        "max_line_in_page": 25,

    },

    "letter_12pt": {
        "cover_size": (2550, 3300),
        "max_hanzi_in_line": 47,
        "max_line_in_page": 43,
    },

    "letter_13pt": {
        "cover_size": (2550, 3300),
        "max_hanzi_in_line": 44,
        "max_line_in_page": 39,
    },

    "letter_14pt": {
        "cover_size": (2550, 3300),
        "max_hanzi_in_line": 41,
        "max_line_in_page": 36,
    },
    "letter_15pt": {
        "cover_size": (2550, 3300),
        "max_hanzi_in_line": 38,
        "max_line_in_page": 34,
    },
    "letter_16pt": {
        "cover_size": (2550, 3300),
        "max_hanzi_in_line": 35,
        "max_line_in_page": 32,
    },
    "letter_17pt": {
        "cover_size": (2550, 3300),
        "max_hanzi_in_line": 33,
        "max_line_in_page": 30,
    },
    "letter_18pt": {
        "cover_size": (2550, 3300),
        "max_hanzi_in_line": 31,
        "max_line_in_page": 28,
    },

    #"23in_h245mm": {
    #    "cover_size": (1440, 1920),
    #    "max_hanzi_in_line": 27,
    #    "max_line_in_page": 25,
    #},

    #"14in_h150mm": {
    #    "cover_size": (1440, 1920),
    #    "max_hanzi_in_line": 27,
    #    "max_line_in_page": 25,
    #}

}

def build_pdf(full_path, data, module, lang, layout, tag, exit_after_done=False):
    work_dir = full_path + "_work"
    out_dir = full_path + "_out"
    os.makedirs(work_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    w, h = layouts[layout]["cover_size"]
    cover_image = ebook_utils.make_cover_image(module, lang, tag, w, h)

    write_main_tex(work_dir, module, lang, layout, cover_image)

    shutil.copy(os.path.join(config.HYNCDZJ_TEX_DIR, "{}.tex".format(layout)), work_dir)

    f = open(os.path.join(work_dir, SUTTAS), "w")
    write_tree(f, module, [], data, lang, layouts[layout]["max_hanzi_in_line"], layouts[layout]["max_line_in_page"])
    f.close()

    write_fontstex(work_dir, lang)

    _write_homage(work_dir, lang)
    _write_zzsm(work_dir, lang)

    my_env = os.environ.copy()
    if os.name == "posix":
        my_env["PATH"] = os.path.expanduser(config.CONTEXT_BIN_PATH) + ":" + my_env["PATH"]
    elif os.name == "nt":
        my_env["PATH"] = os.path.expanduser(config.CONTEXT_BIN_PATH) + ";" + my_env["PATH"]
    mode_list = [layout]
    if config.DEBUG:
        mode_list.append("debug")
    modes = ",".join(mode_list)
    compile_cmd = """context --path="{}" "{}"/"{}" --mode={}""".format(work_dir, work_dir, MAIN, modes)

    stdout_file = open(os.path.join(out_dir, "cmd_stdout"), "w", encoding="utf-8")
    stderr_file = open(os.path.join(out_dir, "cmd_stderr"), "w", encoding="utf-8")

    def _run():
        #print("运行:", compile_cmd, end=" ", flush=True)
        p = subprocess.Popen(compile_cmd, cwd=out_dir, shell=True, env=my_env,
                             stdout=stdout_file, stderr=stderr_file)
        p.communicate()

        if p.returncode != 0:
            pass
            #input("出错")
        else:
            #print("完成")
            shutil.copy(os.path.join(out_dir, "main.pdf"), full_path)
            if not config.DEBUG:
                shutil.rmtree(work_dir)
                shutil.rmtree(out_dir)
        return p.returncode

    return_code = _run()
    if exit_after_done:
        exit(return_code)

    stdout_file.close()
    stderr_file.close()


def write_tree(f, module, namegroups, data: list, lang, max_hanzi_in_line, max_line_in_page, new_page=None):

    if new_page is None and maybe_sub_is_doc(data) is True:
        small_count, medium_count, large_count = count_docs_size(data, max_hanzi_in_line, max_line_in_page)
        new_page = is_ratio_greater(large_count + medium_count, small_count, 1)
        #print("here1", new_page, namegroups)

    for index, (namegroup, obj) in enumerate(data):
        if new_page is True and index > 0:
            f.write("\\page[yes]\n")

        cur_namegroups = namegroups + [namegroup]
        depth = len(cur_namegroups)

        _, _, _, mark_name, title_range, title_name = epub.make_mark_and_heading(module, cur_namegroups, obj, 1)

        if title_range is not None:
            sc_key = title_range
            #title = "\\goto{{{}}}[url(https://suttacentral.net/{})]".format(title_range, title_range) + " " + title_name
        else:
            sc_key = None
            #title = title_name

        f.write(startsec(lang, depth, lang.c(title_name), lang.c(mark_name), lang.c(title_name), sc_key))

        if isinstance(obj, xl.Xml):
            write_doc(f, obj, lang)

        else:
            assert isinstance(obj, list)
            if new_page is None:
                sub_new_page = None
            else: # subs 已经被判定为doc了，是否分页也已经决定了，所以改标志为False，防止后续被分页。
                sub_new_page = False
            #print("here2", sub_new_page)
            write_tree(f, module, cur_namegroups, obj, lang, max_hanzi_in_line, max_line_in_page, sub_new_page)

        f.write(stopsec(depth))
        if new_page is True:
            f.write("\\page[yes]\n")

    check = maybe_sub_is_doc(data)
    if check:
        f.write("\\page[yes]\n")


def write_doc(f, doc, lang):
    for e in doc.root.kids:
        if isinstance(e, xl.Element) and re.match(r"^n\d+$", e.tag):
            break

        elif isinstance(e, xl.Element) and e.tag == "sub":
            #todo
            pass

        elif isinstance(e, xl.Element) and e.tag.startswith("sub"):
            #todo
            pass

        else:
            f.write(xml_to_tex([e], doc.root, lang))


def write_fontstex(work_dir, lang):
    type_name = "type-imp-myfonts-" + lang.en + ".tex"
    fonttex = open(os.path.join(config.HYNCDZJ_TEX_DIR, type_name), "r", encoding="utf-8").read()
    replace_map = {}
    for fontname in re.findall("file:(.*(?:ttf|otf|ttc))", fonttex):
        realfontpath = findfile(config.FONTS_DIRS, os.path.basename(fontname))
        if os.name == "nt":
            realfontpath = ntrelpath(realfontpath, work_dir)
        replace_map[fontname] = realfontpath

    for fontname, realfontpath in replace_map.items():
        fonttex = fonttex.replace(fontname, realfontpath.replace("\\", "/"))

    with open(os.path.join(work_dir, type_name), "w", encoding="utf-8") as new_fonttex_file:
        new_fonttex_file.write(fonttex)

def findfile(font_dirs, name):
    for font_dir in font_dirs:
        for relpath, dirs, files in os.walk(font_dir):
            if name in files:
                full_path = os.path.join(font_dir, relpath, name)
                return os.path.normpath(os.path.abspath(full_path))
    raise FileNotFoundError

def ntrelpath(path1, path2):
    import ntpath
    try:
        path = ntpath.relpath(path1, ntpath.dirname(path2))
    except ValueError:
        path = path1
    return path


def write_main_tex(work_dir, module, lang, layout, cover_image):
    main_t = open(os.path.join(config.HYNCDZJ_TEX_DIR, MAIN), "r", encoding='utf-8').read()
    date = datetime.today().strftime('%Y-%m-%d')
    main = string.Template(main_t).substitute(
        font_type="type-imp-myfonts-sc" if isinstance(lang, ebook_utils.SC) else "type-imp-myfonts-tc",
        layout=layout+".tex",
        title=lang.c(module.info.name),
        author="、".join(module.info.translators) + lang.c("譯"),
        keyword=lang.c("上座部佛教、南傳佛教、" + module.info.name),
        date=date,
        cover_image=cover_image,
    )
    f = open(os.path.join(work_dir, MAIN), "w", encoding="utf-8")
    f.write(main)


def _write_homage(work_dir, lang):
    f = open(os.path.join(config.HYNCDZJ_TEX_DIR, "homage.tex"), "r", encoding="utf-8")
    homage_t = f.read()
    homeage = string.Template(homage_t).substitute(
        line1 = lang.c("歸命彼世尊"),
        line2 = lang.c("應供等覺者")
    )
    f.close()

    f = open(os.path.join(work_dir, "homage.tex"), "w", encoding="utf-8")
    f.write(homeage)
    f.close()


def _write_zzsm(work_dir, lang):
    f = open(os.path.join(work_dir, "readme.tex"), "w", encoding="utf-8")
    f.write(startsec(lang, 1, "制作说明", "制作说明", "制作说明"))
    for line in epub.ZZSM:
        f.write(xml_to_tex(line, None, ebook_utils.Lang()))
        f.write("\n\\blank\n")
    f.write("\\page\n")
    f.write(stopsec(1))


_map = {
    1: ("part", "\\tfd " ),
    2: ("title", "\\tfc "),
    3: ("subject", "\\tfb " ),
    4: ("subsubject", "\\tfa "),
    5: ("subsubsubject", "\\tf "),
    6: ("subsubsubsubject", "\\tfx "),
    7: ("subsubsubsubsubject", "\\tfxx "),
    8: ("subsubsubsubsubsubject", "\\tfxx "),
    9: ("subsubsubsubsubsubsubject", "\\tfxx "),
}

def startsec(lang, depth, title, bookmark, toctext, sc_key=None, abo_key=None):
    # Ugly hack to Title

    sec = _map[depth][0]
    font_size = _map[depth][1]
    s = ""
    s += "\\startalignment[center]\n"
    s += "{\\darkred\n"
    s += "\\setuphead[" + sec + "][before={\\testpage[4]\\blank[1*halfline]"

    if sc_key:
        s += "\\goto{" + font_size + sc_key + "}[url(https://suttacentral.net/"+ sc_key + ")]\\kern 0.5em"
    else:
        s += "\\strut" # 若不添加，上面的居中命令就无效了，我也不知道为什么

    s += "}]\n"

    s += "\\start" + sec + "[\n"
    s += "    title={{{}}},\n".format(title or "")
    s += "    bookmark={{{}}},\n".format(bookmark)
    s += "    list={" + (sc_key + " " if sc_key is not None else "") + toctext + "},]\n"

    if abo_key:
        s += "\\goto{(莊春江" + lang.c("譯") + ")}[url(https://suttacentral.net/" + abo_key + ")]\n"

    s += "}\n"

    s += "\\stopalignment\n"

    s += "\\blank[1*halfline]\n\n"


    return s

def stopsec(depth):
    #return ""
    return "\\stop{}\n\n".format(_map[depth][0])


def xml_to_tex(es, doc, lang):
    s = ""
    for e in es:
        if isinstance(e, str):
            _s = lang.c(e)
            _s = _s.replace("{", "\\{").replace("}", "\\}").replace("[", "\\[").replace("]", "\\]").replace("#", "\\#")
            s += _s

        elif isinstance(e, xl.Element):
            m_t = re.match(r"^t(\d+)$", e.tag)
            m_n = re.match(r"^n\d+$", e.tag)
            if m_t:
                if e.kids:
                    assert (len(e.kids) == 1 and isinstance(e.kids[0], str))
                    text = e.kids[0]
                    s += text
                n_kids = epub.get_note_by_key(doc, m_t.group(1))
                _note = es_to_text(n_kids)

                s += "\\zhfootnote{" + lang.c(_note) + "}"
                #s += "\\high{{\\tfxx \\PDFhighlight[原始注解][{{{}}}]{{{}}}}}".format(_note, text or "㊟")
                #s += "\\high{\\tfxx \\PDFhighlight[原始注解][{" + _note + "}]{" + (text or "㊟") + "}}"

            elif m_t and False:
                text = None
                if e.kids:
                    assert (len(e.kids) == 1 and isinstance(e.kids[0], str))
                    text = e.kids[0]
                n_kids = epub.get_note_by_key(doc, m_t.group(1))
                _note = es_to_text(n_kids)
                #s += "\\high{{\\tfxx \\PDFhighlight[原始注解][{{{}}}]{{{}}}}}".format(_note, text or "㊟")
                s += "\\high{\\tfxx \\PDFhighlight[原始注解][{" + _note + "}]{" + (text or "㊟") + "}}"

            elif e.tag == "p":
                s += xml_to_tex(e.kids, doc, lang)
                s += "\n\n"

            elif e.tag == "j":
                s += "\\startalignment[middle]\n"
                s += "\\startlines\n"
                for index, p in enumerate(e.kids):
                    s += "\\strut "
                    kids, delete_head, delete_tail = xxx(p.kids)
                    lltp_str = ""
                    if index == 0:
                        if "a" in e.attrs.keys():
                            lltp_str = e.attrs["a"]
                        else:
                            lltp_str = ""

                    if delete_head:
                        lltp_str += "「"

                    if lltp_str:
                        s += "\\dontleavehmode\\llap{{{}}}".format(lltp_str)
                    s += xml_to_tex(kids, doc, lang)
                    if delete_tail:
                        s += "\\rlap{{{}}}".format("」")
                    s += "\n"
                s += "\\stoplines\n"
                s += "\\stopalignment\n"

            elif m_n:
                pass

            elif e.tag == "a":
                s += "\\goto{" + xml_to_tex(e.kids, doc, lang) + "}[url(" + e.attrs["href"] + ")]"

            elif e.tag == "list":
                s += "\\startalignment[middle]\n"
                s += "\\startlines\n"
                for item in e.kids:
                    s += xml_to_tex(item.kids, doc, lang)
                    s += "\n\n"
                s += "\\stoplines\n"
                s += "\\stopalignment\n"

            else:
                raise Exception("Unknown element type: {}".format(repr(e.to_str())))
        else:
            raise Exception("Unknown element type: {}".format(repr(e.to_str())))

    return s


def es_to_text(es):
    s = ""
    for x in es:
        if isinstance(x, str):
            s += x
        elif isinstance(x, xl.Element):
            s += es_to_text(x.kids)
        else:
            raise Exception(x)
    return s


def xxx(p_kids):
    kids = []
    delete_head = False
    for index, e in enumerate(p_kids):
        if index == 0 and isinstance(e, str) and e[0] == "「":
            delete_head = True
            kids.append(e[1:])
        else:
            kids.append(e)

    if isinstance(kids[-1], str) and kids[-1][-1] == "」":
        kids[-1] = kids[-1][:-1]
        delete_tail = True
    else:
        delete_tail = False

    return  kids, delete_head, delete_tail


def get_max_depth(data, depth = 0):
    max_depth = 0
    for _, obj in data:
        if isinstance(obj, list):
            max_depth = max(max_depth, get_max_depth(obj, depth + 1))
    return max_depth


def maybe_sub_is_doc(obj:list):
    node_count = 0
    doc_count = 0
    for namegroup, sub in obj:
        if isinstance(sub, xl.Xml):
            doc_count += 1
        elif isinstance(sub, list):
            node_count += 1
        else:
            raise Exception

    if doc_count > 1:
        return True
    else:
        return False


def is_sub_doc(obj:list):
    node_count = 0
    doc_count = 0
    for namegroup, sub in obj:
        if isinstance(sub, xl.Xml):
            doc_count += 1
        elif isinstance(sub, list):
            node_count += 1
    if doc_count > 1:
        return True
    else:
        return False




def count_docs_size(obj: list, max_hanzi_in_line, max_line_in_page, other_rate=0.5):
    small_page_count = 0
    large_page_count = 0
    medium_page_count = 0


    for name, sub in obj:
        #line_count = 3 # 标题和空格
        page_line_count = 0
        line_count = 0
        if isinstance(sub, xl.Xml):
            line_count += count_xml_line(sub, max_hanzi_in_line, other_rate)
        elif isinstance(sub, list):
            line_count = count_data_line(sub, max_hanzi_in_line, other_rate)

        if line_count < max_line_in_page * 0.7:
            small_page_count += 1
        elif line_count > max_line_in_page:
            large_page_count += 1
        else:
            medium_page_count += 1
    return small_page_count, medium_page_count, large_page_count


def count_data_line(obj: list, max_hanzi_in_line, other_rate):
    line_count = 3
    for _, sub in obj:
        if isinstance(sub, list):
            line_count += count_data_line(sub, max_hanzi_in_line, other_rate)
        elif isinstance(sub, xl.Xml):
            line_count += count_xml_line(sub, max_hanzi_in_line, other_rate)
    return line_count

def count_xml_line(obj: xl.Xml, max_hanzi_in_line, other_rate):
    line_count = 3
    root = obj.root
    for p in root.find_kids("p"):
        txt = utils.line_to_txt(p.kids)
        cjk_count, other_count = tag_str.count(txt.strip())
        line_count += math.ceil((cjk_count + 2 + other_count * other_rate) / max_hanzi_in_line)
    return line_count

def is_ratio_greater(num1, num2, threshold):
    try:
        if num1 / num2 > threshold:
            return True
        else:
            return False
    except ZeroDivisionError:
        return True
