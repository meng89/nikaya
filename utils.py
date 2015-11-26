import bs4
import requests


class AnalyseError(Exception):
    pass


def read_text(url):
    soup, last_modified = url_to_soup(url)

    chinese_doc = soup.find('div', {'class': 'nikaya'})
    pali_doc = soup.find('div', {'class': 'pali'})

    return chinese_doc.text, pali_doc.text, last_modified


def url_to_soup(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    last_modified = r.headers['last-modified']
    soup = bs4.BeautifulSoup(r.text, 'html5lib')
    return soup, last_modified
