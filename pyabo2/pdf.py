import typing
import re
import os
import string
import subprocess
import shutil

from datetime import datetime

import urllib.parse

import xl

import config

from . import epub, note, ebook_utils

MAIN = "main.tex"
FONT = "type-imp-myfonts.tex"
SUTTAS = "suttas.tex"

paper_map = {
    "A4": (2480, 3508)
}


def build_pdf(full_path, data, module, lang, size):
    bns = [module.short]
    work_dir = full_path + "_work"
    out_dir = full_path + "_out"
    os.makedirs(work_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    branch = []
    w, h = paper_map[size]
    cover_image = ebook_utils.make_cover(module, data, lang, w, h)

    write_main(work_dir, module, bns, lang, size, cover_image)

    f = open(os.path.join(work_dir, SUTTAS), "w")
    write_data(f, module.short, data, 1, branch, bns, lang)
    f.close()

    write_fontstex(work_dir)

    write_fanli(work_dir, bns, lang)
    write_zzsm(work_dir)

    my_env = os.environ.copy()
    if os.name == "posix":
        my_env["PATH"] = os.path.expanduser(config.CONTEXT_BIN_PATH) + ":" + my_env["PATH"]
    elif os.name == "nt":
        my_env["PATH"] = os.path.expanduser(config.CONTEXT_BIN_PATH) + ";" + my_env["PATH"]

    compile_cmd = "context --path={} {}/{} --mode={}".format(work_dir, work_dir, MAIN, lang.en)

    stdout_file = open(os.path.join(out_dir, "cmd_stdout"), "w", encoding="utf-8")
    stderr_file = open(os.path.join(out_dir, "cmd_stderr"), "w", encoding="utf-8")

    def _run():
        print("运行:", compile_cmd, end=" ", flush=True)
        p = subprocess.Popen(compile_cmd, cwd=out_dir, shell=True, env=my_env,
                             stdout=stdout_file, stderr=stderr_file)
        p.communicate()
        if p.returncode != 0:
            input("出错！")
        else:
            print("完成！")
            shutil.copy(os.path.join(work_dir, "main.pdf"), full_path)
            if not config.DEBUG:
                os.removedirs(work_dir)
                os.removedirs(out_dir)
    _run()
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
        suttas=SUTTAS,
        homage=lang.c("對那位世尊、阿羅漢、遍正覺者禮敬"),
    )
    f = open(os.path.join(work_dir, MAIN), "w", encoding="utf-8")
    f.write(main)


def write_fanli(work_dir, bns, lang):
    f = open(os.path.join(work_dir, "fanli.tex"), "w", encoding="utf-8")
    f.write(startsec(1, "凡例", "凡例"))
    for line in epub.FANLI:
        f.write(_xml_to_tex(bns, line, lang))
        f.write("\n\\blank\n\n")
    f.write(stopsec(1))


def write_zzsm(work_dir):
    f = open(os.path.join(work_dir, "readme.tex"), "w", encoding="utf-8")
    f.write(startsec(1, "制作说明", "制作说明"))
    for line in epub.ZZSM:
        f.write(_xml_to_tex([], line, ebook_utils.Lang()))
        f.write("\n\\blank\n")
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
    s += "    title={},\n".format(title)
    s += "    bookmark={},\n".format(bookmark)
    if reference:
        s += "    reference={},\n".format(reference)
    s += "]\n"
    return s

def stopsec(depth):
    return "\\stop{}\n\n".format(_map[depth])


def write_data(f, data_name, data, depth, parent_branch, bns, lang):
    new_branch = parent_branch + [data_name]

    for name, obj in data:
        if isinstance(obj, list):
            if epub.need_attach_range(name, obj):
                start, end = epub.read_range(obj)
                bookmark = "{}({}～{})".format(name, start, end)
            else:
                bookmark = name
            f.write(startsec(depth, name, bookmark))
            write_data(f, name, obj, depth + 1, new_branch, bns, lang)
            f.write(stopsec(depth))

        else:
            write_sutta(f, obj, depth + 1, new_branch, bns, lang)


    if epub.is_leaf(data):
        f.write("\\page\n")


def write_sutta(file: typing.TextIO, obj, depth, branch, bns, lang):
    sutta_num_abo = epub.get_sutta_num_abo(obj.root)
    sutta_num_sc = epub.get_sutta_num_sc(obj.root)
    sutta_name = epub.get_sutta_name(obj.root)

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

    tex_name = ("\\goto{{{}}}[url()]".format(name,
                                             urllib.parse.urljoin(config.ABO_WEBSITE, epub.get_source_page(obj.root))))

    title = num + " " + tex_name

    file.write(startsec(depth, title, tex_name))

    xml_body = obj.root.find_descendants("body")[0]
    for xml_p in xml_body.find_descendants("p"):
        file.write(_xml_to_tex(bns, xml_p.kids, lang, obj.root))
        file.write("\n\n")

    file.write(stopsec(depth))


def _xml_to_tex(bns, es, lang, root=None):
    s = ""
    for x in es:
        if isinstance(x, str):
            s += lang.c(x)

        elif isinstance(x, xl.Element):
            if x.tag == "ln":
                assert root is not None
                s += _xml_to_tex(bns, x.kids, lang, root)
                for _note in root.find_descendants("notes")[0].kids:
                    if _note.attrs.get("id") == x.attrs["id"]:
                        s += "\\footnote{" + _xml_to_tex(bns, _note.kids, lang, root) + "}"

            elif x.tag == "gn":
                s += _xml_to_tex(bns, x.kids, lang, root)
                gn = note.get_gn()
                es = gn.get_es(x.attrs["id"])
                s += "\\footnote{" + _xml_to_tex(bns, es, lang, root) + "}"
        else:
            print()
            print(x.to_str())
            raise Exception
    return s


def get_max_depth(data, depth = 0):
    max_depth = 0
    for _, obj in data:
        if isinstance(obj, list):
            max_depth = max(max_depth, get_max_depth(obj, depth + 1))
    return max_depth
