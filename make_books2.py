#!/usr/bin/env python3

import datetime
import threading
from urllib.parse import urlparse, urljoin


import jinja2
import os
import re
import uuid

import utils
from config import BOOKS_DIR

from sn2 import Nikaya
from sn2 import Sutra

homepage = 'https://meng89.github.io/nikaya'


class Content:
    def __init__(self):
        self.url = None


def get_toc(url):

    father_title = None
    father_no = None

    toc = []

    soup = utils.url_to_soup(url)[0]

    for table in soup.find_all('table')[3:]:
        all_a = table.find_all('a')

        if len(all_a) == 1:
            # 1.諸天相應(請點選經號進入)：
            # 9集(請點選經號進入)：
            m = re.match('^(\d+)\.?(\S+)\(請點選經號進入\)：$', all_a[0].text)
            if m:
                father_no = m.group(1)
                father_title = m.group(2)
            else:
                raise Exception

        elif len(all_a) > 1:
            # 跳过目录中 相应 或 集 列表
            if [a['href'].startswith('#') for a in all_a].count(True) == len(all_a):
                continue

            for a in all_a:

                # 跳过底部 目录 链接
                m = re.match('\d+(-\d+)?', a.text)
                if not m:
                    continue

                content = {}

                if urlparse(a['href']).netloc:
                    sutra_url = a['href']
                else:
                    sutra_url = urljoin(url, a['href'])

                content['url'] = sutra_url

                content['sutra_no_start'] = a.text.split('-')[0]
                content['sutra_no_end'] = a.text.split('-')[-1]

                if father_no:
                    content['father_no'] = father_no
                if father_title:
                    content['father_title'] = father_title

                print(content)
                toc.append(content)

    exit()
    return toc


def get_xhtml_str(template, head_title, title, head_lines, main_lines, pali, js_path, css_path=None):

    sutra_xhtml_str = template.render(head_title=head_title,
                                      title=title,
                                      js_path=js_path,
                                      css_path=css_path or '',
                                      chinese_head='\n'.join(['<p>'+l+'</p>' for l in head_lines if l.strip()]),
                                      chinese_main='\n'.join(['<p>'+l+'</p>' for l in main_lines if l.strip()]),
                                      pali='\n'.join(['<p>'+l+'</p>' for l in pali.strip().splitlines() if l.strip()])
                                      )
    return sutra_xhtml_str


def make_book(nikaya):
    """

    :param nikaya:
     :type nikaya: Nikaya
    :return:
    """
    from epubuilder.epub3 import Epub3, Section
    from epubuilder.public.metas import Language, Title, Identifier
    from epubuilder.public import File, Joint
    from epubuilder.tools import w3c_utc_date
    from epubuilder.epub3.metas import dcterms

    import epubuilder.tools

    book = Epub3()
    for lang in nikaya.languages:
        book.metadata.append(Language(lang))

    book.metadata.append(Title(nikaya.title_zh_tw))

    book.metadata.append(dcterms.get('modified')(w3c_utc_date()))

    book.metadata.append(Identifier('identifier_' + uuid.uuid4().hex))

    js_path = 'Scripts/a.js'
    book.files[js_path] = File(open('xhtml/js/a.js', 'rb').read())

    sutra_template = jinja2.Template(open('xhtml/templates/sutra.xhtml', 'r').read())

    js_relative_path = epubuilder.tools.relative_path('Pages', js_path)

    last_modified = None

    gmt_format = '%a, %d %b %Y %H:%M:%S GMT'

    def add_page_make_toc(section, subs):
        for sub in subs:

            if not isinstance(sub.title, str):
                print(sub.title)
                exit()

            s = Section(title=sub.sec_title or sub.title)

            if not isinstance(sub, Sutra):

                add_page_make_toc(section=s, subs=sub.subs)

            else:
                sutra = sub
                path = 'Pages/{}.xhtml'.format(sutra.abbreviation)
                sutra_xhtml_str = get_xhtml_str(sutra_template,
                                                sutra.abbreviation + ' ' + sutra.title,
                                                sutra.abbreviation + ' ' + sutra.title,
                                                sutra.header_lines,
                                                sutra.main_lines,
                                                sutra.pali, js_relative_path)

                book.files[path] = File(sutra_xhtml_str.encode())
                book.spine.append(Joint(path))

                s.href = path

                sutra_modified = datetime.datetime.strptime(sutra.modified, gmt_format)

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
    introduction = introduction_template.render(homepage=homepage,
                                                modified_time=last_modified.strftime('%Y-%m-%d'),
                                                created_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
    introduction_path = 'introduction.xhtml'
    book.files[introduction_path] = File(introduction.encode())

    book.toc.append(Section(title='说明', href=introduction_path))
    book.spine.append(Joint(introduction_path))

    return book, nikaya.title_zh_tw


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
    os.makedirs(BOOKS_DIR, exist_ok=True)

    _host = '127.0.0.1'
    _port = 1080

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

    import sn2

    for module, uri in ((sn2, url_part + '/SN/index.htm'),):
        nikaya = module.get_nikaya(uri)
        book, title_zh_tw = make_book(nikaya)

        book.write('{}/{}_e3.epub'.format(BOOKS_DIR, title_zh_tw))

    exit()

if __name__ == '__main__':
    main()
