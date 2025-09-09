import typing
import re
import os
import string

from datetime import datetime

import urllib.parse

import xl

import config

from . import epub, note, ebook_utils

main_filename = "main.tex"
suttas_filename = "suttas.tex"
localnotes_filename = "localnotes.tex"
globalnotes_filename = "globalnotes.tex"
fonttex_filename = "type-imp-myfonts.tex"
creator_note_filename = "creator_note.tex"
read_note_filename = "read_note.tex"

paper_map = {
    "A4": (2480, 3508)
}


def build_pdf(full_path, data, module, lang, size):
    bns = [module.short]
    work_dir = full_path + "_work"
    out_dir = full_path + "_out"

    branch = []
    w, h = paper_map[size]
    cover_image = ebook_utils.make_cover(module, data, lang, w, h)

    write_main(work_dir, module, bns, lang, size, cover_image)

    f = open(os.path.join(work_dir, "suttas.tex"), "w", encoding="utf-8")
    _make_suttas(f, data, branch, bns, lang)
    f.close()

    write_fanli(work_dir)
    write_zzsm(work_dir)


def write_fontstex(work_dir, fonts_dir):
    fonttex = open(os.path.join(config.TEX_DIR, "type-imp-myfonts.tex"), "r", encoding="utf-8").read()
    replace_map = {}
    for fontname in re.findall("file:(.*(?:ttf|otf))", fonttex):
        realfontpath = findfile(fonts_dir, os.path.basename(fontname))
        if os.name == "nt":
            realfontpath = ntrelpath(realfontpath, work_dir)
        replace_map[fontname] = realfontpath

    for fontname, realfontpath in replace_map.items():
        fonttex = fonttex.replace(fontname, realfontpath.replace("\\", "/"))

    with open(os.path.join(work_dir, fonttex_filename), "w", encoding="utf-8") as new_fonttex_file:
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
    main_t = open(os.path.join(config.TEX_DIR, main_filename), "r", encoding='utf-8').read()
    date = datetime.today().strftime('%Y-%m-%d')
    main = string.Template(main_t).substitute(
        size=size,
        title=lang.c(module.name_han),
        author="莊春江" + lang.c("譯"),
        keyword=lang.c("上座部佛教、南傳佛教、經藏、尼柯耶、" + module.name_han),
        date=date,

        cover_image=cover_image,
        suttas=suttas_filename,
        homage=lang.c("對那位世尊、阿羅漢、遍正覺者禮敬"),
    )
    f = open(os.path.join(work_dir, main_filename), "w", encoding="utf-8")
    f.write(main)


def write_fanli(work_dir):
    f = open(os.path.join(work_dir, "fanli.tex"), "w", encoding="utf-8")
    f.write("\\startReadme")
    for line in epub.FANLI:
        f.write(line)
        f.write("\\blank")
    f.write("\\endReadme")


def write_zzsm(work_dir):
    f = open(os.path.join(work_dir, "readme.tex"), "w", encoding="utf-8")
    f.write("\\startReadme")
    for line in epub.ZZSM:
        f.write(_xml_to_tex([], line, ebook_utils.Lang()))
        f.write("\\blank\n")
    f.write("\\startReadme")


def _make_suttas(f, data, branch, bns, lang):
    for name, obj in data:
        new_branch = branch + [name]
        if isinstance(obj, list):
            _make_suttas(f, obj, new_branch, bns, lang)
        else:
            _make_sutta(f, obj, new_branch, bns, lang)

    if epub.is_leaf(data):
        f.write("\\page")


def _make_sutta(file: typing.TextIO, obj, branch, bns, lang):
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
    for node in branch[0, -1]:
        m = re.match(r"^\d+\.(.+)$", node)
        if m:
            serialized_nodes.append(m.group(1))
    assert len(serialized_nodes) <= 1

    if serialized_nodes:
        name = "{}/{}".format(serialized_nodes[0], branch[-1])
    else:
        name = branch[-1]
    if name is not None:
        name = "\\goto{{{}}}[url()]".format(name,
                                            urllib.parse.urljoin(config.ABO_WEBSITE, epub.get_source_page(obj.root)))

    #file.write("\\startcenter")

    file.write("\\subsubsubject{")

    if num:
        file.write(num)
        file.write(" ")
    file.write(name)

    file.write("}")
    #file.write("\\endcenter")

    xml_body = obj.root.find_descendants("body")[0]
    for xml_p in xml_body.find_descendants("p"):
        file.write(_xml_to_tex(bns, xml_p.kids, lang, obj.root))
        file.write("\n\n")


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
