import make_books
import utils


def make_tree(toc):
    tree = []

    last_pian_title = None
    last_xiangying_no = None
    last_xiangying_title = None
    last_pin_title = None

    for content in toc:
        chinese, pali, last_modified = utils.read_text(content['url'])
        head_lines, main_lines = make_books.split_chinese_lines(chinese)

        info = make_books.analyse_head_lines(head_lines)

        if 'pian_title' in info.keys():
            last_pian_title = info['pian_title']

        if content['father_no'] != last_xiangying_no:
            last_xiangying_no = content['father_no']
            last_xiangying_title = content['father_title']
            last_pin_title = None

        last_pin_title = info['pin_title'] if 'pin_title' in info.keys() else last_pin_title
        if last_pin_title is None:
            last_pin_title = make_books.pin_title_when_none

        pian = None
        if tree and tree[-1]['title'] == last_pian_title:
            pian = tree[-1]
        if not pian:
            pian = {'title': last_pian_title, 'xiangyings': []}
            tree.append(pian)

        xiangying = None
        if pian['xiangyings'] and pian['xiangyings'][-1]['title'] == last_xiangying_title:
            xiangying = pian['xiangyings'][-1]
        if not xiangying:
            xiangying = {'no': content['father_no'], 'title': last_xiangying_title, 'pins': []}
            pian['xiangyings'].append(xiangying)

        pin = None
        if xiangying['pins'] and xiangying['pins'][-1]['title'] == last_pin_title:
            pin = xiangying['pins'][-1]
        if not pin:
            pin = {'title': last_pin_title, 'sutras': []}
            xiangying['pins'].append(pin)

        sutra = {'title': info['sutra_title'],
                 'no_start': content['sutra_no_start'],
                 'no_end': content['sutra_no_end'],
                 'main_lines': main_lines,
                 'head_lines': head_lines,
                 'pali': pali,
                 'last_modified': last_modified}

        pin['sutras'].append(sutra)

    return tree


def get_pages(tree):

    pages = []

    for pian in tree:
        toc_pian_part = '{} ({}-{})'.format(pian['title'], pian['xiangyings'][0]['no'], pian['xiangyings'][-1]['no'])

        for xiangying in pian['xiangyings']:
            toc_xiangying_part = '{} {}'.format(xiangying['no'], xiangying['title'])

            for pin in xiangying['pins']:
                toc_pin_part = '{} ({}-{})'.format(pin['title'],
                                                   pin['sutras'][0]['no_start'],
                                                   pin['sutras'][-1]['no_end'])

                for sutra in pin['sutras']:
                    if sutra['no_start'] == sutra['no_end']:
                        sutra_no = sutra['no_start']
                    else:
                        sutra_no = '{}-{}'.format(sutra['no_start'], sutra['no_end'])

                    toc_sutra_part = '{} {}'.format(sutra_no, sutra['title'] or '')

                    full_serial = 'SN.{}.{}'.format(xiangying['no'], sutra_no)

                    expected_path = 'Sutras/{}.xhtml'.format(full_serial)

                    toc = (toc_pian_part, toc_xiangying_part, toc_pin_part, toc_sutra_part)

                    pages.append({'head_title': sutra['title'],
                                  'title': '{} {}'.format(full_serial, sutra['title']),
                                  'head_lines': sutra['head_lines'],
                                  'main_lines': sutra['main_lines'],
                                  'pali': sutra['pali'],
                                  'epub_expected_path': expected_path,
                                  'epub_toc': toc})

    return pages
