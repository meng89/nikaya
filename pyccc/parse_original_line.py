import bs4


def _do_line2(olines, funs, **kwargs):
    line = []
    for oe in olines:
        try:
            line.extend(_do_e(oe, funs, **kwargs))
        except TypeError:
            raise Exception((type(oe), oe))
    return line


def _do_line(contents, funs, **kwargs):
    line = []
    while contents:
        if isinstance(contents[0], bs4.element.Tag) and contents[0].name == "br":
            contents.pop(0)
            break
        elif contents[0] == "\n":
            contents.pop(0)
            break
        x = _do_e(contents.pop(0), funs, **kwargs)
        line.extend(x)

    return line


class ElementError(Exception):
    pass


def _do_e(e, funs, **kwargs):
    for fun in funs:
        answer, x = fun(e=e, **kwargs)
        if answer:
            return x
    raise ElementError(e)
