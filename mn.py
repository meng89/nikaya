import make_books
import utils


def make_tree(toc):  # private
    tree = []

    last_pian_title = None

    for content in toc:
        chinese, pali, last_modified = utils.read_text(content['url'])
        head_lines, main_lines = make_books.split_chinese_lines(chinese)

        info = make_books.analyse_head_lines(head_lines)
        pian = None

        last_pian_title = info['pian_title'] if 'pian_title' in info.keys() else last_pian_title

        for one in tree:
            if one['title'] == last_pian_title:
                pian = one

        if not pian:
            pian = {'title': last_pian_title, 'pins': []}
            tree.append(pian)

        pin = None
        if pian['pins'] and pian['pins'][-1]['title'] == info['pin_title']:
            pin = pian['pins'][-1]
        if not pin:
            pin = {'title': info['pin_title'], 'sutras': []}
            pian['pins'].append(pin)

        sutra = {'no_start': content['sutra_no_start'],
                 'no_end': content['sutra_no_end'],
                 'title': info['sutra_title'],
                 'head_lines': head_lines,
                 'main_lines': main_lines,
                 'pali': pali,
                 'last_modified': last_modified}

        pin['sutras'].append(sutra)

    return tree


def get_pages(tree):  # private

    pages = []

    for pian in tree:
        toc_pian_part = '{} ({}-{})'.format(pian['title'],
                                            pian['pins'][0]['sutras'][0]['no_start'],
                                            pian['pins'][-1]['sutras'][-1]['no_end']
                                            )
        for pin in pian['pins']:
            toc_pin_part = '{} ({}-{})'.format(pin['title'],
                                               pin['sutras'][0]['no_start'],
                                               pin['sutras'][-1]['no_end']
                                               )
            for sutra in pin['sutras']:
                full_serial = 'MN.{}'.format(sutra['no_start'])

                toc_sutra_part = '{} {}'.format(sutra['no_start'], sutra['title'])

                expected_path = 'Sutras/{}.xhtml'.format(full_serial)

                toc = (toc_pian_part, toc_pin_part, toc_sutra_part)

                pages.append({'head_title': sutra['title'],
                              'title': '{} {}'.format(full_serial, sutra['title']),
                              'head_lines': sutra['head_lines'],
                              'main_lines': sutra['main_lines'],
                              'pali': sutra['pali'],
                              'epub_expected_path': expected_path,
                              'epub_toc': toc})

    return pages
