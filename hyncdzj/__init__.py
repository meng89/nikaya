import xl


def trans_data(data, f):
    new_data = []
    for (start, end, name), obj in data:
        new_namegroup = (start, end, f(name))
        if isinstance(obj, list):
            new_obj = trans_data(obj, f)
        else:
            new_obj = trans_e(obj, f)

        new_data.append((new_namegroup, new_obj))
    return new_data


def trans_e(e: xl.Element, f):
    new_e = xl.Element(e.tag)
    for k, v in e.attrs.items():
        new_e.attrs[k] = f(v)

    for sub in e.kids:
        if isinstance(sub, str):
            new_e.kids.append(f(sub))
        if isinstance(sub, xl.Element):
            new_e.kids.append(trans_e(sub, f))
    return new_e


def trans_es(es:list, f):
    new_es = []
    for e in es:
        if isinstance(e, str):
            new_es.append(f(e))
        elif isinstance(e, xl.Element):
            new_es.append(trans_e(e, f))
        else:
            raise Exception(e)
    return new_es