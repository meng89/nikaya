from urllib.parse import urlparse, urljoin

import re

import utils


def split_chinese_lines(chinese):
    lines = chinese.strip().splitlines()

    header_lines = []
    main_lines = []

    is_sutra_name_line_passed = False

    for line in lines:

        if is_sutra_name_line_passed:

            main_lines.append(line)
        else:
            header_lines.append(line)

            if re.search('\(莊春江譯\)', line):
                is_sutra_name_line_passed = True

            elif re.match('相應部48相應 83-114經', line):
                is_sutra_name_line_passed = True

    return header_lines, main_lines


def get_sutra_urls(nikaya_url):

    sutra_urls = []

    soup = utils.url_to_soup(nikaya_url)[0]

    for table in soup.find_all('table')[3:]:
        all_a = table.find_all('a')

        if len(all_a) == 1:
            # 1.諸天相應(請點選經號進入)：
            # 9集(請點選經號進入)：
            m = re.match('^(\d+)\.?(\S+)\(請點選經號進入\)：$', all_a[0].text)
            if m:
                pass
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

                if urlparse(a['href']).netloc:
                    sutra_url = a['href']
                else:
                    sutra_url = urljoin(nikaya_url, a['href'])

                sutra_urls.append(sutra_url)

    return sutra_urls
