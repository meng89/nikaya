import typing
import re
import os
import string

from datetime import datetime

import urllib.parse

import xl

import config
import pyabo

from . import epub, note

main_filename = "main.tex"
suttas_filename = "suttas.tex"
localnotes_filename = "localnotes.tex"
globalnotes_filename = "globalnotes.tex"
fonttex_filename = "type-imp-myfonts.tex"
creator_note_filename = "creator_note.tex"
read_note_filename = "read_note.tex"


def build_pdf(full_path, data, module, lang, size):
    bns = []
    sources_dir = full_path + "_work"

    with open(os.path.join(sources_dir, main_filename), "w", encoding="utf-8") as f:
        write_main(f, bns, lang, size)

    with open(os.path.join(sources_dir, suttas_filename), "w", encoding="utf-8") as f:
        branch = []
        gn = note.get_gn()
        _make_suttas(f, data, branch, bns, gn, lang)


def write_main(file: typing.TextIO, bns, lang, size):
    # homage = dopdf.join_to_tex(nikaya.homage_line, bns, c)
    main_t = open(os.path.join(config.TEX_DIR, main_filename), "r", encoding='utf-8').read()
    strdate = datetime.today().strftime('%Y-%m-%d')
    main = string.Template(main_t).substitute(
        date=strdate,
        suttas=suttas_filename,
        homage=lang.c("對那位世尊、阿羅漢、遍正覺者禮敬"),
    )
    file.write(main)

def write_fanli(file):
    for line in epub.FANLI:
        file.write(line)

def write_zzsm(file, bns, lang):
    for line in epub.ZZSM:
        file.write(_xml_to_tex(bns, line, lang))
        file.write("\\blank\n")

def _make_suttas(file: typing.TextIO, data, branch, bns, gn, lang):
    for name, obj in data:
        new_branch = branch + [name]
        if isinstance(obj, list):
            _make_suttas(file, obj, new_branch, bns, gn, lang)
        else:
            _make_sutta(file, obj, new_branch, bns, gn, lang)

    if epub.is_leaf(data):
        file.write("\\page")


def _make_sutta(file: typing.TextIO, obj, branch, bns, gn, lang):
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
