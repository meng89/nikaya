#!/bin/env python3

import os
import re
import sys
from urllib.parse import urlparse, urljoin

import jinja2

import utils

sys.path.append('/media/data/mine/projects/epubuilder')
import epubuilder


pin_title_when_none = '(未分品)'


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

                toc.append(content)

    return toc


def split_chinese_lines(chinese):
    lines = chinese.strip().splitlines()

    head_lines = []
    main_lines = []

    is_sutra_name_line_passed = False

    for line in lines:
        if is_sutra_name_line_passed:
            main_lines.append(line)
        else:
            head_lines.append(line)
            if re.search('\(莊春江譯\)', line):
                is_sutra_name_line_passed = True

            elif re.match('相應部48相應 83-114經', line):
                is_sutra_name_line_passed = True

    return head_lines, main_lines


def analyse_head_lines(lines):  # public
    # 根本五十則篇
    # 1.根本法門品

    info = {}
    for line in lines[:-1]:

        # '(1)有偈篇' SN.1.1
        m = re.match('^\((\d)\)(\S+篇)$', line)
        if m:
            info['pian_no'] = m.group(1)
            info['pian_title'] = m.group(2)
            continue

        m = re.match('^(\S+篇)$', line)
        if m:
            info['pian_title'] = m.group(1)
            continue

        m = re.match('^(\d+)\.?(\S+品)$', line)
        if m:
            info['pin_no'] = m.group(1)
            info['pin_title'] = m.group(2)
            continue

        # 长部 二、大品
        m = re.match('^\S+、(\S+品)$', line)
        if m:
            info['pin_title'] = m.group(1)

        m = re.match('\d+[\./](?:\(\d+\))?\.?(.+相應)$', line)
        if m:
            info['xiangying_title'] = m.group(1)
            continue

    # 相应部
    m = re.match('^ *相+應部?(\d+)相應 ?第?(\d+(?:\-\d+)?)經(?:/(.+?經.*?))?\((?:\S+?)相應/(?:\S+?)篇/(?:\S+?)\)', lines[-1])
    if m:
        info['xiangying_no'] = m.group(1)
        info['sutra_title'] = m.group(3)

    m = re.match('^相應部(48)相應 (83)-(114)經$', lines[-1])
    if m:
        info['xiangying_no'] = m.group(1)
        info['sutra_title'] = ''

    # 中部：
    # 中部1經/根本法門經(根本法門品[1])(莊春江譯)
    # 中部24經接力車經(譬喻品[3])(莊春江譯)
    m = re.match('^\S+?(\d+)經/?(\S+經)\((\S+品)\[(\d+)\]\)\(莊春江譯\)$', lines[-1])
    if m:
        info['sutra_title'] = m.group(2)
        info['pin_title'] = m.group(3)
        info['pin_no'] = m.group(4)

    # 长部
    # 長部14經/譬喻大經(大品[第二])(莊春江譯)
    m = re.match('^長部(\d+)經/(\S+經)\((\S+品)\[\S+\]\)\(莊春江譯\)$', lines[-1])
    if m:
        info['sutra_title'] = m.group(2)
        info['pin_title'] = m.group(3)

    # 增支部
    # 增支部1集1經(莊春江譯)
    # 增支部6集35經/明的一部分經(莊春江譯)
    m = re.match('^增支部(\d+)集(\d+(?:\-\d+)?)經(?:/?(\S+經(\S+)?|))\(莊春江譯\)$', lines[-1])
    if m:
        info['ji_no'] = m.group(1)
        info['sutra_title'] = m.group(3)
    return info


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


def make(make_tree, get_pages, url, book_info, write_path):

    sources = get_toc(url)
    tree = make_tree(sources)

    book = epubuilder.EasyEpub()

    book.set_language('zh-TW')
    book.set_title(book_info['title_chinese'])

    js_path = book.add_other_file(open('xhtml/js/a.js', 'rb').read(), 'Scripts/a.js')

    pages = get_pages(tree)
    template = jinja2.Template(open('xhtml/templates/sutra.xhtml', 'r').read())
    for page in pages:

        js_relative_path = book.relative_path(js_path, os.path.split(page['epub_expected_path'])[0])

        sutra_xhtml_str = get_xhtml_str(template, page['head_title'], page['title'], page['head_lines'],
                                        page['main_lines'],
                                        page['pali'], js_relative_path)

        page_path = book.add_page(sutra_xhtml_str.encode(), page['epub_expected_path'])
        book.set_toc(page['epub_toc'], page_path)

        print(book_info['title_chinese'], page['epub_toc'], page_path)

    book.write(write_path)


def main():
    built_books_dir = 'built_books/'
    url_part = 'http://127.0.0.1:8866'

    import sn
    import mn
    import dn
    import an

    sn_info = {'title_chinese': '相應部', 'title_pali': 'Saṃyutta Nikāya', 'url': url_part + '/SN/index.htm'}
    mn_info = {'title_chinese': '中部', 'title_pali': 'Majjhima Nikāya', 'url': url_part + '/MN/index.htm'}
    dn_info = {'title_chinese': '長部', 'title_pali': 'Digha Nikāya', 'url': url_part + '/DN/index.htm'}
    an_info = {'title_chinese': '增支部', 'title_pali': 'Aṅguttara nikāya', 'url': url_part + '/AN/index.htm'}

    for module, n_info in ((sn, sn_info), (mn, mn_info), (dn, dn_info), (an, an_info))[:]:
        make(module.make_tree, module.get_pages, n_info['url'], n_info,
             '{}/{}.epub'.format(built_books_dir, n_info['title_chinese'])
             )


if __name__ == '__main__':
    main()