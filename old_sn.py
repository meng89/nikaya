#!/bin/env python3

import re
import sys
from urllib.parse import urlparse, urljoin

import jinja2

import utils
from utils import get_child_by_name

sys.path.append('/media/data/mine/projects/epubuilder')
import epubuilder


def get_chapters(url):

    chapters = []

    soup = utils.url_to_soup(url)[0]

    father_title = None
    for table in soup.find_all('table')[4:]:
        all_a = table.find_all('a')
        if len(all_a) == 1:
            father_title = re.sub('\(.*?\)：', '', all_a[0].text)
        else:
            for a in all_a:
                if not re.match('\d+(-\d+)?', a.text):
                    continue

                chapter = {}

                if urlparse(a['href']).netloc:
                    text_url = a['href']
                else:
                    text_url = urljoin(url, a['href'])

                toc = [a.text]
                if father_title:
                    toc.insert(0, father_title)
                chapter['toc'] = toc

                text_chinese, text_pali, last_modified = utils.read_text(text_url)
                chapter['chinese'] = text_chinese.strip()
                chapter['pali'] = text_pali.strip()
                chapter['last_modified'] = last_modified

                chapters.append(chapter)

    return chapters


def analyse_text(chinese):
    lines = [line.rstrip() for line in chinese.split('\n')]

    chinese_head_lines = []
    chinese_main_lines = []
    sutra_name_line = None

    if lines[0] in ('相應部48相應 83-114經', '相應部48相應 137-168經(根相應/大篇/修多羅)(莊春江譯)'):
        m = re.match('相應部\d+相應 (\d+\-\d+)經', lines[0])
        return None, None, None, None, m.group(1), lines[1:], lines[:1]

    for line in lines:
        if sutra_name_line is None:
            if re.search('\(莊春江譯\)', line):
                sutra_name_line = line
            chinese_head_lines.append(line)
        else:
            chinese_main_lines.append(line)

    if sutra_name_line is None:
        raise utils.AnalyseError('no sutra_name_lines: {}'.format(lines))

    if len(chinese_head_lines) > 6:
        raise utils.AnalyseError('head_lines > 5 : {}'.format(chinese_head_lines))

    # 篇     相应     品    经      相应号         经号
    pian, xiangying, pin, sutra, xiangying_no, sutra_no = None, None, None, None, None, None

    for line in chinese_head_lines:
        m = re.match('^(?:\(\d\))?(.*?篇)$', line)
        if m:
            pian = m.group(1)
            continue
        m = re.match('\d+[\./](?:\(\d+\))?\.?(.+相應)$', line)
        if m:
            xiangying = m.group(1)
            continue
        m = re.match('^(?:\d+\.)(.*?品)$', line)
        if m:
            pin = m.group(1)
            continue

    m = re.match('^ *相+應部?(\d+)相應 ?第?(\d+(?:\-\d+)?)經(?:/(.+?經.*?))?\((?:\S+?)相應/(?:\S+?)篇/(?:\S+?)\)', sutra_name_line)

    if not m:
        raise utils.AnalyseError("Can't analyse sutra_name_lines: {}".format(sutra_name_line))
    xiangying_no, sutra_no, sutra = m.group(1), m.group(2), m.group(3)

    print(xiangying_no, sutra_no)
    return pian, xiangying, pin, sutra, sutra_no, chinese_main_lines, chinese_head_lines


def make_tree(chapters):
    pians = []
    last_pian_name, last_xiangying_name, last_pin_name = None, None, None

    for chapter in chapters:
        pian_name, xiangying_name, pin_name, sutra_name, sutra_no,\
          chinese_main_lines, chinese_head_lines = analyse_text(chapter['chinese'])

        sutra_nos = sutra_no.split('-')
        sutra_no_start = sutra_nos[0]
        sutra_no_end = sutra_nos[-1]

        last_pian_name = pian_name or last_pian_name

        if xiangying_name:
            last_pin_name = '（未分品）'

        last_xiangying_name = xiangying_name or last_xiangying_name

        last_pin_name = pin_name or last_pin_name

        pian = get_child_by_name(last_pian_name, pians)
        if not pian:
            pian = {'name': last_pian_name, 'xiangyings': []}
            pians.append(pian)

        xiangying = get_child_by_name(last_xiangying_name, pian['xiangyings'])
        if not xiangying:
            xiangying = {'name': last_xiangying_name, 'pins': []}
            pian['xiangyings'].append(xiangying)

        if xiangying['pins'] and xiangying['pins'][-1]['name'] == last_pin_name:
            pin = xiangying['pins'][-1]
        else:
            pin = {'name': last_pin_name, 'sutras': []}
            xiangying['pins'].append(pin)

        sutra = {'name': sutra_name, 'start': sutra_no_start, 'end': sutra_no_end,
                 'chinese_main_lines': chinese_main_lines, 'chinese_head_lines': chinese_head_lines,
                 'pali': chapter['pali']}
        pin['sutras'].append(sutra)

    return pians


def make_epub(book_info, pians):

    pian_contain_xiangying_section = {}

    xiangying_qty = 0
    for pian in pians:
        pian_contain_xiangying_section[pian['name']] = (xiangying_qty + 1, xiangying_qty + len(pian['xiangyings']))
        xiangying_qty += len(pian['xiangyings'])

    book = epubuilder.EasyEpub()
    book.set_language('en-GB')
    book.set_title(book_info['title_chinese'])

    sutra_template = jinja2.Template(open('xhtml/templates/sutra.xhtml', 'r').read())

    book.add_other_file(open('xhtml/js/a.js', 'rb').read(), 'Scripts/a.js')

    xiangying_serial_no = 0
    for pian in pians:
        for xiangying in pian['xiangyings']:
            xiangying_serial_no += 1
            for pin in xiangying['pins']:

                for sutra in pin['sutras']:
                    sutra_serial_no = sutra['start'] + ('-' + sutra['end'] if sutra['end'] != sutra['start'] else '')

                    full_serial = 'SN.{}.{}'.format(xiangying_serial_no, sutra_serial_no)

                    sutra_xhtml_str = sutra_template.render(head_title=sutra['name'],
                                                            title=full_serial + ' ' + (sutra['name'] or 'none'),
                                                            js_path='../Scripts/a.js',
                                                            chinese_head='\n'.join(['<p>'+line+'</p>'for line in
                                                                                    sutra['chinese_head_lines']]),
                                                            chinese_main='\n'.join(['<p>'+line+'</p>' for line in
                                                                                    sutra['chinese_main_lines']]),
                                                            pali='\n'.join(['<p>'+line+'</p>' for line in
                                                                            sutra['pali'].split('\n')])
                                                            )

                    file_path = book.add_page(sutra_xhtml_str.encode(), 'Text/{}.xhtml'.format(full_serial))

                    toc_pian_part = '{} ({}-{})'.format(pian['name'],
                                                        pian_contain_xiangying_section[pian['name']][0],
                                                        pian_contain_xiangying_section[pian['name']][1])

                    toc_xiangying_part = '{} {}'.format(xiangying_serial_no, xiangying['name'])

                    toc_pin_part = '{} ({}-{})'.format(pin['name'], pin['sutras'][0]['start'], pin['sutras'][-1]['end'])

                    toc_sutra_part = '{} {}'.format(sutra_serial_no, sutra['name'] or 'None')

                    book.set_toc([toc_pian_part, toc_xiangying_part, toc_pin_part, toc_sutra_part], file_path)
                    print((toc_pian_part, toc_xiangying_part, toc_pin_part, toc_sutra_part), file_path)

    return book


def main():

    book_info = {'title_chinese': '相應部', 'title_pali': 'Saṃyutta Nikāya'}

    url = 'http://127.0.0.1:8866/SN/index.htm'

    chapters = get_chapters(url)
    pians = make_tree(chapters)

    book = make_epub(book_info, pians)
    book.write('built_books/sn.epub')

if __name__ == '__main__':
    main()
