from urllib.parse import urlparse, urljoin

import re

from pyccc import page_parsing


def get_sutta_urls(nikaya_url):
    sutra_urls = []

    soup = page_parsing.read_url(nikaya_url)[0]

    for table in soup.find_all('table')[3:]:
        all_a = table.find_all('a')

        if len(all_a) == 1:
            # 1.諸天相應(請點選經號進入)：
            # 9集(請點選經號進入)：
            m = re.match("^(\\d+)\\.?(\\S+)\\(請點選經號進入\\)：$", all_a[0].text)
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
                m = re.match("\\d+(-\\d+)?", a.text)
                if not m:
                    continue

                if urlparse(a['href']).netloc:
                    sutra_url = a['href']
                else:
                    sutra_url = urljoin(nikaya_url, a['href'])

                sutra_urls.append(sutra_url)

    return sutra_urls
