import re

from urllib.parse import urlparse, urljoin


import utils
import tools


class Link:
    pass


def get_sutra_urls(nikaya_url):

    father_title = None
    father_no = None

    toc = []

    sutra_urls = []

    soup = utils.url_to_soup(nikaya_url)[0]

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
                    sutra_url = urljoin(nikaya_url, a['href'])

                sutra_urls.append(sutra_url)

                content['url'] = sutra_url

                content['sutra_no_start'] = a.text.split('-')[0]
                content['sutra_no_end'] = a.text.split('-')[-1]

                if father_no:
                    content['father_no'] = father_no
                if father_title:
                    content['father_title'] = father_title

                print(content)
                toc.append(content)

    return sutra_urls
    # return toc


class Nikaya:
    def __init__(self):
        self.languages = ['zh-tw', 'pali']
        self.title_zh_tw = None
        self.title_pali = None

        self.subs = []

    @property
    def pians(self):
        return self.subs


class Node:
    def __init__(self):
        self.title = None
        self.serial = None
        self.subs = []


class Pian(Node):
    @property
    def xiangyings(self):
        return self.subs


class XiangYing(Node):
    @property
    def pins(self):
        return self.subs


class Pin(Node):
    @property
    def sutras(self):
        return self.subs


class Sutra:
    def __init__(self):
        self.title = None
        self.serial_start = None
        self.serial_end = None

        self.header_lines = None
        self.main_lines = None
        self.pali = None

        self.sutra_tw = None
        self.sutra_bali = None
        self.sutra_cn = None

        self.sort_name = None



class Info:
    def __init__(self):
        self.pian_serial = None
        self.pian_title = None

        self.xiangying_serial = None
        self.xiangying_title = None

        self.pin_serial = None
        self.pin_title = None

        self.sutra_serial_start = None
        self.sutra_serial_end = None
        self.sutra_title = None


def analyse_header(lines):  # public
    """
    :param lines:
     :type lines: list
    :return:
    :rtype: Info
    """

    info = Info()

    for line in lines[:-1]:

        m = re.match('^\((\d)\)(\S+篇)$', line)
        if m:
            info.pian_serial = m.group(1)
            info.pian_title = m.group(2)
            continue

        m = re.match('^(\d+)\.?(\S+品)$', line)
        if m:
            info.pin_serial = m.group(1)
            info.pin_title = m.group(2)
            continue

        m = re.match('\d+[./](?:\(\d+\))?\.?(.+相應)$', line)
        if m:
            info.xiangying_title = m.group(1)
            continue

    m = re.match('^ *相+應部?(\d+)相應 ?第?(\d+(?:-\d+)?)經(?:/(.+?經.*?))?\((?:\S+?)相應/(?:\S+?)篇/(?:\S+?)\)', lines[-1])
    if m:
        info.xiangying_serial = m.group(1)
        serial = m.group(2).split('-')

        if len(serial) == 1:
            info.sutra_serial_start = serial[0]
            info.sutra_serial_end = serial[0]
        else:
            info.sutra_serial_start = serial[0]
            info.sutra_serial_end = serial[1]

        info.sutra_title = m.group(3)

    m = re.match('^相應部(48)相應 (83)-(114)經$', lines[-1])
    if m:
        info.xiangying_serial = m.group(1)
        info.sutra_title = ''

    return info


def add_title_range(nikaya):
    for pian in nikaya.pians:
        pian.title += ' ({}-{})'.format(pian.xiangyings[0].serial, pian.xiangyings[-1].serial)

        for xiangying in pian.xiangyings:
            for pin in xiangying.pins:
                pin.title += ' ({}-{})'.format(pin.sutras[0].serial_start, pin.sutras[-1].serial_end)

    return nikaya


def make_nikaya(sutra_urls):

    nikaya = Nikaya()
    nikaya.title_zh_tw = '相應部'
    nikaya.title_pali = 'Saṃyutta Nikāya',

    for url in sutra_urls:

        chinese, pali, last_modified = utils.read_text(url)

        header_lines, main_lines = tools.split_chinese_lines(chinese)

        info = analyse_header(header_lines)

        if info.pian_serial is not None:
            if not nikaya.subs or nikaya.subs[-1].serial != info.pian_serial:
                pian = Node()
                pian.serial = info.pian_serial
                pian.title = info.pian_title

                nikaya.subs.append(pian)

        if info.xiangying_serial is not None:
            if not nikaya.subs[-1].subs or nikaya.subs[-1].subs[-1].serial != info.xiangying_serial:
                xiangying = Node()
                xiangying.serial = info.xiangying_serial
                xiangying.title = info.xiangying_title

                nikaya.subs[-1].subs.append(xiangying)

        if info.pin_serial is not None:
            if not nikaya.subs[-1].subs[-1].subs or nikaya.subs[-1].subs[-1].subs[-1].serial != info.pin_serial:
                pin = Node()
                pin.serial = info.pin_serial
                pin.title = info.pin_title

                nikaya.subs[-1].subs[-1].subs.append(pin)

        sutra = Sutra()

        sutra.title = info.sutra_title
        sutra.serial_start = info.sutra_serial_start
        sutra.serial_end = info.sutra_serial_end

        sutra.pali = pali
        sutra.header_lines = header_lines
        sutra.main_lines = main_lines

        if sutra.serial_start == sutra.serial_end:
            sutra_start_end = sutra.serial_start
        else:
            sutra_start_end = '{}-{}'.format(sutra.serial_start, sutra.serial_end)

        sutra.sort_name = 'SN.{}.{}'.format(nikaya.pians[-1].xiangyings[-1].serial, sutra_start_end)

        nikaya.subs[-1].subs[-1].subs[-1].subs.append(sutra)

    return nikaya


def get_nikaya(url):
    sutra_urls = get_sutra_urls(url)
    nikaya = make_nikaya(sutra_urls)
    nikaya = add_title_range(nikaya)
    return nikaya
