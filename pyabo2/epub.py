import epubpacker


def make_epub(data, module, trans):
    epub = epubpacker.Epub()
    for name, obj in data:
