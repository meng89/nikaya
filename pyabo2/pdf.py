import typing

import xl

import pyabo


def build_pdf(data, module, lang):
    _make_sutta()



def _make_suttas(file: typing.TextIO, data, bns, gn, lang):
    for name, obj in data:
        if isinstance(obj, list):
            _make_suttas(file, obj, bns, gn, lang)
        else:
            _make_sutta(file, obj, bns, gn, lang)


def _make_sutta(file: typing.TextIO, obj, bns, gn, lang):
    xml_body = obj.root.find_descendants("body")[0]
    sutta_num_abo: str
    sutta_num_sc: str
    title: str
    file.write("\\sutta_title{" +  sutta_num_abo + "}" +
               "{" + sutta_num_sc + "}" +
               "{" + title + "}")


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
