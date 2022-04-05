def do_line(oline, funs, **kwargs):
    line = []
    for oe in oline:
        try:
            line.extend(_do_e(oe, funs, **kwargs))
        except TypeError:
            raise Exception((type(oe), oe))
    return line


class ElementError(Exception):
    pass


def _do_e(e, funs, **kwargs):
    for fun in funs:
        answer, x = fun(e=e, **kwargs)
        if answer:
            return x
    raise ElementError(e)
