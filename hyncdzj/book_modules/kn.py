from hyncdzj import base
import make_ebooks



author_set = set()
for _m in _ms:
    author_set.update(_m.info.translators)

info = base.Info(None, "小部", tuple(author_set), "KN")


def get_book():
    d = base.Dir()
    for m in _ms:
        book = make_ebooks.load_book_from_dir(m)
        d.list.append((m.info.name, book))
    return d
