#!/usr/bin/env python3
from html2image import Html2Image
#hti = Html2Image()
#with open('./test.html') as f:
#    hti.screenshot(f.read(), save_as='out.png')


hti = Html2Image("firefox", browser_executable="/usr/lib64/firefox")
hti.screenshot(url='https://cn.bing.com', save_as='bing.png')


cjk_table = [
    (0x2E80, 0x2EFF),
    (0x3000, 0x303f),
    (0x31c0, 0x31ef),
    (0x3300, 0x33ff),
    (0x3400, 0x4dbf),
    (0x4E00, 0x9FFF),
    (0xf900, 0xfaff),
    (0xfe30, 0xfe4f),

    (0x20000, 0x2a6df),
    (0x2a700, 0x2b73f),
    (0x2b740, 0x2b81f),
    (0x2b820, 0x2ceaf),
    (0x2ceb0, 0x2ebef),
    (0x2f800, 0x2fa1f),
    (0x30000, 0x3134f),

]

latin_table = [

]


def is_cjk(char):
    pass


def is_latin(char):
    pass


def is_tibetan(char):
    pass
