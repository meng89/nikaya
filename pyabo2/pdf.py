import typing
import re
import os
import string
import subprocess
import shutil
import math

from datetime import datetime
import urllib.parse

import xl

import config
from . import epub, note, ebook_utils, tag_str, utils

MAIN = "main.tex"
FONT = "type-imp-myfonts.tex"
SUTTAS = "suttas.tex"

cover_size_map = {
    "A4": (2480, 3508)
}

ELECTRONIC="E"
PAPER="P"

type_map = {
    ("A4", ELECTRONIC): {
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
    ("A4", "P"): None

}

def write_setuplayout(work_dir, size, medium):

    f = open(os.path.join(work_dir, "setuplayout.tex"), "w")

    d = type_map[(size, medium)]
    f.write("\n\\setuplayout[\n")
    for k, v in d.items():
        if v is None:
            continue
        f.write("  {}={},\n".format(k, v))
    f.write("]\n")


def build_pdf(full_path, data, module, lang, size, exit_after_done=False, medium=ELECTRONIC):
    bns = [module.short]
    work_dir = full_path + "_work"
    out_dir = full_path + "_out"
    os.makedirs(work_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    branch = []
    w, h = cover_size_map[size]
    cover_image = ebook_utils.make_cover(module, data, lang, w, h)

    write_main(work_dir, module, bns, lang, size, cover_image)

    f = open(os.path.join(work_dir, SUTTAS), "w")
    write_data(f, module.short, data, 1, branch, bns, lang)
    f.close()

    write_setuplayout(work_dir, size, medium)

    write_fontstex(work_dir)

    _write_fanli(work_dir, bns, lang)
    _write_homage(work_dir, bns, lang)
    _write_zzsm(work_dir)

    my_env = os.environ.copy()
    if os.name == "posix":
        my_env["PATH"] = os.path.expanduser(config.CONTEXT_BIN_PATH) + ":" + my_env["PATH"]
    elif os.name == "nt":
        my_env["PATH"] = os.path.expanduser(config.CONTEXT_BIN_PATH) + ";" + my_env["PATH"]

    compile_cmd = "context --path=\"{}\" \"{}\"/\"{}\" --mode={}".format(work_dir, work_dir, MAIN, lang.en)

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
    fonttex = open(os.path.join(config.TEX_DIR, "type-imp-myfonts.tex"), "r", encoding="utf-8").read()
    replace_map = {}
    for fontname in re.findall("file:(.*(?:ttf|otf))", fonttex):
        realfontpath = findfile(config.FONTS_DIR, os.path.basename(fontname))
        if os.name == "nt":
            realfontpath = ntrelpath(realfontpath, work_dir)
        replace_map[fontname] = realfontpath

    for fontname, realfontpath in replace_map.items():
        fonttex = fonttex.replace(fontname, realfontpath.replace("\\", "/"))

    with open(os.path.join(work_dir, FONT), "w", encoding="utf-8") as new_fonttex_file:
        new_fonttex_file.write(fonttex)

def findfile(start, name):
    for relpath, dirs, files in os.walk(start):
        if name in files:
            full_path = os.path.join(start, relpath, name)
            return os.path.normpath(os.path.abspath(full_path))
    raise FileNotFoundError

def ntrelpath(path1, path2):
    import ntpath
    try:
        path = ntpath.relpath(path1, ntpath.dirname(path2))
    except ValueError:
        path = path1
    return path


def write_main(work_dir, module, bns, lang, size, cover_image):

    # homage = dopdf.join_to_tex(nikaya.homage_line, bns, c)
    main_t = open(os.path.join(config.TEX_DIR, MAIN), "r", encoding='utf-8').read()
    date = datetime.today().strftime('%Y-%m-%d')
    main = string.Template(main_t).substitute(
        size=size,
        title=lang.c(module.name_han),
        author="莊春江" + lang.c("譯"),
        keyword=lang.c("上座部佛教、南傳佛教、經藏、尼柯耶、" + module.name_han),
        date=date,

        cover_image=cover_image,
        homage=lang.c("對那位世尊、阿羅漢、遍正覺者禮敬"),
    )
    f = open(os.path.join(work_dir, MAIN), "w", encoding="utf-8")
    f.write(main)

def _write_cover(work_dir, module, data, lang, size):
    w, h = cover_size_map[size]
    cover_image = ebook_utils.make_cover(module, data, lang, w, h)
    f = open(os.path.join(work_dir, "cover.tex"), "w", encoding="utf-8")
    f.write("""
    
    """)

def _write_fanli(work_dir, bns, lang):
    f = open(os.path.join(work_dir, "fanli.tex"), "w", encoding="utf-8")
    s = ""
    s += startsec(1, "凡例", "凡例")
    #f.write("\\bookmark[mylist]{fanli}\n")
    for line in epub.FANLI:
        s += _xml_to_tex(bns, line, lang)
        s += "\n\\blank\n\n"
    s += "\\page\n"
    s += stopsec(1)

    f.write(s)

def _write_homage(work_dir, bns, lang):
    f = open(os.path.join(work_dir, "homage.tex"), "w", encoding="utf-8")
    es = epub.get_homage_xml_es()

    #f.write("\\bookmark[mylist]{{{}}}\n".format(lang.c("禮敬世尊")))
    #\\bookmark[mylist]{{{}}}
    f.write("""
    \\bookmark[mylist]{{{}}}
    %\\startstandardmakeup
    \\vfill % 在内容前添加弹性空间
    \\startalignment[center]
    {{\\tfd {{{}}}}}
    \\stopalignment
    \\vfill % 在内容后添加弹性空间
    %\\stopstandardmakeup
    \\page
    """.format(lang.c("禮敬世尊"), _xml_to_tex(bns, es, lang)))


def _write_zzsm(work_dir):
    f = open(os.path.join(work_dir, "readme.tex"), "w", encoding="utf-8")
    f.write(startsec(1, "制作说明", "制作说明"))
    for line in epub.ZZSM:
        f.write(_xml_to_tex([], line, ebook_utils.Lang()))
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


def write_data(f, data_name, data, depth, parent_branch, bns, lang):
    new_branch = parent_branch + [data_name]

    add_page = False

    if epub.is_leaf(data):
        small, lage = count_suttas_size(data, 40, 43)
        add_page = is_ratio_greater(lage, small, 1)

    for name, obj in data:
        if isinstance(obj, list):
            if epub.need_attach_range(name, obj):
                start, end = epub.read_range(obj)
                bookmark = "{}({}～{})".format(name, start, end)
            else:
                bookmark = name

            f.write(startsec(depth, lang.c(name), lang.c(bookmark)))
            write_data(f, name, obj, depth + 1, new_branch, bns, lang)
            f.write(stopsec(depth))

        else:
            write_sutta(f, obj, depth, new_branch, bns, lang, add_page)


    if epub.is_leaf(data):
        pass
        #f.write("\\page\n")


def write_sutta(file: typing.TextIO, obj, depth, branch, bns, lang, add_page):
    sutta_num_abo = epub.get_sutta_num_abo(obj.root)
    sutta_num_sc = epub.get_sutta_num_sc(obj.root)
    sutta_name = epub.get_sutta_name(obj.root)

    start, end = epub.get_sutta_range(obj.root)
    if start == end:
        _range = start
    else:
        _range = "{}-{}".format(start, end)

    source_url = urllib.parse.urljoin(config.ABO_WEBSITE, epub.get_source_page(obj.root))

    if sutta_num_sc is not None:
        #url = "https://suttacentral.net/" + sutta_num_sc.replace(" ","")
        sutta_num_sc = "\\goto{{{}}}[url(https://suttacentral.net/{})]".format(sutta_num_sc,
                                                                               sutta_num_sc.replace(" ", ""))

    if sutta_num_sc and sutta_num_abo:
        num = "{}/{}".format(sutta_num_sc, sutta_num_abo)
    elif sutta_num_abo:
        num = sutta_num_abo
    elif sutta_num_sc:
        num = sutta_num_sc
    else:
        num = ""

    serialized_nodes = []
    for node in branch:
        m = re.match(r"^\d+\.(.+)$", node)
        if m:
            serialized_nodes.append(m.group(1))
    assert len(serialized_nodes) <= 1

    if serialized_nodes:
        name = "{}/{}".format(serialized_nodes[0], sutta_name)
    else:
        name = sutta_name

    tex_name = ("\\goto{{{}}}[url({})]".format(name, source_url))

    if num:
        title = num + " " + tex_name
    else:
        title = _range + "." + tex_name

    file.write(startsec(depth, lang.c(title), _range + "." + lang.c(sutta_name)))

    xml_body = obj.root.find_descendants("body")[0]
    for xml_p in xml_body.find_descendants("p"):
        file.write(_xml_to_tex(bns, xml_p.kids, lang, obj.root))
        file.write("\n\n")
    if add_page:
        file.write("\\page\n")
    file.write(stopsec(depth))


def _xml_to_tex(bns, es, lang, root=None):
    s = ""
    for x in es:
        if isinstance(x, str):
            _s = lang.c(x)
            _s = _s.replace("{", "\\{").replace("}", "\\}").replace("[", "\\[").replace("]", "\\]").replace("#", "\\#")
            s += _s

        elif isinstance(x, xl.Element):
            if x.tag == "ln":
                assert root is not None
                #s += _xml_to_tex(bns, x.kids, lang, root)
                _text = _xml_to_tex(bns, x.kids, lang, root)
                _text = lang.c(_text)
                _note = None
                for _note_e in root.find_descendants("notes")[0].kids:
                    if _note_e.attrs.get("id") == x.attrs["id"]:
                        #_note = _xml_to_tex(bns, _note_e.kids, lang, root)
                        _note = utils.line_to_txt(_note_e.kids)
                        _note = lang.c(_note)
                        #s += "\\footnote{" + _xml_to_tex(bns, _note.kids, lang, root) + "}"
                if _note:
                    s += "\\PDFhighlight[莊春江][{{{}}}]{{{}}}".format(_note, _text)
                else:
                    s += _text

            elif x.tag == "gn":
                _text = _xml_to_tex(bns, x.kids, lang, root)
                _text = lang.c(_text)
                gn = note.get_gn()
                _note = gn.get_es(x.attrs["id"])
                _note = utils.line_to_txt(_note)
                #_note = _xml_to_tex(bns, _note, lang, root)
                _note = lang.c(_note)
                #lang.c("註解")
                s += "\\PDFhighlight[莊春江][{{{}}}]{{{}}}".format(_note, _text)
            elif x.tag == "br":
                "\\par\n"
            elif x.tag == "a":
                #print(x.to_str())
                "\\goto{莊春江工作站}[url(https://agama.buddhason.org)]"
                s += "\\goto{" + _xml_to_tex(bns, x.kids, lang, root) + "}[url(" + x.attrs["href"] + ")]"

            elif x.tag == "span" and x.attrs.get("class") == "sutra_name":
                s += _xml_to_tex(bns, x.kids, lang, root)
                s += "\n\n"
            else:
                print()
                print(x.to_str())
                print()
                raise Exception
    return s


def get_max_depth(data, depth = 0):
    max_depth = 0
    for _, obj in data:
        if isinstance(obj, list):
            max_depth = max(max_depth, get_max_depth(obj, depth + 1))
    return max_depth



def count_suttas_size(obj, one_line_cjk, one_page_line, other_rate=0.5):
    small_page = 0
    large_page = 0

    for name, xml in obj:
        xml: xl.Xml
        line_count = 0
        line_count += 3 # 标题和空格
        root = xml.root
        body = root.find_kids("body")[0]
        for p in body.find_kids("p"):
            txt = utils.line_to_txt(p.kids)
            cjk_count, other_count = tag_str.count(txt.strip())
            line_count += math.ceil((cjk_count + 2 + other_count * other_rate) / one_line_cjk)
        if line_count <= one_page_line:
            small_page += 1
        else:
            large_page += 1

    return small_page, large_page


def is_ratio_greater(num1, num2, threshold):
    try:
        if num1 / num2 > threshold:
            return True
        else:
            return False
    except ZeroDivisionError:
        return True
