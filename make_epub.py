#!/usr/bin/env python3

import datetime
import threading
import multiprocessing

import copy

import jinja2
import os
import uuid
from opencc import convert

from user_config import EPUB_DIR

from public import Nikaya, Sutta

HOME_PAGE = 'https://meng89.github.io/nikaya'


def translate_to_zh_cn(nikaya_book):
    """
    :param nikaya_book:
     :type nikaya_book: Nikaya
    :return:
    """

    nikaya = copy.deepcopy(nikaya_book)

    nikaya.title_st = convert(nikaya.title_st)
    nikaya.languages.append('zh-cn')

    def convert_tree(subs):
        for sub in subs:

            if sub.title is not None:
                sub.title = convert(sub.title)

            if sub.sec_title is not None:
                sub.sec_title = convert(sub.sec_title)

            if isinstance(sub, Sutta):
                sub.body_lines = [convert(line) for line in sub.body_lines]

            else:
                convert_tree(sub.subs)

    convert_tree(nikaya.subs)

    return nikaya


def make_book(nikaya):
    """

    :param nikaya:
     :type nikaya: Nikaya
    :return:
    """
    from epubaker import Epub3, Section, File, Joint
    from epubaker.metas import Language, Title, Identifier, get_dcterm

    from epubaker.tools import w3c_utc_date, relative_path

    book = Epub3()
    for lang in nikaya.languages:
        book.metadata.append(Language(lang))

    book.metadata.append(Title(nikaya.title_st))

    book.metadata.append(get_dcterm('modified')(w3c_utc_date()))

    book.metadata.append(Identifier('identifier_' + uuid.uuid4().hex))

    js_path = 'Scripts/a.js'
    book.files[js_path] = File(open('xhtml/js/a.js', 'rb').read())

    sutra_template = jinja2.Template(open('xhtml/templates/sutra.xhtml', 'r').read())

    js_relative_path = relative_path('Pages', js_path)

    last_modified = None

    gmt_format = '%a, %d %b %Y %H:%M:%S GMT'

    def add_page_make_toc(section, subs):
        for sub in subs:
            if not isinstance(sub.sec_title, str):
                print(type(sub), sub.sec_title)
                exit()

            s = Section(title=sub.sec_title or sub.title)

            if not isinstance(sub, Sutta):

                add_page_make_toc(section=s, subs=sub.subs)

            else:
                sutra = sub
                path = 'Pages/{}.xhtml'.format(sutra.abbreviation)

                sutra_xhtml_str = sutra_template.render(head_title=sutra.abbreviation + ' ' + sutra.title,
                                                        title=sutra.abbreviation + ' ' + sutra.title,
                                                        main_lines=sutra.body_lines,

                                                        chinese_lines=[x for x in sutra.chinese.strip().splitlines()
                                                                       if x.strip()],

                                                        pali_lines=[x for x in sutra.pali.strip().splitlines()
                                                                    if x.strip()],

                                                        js_path=js_relative_path)

                book.files[path] = File(sutra_xhtml_str.encode())
                book.spine.append(Joint(path))

                s.href = path

                sutra_modified = datetime.datetime.strptime(sutra.last_modified, gmt_format)

                nonlocal last_modified
                if last_modified is None:
                    last_modified = sutra_modified

                if sutra_modified > last_modified:
                    last_modified = sutra_modified

            if hasattr(section, 'subs'):
                section.subs.append(s)
            else:
                section.append(s)

    add_page_make_toc(book.toc, nikaya.subs)

    introduction_template = jinja2.Template(open('xhtml/templates/说明.xhtml', 'r').read())
    introduction = introduction_template.render(homepage=HOME_PAGE,
                                                modified_time=last_modified.strftime('%Y-%m-%d'),
                                                created_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
    introduction_path = 'introduction.xhtml'
    book.files[introduction_path] = File(introduction.encode())

    book.toc.append(Section(title='说明', href=introduction_path))
    book.spine.append(Joint(introduction_path))

    return book


class RunCccThread(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self._host = host
        self._port = port

    def run(self):
        from run_ccc import app
        app.run(host=self._host, port=self._port, debug=False)


def is_socket_open(host, port):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
        s.close()
        return True
    except OSError:
        return False


def main():

    _host = '127.0.0.1'
    _port = 8088

    while True:
        if is_socket_open(_host, _port):
            break
        else:
            _port += 1

    run_ccc_thread = RunCccThread(_host, _port)
    run_ccc_thread.daemon = True
    run_ccc_thread.start()

    import time
    time.sleep(3)

    url_part = 'http://{}:{}'.format(_host, _port)

    def write_book(book_, path):
        book_.write(path)

    from pyccc import sn
    import mn
    import dn
    import an

    os.makedirs(EPUB_DIR, exist_ok=True)

    for module, uri in (
            (sn, url_part + '/SN/index.htm'), (mn, url_part + '/MN/index.htm'),
            (dn, url_part + '/DN/index.htm'), (an, url_part + '/AN/index.htm'),):

        nikaya = module.load_global(uri)

        book = make_book(nikaya)

        p1 = multiprocessing.Process(target=write_book,
                                     args=(book, '{}/{}.epub'.format(EPUB_DIR, nikaya.title_st))
                                     )
        p1.start()

        book_zh_cn = make_book(translate_to_zh_cn(nikaya))
        p2 = multiprocessing.Process(target=write_book,
                                     args=(book_zh_cn, '{}/{}_简体.epub'.format(EPUB_DIR, nikaya.title_st))
                                     )
        p2.start()

    exit()


if __name__ == '__main__':
    main()
