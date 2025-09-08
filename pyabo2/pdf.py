import typing
import re

import xl

import pyabo

from . import epub

def build_pdf(data, module, lang):
    _make_sutta()



def _make_suttas(file: typing.TextIO, data, branch, bns, gn, lang):
    for name, obj in data:
        new_branch = branch + [name]
        if isinstance(obj, list):
            _make_suttas(file, obj, new_branch, bns, gn, lang)
        else:
            _make_sutta(file, obj, new_branch, bns, gn, lang)

        if epub.is_leaf(obj):
            file.write("\\page")


def _make_sutta(file: typing.TextIO, obj, branch, bns, gn, lang):

    sutta_num_abo = epub.get_sutta_num_abo(obj.root)
    sutta_num_sc =  epub.get_sutta_num_sc(obj.root)

    if sutta_num_sc is not None:
        url = "https://suttacentral.net/" + sutta_num_sc.replace(" ","")



    xml_body = obj.root.find_descendants("body")[0]
    file.write("\\sutta_title{" +  sutta_num_abo + "}" +
               "{" + sutta_num_sc + "}" +
               "{" + title + "}")


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


    for xml_p in xml_body.find_descendants("p"):
        file.write(_xml_to_tex(bns, xml_p.kids, obj.root, gn, lang))
        file.write("\n\n")




def _xml_to_tex(bns, es, root, gn, lang):
    s = ""
    for x in es:
        if isinstance(x, str):
            s += lang.c(x)

        elif isinstance(x, xl.Element):
            if x.tag == "ln":
                s += _xml_to_tex(bns, x.kids, root, gn, lang)
                for note in root.find_descendants("notes")[0].kids:
                    if note.attrs.get("id") == x.attrs["id"]:
                        s += "\\footnote{" + _xml_to_tex(bns, note.kids, root, gn, lang) + "}"

            elif x.tag == "gn":
                s += _xml_to_tex(bns, x.kids, root, gn, lang)
                es = gn.get_es(x.attrs["id"])
                s += "\\footnote{" + _xml_to_tex(bns, es, root, gn, lang) + "}"
        else:
            print()
            print(x.to_str())
            raise Exception
    return s
