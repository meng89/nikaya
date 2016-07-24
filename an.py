
import tools
import utils


def make_tree(toc):
    tree = []

    last_ji_no = None
    last_ji_title = None

    last_pin_title = None

    for content in toc:

        chinese, pali, last_modified = utils.read_text(content['url'])

        head_lines, main_lines = tools.split_chinese_lines(chinese)

        info = tools.analyse_head_lines(head_lines)

        if 'father_title' in content.keys():
            last_ji_title = content['father_title']
        if 'father_no' in content.keys():
            last_ji_no = content['father_no']

        ji = None
        if tree and tree[-1]['no'] == last_ji_no:
            ji = tree[-1]
        if not ji:
            ji = {'title': last_ji_title, 'no': last_ji_no, 'pins': []}
            tree.append(ji)
            last_pin_title = '(未分品)'  # 新集，新品

        if 'pin_title' in info.keys():
            last_pin_title = info['pin_title']

        pin = None
        if ji['pins'] and ji['pins'][-1]['title'] == last_pin_title:
            pin = ji['pins'][-1]
        if not pin:
            pin = {'title': info['pin_title'], 'sutras': []}
            ji['pins'].append(pin)

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

    for ji in tree:
        toc_ji_part = '{} {}'.format(ji['no'], ji['title'])

        for pin in ji['pins']:
            toc_pin_part = '{} ({}-{})'.format(pin['title'],
                                               pin['sutras'][0]['no_start'],
                                               pin['sutras'][-1]['no_end'])

            for sutra in pin['sutras']:

                sutra_no = sutra['no_start']
                if sutra['no_start'] != sutra['no_end']:
                    sutra_no += '-' + sutra['no_end']

                toc_sutra_part = sutra_no
                if sutra['title']:
                    toc_sutra_part += ' ' + sutra['title']

                toc = (toc_ji_part, toc_pin_part, toc_sutra_part)

                full_serial = 'AN.{}.{}'.format(ji['no'], sutra_no)

                expected_path = 'Sutras/{}.xhtml'.format(full_serial)

                pages.append({'head_title': sutra['title'],
                              'title': '{} {}'.format(full_serial, sutra['title']),
                              'head_lines': sutra['head_lines'],
                              'main_lines': sutra['main_lines'],
                              'pali': sutra['pali'],
                              'last_modified': sutra['last_modified'],
                              'epub_expected_path': expected_path,
                              'epub_toc': toc})
    return pages
