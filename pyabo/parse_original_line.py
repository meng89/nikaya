import bs4.element


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


def _do_e(e, funs, url_path, **kwargs):
    for fun in funs:
        answer, x = fun(e=e, url_path=url_path, **kwargs)
        if answer:
            return x
    # abo bug
    if isinstance(e, bs4.element.Tag):
        from . import page_parsing
        page_parsing.ccc_bug(page_parsing.WARNING, url_path,
                             "Element {} 不能解析".format(repr(e)))
        return [e.get_text()]
    raise ElementError((type(e), e))
