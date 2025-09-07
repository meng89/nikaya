import typing

import xl

import pyabo


def build_pdf(data, module, lang):
    _make_sutta()



def _make_suttas(file: typing.TextIO, data, module, lang):
    for name, obj in data:
        if isinstance(obj, list):
            _make_suttas(file, obj, module, lang)
        else:
            _make_sutta(file, obj, module, lang)


def _make_sutta(file: typing.TextIO, obj, module, lang):
    xml_body = obj.root.find_descendants("body")[0]
    for xml_p in xml_body.find_descendants("p"):
        file.write(_xml_to_tex(bns, xml_p.kids, obj.root, ln, gn, doc_path, lang))




def _xml_to_tex(bns, es, root, ln, gn, doc_path, lang):
    s = ""
    for x in es:
        if isinstance(x, str):
            

        elif isinstance(x, xl.Element):
            if x.tag == "ln":

            elif x.tag == "gn":
