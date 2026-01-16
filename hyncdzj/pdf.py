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
FONT = "type-imp-myfonts.tex"
SUTTAS = "suttas.tex"


LAYOUTS = [
    "A4",
    #"19.5比9",
    #"21比9",

]
cover_size_map = {
    "A4": (2480, 3508)
}

type_map = {
    "A4": {
        "max_hanzi_in_line": 40,
        "max_line_in_page": 43,
        "topspace": "49pt", # 最边边 + top + topdistance

        "top": "45pt",
        "topdistance": "2pt",
        "header": "20pt",
        "headerdistance": "20pt",

        #"cutspace":"73pt",

        "footerdistance": "20pt",
        "footer": "20pt",
        "bottomdistance": "2pt",
        "bottom": "45pt",

        #"bottomspace": "1pt",

        "leftedge": "2pt",
        "leftedgedistance": "2pt",
        "leftmargin": "60pt",
        "leftmargindistance": "2pt",

        #"margin": "40pt",

        "backspace":"68pt", # 最边边 + all left *

        "rightmargindistance": "2pt",
        "rightmargin": "60pt",
        "rightedgedistance": "2pt",
        "rightedge": "2pt",

        #"horoffset":"30pt",
        #"veroffset":"30pt",
        #"textwidth": "200pt",
        "width": "460pt",
        "height": "745pt",
    },
}

def write_setuplayout(work_dir, layout):

    f = open(os.path.join(work_dir, "setuplayout.tex"), "w")

    d = type_map[layout]
    f.write("\n\\setuplayout[\n")
    for k, v in d.items():
        if v is None:
            continue
        f.write("  {}={},\n".format(k, v))
    f.write("]\n")


def build_pdf(full_path, data, module, lang, layout, tag, exit_after_done=False):
    work_dir = full_path + "_work"
    out_dir = full_path + "_out"
    os.makedirs(work_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    w, h = cover_size_map[layout]
    cover_image = ebook_utils.make_cover_image(module, lang, tag, w, h)

    write_main_tex(work_dir, module, lang, layout, cover_image)

    f = open(os.path.join(work_dir, SUTTAS), "w")
    write_tree(f, module, [(None, None, None, None)], data, lang, 40, 43)
    f.close()

    write_setuplayout(work_dir, layout)

    write_fontstex(work_dir)

    _write_homage(work_dir, lang)
    _write_zzsm(work_dir)

    my_env = os.environ.copy()
    if os.name == "posix":
        my_env["PATH"] = os.path.expanduser(config.CONTEXT_BIN_PATH) + ":" + my_env["PATH"]
    elif os.name == "nt":
        my_env["PATH"] = os.path.expanduser(config.CONTEXT_BIN_PATH) + ";" + my_env["PATH"]

    compile_cmd = """context --path="{}" "{}"/"{}" --mode={}""".format(work_dir, work_dir, MAIN, lang.en)

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


def write_fontstex(work_dir):
    fonttex = open(os.path.join(config.HYNCDZJ_TEX_DIR, "type-imp-myfonts.tex"), "r", encoding="utf-8").read()
    replace_map = {}
    for fontname in re.findall("file:(.*(?:ttf|otf|ttc))", fonttex):
        realfontpath = findfile(config.FONTS_DIRS, os.path.basename(fontname))
        if os.name == "nt":
            realfontpath = ntrelpath(realfontpath, work_dir)
        replace_map[fontname] = realfontpath

    for fontname, realfontpath in replace_map.items():
        fonttex = fonttex.replace(fontname, realfontpath.replace("\\", "/"))

    with open(os.path.join(work_dir, FONT), "w", encoding="utf-8") as new_fonttex_file:
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


def write_main_tex(work_dir, module, lang, size, cover_image):
    main_t = open(os.path.join(config.HYNCDZJ_TEX_DIR, MAIN), "r", encoding='utf-8').read()
    date = datetime.today().strftime('%Y-%m-%d')
    main = string.Template(main_t).substitute(
        size=size,
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


def _write_zzsm(work_dir):
    f = open(os.path.join(work_dir, "readme.tex"), "w", encoding="utf-8")
    f.write(startsec(1, "制作说明", "制作说明"))
    for line in epub.ZZSM:
        f.write(xml_to_tex([line], None, ebook_utils.Lang()))
        f.write("\n\\blank\n")
    f.write("\\page\n")
    f.write(stopsec(1))


_map = {
    1: "title",
    2: "subject",
    3: "subsubject",
    4: "subsubsubject",
    5: "subsubsubsubject",
    6: "subsubsubsubsubject",
    7: "subsubsubsubsubsubject",
    8: "subsubsubsubsubsubsubject",

}
def startsec(depth, title, bookmark, reference=None):
    s =  "\\start{}[\n".format(_map[depth])
    s += "    title={{{}}},\n".format(title or "")
    s += "    bookmark={{{}}},\n".format(bookmark)
    if reference:
        s += "    reference={{{}}},\n".format(reference)
    s += "]\n"
    return s

def stopsec(depth):
    return "\\stop{}\n\n".format(_map[depth])


def write_tree(f, module, namegroups, data, lang, max_hanzi_in_line, max_line_in_page, add_page_break=False):
    if epub.is_leaf(namegroups[-1], data):
        small_count, large_count = count_doc_size(data, max_hanzi_in_line, max_line_in_page)
        add_page_break = is_ratio_greater(large_count, small_count, 1)

    for namegroup, obj in data:
        cur_namegroups = namegroups + [namegroup]
        depth = len(cur_namegroups)

        _, _, _, mark_name, title_range, title_name = epub.make_mark_and_heading(module, cur_namegroups, obj, 1)

        if title_range is not None:
            title = "\\goto{{{}}}[url(https://suttacentral.net/{})]".format(title_range, title_range) + " " + title_name
        else:
            title = title_name

        f.write(startsec(depth, lang.c(title), lang.c(mark_name)))

        if isinstance(obj, xl.Xml):
            write_doc(f, obj, lang, add_page_break)

        else:
            assert isinstance(obj, list)
            write_tree(f, module, cur_namegroups, obj, lang, max_hanzi_in_line, max_line_in_page)

        f.write(stopsec(depth))


def write_doc(f, doc, lang, add_page_break):
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

    if add_page_break:
        f.write("\\page\n\n\n\n")


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



def count_doc_size(obj, max_hanzi_in_line, max_line_in_page, other_rate=0.5):
    small_page_count = 0
    large_page_count = 0

    for name, xml in obj:
        xml: xl.Xml
        line_count = 0
        line_count += 3 # 标题和空格
        root = xml.root
        for p in root.find_kids("p"):
            txt = utils.line_to_txt(p.kids)
            cjk_count, other_count = tag_str.count(txt.strip())
            line_count += math.ceil((cjk_count + 2 + other_count * other_rate) / max_hanzi_in_line)
        if line_count <= max_line_in_page:
            small_page_count += 1
        else:
            large_page_count += 1

    return small_page_count, large_page_count


def is_ratio_greater(num1, num2, threshold):
    try:
        if num1 / num2 > threshold:
            return True
        else:
            return False
    except ZeroDivisionError:
        return True
