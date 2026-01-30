import xl


def trans_data(data, lang):
    new_data = []
    for (file_index, start, end, name), obj in data:
        new_namegroup = (file_index, start, end, lang.c(name))
        if isinstance(obj, xl.Xml):
            new_obj = trans_xml(obj, lang)
        else:
            new_obj= trans_data(obj, lang)
        new_data.append((new_namegroup, new_obj))
    return new_data


def trans_noindex_data(data):
    new_data = []
    for (file_index, start, end, name), obj in data:
        namegroup = (start, end, name)
        if isinstance(obj, xl.Xml):
            new_data.append((namegroup, obj))
        else:
            new_data.append((namegroup, trans_noindex_data(obj)))
    return new_data


def trans_xml(xml, lang):
    root = xml.root
    new_root = trans_e(root, lang)
    new_xml = xl.Xml(new_root)
    return new_xml


def trans_e(e: xl.Element, lang):
    new_e = xl.Element(e.tag)
    for k, v in e.attrs.items():
        new_e.attrs[k] = lang.c(v)

    for sub in e.kids:
        if isinstance(sub, str):
            new_e.kids.append(lang.c(sub))
        if isinstance(sub, xl.Element):
            new_e.kids.append(trans_e(sub, lang))
    return new_e
