import make_books
import utils


def make_tree(toc):
    tree = []
    last_pin_title = None
    for content in toc:

        chinese, pali, last_modified = utils.read_text(content['url'])

        head_lines, main_lines = make_books.split_chinese_lines(chinese)

        info = make_books.analyse_head_lines(head_lines)

        if 'pin_title' in info.keys():
            last_pin_title = info['pin_title']

        pin = None

        for one in tree:
            if one['title'] == last_pin_title:
                pin = one
                break
        if not pin:
            pin = {'title': last_pin_title, 'sutras': []}
            tree.append(pin)

        sutra = {'no_start': content['sutra_no_start'],
                 'no_end': content['sutra_no_end'],
                 'title': info['sutra_title'],
                 'head_lines': head_lines,
                 'main_lines': main_lines,
                 'pali': pali,
                 'last_modified': last_modified}

        pin['sutras'].append(sutra)

    return tree


def get_pages(tree):
    pages = []

    for pin in tree:
        toc_pin_part = '{} ({}-{})'.format(pin['title'], pin['sutras'][0]['no_start'], pin['sutras'][-1]['no_end'])
        for sutra in pin['sutras']:
            full_serial = 'DN.{}'.format(sutra['no_start'])
            toc_sutra_part = '{} {}'.format(sutra['no_start'], sutra['title'])

            expected_path = 'Sutras/{}.xhtml'.format(full_serial)

            toc = (toc_pin_part, toc_sutra_part)

            pages.append({'head_title': sutra['title'],
                          'title': '{} {}'.format(full_serial, sutra['title']),
                          'head_lines': sutra['head_lines'],
                          'main_lines': sutra['main_lines'],
                          'pali': sutra['pali'],
                          'last_modified': sutra['last_modified'],
                          'epub_expected_path': expected_path,
                          'epub_toc': toc})

    return pages
